---
title: ADMIN EVOLVE BINDINGS | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
---

# ADMIN EVOLVE BINDINGS

The statement `ADMIN EVOLVE BINDINGS` allows you to manually trigger TiDB to generate new plan bindings for scenarios where the previously saved bindings have been discovered to be suboptimal.

## Synopsis

**AdminStmt:**

![AdminStmt](/media/sqlgram/AdminStmt.png)

## Examples

Start with some example data:

{{< copyable "sql" >}}

```sql
DROP TABLE IF EXISTS t1;
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 b INT NOT NULL,
 c INT NOT NULL,
 pad VARBINARY(255),
 INDEX (b)
);
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
SELECT SLEEP(1);
ANALYZE TABLE t1;
```

Ensure that the following statement is captured in a plan binding. It is okay if other statements also have bindings:

{{< copyable "sql" >}}

```sql
SELECT c FROM t1 WHERE b = 1234;
SELECT c FROM t1 WHERE b = 199;
SELECT c FROM t1 WHERE b = 2048;
DROP GLOBAL BINDING FOR SELECT c FROM t1 WHERE b = 2048; -- drop incase this example is run twice
SHOW GLOBAL BINDINGS;
ADMIN CAPTURE BINDINGS;
SHOW GLOBAL BINDINGS;
```

```sql
+------------------------------+-------------------------------------------------------------------------------+------------+--------+-------------------------+-------------------------+---------+-----------+---------+
| Original_sql                 | Bind_sql                                                                      | Default_db | Status | Create_time             | Update_time             | Charset | Collation | Source  |
+------------------------------+-------------------------------------------------------------------------------+------------+--------+-------------------------+-------------------------+---------+-----------+---------+
| select * from t1 where b = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`)*/ * FROM `t1` WHERE `b`=1234   | test       | using  | 2020-09-29 20:43:30.508 | 2020-09-29 20:43:30.508 |         |           | capture |
+------------------------------+-------------------------------------------------------------------------------+------------+--------+-------------------------+-------------------------+---------+-----------+---------+
1 rows in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

+------------------------------+-------------------------------------------------------------------------------+------------+--------+-------------------------+-------------------------+---------+-----------+---------+
| Original_sql                 | Bind_sql                                                                      | Default_db | Status | Create_time             | Update_time             | Charset | Collation | Source  |
+------------------------------+-------------------------------------------------------------------------------+------------+--------+-------------------------+-------------------------+---------+-----------+---------+
| select c from t1 where b = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`)*/ `c` FROM `t1` WHERE `b`=1234 | test       | using  | 2020-09-29 20:43:30.508 | 2020-09-29 20:43:30.508 |         |           | capture |
| select * from t1 where b = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`)*/ * FROM `t1` WHERE `b`=1234   | test       | using  | 2020-09-29 20:43:30.508 | 2020-09-29 20:43:30.508 |         |           | capture |
+------------------------------+-------------------------------------------------------------------------------+------------+--------+-------------------------+-------------------------+---------+-----------+---------+
2 rows in set (0.00 sec)
```

The next step is to add an index on `(b,c)`. This index is actually a better index for the statement since it can apply a covering index optimization, but because there is a plan binding in place it should not be used. We can confirm this using `EXPLAIN`:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT c FROM t1 WHERE b = 1234;
ALTER TABLE t1 ADD INDEX (b,c);
SELECT SLEEP(1);
ANALYZE TABLE t1;
EXPLAIN SELECT c FROM t1 WHERE b = 1234;
```
```sql
+---------------------------------+---------+-----------+----------------------+-------------------------------------+
| id                              | estRows | task      | access object        | operator info                       |
+---------------------------------+---------+-----------+----------------------+-------------------------------------+
| Projection_4                    | 0.00    | root      |                      | test.t1.c                           |
| └─IndexLookUp_7                 | 0.00    | root      |                      |                                     |
|   ├─IndexRangeScan_5(Build)     | 0.00    | cop[tikv] | table:t1, index:b(b) | range:[1234,1234], keep order:false |
|   └─TableRowIDScan_6(Probe)     | 0.00    | cop[tikv] | table:t1             | keep order:false                    |
+---------------------------------+---------+-----------+----------------------+-------------------------------------+
4 rows in set (0.00 sec)

Query OK, 0 rows affected (14.02 sec)

+----------+
| SLEEP(1) |
+----------+
|        0 |
+----------+
1 row in set (1.00 sec)

Query OK, 0 rows affected (5.00 sec)

+---------------------------------+---------+-----------+----------------------+-------------------------------------+
| id                              | estRows | task      | access object        | operator info                       |
+---------------------------------+---------+-----------+----------------------+-------------------------------------+
| Projection_4                    | 0.00    | root      |                      | test.t1.c                           |
| └─IndexLookUp_7                 | 0.00    | root      |                      |                                     |
|   ├─IndexRangeScan_5(Build)     | 0.00    | cop[tikv] | table:t1, index:b(b) | range:[1234,1234], keep order:false |
|   └─TableRowIDScan_6(Probe)     | 0.00    | cop[tikv] | table:t1             | keep order:false                    |
+---------------------------------+---------+-----------+----------------------+-------------------------------------+
4 rows in set (0.00 sec)
```

By default, TiDB will continue to use the suboptimal index on `b` instead of `(b, c)`. When the option [`tidb_evolve_plan_baselines`](/system-variables.md#tidb_evolve_plan_baselines-new-in-v40) is enabled, TiDB will detect when a suboptimal plan is selected. After `bind-info-lease` has elapsed (default: 3s), the new plan will be either used or rejected:

```sql
SET tidb_evolve_plan_baselines = 1;
SELECT c FROM t1 WHERE b = 1234; # TiDB will discover this plan is suboptimal while executing this statement
SHOW GLOBAL BINDINGS;
SELECT SLEEP(5);
SHOW GLOBAL BINDINGS;
```

```sql
Query OK, 0 rows affected (0.00 sec)

..

+------------------------------+----------------------------------------------------------------------------------------+------------+----------------+-------------------------+-------------------------+---------+-----------------+---------+
| Original_sql                 | Bind_sql                                                                               | Default_db | Status         | Create_time             | Update_time             | Charset | Collation       | Source  |
+------------------------------+----------------------------------------------------------------------------------------+------------+----------------+-------------------------+-------------------------+---------+-----------------+---------+
| select c from t1 where b = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`)*/ `c` FROM `t1` WHERE `b`=1234          | test       | using          | 2020-09-29 21:30:33.978 | 2020-09-29 21:30:33.978 |         |                 | capture |
| select c from t1 where b = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b_2`)*/ `c` FROM `test`.`t1` WHERE `b`=1234 | test       | pending verify | 2020-09-29 21:32:20.978 | 2020-09-29 21:32:20.978 | utf8    | utf8_general_ci | evolve  |
+------------------------------+----------------------------------------------------------------------------------------+------------+----------------+-------------------------+-------------------------+---------+-----------------+---------+
2 rows in set (0.00 sec)

+------------------------------+----------------------------------------------------------------------------------------+------------+----------+-------------------------+-------------------------+---------+-----------------+---------+
| Original_sql                 | Bind_sql                                                                               | Default_db | Status   | Create_time             | Update_time             | Charset | Collation       | Source  |
+------------------------------+----------------------------------------------------------------------------------------+------------+----------+-------------------------+-------------------------+---------+-----------------+---------+
| select c from t1 where b = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`)*/ `c` FROM `t1` WHERE `b`=1234          | test       | using    | 2020-09-29 21:30:33.978 | 2020-09-29 21:30:33.978 |         |                 | capture |
| select c from t1 where b = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b_2`)*/ `c` FROM `test`.`t1` WHERE `b`=1234 | test       | rejected | 2020-09-29 21:32:20.978 | 2020-09-29 21:32:23.978 | utf8    | utf8_general_ci | evolve  |
+------------------------------+----------------------------------------------------------------------------------------+------------+----------+-------------------------+-------------------------+---------+-----------------+---------+
2 rows in set (0.00 sec)
```

TODO: Why is the plan above rejected????

The statement `ADMIN EVOLVE BINDINGS` will force evalation of new plans without waiting for `bind-info-lease` to elapse:

```sql
ADMIN EVOLVE BINDINGS;
SHOW GLOBAL BINDINGS;
```

```sql
Query OK, 0 rows affected (0.00 sec)

+------------------------------+----------------------------------------------------------------------------------------+------------+----------+-------------------------+-------------------------+---------+-----------------+---------+
| Original_sql                 | Bind_sql                                                                               | Default_db | Status   | Create_time             | Update_time             | Charset | Collation       | Source  |
+------------------------------+----------------------------------------------------------------------------------------+------------+----------+-------------------------+-------------------------+---------+-----------------+---------+
| select c from t1 where b = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`)*/ `c` FROM `t1` WHERE `b`=1234          | test       | using    | 2020-09-29 21:30:33.978 | 2020-09-29 21:30:33.978 |         |                 | capture |
| select c from t1 where b = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b_2`)*/ `c` FROM `test`.`t1` WHERE `b`=1234 | test       | rejected | 2020-09-29 21:32:20.978 | 2020-09-29 21:32:23.978 | utf8    | utf8_general_ci | evolve  |
+------------------------------+----------------------------------------------------------------------------------------+------------+----------+-------------------------+-------------------------+---------+-----------------+---------+
2 rows in set (0.00 sec)
```

Alternatively, undesired plans can also be removed by using `DROP GLOBAL BINDING`:

{{< copyable "sql" >}}

```sql
DROP GLOBAL BINDING FOR SELECT c FROM t1 WHERE b = 1234;
EXPLAIN SELECT c FROM t1 WHERE b = 1234;
```
```sql
Query OK, 0 rows affected (0.02 sec)

+--------------------------+---------+-----------+---------------------------+-------------------------------------+
| id                       | estRows | task      | access object             | operator info                       |
+--------------------------+---------+-----------+---------------------------+-------------------------------------+
| Projection_4             | 0.00    | root      |                           | test.t1.c                           |
| └─IndexReader_6          | 0.00    | root      |                           | index:IndexRangeScan_5              |
|   └─IndexRangeScan_5     | 0.00    | cop[tikv] | table:t1, index:b_2(b, c) | range:[1234,1234], keep order:false |
+--------------------------+---------+-----------+---------------------------+-------------------------------------+
3 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [SQL Plan Management (Baseline Evolution)](/sql-plan-management.md#baseline-evolution)
* [ADMIN CAPTURE BINDINGS](/sql-statements/sql-statement-admin-capture-bindings.md)
* [CREATE [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-create-binding.md)
* [DROP [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-drop-binding.md)
* [SHOW [GLOBAL|SESSION] BINDINGS](/sql-statements/sql-statement-show-bindings.md)