---
title: Migrate Data to a Downstream TiDB Table with More Columns
summary: Learn how to migrate data to a downstream TiDB table with more columns than the corresponding upstream table.
---

# より多くの列を持つ下流の TiDB テーブルにデータを移行する {#migrate-data-to-a-downstream-tidb-table-with-more-columns}

このドキュメントでは、対応する上流のテーブルよりも多くの列を持つ下流の TiDB テーブルにデータを移行するときに実行する追加の手順について説明します。通常の移行手順については、次の移行シナリオを参照してください。

-   [小さなデータセットの MySQL を TiDB に移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットの MySQL を TiDB に移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## DM を使用して、より多くの列を持つ下流の TiDB テーブルにデータを移行する {#use-dm-to-migrate-data-to-a-downstream-tidb-table-with-more-columns}

アップストリームのbinlogをレプリケートするとき、DM はダウンストリームの現在のテーブル スキーマを使用してbinlogを解析し、対応する DML ステートメントを生成しようとします。アップストリームbinlogのテーブルの列番号がダウンストリーム テーブル スキーマの列番号と一致しない場合、次のエラーが発生します。

```json
"errors": [
    {
        "ErrCode": 36027,
        "ErrClass": "sync-unit",
        "ErrScope": "internal",
        "ErrLevel": "high",
        "Message": "startLocation: [position: (mysql-bin.000001, 2022), gtid-set:09bec856-ba95-11ea-850a-58f2b4af5188:1-9 ], endLocation: [ position: (mysql-bin.000001, 2022), gtid-set: 09bec856-ba95-11ea-850a-58f2b4af5188:1-9]: gen insert sqls failed, schema: log, table: messages: Column count doesn't match value count: 3 (columns) vs 2 (values)",
        "RawCause": "",
        "Workaround": ""
    }
]
```

以下は、アップストリーム テーブル スキーマの例です。

```sql
# Upstream table schema
CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
)
```

以下は、ダウンストリーム テーブル スキーマの例です。

```sql
# Downstream table schema
CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `message` varchar(255) DEFAULT NULL, # This is the additional column that only exists in the downstream table.
  PRIMARY KEY (`id`)
)
```

DM がダウンストリーム テーブル スキーマを使用して、アップストリームによって生成されたbinlogイベントを解析しようとすると、DM は上記の`Column count doesn't match`エラーを報告します。

このような場合は、 `binlog-schema`コマンドを使用して、データ ソースから移行するテーブルのテーブル スキーマを設定できます。指定されたテーブル スキーマは、DM によってレプリケートされるbinlogイベント データに対応している必要があります。シャード テーブルを移行する場合は、シャード テーブルごとに、DM でテーブル スキーマを設定してbinlogイベント データを解析する必要があります。手順は次のとおりです。

1.  DM で SQL ファイルを作成し、上流のテーブル スキーマに対応する`CREATE TABLE`ステートメントをファイルに追加します。たとえば、次のテーブル スキーマを`log.messages.sql`に保存します。 DM v6.0 以降のバージョンでは、SQL ファイルを作成せずに`--from-source`または`--from-target`フラグを追加することで、テーブル スキーマを更新できます。詳細については、 [移行するテーブルのテーブル スキーマの管理](/dm/dm-manage-schema.md)を参照してください。

    ```sql
    # Upstream table schema
    CREATE TABLE `messages` (
    `id` int(11) NOT NULL,
    PRIMARY KEY (`id`)
    )
    ```

2.  `binlog-schema`コマンドを使用して、データ ソースから移行するテーブルのテーブル スキーマを設定します。この時点で、データ移行タスクは上記`Column count doesn't match`エラーにより一時停止状態になっているはずです。

    {{< copyable "" >}}

    ```
    tiup dmctl --master-addr ${advertise-addr} binlog-schema update -s ${source-id} ${task-name} ${database-name} ${table-name} ${schema-file}
    ```

    このコマンドのパラメータの説明は次のとおりです。

    | パラメータ               | 説明                                                                                                                 |
    | :------------------ | :----------------------------------------------------------------------------------------------------------------- |
    | `-master-addr`      | dmctl が接続されるクラスター内の任意の DM マスター ノードの`${advertise-addr}`を指定します。 `${advertise-addr}` DM-master が外部にアドバタイズするアドレスを示します。 |
    | `binlog-schema set` | スキーマ情報を手動で設定します。                                                                                                   |
    | `-s`                | ソースを指定します。 `${source-id}` MySQL データのソース ID を示します。                                                                  |
    | `${task-name}`      | データ移行タスクの`task.yaml`の構成ファイルで定義されている移行タスクの名前を指定します。                                                                 |
    | `${database-name}`  | データベースを指定します。 `${database-name}`上流データベースの名前を示します。                                                                  |
    | `${table-name}`     | アップストリーム テーブルの名前を指定します。                                                                                            |
    | `${schema-file}`    | 設定するテーブルスキーマファイルを指定します。                                                                                            |

    例えば：

    {{< copyable "" >}}

    ```
    tiup dmctl --master-addr 172.16.10.71:8261 binlog-schema update -s mysql-01 task-test -d log -t message log.message.sql
    ```

3.  `resume-task`コマンドを使用して、一時停止状態の移行タスクを再開します。

    {{< copyable "" >}}

    ```
    tiup dmctl --master-addr ${advertise-addr} resume-task ${task-name}
    ```

4.  `query-status`コマンドを使用して、データ移行タスクが正しく実行されていることを確認します。

    {{< copyable "" >}}

    ```
    tiup dmctl --master-addr ${advertise-addr} query-status resume-task ${task-name}
    ```
