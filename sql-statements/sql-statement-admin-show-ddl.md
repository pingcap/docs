---
title: ADMIN SHOW DDL [JOBS|QUERIES] | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
---

# ADMIN SHOW DDL [JOBS | QUERIES] {#admin-show-ddl-jobs-queries}

`ADMIN SHOW DDL [JOBS|QUERIES]`ステートメントは、実行中および最近完了したDDLジョブに関する情報を示しています。

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

NumList ::=
    Int64Num ( ',' Int64Num )*

WhereClauseOptional ::=
    WhereClause?
```

## 例 {#examples}

### <code>ADMIN SHOW DDL</code> {#code-admin-show-ddl-code}

現在実行中のDDLジョブを表示するには、 `ADMIN SHOW DDL`を使用します。

{{< copyable "" >}}

```sql
ADMIN SHOW DDL;
```

```sql
mysql> ADMIN SHOW DDL;
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
| SCHEMA_VER | OWNER_ID                             | OWNER_ADDRESS | RUNNING_JOBS | SELF_ID                              | QUERY |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
|         26 | 2d1982af-fa63-43ad-a3d5-73710683cc63 | 0.0.0.0:4000  |              | 2d1982af-fa63-43ad-a3d5-73710683cc63 |       |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
1 row in set (0.00 sec)
```

### <code>ADMIN SHOW DDL JOBS</code> {#code-admin-show-ddl-jobs-code}

現在のDDLジョブキュー内のすべての結果（実行中および実行待ちのタスクを含む）と、完了したDDLジョブキュー内の最後の10個の結果を表示するには、次を使用し`ADMIN SHOW DDL JOBS` 。

{{< copyable "" >}}

```sql
ADMIN SHOW DDL JOBS;
```

```sql
mysql> ADMIN SHOW DDL JOBS;
+--------+---------+--------------------+--------------+----------------------+-----------+----------+-----------+-----------------------------------------------------------------+---------+
| JOB_ID | DB_NAME | TABLE_NAME         | JOB_TYPE     | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME         | START_TIME          | END_TIME            | STATE   |
+--------+---------+--------------------+--------------+----------------------+-----------+----------+-----------+---------------------+-------------------------------------------+---------+
|     59 | test    | t1                 | add index    | write reorganization |         1 |       55 |     88576 | 2020-08-17 07:51:58 | 2020-08-17 07:51:58 | NULL                | running |
|     60 | test    | t2                 | add index    | none                 |         1 |       57 |         0 | 2020-08-17 07:51:59 | 2020-08-17 07:51:59 | NULL                | none    |
|     58 | test    | t2                 | create table | public               |         1 |       57 |         0 | 2020-08-17 07:41:28 | 2020-08-17 07:41:28 | 2020-08-17 07:41:28 | synced  |
|     56 | test    | t1                 | create table | public               |         1 |       55 |         0 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | synced  |
|     54 | test    | t1                 | drop table   | none                 |         1 |       50 |         0 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | 2020-08-17 07:41:02 | synced  |
|     53 | test    | t1                 | drop index   | none                 |         1 |       50 |         0 | 2020-08-17 07:35:44 | 2020-08-17 07:35:44 | 2020-08-17 07:35:44 | synced  |
|     52 | test    | t1                 | add index    | public               |         1 |       50 |    451010 | 2020-08-17 07:34:43 | 2020-08-17 07:34:43 | 2020-08-17 07:35:16 | synced  |
|     51 | test    | t1                 | create table | public               |         1 |       50 |         0 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | synced  |
|     49 | test    | t1                 | drop table   | none                 |         1 |       47 |         0 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | 2020-08-17 07:34:02 | synced  |
|     48 | test    | t1                 | create table | public               |         1 |       47 |         0 | 2020-08-17 07:33:37 | 2020-08-17 07:33:37 | 2020-08-17 07:33:37 | synced  |
|     46 | mysql   | stats_extended     | create table | public               |         3 |       45 |         0 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | synced  |
|     44 | mysql   | opt_rule_blacklist | create table | public               |         3 |       43 |         0 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | 2020-08-17 06:42:38 | synced  |
+--------+---------+--------------------+--------------+----------------------+-----------+----------+-----------+---------------------+---------------------+-------------------------------+
12 rows in set (0.00 sec)
```

上記の出力から：

-   ジョブ59は現在進行中`running` `STATE` 。スキーマの状態は現在`write reorganization`ですが、タスクが完了すると`public`に切り替わり、ユーザーセッションによって変更を公開で確認できることに注意してください。 `end_time`列も`NULL`であり、ジョブの完了時刻が現在不明であることを示しています。

-   ジョブ60は`add index`のジョブであり、現在、ジョブ59が完了するのを待ってキューに入れられています。ジョブ59が完了すると、ジョブ60の`STATE`が`running`に切り替わります。

-   インデックスの削除やテーブルの削除などの破壊的な変更の場合、ジョブが完了すると`SCHEMA_STATE`が`none`に変更されます。付加的な変更の場合、 `SCHEMA_STATE`は`public`に変更されます。

表示される行数を制限するには、数とwhere条件を指定します。

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

-   `NUM` ：完了したDDLジョブキューの最後の`NUM`の結果を表示します。指定しない場合、デフォルトでは`NUM`が10になります。
-   `WHERE` ：フィルター条件を追加します。

### <code>ADMIN SHOW DDL JOB QUERIES</code> {#code-admin-show-ddl-job-queries-code}

`job_id`に対応するDDLジョブの元のSQLステートメントを表示するには、 `ADMIN SHOW DDL JOB QUERIES`を使用します。

{{< copyable "" >}}

```sql
ADMIN SHOW DDL JOBS;
ADMIN SHOW DDL JOB QUERIES 51;
```

```sql
mysql> ADMIN SHOW DDL JOB QUERIES 51;
+--------------------------------------------------------------+
| QUERY                                                        |
+--------------------------------------------------------------+
| CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY auto_increment) |
+--------------------------------------------------------------+
1 row in set (0.02 sec)
```

DDL履歴ジョブキュー内の最後の10件の結果内で`job_id`に対応する実行中のDDLジョブのみを検索できます。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [管理キャンセルDDL](/sql-statements/sql-statement-admin-cancel-ddl.md)
