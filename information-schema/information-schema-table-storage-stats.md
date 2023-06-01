---
title: TABLE_STORAGE_STATS
summary: Learn the `TABLE_STORAGE_STATS` INFORMATION_SCHEMA table.
---

# TABLE_STORAGE_STATS {#table-storage-stats}

`TABLE_STORAGE_STATS`テーブルは、storageエンジン (TiKV) によって格納されるテーブル サイズに関する情報を提供します。

```sql
USE INFORMATION_SCHEMA;
DESC TABLE_STORAGE_STATS;
```

出力は次のとおりです。

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA       | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME         | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID           | bigint(21)  | YES  |      | NULL    |       |
| PEER_COUNT         | bigint(21)  | YES  |      | NULL    |       |
| REGION_COUNT       | bigint(21)  | YES  |      | NULL    |       |
| EMPTY_REGION_COUNT | bigint(21)  | YES  |      | NULL    |       |
| TABLE_SIZE         | bigint(64)  | YES  |      | NULL    |       |
| TABLE_KEYS         | bigint(64)  | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

```sql
CREATE TABLE test.t1 (id INT);
INSERT INTO test.t1 VALUES (1);
SELECT * FROM TABLE_STORAGE_STATS WHERE table_schema = 'test' AND table_name = 't1'\G
```

出力は次のとおりです。

```sql
*************************** 1. row ***************************
      TABLE_SCHEMA: test
        TABLE_NAME: t1
          TABLE_ID: 56
        PEER_COUNT: 1
      REGION_COUNT: 1
EMPTY_REGION_COUNT: 1
        TABLE_SIZE: 1
        TABLE_KEYS: 0
1 row in set (0.00 sec)
```

`TABLE_STORAGE_STATS`テーブルのフィールドは次のように説明されています。

-   `TABLE_SCHEMA` : テーブルが属するスキーマの名前。
-   `TABLE_NAME` : テーブルの名前。
-   `TABLE_ID` : テーブルの ID。
-   `PEER_COUNT` : テーブルのレプリカの数。
-   `REGION_COUNT` : リージョンの数。
-   `EMPTY_REGION_COUNT` : このテーブルにデータが含まれていないリージョンの数。
-   `TABLE_SIZE` : テーブルの合計サイズ (MiB 単位)。
-   `TABLE_KEYS` : テーブル内のレコードの総数。
