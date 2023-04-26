---
title: PROCESSLIST
summary: Learn the `PROCESSLIST` information_schema table.
---

# プロセスリスト {#processlist}

`PROCESSLIST`は`SHOW PROCESSLIST`と同様に、処理中のリクエストを表示するために使用されます。

`PROCESSLIST`テーブルには、 `SHOW PROCESSLIST`には存在しない追加の列があります。

-   SQL ステートメントのダイジェストを表示する`DIGEST`列。
-   処理中のリクエストによって使用されたメモリをバイト単位で表示する`MEM`列。
-   ディスク使用量をバイト単位で表示する`DISK`列。
-   トランザクションの開始時刻を示す`TxnStart`列

{{< copyable "" >}}

```sql
USE information_schema;
DESC processlist;
```

```
+----------+---------------------+------+------+---------+-------+
| Field    | Type                | Null | Key  | Default | Extra |
+----------+---------------------+------+------+---------+-------+
| ID       | bigint(21) unsigned | NO   |      | 0       |       |
| USER     | varchar(16)         | NO   |      |         |       |
| HOST     | varchar(64)         | NO   |      |         |       |
| DB       | varchar(64)         | YES  |      | NULL    |       |
| COMMAND  | varchar(16)         | NO   |      |         |       |
| TIME     | int(7)              | NO   |      | 0       |       |
| STATE    | varchar(7)          | YES  |      | NULL    |       |
| INFO     | longtext            | YES  |      | NULL    |       |
| DIGEST   | varchar(64)         | YES  |      |         |       |
| MEM      | bigint(21) unsigned | YES  |      | NULL    |       |
| DISK     | bigint(21) unsigned | YES  |      | NULL    |       |
| TxnStart | varchar(64)         | NO   |      |         |       |
+----------+---------------------+------+------+---------+-------+
12 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM processlist\G
```

```
*************************** 1. row ***************************
      ID: 16
    USER: root
    HOST: 127.0.0.1
      DB: information_schema
 COMMAND: Query
    TIME: 0
   STATE: autocommit
    INFO: SELECT * FROM processlist
     MEM: 0
TxnStart:
1 row in set (0.00 sec)
```

`PROCESSLIST`テーブルのフィールドは次のとおりです。

-   ID: ユーザー接続の ID。
-   USER: `PROCESS`を実行しているユーザーの名前。
-   HOST: ユーザーが接続しているアドレス。
-   DB: 現在接続されているデフォルト データベースの名前。
-   COMMAND: `PROCESS`が実行しているコマンドの種類。
-   TIME: `PROCESS`の現在の実行時間 (秒単位)。
-   STATE: 現在の接続状態。
-   情報: 要求されたステートメントが処理されています。
-   DIGEST: SQL ステートメントのダイジェスト。
-   MEM: 処理中のリクエストが使用するメモリ(バイト単位)。
-   DISK: ディスクの使用量 (バイト単位)。
-   TxnStart: トランザクションの開始時刻。

## CLUSTER_PROCESSLIST {#cluster-processlist}

`CLUSTER_PROCESSLIST`は`PROCESSLIST`に対応するクラスタ システム テーブルです。クラスター内のすべての TiDB ノードの`PROCESSLIST`情報を照会するために使用されます。 `CLUSTER_PROCESSLIST`のテーブル スキーマには、 `PROCESSLIST`よりも 1 つ多い列`INSTANCE`列) があり、このデータ行の元の TiDB ノードのアドレスが格納されます。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```sql
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
| INSTANCE        | ID  | USER | HOST     | DB   | COMMAND | TIME | STATE      | INFO                                                 | MEM | TxnStart                               |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
| 10.0.1.22:10080 | 150 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077223) |
| 10.0.1.22:10080 | 138 | root | 10.0.1.1 | test | Query   | 0    | autocommit | SELECT * FROM information_schema.cluster_processlist | 0   | 05-28 03:54:21.230(416976223923077220) |
| 10.0.1.22:10080 | 151 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077224) |
| 10.0.1.21:10080 | 15  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077222) |
| 10.0.1.21:10080 | 14  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077225) |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
```
