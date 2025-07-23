---
title: FOREIGN KEY Constraints
summary: 关于 TiDB 数据库中 FOREIGN KEY 约束的使用概述。
---

# FOREIGN KEY Constraints

外键允许跨表引用相关数据，而外键约束确保相关数据的一致性。从 v6.6.0 版本开始，TiDB 支持外键和外键约束。从 v8.5.0 版本开始，此功能变为正式可用。

> **Warning:**
>
> 该外键功能通常用于强制执行 [referential integrity](https://en.wikipedia.org/wiki/Referential_integrity) 约束检查。它可能导致性能下降，因此建议在性能敏感场景中使用前进行充分测试。

外键在子表中定义。语法如下：

```ebnf+diagram
ForeignKeyDef
         ::= ( 'CONSTRAINT' Identifier )? 'FOREIGN' 'KEY'
             Identifier? '(' ColumnName ( ',' ColumnName )* ')'
             'REFERENCES' TableName '(' ColumnName ( ',' ColumnName )* ')'
             ( 'ON' 'DELETE' ReferenceOption )?
             ( 'ON' 'UPDATE' ReferenceOption )?

ReferenceOption
         ::= 'RESTRICT'
           | 'CASCADE'
           | 'SET' 'NULL'
           | 'SET' 'DEFAULT'
           | 'NO' 'ACTION'
```

## 命名

外键的命名遵循以下规则：

- 如果在 `CONSTRAINT identifier` 中指定了名称，则使用该名称。
- 如果在 `CONSTRAINT identifier` 中未指定名称，但在 `FOREIGN KEY identifier` 中指定了名称，则使用 `FOREIGN KEY` 中的名称。
- 如果 `CONSTRAINT identifier` 和 `FOREIGN KEY identifier` 都未指定名称，则会自动生成名称，例如 `fk_1`、`fk_2` 和 `fk_3`。
- 外键名称在当前表中必须唯一，否则在创建外键时会报错 `ERROR 1826: Duplicate foreign key constraint name 'fk'`。

## 限制条件

创建外键时，必须满足以下条件：

- 父表和子表都不能是临时表。
- 用户必须拥有父表的 `REFERENCES` 权限。
- 父表和子表中被引用的列必须具有相同的数据类型、相同的大小、精度、长度、字符集和排序规则。
- 外键列不能引用自身。
- 外键列与被引用父表中的列必须具有相同的索引，且索引中列的顺序必须与外键中的列顺序一致，以利用索引避免全表扫描进行外键约束检查。

    - 如果父表中没有对应的外键索引，会报错 `ERROR 1822: Failed to add the foreign key constraint. Missing index for constraint 'fk' in the referenced table 't'`。
    - 如果子表中没有对应的外键索引，则会自动创建一个与外键同名的索引。

- 不支持在 `BLOB` 或 `TEXT` 类型的列上创建外键。
- 不支持在分区表上创建外键。
- 不支持在虚拟生成列上创建外键。

## 引用操作

如果对父表中的外键值执行 `UPDATE` 或 `DELETE` 操作，则子表中对应的外键值由外键定义中的 `ON UPDATE` 或 `ON DELETE` 子句所定义的引用操作决定。引用操作包括：

- `CASCADE`：当影响父表时，自动更新或删除子表中匹配的行。级联操作采用深度优先方式执行。
- `SET NULL`：当影响父表时，自动将子表中匹配的外键列设置为 `NULL`。
- `RESTRICT`：如果子表中存在匹配行，则拒绝 `UPDATE` 或 `DELETE` 操作。
- `NO ACTION`：与 `RESTRICT` 相同。
- `SET DEFAULT`：与 `RESTRICT` 相同。

如果父表中没有匹配的外键值，则对子表的 `INSERT` 或 `UPDATE` 操作会被拒绝。

如果外键定义未指定 `ON DELETE` 或 `ON UPDATE`，则默认行为为 `NO ACTION`。

在定义在 `STORED GENERATED COLUMN` 上的外键中，不支持 `CASCADE`、`SET NULL` 和 `SET DEFAULT` 引用。

## 外键使用示例

以下示例使用单列外键关联父表和子表：

```sql
CREATE TABLE parent (
    id INT KEY
);

CREATE TABLE child (
    id INT,
    pid INT,
    INDEX idx_pid (pid),
    FOREIGN KEY (pid) REFERENCES parent(id) ON DELETE CASCADE
);
```

以下是一个较复杂的示例，`product_order` 表有两个外键，分别引用另外两个表。其中一个外键引用 `product` 表的两个索引，另一个引用 `customer` 表的单个索引：

```sql
CREATE TABLE product (
    category INT NOT NULL,
    id INT NOT NULL,
    price DECIMAL(20,10),
    PRIMARY KEY(category, id)
);

CREATE TABLE customer (
    id INT KEY
);

CREATE TABLE product_order (
    id INT NOT NULL AUTO_INCREMENT,
    product_category INT NOT NULL,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,

    PRIMARY KEY(id),
    INDEX (product_category, product_id),
    INDEX (customer_id),

    FOREIGN KEY (product_category, product_id)
      REFERENCES product(category, id)
      ON UPDATE CASCADE ON DELETE RESTRICT,

    FOREIGN KEY (customer_id)
      REFERENCES customer(id)
);
```

## 创建外键约束

可以使用以下 `ALTER TABLE` 语句创建外键约束：

```sql
ALTER TABLE table_name
    ADD [CONSTRAINT [identifier]] FOREIGN KEY
    [identifier] (col_name, ...)
    REFERENCES tbl_name (col_name,...)
    [ON DELETE reference_option]
    [ON UPDATE reference_option]
```

外键可以自引用，即引用同一张表。在使用 `ALTER TABLE` 添加外键约束前，需要先在父表的被引用列上创建索引。

## 删除外键约束

可以使用以下 `ALTER TABLE` 语句删除外键约束：

```sql
ALTER TABLE table_name DROP FOREIGN KEY fk_identifier;
```

如果在创建时为外键约束命名，则可以通过名称引用删除。否则，必须使用系统自动生成的约束名。可以通过 `SHOW CREATE TABLE` 查看外键名：

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

## 外键约束检查

TiDB 支持外键约束检查，由系统变量 [`foreign_key_checks`](/system-variables.md#foreign_key_checks) 控制。默认情况下，该变量设置为 `ON`，表示启用外键约束检查。该变量有两个作用域：`GLOBAL` 和 `SESSION`。保持启用状态可以确保外键引用关系的完整性。

禁用外键约束检查的效果如下：

- 当删除被外键引用的父表时，只有在禁用外键约束检查时，删除操作才会成功。
- 在导入数据时，创建表的顺序可能与外键依赖顺序不同，可能导致创建表失败。只有在禁用外键约束检查时，才能成功创建表。此外，禁用外键检查可以加快数据导入速度。
- 在导入子表数据时，如果先导入子表数据，会报错。只有在禁用外键约束检查时，子表数据才能成功导入。
- 如果执行的 `ALTER TABLE` 操作涉及更改外键，只有在禁用外键约束检查时，操作才会成功。

禁用外键约束检查后，外键约束检查和引用操作不会执行，除非出现以下情况：

- 如果执行 `ALTER TABLE` 可能导致外键定义错误，执行过程中仍会报错。
- 删除外键所需的索引时，应先删除外键，否则会报错。
- 创建外键时，如果不满足相关条件或限制，也会报错。

## 锁定

在对子表执行 `INSERT` 或 `UPDATE` 时，TiDB 会检查对应的外键值是否存在于父表中，并锁定父表中的行，以避免被其他操作删除或修改，违反外键约束。锁定行为等同于对父表中外键值所在行执行 `SELECT FOR UPDATE`。

由于 TiDB 目前不支持 `LOCK IN SHARE MODE`，如果子表接受大量并发写入且大部分引用的外键值相同，可能会出现严重的锁冲突。建议在大量写入子表数据时禁用 [`foreign_key_checks`](/system-variables.md#foreign_key_checks)。

## 外键的定义和元数据

要查看外键约束的定义，可以执行 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)：

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

你也可以通过以下系统表获取外键信息：

- [`INFORMATION_SCHEMA.KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)
- [`INFORMATION_SCHEMA.TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)
- [`INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`](/information-schema/information-schema-referential-constraints.md)

示例：

从 `INFORMATION_SCHEMA.KEY_COLUMN_USAGE` 系统表获取外键信息：

```sql
mysql> SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA IS NOT NULL;
+--------------+---------------+------------------+-----------------+
| TABLE_SCHEMA | TABLE_NAME    | COLUMN_NAME      | CONSTRAINT_NAME |
+--------------+---------------+------------------+-----------------+
| test         | child         | pid              | fk_1            |
| test         | product_order | product_category | fk_1            |
| test         | product_order | product_id       | fk_1            |
| test         | product_order | customer_id      | fk_2            |
+--------------+---------------+------------------+-----------------+
```

从 `INFORMATION_SCHEMA.TABLE_CONSTRAINTS` 系统表获取外键信息：

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE='FOREIGN KEY'\G
***************************[ 1. row ]***************************
CONSTRAINT_CATALOG | def
CONSTRAINT_SCHEMA  | test
CONSTRAINT_NAME    | fk_1
TABLE_SCHEMA       | test
TABLE_NAME         | child
CONSTRAINT_TYPE    | FOREIGN KEY
```

从 `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS` 系统表获取外键信息：

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS\G
***************************[ 1. row ]***************************
CONSTRAINT_CATALOG        | def
CONSTRAINT_SCHEMA         | test
CONSTRAINT_NAME           | fk_1
UNIQUE_CONSTRAINT_CATALOG | def
UNIQUE_CONSTRAINT_SCHEMA  | test
UNIQUE_CONSTRAINT_NAME    | PRIMARY
MATCH_OPTION              | NONE
UPDATE_RULE               | NO ACTION
DELETE_RULE               | CASCADE
TABLE_NAME                | child
REFERENCED_TABLE_NAME     | parent
```

## 查看带有外键的执行计划

可以使用 `EXPLAIN` 语句查看执行计划。`Foreign_Key_Check` 操作符会对执行的 DML 语句进行外键约束检查。

```sql
mysql> explain insert into child values (1,1);
+-----------------------+---------+------+---------------+-------------------------------+
| id                    | estRows | task | access object | operator info                 |
+-----------------------+---------+------+---------------+-------------------------------+
| Insert_1              | N/A     | root |               | N/A                           |
| └─Foreign_Key_Check_3 | 0.00    | root | table:parent  | foreign_key:fk_1, check_exist |
+-----------------------+---------+------+---------------+-------------------------------+
```

也可以使用 `EXPLAIN ANALYZE` 查看外键引用行为的执行情况。`Foreign_Key_Cascade` 操作符会对执行的 DML 语句进行外键引用。

```sql
mysql> explain analyze delete from parent where id = 1;
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
| id                               | estRows | actRows | task      | access object                   | execution info                                                                                                                                                                               | operator info                               | memory    | disk |
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
| Delete_2                         | N/A     | 0       | root      |                                 | time:117.3µs, loops:1                                                                                                                                                                        | N/A                                         | 380 Bytes | N/A  |
| ├─Point_Get_1                    | 1.00    | 1       | root      | table:parent                    | time:63.6µs, loops:2, Get:{num_rpc:1, total_time:29.9µs}                                                                                                                                     | handle:1                                    | N/A       | N/A  |
| └─Foreign_Key_Cascade_3          | 0.00    | 0       | root      | table:child, index:idx_pid      | total:1.28ms, foreign_keys:1                                                                                                                                                                 | foreign_key:fk_1, on_delete:CASCADE         | N/A       | N/A  |
|   └─Delete_7                     | N/A     | 0       | root      |                                 | time:904.8µs, loops:1                                                                                                                                                                        | N/A                                         | 1.11 KB   | N/A  |
|     └─IndexLookUp_11             | 10.00   | 1       | root      |                                 | time:869.5µs, loops:2, index_task: {total_time: 371.1µs, fetch_handle: 357.3µs, build: 1.25µs, wait: 12.5µs}, table_task: {total_time: 382.6µs, num: 1, concurrency: 5}                      |                                             | 9.13 KB   | N/A  |
|       ├─IndexRangeScan_9(Build)  | 10.00   | 1       | cop[tikv] | table:child, index:idx_pid(pid) | time:351.2µs, loops:3, cop_task: {num: 1, max: 282.3µs, proc_keys: 0, rpc_num: 1, rpc_time: 263µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}, tikv_task:{time:220.2µs, loops:0}   | range:[1,1], keep order:false, stats:pseudo | N/A       | N/A  |
|       └─TableRowIDScan_10(Probe) | 10.00   | 1       | cop[tikv] | table:child                     | time:223.9µs, loops:2, cop_task: {num: 1, max: 168.8µs, proc_keys: 0, rpc_num: 1, rpc_time: 154.5µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}, tikv_task:{time:145.6µs, loops:0} | keep order:false, stats:pseudo              | N/A       | N/A  |
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
```

## 兼容性

### TiDB 版本间的兼容性

在 v6.6.0 之前，TiDB 支持创建外键的语法，但创建的外键无效。若将 v6.6.0 之前创建的 TiDB 集群升级到 v6.6.0 或更高版本，升级前创建的外键仍然无效。只有在 v6.6.0 及以后版本创建的外键才有效。可以删除无效的外键并重新创建以使外键约束生效。可使用 `SHOW CREATE TABLE` 查看外键是否有效，无效的外键会带有 `/* FOREIGN KEY INVALID */` 注释。

```sql
mysql> SHOW CREATE TABLE child\G
***************************[ 1. row ]***************************
Table        | child
Create Table | CREATE TABLE `child` (
  `id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE /* FOREIGN KEY INVALID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

### TiDB 工具的兼容性

<CustomContent platform="tidb">

- [DM](/dm/dm-overview.md) 不支持外键。在将数据复制到 TiDB 时，DM 会禁用下游 TiDB 的 [`foreign_key_checks`](/system-variables.md#foreign_key_checks)。因此，外键引起的级联操作不会从上游复制到下游，可能导致数据不一致。
- [TiCDC](/ticdc/ticdc-overview.md) v6.6.0 兼容外键。早期版本的 TiCDC 在复制带有外键的表时可能会报错。建议在使用 v6.6.0 之前的 TiCDC 时，禁用下游 TiDB 的 `foreign_key_checks`。
- [BR](/br/backup-and-restore-overview.md) v6.6.0 兼容外键。早期版本的 BR 在还原带有外键的表到 v6.6.0 或更高版本的集群时可能会报错。建议在使用早于 v6.6.0 的 BR 时，先禁用下游 TiDB 的 `foreign_key_checks`。
- 使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 时，如果目标表使用了外键，建议在导入数据前禁用下游 TiDB 的 `foreign_key_checks`。对于早于 v6.6.0 的版本，禁用此系统变量不会生效，需授予下游数据库用户 `REFERENCES` 权限，或提前在下游数据库中手动创建目标表，以确保数据导入顺利。

</CustomContent>

- [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 也兼容外键。

<CustomContent platform="tidb">

- 当你使用 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 比较上游和下游数据库的数据时，如果两个数据库版本不同且下游 TiDB 存在 [无效外键](#compatibility-between-tidb-versions)，sync-diff-inspector 可能会报告表结构不一致的错误。这是因为 TiDB v6.6.0 为无效外键添加了 `/* FOREIGN KEY INVALID */` 注释。

</CustomContent>

### 与 MySQL 的兼容性

当你创建外键时未指定名称，TiDB 生成的名称与 MySQL 不同。例如，TiDB 生成的外键名为 `fk_1`、`fk_2` 和 `fk_3`，而 MySQL 生成的外键名为 `table_name_ibfk_1`、`table_name_ibfk_2` 和 `table_name_ibfk_3`。

MySQL 和 TiDB 都会解析但忽略“内联 `REFERENCES` 规范”。只有作为 `FOREIGN KEY` 定义一部分的 `REFERENCES` 规范才会被检查和强制执行。以下示例使用 `REFERENCES` 子句创建外键约束：

```sql
CREATE TABLE parent (
    id INT KEY
);

CREATE TABLE child (
    id INT,
    pid INT REFERENCES parent(id)
);

SHOW CREATE TABLE child;
```

输出显示 `child` 表不包含任何外键：

```sql
+-------+-------------------------------------------------------------+
| Table | Create Table                                                |
+-------+-------------------------------------------------------------+
| child | CREATE TABLE `child` (                                      |
|       |   `id` int DEFAULT NULL,                                |
|       |   `pid` int DEFAULT NULL                                |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+-------------------------------------------------------------+
```