---
title: ADMIN | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
---

# 管理者 {#admin}

このステートメントはTiDB拡張構文であり、TiDBのステータスを表示し、TiDB内のテーブルのデータを確認するために使用されます。

## DDL関連のステートメント {#ddl-related-statement}

| 声明                                                                                      | 説明                                |
| --------------------------------------------------------------------------------------- | --------------------------------- |
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)            | 現在実行中のDDLジョブをキャンセルします。            |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのすべての行+インデックスのCRC64を計算します。    |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの整合性をチェックします。        |
| [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)      | 現在実行中または最近完了したDDLジョブに関する詳細を表示します。 |

## <code>ADMIN RELOAD</code>ステートメント {#code-admin-reload-code-statement}

{{< copyable "" >}}

```sql
ADMIN RELOAD expr_pushdown_blacklist;
```

上記のステートメントは、式によってプッシュダウンされたブロックリストを再ロードするために使用されます。

{{< copyable "" >}}

```sql
ADMIN RELOAD opt_rule_blacklist;
```

上記のステートメントは、ロジック最適化ルールのブロックリストを再ロードするために使用されます。

## <code>ADMIN PLUGINS</code>関連のステートメント {#code-admin-plugins-code-related-statement}

{{< copyable "" >}}

```sql
ADMIN PLUGINS ENABLE plugin_name [, plugin_name] ...;
```

上記のステートメントは、 `plugin_name`プラグインを有効にするために使用されます。

{{< copyable "" >}}

```sql
ADMIN PLUGINS DISABLE plugin_name [, plugin_name] ...;
```

上記のステートメントは、 `plugin_name`プラグインを無効にするために使用されます。

## <code>ADMIN BINDINGS</code>関連ステートメント {#code-admin-bindings-code-related-statement}

{{< copyable "" >}}

```sql
ADMIN FLUSH bindings;
```

上記のステートメントは、SQLプランのバインディング情報を永続化するために使用されます。

{{< copyable "" >}}

```sql
ADMIN CAPTURE bindings;
```

上記のステートメントは、複数回発生する`SELECT`のステートメントからSQLプランのバインディングを生成できます。

{{< copyable "" >}}

```sql
ADMIN EVOLVE bindings;
```

自動バインド機能を有効にすると、SQLプランのバインド情報の展開が`bind-info-leave`ごとにトリガーされます（デフォルト値は`3s` ）。上記のステートメントは、この進化を積極的にトリガーするために使用されます。

{{< copyable "" >}}

```sql
ADMIN RELOAD bindings;
```

上記のステートメントは、SQLプランのバインディング情報を再ロードするために使用されます。

## <code>ADMIN REPAIR</code>ステートメント {#code-admin-repair-code-statement}

極端な場合に信頼できない方法で保存されたテーブルのメタデータを上書きするには、 `ADMIN REPAIR TABLE`を使用します。

{{< copyable "" >}}

```sql
ADMIN REPAIR TABLE tbl_name CREATE TABLE STATEMENT;
```

ここで「信頼できない」とは、元のテーブルのメタデータが`CREATE TABLE STATEMENT`の操作でカバーできることを手動で確認する必要があることを意味します。この`REPAIR`ステートメントを使用するには、 [`repair-mode`](/tidb-configuration-file.md#repair-mode)構成項目を有効にし、修復するテーブルが[`repair-table-list`](/tidb-configuration-file.md#repair-table-list)にリストされていることを確認します。

## <code>ADMIN SHOW SLOW</code>ステートメント {#code-admin-show-slow-code-statement}

{{< copyable "" >}}

```sql
ADMIN SHOW SLOW RECENT N;
```

{{< copyable "" >}}

```sql
ADMIN SHOW SLOW TOP [INTERNAL | ALL] N;
```

詳しくは[adminshowslowステートメント](/identify-slow-queries.md#admin-show-slow-command)をご覧ください。

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )
```

## 例 {#examples}

次のコマンドを実行して、現在実行中のDDLジョブキュー内の最後の10個の完了したDDLジョブを表示します。 `NUM`が指定されていない場合、デフォルトでは、最後に完了した10個のDDLジョブのみが表示されます。

{{< copyable "" >}}

```sql
admin show ddl jobs;
```

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
```

次のコマンドを実行して、現在実行中のDDLジョブキューで最後に完了した5つのDDLジョブを表示します。

{{< copyable "" >}}

```sql
admin show ddl jobs 5;
```

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
```

次のコマンドを実行して、テストデータベース内の未完了のDDLジョブを表示します。結果には、実行中のDDLジョブと、完了したが失敗した最後の5つのDDLジョブが含まれます。

{{< copyable "" >}}

```sql
admin show ddl jobs 5 where state!='synced' and db_name='test';
```

```
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
```

-   `JOB_ID` ：各DDL操作は1つのDDLジョブに対応します。 `JOB_ID`は世界的にユニークです。
-   `DB_NAME` ：DDL操作が実行されるデータベースの名前。
-   `TABLE_NAME` ：DDL操作が実行されるテーブルの名前。
-   `JOB_TYPE` ：DDL操作のタイプ。
-   `SCHEMA_STATE` ：スキーマの現在の状態。 `JOB_TYPE`が`add index`の場合、それはインデックスの状態です。 `JOB_TYPE`が`add column`の場合、それは列の状態です。 `JOB_TYPE`が`create table`の場合、それはテーブルの状態です。一般的な状態は次のとおりです。
    -   `none` ：存在しないことを示します。 `drop`または`create`の操作が失敗してロールバックすると、通常は`none`の状態になります。
    -   `delete only` ：これらの`write only` `delete reorganization`の`write reorganization`は中間状態です。中間状態からの変換は非常に高速であるため、これらの状態は一般的な操作では表示されません。 `write reorganization`の状態は`add index`の操作でのみ確認できます。これは、インデックスデータが追加されていることを意味します。
    -   `public` ：既存で使用可能であることを示します。 `create table`や`add index/column`のような操作が終了すると、通常は`public`の状態になります。つまり、作成されたテーブル/列/インデックスは通常、読み取りと書き込みが可能になります。
-   `SCHEMA_ID` ：DDL操作が実行されるデータベースのID。
-   `TABLE_ID` ：DDL操作が実行されるテーブルのID。
-   `ROW_COUNT` ： `add index`操作の実行時に追加されたデータ行の数。
-   `START_TIME` ：DDL操作の開始時刻。
-   `END_TIME` ：DDL操作の終了時刻。
-   `STATE` ：DDL操作の状態。一般的な状態は次のとおりです。
    -   `none` ：操作タスクがDDLジョブキューに入れられたが、前のタスクが完了するのを待っているため、まだ実行されていないことを示します。もう1つの理由は、ドロップ操作の実行後に`none`状態になるが、まもなく`synced`状態に更新されるためです。これは、すべてのTiDBインスタンスがこの状態に同期されたことを意味します。
    -   `running` ：操作が実行されていることを示します。
    -   `synced` ：操作が正常に実行され、すべてのTiDBインスタンスがこの状態に同期されたことを示します。
    -   `rollback done` ：操作が失敗し、ロールバックが終了したことを示します。
    -   `rollingback` ：操作が失敗し、ロールバックしていることを示します。
    -   `cancelling` ：操作がキャンセルされていることを示します。この状態は、 `ADMIN CANCEL DDL JOBS`コマンドを使用してDDLジョブをキャンセルした場合にのみ発生します。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。
