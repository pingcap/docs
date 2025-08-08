---
title: SHOW INDEXES [FROM|IN] | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW INDEXES [FROM|IN] の使用法の概要。
---

# インデックスを表示 [FROM|IN] {#show-indexes-from-in}

文`SHOW INDEXES [FROM|IN]` 、指定されたテーブルのインデックスを一覧表示します。文`SHOW INDEX [FROM|IN]`と`SHOW KEYS [FROM|IN]`この文のエイリアスであり、MySQLとの互換性のために用意されています。

## 概要 {#synopsis}

```ebnf+diagram
ShowIndexStmt ::=
    "SHOW" ( "INDEX" | "INDEXES" | "KEYS" ) ("FROM" | "IN" ) TableName (("FROM" | "IN") SchemaName )? ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT, INDEX(col1));
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW INDEXES FROM t1;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| t1    |          0 | PRIMARY  |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       |
| t1    |          1 | col1     |            1 | col1        | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               | YES     | NULL       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
2 rows in set (0.00 sec)

mysql> SHOW INDEX FROM t1;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| t1    |          0 | PRIMARY  |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       |
| t1    |          1 | col1     |            1 | col1        | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               | YES     | NULL       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
2 rows in set (0.00 sec)

mysql> SHOW KEYS FROM t1;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| t1    |          0 | PRIMARY  |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       |
| t1    |          1 | col1     |            1 | col1        | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               | YES     | NULL       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
2 rows in set (0.00 sec)
```

TiDB `BTREE` `HASH`のインデックス タイプを`RTREE`ますが、無視されることに注意してください。

## MySQLの互換性 {#mysql-compatibility}

TiDBの`SHOW INDEXES [FROM|IN]`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
-   [インデックスの削除](/sql-statements/sql-statement-drop-index.md)
-   [インデックスの作成](/sql-statements/sql-statement-create-index.md)
-   [`information_schema.TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)
-   [`information_schema.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)
-   [`information_schema.KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)
-   [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)
