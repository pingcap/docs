---
title: DROP PLACEMENT POLICY
summary: The usage of ALTER PLACEMENT POLICY in TiDB.
---

# DROP PLACEMENT POLICY

`DROP PLACEMENT POLICY` is used to drop a previously created placement policy.

## Synopsis

```ebnf+diagram
DropPolicyStmt ::=
    "DROP" "PLACEMENT" "POLICY" IfExists PolicyName

PolicyName ::=
    Identifier
```

## Examples

Placement policies can only be dropped when they are not referenced by any tables or partitions.

{{< copyable "sql" >}}

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=4;
CREATE TABLE t1 (a INT PRIMARY KEY) PLACEMENT POLICY=p1;
DROP PLACEMENT POLICY p1;  -- This statement fails because the placement policy p1 is referenced.

-- Finds which tables and partitions reference the placement policy.
SELECT table_schema, table_name FROM information_schema.tables WHERE tidb_placement_policy_name='p1';
SELECT table_schema, table_name FROM information_schema.partitions WHERE tidb_placement_policy_name='p1';

ALTER TABLE t1 PLACEMENT POLICY=default;  -- Removes the placement policy from t1.
DROP PLACEMENT POLICY p1;  -- Succeeds.
```

```sql
Query OK, 0 rows affected (0.10 sec)

Query OK, 0 rows affected (0.11 sec)

ERROR 8241 (HY000): Placement policy 'p1' is still in use

+--------------+------------+
| table_schema | table_name |
+--------------+------------+
| test         | t1         |
+--------------+------------+
1 row in set (0.00 sec)

Empty set (0.01 sec)

Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.21 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/common/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/common/sql-statements/sql-statement-create-placement-policy.md)
* [ALTER PLACEMENT POLICY](/common/sql-statements/sql-statement-alter-placement-policy.md)
