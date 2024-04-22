---
title: TIDB_SERVERS_INFO
summary: 表`TIDB_SERVERS_INFO`は、TiDBクラスタ内のTiDBサーバーに関する情報を提供します。このテーブルはTiDBサーバーレスクラスターでは使用できません。フィールドにはDDL_ID、IP、PORT、STATUS_PORT、LEASE、VERSION、GIT_HASH、BINLOG_STATUS、LABELSが含まれます。ビューを作成すると、サーバーの情報が表示されます。
---

# TIDB_SERVERS_INFO {#tidb-servers-info}

表`TIDB_SERVERS_INFO`は、TiDBクラスタ内の TiDB サーバー (つまり、tidb-server プロセス) に関する情報を提供します。

> **注記：**
>
> このテーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

```sql
USE INFORMATION_SCHEMA;
DESC tidb_servers_info;
```

出力は次のとおりです。

```sql
+---------------+--------------+------+------+---------+-------+
| Field         | Type         | Null | Key  | Default | Extra |
+---------------+--------------+------+------+---------+-------+
| DDL_ID        | varchar(64)  | YES  |      | NULL    |       |
| IP            | varchar(64)  | YES  |      | NULL    |       |
| PORT          | bigint(21)   | YES  |      | NULL    |       |
| STATUS_PORT   | bigint(21)   | YES  |      | NULL    |       |
| LEASE         | varchar(64)  | YES  |      | NULL    |       |
| VERSION       | varchar(64)  | YES  |      | NULL    |       |
| GIT_HASH      | varchar(64)  | YES  |      | NULL    |       |
| BINLOG_STATUS | varchar(64)  | YES  |      | NULL    |       |
| LABELS        | varchar(128) | YES  |      | NULL    |       |
+---------------+--------------+------+------+---------+-------+
9 rows in set (0.00 sec)
```

`TIDB_SERVERS_INFO`テーブルをビュー。

```sql
SELECT * FROM TIDB_SERVERS_INFO\G
```

出力は次のとおりです。

```sql
*************************** 1. row ***************************
       DDL_ID: 771c169d-0a3a-48ea-a93c-a4d6751d3674
           IP: 0.0.0.0
         PORT: 4000
  STATUS_PORT: 10080
        LEASE: 45s
      VERSION: 8.0.11-TiDB-v7.5.1
     GIT_HASH: 827d8ff2d22ac4c93ae1b841b79d468211e1d393
BINLOG_STATUS: Off
       LABELS:
1 row in set (0.006 sec)
```
