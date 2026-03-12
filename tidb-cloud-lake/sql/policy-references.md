---
title: POLICY_REFERENCES
---

Returns the associations between security policies (Masking Policy or Row Access Policy) and tables/views. You can query by policy name to find all tables using it, or by table name to find all policies applied to it.

See also:

- [MASKING POLICY](/guides/security/masking-policy)

## Syntax

```sql
-- Find all tables/views using a specific policy
POLICY_REFERENCES(POLICY_NAME => '<policy_name>')

-- Find all policies applied to a specific table/view
POLICY_REFERENCES(
    REF_ENTITY_NAME => '[<database>.]<table_name>',
    REF_ENTITY_DOMAIN => 'TABLE' | 'VIEW'
)
```

## Output Columns

| Column               | Description                                                        |
|----------------------|--------------------------------------------------------------------|
| policy_name          | Name of the policy                                                 |
| policy_kind          | Type of policy: `MASKING POLICY` or `ROW ACCESS POLICY`            |
| ref_database_name    | Database containing the referenced table/view                      |
| ref_entity_name      | Name of the referenced table or view                               |
| ref_entity_domain    | `TABLE` or `VIEW`                                                  |
| ref_column_name      | Column the policy is applied to (for masking policies)             |
| ref_arg_column_names | Argument columns used by the policy                                |
| policy_status        | Policy status, typically `ACTIVE`                                  |

## Examples

### Find Tables Using a Row Access Policy

```sql
-- Create a row access policy
CREATE ROW ACCESS POLICY rap_employees AS (department STRING) RETURNS BOOLEAN ->
  CASE
    WHEN current_role() = 'admin' THEN true
    WHEN department = 'Engineering' THEN true
    ELSE false
  END;

-- Apply the policy to a table
CREATE TABLE employees(id INT, name STRING, department STRING);
ALTER TABLE employees ADD ROW ACCESS POLICY rap_employees ON (department);

-- Find all tables using this policy
SELECT * FROM policy_references(POLICY_NAME => 'rap_employees');

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   policy_name   │    policy_kind    │ ref_database_name │ ref_entity_name │ ref_entity_domain │ ref_column_name │ ref_arg_column_names │ policy_status │
├─────────────────┼───────────────────┼───────────────────┼─────────────────┼───────────────────┼─────────────────┼──────────────────────┼───────────────┤
│ rap_employees   │ ROW ACCESS POLICY │ default           │ employees       │ TABLE             │ NULL            │ department           │ ACTIVE        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Find All Policies Applied to a Table

```sql
-- Create a masking policy
CREATE MASKING POLICY mask_salary AS (val INT) RETURNS INT ->
  CASE WHEN current_role() = 'admin' THEN val ELSE 0 END;

-- Apply both policies to the table
ALTER TABLE employees ADD COLUMN salary INT;
ALTER TABLE employees MODIFY COLUMN salary SET MASKING POLICY mask_salary;

-- Find all policies on this table
SELECT * FROM policy_references(
    REF_ENTITY_NAME => 'default.employees',
    REF_ENTITY_DOMAIN => 'TABLE'
);

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   policy_name   │    policy_kind    │ ref_database_name │ ref_entity_name │ ref_entity_domain │ ref_column_name │ ref_arg_column_names │ policy_status │
├─────────────────┼───────────────────┼───────────────────┼─────────────────┼───────────────────┼─────────────────┼──────────────────────┼───────────────┤
│ mask_salary     │ MASKING POLICY    │ default           │ employees       │ TABLE             │ salary          │ NULL                 │ ACTIVE        │
│ rap_employees   │ ROW ACCESS POLICY │ default           │ employees       │ TABLE             │ NULL            │ department           │ ACTIVE        │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Find Tables Using a Masking Policy with Multiple Arguments

```sql
-- Create a masking policy with conditional arguments
CREATE MASKING POLICY mask_ssn AS (val STRING, user_role STRING) RETURNS STRING ->
  CASE
    WHEN user_role = current_role() THEN val
    ELSE '***-**-****'
  END;

-- Apply to multiple tables
CREATE TABLE employees1(id INT, ssn STRING, role STRING);
CREATE TABLE employees2(id INT, ssn STRING, role STRING);

ALTER TABLE employees1 MODIFY COLUMN ssn SET MASKING POLICY mask_ssn USING (ssn, role);
ALTER TABLE employees2 MODIFY COLUMN ssn SET MASKING POLICY mask_ssn USING (ssn, role);

-- Find all tables using this policy
SELECT * FROM policy_references(POLICY_NAME => 'mask_ssn') ORDER BY ref_entity_name;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ policy_name │   policy_kind  │ ref_database_name │ ref_entity_name │ ref_entity_domain │ ref_column_name │ ref_arg_column_names │ policy_status │
├─────────────┼────────────────┼───────────────────┼─────────────────┼───────────────────┼─────────────────┼──────────────────────┼───────────────┤
│ mask_ssn    │ MASKING POLICY │ default           │ employees1      │ TABLE             │ ssn             │ role                 │ ACTIVE        │
│ mask_ssn    │ MASKING POLICY │ default           │ employees2      │ TABLE             │ ssn             │ role                 │ ACTIVE        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
