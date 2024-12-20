---
title: CREATE [GLOBAL|SESSION] BINDING
summary: Use of CREATE BINDING in TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-create-binding/']
---

# CREATE [GLOBAL|SESSION] BINDING

This statement creates a new execution plan binding in TiDB. Binding can be used to inject a hint into a statement without requiring changes to the underlying query.

A `BINDING` can be on either a `GLOBAL` or `SESSION` basis. The default is `SESSION`.

The bound SQL statement is parameterized and stored in the system table. When a SQL query is processed, as long as the parameterized SQL statement and a bound one in the system table are consistent and the system variable `tidb_use_plan_baselines` is set to `ON` (default), the corresponding optimizer hint is available. If multiple execution plans are available, the optimizer chooses to bind the plan with the least cost. For more information, see [Create a binding](/sql-plan-management.md#create-a-binding).

## Synopsis

```ebnf+diagram
CreateBindingStmt ::=
    'CREATE' GlobalScope 'BINDING' ( 'FOR' BindableStmt 'USING' BindableStmt
|   'FROM' 'HISTORY' 'USING' 'PLAN' 'DIGEST' StringLiteralOrUserVariableList )

GlobalScope ::=
    ( 'GLOBAL' | 'SESSION' )?

BindableStmt ::=
    ( SelectStmt | UpdateStmt | InsertIntoStmt | ReplaceIntoStmt | DeleteStmt )

StringLiteralOrUserVariableList ::=
    ( StringLitOrUserVariable | StringLiteralOrUserVariableList ',' StringLitOrUserVariable )

StringLiteralOrUserVariable ::=
    ( stringLiteral | UserVariable )
```

****

## Examples

You can create a binding according to a SQL statement or a historical execution plan.

When you create a binding according to a historical execution plan, you need to specify the corresponding Plan Digest:

- You can use either the string literal or user variable of the string type to specify the Plan Digest.
- You can specify multiple Plan Digests to create bindings for multiple statements at the same time. In this case, you can specify multiple strings, and include multiple digests in each string. Note that the strings or digests need to be separated by commas.

The following example shows how to create a binding according to a SQL statement.

{{< copyable "sql" >}}

```sql
mysql> CREATE TABLE t1 (
     id INT NOT NULL PRIMARY KEY auto_increment,
     b INT NOT NULL,
     pad VARBINARY(255),
     INDEX(b)
    );
Query OK, 0 rows affected (0.07 sec)

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM dual;
Query OK, 1 row affected (0.01 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 8 rows affected (0.00 sec)
Records: 8  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 1000 rows affected (0.04 sec)
Records: 1000  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 100000 rows affected (1.74 sec)
Records: 100000  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 100000 rows affected (2.15 sec)
Records: 100000  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 100000 rows affected (2.64 sec)
Records: 100000  Duplicates: 0  Warnings: 0

mysql> SELECT SLEEP(1);
+----------+
| SLEEP(1) |
+----------+
|        0 |
+----------+
1 row in set (1.00 sec)

mysql> ANALYZE TABLE t1;
Query OK, 0 rows affected (1.33 sec)

mysql> EXPLAIN ANALYZE SELECT * FROM t1 WHERE b = 123;
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
| id                            | estRows | actRows | task      | access object        | execution info                                                            | operator info                     | memory         | disk |
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
| IndexLookUp_10                | 583.00  | 297     | root      |                      | time:10.545072ms, loops:2, rpc num: 1, rpc time:398.359µs, proc keys:297  |                                   | 109.1484375 KB | N/A  |
| ├─IndexRangeScan_8(Build)     | 583.00  | 297     | cop[tikv] | table:t1, index:b(b) | time:0s, loops:4                                                          | range:[123,123], keep order:false | N/A            | N/A  |
| └─TableRowIDScan_9(Probe)     | 583.00  | 297     | cop[tikv] | table:t1             | time:12ms, loops:4                                                        | keep order:false                  | N/A            | N/A  |
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
3 rows in set (0.02 sec)

mysql> CREATE SESSION BINDING FOR
         SELECT * FROM t1 WHERE b = 123
        USING
         SELECT * FROM t1 IGNORE INDEX (b) WHERE b = 123;
Query OK, 0 rows affected (0.00 sec)

mysql> EXPLAIN ANALYZE SELECT * FROM t1 WHERE b = 123;
+-------------------------+-----------+---------+-----------+---------------+--------------------------------------------------------------------------------+--------------------+---------------+------+
| id                      | estRows   | actRows | task      | access object | execution info                                                                 | operator info      | memory        | disk |
+-------------------------+-----------+---------+-----------+---------------+--------------------------------------------------------------------------------+--------------------+---------------+------+
| TableReader_7           | 583.00    | 297     | root      |               | time:222.32506ms, loops:2, rpc num: 1, rpc time:222.078952ms, proc keys:301010 | data:Selection_6   | 88.6640625 KB | N/A  |
| └─Selection_6           | 583.00    | 297     | cop[tikv] |               | time:224ms, loops:298                                                          | eq(test.t1.b, 123) | N/A           | N/A  |
|   └─TableFullScan_5     | 301010.00 | 301010  | cop[tikv] | table:t1      | time:220ms, loops:298                                                          | keep order:false   | N/A           | N/A  |
+-------------------------+-----------+---------+-----------+---------------+--------------------------------------------------------------------------------+--------------------+---------------+------+
3 rows in set (0.22 sec)

mysql> SHOW SESSION BINDINGS\G
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

mysql> DROP SESSION BINDING FOR SELECT * FROM t1 WHERE b = 123;
Query OK, 0 rows affected (0.00 sec)

mysql> EXPLAIN ANALYZE SELECT * FROM t1 WHERE b = 123;
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------+-----------------------------------+----------------+------+
| id                            | estRows | actRows | task      | access object        | execution info                                                          | operator info                     | memory         | disk |
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------+-----------------------------------+----------------+------+
| IndexLookUp_10                | 583.00  | 297     | root      |                      | time:5.31206ms, loops:2, rpc num: 1, rpc time:665.927µs, proc keys:297  |                                   | 109.1484375 KB | N/A  |
| ├─IndexRangeScan_8(Build)     | 583.00  | 297     | cop[tikv] | table:t1, index:b(b) | time:0s, loops:4                                                        | range:[123,123], keep order:false | N/A            | N/A  |
| └─TableRowIDScan_9(Probe)     | 583.00  | 297     | cop[tikv] | table:t1             | time:0s, loops:4                                                        | keep order:false                  | N/A            | N/A  |
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------+-----------------------------------+----------------+------+
3 rows in set (0.01 sec)
```

The following example shows how to create a binding according to a historical execution plan.

```sql
USE test;
CREATE TABLE t1(a INT, b INT, c INT, INDEX ia(a));
CREATE TABLE t2(a INT, b INT, c INT, INDEX ia(a));
INSERT INTO t1 SELECT * FROM t2 WHERE a = 1;
SELECT @@LAST_PLAN_FROM_BINDING;
UPDATE /*+ INL_JOIN(t2) */ t1, t2 SET t1.a = 1 WHERE t1.b = t2.a;
SELECT @@LAST_PLAN_FROM_BINDING;
DELETE /*+ HASH_JOIN(t1) */ t1 FROM t1 JOIN t2 WHERE t1.b = t2.a;
SELECT @@LAST_PLAN_FROM_BINDING;
SELECT * FROM t1 WHERE t1.a IN (SELECT a FROM t2);
SELECT @@LAST_PLAN_FROM_BINDING;
```

Method 1:

```sql
SELECT query_sample_text, stmt_type, table_names, plan_digest FROM information_schema.statements_summary_history WHERE table_names LIKE '%test.t1%' AND stmt_type != 'CreateTable';
CREATE GLOBAL BINDING FROM HISTORY USING PLAN DIGEST 'e72819cf99932f63a548156dbf433adda60e10337e89dcaa8638b4caf16f64d8,c291edc36b2482738d3389d335f37efc76290be2930330fe5034c5f4c42eeb36,8dc146249484f4a6ab219bfe9effa6b7a18aeed3764d49b610da61ac347ab914,73b2dec866595688ea416675f88ccb3456eb8e7443a79cd816695b688e07ac6b';
```

Method 2:

```sql
SELECT @digests:=GROUP_CONCAT(plan_digest) FROM information_schema.statements_summary_history WHERE table_names LIKE '%test.t1%' AND stmt_type != 'CreateTable';
CREATE GLOBAL BINDING FROM HISTORY USING PLAN DIGEST @digests;
```

```sql
SHOW GLOBAL BINDINGS;
INSERT INTO t1 SELECT * FROM t2 WHERE a = 1;
SELECT @@LAST_PLAN_FROM_BINDING;
UPDATE t1, t2 SET t1.a = 1 WHERE t1.b = t2.a;
SELECT @@LAST_PLAN_FROM_BINDING;
DELETE t1 FROM t1 JOIN t2 WHERE t1.b = t2.a;
SELECT @@LAST_PLAN_FROM_BINDING;
SELECT * FROM t1 WHERE t1.a IN (SELECT a FROM t2);
SELECT @@LAST_PLAN_FROM_BINDING;
```

```sql
> CREATE TABLE t1(a INT, b INT, c INT, INDEX ia(a));
Query OK, 0 rows affected (0.048 sec)

> CREATE TABLE t2(a INT, b INT, c INT, INDEX ia(a));
Query OK, 0 rows affected (0.035 sec)

> INSERT INTO t1 SELECT * FROM t2 WHERE a = 1;
Query OK, 0 rows affected (0.002 sec)
Records: 0  Duplicates: 0  Warnings: 0

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.001 sec)

> UPDATE /*+ INL_JOIN(t2) */ t1, t2 SET t1.a = 1 WHERE t1.b = t2.a;
Query OK, 0 rows affected (0.005 sec)
Rows matched: 0  Changed: 0  Warnings: 0

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.000 sec)

> DELETE /*+ HASH_JOIN(t1) */ t1 FROM t1 JOIN t2 WHERE t1.b = t2.a;
Query OK, 0 rows affected (0.003 sec)

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.000 sec)

> SELECT * FROM t1 WHERE t1.a IN (SELECT a FROM t2);
Empty set (0.002 sec)

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.001 sec)

> SELECT @digests:=GROUP_CONCAT(plan_digest) FROM information_schema.statements_summary_history WHERE table_names LIKE '%test.t1%' AND stmt_type != 'CreateTable';
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| @digests:=GROUP_CONCAT(plan_digest)                                                                                                                                                                                                                                 |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 73b2dec866595688ea416675f88ccb3456eb8e7443a79cd816695b688e07ac6b,8dc146249484f4a6ab219bfe9effa6b7a18aeed3764d49b610da61ac347ab914,c291edc36b2482738d3389d335f37efc76290be2930330fe5034c5f4c42eeb36,e72819cf99932f63a548156dbf433adda60e10337e89dcaa8638b4caf16f64d8 |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)

> CREATE GLOBAL BINDING FROM HISTORY USING PLAN DIGEST @digests;
Query OK, 0 rows affected (0.060 sec)

> SHOW GLOBAL BINDINGS;
+----------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+---------+------------------------------------------------------------------+------------------------------------------------------------------+
| Original_sql                                                                                 | Bind_sql                                                                                                                                                                                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source  | Sql_digest                                                       | Plan_digest                                                      |
+----------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+---------+------------------------------------------------------------------+------------------------------------------------------------------+
| insert into `test` . `t1` select * from `test` . `t2` where `a` = ?                          | INSERT INTO `test`.`t1` SELECT /*+ use_index(@`sel_1` `test`.`t2` `ia`) no_order_index(@`sel_1` `test`.`t2` `ia`)*/ * FROM `test`.`t2` WHERE `a` = 1                                                                                   | test       | enabled | 2024-08-11 05:27:19.669 | 2024-08-11 05:27:19.669 | utf8    | utf8_general_ci | history | bd23e6af17e7b77b25383e50e258f0dece18583d19772f08caacb2021945a300 | e72819cf99932f63a548156dbf433adda60e10337e89dcaa8638b4caf16f64d8 |
| update ( `test` . `t1` ) join `test` . `t2` set `t1` . `a` = ? where `t1` . `b` = `t2` . `a` | UPDATE /*+ inl_join(`test`.`t2`) use_index(@`upd_1` `test`.`t1` ) use_index(@`upd_1` `test`.`t2` `ia`) no_order_index(@`upd_1` `test`.`t2` `ia`)*/ (`test`.`t1`) JOIN `test`.`t2` SET `t1`.`a`=1 WHERE `t1`.`b` = `t2`.`a`             | test       | enabled | 2024-08-11 05:27:19.667 | 2024-08-11 05:27:19.667 | utf8    | utf8_general_ci | history | 987e91af17eb40e36fecfc0634cce0b6a736de02bb009091810f932804fc02e9 | c291edc36b2482738d3389d335f37efc76290be2930330fe5034c5f4c42eeb36 |
| delete `test` . `t1` from `test` . `t1` join `test` . `t2` where `t1` . `b` = `t2` . `a`     | DELETE /*+ hash_join_build(`test`.`t2`) use_index(@`del_1` `test`.`t1` ) use_index(@`del_1` `test`.`t2` )*/ `test`.`t1` FROM `test`.`t1` JOIN `test`.`t2` WHERE `t1`.`b` = `t2`.`a`                                                    | test       | enabled | 2024-08-11 05:27:19.664 | 2024-08-11 05:27:19.664 | utf8    | utf8_general_ci | history | 70ef3d442d95c51020a76c7c86a3ab674258606d4dd24bbd16ac6f69d87a4316 | 8dc146249484f4a6ab219bfe9effa6b7a18aeed3764d49b610da61ac347ab914 |
| select * from `test` . `t1` where `t1` . `a` in ( select `a` from `test` . `t2` )            | SELECT /*+ use_index(@`sel_1` `test`.`t1` ) stream_agg(@`sel_2`) use_index(@`sel_2` `test`.`t2` `ia`) order_index(@`sel_2` `test`.`t2` `ia`) agg_to_cop(@`sel_2`)*/ * FROM `test`.`t1` WHERE `t1`.`a` IN (SELECT `a` FROM `test`.`t2`) | test       | enabled | 2024-08-11 05:27:19.649 | 2024-08-11 05:27:19.649 | utf8    | utf8_general_ci | history | b58508a5e29d7889adf98cad50343d7a575fd32ad55dbdaa88e14ecde54f3d93 | 73b2dec866595688ea416675f88ccb3456eb8e7443a79cd816695b688e07ac6b |
+----------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+---------+------------------------------------------------------------------+------------------------------------------------------------------+
4 rows in set (0.001 sec)

> INSERT INTO t1 SELECT * FROM t2 WHERE a = 1;
Query OK, 0 rows affected (0.002 sec)
Records: 0  Duplicates: 0  Warnings: 0

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.000 sec)

> UPDATE t1, t2 SET t1.a = 1 WHERE t1.b = t2.a;
Query OK, 0 rows affected (0.002 sec)
Rows matched: 0  Changed: 0  Warnings: 0

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.000 sec)

> DELETE t1 FROM t1 JOIN t2 WHERE t1.b = t2.a;
Query OK, 0 rows affected (0.002 sec)

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.000 sec)

> SELECT * FROM t1 WHERE t1.a IN (SELECT a FROM t2);
Empty set (0.002 sec)

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.002 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [DROP [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-drop-binding.md)
* [SHOW [GLOBAL|SESSION] BINDINGS](/sql-statements/sql-statement-show-bindings.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [Optimizer Hints](/optimizer-hints.md)
* [SQL Plan Management](/sql-plan-management.md)
