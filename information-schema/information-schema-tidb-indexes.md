---
title: TIDB_INDEXES
summary: Learn the `TIDB_INDEXES` information_schema table.
---

# TIDB_INDEXES {#tidb-indexes}

`TIDB_INDEXES`テーブルは、すべてのテーブルの INDEX 情報を提供します。

```sql
USE information_schema;
DESC tidb_indexes;
```

    +---------------+---------------+------+------+---------+-------+
    | Field         | Type          | Null | Key  | Default | Extra |
    +---------------+---------------+------+------+---------+-------+
    | TABLE_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
    | TABLE_NAME    | varchar(64)   | YES  |      | NULL    |       |
    | NON_UNIQUE    | bigint(21)    | YES  |      | NULL    |       |
    | KEY_NAME      | varchar(64)   | YES  |      | NULL    |       |
    | SEQ_IN_INDEX  | bigint(21)    | YES  |      | NULL    |       |
    | COLUMN_NAME   | varchar(64)   | YES  |      | NULL    |       |
    | SUB_PART      | bigint(21)    | YES  |      | NULL    |       |
    | INDEX_COMMENT | varchar(2048) | YES  |      | NULL    |       |
    | Expression    | varchar(64)   | YES  |      | NULL    |       |
    | INDEX_ID      | bigint(21)    | YES  |      | NULL    |       |
    | IS_VISIBLE    | varchar(64)   | YES  |      | NULL    |       |
    | CLUSTERED     | varchar(64)   | YES  |      | NULL    |       |
    +---------------+---------------+------+------+---------+-------+
    12 rows in set (0.00 sec)

`INDEX_ID`は、TiDB が各インデックスに割り当てる一意の ID です。別のテーブルまたは API から取得した`INDEX_ID`の結合操作を行うために使用できます。

たとえば、 [`SLOW_QUERY`テーブル](/information-schema/information-schema-slow-query.md)の遅いクエリに関係する`TABLE_ID`と`INDEX_ID`を取得し、次の SQL ステートメントを使用して特定のインデックス情報を取得できます。

```sql
SELECT
 tidb_indexes.*
FROM
 tidb_indexes,
 tables
WHERE
  tidb_indexes.table_schema = tables.table_schema
 AND tidb_indexes.table_name = tidb_indexes.table_name
 AND tables.tidb_table_id = ?
 AND index_id = ?
```

`TIDB_INDEXES`テーブルのフィールドは次のように説明されています。

-   `TABLE_SCHEMA` : インデックスが属するスキーマの名前。
-   `TABLE_NAME` : インデックスが属するテーブルの名前。
-   `NON_UNIQUE` : インデックスが一意の場合、値は`0`です。それ以外の場合、値は`1`です。
-   `KEY_NAME` : インデックス名。インデックスが主キーの場合、名前は`PRIMARY`です。
-   `SEQ_IN_INDEX` : `1`から始まるインデックス内の列の連続番号。
-   `COLUMN_NAME` : インデックスが配置されている列の名前。
-   `SUB_PART` : インデックスのプレフィックス長。列が部分的にインデックス付けされている場合、値`SUB_PART`はインデックス付けされた文字の数になります。それ以外の場合、値は`NULL`です。
-   `INDEX_COMMENT` : インデックスのコメント。インデックスの作成時に作成されます。
-   `INDEX_ID` : インデックス ID。
-   `IS_VISIBLE` : インデックスが表示されるかどうか。
-   `CLUSTERED` : [クラスター化インデックス](/clustered-indexes.md)かどうか。
