---
title: CREATE INDEX | TiDB SQL 语句参考
summary: TiDB 数据库中 CREATE INDEX 的用法概述。
---

# CREATE INDEX

该语句用于为已存在的表添加新索引。它是 [`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-alter-table.md) 的另一种语法形式，并为兼容 MySQL 而提供。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 对于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群（4 vCPU），建议手动关闭 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)，以防止在创建索引期间资源限制影响集群稳定性。关闭该设置后，索引将通过事务方式创建，从而降低对集群的整体影响。

</CustomContent>

## 语法

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

在某些场景下，查询的过滤条件基于某个表达式。在这些场景下，由于普通索引无法生效，查询只能通过全表扫描来执行，导致查询性能较差。表达式索引是一种可以在表达式上创建的特殊索引。创建表达式索引后，TiDB 可以针对基于表达式的查询使用该索引，从而显著提升查询性能。

例如，如果你希望基于 `LOWER(col1)` 创建索引，可以执行如下 SQL 语句：

```sql
CREATE INDEX idx1 ON t1 ((LOWER(col1)));
```

或者你也可以执行如下等价语句：

```sql
ALTER TABLE t1 ADD INDEX idx1((LOWER(col1)));
```

你还可以在建表时指定表达式索引：

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

表达式索引涉及多种表达式。为保证正确性，仅允许使用部分经过充分测试的函数来创建表达式索引。这意味着在生产环境中，表达式中只能使用这些函数。你可以通过查询 [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520) 变量获取这些函数。目前允许的函数如下：

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

对于未包含在上述列表中的函数，这些函数尚未经过充分测试，不建议在生产环境中使用，可视为实验性特性。其他表达式如运算符、`CAST`、`CASE WHEN` 等也属于实验性特性，不建议在生产环境中使用。

<CustomContent platform="tidb">

如果你仍然希望使用这些表达式，可以在 [TiDB 配置文件](/tidb-configuration-file.md#allow-expression-index-new-in-v400) 中进行如下配置：

```sql
allow-expression-index = true
```

</CustomContent>

> **Note:**
>
> 表达式索引不能创建在主键上。
>
> 表达式索引中的表达式不能包含以下内容：
>
> - 易变函数，如 `RAND()` 和 `NOW()`。
> - [系统变量](/system-variables.md) 和 [用户变量](/user-defined-variables.md)。
> - 子查询。
> - [`AUTO_INCREMENT`](/auto-increment.md) 列。你可以通过将 [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated)（系统变量）设置为 `true` 来移除此限制。
> - [窗口函数](/functions-and-operators/window-functions.md)。
> - ROW 函数，如 `CREATE TABLE t (j JSON, INDEX k (((j,j))));`。
> - [聚合函数](/functions-and-operators/aggregate-group-by-functions.md)。
>
> 表达式索引会隐式占用一个名称（例如 `_V$_{index_name}_{index_offset}`）。如果你尝试创建与已有列同名的表达式索引，会报错。同样，如果你添加了与之同名的新列，也会报错。
>
> 请确保表达式索引中函数的参数数量正确。
>
> 当索引表达式包含字符串相关函数时，受返回类型和长度影响，可能导致表达式索引创建失败。此时，你可以使用 `CAST()` 函数显式指定返回类型和长度。例如，若要基于 `REPEAT(a, 3)` 表达式创建索引，需要将表达式修改为 `CAST(REPEAT(a, 3) AS CHAR(20))`。

当查询语句中的表达式与表达式索引中的表达式匹配时，优化器可以选择表达式索引进行查询。在某些情况下，优化器可能不会选择表达式索引，这取决于统计信息。此时，你可以通过优化器提示强制优化器选择表达式索引。

在以下示例中，假设你在表达式 `LOWER(col1)` 上创建了表达式索引 `idx`：

如果查询语句的结果是相同的表达式，则会使用表达式索引。例如：

```sql
SELECT LOWER(col1) FROM t;
```

如果过滤条件中包含相同的表达式，也会使用表达式索引。例如：

```sql
SELECT * FROM t WHERE LOWER(col1) = "a";
SELECT * FROM t WHERE LOWER(col1) > "a";
SELECT * FROM t WHERE LOWER(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE LOWER(col1) IN ("a", "b");
SELECT * FROM t WHERE LOWER(col1) > "a" AND LOWER(col1) < "b";
SELECT * FROM t WHERE LOWER(col1) > "b" OR LOWER(col1) < "a";
```

当查询按相同表达式排序时，也会使用表达式索引。例如：

```sql
SELECT * FROM t ORDER BY LOWER(col1);
```

如果聚合（`GROUP BY`）函数中包含相同的表达式，也会使用表达式索引。例如：

```sql
SELECT MAX(LOWER(col1)) FROM t;
SELECT MIN(col1) FROM t GROUP BY LOWER(col1);
```

要查看表达式索引对应的表达式，可以执行 [`SHOW INDEX`](/sql-statements/sql-statement-show-indexes.md)，或查看系统表 [`information_schema.tidb_indexes`](/information-schema/information-schema-tidb-indexes.md) 以及表 [`information_schema.STATISTICS`](/information-schema/information-schema-statistics.md)。输出结果中的 `Expression` 列表示对应的表达式。对于非表达式索引，该列显示为 `NULL`。

维护表达式索引的成本高于维护其他索引，因为每次插入或更新行时都需要计算表达式的值。表达式的值已存储在索引中，因此当优化器选择表达式索引时，无需再次计算该值。

因此，当查询性能优先于插入和更新性能时，可以考虑对表达式建立索引。

表达式索引的语法和限制与 MySQL 保持一致。其实现方式是基于不可见的虚拟生成列创建索引，因此支持的表达式也继承了 [虚拟生成列的所有限制](/generated-columns.md#limitations)。

## 多值索引

多值索引是一种定义在数组列上的二级索引。在普通索引中，一个索引记录对应一条数据记录（1:1）。而在多值索引中，多条索引记录对应一条数据记录（N:1）。多值索引用于为 JSON 数组建立索引。例如，在 `zipcode` 字段上定义多值索引时，`zipcode` 数组中的每个元素都会生成一条索引记录。

```json
{
    "user":"Bob",
    "user_id":31,
    "zipcode":[94477,94536]
}
```

### 创建多值索引

你可以在索引定义中使用 [`CAST(... AS ... ARRAY)`](/functions-and-operators/cast-functions-and-operators.md#cast) 函数来创建多值索引，方式与创建表达式索引类似。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips((CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

你可以将多值索引定义为唯一索引。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    UNIQUE INDEX zips( (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

当多值索引被定义为唯一索引时，如果你尝试插入重复数据，则会报错。

```sql
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1,2]}');
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [2,3]}');
ERROR 1062 (23000): Duplicate entry '2' for key 'customers.zips'
```

同一条记录可以有重复值，但当不同记录有重复值时，会报错。

```sql
-- 插入成功
mysql> INSERT INTO t1 VALUES('[1,1,2]');
mysql> INSERT INTO t1 VALUES('[3,3,3,4,4,4]');

-- 插入失败
mysql> INSERT INTO t1 VALUES('[1,2]');
mysql> INSERT INTO t1 VALUES('[2,3]');
```

你还可以将多值索引定义为复合索引：

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

当多值索引被定义为复合索引时，多值部分可以出现在任意位置，但只能出现一次。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)), (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
ERROR 1235 (42000): This version of TiDB doesn't yet support 'more than one multi-valued key part per index'.
```

写入的数据必须与多值索引定义的类型完全一致，否则数据写入会失败：

```sql
-- zipcode 字段中的所有元素必须为 UNSIGNED 类型。
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [-1]}');
ERROR 3752 (HY000): Value is out of range for expression index 'zips' at row 1

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": ["1"]}'); -- 与 MySQL 不兼容
ERROR 3903 (HY000): Invalid JSON value for CAST for expression index 'zips'

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1]}');
Query OK, 1 row affected (0.00 sec)
```

### 使用多值索引

更多详情请参见 [索引选择 - 使用多值索引](/choose-index.md#use-multi-valued-indexes)。

### 限制

- 对于空的 JSON 数组，不会生成对应的索引记录。
- `CAST(... AS ... ARRAY)` 中的目标类型不能为 `BINARY`、`JSON`、`YEAR`、`FLOAT` 和 `DECIMAL`，源类型必须为 JSON。
- 多值索引不能用于排序。
- 只能在 JSON 数组上创建多值索引。
- 多值索引不能作为主键或外键。
- 多值索引额外占用的存储空间 = 每行数组元素的平均个数 × 普通二级索引占用的空间。
- 与普通索引相比，DML 操作会修改更多的多值索引记录，因此多值索引对性能的影响大于普通索引。
- 由于多值索引属于特殊类型的表达式索引，因此多值索引具有与表达式索引相同的限制。
- 如果表使用了多值索引，则无法通过 BR、TiCDC 或 TiDB Lightning 将该表备份、同步或导入到 v6.6.0 之前的 TiDB 集群。
- 对于包含复杂条件的查询，TiDB 可能无法选择多值索引。关于多值索引支持的条件模式，请参见 [使用多值索引](/choose-index.md#use-multi-valued-indexes)。

## 不可见索引

默认情况下，不可见索引是查询优化器会忽略的索引：

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

自 TiDB v8.0.0 起，你可以通过修改系统变量 [`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800) 让优化器选择不可见索引。

详情参见 [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)。

## 相关系统变量

与 `CREATE INDEX` 语句相关的系统变量有 `tidb_ddl_enable_fast_reorg`、`tidb_ddl_reorg_worker_cnt`、`tidb_ddl_reorg_batch_size`、`tidb_enable_auto_increment_in_generated` 和 `tidb_ddl_reorg_priority`。详情请参见 [系统变量](/system-variables.md#tidb_ddl_reorg_worker_cnt)。

## MySQL 兼容性

* TiDB 自托管版和 TiDB Cloud Dedicated 支持解析 `FULLTEXT` 语法，但不支持使用 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引。

    >**Note:**
    >
    > 目前，只有部分 AWS 区域的 {{{ .starter }} 和 {{{ .essential }}} 集群支持 [`FULLTEXT` 语法和索引](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)。

* TiDB 为兼容 MySQL，语法上接受 `HASH`、`BTREE` 和 `RTREE` 等索引类型，但会忽略它们。
* 不支持降序索引（与 MySQL 5.7 类似）。
* 不支持为表添加 `CLUSTERED` 类型的主键。关于 `CLUSTERED` 类型主键的更多信息，参见 [聚簇索引](/clustered-indexes.md)。
* 表达式索引与视图不兼容。通过视图执行查询时，无法同时使用表达式索引。
* 表达式索引与绑定存在兼容性问题。当表达式索引的表达式中包含常量时，为对应查询创建的绑定会扩展其适用范围。例如，假设表达式索引的表达式为 `a+1`，对应的查询条件为 `a+1 > 2`，此时创建的绑定为 `a+? > ?`，这意味着条件如 `a+2 > 2` 的查询也会被强制使用表达式索引，可能导致执行计划不佳。此外，这也会影响 SQL Plan Management (SPM) 中的基线捕获和基线演进。
* 使用多值索引写入的数据必须与定义的数据类型完全一致，否则数据写入会失败。详情参见 [创建多值索引](/sql-statements/sql-statement-create-index.md#create-multi-valued-indexes)。
* 将 `UNIQUE KEY` 作为 [全局索引](/partitioned-table.md#global-indexes) 并使用 `GLOBAL` 索引选项是 TiDB 针对 [分区表](/partitioned-table.md) 的扩展，不兼容 MySQL。

## 另请参阅

* [索引选择](/choose-index.md)
* [错误索引解决方案](/wrong-index-solution.md)
* [ADD INDEX](/sql-statements/sql-statement-add-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
