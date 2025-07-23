---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: 关于在 TiDB 数据库中使用 CREATE INDEX 的概述。
---

# CREATE INDEX

此语句用于为现有表添加新的索引。它是 [`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-alter-table.md) 的替代语法，出于 MySQL 兼容性考虑而包含。

## 概要

```ebnf+diagram
CreateIndexStmt ::=
    'CREATE' IndexKeyTypeOpt 'INDEX' IfNotExists Identifier IndexTypeOpt 'ON' TableName '(' IndexPartSpecificationList ')' IndexOptionList IndexLockAndAlgorithmOpt

IndexKeyTypeOpt ::=
    ( 'UNIQUE' | 'SPATIAL' | 'FULLTEXT' )?

IfNotExists ::=
    ( 'IF' 'NOT' 'EXISTS' )?

IndexTypeOpt ::=
    IndexType?

IndexPartSpecificationList ::=
    IndexPartSpecification ( ',' IndexPartSpecification )*

IndexOptionList ::=
    IndexOption*

IndexLockAndAlgorithmOpt ::=
    ( LockClause AlgorithmClause? | AlgorithmClause LockClause? )?

IndexType ::=
    ( 'USING' | 'TYPE' ) IndexTypeName

IndexPartSpecification ::=
    ( ColumnName OptFieldLen | '(' Expression ')' ) Order

IndexOption ::=
    'KEY_BLOCK_SIZE' '='? LengthNum
|   IndexType
|   'WITH' 'PARSER' Identifier
|   'COMMENT' stringLit
|   ("VISIBLE" | "INVISIBLE")
|   ("GLOBAL" | "LOCAL")

IndexTypeName ::=
    'BTREE'
|   'HASH'
|   'RTREE'

ColumnName ::=
    Identifier ( '.' Identifier ( '.' Identifier )? )?

OptFieldLen ::=
    FieldLen?

IndexNameList ::=
    ( Identifier | 'PRIMARY' )? ( ',' ( Identifier | 'PRIMARY' ) )*

KeyOrIndex ::=
    'Key' | 'Index'
```

## 示例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)

mysql> CREATE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)

mysql> ALTER TABLE t1 DROP INDEX c1;
Query OK, 0 rows affected (0.30 sec)

mysql> CREATE UNIQUE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.31 sec)
```

## 表达式索引

在某些场景下，查询的过滤条件基于某个表达式。在这些场景中，由于普通索引无法生效，查询只能通过扫描整个表来执行，导致性能较差。表达式索引是一种特殊索引，可以在表达式上创建。一旦创建了表达式索引，TiDB 就可以利用索引进行基于表达式的查询，从而显著提升查询性能。

例如，若你想基于 `LOWER(col1)` 创建索引，可以执行以下 SQL 语句：

```sql
CREATE INDEX idx1 ON t1 ((LOWER(col1)));
```

或者执行等价的语句：

```sql
ALTER TABLE t1 ADD INDEX idx1((LOWER(col1)));
```

你也可以在创建表时指定表达式索引：

```sql
CREATE TABLE t1 (
    col1 CHAR(10), 
    col2 CHAR(10),
    INDEX ((LOWER(col1)))
);
```

> **Note:**
>
> 表达式索引中的表达式必须用 `(` 和 `)` 包裹，否则会报语法错误。

你可以像删除普通索引一样删除表达式索引：

```sql
DROP INDEX idx1 ON t1;
```

表达式索引涉及多种表达式。为了确保正确性，只有一些经过充分测试的函数可以用于创建表达式索引。这意味着在生产环境中，只允许使用这些函数在表达式中。你可以通过查询 [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520) 变量获取这些函数。目前，允许的函数包括：

- [`JSON_ARRAY()`](/functions-and-operators/json-functions.md)
- [`JSON_ARRAY_APPEND()`](/functions-and-operators/json-functions.md)
- [`JSON_ARRAY_INSERT()`](/functions-and-operators/json-functions.md)
- [`JSON_CONTAINS()`](/functions-and-operators/json-functions.md)
- [`JSON_CONTAINS_PATH()`](/functions-and-operators/json-functions.md)
- [`JSON_DEPTH()`](/functions-and-operators/json-functions.md)
- [`JSON_EXTRACT()`](/functions-and-operators/json-functions.md)
- [`JSON_INSERT()`](/functions-and-operators/json-functions.md)
- [`JSON_KEYS()`](/functions-and-operators/json-functions.md)
- [`JSON_LENGTH()`](/functions-and-operators/json-functions.md)
- [`JSON_MERGE_PATCH()`](/functions-and-operators/json-functions.md)
- [`JSON_MERGE_PRESERVE()`](/functions-and-operators/json-functions.md)
- [`JSON_OBJECT()`](/functions-and-operators/json-functions.md)
- [`JSON_PRETTY()`](/functions-and-operators/json-functions.md)
- [`JSON_QUOTE()`](/functions-and-operators/json-functions.md)
- [`JSON_REMOVE()`](/functions-and-operators/json-functions.md)
- [`JSON_REPLACE()`](/functions-and-operators/json-functions.md)
- [`JSON_SCHEMA_VALID()`](/functions-and-operators/json-functions/json-functions-validate.md)
- [`JSON_SEARCH()`](/functions-and-operators/json-functions.md)
- [`JSON_SET()`](/functions-and-operators/json-functions.md)
- [`JSON_STORAGE_SIZE()`](/functions-and-operators/json-functions.md)
- [`JSON_TYPE()`](/functions-and-operators/json-functions.md)
- [`JSON_UNQUOTE()`](/functions-and-operators/json-functions.md)
- [`JSON_VALID()`](/functions-and-operators/json-functions.md)
- [`LOWER()`](/functions-and-operators/string-functions.md#lower)
- [`MD5()`](/functions-and-operators/encryption-and-compression-functions.md)
- [`REVERSE()`](/functions-and-operators/string-functions.md#reverse)
- [`TIDB_SHARD()`](/functions-and-operators/tidb-functions.md#tidb_shard)
- [`UPPER()`](/functions-and-operators/string-functions.md#upper)
- [`VITESS_HASH()`](/functions-and-operators/tidb-functions.md)

对于未包含在上述列表中的函数，这些函数未经过充分测试，不建议在生产环境中使用，属于实验性质。其他表达式如操作符、`CAST` 和 `CASE WHEN` 也被视为实验性质，不建议在生产环境中使用。

<CustomContent platform="tidb">

如果你仍希望使用这些表达式，可以在 [TiDB 配置文件](/tidb-configuration-file.md#allow-expression-index-new-in-v400) 中进行如下配置：

```sql
allow-expression-index = true
```

</CustomContent>

> **Note:**
>
> 不能在主键上创建表达式索引。
>
> 表达式索引中的表达式不能包含以下内容：
>
> - 易变函数，如 `RAND()` 和 `NOW()`。
> - [系统变量](/system-variables.md) 和 [用户变量](/user-defined-variables.md)。
> - 子查询。
> - [`AUTO_INCREMENT`](/auto-increment.md) 列。可以通过将 [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated) 设置为 `true` 来取消此限制。
> - [窗口函数](/functions-and-operators/window-functions.md)。
> - ROW 函数，例如 `CREATE TABLE t (j JSON, INDEX k (((j,j))));`。
> - [聚合函数](/functions-and-operators/aggregate-group-by-functions.md)。
>
> 表达式索引会隐式占用一个名称（例如 `_V$_{index_name}_{index_offset}`）。如果你试图用已存在的列名创建新的表达式索引，会报错。此外，添加同名新列也会报错。
>
> 确保表达式中函数参数的数量正确。
>
> 当索引表达式包含字符串相关函数时，受返回类型和长度影响，创建表达式索引可能会失败。在这种情况下，可以使用 `CAST()` 函数显式指定返回类型和长度。例如，要基于 `REPEAT(a, 3)` 创建表达式索引，可以将表达式修改为 `CAST(REPEAT(a, 3) AS CHAR(20))`。

当查询语句中的表达式与表达式索引中的表达式匹配时，优化器可以选择使用表达式索引。在某些情况下，优化器可能不会选择表达式索引，取决于统计信息。这时，可以通过使用优化器提示强制选择表达式索引。

以下示例假设你在表达式 `LOWER(col1)` 上创建了索引 `idx`：

如果查询结果中的表达式相同，则表达式索引适用。例如：

```sql
SELECT LOWER(col1) FROM t;
```

如果过滤条件中包含相同的表达式，则表达式索引适用。例如：

```sql
SELECT * FROM t WHERE LOWER(col1) = "a";
SELECT * FROM t WHERE LOWER(col1) > "a";
SELECT * FROM t WHERE LOWER(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE LOWER(col1) IN ("a", "b");
SELECT * FROM t WHERE LOWER(col1) > "a" AND LOWER(col1) < "b";
SELECT * FROM t WHERE LOWER(col1) > "b" OR LOWER(col1) < "a";
```

当按相同表达式排序时，表达式索引适用。例如：

```sql
SELECT * FROM t ORDER BY LOWER(col1);
```

如果在聚合（`GROUP BY`）函数中包含相同表达式，表达式索引也适用。例如：

```sql
SELECT MAX(LOWER(col1)) FROM t;
SELECT MIN(col1) FROM t GROUP BY LOWER(col1);
```

要查看对应的表达式索引，可以执行 [`SHOW INDEX`](/sql-statements/sql-statement-show-indexes.md)，或查询系统表 [`information_schema.tidb_indexes`](/information-schema/information-schema-tidb-indexes.md) 和表 [`information_schema.STATISTICS`](/information-schema/information-schema-statistics.md)。输出中的 `Expression` 列显示对应的表达式。对于非表达式索引，该列显示 `NULL`。

维护表达式索引的成本高于其他索引，因为每次插入或更新行时都需要计算表达式的值。索引中已存储表达式的值，因此优化器在选择表达式索引时无需重新计算。

因此，当查询性能优于插入和更新性能时，可以考虑对表达式建立索引。

表达式索引的语法和限制与 MySQL 相同。它们通过在不可见的虚拟生成列上创建索引实现，支持的表达式继承所有 [虚拟生成列的限制](/generated-columns.md#limitations)。

## 多值索引

多值索引是一种定义在数组列上的二级索引。在普通索引中，一个索引记录对应一条数据记录（1:1）。在多值索引中，多个索引记录对应一条数据记录（N:1）。多值索引用于索引 JSON 数组。例如，在 `zipcode` 字段上定义的多值索引会为 `zipcode` 数组中的每个元素生成一个索引记录。

```json
{
    "user":"Bob",
    "user_id":31,
    "zipcode":[94477,94536]
}
```

### 创建多值索引

你可以在索引定义中使用 [`CAST(... AS ... ARRAY)`](/functions-and-operators/cast-functions-and-operators.md#cast) 函数，类似创建表达式索引。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips((CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

你也可以将多值索引定义为唯一索引。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    UNIQUE INDEX zips( (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

定义为唯一索引的多值索引，如果插入重复数据会报错。

```sql
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1,2]}');
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [2,3]}');
ERROR 1062 (23000): Duplicate entry '2' for key 'customers.zips'
```

同一条记录可以有重复值，但不同记录有重复值时会报错。

```sql
-- 插入成功
mysql> INSERT INTO t1 VALUES('[1,1,2]');
mysql> INSERT INTO t1 VALUES('[3,3,3,4,4,4]');

-- 插入失败
mysql> INSERT INTO t1 VALUES('[1,2]');
mysql> INSERT INTO t1 VALUES('[2,3]');
```

你也可以将多值索引定义为复合索引：

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

定义为复合索引的多值索引中，多值部分可以出现在任何位置，但只能出现一次。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)), (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
ERROR 1235 (42000): This version of TiDB doesn't yet support 'more than one multi-valued key part per index'.
```

存储的数据必须与多值索引定义的类型完全一致，否则写入数据会失败：

```sql
-- zipcode 字段中的所有元素必须是 UNSIGNED 类型。
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [-1]}');
ERROR 3752 (HY000): Value is out of range for expression index 'zips' at row 1

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": ["1"]}'); -- 与 MySQL 不兼容
ERROR 3903 (HY000): Invalid JSON value for CAST for expression index 'zips'

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1]}');
Query OK, 1 row affected (0.00 sec)
```

### 使用多值索引

详见 [Index Selection - Use multi-valued indexes](/choose-index.md#use-multi-valued-indexes)。

### 限制

- 空 JSON 数组不会生成对应的索引记录。
- `CAST(... AS ... ARRAY)` 中的目标类型不能是 `BINARY`、`JSON`、`YEAR`、`FLOAT` 和 `DECIMAL`。源类型必须是 JSON。
- 不能用多值索引进行排序。
- 只能在 JSON 数组上创建多值索引。
- 多值索引不能作为主键或外键。
- 多值索引占用的额外存储空间 = 每行数组元素的平均数量 * 普通二级索引占用的空间。
- 与普通索引相比，DML 操作会修改更多的索引记录，因此多值索引的性能影响更大。
- 由于多值索引是特殊类型的表达式索引，具有与表达式索引相同的限制。
- 如果表使用多值索引，则不能用 BR、TiCDC 或 TiDB Lightning 备份、复制或导入到早于 v6.6.0 的 TiDB 集群。
- 对于复杂条件的查询，TiDB 可能无法选择多值索引。关于支持的条件模式，详见 [Use multi-valued indexes](/choose-index.md#use-multi-valued-indexes)。

## 不可见索引

默认情况下，不可见索引是被查询优化器忽略的索引：

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

从 TiDB v8.0.0 开始，你可以通过修改系统变量 [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) 让优化器选择不可见索引。

详情请参见 [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)。

## 相关系统变量

与 `CREATE INDEX` 语句相关的系统变量包括 `tidb_ddl_enable_fast_reorg`、`tidb_ddl_reorg_worker_cnt`、`tidb_ddl_reorg_batch_size`、`tidb_enable_auto_increment_in_generated` 和 `tidb_ddl_reorg_priority`。详细信息请参见 [system variables](/system-variables.md#tidb_ddl_reorg_worker_cnt)。

## MySQL 兼容性

* TiDB 支持解析 `FULLTEXT` 语法，但不支持使用 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引。
* TiDB 在语法中接受 `HASH`、`BTREE` 和 `RTREE` 等索引类型以兼容 MySQL，但会忽略它们。
* 不支持降序索引（类似于 MySQL 5.7）。
* 不支持向表添加 `CLUSTERED` 类型的主键。关于 `CLUSTERED` 主键的更多信息，请参见 [clustered index](/clustered-indexes.md)。
* 表达式索引与视图不兼容。当使用视图执行查询时，不能同时使用表达式索引。
* 表达式索引与绑定存在兼容性问题。当表达式索引的表达式中有常量时，为对应查询创建的绑定会扩大作用范围。例如，假设表达式索引中的表达式是 `a+1`，对应的查询条件是 `a+1 > 2`，此时创建的绑定为 `a+? > ?`，意味着条件如 `a+2 > 2` 的查询也会被强制使用表达式索引，导致执行计划不佳。此外，这也会影响 SQL 计划管理（SPM）中的基线捕获和基线演化。
* 多值索引写入的数据必须与定义的数据类型完全匹配，否则写入失败。详细信息请参见 [create multi-valued indexes](/sql-statements/sql-statement-create-index.md#create-multi-valued-indexes)。
* 将 `UNIQUE KEY` 设置为带有 `GLOBAL` 索引选项的 [全局索引](/partitioned-table.md#global-indexes) 是 TiDB 对 [分区表](/partitioned-table.md) 的扩展，不兼容 MySQL。

## 相关链接

* [Index Selection](/choose-index.md)
* [Wrong Index Solution](/wrong-index-solution.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
