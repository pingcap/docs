---
title: CREATE [GLOBAL|SESSION] BINDING
summary: Use of CREATE BINDING in TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-create-binding/']
---

# CREATE [GLOBAL|SESSION] BINDING

This statement creates a new execution plan binding in TiDB. Binding can be used to inject a hint into a statement without requiring changes to the underlying query.

A `BINDING` can be on either a `GLOBAL` or `SESSION` basis. The default is `SESSION`.

The bound SQL statement is parameterized and stored in the system table. When a SQL query is processed, as long as the parameterized SQL statement and a bound one in the system table are consistent and the system variable `tidb_use_plan_baselines` is set to `ON` (default), the corresponding optimizer hint is available. If multiple execution plans are available, the optimizer chooses to bind the plan with the least cost.

## Synopsis

**CreateBindingStmt:**

![CreateBindingStmt](/media/sqlgram/CreateBindingStmt.png)

**GlobalScope:**

![GlobalScope](/media/sqlgram/GlobalScope.png)

**SelectStmt**

![SelectStmt](/media/sqlgram/SelectStmt.png)

****

## Examples

Start with some example data:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 b INT NOT NULL,
 pad VARBINARY(255),
 INDEX(b)
);
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
SELECT SLEEP(1);
ANALYZE TABLE t1;
```

The following statement has the current query execution plan:

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE SELECT * FROM t1 WHERE b = 123;
```

```sql
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
| id                            | estRows | actRows | task      | access object        | execution info                                                            | operator info                     | memory         | disk |
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
| IndexLookUp_10                | 583.00  | 297     | root      |                      | time:10.545072ms, loops:2, rpc num: 1, rpc time:398.359µs, proc keys:297  |                                   | 109.1484375 KB | N/A  |
| ├─IndexRangeScan_8(Build)     | 583.00  | 297     | cop[tikv] | table:t1, index:b(b) | time:0s, loops:4                                                          | range:[123,123], keep order:false | N/A            | N/A  |
| └─TableRowIDScan_9(Probe)     | 583.00  | 297     | cop[tikv] | table:t1             | time:12ms, loops:4                                                        | keep order:false                  | N/A            | N/A  |
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
3 rows in set (0.02 sec)
```

A different plan can be forced by adding a plan binding. In this case, the binding will ignore the index `(b)`:

{{< copyable "sql" >}}

```sql
CREATE SESSION BINDING FOR
 SELECT * FROM t1 WHERE b = 123
USING
 SELECT * FROM t1 IGNORE INDEX (b) WHERE b = 123;
EXPLAIN ANALYZE  SELECT * FROM t1 WHERE b = 123;
```

```sql
Query OK, 0 rows affected (0.00 sec)

+-------------------------+-----------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+--------------------+-----------------+------+
| id                      | estRows   | actRows | task      | access object | execution info                                                                                                                                      | operator info      | memory          | disk |
+-------------------------+-----------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+--------------------+-----------------+------+
| TableReader_7           | 595.00    | 297     | root      |               | time:187.843107ms, loops:2, cop_task: {num: 1, max:187.675378ms, proc_keys: 301010, rpc_num: 1, rpc_time: 187.655538ms, copr_cache_hit_ratio: 0.00} | data:Selection_6   | 88.232421875 KB | N/A  |
| └─Selection_6           | 595.00    | 297     | cop[tikv] |               | time:184ms, loops:298                                                                                                                               | eq(test.t1.b, 123) | N/A             | N/A  |
|   └─TableFullScan_5     | 301010.00 | 301010  | cop[tikv] | table:t1      | time:176ms, loops:298                                                                                                                               | keep order:false   | N/A             | N/A  |
+-------------------------+-----------+---------+-----------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+--------------------+-----------------+------+
3 rows in set (0.18 sec)
```

The binding can then be checked and removed with:

{{< copyable "sql" >}}

```sql
SHOW SESSION BINDINGS\G
DROP SESSION BINDING FOR SELECT * FROM t1 WHERE b = 123;
EXPLAIN ANALYZE  SELECT * FROM t1 WHERE b = 123;
```

```sql
*************************** 1. row ***************************
Original_sql: select * from t1 where b = ?
    Bind_sql: SELECT * FROM t1 IGNORE INDEX (b) WHERE b = 123
  Default_db: test
      Status: using
 Create_time: 2020-05-22 14:38:03.456
 Update_time: 2020-05-22 14:38:03.456
     Charset: utf8mb4
   Collation: utf8mb4_0900_ai_ci
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------+-----------------------------------+----------------+------+
| id                            | estRows | actRows | task      | access object        | execution info                                                          | operator info                     | memory         | disk |
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------+-----------------------------------+----------------+------+
| IndexLookUp_10                | 583.00  | 297     | root      |                      | time:5.31206ms, loops:2, rpc num: 1, rpc time:665.927µs, proc keys:297  |                                   | 109.1484375 KB | N/A  |
| ├─IndexRangeScan_8(Build)     | 583.00  | 297     | cop[tikv] | table:t1, index:b(b) | time:0s, loops:4                                                        | range:[123,123], keep order:false | N/A            | N/A  |
| └─TableRowIDScan_9(Probe)     | 583.00  | 297     | cop[tikv] | table:t1             | time:0s, loops:4                                                        | keep order:false                  | N/A            | N/A  |
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------+-----------------------------------+----------------+------+
3 rows in set (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [DROP [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-drop-binding.md)
* [SHOW [GLOBAL|SESSION] BINDINGS](/sql-statements/sql-statement-show-bindings.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [Optimizer Hints](/optimizer-hints.md)
* [SQL Plan Management](/sql-plan-management.md)