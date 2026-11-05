---
title: TIDB_CHECK_CONSTRAINTS
summary: Learn the `TIDB_CHECK_CONSTRAINTS` INFORMATION_SCHEMA table.
---

# TIDB\_CHECK\_CONSTRAINTS

The `TIDB_CHECK_CONSTRAINTS` table provides information about [`CHECK` constraints](/constraints.md#check) on tables. In addition to the columns in [`CHECK_CONSTRAINTS`](/information-schema/information-schema-check-constraints.md), `TIDB_CHECK_CONSTRAINTS` provides the name and ID of the table that defines the `CHECK` constraint.

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_CHECK_CONSTRAINTS;
```

The output is as follows:

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| CONSTRAINT_CATALOG | varchar(64) | NO   |      | NULL    |       |
| CONSTRAINT_SCHEMA  | varchar(64) | NO   |      | NULL    |       |
| CONSTRAINT_NAME    | varchar(64) | NO   |      | NULL    |       |
| CHECK_CLAUSE       | longtext    | NO   |      | NULL    |       |
| TABLE_NAME         | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID           | bigint(21)  | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

The following example adds a `CHECK` constraint using the `CREATE TABLE` statement:

```sql
SET GLOBAL tidb_enable_check_constraint = ON;
CREATE TABLE test.t1 (id INT PRIMARY KEY, CHECK (id%2 = 0));
SELECT * FROM TIDB_CHECK_CONSTRAINTS\G
```

The output is as follows:

```sql
*************************** 1. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: test
   CONSTRAINT_NAME: t1_chk_1
      CHECK_CLAUSE: (`id` % 2 = 0)
        TABLE_NAME: t1
          TABLE_ID: 107
1 row in set (0.02 sec)
```

Fields in the `TIDB_CHECK_CONSTRAINTS` table are described as follows:

* `CONSTRAINT_CATALOG`: The catalog of the constraint, which is always `def`.
* `CONSTRAINT_SCHEMA`: The schema of the constraint.
* `CONSTRAINT_NAME`: The name of the constraint.
* `CHECK_CLAUSE`: The clause of the check constraint.
* `TABLE_NAME`: The name of the table where the constraint is located.
* `TABLE_ID`: The ID of the table where the constraint is located.
