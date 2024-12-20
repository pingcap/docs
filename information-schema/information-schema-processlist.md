---
title: PROCESSLIST
summary: PROCESSLIST` information_schema テーブルについて学習します。
---

# プロセスリスト {#processlist}

`PROCESSLIST`は[`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md)と同様に、処理中のリクエストを表示するために使用されます。

`PROCESSLIST`テーブルには`SHOW PROCESSLIST`にはない追加の列があります。

<CustomContent platform="tidb">

-   SQL ステートメントのダイジェストを表示する`DIGEST`列。
-   処理中のリクエストによって使用されるメモリをバイト単位で表示する`MEM`列。
-   ディスク使用量をバイト単位で表示する`DISK`列。
-   トランザクションの開始時刻を表示する`TxnStart`列。
-   リソース グループ名を表示する`RESOURCE_GROUP`列。
-   現在のセッションのエイリアスを表示する`SESSION_ALIAS`列。
-   ステートメントによって現在影響を受けている行数を示す`ROWS_AFFECTED`列。
-   `TIDB_CPU`列は、ステートメントが TiDBサーバーのCPU を消費する時間をナノ秒単位で表示します。この列には、 [Top SQL](/dashboard/top-sql.md)機能が有効な場合にのみ意味のある値が表示されます。それ以外の場合、値は`0`になります。
-   ステートメントが TiKVサーバーCPU を消費する時間をナノ秒単位で表示する`TIKV_CPU`列。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   SQL ステートメントのダイジェストを表示する`DIGEST`列。
-   処理中のリクエストによって使用されるメモリをバイト単位で表示する`MEM`列。
-   ディスク使用量をバイト単位で表示する`DISK`列。
-   トランザクションの開始時刻を表示する`TxnStart`列。
-   リソース グループ名を表示する`RESOURCE_GROUP`列。
-   現在のセッションのエイリアスを表示する`SESSION_ALIAS`列。
-   ステートメントによって現在影響を受けている行数を示す`ROWS_AFFECTED`列。
-   `TIDB_CPU`列は、ステートメントが TiDBサーバーのCPU を消費する時間をナノ秒単位で表示します。この列には、 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)機能が有効な場合にのみ意味のある値が表示されます。それ以外の場合、値は`0`になります。
-   ステートメントが TiKVサーバーCPU を消費する時間をナノ秒単位で表示する`TIKV_CPU`列。

</CustomContent>

```sql
USE information_schema;
DESC processlist;
```

```sql
+----------------+---------------------+------+------+---------+-------+
| Field          | Type                | Null | Key  | Default | Extra |
+----------------+---------------------+------+------+---------+-------+
| ID             | bigint(21) unsigned | NO   |      | 0       |       |
| USER           | varchar(16)         | NO   |      |         |       |
| HOST           | varchar(64)         | NO   |      |         |       |
| DB             | varchar(64)         | YES  |      | NULL    |       |
| COMMAND        | varchar(16)         | NO   |      |         |       |
| TIME           | int(7)              | NO   |      | 0       |       |
| STATE          | varchar(7)          | YES  |      | NULL    |       |
| INFO           | longtext            | YES  |      | NULL    |       |
| DIGEST         | varchar(64)         | YES  |      |         |       |
| MEM            | bigint(21) unsigned | YES  |      | NULL    |       |
| DISK           | bigint(21) unsigned | YES  |      | NULL    |       |
| TxnStart       | varchar(64)         | NO   |      |         |       |
| RESOURCE_GROUP | varchar(32)         | NO   |      |         |       |
| SESSION_ALIAS  | varchar(64)         | NO   |      |         |       |
| ROWS_AFFECTED  | bigint(21) unsigned | YES  |      | NULL    |       |
| TIDB_CPU       | bigint(21)          | NO   |      | 0       |       |
| TIKV_CPU       | bigint(21)          | NO   |      | 0       |       |
+----------------+---------------------+------+------+---------+-------+
```

```sql
SELECT * FROM information_schema.processlist\G
```

```sql
*************************** 1. row ***************************
            ID: 1268776964
          USER: root
          HOST: 127.0.0.1:59922
            DB: NULL
       COMMAND: Query
          TIME: 0
         STATE: autocommit
          INFO: SELECT * FROM information_schema.processlist
        DIGEST: 4b5e7cdd5d3ed84d6c1a6d56403a3d512554b534313caf296268abdec1c9ea99
           MEM: 0
          DISK: 0
      TxnStart:
RESOURCE_GROUP: default
 SESSION_ALIAS:
 ROWS_AFFECTED: 0
      TIDB_CPU: 0
      TIKV_CPU: 0
```

`PROCESSLIST`テーブル内のフィールドは次のように説明されます。

<CustomContent platform="tidb">

-   `ID` : ユーザー接続の ID。
-   `USER` : `PROCESS`を実行しているユーザーの名前。
-   `HOST` : ユーザーが接続しているアドレス。
-   `DB` : 現在接続されているデフォルト データベースの名前。
-   `COMMAND` : `PROCESS`が実行しているコマンドの種類。
-   `TIME` : 現在の実行時間`PROCESS` (秒単位)。
-   `STATE` : 現在の接続状態。
-   `INFO` : 処理中の要求されたステートメント。
-   `DIGEST` : SQL ステートメントのダイジェスト。
-   `MEM` : 処理中のリクエストによって使用されるメモリ（バイト単位）。
-   `DISK` : ディスク使用量（バイト単位）。
-   `TxnStart` : トランザクションの開始時刻。
-   `RESOURCE_GROUP` : リソース グループ名。
-   `SESSION_ALIAS` : 現在のセッションのエイリアス。
-   `ROWS_AFFECTED` : 現在ステートメントによって影響を受けている行の数。
-   `TIDB_CPU` : ステートメントが TiDBサーバーのCPU を消費する時間 (ナノ秒単位)。この列には、 [Top SQL](/dashboard/top-sql.md)機能が有効な場合にのみ意味のある値が表示されます。それ以外の場合、値は`0`になります。
-   `TIKV_CPU` : ステートメントが TiKVサーバーCPU を消費する時間 (ナノ秒単位)。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `ID` : ユーザー接続の ID。
-   `USER` : `PROCESS`を実行しているユーザーの名前。
-   `HOST` : ユーザーが接続しているアドレス。
-   `DB` : 現在接続されているデフォルト データベースの名前。
-   `COMMAND` : `PROCESS`が実行しているコマンドの種類。
-   `TIME` : 現在の実行時間`PROCESS` (秒単位)。
-   `STATE` : 現在の接続状態。
-   `INFO` : 処理中の要求されたステートメント。
-   `DIGEST` : SQL ステートメントのダイジェスト。
-   `MEM` : 処理中のリクエストによって使用されるメモリ（バイト単位）。
-   `DISK` : ディスク使用量（バイト単位）。
-   `TxnStart` : トランザクションの開始時刻。
-   `RESOURCE_GROUP` : リソース グループ名。
-   `SESSION_ALIAS` : 現在のセッションのエイリアス。
-   `ROWS_AFFECTED` : 現在ステートメントによって影響を受けている行の数。
-   `TIDB_CPU` : ステートメントが TiDBサーバーのCPU を消費する時間 (ナノ秒単位)。この列には、 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql)機能が有効な場合にのみ意味のある値が表示されます。それ以外の場合、値は`0`になります。
-   `TIKV_CPU` : ステートメントが TiKVサーバーCPU を消費する時間 (ナノ秒単位)。

</CustomContent>

## クラスタープロセスリスト {#cluster-processlist}

`CLUSTER_PROCESSLIST` `PROCESSLIST`に対応するクラスター システム テーブルです。クラスター内のすべての TiDB ノードの`PROCESSLIST`情報を照会するために使用されます。 `CLUSTER_PROCESSLIST`のテーブル スキーマには`PROCESSLIST`よりも 1 つ多い列、つまり`INSTANCE`列があり、このデータ行の元の TiDB ノードのアドレスが格納されます。

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```sql
+-----------------+------------+------+-----------------+------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+------+----------------------------------------+----------------+---------------+---------------+----------+----------+
| INSTANCE        | ID         | USER | HOST            | DB   | COMMAND | TIME | STATE      | INFO                                                 | DIGEST                                                           | MEM  | DISK | TxnStart                               | RESOURCE_GROUP | SESSION_ALIAS | ROWS_AFFECTED | TIDB_CPU | TIKV_CPU |
+-----------------+------------+------+-----------------+------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+------+----------------------------------------+----------------+---------------+---------------+----------+----------+
| 127.0.0.1:10080 | 1268776964 | root | 127.0.0.1:59922 | NULL | Query   |    0 | autocommit | SELECT * FROM information_schema.cluster_processlist | b1e38e59fbbc3e2b35546db5c8053040db989a497ac6cd71ff8dd4394395701a |    0 |    0 | 07-29 12:39:24.282(451471727468740609) | default        |               |             0 |        0 |        0 |
+-----------------+------------+------+-----------------+------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+------+----------------------------------------+----------------+---------------+---------------+----------+----------+
```
