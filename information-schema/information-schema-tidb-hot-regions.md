---
title: TIDB_HOT_REGIONS
summary: Learn the `TIDB_HOT_REGIONS` information_schema table.
---

# TIDB_HOT_REGIONS {#tidb-hot-regions}

`TIDB_HOT_REGIONS`の表は、現在のホットリージョンに関する情報を提供します。歴史的なホットリージョンについては、 `[TIDB_HOT_REGIONS_HISTORY](/information-schema/information-schema-tidb-hot-regions-history.md)`を参照してください。

{{< copyable "" >}}

```sql
USE information_schema;
DESC tidb_hot_regions;
```

```
+----------------+-------------+------+------+---------+-------+
| Field          | Type        | Null | Key  | Default | Extra |
+----------------+-------------+------+------+---------+-------+
| TABLE_ID       | bigint(21)  | YES  |      | NULL    |       |
| INDEX_ID       | bigint(21)  | YES  |      | NULL    |       |
| DB_NAME        | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME     | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME     | varchar(64) | YES  |      | NULL    |       |
| REGION_ID      | bigint(21)  | YES  |      | NULL    |       |
| TYPE           | varchar(64) | YES  |      | NULL    |       |
| MAX_HOT_DEGREE | bigint(21)  | YES  |      | NULL    |       |
| REGION_COUNT   | bigint(21)  | YES  |      | NULL    |       |
| FLOW_BYTES     | bigint(21)  | YES  |      | NULL    |       |
+----------------+-------------+------+------+---------+-------+
10 rows in set (0.00 sec)
```

`TIDB_HOT_REGIONS`テーブルの列の説明は次のとおりです。

-   `TABLE_ID` ：ホットリージョンが配置されているテーブルのID。
-   `INDEX_ID` ：ホットリージョンが配置されているインデックスのID。
-   `DB_NAME` ：ホットリージョンが配置されているオブジェクトのデータベース名。
-   `TABLE_NAME` ：ホットリージョンが配置されているテーブルの名前。
-   `INDEX_NAME` ：ホットリージョンが配置されているインデックスの名前。
-   `REGION_ID` ：ホットリージョンのID。
-   `TYPE` ：ホットリージョンのタイプ。
-   `MAX_HOT_DEGREE` ：リージョンの最大ホット度。
-   `REGION_COUNT` ：インスタンス内のホットリージョンの数。
-   `FLOW_BYTES` ：リージョンで書き込まれ、読み取られたバイト数。
