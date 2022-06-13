---
title: Migration Task Precheck
summary: Learn the precheck that DM performs before starting a migration task.
---

# 移行タスクの事前チェック {#migration-task-precheck}

DMを使用してアップストリームからダウンストリームにデータを移行する前に、事前チェックにより、アップストリームデータベース構成のエラーを検出し、移行がスムーズに行われるようにします。このドキュメントでは、DM事前チェック機能を紹介します。これには、その使用シナリオ、チェック項目、および引数が含まれます。

## 使用シナリオ {#usage-scenario}

データ移行タスクをスムーズに実行するために、DMはタスクの開始時に事前チェックを自動的にトリガーし、チェック結果を返します。 DMは、事前チェックに合格した後にのみ移行を開始します。

事前チェックを手動でトリガーするには、 `check-task`コマンドを実行します。

例えば：

{{< copyable "" >}}

```bash
tiup dmctl check-task ./task.yaml
```

## チェック項目の説明 {#descriptions-of-check-items}

タスクの事前チェックがトリガーされた後、DMは移行モードの構成に従って対応するアイテムをチェックします。

このセクションには、すべての事前チェック項目がリストされています。

> **ノート：**
>
> このドキュメントでは、合格する必要のあるチェック項目に「（必須）」というラベルが付いています。

> -   必須のチェック項目に合格しなかった場合、DMはチェック後にエラーを返し、移行タスクを続行しません。この場合、エラーメッセージに従って構成を変更し、事前チェックの要件を満たした後でタスクを再試行してください。
>
> -   必須ではないチェック項目に合格しなかった場合、DMはチェック後に警告を返します。チェック結果に警告のみが含まれ、エラーが含まれていない場合、DMは自動的に移行タスクを開始します。

### 一般的なチェック項目 {#common-check-items}

選択した移行モードに関係なく、事前チェックには常に次の一般的なチェック項目が含まれます。

-   データベースバージョン

    -   MySQLバージョン&gt;5.5

    -   MariaDBバージョン&gt;=10.1.2

    > **警告：**
    >
    > -   DMを使用してMySQL8.0からTiDBにデータを移行することは、実験的機能です（DM v2.0以降に導入されました）。実稼働環境で使用することはお勧めしません。
    > -   DMを使用してMariaDBからTiDBにデータを移行することは、実験的機能です。実稼働環境で使用することはお勧めしません。

-   アップストリームMySQLテーブルスキーマの互換性

    -   アップストリームテーブルに、TiDBでサポートされていない外部キーがあるかどうかを確認します。事前チェックで外部キーが見つかった場合は、警告が返されます。
    -   （必須）文字セットに互換性の違いがあるかどうかを確認します。詳細については、 [TiDBがサポートする文字セット](/character-set-and-collation.md)を参照してください。
    -   （必須）アップストリームテーブルに主キー制約または一意キー制約があるかどうかを確認します（v1.0.7から導入）

### 完全なデータ移行の項目を確認してください {#check-items-for-full-data-migration}

フルデータ移行モード（ `task-mode: full` ）の場合、事前チェックには[共通のチェック項目](#common-check-items)に加えて、次のチェック項目も含まれます。

-   （必須）アップストリームデータベースのダンプ許可

    -   INFORMATION_SCHEMAおよびダンプテーブルに対するSELECT権限
    -   `consistency=flush`の場合はRELOAD権限
    -   `consistency=flush/lock`の場合、ダンプテーブルに対するLOCKTABLES権限

-   （必須）アップストリームMySQLマルチインスタンスシャーディングテーブルの一貫性

    -   ペシミスティックモードで、すべてのシャーディングされたテーブルのテーブルスキーマが次の項目で一貫しているかどうかを確認します。

        -   列の数
        -   列名
        -   列の順序
        -   列タイプ
        -   主キー
        -   一意のインデックス

    -   オプティミスティックモードで、すべてのシャードテーブルのスキーマが[楽観的な互換性](https://github.com/pingcap/tiflow/blob/master/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types)を満たしているかどうかを確認します。

    -   移行タスクが`start-task`コマンドによって正常に開始された場合、このタスクの事前チェックは整合性チェックをスキップします。

-   シャーディングされたテーブルの主キーを自動インクリメントします

    -   シャーディングされたテーブルに自動インクリメントの主キーがある場合、事前チェックは警告を返します。自動インクリメントの主キーに競合がある場合、解決策については[自動インクリメント主キーの競合を処理します](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照してください。

### 増分データ移行の項目を確認してください {#check-items-for-incremental-data-migration}

インクリメンタルデータ移行モード（ `task-mode: incremental` ）の場合、 [共通のチェック項目](#common-check-items)に加えて、事前チェックには次のチェック項目も含まれます。

-   （必須）アップストリームデータベースのREPLICATION権限

    -   レプリケーションクライアントの許可
    -   REPLICATIONSLAVEパーミッション

-   （必須）データベースのプライマリ-セカンダリ構成

    -   アップストリームデータベースのデータベース`server_id`を指定する必要があります（AWS以外のAurora環境ではGTIDをお勧めします）。

-   （必須）MySQLbinlog構成

    -   binlogが有効になっているかどうかを確認します（DMで必要）。
    -   `binlog_format=ROW`が構成されているかどうかを確認します（DMはROW形式のbinlogの移行のみをサポートします）。
    -   `binlog_row_image=FULL`が構成されているかどうかを確認します（DMは`binlog_row_image=FULL`のみをサポートします）。
    -   `binlog_do_db`または`binlog_ignore_db`が構成されている場合は、移行するデータベース表が`binlog_do_db`および`binlog_ignore_db`の条件を満たしているかどうかを確認してください。

-   （必須）アップストリームデータベースが[オンライン-DDL](/dm/feature-online-ddl.md)プロセスにあるかどうかを確認します（ `ghost`テーブルは作成されますが、 `rename`フェーズはまだ実行されていません）。アップストリームがonline-DDLプロセスにある場合、事前チェックはエラーを返します。この場合、DDLが完了するまで待ってから再試行してください。

### 完全および増分データ移行の項目を確認してください {#check-items-for-full-and-incremental-data-migration}

フルおよびインクリメンタルデータ移行モード（ `task-mode: all` ）の場合、 [共通のチェック項目](#common-check-items)に加えて、事前チェックには[完全なデータ移行チェック項目](#check-items-for-full-data-migration)と[増分データ移行チェック項目](#check-items-for-incremental-data-migration)も含まれます。

### 無視できるチェック項目 {#ignorable-check-items}

事前チェックにより、環境内の潜在的なリスクを見つけることができます。チェック項目を無視することはお勧めしません。データ移行タスクに特別なニーズがある場合は、 [`ignore-checking-items`構成アイテム](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)を使用していくつかのチェック項目をスキップできます。

| チェック項目                   | 説明                                                           |
| :----------------------- | :----------------------------------------------------------- |
| `dump_privilege`         | アップストリームMySQLインスタンスのユーザーのダンプ特権をチェックします。                      |
| `replication_privilege`  | アップストリームMySQLインスタンスのユーザーのレプリケーション権限を確認します。                   |
| `version`                | アップストリームデータベースのバージョンを確認します。                                  |
| `server_id`              | server_idがアップストリームデータベースで構成されているかどうかを確認します。                  |
| `binlog_enable`          | アップストリームデータベースでbinlogが有効になっているかどうかを確認します。                    |
| `table_schema`           | アップストリームMySQLテーブルのテーブルスキーマの互換性をチェックします。                      |
| `schema_of_shard_tables` | アップストリームのMySQLマルチインスタンスシャードのテーブルスキーマの整合性をチェックします。            |
| `auto_increment_ID`      | 自動インクリメントの主キーがアップストリームのMySQLマルチインスタンスシャードで競合していないかどうかを確認します。 |

> **ノート：**
>
> v6.0より前のバージョンでは、より無視できるチェック項目がサポートされています。 v6.0以降、DMではデータの安全性に関連するいくつかのチェック項目を無視することはできません。たとえば、 `binlog_row_image`パラメータを誤って設定すると、レプリケーション中にデータが失われる可能性があります。

## 事前チェック引数を構成する {#configure-precheck-arguments}

移行タスクの事前チェックは、並列処理をサポートします。シャーディングされたテーブルの行数が100万レベルに達した場合でも、事前チェックは数分で完了できます。

事前チェックのスレッド数を指定するには、移行タスク構成ファイルの`mydumpers`フィールドの`threads`引数を構成できます。

```yaml
mydumpers:                           # Configuration arguments of the dump processing unit
  global:                            # Configuration name
    threads: 4                       # The number of threads that access the upstream when the dump processing unit performs the precheck and exports data from the upstream database (4 by default)
    chunk-filesize: 64               # The size of the files generated by the dump processing unit (64 MB by default)
    extra-args: "--consistency none" # Other arguments of the dump processing unit. You do not need to manually configure table-list in `extra-args`, because it is automatically generated by DM.

```

> **ノート：**
>
> 値`threads`は、アップストリームデータベースとDM間の物理接続の数を決定します。 `threads`の値が大きすぎると、アップストリームの負荷が増加する可能性があります。したがって、 `threads`を適切な値に設定する必要があります。
