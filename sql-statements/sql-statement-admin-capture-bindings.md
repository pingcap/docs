---
title: ADMIN CAPTURE BINDINGS | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
---

# ADMIN CAPTURE BINDINGS

The statement `ADMIN CAPTURE BINDINGS` allows you to create plan bindings for SQL statements that have previously been executed on a TiDB servers more than once.

## Synopsis

**AdminStmt:**

![AdminStmt](/media/sqlgram/AdminStmt.png)

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

Initially this system has no global plan bindings:

{{< copyable "sql" >}}

```sql
SHOW GLOBAL BINDINGS;
```

```sql
Empty set (0.00 sec)
```

Execute the following statement multiple times, and then confirm its execution in [`information_schema.statements_summary`](/statement-summary-tables.md):

{{< copyable "sql" >}}

```sql
SELECT * FROM t1 WHERE b = 1234;
SELECT * FROM t1 WHERE b = 199;
SELECT * FROM t1 WHERE b = 2048;
SELECT digest_text, exec_count FROM information_schema.statements_summary WHERE exec_count > 1;
```

```sql
+----------------------------------------------------------------------------------------------------------------+------------+
| digest_text                                                                                                    | exec_count |
+----------------------------------------------------------------------------------------------------------------+------------+
| select * from t1 where b = ?                                                                                   |          3 |
| insert into t1 select null , floor ( rand ( ) * ? ) , random_bytes ( ? ) from t1 a join t1 b join t1 c limit ? |          6 |
+----------------------------------------------------------------------------------------------------------------+------------+
2 rows in set (0.00 sec)
```

The query execution plan for `SELECT` statements with an `exec_count >= 1` will be _captured_ by `ADMIN CAPTURE BINDINGS`. This helps improve plan stability because the execution plan is locked in place:

{{< copyable "sql" >}}

```sql
ADMIN CAPTURE BINDINGS;
SHOW GLOBAL BINDINGS\G
```

```sql
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GLOBAL BINDINGS\G
*************************** 1. row ***************************
Original_sql: select * from t1 where b = ?
    Bind_sql: SELECT /*+ use_index(@`sel_1` `test`.`t1` `b`)*/ * FROM `t1` WHERE `b`=1234
  Default_db: test
      Status: using
 Create_time: 2020-09-29 20:03:42.458
 Update_time: 2020-09-29 20:03:42.458
     Charset: 
   Collation: 
      Source: capture
1 row in set (0.00 sec)

```

Any automatically captured plan bindings can be dropped with `DROP GLOBAL BINDINGS`:

```sql
DROP GLOBAL BINDING FOR SELECT * FROM t1 WHERE b = 123;
SHOW GLOBAL BINDINGS;
```

```sql
Query OK, 0 rows affected (0.02 sec)

Empty set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [SQL Plan Management (Baseline Capturing)](/sql-plan-management.md#baseline-capturing)
* [ADMIN EVOLVE BINDINGS](/sql-statements/sql-statement-admin-evolve-bindings.md)
* [CREATE [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-create-binding.md)
* [DROP [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-drop-binding.md)
* [SHOW [GLOBAL|SESSION] BINDINGS](/sql-statements/sql-statement-show-bindings.md)