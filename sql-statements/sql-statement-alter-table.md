---
title: ALTER TABLE | TiDB SQL Statement Reference
summary: 关于在 TiDB 数据库中使用 ALTER TABLE 的概述。
---

# ALTER TABLE

此语句用于修改现有表以符合新的表结构。`ALTER TABLE` 可以用来：

- [`ADD`](/sql-statements/sql-statement-add-index.md)、[`DROP`](/sql-statements/sql-statement-drop-index.md) 或 [`RENAME`](/sql-statements/sql-statement-rename-index.md) 索引
- [`ADD`](/sql-statements/sql-statement-add-column.md)、[`DROP`](/sql-statements/sql-statement-drop-column.md)、[`MODIFY`](/sql-statements/sql-statement-modify-column.md) 或 [`CHANGE`](/sql-statements/sql-statement-change-column.md) 列
- [`COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) 表数据

## 概述

```ebnf+diagram
AlterTableStmt ::=
    'ALTER' IgnoreOptional 'TABLE' TableName (
        AlterTableSpecListOpt AlterTablePartitionOpt |
        'ANALYZE' 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList )? AnalyzeOptionListOpt |
        'COMPACT' ( 'PARTITION' PartitionNameList )? 'TIFLASH' 'REPLICA'
    )

TableName ::=
    Identifier ('.' Identifier)?

AlterTableSpec ::=
    TableOptionList
|   'SET' 'TIFLASH' 'REPLICA' LengthNum LocationLabelList
|   'CONVERT' 'TO' CharsetKw ( CharsetName | 'DEFAULT' ) OptCollate
|   'ADD' ( ColumnKeywordOpt IfNotExists ( ColumnDef ColumnPosition | '(' TableElementList ')' ) | Constraint | 'PARTITION' IfNotExists NoWriteToBinLogAliasOpt ( PartitionDefinitionListOpt | 'PARTITIONS' NUM ) )
|   ( ( 'CHECK' | 'TRUNCATE' ) 'PARTITION' | ( 'OPTIMIZE' | 'REPAIR' | 'REBUILD' ) 'PARTITION' NoWriteToBinLogAliasOpt ) AllOrPartitionNameList
|   'COALESCE' 'PARTITION' NoWriteToBinLogAliasOpt NUM
|   'DROP' ( ColumnKeywordOpt IfExists ColumnName RestrictOrCascadeOpt | 'PRIMARY' 'KEY' |  'PARTITION' IfExists PartitionNameList | ( KeyOrIndex IfExists | 'CHECK' ) Identifier | 'FOREIGN' 'KEY' Symbol )
|   'EXCHANGE' 'PARTITION' Identifier 'WITH' 'TABLE' TableName WithValidationOpt
|   ( 'IMPORT' | 'DISCARD' ) ( 'PARTITION' AllOrPartitionNameList )? 'TABLESPACE'
|   'REORGANIZE' 'PARTITION' NoWriteToBinLogAliasOpt ReorganizePartitionRuleOpt
|   'ORDER' 'BY' AlterOrderItem ( ',' AlterOrderItem )*
|   ( 'DISABLE' | 'ENABLE' ) 'KEYS'
|   ( 'MODIFY' ColumnKeywordOpt IfExists | 'CHANGE' ColumnKeywordOpt IfExists ColumnName ) ColumnDef ColumnPosition
|   'ALTER' ( ColumnKeywordOpt ColumnName ( 'SET' 'DEFAULT' ( SignedLiteral | '(' Expression ')' ) | 'DROP' 'DEFAULT' ) | 'CHECK' Identifier EnforcedOrNot | 'INDEX' Identifier ("VISIBLE" | "INVISIBLE") )
|   'RENAME' ( ( 'COLUMN' | KeyOrIndex ) Identifier 'TO' Identifier | ( 'TO' | '='? | 'AS' ) TableName )
|   LockClause
|   AlgorithmClause
|   'FORCE'
|   ( 'WITH' | 'WITHOUT' ) 'VALIDATION'
|   'SECONDARY_LOAD'
|   'SECONDARY_UNLOAD'
|   ( 'AUTO_INCREMENT' | 'AUTO_ID_CACHE' | 'AUTO_RANDOM_BASE' | 'SHARD_ROW_ID_BITS' ) EqOpt LengthNum
|   ( 'CACHE' | 'NOCACHE' )
|   (
        'TTL' EqOpt TimeColumnName '+' 'INTERVAL' Expression TimeUnit (TTLEnable EqOpt ( 'ON' | 'OFF' ))?
        | 'REMOVE' 'TTL'
        | TTLEnable EqOpt ( 'ON' | 'OFF' )
        | TTLJobInterval EqOpt stringLit
    )
|   PlacementPolicyOption

PlacementPolicyOption ::=
    "PLACEMENT" "POLICY" EqOpt PolicyName
|   "PLACEMENT" "POLICY" (EqOpt | "SET") "DEFAULT"
```

## 示例

创建一个带有初始数据的表：


```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```sql
Query OK, 0 rows affected (0.11 sec)

Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

以下查询需要进行全表扫描，因为列 c1 没有建立索引：


```sql
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```sql
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

可以使用 [`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-add-index.md) 来为 t1 表添加索引。`EXPLAIN` 确认，原始查询现在使用索引范围扫描，效率更高：


```sql
ALTER TABLE t1 ADD INDEX (c1);
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```sql
Query OK, 0 rows affected (0.30 sec)

+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

TiDB 支持断言 DDL 更改使用特定的 `ALTER` 算法。注意，这只是一个断言，并不会改变实际用于修改表的算法：


```sql
ALTER TABLE t1 DROP INDEX c1, ALGORITHM=INSTANT;
```

```sql
Query OK, 0 rows affected (0.24 sec)
```

在需要 `INPLACE` 算法的操作上使用 `ALGORITHM=INSTANT` 断言会导致语句错误：


```sql
ALTER TABLE t1 ADD INDEX (c1), ALGORITHM=INSTANT;
```

```sql
ERROR 1846 (0A000): ALGORITHM=INSTANT is not supported. Reason: Cannot alter table by INSTANT. Try ALGORITHM=INPLACE.
```

然而，在 `INPLACE` 操作中使用 `ALGORITHM=COPY` 断言会产生警告而非错误。这是因为 TiDB 将断言理解为 _this algorithm or better_。这种行为差异对于 MySQL 兼容性很有用，因为 TiDB 使用的算法可能与 MySQL 不同：


```sql
ALTER TABLE t1 ADD INDEX (c1), ALGORITHM=COPY;
SHOW WARNINGS;
```

```sql
Query OK, 0 rows affected, 1 warning (0.25 sec)

+-------+------+---------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                     |
+-------+------+---------------------------------------------------------------------------------------------+
| Error | 1846 | ALGORITHM=COPY is not supported. Reason: Cannot alter table by COPY. Try ALGORITHM=INPLACE. |
+-------+------+---------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

在 TiDB 中，`ALTER TABLE` 主要限制如下：

- 当在单个 `ALTER TABLE` 语句中修改多个 schema 对象时：

    - 不支持对同一对象进行多次修改。
    - TiDB 在执行前会验证表的 schema **在执行之前**。例如，执行 `ALTER TABLE t ADD COLUMN c1 INT, ADD COLUMN c2 INT AFTER c1;` 时会报错，因为表中不存在列 `c1`。
    - 对于 `ALTER TABLE` 语句，TiDB 的执行顺序是从左到右逐个执行每个变更，这在某些情况下与 MySQL 不兼容。

- 不支持对主键列进行 [Reorg-Data](/sql-statements/sql-statement-modify-column.md#reorg-data-change) 类型的变更。

- 不支持对分区表的列类型变更。

- 不支持对生成列的列类型变更。

- 由于 TiDB 和 MySQL 在 `CAST` 函数行为上的兼容性问题，不支持某些数据类型（例如部分 TIME、Bit、Set、Enum 和 JSON 类型）的变更。

- 不支持空间数据类型。

- `ALTER TABLE t CACHE | NOCACHE` 是 TiDB 对 MySQL 语法的扩展。详情请参见 [Cached Tables](/cached-tables.md)。

关于更多限制，请参见 [MySQL Compatibility](/mysql-compatibility.md#ddl-operations)。

## 相关链接

- [MySQL Compatibility](/mysql-compatibility.md#ddl-operations)
- [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
- [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
- [ADD INDEX](/sql-statements/sql-statement-add-index.md)
- [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
- [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
- [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
- [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
- [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
- [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)