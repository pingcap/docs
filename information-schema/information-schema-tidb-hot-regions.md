---
title: TIDB_HOT_REGIONS
summary: TIDB_HOT_REGIONS` information_schema テーブルについて学習します。
---

# TIDB_HOT_REGIONS {#tidb-hot-regions}

`TIDB_HOT_REGIONS`表は、現在のホットリージョンに関する情報を提供します。過去のホットリージョンに関する情報については、 `[TIDB_HOT_REGIONS_HISTORY](/information-schema/information-schema-tidb-hot-regions-history.md)`ご覧ください。

> **注記：**
>
> このテーブルは TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

```sql
USE information_schema;
DESC tidb_hot_regions;
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

`TIDB_HOT_REGIONS`表の列の説明は次のとおりです。

-   `TABLE_ID` : ホットリージョンが配置されているテーブルの ID。
-   `INDEX_ID` : ホットリージョンが配置されているインデックスの ID。
-   `DB_NAME` : ホットリージョンが配置されているオブジェクトのデータベース名。
-   `TABLE_NAME` : ホットリージョンが配置されているテーブルの名前。
-   `INDEX_NAME` : ホットリージョンが配置されているインデックスの名前。
-   `REGION_ID` : ホットリージョンの ID。
-   `TYPE` : ホットリージョンのタイプ。
-   `MAX_HOT_DEGREE` :リージョンの最大暑さ度。
-   `REGION_COUNT` : インスタンス内のホット領域の数。
-   `FLOW_BYTES` :リージョン内で書き込まれたバイト数と読み取られたバイト数。
