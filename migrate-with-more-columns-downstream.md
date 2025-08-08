---
title: Migrate Data to a Downstream TiDB Table with More Columns
summary: 対応するアップストリーム テーブルよりも多くの列を持つダウンストリーム TiDB テーブルにデータを移行する方法を学習します。
---

# より多くの列を持つ下流の TiDB テーブルにデータを移行する {#migrate-data-to-a-downstream-tidb-table-with-more-columns}

このドキュメントでは、対応する上流テーブルよりも多くの列を持つ下流TiDBテーブルにデータを移行する際に必要な追加手順について説明します。通常の移行手順については、以下の移行シナリオをご覧ください。

-   [小規模データセットをMySQLからTiDBに移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模データセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模データセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## DM を使用して、より多くの列を持つ下流の TiDB テーブルにデータを移行します。 {#use-dm-to-migrate-data-to-a-downstream-tidb-table-with-more-columns}

アップストリームのbinlogを複製する際、DMはダウンストリームの現在のテーブルスキーマを使用してbinlogを解析し、対応するDML文を生成しようとします。アップストリームのバイナリbinlog内のテーブルの列番号がダウンストリームのテーブルスキーマ内の列番号と一致しない場合、次のエラーが発生します。

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

以下はアップストリーム テーブル スキーマの例です。

```sql
# Upstream table schema
CREATE TABLE `messages` (
  `id` int NOT NULL,
  PRIMARY KEY (`id`)
)
```

以下はダウンストリーム テーブル スキーマの例です。

```sql
# Downstream table schema
CREATE TABLE `messages` (
  `id` int NOT NULL,
  `message` varchar(255) DEFAULT NULL, # This is the additional column that only exists in the downstream table.
  PRIMARY KEY (`id`)
)
```

DM がダウンストリーム テーブル スキーマを使用してアップストリームによって生成されたbinlogイベントを解析しようとすると、DM は上記の`Column count doesn't match`エラーを報告します。

このような場合、 `binlog-schema`コマンドを使用して、データソースから移行するテーブルのテーブルスキーマを設定できます。指定するテーブルスキーマは、DM によって複製されるbinlogイベントデータに対応している必要があります。シャード化されたテーブルを移行する場合は、シャード化されたテーブルごとに、binlogイベントデータを解析するためのテーブルスキーマを DM で設定する必要があります。手順は以下のとおりです。

1.  DMでSQLファイルを作成し、上流のテーブルスキーマに対応する`CREATE TABLE`ステートメントをファイルに追加します。例えば、次のテーブルスキーマを`log.messages.sql`に保存します。DM v6.0以降のバージョンでは、SQLファイルを作成せずに、 `--from-source`または`--from-target`フラグを追加することでテーブルスキーマを更新できます。詳細は[移行するテーブルのテーブルスキーマを管理する](/dm/dm-manage-schema.md)参照してください。

    ```sql
    # Upstream table schema
    CREATE TABLE `messages` (
    `id` int NOT NULL,
    PRIMARY KEY (`id`)
    )
    ```

2.  `binlog-schema`コマンドを使用して、データソースから移行するテーブルのテーブルスキーマを設定します。この時点で、データ移行タスクは上記の`Column count doesn't match`エラーにより一時停止状態になっているはずです。

        tiup dmctl --master-addr ${advertise-addr} binlog-schema update -s ${source-id} ${task-name} ${database-name} ${table-name} ${schema-file}

    このコマンドのパラメータの説明は次のとおりです。

    | パラメータ               | 説明                                                                                                               |
    | :------------------ | :--------------------------------------------------------------------------------------------------------------- |
    | `-master-addr`      | dmctl が接続されるクラスター内の任意の DM マスター ノードの`${advertise-addr}`指定します。3 `${advertise-addr}` 、DM マスターが外部にアドバタイズするアドレスを示します。 |
    | `binlog-schema set` | スキーマ情報を手動で設定します。                                                                                                 |
    | `-s`                | ソースを指定します。1 `${source-id}` MySQL データのソース ID を示します。                                                               |
    | `${task-name}`      | データ移行タスクの`task.yaml`構成ファイルで定義されている移行タスクの名前を指定します。                                                                |
    | `${database-name}`  | データベースを指定します。1 `${database-name}`アップストリーム データベースの名前を示します。                                                        |
    | `${table-name}`     | アップストリーム テーブルの名前を指定します。                                                                                          |
    | `${schema-file}`    | 設定するテーブル スキーマ ファイルを指定します。                                                                                        |

    例えば：

        tiup dmctl --master-addr 172.16.10.71:8261 binlog-schema update -s mysql-01 task-test -d log -t message log.message.sql

3.  一時停止状態の移行タスクを再開するには、 `resume-task`コマンドを使用します。

        tiup dmctl --master-addr ${advertise-addr} resume-task ${task-name}

4.  `query-status`コマンドを使用して、データ移行タスクが正しく実行されていることを確認します。

        tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
