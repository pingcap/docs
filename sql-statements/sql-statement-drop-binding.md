---
title: DROP [GLOBAL|SESSION] BINDING
summary: Use of DROP BINDING in TiDB database.
---

# DROP [GLOBAL|SESSION] BINDING

This statement removes a binding from a specific SQL statement. Bindings can be used to inject a hint into a statement without requiring changes to the underlying query.

A `BINDING` can be on either a `GLOBAL` or `SESSION` basis. The default is `SESSION`.

## Synopsis

```ebnf+diagram
DropBindingStmt ::=
    'DROP' GlobalScope 'BINDING' 'FOR' ( BindableStmt ( 'USING' BindableStmt )?
|   'SQL' 'DIGEST' StringLiteralOrUserVariableList )

GlobalScope ::=
    ( 'GLOBAL' | 'SESSION' )?

BindableStmt ::=
    ( SelectStmt | UpdateStmt | InsertIntoStmt | ReplaceIntoStmt | DeleteStmt )

StringLiteralOrUserVariableList ::=
    ( StringLitOrUserVariable | StringLiteralOrUserVariableList ',' StringLitOrUserVariable )

StringLiteralOrUserVariable ::=
    ( stringLiteral | UserVariable )
```

## Examples

You can remove a binding according to a SQL statement or SQL Digest.

When you remove a binding according to SQL Digest, you need to specify the corresponding SQL Digest:

- You can use either the string literal or user variable of the string type to specify the Plan Digest.
- You can specify multiple string values, and include multiple digests in each string. Note that the strings or digests need to be separated by commas.

The following example shows how to remove a binding according to a SQL statement.

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

mysql> SHOW SESSION BINDINGS\G
Empty set (0.00 sec)
```

The following example shows how to remove a binding according to SQL Digest.

```sql
CREATE TABLE t1(a INT, b INT, c INT, INDEX ia(a));
CREATE TABLE t2(a INT, b INT, c INT, INDEX ia(a));
CREATE GLOBAL BINDING FOR SELECT * FROM t1 WHERE a > 1 USING SELECT * FROM t1 USE INDEX (ia) WHERE a > 1;
CREATE GLOBAL BINDING FOR SELECT * FROM t2 WHERE a < 1 USING SELECT * FROM t2 USE INDEX (ia) WHERE a < 1;
CREATE GLOBAL BINDING FOR SELECT * FROM t1 JOIN t2 ON t1.b = t2.a USING SELECT /*+ HASH_JOIN(t1) */ * FROM t1 JOIN t2 ON t1.b = t2.a;
SHOW GLOBAL BINDINGS;
```

Method 1:

```sql
DROP GLOBAL BINDING FOR SQL DIGEST '31026623c8f22264fe0dfc26f29c69c5c457d6b85960c578ebcf17a967ed7893', '0f38b2e769927ae37981c66f0988c6299b602e03f029e38aa071e656fc321593', '3c8dfc451b0e36afd904cefca5137e68fb051f02964e1958ed60afdadc25f57e';
SHOW GLOBAL BINDINGS;
```

Method 2:

```sql
SET @digests='31026623c8f22264fe0dfc26f29c69c5c457d6b85960c578ebcf17a967ed7893, 0f38b2e769927ae37981c66f0988c6299b602e03f029e38aa071e656fc321593, 3c8dfc451b0e36afd904cefca5137e68fb051f02964e1958ed60afdadc25f57e';
DROP GLOBAL BINDING FOR SQL DIGEST @digests;
SHOW GLOBAL BINDINGS;
```

```sql
> CREATE TABLE t1(a INT, b INT, c INT, INDEX ia(a));
Query OK, 0 rows affected (0.044 sec)

> CREATE TABLE t2(a INT, b INT, c INT, INDEX ia(a));
Query OK, 0 rows affected (0.035 sec)

> CREATE GLOBAL BINDING FOR SELECT * FROM t1 WHERE a > 1 USING SELECT * FROM t1 USE INDEX (ia) WHERE a > 1;
Query OK, 0 rows affected (0.011 sec)

> CREATE GLOBAL BINDING FOR SELECT * FROM t2 WHERE a < 1 USING SELECT * FROM t2 USE INDEX (ia) WHERE a < 1;
Query OK, 0 rows affected (0.013 sec)

> CREATE GLOBAL BINDING FOR SELECT * FROM t1 JOIN t2 ON t1.b = t2.a USING SELECT /*+ HASH_JOIN(t1) */ * FROM t1 JOIN t2 ON t1.b = t2.a;
Query OK, 0 rows affected (0.012 sec)

> SHOW GLOBAL BINDINGS;
+---------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| Original_sql                                                              | Bind_sql                                                                                | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source | Sql_digest                                                       | Plan_digest |
+---------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| select * from `test` . `t1` join `test` . `t2` on `t1` . `b` = `t2` . `a` | SELECT /*+ HASH_JOIN(`t1`)*/ * FROM `test`.`t1` JOIN `test`.`t2` ON `t1`.`b` = `t2`.`a` | test       | enabled | 2024-08-11 04:06:49.953 | 2024-08-11 04:06:49.953 | utf8    | utf8_general_ci | manual | 31026623c8f22264fe0dfc26f29c69c5c457d6b85960c578ebcf17a967ed7893 |             |
| select * from `test` . `t2` where `a` < ?                                 | SELECT * FROM `test`.`t2` USE INDEX (`ia`) WHERE `a` < 1                                | test       | enabled | 2024-08-11 04:06:49.937 | 2024-08-11 04:06:49.937 | utf8    | utf8_general_ci | manual | 0f38b2e769927ae37981c66f0988c6299b602e03f029e38aa071e656fc321593 |             |
| select * from `test` . `t1` where `a` > ?                                 | SELECT * FROM `test`.`t1` USE INDEX (`ia`) WHERE `a` > 1                                | test       | enabled | 2024-08-11 04:06:49.924 | 2024-08-11 04:06:49.924 | utf8    | utf8_general_ci | manual | 3c8dfc451b0e36afd904cefca5137e68fb051f02964e1958ed60afdadc25f57e |             |
+---------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
3 rows in set (0.001 sec)

> DROP GLOBAL BINDING FOR SQL DIGEST '31026623c8f22264fe0dfc26f29c69c5c457d6b85960c578ebcf17a967ed7893', '0f38b2e769927ae37981c66f0988c6299b602e03f029e38aa071e656fc321593', '3c8dfc451b0e36afd904cefca5137e68fb051f02964e1958ed60afdadc25f57e';
Query OK, 3 rows affected (0.019 sec)

> SHOW GLOBAL BINDINGS;
Empty set (0.002 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [CREATE [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-create-binding.md)
* [SHOW [GLOBAL|SESSION] BINDINGS](/sql-statements/sql-statement-show-bindings.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [Optimizer Hints](/optimizer-hints.md)
* [SQL Plan Management](/sql-plan-management.md)
