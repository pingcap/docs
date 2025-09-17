---
title: ADD INDEX | TiDB SQL 语句参考
summary: TiDB 数据库中 ADD INDEX 的用法概述。
---

# ADD INDEX

`ALTER TABLE.. ADD INDEX` 语句用于为已有表添加索引。该操作在 TiDB 中是在线进行的，这意味着在添加索引的过程中，表的读写操作都不会被阻塞。

> **Tip:**
>
> 可以使用 [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md) 来加速该语句的执行。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 对于 [TiDB Cloud Dedicated 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)（4 vCPU），建议手动关闭 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)，以防止在创建索引时资源受限影响集群稳定性。关闭该设置后，索引将通过事务方式创建，从而降低对集群的整体影响。

</CustomContent>

<CustomContent platform="tidb">

> **Warning:**
>
> - 在集群中执行 DDL 语句时（通常是耗时较长的 DDL 语句，如 `ADD INDEX` 和列类型变更），**DO NOT** 升级 TiDB 集群。
> - 升级前，建议使用 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) 命令检查 TiDB 集群中是否有正在进行的 DDL 任务。如果存在 DDL 任务，升级集群前应等待 DDL 执行完成，或使用 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 任务后再进行升级。
> - 此外，在集群升级过程中，**DO NOT** 执行任何 DDL 语句。否则，可能会出现未定义的行为。
>
> 当你将 TiDB 从 v7.1.0 升级到更高版本时，可以忽略上述限制。详情参见 [TiDB 平滑升级的限制](/smooth-upgrade-tidb.md)。

</CustomContent>

## 语法

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddIndexSpec ( ',' AddIndexSpec )*

AddIndexSpec
         ::= 'ADD' ( ( 'PRIMARY' 'KEY' | ( 'KEY' | 'INDEX' ) 'IF NOT EXISTS'? | 'UNIQUE' ( 'KEY' | 'INDEX' )? ) ( ( Identifier? 'USING' | Identifier 'TYPE' ) IndexType )? | 'FULLTEXT' ( 'KEY' | 'INDEX' )? IndexName ) '(' IndexPartSpecification ( ',' IndexPartSpecification )* ')' IndexOption*

IndexPartSpecification
         ::= ( ColumnName ( '(' LengthNum ')' )? | '(' Expression ')' ) ( 'ASC' | 'DESC' )

IndexOption
         ::= 'KEY_BLOCK_SIZE' '='? LengthNum
           | 'USING' IndexType
           | 'WITH' 'PARSER' Identifier
           | 'COMMENT' stringLit
           | 'VISIBLE'
           | 'INVISIBLE'
           | 'GLOBAL'
           | 'LOCAL'

IndexType
         ::= 'BTREE'
           | 'HASH'
           | 'RTREE'
```

## 示例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
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

mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 0.01    | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 0.01    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

* TiDB 在语法上兼容 MySQL，支持 `HASH`、`BTREE` 和 `RTREE` 等索引类型，但会忽略这些类型。
* 不支持 `SPATIAL` 索引。
* TiDB 支持解析 `FULLTEXT` 语法，但不支持使用 `FULLTEXT` 索引。
* 不支持降序索引（与 MySQL 5.7 类似）。
* 不支持为表添加 `CLUSTERED` 类型的主键。关于 `CLUSTERED` 类型主键的更多信息，参见 [聚簇索引](/clustered-indexes.md)。
* 通过 `GLOBAL` 索引选项将 `PRIMARY KEY` 或 `UNIQUE INDEX` 设置为 [全局索引](/partitioned-table.md#global-indexes) 是 TiDB 针对 [分区表](/partitioned-table.md) 的扩展功能，不兼容 MySQL。

## 另请参阅

* [索引选择](/choose-index.md)
* [错误索引解决方案](/wrong-index-solution.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md)
