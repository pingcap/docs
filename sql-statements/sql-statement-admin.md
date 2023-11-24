---
title: ADMIN | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
---

# 管理者 {#admin}

このステートメントは TiDB 拡張構文であり、TiDB のステータスを表示し、TiDB 内のテーブルのデータをチェックするために使用されます。このドキュメントでは、次の`ADMIN`関連ステートメントを紹介します。

-   [`ADMIN RELOAD`](#admin-reload-statement)
-   [`ADMIN PLUGINS`](#admin-plugins-related-statement)
-   [`ADMIN ... BINDINGS`](#admin-bindings-related-statement)
-   [`ADMIN REPAIR`](#admin-repair-statement)
-   [`ADMIN SHOW NEXT_ROW_ID`](#admin-show-next_row_id-statement)
-   [`ADMIN SHOW SLOW`](#admin-show-slow-statement)

## DDL 関連のステートメント {#ddl-related-statement}

<CustomContent platform="tidb-cloud">

| 声明                                                                                      | 説明                                 |
| --------------------------------------------------------------------------------------- | ---------------------------------- |
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)            | 現在実行中の DDL ジョブをキャンセルします。           |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのすべての行 + インデックスの CRC64 を計算します。 |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの整合性をチェックします。         |
| [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)      | 現在実行中または最近完了した DDL ジョブの詳細を表示します。   |

</CustomContent>

<CustomContent platform="tidb">

| 声明                                                                                      | 説明                                      |
| --------------------------------------------------------------------------------------- | --------------------------------------- |
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)            | 現在実行中の DDL ジョブをキャンセルします。                |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのすべての行 + インデックスの CRC64 を計算します。      |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの整合性をチェックします。              |
| [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)      | 現在実行中または最近完了した DDL ジョブの詳細を表示します。        |
| [`ADMIN SHOW TELEMETRY`](/sql-statements/sql-statement-admin-show-telemetry.md)         | テレメトリ機能の一部として PingCAP にレポートされる情報を表示します。 |

</CustomContent>

## <code>ADMIN RELOAD</code>ステートメント {#code-admin-reload-code-statement}

```sql
ADMIN RELOAD expr_pushdown_blacklist;
```

上記のステートメントは、式によってプッシュダウンされたブロックリストを再ロードするために使用されます。

```sql
ADMIN RELOAD opt_rule_blacklist;
```

上記のステートメントは、ロジック最適化ルールのブロックリストを再ロードするために使用されます。

## <code>ADMIN PLUGINS</code>関連のステートメント {#code-admin-plugins-code-related-statement}

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

```sql
ADMIN PLUGINS ENABLE plugin_name [, plugin_name] ...;
```

上記のステートメントは、 `plugin_name`プラグインを有効にするために使用されます。

```sql
ADMIN PLUGINS DISABLE plugin_name [, plugin_name] ...;
```

上記のステートメントは、 `plugin_name`プラグインを無効にするために使用されます。

## <code>ADMIN BINDINGS</code>関連のステートメント {#code-admin-bindings-code-related-statement}

```sql
ADMIN FLUSH BINDINGS;
```

上記のステートメントは、SQL プラン バインディング情報を永続化するために使用されます。

```sql
ADMIN CAPTURE BINDINGS;
```

上記のステートメントは、複数回発生する`SELECT`ステートメントから SQL Plan のバインディングを生成できます。

```sql
ADMIN EVOLVE BINDINGS;
```

自動バインド機能が有効になった後、SQL プラン バインディング情報の進化は`bind-info-leave`ごとにトリガーされます (デフォルト値は`3s` )。上記のステートメントは、この進化を積極的に引き起こすために使用されます。

```sql
ADMIN RELOAD BINDINGS;
```

上記のステートメントは、SQL プラン バインディング情報を再ロードするために使用されます。

## <code>ADMIN REPAIR</code>ステートメント {#code-admin-repair-code-statement}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB ステートメントはTiDB Cloudには適用されません。

</CustomContent>

極端な場合に、保存されたテーブルのメタデータを信頼できない方法で上書きするには、 `ADMIN REPAIR TABLE`を使用します。

```sql
ADMIN REPAIR TABLE tbl_name CREATE TABLE STATEMENT;
```

<CustomContent platform="tidb">

ここでの「信頼できない」とは、元のテーブルのメタデータが`CREATE TABLE STATEMENT`操作でカバーできることを手動で確認する必要があることを意味します。この`REPAIR`ステートメントを使用するには、 [`repair-mode`](/tidb-configuration-file.md#repair-mode)構成項目を有効にし、修復するテーブルが[`repair-table-list`](/tidb-configuration-file.md#repair-table-list)にリストされていることを確認します。

</CustomContent>

## <code>ADMIN SHOW NEXT_ROW_ID</code>ステートメント {#code-admin-show-next-row-id-code-statement}

```sql
ADMIN SHOW t NEXT_ROW_ID;
```

上記のステートメントは、テーブルのいくつかの特別な列の詳細を表示するために使用されます。出力は[テーブルのNEXT_ROW_IDを表示](/sql-statements/sql-statement-show-table-next-rowid.md)と同じです。

## <code>ADMIN SHOW SLOW</code>ステートメント {#code-admin-show-slow-code-statement}

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

```sql
ADMIN SHOW SLOW RECENT N;
```

```sql
ADMIN SHOW SLOW TOP [INTERNAL | ALL] N;
```

<CustomContent platform="tidb">

詳細は[`ADMIN SHOW SLOW`コマンド](/identify-slow-queries.md#admin-show-slow-command)を参照してください。

</CustomContent>

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )
```

## 例 {#examples}

次のコマンドを実行して、現在実行中の DDL ジョブ キュー内の完了した最後の 10 個の DDL ジョブを表示します。 `NUM`が指定されていない場合、デフォルトでは、最後に完了した 10 個の DDL ジョブのみが表示されます。

```sql
ADMIN SHOW DDL JOBS;
```

    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
    | 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
    | 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | 2019-01-10 12:35:14.925 +0800 CST | synced        |
    | 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | 2019-01-10 12:34:36.958 +0800 CST | synced        |
    | 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | 2019-01-10 12:33:24.625 +0800 CST | synced        |
    | 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | 2019-01-10 12:33:09.78 +0800 CST  | synced        |
    | 39     | test    | t1         | add column    | public               | 32        | 37       | 0         | 2019-01-10 12:32:55.42 +0800 CST  | 2019-01-10 12:32:56.24 +0800 CST  | synced        |
    | 38     | test    | t1         | create table  | public               | 32        | 37       | 0         | 2019-01-10 12:32:41.956 +0800 CST | 2019-01-10 12:32:43.956 +0800 CST | synced        |
    | 36     | test    |            | drop table    | none                 | 32        | 34       | 0         | 2019-01-10 11:29:59.982 +0800 CST | 2019-01-10 11:30:00.45 +0800  CST | synced        |
    | 35     | test    |            | create table  | public               | 32        | 34       | 0         | 2019-01-10 11:29:40.741 +0800 CST | 2019-01-10 11:29:41.682 +0800 CST | synced        |
    | 33     | test    |            | create schema | public               | 32        | 0        | 0         | 2019-01-10 11:29:22.813 +0800 CST | 2019-01-10 11:29:23.954 +0800 CST | synced        |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+

次のコマンドを実行して、現在実行中の DDL ジョブ キュー内の最後に完了した 5 つの DDL ジョブを表示します。

```sql
ADMIN SHOW DDL JOBS 5;
```

    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
    | 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
    | 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | 2019-01-10 12:35:14.925 +0800 CST | synced        |
    | 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | 2019-01-10 12:34:36.958 +0800 CST | synced        |
    | 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | 2019-01-10 12:33:24.625 +0800 CST | synced        |
    | 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | 2019-01-10 12:33:09.78 +0800 CST  | synced        |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+

次のコマンドを実行して、テーブルのいくつかの特別な列の詳細を表示します。出力は[テーブルのNEXT_ROW_IDを表示](/sql-statements/sql-statement-show-table-next-rowid.md)と同じです。

```sql
ADMIN SHOW t NEXT_ROW_ID;
```

```sql
+---------+------------+-------------+--------------------+----------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID | ID_TYPE        |
+---------+------------+-------------+--------------------+----------------+
| test    | t          | _tidb_rowid |                101 | _TIDB_ROWID    |
| test    | t          | _tidb_rowid |                  1 | AUTO_INCREMENT |
+---------+------------+-------------+--------------------+----------------+
2 rows in set (0.01 sec)
```

次のコマンドを実行して、テスト データベース内の未完了の DDL ジョブを表示します。結果には、実行中の DDL ジョブと、完了したが失敗した最後の 5 つの DDL ジョブが含まれます。

```sql
ADMIN SHOW DDL JOBS 5 WHERE state != 'synced' AND db_name = 'test';
```

    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
    | 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+

-   `JOB_ID` : 各 DDL 操作は 1 つの DDL ジョブに対応します。 `JOB_ID`世界的にユニークです。
-   `DB_NAME` : DDL 操作が実行されるデータベースの名前。
-   `TABLE_NAME` : DDL 操作が実行されるテーブルの名前。
-   `JOB_TYPE` : DDL 操作のタイプ。
-   `SCHEMA_STATE` : スキーマの現在の状態。 `JOB_TYPE`が`add index`の場合、それはインデックスの状態です。 `JOB_TYPE`が`add column`の場合、それは列の状態です。 `JOB_TYPE`が`create table`の場合、それがテーブルの状態です。一般的な状態には次のようなものがあります。
    -   `none` : 存在しないことを示します。 `drop`または`create`操作が失敗してロールバックすると、通常は`none`状態になります。
    -   `delete only` 、 `write only` 、 `delete reorganization` 、 `write reorganization` : これら 4 つの状態は中間状態です。中間状態からの変換は非常に速いため、これらの状態は一般的な操作では表示されません。 `add index`の操作でのみ`write reorganization`状態が表示されます。これは、インデックス データが追加されていることを意味します。
    -   `public` : 存在し、使用可能であることを示します。 `create table`や`add index/column`の操作が完了すると、通常は`public`状態になります。これは、作成されたテーブル/カラム/インデックスが正常に読み書きできるようになることを意味します。
-   `SCHEMA_ID` : DDL 操作が実行されるデータベースの ID。
-   `TABLE_ID` : DDL 操作が実行されるテーブルの ID。
-   `ROW_COUNT` : `add index`操作の実行時に追加されたデータ行の数。
-   `START_TIME` : DDL 操作の開始時刻。
-   `END_TIME` : DDL 操作の終了時刻。
-   `STATE` : DDL 操作の状態。一般的な状態には次のものがあります。
    -   `none` : 操作タスクは DDL ジョブ キューに入れられていますが、前のタスクが完了するのを待っているため、まだ実行されていないことを示します。もう 1 つの理由は、ドロップ操作の実行後に`none`状態になるが、すぐに`synced`状態に更新されることです。これは、すべての TiDB インスタンスがこの状態に同期されていることを意味します。
    -   `running` : 操作が実行中であることを示します。
    -   `synced` : 操作が正常に実行され、すべての TiDB インスタンスがこの状態に同期されたことを示します。
    -   `rollback done` : 操作が失敗し、ロールバックが終了したことを示します。
    -   `rollingback` : 操作が失敗し、ロールバック中であることを示します。
    -   `cancelling` : 操作がキャンセルされていることを示します。この状態は、 `ADMIN CANCEL DDL JOBS`コマンドを使用して DDL ジョブをキャンセルした場合にのみ発生します。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。
