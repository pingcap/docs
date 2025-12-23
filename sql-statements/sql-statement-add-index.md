---
title: ADD INDEX | TiDB SQL 语句参考
summary: TiDB 数据库中 ADD INDEX 的用法概述。
---

# ADD INDEX

`ALTER TABLE.. ADD INDEX` 语句用于为已有表添加索引。此操作在 TiDB 中是在线的，这意味着在添加索引期间，表的读写都不会被阻塞。

> **提示：**
>
> 可以使用 [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md) 来加速该语句的操作。

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 对于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 4 vCPU 的集群，建议手动关闭 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) 变量，以防止资源限制在创建索引时影响集群稳定性。关闭该设置后，索引将通过事务方式创建，从而降低对集群的整体影响。

</CustomContent>

<CustomContent platform="tidb">

> **警告：**
>
> - **切勿**在集群中有 DDL 语句正在执行时升级 TiDB 集群（通常是耗时较长的 DDL 语句，如 `ADD INDEX` 和列类型变更）。
> - 升级前，建议使用 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md) 命令检查 TiDB 集群是否有正在进行的 DDL 任务。如果集群有 DDL 任务，需等待 DDL 执行完成，或使用 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 任务后再升级集群。
> - 此外，在集群升级期间，**切勿**执行任何 DDL 语句。否则，可能会出现未定义行为的问题。
>
> 当你将 TiDB 从 v7.1.0 升级到以上版本时，可以忽略上述限制。详情参见 [TiDB 平滑升级的限制](/smooth-upgrade-tidb.md)。

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

* TiDB 在语法上接受 `HASH`、`BTREE` 和 `RTREE` 等索引类型以兼容 MySQL，但会忽略这些类型。
* 不支持 `SPATIAL` 索引。
* TiDB 自建版和 TiDB Cloud Dedicated 支持解析 `FULLTEXT` 语法，但不支持使用 `FULLTEXT` 索引。

    >**注意：**
    >
    > 目前，仅部分 AWS 区域的 TiDB Cloud Starter 和 TiDB Cloud Essential 集群支持 [`FULLTEXT` 语法和索引](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)。

* 不支持降序索引（与 MySQL 5.7 类似）。
* 不支持为表添加 `CLUSTERED` 类型的主键。关于 `CLUSTERED` 类型主键的更多信息，参见 [聚簇索引](/clustered-indexes.md)。
* 将 `PRIMARY KEY` 或 `UNIQUE INDEX` 通过 `GLOBAL` 索引选项设置为 [全局索引](/global-indexes.md) 是 TiDB 针对 [分区表](/partitioned-table.md) 的扩展，且与 MySQL 不兼容。

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
* [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md)
