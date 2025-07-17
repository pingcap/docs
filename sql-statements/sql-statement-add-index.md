---
title: ADD INDEX | TiDB SQL Statement Reference
summary: 关于在 TiDB 数据库中使用 ADD INDEX 的概述。
---

# ADD INDEX

`ALTER TABLE.. ADD INDEX` 语句在现有表中添加索引。这个操作在 TiDB 中是在线进行的，意味着添加索引时不会阻塞对表的读写操作。

> **Tip:**
>
> [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md) 可以用来加快此语句的执行速度。

<CustomContent platform="tidb">

> **Warning:**
>
> - **请勿** 在集群中执行 DDL 语句时升级 TiDB 集群（通常针对耗时较长的 DDL 语句，如 `ADD INDEX` 和列类型变更）。
> - 在升级前，建议使用 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) 命令检查 TiDB 集群是否存在正在进行的 DDL 任务。如果集群有 DDL 任务，为了升级集群，应等待 DDL 执行完成或使用 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 任务后再进行升级。
> - 此外，在集群升级期间，**请勿** 执行任何 DDL 语句，否则可能会出现未定义行为的问题。
>
> 当你将 TiDB 从 v7.1.0 升级到更高版本时，可以忽略上述限制。详情请参见 [TiDB 平滑升级的限制](/smooth-upgrade-tidb.md)。

</CustomContent>

## 概要

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

* TiDB 支持 `HASH`、`BTREE` 和 `RTREE` 等索引类型的语法以兼容 MySQL，但会忽略它们。
* 不支持 `SPATIAL` 索引。
* TiDB 支持解析 `FULLTEXT` 语法，但不支持使用 `FULLTEXT` 索引。
* 不支持降序索引（与 MySQL 5.7 类似）。
* 不支持向表中添加 `CLUSTERED` 类型的主键。关于 `CLUSTERED` 类型主键的更多细节，请参见 [clustered index](/clustered-indexes.md)。
* 设置 `PRIMARY KEY` 或 `UNIQUE INDEX` 为带有 `GLOBAL` 索引选项的 [全局索引](/partitioned-table.md#global-indexes) 是 TiDB 针对 [分区表](/partitioned-table.md) 的扩展，不兼容 MySQL。

## 相关链接

* [Index Selection](/choose-index.md)
* [Wrong Index Solution](/wrong-index-solution.md)
* [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
* [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
* [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
* [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md)
