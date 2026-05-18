---
title: CREATE ROW ACCESS POLICY
summary: "Creates a new row access policy in {{{ .lake }}}. A row access policy defines a Boolean predicate that {{{ .lake }}} applies to rows when the policy is attached to a table."
---

# CREATE ROW ACCESS POLICY

> **Note:**
>
> Introduced or updated in v1.2.845.

Creates a new row access policy in {{{ .lake }}}. A row access policy defines a Boolean predicate that {{{ .lake }}} applies to rows when the policy is attached to a table.

## Syntax

```sql
CREATE ROW ACCESS POLICY [ IF NOT EXISTS ] <policy_name> AS
    ( <arg_name> <arg_type> [ , <arg_name> <arg_type> ... ] )
    RETURNS BOOLEAN -> <predicate_expression>
    [ COMMENT = '<comment>' ]
```

| Parameter | Description |
|-----------|-------------|
| `policy_name` | Name of the row access policy to create. Policy names share the same namespace as masking policies. |
| `arg_name` | Policy argument name used inside the predicate expression. Argument names do not need to match table column names. |
| `arg_type` | Data type for the argument. When the policy is attached, each listed table column must match the corresponding argument type. |
| `predicate_expression` | Boolean expression that decides whether a row is visible. Rows are returned only when this expression evaluates to `TRUE`. |
| `comment` | Optional comment that stores notes about the policy. |

> **Note:**
>
> - Row access policy is currently experimental. Enable it with `SET enable_experimental_row_access_policy = 1` or `SET GLOBAL enable_experimental_row_access_policy = 1`.
> - The policy must return `BOOLEAN`.
> - The columns listed in `ALTER TABLE ... ADD ROW ACCESS POLICY ... ON (...)` bind to policy arguments by position.
> - Subquery predicates are not supported in row access policy definitions.

## Access Control Requirements

| Privilege | Description |
|:----------|:------------|
| CREATE ROW ACCESS POLICY | Required to create a row access policy. Typically granted on `*.*`. |

{{{ .lake }}} automatically grants OWNERSHIP on the new row access policy to the current role so that it can manage the policy with others.

## Examples

This example creates a policy that only exposes rows from the `Engineering` department, unless the current role is `admin`.

```sql
SET enable_experimental_row_access_policy = 1;

CREATE TABLE employees (
    id INT,
    name STRING,
    department STRING
);

INSERT INTO employees VALUES
    (1, 'Alice', 'Engineering'),
    (2, 'Bob', 'Sales'),
    (3, 'Charlie', 'Engineering');

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN ->
  CASE
    WHEN current_role() = 'admin' THEN true
    WHEN dept = 'Engineering' THEN true
    ELSE false
  END
  COMMENT = 'show engineering rows';

ALTER TABLE employees
ADD ROW ACCESS POLICY rap_engineering ON (department);

SELECT id, name, department FROM employees ORDER BY id;

┌────┬─────────┬─────────────┐
│ id │ name    │ department  │
├────┼─────────┼─────────────┤
│  1 │ Alice   │ Engineering │
│  3 │ Charlie │ Engineering │
└────┴─────────┴─────────────┘
```

The `ON (department)` clause maps the table column `department` to the policy argument `dept`.
