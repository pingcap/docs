---
title: ADMIN SHOW DDL [JOBS|JOB QUERIES] | TiDB SQL Statement Reference
summary: TiDB データベースの ADMIN の使用法の概要。
---

# 管理者は DDL を表示 [ジョブ|ジョブ クエリ] {#admin-show-ddl-jobs-job-queries}

`ADMIN SHOW DDL [JOBS|JOB QUERIES]`ステートメントは、実行中の DDL ジョブと最近完了した DDL ジョブに関する情報を表示します。

## 概要 {#synopsis}

```ebnf+diagram
AdminShowDDLStmt ::=
    'ADMIN' 'SHOW' 'DDL'
    ( 
        'JOBS' Int64Num? WhereClauseOptional 
    |   'JOB' 'QUERIES' NumList 
    |   'JOB' 'QUERIES' 'LIMIT' m ( ('OFFSET' | ',') n )?
    )?

NumList ::=
    Int64Num ( ',' Int64Num )*

WhereClauseOptional ::=
    WhereClause?
```

## 例 {#examples}

### <code>ADMIN SHOW DDL</code> {#code-admin-show-ddl-code}

現在実行中の DDL ジョブのステータスを表示するには、 `ADMIN SHOW DDL`使用します。出力には、現在のスキーマ バージョン、所有者の DDL ID とアドレス、実行中の DDL ジョブと SQL ステートメント、現在の TiDB インスタンスの DDL ID が含まれます。

-   `SCHEMA_VER` : スキーマのバージョンを示す数値。
-   `OWNER_ID` : DDL所有者の[`TIDB_IS_DDL_OWNER()`](/functions-and-operators/tidb-functions.md)も参照してください。
-   `OWNER_ADDRESS` : DDL 所有者の IP アドレス。
-   `RUNNING_JOBS` : 実行中の DDL ジョブの詳細。
-   `SELF_ID` : 現在接続している TiDB ノードの UUID。 `SELF_ID` `OWNER_ID`と同じ場合は、DDL 所有者に接続していることを意味します。
-   `QUERY` : クエリのステートメント。

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

`ADMIN SHOW DDL JOBS`ステートメントは、実行中およびキューイング中のタスクを含む現在の DDL ジョブ キュー内のすべての結果と、完了した DDL ジョブ キュー内の最新の 10 件の結果を表示するために使用されます。返される結果フィールドは次のように説明されます。

<CustomContent platform="tidb">

-   `JOB_ID` : 各 DDL 操作は DDL ジョブに対応します。2 `JOB_ID`グローバルに一意です。
-   `DB_NAME` : DDL 操作が実行されるデータベースの名前。
-   `TABLE_NAME` : DDL 操作が実行されるテーブルの名前。
-   `JOB_TYPE` : DDL 操作のタイプ。一般的なジョブ タイプは次のとおりです。
    -   `ingest` : [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)で設定された高速インデックスバックフィルによる取り込み。
    -   `txn` : 基本的なトランザクション バックフィル。
    -   `txn-merge` : バックフィルが完了すると元のインデックスとマージされる一時インデックスを使用したトランザクション バックフィル。
-   `SCHEMA_STATE` : DDL が操作するスキーマ オブジェクトの現在の状態。 `JOB_TYPE`が`ADD INDEX`の場合はインデックスの状態、 `JOB_TYPE`が`ADD COLUMN`の場合は列の状態、 `JOB_TYPE`が`CREATE TABLE`の場合はテーブルの状態です。一般的な状態は次のとおりです。
    -   `none` : 存在しないことを示します。通常、 `DROP`操作の後、または`CREATE`操作が失敗してロールバックした後は、 `none`の状態になります。
    -   `delete only` `write reorganization`これらの 4 つの状態は中間状態です。具体的な意味については`write only` [TiDB でのオンライン DDL 非同期変更の仕組み](/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb) `ADD INDEX`参照してください。中間状態の変換は高速である`delete reorganization` 、これらの状態は通常、操作中に表示されません。10 操作を実行している場合にのみ、インデックス データが追加されていることを示す`write reorganization`状態が表示されます。
    -   `public` : 存在し、ユーザーが利用できることを示します。通常、 `CREATE TABLE`と`ADD INDEX` (または`ADD COLUMN` ) の操作が完了すると、 `public`状態になり、新しく作成されたテーブル、列、およびインデックスを正常に読み書きできることを示します。
-   `SCHEMA_ID` : DDL 操作が実行されるデータベースの ID。
-   `TABLE_ID` : DDL 操作が実行されるテーブルの ID。
-   `ROW_COUNT` : `ADD INDEX`操作を実行すると、追加されたデータ行の数になります。
-   `START_TIME` : DDL 操作の開始時刻。
-   `STATE` : DDL 操作の状態。一般的な状態は次のとおりです。
    -   `queueing` : 操作ジョブが DDL ジョブ キューに入ったが、以前の DDL ジョブの完了を待機しているため実行されていないことを示します。別の理由としては、 `DROP`操作を実行した後、 `none`の状態になりますが、すぐに`synced`の状態に更新され、すべての TiDB インスタンスがその状態に同期されたことが示されることが考えられます。
    -   `running` : 操作が実行中であることを示します。
    -   `synced` : 操作が正常に実行され、すべての TiDB インスタンスがこの状態に同期されていることを示します。
    -   `rollback done` : 操作が失敗し、ロールバックが完了したことを示します。
    -   `rollingback` : 操作が失敗し、ロールバック中であることを示します。
    -   `cancelling` : 操作がキャンセルされていることを示します。この状態は、 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルした場合にのみ表示されます。
    -   `paused` : 操作が一時停止されていることを示します。この状態は[`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)コマンドを使用して DDL ジョブを一時停止した場合にのみ表示されます。4 コマンドを使用して DDL ジョブを再開できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `JOB_ID` : 各 DDL 操作は DDL ジョブに対応します。2 `JOB_ID`グローバルに一意です。
-   `DB_NAME` : DDL 操作が実行されるデータベースの名前。
-   `TABLE_NAME` : DDL 操作が実行されるテーブルの名前。
-   `JOB_TYPE` : DDL 操作のタイプ。
-   `SCHEMA_STATE` : DDL が操作するスキーマ オブジェクトの現在の状態。 `JOB_TYPE`が`ADD INDEX`の場合はインデックスの状態、 `JOB_TYPE`が`ADD COLUMN`の場合は列の状態、 `JOB_TYPE`が`CREATE TABLE`の場合はテーブルの状態です。一般的な状態は次のとおりです。
    -   `none` : 存在しないことを示します。通常、 `DROP`操作の後、または`CREATE`操作が失敗してロールバックした後は、 `none`の状態になります。
    -   `delete only` `write reorganization`これらの 4 つの状態は中間状態です。具体的な意味については`write only` [TiDB でのオンライン DDL 非同期変更の仕組み](https://docs.pingcap.com/tidb/stable/ddl-introduction#how-the-online-ddl-asynchronous-change-works-in-tidb) `ADD INDEX`参照してください。中間状態の変換は高速である`delete reorganization` 、これらの状態は通常、操作中に表示されません。10 操作を実行している場合にのみ、インデックス データが追加されていることを示す`write reorganization`状態が表示されます。
    -   `public` : 存在し、ユーザーが利用できることを示します。通常、 `CREATE TABLE`と`ADD INDEX` (または`ADD COLUMN` ) の操作が完了すると、 `public`状態になり、新しく作成されたテーブル、列、およびインデックスを正常に読み書きできることを示します。
-   `SCHEMA_ID` : DDL 操作が実行されるデータベースの ID。
-   `TABLE_ID` : DDL 操作が実行されるテーブルの ID。
-   `ROW_COUNT` : `ADD INDEX`操作を実行すると、追加されたデータ行の数になります。
-   `START_TIME` : DDL 操作の開始時刻。
-   `STATE` : DDL 操作の状態。一般的な状態は次のとおりです。
    -   `queueing` : 操作ジョブが DDL ジョブ キューに入ったが、以前の DDL ジョブの完了を待機しているため実行されていないことを示します。別の理由としては、 `DROP`操作を実行した後、 `none`の状態になりますが、すぐに`synced`の状態に更新され、すべての TiDB インスタンスがその状態に同期されたことが示されることが考えられます。
    -   `running` : 操作が実行中であることを示します。
    -   `synced` : 操作が正常に実行され、すべての TiDB インスタンスがこの状態に同期されていることを示します。
    -   `rollback done` : 操作が失敗し、ロールバックが完了したことを示します。
    -   `rollingback` : 操作が失敗し、ロールバック中であることを示します。
    -   `cancelling` : 操作がキャンセルされていることを示します。この状態は、 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルした場合にのみ表示されます。
    -   `paused` : 操作が一時停止されていることを示します。この状態は[`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)コマンドを使用して DDL ジョブを一時停止した場合にのみ表示されます。4 コマンドを使用して DDL ジョブを再開できます。

</CustomContent>

次の例は`ADMIN SHOW DDL JOBS`の結果を示しています。

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

上記の出力から:

-   ジョブ 59 は現在進行中です ( `STATE` )。スキーマの状態は現在`write reorganization`ですが、タスクが完了すると`public`に切り替わり`running`ユーザー セッションによって変更が公開されることに注意してください。9 列も`end_time` `NULL`なっており、ジョブの完了時間が現在不明であることを示しています。

-   ジョブ 60 は`add index`ジョブであり、現在キューに入れられてジョブ 59 の完了を待機しています。ジョブ 59 が完了すると、ジョブ 60 の`STATE` `running`に切り替わります。

-   インデックスの削除やテーブルの削除などの破壊的な変更の場合、ジョブが完了すると`SCHEMA_STATE` `none`に変わります。追加的な変更の場合、 `SCHEMA_STATE` `public`に変わります。

表示される行数を制限するには、数値と where 条件を指定します。

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

-   `NUM` : 完了した DDL ジョブ キューの最後の`NUM`結果を表示します。指定しない場合は、デフォルトで`NUM`または 10 になります。
-   `WHERE` : フィルター条件を追加します。

### <code>ADMIN SHOW DDL JOB QUERIES</code> {#code-admin-show-ddl-job-queries-code}

`job_id`に対応する DDL ジョブの元の SQL ステートメントを表示するには、 `ADMIN SHOW DDL JOB QUERIES`使用します。

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

DDL 履歴ジョブ キュー内の最後の 10 件の結果のうち、 `job_id`に対応する実行中の DDL ジョブのみを検索できます。

### <code>ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n</code> {#code-admin-show-ddl-job-queries-limit-m-offset-n-code}

`job_id`に対応する指定された範囲`[n+1, n+m]`内の DDL ジョブの元の SQL ステートメントを表示するには、 `ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n`使用します。

```sql
 ADMIN SHOW DDL JOB QUERIES LIMIT m;  # Retrieve first m rows
 ADMIN SHOW DDL JOB QUERIES LIMIT n, m;  # Retrieve rows [n+1, n+m]
 ADMIN SHOW DDL JOB QUERIES LIMIT m OFFSET n;  # Retrieve rows [n+1, n+m]
```

ここで、 `n`と`m` 0 以上の整数です。

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT 3;  # Retrieve first 3 rows
+--------+--------------------------------------------------------------+
| JOB_ID | QUERY                                                        |
+--------+--------------------------------------------------------------+
|     59 | ALTER TABLE t1 ADD INDEX index2 (col2)                       |
|     60 | ALTER TABLE t2 ADD INDEX index1 (col1)                       |
|     58 | CREATE TABLE t2 (id INT NOT NULL PRIMARY KEY auto_increment) |
+--------+--------------------------------------------------------------+
3 rows in set (0.00 sec)
```

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT 6, 2;  # Retrieve rows 7-8
+--------+----------------------------------------------------------------------------+
| JOB_ID | QUERY                                                                      |
+--------+----------------------------------------------------------------------------+
|     52 | ALTER TABLE t1 ADD INDEX index1 (col1)                                     |
|     51 | CREATE TABLE IF NOT EXISTS t1 (id INT NOT NULL PRIMARY KEY auto_increment) |
+--------+----------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

```sql
ADMIN SHOW DDL JOB QUERIES LIMIT 3 OFFSET 4;  # Retrieve rows 5-7
+--------+----------------------------------------+
| JOB_ID | QUERY                                  |
+--------+----------------------------------------+
|     54 | DROP TABLE IF EXISTS t3                |
|     53 | ALTER TABLE t1 DROP INDEX index1       |
|     52 | ALTER TABLE t1 ADD INDEX index1 (col1) |
+--------+----------------------------------------+
3 rows in set (0.00 sec)
```

DDL 履歴ジョブ キュー内の任意に指定した結果範囲内で、 `job_id`に対応する実行中の DDL ジョブを検索できます。この構文には、 `ADMIN SHOW DDL JOB QUERIES`の最後の 10 件の結果という制限はありません。

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [管理者はDDLをキャンセルします](/sql-statements/sql-statement-admin-cancel-ddl.md)
-   [管理者一時停止DDL](/sql-statements/sql-statement-admin-pause-ddl.md)
-   [管理者履歴書 DDL](/sql-statements/sql-statement-admin-resume-ddl.md)
