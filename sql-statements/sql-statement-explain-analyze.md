---
title: EXPLAIN ANALYZE | TiDB SQL Statement Reference
summary: An overview of the usage of EXPLAIN ANALYZE for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-explain-analyze/','/docs/dev/reference/sql/statements/explain-analyze/']
---

# EXPLAIN ANALYZE

The `EXPLAIN ANALYZE` statement works similar to `EXPLAIN`, with the major difference being that it will actually execute the statement. This allows you to compare the estimates used as part of query planning to actual values encountered during execution.  If the estimates differ significantly from the actual values, you should consider running `ANALYZE TABLE` on the affected tables.

## Synopsis

**ExplainSym:**

![ExplainSym](/media/sqlgram/ExplainSym.png)

**ExplainStmt:**

![ExplainStmt](/media/sqlgram/ExplainStmt.png)

**ExplainableStmt:**

![ExplainableStmt](/media/sqlgram/ExplainableStmt.png)

## Examples

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```
mysql> EXPLAIN ANALYZE SELECT * FROM t1 WHERE id = 1;
```

```
+-------------+-------+------+--------------------+---------------------------+
| id          | count | task | operator info      | execution info            |
+-------------+-------+------+--------------------+---------------------------+
| Point_Get_1 | 1.00  | root | table:t1, handle:1 | time:0ns, loops:0, rows:0 |
+-------------+-------+------+--------------------+---------------------------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```
mysql> EXPLAIN ANALYZE SELECT * FROM t1;
```

```
+-----------------------+----------+-----------+------------------------------------------+-------------------------------------------------------------------------------+-----------+------+
| id                    | count    | task      | operator info                            | execution info                                                                | memory    | disk |
+-----------------------+----------+-----------+------------------------------------------+-------------------------------------------------------------------------------+-----------+------+
| TableReader_5         | 10000.00 | root      | data:TableFullScan_4                     | time:148.128µs, loops:2, rows:3, rpc num: 1, rpc time:97.812µs, proc keys:0   | 199 Bytes | N/A  |
| └─TableFullScan_4     | 10000.00 | cop[tikv] | table:t1, keep order:false, stats:pseudo | time:40.918µs, loops:4, rows:3                                                | N/A       | N/A  |
+-----------------------+----------+-----------+------------------------------------------+-------------------------------------------------------------------------------+-----------+------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Understanding the Query Execution Plan](/query-execution-plan.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)
