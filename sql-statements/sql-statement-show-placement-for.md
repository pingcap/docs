---
title: SHOW PLACEMENT FOR
summary: The usage of SHOW PLACEMENT FOR in TiDB.
---

# SHOW PLACEMENT FOR

`SHOW PLACEMENT FOR` summarizes all placement options from direct placement and placement policies, and presents them in canonical form for a specific table, database schema or partition.

## Synopsis

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT" "FOR" ShowPlacementTarget

ShowPlacementTarget ::=
	DatabaseSym DBName
|	"TABLE" TableName
|	"TABLE" TableName "PARTITION" Identifier
```

## Examples

{{< copyable "sql" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
use test;
ALTER DATABASE test PLACEMENT POLICY=p1;
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
SHOW PLACEMENT FOR DATABASE test;
SHOW PLACEMENT FOR TABLE t1;
SHOW CREATE TABLE t1\G
SHOW PLACEMENT FOR TABLE t2;
CREATE TABLE t3 (a INT) PARTITION BY RANGE (a) (PARTITION p1 VALUES LESS THAN (10), PARTITION p2 VALUES LESS THAN (20) FOLLOWERS=4);
SHOW TABLE FOR TABLE t3 PARTITION p1;
```

```
Query OK, 0 rows affected (0.02 sec)

Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.01 sec)

+---------------+----------------------------------------------------------------------+
| Target        | Placement                                                            |
+---------------+----------------------------------------------------------------------+
| DATABASE test | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 |
+---------------+----------------------------------------------------------------------+
1 row in set (0.00 sec)

+---------------+----------------------------------------------------------------------+
| Target        | Placement                                                            |
+---------------+----------------------------------------------------------------------+
| TABLE test.t1 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 |
+---------------+----------------------------------------------------------------------+
1 row in set (0.00 sec)

*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`p1` */
1 row in set (0.00 sec)

+---------------+----------------------------------------------------------------------+
| Target        | Placement                                                            |
+---------------+----------------------------------------------------------------------+
| TABLE test.t2 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 |
+---------------+----------------------------------------------------------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.14 sec)

+----------------------------+-------------+
| Target                     | Placement   |
+----------------------------+-------------+
| TABLE test.t3 PARTITION p2 | FOLLOWERS=4 |
+----------------------------+-------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Placement Rules](/placement-rules.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)