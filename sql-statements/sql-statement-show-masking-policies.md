---
title: SHOW MASKING POLICIES
summary: An overview of the usage of SHOW MASKING POLICIES in the TiDB database.
---

# SHOW MASKING POLICIES

The `SHOW MASKING POLICIES` statement lets you view information about the [Column-level masking policies](column-level-masking-policy.md) defined on a specified table.

## Required privileges

To view masking policies, you must have the `ALTER MASKING POLICY` privilege on the target table.

## Syntax diagram

```ebnf+diagram
ShowMaskingPoliciesStmt ::=
    'SHOW' 'MASKING' 'POLICIES' 'FOR' TableName WhereClauseOptional

TableName ::=
    Identifier ('.' Identifier)?

WhereClauseOptional ::=
    ( 'WHERE' Expression )?
```

## Examples

After creating masking policies, use `SHOW MASKING POLICIES` to view policy information:

```sql
CREATE TABLE employees (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  ssn VARCHAR(20),
  salary DECIMAL(10,2)
);

CREATE MASKING POLICY p_mask_ssn
  ON employees(ssn)
  AS MASK_FULL(ssn) ENABLE;

CREATE MASKING POLICY p_mask_salary
  ON employees(salary)
  AS MASK_NULL(salary) ENABLE;

SHOW MASKING POLICIES FOR employees;
```

```
Query OK, 0 rows affected (0.10 sec)

Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.08 sec)

+----------------+---------+--------+-----------------+-----------+
| PolicyName     | Column  | Status | Expression      | Restrict  |
+----------------+---------+--------+-----------------+-----------+
| p_mask_ssn     | ssn     | ENABLE | MASK_FULL(ssn)  | NONE      |
| p_mask_salary  | salary  | ENABLE | MASK_NULL(salary) | NONE    |
+----------------+---------+--------+-----------------+-----------+
2 rows in set (0.01 sec)
```

### Filter results using the WHERE clause

You can also use the `WHERE` clause to filter masking policies that meet specific conditions. For example, you can view enabled masking policies on the `employees` table as follows:

```sql
SHOW MASKING POLICIES FOR employees WHERE Status = 'ENABLE';
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [CREATE MASKING POLICY](/sql-statements/sql-statement-create-masking-policy.md)
* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)