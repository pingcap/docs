---
title: ADMIN ALTER DDL JOBS
summary: TiDBデータベースにおけるADMIN ALTER DDL JOBS`の使用方法の概要。
---

# 管理者によるDDLジョブの変更 {#admin-alter-ddl-jobs}

> **注記：**
>
> 現在、この機能は[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

`ADMIN ALTER DDL JOBS`ステートメントを使用すると、実行中の単一の DDL ジョブのパラメーターを変更できます。例:

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
```

-   `101` : DDL ジョブの ID を示します。この ID は、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)実行することで取得できます。
-   `THREAD` : DDL ジョブの同時実行数を示します。システム変数[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)を使用して初期値を構成できます。

`ADMIN ALTER DDL JOBS`ステートメントでサポートされている DDL ジョブ タイプには、 `ADD INDEX` 、 `MODIFY COLUMN` 、および`REORGANIZE PARTITION`が含まれます。その他の DDL ジョブ タイプの場合、 `ADMIN ALTER DDL JOBS`を実行すると`unsupported DDL operation`エラーが返されます。

現在、 `ADMIN ALTER DDL JOBS`を実行することで、単一の DDL ジョブのパラメータのみを変更できます。複数の DDL ジョブ ID のパラメータを同時に変更することはサポートされていません。

以下は、さまざまなDDLジョブでサポートされているパラメータと、それに対応するシステム変数です。

-   `ADD INDEX` :

    -   `THREAD` : DDL ジョブの同時実行数。初期値は`tidb_ddl_reorg_worker_cnt`で設定されます。
    -   `BATCH_SIZE` : バッチサイズ。初期値は[`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)で設定されます。
    -   `MAX_WRITE_SPEED` : 各 TiKV にインデックス レコードをインポートするための最大帯域幅制限。初期値は[`tidb_ddl_reorg_max_write_speed`](/system-variables.md#tidb_ddl_reorg_max_write_speed-new-in-v6512-v755-and-v850)によって設定されます。

    TiDB バージョン v8.5.5 より前のバージョンでは、上記のパラメータは[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)が無効になった後に送信され実行されている`ADD INDEX`ジョブに対してのみ機能することに注意してください。

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premiumでは、 `THREAD`と`MAX_WRITE_SPEED`は自動的に適切な値に調整されるため、ユーザーが変更することはできません。これらの設定を調整する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

-   `MODIFY COLUMN` :
    -   `THREAD` : DDL ジョブの同時実行数。初期値は`tidb_ddl_reorg_worker_cnt`で設定されます。
    -   `BATCH_SIZE` : バッチサイズ。初期値は`tidb_ddl_reorg_batch_size`で設定されます。

-   `REORGANIZE PARTITION` :
    -   `THREAD` : DDL ジョブの同時実行数。初期値は`tidb_ddl_reorg_worker_cnt`で設定されます。
    -   `BATCH_SIZE` : バッチサイズ。初期値は`tidb_ddl_reorg_batch_size`で設定されます。

前述のパラメータの値の範囲は、対応するシステム変数の値の範囲と一致しています。

`ADMIN ALTER DDL JOBS`実行中の DDL ジョブに対してのみ有効です。DDL ジョブが存在しない場合、または既に完了している場合は、このステートメントを実行すると`ddl job is not running`エラーが返されます。

以下に、この記述の例をいくつか示します。

```sql
ADMIN ALTER DDL JOBS 101 THREAD = 8;
ADMIN ALTER DDL JOBS 101 BATCH_SIZE = 256;
ADMIN ALTER DDL JOBS 101 MAX_WRITE_SPEED = '200MiB';
ADMIN ALTER DDL JOBS 101 THREAD = 8, BATCH_SIZE = 256;
```

特定の DDL ジョブの現在のパラメータ値を表示するには、 `ADMIN SHOW DDL JOBS`を実行します。結果は`COMMENTS`列に表示されます。

```sql
ADMIN SHOW DDL JOBS 1;
```

    +--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE  | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE  | COMMENTS              |
    +--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
    |    124 | test    | t          | add index | public       |         2 |      122 |         3 | 2024-11-15 11:17:06.213000 | 2024-11-15 11:17:06.213000 | 2024-11-15 11:17:08.363000 | synced | ingest, DXF, thread=8 |
    +--------+---------+------------+-----------+--------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+--------+-----------------------+
    1 row in set (0.01 sec)

## あらすじ {#synopsis}

```ebnf+diagram
AdminAlterDDLStmt ::=
    'ADMIN' 'ALTER' 'DDL' 'JOBS' Int64Num AlterJobOptionList

AlterJobOptionList ::=
    AlterJobOption ( ',' AlterJobOption )*

AlterJobOption ::=
    identifier "=" SignedLiteral
```

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)
-   [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)
-   [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)
-   [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)
