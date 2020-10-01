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
 pad VARBINARY(2048),
 INDEX (b)
);
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*10), FLOOR(RAND()*10000), HEX(RANDOM_BYTES(1000)) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;

SELECT SLEEP(1);
ANALYZE TABLE t1;
```

Ensure that the following statement is captured in a plan binding. It is okay if other statements also have bindings:

{{< copyable "sql" >}}

```sql
SELECT * FROM t1 WHERE b = 5 AND c = 1234;
SELECT * FROM t1 WHERE b = 4 AND c = 3928;
SELECT * FROM t1 WHERE b = 6 AND c = 9329;
DROP GLOBAL BINDING FOR SELECT * FROM t1 WHERE b = 5 AND c = 3210; -- drop incase this example is run twice
SHOW GLOBAL BINDINGS;
ADMIN CAPTURE BINDINGS;
SHOW GLOBAL BINDINGS;
```

```sql
IGNORE OUTPUT HERE...
```

The next step is to add an index on `(c)`. This index is actually a better index for the statement since `c` is more selective. However, because there is a plan binding in place it should not be used. We can confirm this using `EXPLAIN`:

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE b = 4 AND c = 3928;
ALTER TABLE t1 ADD INDEX (c);
SELECT SLEEP(1);
ANALYZE TABLE t1;
EXPLAIN SELECT * FROM t1 WHERE b = 4 AND c = 3928;
```
```sql
TODO... paste output.
```

By default, TiDB will continue to use the suboptimal index on `b` instead of `c`. When the option [`tidb_evolve_plan_baselines`](/system-variables.md#tidb_evolve_plan_baselines-new-in-v40) is enabled, TiDB will detect when a suboptimal plan is selected. After `bind-info-lease` has elapsed (default: 3s), the new plan will be either used or rejected:

```sql
SET tidb_evolve_plan_baselines = 1;
SELECT * FROM t1 WHERE b = 5 AND c = 1232;
SHOW GLOBAL BINDINGS;
SELECT SLEEP(5);
SHOW GLOBAL BINDINGS;
```

```sql
Query OK, 0 rows affected (0.00 sec)

..

+----------------------------------------+--------------------------------------------------------------------------------------------------+------------+--------+-------------------------+-------------------------+---------+-----------+---------+
| Original_sql                           | Bind_sql                                                                                         | Default_db | Status | Create_time             | Update_time             | Charset | Collation | Source  |
+----------------------------------------+--------------------------------------------------------------------------------------------------+------------+--------+-------------------------+-------------------------+---------+-----------+---------+
| select count ( ? ) from test . t1      | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`), stream_agg(@`sel_1`)*/ COUNT(1) FROM `test`.`t1` |            | using  | 2020-09-30 19:14:55.343 | 2020-09-30 19:14:55.343 |         |           | capture |
| select * from t1 where b = ? and c = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`)*/ * FROM `t1` WHERE `b`=5 AND `c`=1234            | test       | using  | 2020-09-30 19:14:55.393 | 2020-09-30 19:14:55.393 |         |           | capture |
+----------------------------------------+--------------------------------------------------------------------------------------------------+------------+--------+-------------------------+-------------------------+---------+-----------+---------+
2 rows in set (0.00 sec)

+----------+
| SLEEP(5) |
+----------+
|        0 |
+----------+
1 row in set (5.00 sec)

+----------------------------------------+--------------------------------------------------------------------------------------------------+------------+----------+-------------------------+-------------------------+---------+-----------------+---------+
| Original_sql                           | Bind_sql                                                                                         | Default_db | Status   | Create_time             | Update_time             | Charset | Collation       | Source  |
+----------------------------------------+--------------------------------------------------------------------------------------------------+------------+----------+-------------------------+-------------------------+---------+-----------------+---------+
| select count ( ? ) from test . t1      | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`), stream_agg(@`sel_1`)*/ COUNT(1) FROM `test`.`t1` |            | using    | 2020-09-30 19:14:55.343 | 2020-09-30 19:14:55.343 |         |                 | capture |
| select * from t1 where b = ? and c = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`)*/ * FROM `t1` WHERE `b`=5 AND `c`=1234            | test       | using    | 2020-09-30 19:14:55.393 | 2020-09-30 19:14:55.393 |         |                 | capture |
| select * from t1 where b = ? and c = ? | SELECT /*+ use_index(@`sel_1` `test`.`t1` `c`)*/ * FROM `test`.`t1` WHERE `b`=5 AND `c`=1232     | test       | rejected | 2020-09-30 19:16:44.693 | 2020-09-30 19:16:47.743 | utf8    | utf8_general_ci | evolve  |
+----------------------------------------+--------------------------------------------------------------------------------------------------+------------+----------+-------------------------+-------------------------+---------+-----------------+---------+
3 rows in set (0.00 sec)
```

TODO: Why is the plan above rejected???? There is clearly a performance improvement now:

```sql
mysql> DROP GLOBAL BINDING FOR SELECT * FROM t1 WHERE b = 5 AND c = 1232;
Query OK, 0 rows affected (0.03 sec)

mysql> EXPLAIN ANALYZE SELECT * FROM t1 FORCE INDEX (b) WHERE b = 5 AND c = 1232;
+-------------------------------+----------+---------+-----------+----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+-----------------------+------+
| id                            | estRows  | actRows | task      | access object        | execution info                                                                                                                                   | operator info                 | memory                | disk |
+-------------------------------+----------+---------+-----------+----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+-----------------------+------+
| IndexLookUp_8                 | 0.69     | 1       | root      |                      | time:118.168454ms, loops:2, cop_task: {num: 1, max:25.694373ms, proc_keys: 56943, rpc_num: 1, rpc_time: 25.670773ms, copr_cache_hit_ratio: 0.00} |                               | 1.0916099548339844 MB | N/A  |
| ├─IndexRangeScan_5(Build)     | 56544.00 | 56943   | cop[tikv] | table:t1, index:b(b) | time:24ms, loops:60                                                                                                                              | range:[5,5], keep order:false | N/A                   | N/A  |
| └─Selection_7(Probe)          | 0.69     | 0       | cop[tikv] |                      | time:0ns, loops:0                                                                                                                                | eq(test.t1.c, 1232)           | N/A                   | N/A  |
|   └─TableRowIDScan_6          | 56544.00 | 0       | cop[tikv] | table:t1             | time:0ns, loops:0                                                                                                                                | keep order:false              | N/A                   | N/A  |
+-------------------------------+----------+---------+-----------+----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------+-----------------------+------+
4 rows in set (0.12 sec)

mysql> EXPLAIN ANALYZE SELECT * FROM t1 FORCE INDEX (c) WHERE b = 5 AND c = 1232;
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------+----------------+------+
| id                            | estRows | actRows | task      | access object        | execution info                                                                                                                            | operator info                       | memory         | disk |
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------+----------------+------+
| IndexLookUp_8                 | 0.69    | 1       | root      |                      | time:9.246177ms, loops:2, cop_task: {num: 1, max:386.167µs, proc_keys: 44, rpc_num: 1, rpc_time: 370.197µs, copr_cache_hit_ratio: 0.00}   |                                     | 12.01171875 KB | N/A  |
| ├─IndexRangeScan_5(Build)     | 7.00    | 44      | cop[tikv] | table:t1, index:c(c) | time:0s, loops:2                                                                                                                          | range:[1232,1232], keep order:false | N/A            | N/A  |
| └─Selection_7(Probe)          | 0.69    | 0       | cop[tikv] |                      | time:0ns, loops:0                                                                                                                         | eq(test.t1.b, 5)                    | N/A            | N/A  |
|   └─TableRowIDScan_6          | 7.00    | 0       | cop[tikv] | table:t1             | time:0ns, loops:0                                                                                                                         | keep order:false                    | N/A            | N/A  |
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------+----------------+------+
4 rows in set (0.01 sec)
```

The statement `ADMIN EVOLVE BINDINGS` will force evalation of new plans without waiting for `bind-info-lease` to elapse:

```sql
ADMIN EVOLVE BINDINGS;
SHOW GLOBAL BINDINGS;
```

```sql
Query OK, 0 rows affected (0.00 sec)

TODO: show output.
```

Alternatively, undesired plans can also be removed by using `DROP GLOBAL BINDING`:

{{< copyable "sql" >}}

```sql
DROP GLOBAL BINDING FOR SELECT * FROM t1 WHERE b = 5 AND c = 1234;
EXPLAIN SELECT * FROM t1 WHERE b = 5 AND c = 1234;
```
```sql
Query OK, 0 rows affected (0.02 sec)

TODO - show output
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [SQL Plan Management (Baseline Evolution)](/sql-plan-management.md#baseline-evolution)
* [ADMIN CAPTURE BINDINGS](/sql-statements/sql-statement-admin-capture-bindings.md)
* [CREATE [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-create-binding.md)
* [DROP [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-drop-binding.md)
* [SHOW [GLOBAL|SESSION] BINDINGS](/sql-statements/sql-statement-show-bindings.md)
