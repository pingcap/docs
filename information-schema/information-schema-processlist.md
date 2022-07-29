---
title: PROCESSLIST
summary: Learn the `PROCESSLIST` information_schema table.
---

# プロセスリスト {#processlist}

`PROCESSLIST`は、 `SHOW PROCESSLIST`と同様に、処理されている要求を表示するために使用されます。

`PROCESSLIST`のテーブルには、 `SHOW PROCESSLIST`には存在しない追加の列があります。

-   処理中のリクエストで使用されているメモリをバイト単位で表示する`MEM`列。
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
| INFO     | binary(512)         | YES  |      | NULL    |       |
| MEM      | bigint(21) unsigned | YES  |      | NULL    |       |
| TxnStart | varchar(64)         | NO   |      |         |       |
+----------+---------------------+------+------+---------+-------+
10 rows in set (0.00 sec)
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

`PROCESSLIST`表のフィールドは次のように説明されています。

-   ID：ユーザー接続のID。
-   USER： `PROCESS`を実行しているユーザーの名前。
-   HOST：ユーザーが接続しているアドレス。
-   DB：現在接続されているデフォルトデータベースの名前。
-   コマンド： `PROCESS`が実行しているコマンドタイプ。
-   時間： `PROCESS`の現在の実行時間（秒単位）。
-   STATE：現在の接続状態。
-   情報：処理中の要求されたステートメント。
-   MEM：処理中のリクエストで使用されるメモリ（バイト単位）。
-   TxnStart：トランザクションの開始時刻。

## CLUSTER_PROCESSLIST {#cluster-processlist}

`CLUSTER_PROCESSLIST`は、 `PROCESSLIST`に対応するクラスタシステムテーブルです。これは、クラスタのすべてのTiDBノードの`PROCESSLIST`の情報を照会するために使用されます。 `CLUSTER_PROCESSLIST`のテーブルスキーマには、 `PROCESSLIST`よりも1つ多い列があります`INSTANCE`列には、このデータ行の元のTiDBノードのアドレスが格納されます。

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
