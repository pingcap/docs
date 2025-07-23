---
title: STATISTICS
summary: 了解 `STATISTICS` information_schema 表。
---

# STATISTICS

`STATISTICS` 表提供关于表索引的信息。

```sql
USE information_schema;
DESC statistics;
```

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| TABLE_CATALOG | varchar(512)  | YES  |      | NULL    |       |
| TABLE_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| TABLE_NAME    | varchar(64)   | YES  |      | NULL    |       |
| NON_UNIQUE    | varchar(1)    | YES  |      | NULL    |       |
| INDEX_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| INDEX_NAME    | varchar(64)   | YES  |      | NULL    |       |
| SEQ_IN_INDEX  | bigint(2)     | YES  |      | NULL    |       |
| COLUMN_NAME   | varchar(21)   | YES  |      | NULL    |       |
| COLLATION     | varchar(1)    | YES  |      | NULL    |       |
| CARDINALITY   | bigint(21)    | YES  |      | NULL    |       |
| SUB_PART      | bigint(3)     | YES  |      | NULL    |       |
| PACKED        | varchar(10)   | YES  |      | NULL    |       |
| NULLABLE      | varchar(3)    | YES  |      | NULL    |       |
| INDEX_TYPE    | varchar(16)   | YES  |      | NULL    |       |
| COMMENT       | varchar(16)   | YES  |      | NULL    |       |
| INDEX_COMMENT | varchar(1024) | YES  |      | NULL    |       |
| IS_VISIBLE    | varchar(3)    | YES  |      | NULL    |       |
| Expression    | varchar(64)   | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
18 行结果（0.00 秒）
```

`STATISTICS` 表中的字段说明如下：

* `TABLE_CATALOG`：包含索引的表所属的目录名称。该值始终为 `def`。
* `TABLE_SCHEMA`：包含索引的表所属的数据库名称。
* `TABLE_NAME`：包含索引的表的名称。
* `NON_UNIQUE`：如果索引不允许重复值，则值为 `0`；如果索引允许重复值，则值为 `1`。
* `INDEX_SCHEMA`：索引所属的数据库名称。
* `INDEX_NAME`：索引的名称。如果是主键，则该值始终为 `PRIMARY`。
* `SEQ_IN_INDEX`：索引中的列序号，从 `1` 开始。
* `COLUMN_NAME`：列名。请参阅 `Expression` 列的描述。
* `COLLATION`：索引中列的排序方式。值可以是 `A`（升序）、`D`（降序）或 `NULL`（未排序）。
* `CARDINALITY`：TiDB 不使用此字段。该字段的值始终为 `0`。
* `SUB_PART`：索引的前缀。如果只对列的部分前缀建立索引，则该值为索引字符数；如果对整个列建立索引，则该值为 `NULL`。
* `PACKED`：TiDB 不使用此字段。该值始终为 `NULL`。
* `NULLABLE`：如果该列可能包含 `NULL` 值，则值为 `YES`；否则为空字符串 `''`。
* `INDEX_TYPE`：索引的类型。
* `COMMENT`：与索引相关的其他信息。
* `INDEX_COMMENT`：创建索引时提供的带有注释属性的任何备注。
* `IS_VISIBLE`：该索引是否可见。详见 [Invisible index](/sql-statements/sql-statement-create-index.md#invisible-index)。
* `Expression`：非表达式部分的索引键，该值为 `NULL`；表达式部分的索引键，该值为表达式本身。详见 [Expression Index](/sql-statements/sql-statement-create-index.md#expression-index)。

以下语句等价：

```sql
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'

SHOW INDEX
  FROM tbl_name
  FROM db_name
```