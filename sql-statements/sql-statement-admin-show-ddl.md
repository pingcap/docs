---
title: ADMIN SHOW DDL [JOBS|JOB QUERIES] | TiDB SQL Statement Reference
summary: TiDB データベースにおける ADMIN の使用法の概要。
---

# 管理者 SHOW DDL [ジョブ|ジョブクエリ] {#admin-show-ddl-jobs-job-queries}

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

現在実行中のDDLジョブのステータスを表示するには、 `ADMIN SHOW DDL`使用します。出力には、現在のスキーマバージョン、DDL IDと所有者のアドレス、実行中のDDLジョブとSQL文、現在のTiDBインスタンスのDDL IDが含まれます。返される結果フィールドは以下のとおりです。

-   `SCHEMA_VER` : スキーマのバージョンを示す数値。
-   `OWNER_ID` : DDL所有者の[`TIDB_IS_DDL_OWNER()`](/functions-and-operators/tidb-functions.md)も参照してください。
-   `OWNER_ADDRESS` : DDL 所有者の IP アドレス。
-   `RUNNING_JOBS` : 実行中の DDL ジョブの詳細。
-   `SELF_ID` : 現在接続しているTiDBノードのUUID。2 `SELF_ID` `OWNER_ID`と同じ場合は、DDL所有者に接続していることを意味します。
-   `QUERY` : クエリのステートメント。

```sql
ADMIN SHOW DDL\G;
```

```sql
*************************** 1. row ***************************
   SCHEMA_VER: 26
     OWNER_ID: 2d1982af-fa63-43ad-a3d5-73710683cc63
OWNER_ADDRESS: 0.0.0.0:4000
 RUNNING_JOBS:
      SELF_ID: 2d1982af-fa63-43ad-a3d5-73710683cc63
        QUERY:
1 row in set (0.00 sec)
```

### <code>ADMIN SHOW DDL JOBS</code> {#code-admin-show-ddl-jobs-code}

`ADMIN SHOW DDL JOBS`文は、現在のDDLジョブキューにある10個のジョブ（実行中および保留中のジョブ（存在する場合）を含む）と、実行済みのDDLジョブキューにある最後の10個のジョブ（存在する場合）を表示します。返される結果フィールドは、以下のとおりです。

<CustomContent platform="tidb">

-   `JOB_ID` : 各 DDL 操作は DDL ジョブに対応します。2 `JOB_ID`グローバルに一意です。
-   `DB_NAME` : DDL 操作が実行されるデータベースの名前。
-   `TABLE_NAME` : DDL 操作が実行されるテーブルの名前。
-   `JOB_TYPE` : DDL操作の種類。一般的なジョブの種類は次のとおりです。
    -   `create schema` : [`CREATE SCHEMA`](/sql-statements/sql-statement-create-database.md)操作の場合。
    -   `create table` : [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)操作の場合。
    -   `create view` : [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md)操作の場合。
    -   `add index` : [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)操作の場合。
-   `SCHEMA_STATE` : DDLが操作するスキーマオブジェクトの現在の状態。2 が`JOB_TYPE` `ADD INDEX`場合はインデックスの状態、 `JOB_TYPE`が`ADD COLUMN`場合は列の状態、 `JOB_TYPE`が`CREATE TABLE`の場合はテーブルの状態です。一般的な状態には以下が含まれます。
    -   `none` : 存在しないことを示します。通常、 `DROP`操作の後、または`CREATE`操作が失敗してロールバックした後、 `none`状態になります。
    -   `delete only` ：これら`write reorganization` 4 `delete reorganization`の状態は中間状態です。それぞれの具体的な意味については、 [TiDBにおけるオンラインDDL非同期変更の仕組み](/ddl-introduction.md#how-the-online-ddl-asynchronous-change-works-in-tidb)参照してください。中間状態の変換は高速であるため、これらの状態`write only`通常、演算中は表示されません。10 `ADD INDEX`演算を実行する場合にのみ、 `write reorganization`状態が表示され、インデックスデータが追加されていることを示します。
    -   `public` : 存在し、ユーザーが利用できることを示します。通常、 `CREATE TABLE`と`ADD INDEX` （または`ADD COLUMN` ）の操作が完了すると、状態は`public`になり、新しく作成されたテーブル、列、およびインデックスが正常に読み書きできることを示します。
-   `SCHEMA_ID` : DDL 操作が実行されるデータベースの ID。
-   `TABLE_ID` : DDL 操作が実行されるテーブルの ID。
-   `ROW_COUNT` : `ADD INDEX`操作を実行すると、追加されたデータ行の数になります。
-   `CREATE_TIME` : DDL 操作の作成時刻。
-   `START_TIME` : DDL 操作の開始時刻。
-   `END_TIME` : DDL 操作の終了時刻。
-   `STATE` : DDL操作の状態。一般的な状態は次のとおりです。
    -   `none` : 操作がまだ開始されていないことを示します。
    -   `queueing` : 操作ジョブがDDLジョブキューに入ったものの、前のDDLジョブの完了を待機しているため実行されていないことを示します。別の理由としては、 `DROP`操作の実行後、 `queueing`番目の状態が`done`番目の状態になるものの、すぐに`synced`番目の状態に更新され、すべてのTiDBインスタンスがその状態に同期されたことが考えられます。
    -   `running` : 操作が実行中であることを示します。
    -   `synced` : 操作が正常に実行され、すべての TiDB インスタンスがこの状態に同期されていることを示します。
    -   `rollback done` : 操作が失敗し、ロールバックが完了したことを示します。
    -   `rollingback` : 操作が失敗し、ロールバック中であることを示します。
    -   `cancelling` : 操作がキャンセルされていることを示します。この状態は、 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルした場合にのみ表示されます。
    -   `cancelled` : 操作がキャンセルされたことを示します。
    -   `pausing` : 操作が一時停止されていることを示します。
    -   `paused` : 操作が一時停止されていることを示します。この状態は、 [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)コマンドを使用して DDL ジョブを一時停止した場合にのみ表示されます。4 コマンド[`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)使用して DDL ジョブを再開できます。
    -   `done` : 操作は TiDB 所有者ノードで正常に実行されたが、他の TiDB ノードではこの DDL ジョブによって実行された変更がまだ同期されていないことを示します。
-   `COMMENTS` : 診断目的の追加情報が含まれます。
    -   `ingest` : [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)で構成された高速化されたインデックス バックフィルの追加のためのタスクを取り込みます。
    -   `txn` : [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)以降のトランザクションベースのインデックス バックフィルは無効になります。
    -   `txn-merge` : バックフィルが完了すると元のインデックスとマージされる一時インデックスを使用したトランザクション バックフィル。
    -   `DXF` : [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)で構成された Distributed eXecution Framework (DXF) を使用して実行されるタスク。
    -   `service_scope` : [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)で設定された TiDB ノードのサービス スコープ。
    -   `thread` : バックフィルタスクの同時実行数。初期値は`tidb_ddl_reorg_worker_cnt`に設定できます。4 [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md)指定することで動的な変更が可能です。
    -   `batch_size` : バックフィルタスクのバッチサイズ。初期値は`tidb_ddl_reorg_batch_size`に設定できます。4 `ADMIN ALTER DDL JOBS`指定することで動的な変更が可能です。
    -   `max_write_speed` : インジェストタスクのインポート時のフロー制御。初期値は`tidb_ddl_reorg_max_write_speed`に設定できます`ADMIN ALTER DDL JOBS`による動的な変更もサポートします。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `JOB_ID` : 各 DDL 操作は DDL ジョブに対応します。2 `JOB_ID`グローバルに一意です。
-   `DB_NAME` : DDL 操作が実行されるデータベースの名前。
-   `TABLE_NAME` : DDL 操作が実行されるテーブルの名前。
-   `JOB_TYPE` : DDL 操作のタイプ。
-   `SCHEMA_STATE` : DDLが操作するスキーマオブジェクトの現在の状態。2 が`JOB_TYPE` `ADD INDEX`場合はインデックスの状態、 `JOB_TYPE`が`ADD COLUMN`場合は列の状態、 `JOB_TYPE`が`CREATE TABLE`の場合はテーブルの状態です。一般的な状態には以下が含まれます。
    -   `none` : 存在しないことを示します。通常、 `DROP`操作の後、または`CREATE`操作が失敗してロールバックした後、 `none`状態になります。
    -   `delete only` ：これら`write reorganization` 4 `delete reorganization`の状態は中間状態です。それぞれの具体的な意味については、 [TiDBにおけるオンラインDDL非同期変更の仕組み](https://docs.pingcap.com/tidb/stable/ddl-introduction#how-the-online-ddl-asynchronous-change-works-in-tidb)参照してください。中間状態の変換は高速であるため、これらの状態`write only`通常、演算中は表示されません。10 `ADD INDEX`演算を実行する場合にのみ、 `write reorganization`状態が表示され、インデックスデータが追加されていることを示します。
    -   `public` : 存在し、ユーザーが利用できることを示します。通常、 `CREATE TABLE`と`ADD INDEX` （または`ADD COLUMN` ）の操作が完了すると、状態は`public`になり、新しく作成されたテーブル、列、およびインデックスが正常に読み書きできることを示します。
-   `SCHEMA_ID` : DDL 操作が実行されるデータベースの ID。
-   `TABLE_ID` : DDL 操作が実行されるテーブルの ID。
-   `ROW_COUNT` : `ADD INDEX`操作を実行すると、追加されたデータ行の数になります。
-   `START_TIME` : DDL 操作の開始時刻。
-   `STATE` : DDL操作の状態。一般的な状態は次のとおりです。
    -   `queueing` : 操作ジョブがDDLジョブキューに入ったものの、前のDDLジョブの完了を待機しているため実行されていないことを示します。別の理由としては、 `DROP`操作を実行した後、状態`none`になりますが、すぐに状態`synced`に更新され、すべてのTiDBインスタンスがその状態に同期されたことが考えられます。
    -   `running` : 操作が実行中であることを示します。
    -   `synced` : 操作が正常に実行され、すべての TiDB インスタンスがこの状態に同期されていることを示します。
    -   `rollback done` : 操作が失敗し、ロールバックが完了したことを示します。
    -   `rollingback` : 操作が失敗し、ロールバック中であることを示します。
    -   `cancelling` : 操作がキャンセルされていることを示します。この状態は、 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルした場合にのみ表示されます。
    -   `paused` : 操作が一時停止されていることを示します。この状態は、 [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)コマンドを使用して DDL ジョブを一時停止した場合にのみ表示されます。4 コマンド[`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)使用して DDL ジョブを再開できます。

</CustomContent>

次の例は`ADMIN SHOW DDL JOBS`の結果を示しています。

```sql
ADMIN SHOW DDL JOBS;
```

```sql
+--------+---------+------------+---------------------------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+----------+-------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE                        | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE    | COMMENTS    |
+--------+---------+------------+---------------------------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+----------+-------------+
|    565 | test    | sbtest1    | add index                       | write reorganization |       554 |      556 |         0 | 2024-11-22 12:39:25.475000 | 2024-11-22 12:39:25.524000 | NULL                       | running  | ingest, DXF |
|    566 | test    | sbtest1    | add index                       | none                 |       554 |      556 |         0 | 2024-11-22 12:39:26.425000 | NULL                       | NULL                       | queueing |             |
|    564 | test    | sbtest1    | alter table multi-schema change | none                 |       554 |      556 |         0 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:03.275000 | synced   |             |
|    564 | test    | sbtest1    | drop index /* subjob */         | none                 |       554 |      556 |         0 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:03.275000 | done     |             |
|    564 | test    | sbtest1    | drop index /* subjob */         | none                 |       554 |      556 |         0 | 2024-11-22 12:39:02.925000 | 2024-11-22 12:39:02.975000 | 2024-11-22 12:39:03.275000 | done     |             |
|    563 | test    | sbtest1    | modify column                   | public               |       554 |      556 |         0 | 2024-11-22 12:38:35.624000 | 2024-11-22 12:38:35.624000 | 2024-11-22 12:38:35.674000 | synced   |             |
|    562 | test    | sbtest1    | add index                       | public               |       554 |      556 |   1580334 | 2024-11-22 12:36:58.471000 | 2024-11-22 12:37:05.271000 | 2024-11-22 12:37:13.374000 | synced   | ingest, DXF |
|    561 | test    | sbtest1    | add index                       | public               |       554 |      556 |   1580334 | 2024-11-22 12:36:57.771000 | 2024-11-22 12:36:57.771000 | 2024-11-22 12:37:04.671000 | synced   | ingest, DXF |
|    560 | test    | sbtest1    | add index                       | public               |       554 |      556 |   1580334 | 2024-11-22 12:34:53.314000 | 2024-11-22 12:34:53.314000 | 2024-11-22 12:34:57.114000 | synced   | ingest      |
|    559 | test    | sbtest1    | drop index                      | none                 |       554 |      556 |         0 | 2024-11-22 12:34:43.565000 | 2024-11-22 12:34:43.565000 | 2024-11-22 12:34:43.764000 | synced   |             |
|    558 | test    | sbtest1    | add index                       | public               |       554 |      556 |   1580334 | 2024-11-22 12:34:06.215000 | 2024-11-22 12:34:06.215000 | 2024-11-22 12:34:14.314000 | synced   | ingest, DXF |
|    557 | test    | sbtest1    | create table                    | public               |       554 |      556 |         0 | 2024-11-22 12:32:09.515000 | 2024-11-22 12:32:09.915000 | 2024-11-22 12:32:10.015000 | synced   |             |
|    555 | test    |            | create schema                   | public               |       554 |        0 |         0 | 2024-11-22 12:31:51.215000 | 2024-11-22 12:31:51.264000 | 2024-11-22 12:31:51.264000 | synced   |             |
|    553 | test    |            | drop schema                     | none                 |         2 |        0 |         0 | 2024-11-22 12:31:48.615000 | 2024-11-22 12:31:48.615000 | 2024-11-22 12:31:48.865000 | synced   |             |
+--------+---------+------------+---------------------------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+----------+-------------+
14 rows in set (0.00 sec)
```

上記の出力から:

-   ジョブ565は現在進行中です（ `running`中`STATE` ）。スキーマ状態は現在`write reorganization`ですが、ジョブが完了すると`public`に切り替わります。これは、この変更がユーザーセッションから公開される可能性があるためです`end_time`列目も`NULL`なっており、これはジョブの完了時刻が現在不明であることを示しています。

-   `job_id` 566 の`STATE` `queueing`と表示され、キューイング中であることを示します。ジョブ 565 が完了し、ジョブ 566 の実行が開始されると、ジョブ 566 の`STATE` `running`に変わります。

-   インデックスやテーブルの削除などの破壊的な変更の場合、ジョブが完了すると`SCHEMA_STATE` `none`に変わります。追加的な変更の場合、 `SCHEMA_STATE` `public`に変わります。

表示される行数を制限するには、数値と where 条件を指定します。

```sql
ADMIN SHOW DDL JOBS [NUM] [WHERE where_condition];
```

-   `NUM` : 完了したDDLジョブキューの最後の`NUM`結果を表示します。指定しない場合は、デフォルトで`NUM` （10）になります。
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

DDL 履歴ジョブ キュー内の最後の 10 件の結果のうち、 `job_id`に該当する実行中の DDL ジョブのみを検索できます。

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

DDL履歴ジョブキュー内の任意の結果範囲から、 `job_id`に対応する実行中のDDLジョブを検索できます。この構文には、 `ADMIN SHOW DDL JOB QUERIES`の最後の10件の結果という制限はありません。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [DDLの紹介](/ddl-introduction.md)
-   [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
-   [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
-   [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
-   [`ADMIN ALTER DDL`](/sql-statements/sql-statement-admin-alter-ddl.md)
-   [情報スキーマ.DDL_JOBS](/information-schema/information-schema-ddl-jobs.md)
