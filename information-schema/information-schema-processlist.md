---
title: PROCESSLIST
summary: Learn the `PROCESSLIST` information_schema table.
---

# プロセスリスト {#processlist}

`PROCESSLIST`は、 `SHOW PROCESSLIST`と同様に、処理されているリクエストを表示するために使用されます。

`PROCESSLIST`テーブルには、 `SHOW PROCESSLIST`に存在しない追加の列があります。

-   SQL ステートメントのダイジェストを表示する`DIGEST`列。
-   `MEM`列は、処理中のリクエストによって使用されているメモリをバイト単位で示します。
-   ディスク使用量をバイト単位で示す`DISK`列。
-   トランザクションの開始時間を示す`TxnStart`列。
-   `RESOURCE_GROUP`列にはリソース グループ名が表示されます。

```sql
USE information_schema;
DESC processlist;
```

```sql
+---------------------+---------------------+------+------+---------+-------+
| Field               | Type                | Null | Key  | Default | Extra |
+---------------------+---------------------+------+------+---------+-------+
| ID                  | bigint(21) unsigned | NO   |      | 0       |       |
| USER                | varchar(16)         | NO   |      |         |       |
| HOST                | varchar(64)         | NO   |      |         |       |
| DB                  | varchar(64)         | YES  |      | NULL    |       |
| COMMAND             | varchar(16)         | NO   |      |         |       |
| TIME                | int(7)              | NO   |      | 0       |       |
| STATE               | varchar(7)          | YES  |      | NULL    |       |
| INFO                | longtext            | YES  |      | NULL    |       |
| DIGEST              | varchar(64)         | YES  |      |         |       |
| MEM                 | bigint(21) unsigned | YES  |      | NULL    |       |
| DISK                | bigint(21) unsigned | YES  |      | NULL    |       |
| TxnStart            | varchar(64)         | NO   |      |         |       |
| RESOURCE_GROUP      | varchar(32)         | NO   |      |         |       |
+---------------------+---------------------+------+------+---------+-------+
13 rows in set (0.00 sec)
```

```sql
SELECT * FROM processlist\G
```

```sql
*************************** 1. row ***************************
                 ID: 2300033189772525975
               USER: root
               HOST: 127.0.0.1:51289
                 DB: NULL
            COMMAND: Query
               TIME: 0
              STATE: autocommit
               INFO: SELECT * FROM processlist
             DIGEST: dbfaa16980ec628011029f0aaf0d160f4b040885240dfc567bf760d96d374f7e
                MEM: 0
               DISK: 0
           TxnStart:
     RESOURCE_GROUP: rg1
1 row in set (0.00 sec)
```

`PROCESSLIST`テーブルのフィールドは次のように説明されています。

-   ID: ユーザー接続の ID。
-   USER: `PROCESS`を実行しているユーザーの名前。
-   HOST: ユーザーが接続しているアドレス。
-   DB: 現在接続されているデフォルトのデータベースの名前。
-   COMMAND: `PROCESS`が実行しているコマンドの種類。
-   TIME: 現在の実行期間`PROCESS` (秒単位)。
-   STATE: 現在の接続状態。
-   情報: 処理中の要求されたステートメント。
-   DIGEST: SQL ステートメントのダイジェスト。
-   MEM: 処理中のリクエストによって使用されるメモリ(バイト単位)。
-   DISK: ディスク使用量 (バイト単位)。
-   TxnStart: トランザクションの開始時刻。
-   RESOURCE_GROUP: リソースグループ名。

## CLUSTER_PROCESSLIST {#cluster-processlist}

`CLUSTER_PROCESSLIST`は`PROCESSLIST`に対応するクラスタシステムテーブルです。これは、クラスター内の`PROCESSLIST`の TiDB ノードの情報を照会するために使用されます。 `CLUSTER_PROCESSLIST`のテーブル スキーマには`PROCESSLIST`よりも 1 列多い`INSTANCE`列があり、この列のデータの元の TiDB ノードのアドレスが格納されます。

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```sql
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+----------------+
| INSTANCE        | ID  | USER | HOST     | DB   | COMMAND | TIME | STATE      | INFO                                                 | MEM | TxnStart                               | RESOURCE_GROUP | 
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+----------------+

| 10.0.1.22:10080 | 150 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077223) | default        |
| 10.0.1.22:10080 | 138 | root | 10.0.1.1 | test | Query   | 0    | autocommit | SELECT * FROM information_schema.cluster_processlist | 0   | 05-28 03:54:21.230(416976223923077220) | rg1            |
| 10.0.1.22:10080 | 151 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077224) | rg2            |
| 10.0.1.21:10080 | 15  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077222) | default        |
| 10.0.1.21:10080 | 14  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077225) | default        |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+----------------+
```
