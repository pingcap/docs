---
title: ANALYZE | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 ANALYZE 的概述。
---

# ANALYZE

此语句用于更新 TiDB 在表和索引上构建的统计信息。建议在执行大量批量更新或导入记录后，或者当你发现查询执行计划不理想时，运行 `ANALYZE`。

TiDB 也会随着时间的推移自动更新其统计信息，当它发现统计信息与自身的估算不一致时。

目前，TiDB 通过使用 `ANALYZE TABLE` 语句以完整采集的方式收集统计信息。更多信息请参见 [统计信息简介](/statistics.md)。

## 语法概要

```ebnf+diagram
AnalyzeTableStmt ::=
    'ANALYZE' ( 'TABLE' ( TableNameList ( 'ALL COLUMNS' | 'PREDICATE COLUMNS' ) | TableName ( 'INDEX' IndexNameList? | AnalyzeColumnOption | 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList? | AnalyzeColumnOption )? )? ) ) AnalyzeOptionListOpt

AnalyzeOptionListOpt ::=
( WITH AnalyzeOptionList )?

AnalyzeOptionList ::=
AnalyzeOption ( ',' AnalyzeOption )*

AnalyzeOption ::=
( NUM ( 'BUCKETS' | 'TOPN' | ( 'CMSKETCH' ( 'DEPTH' | 'WIDTH' ) ) | 'SAMPLES' ) ) | ( FLOATNUM 'SAMPLERATE' )

AnalyzeColumnOption ::=
( 'ALL COLUMNS' | 'PREDICATE COLUMNS' | 'COLUMNS' ColumnNameList )

TableNameList ::=
    TableName (',' TableName)*

TableName ::=
    Identifier ( '.' Identifier )?

ColumnNameList ::=
    Identifier ( ',' Identifier )*

IndexNameList ::=
    Identifier ( ',' Identifier )*

PartitionNameList ::=
    Identifier ( ',' Identifier )*
```

## 示例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)
```

```sql
mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

```sql
mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)
```

```sql
mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

当前统计信息的状态为 `pseudo`，意味着统计信息不准确。

```sql
mysql> ANALYZE TABLE t1;
Query OK, 0 rows affected (0.13 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+-------------------------------+
| id                     | estRows | task      | access object          | operator info                 |
+------------------------+---------+-----------+------------------------+-------------------------------+
| IndexReader_6          | 1.00    | root      |                        | index:IndexRangeScan_5        |
| └─IndexRangeScan_5     | 1.00    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false |
+------------------------+---------+-----------+------------------------+-------------------------------+
2 rows in set (0.00 sec)
```

统计信息现已正确更新并加载。

## MySQL 兼容性

TiDB 在 **统计信息的收集** 和 **查询执行时统计信息的使用** 方面与 MySQL 存在差异。虽然此语句在语法上与 MySQL 类似，但存在以下不同点：

+ 在运行 `ANALYZE TABLE` 时，TiDB 可能不会包含最近提交的变更。在批量更新行后，你可能需要 `sleep(1)`，然后再执行 `ANALYZE TABLE`，以使统计信息反映这些变更。详见 [#16570](https://github.com/pingcap/tidb/issues/16570)。
+ 在 TiDB 中，`ANALYZE TABLE` 的执行时间明显长于 MySQL。

## 相关链接

* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md)