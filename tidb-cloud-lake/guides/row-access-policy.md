---
title: Row Access Policy
summary: Row access policies protect data by filtering table rows at query time. They let you define centralized row-level predicates once, attach them to tables, and ensure users only see rows that satisfy the policy.
---

# Row Access Policy

Row access policies protect data by filtering table rows at query time. They let you define centralized row-level predicates once, attach them to tables, and ensure users only see rows that satisfy the policy.

> **Note:**
>
> Row access policy is currently experimental. Enable it with `SET enable_experimental_row_access_policy = 1` for the current session or `SET GLOBAL enable_experimental_row_access_policy = 1` for the account.

## How Row Access Works

Policies evaluate a Boolean expression for each row. Only rows where the expression returns `TRUE` are visible.

**Admin role sees all rows**

```sql
id | name    | department
---|---------|-------------
 1 | Alice   | Engineering
 2 | Bob     | Sales
 3 | Charlie | Engineering
```

**Other roles see policy-visible rows**

```sql
id | name    | department
---|---------|-------------
 1 | Alice   | Engineering
 3 | Charlie | Engineering
```

### Key Traits

- **Query-time** - rows are filtered during SELECT and DML planning; stored data never changes.
- **Role-aware** - expressions can reference `current_role()` or other context functions.
- **Table-scoped** - attach one row access policy to a table and map one or more table columns to policy arguments.
- **Reusable** - use the same policy across tables when the mapped columns have compatible types.

## End-to-End Workflow

### 1. Enable the feature

```sql
SET enable_experimental_row_access_policy = 1;
```

### 2. Create the target table

```sql
CREATE TABLE employees (
    id INT,
    name STRING,
    department STRING
);

INSERT INTO employees VALUES
    (1, 'Alice', 'Engineering'),
    (2, 'Bob', 'Sales'),
    (3, 'Charlie', 'Engineering');
```

### 3. Define the row access policy

```sql
CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN ->
CASE
  WHEN current_role() = 'admin' THEN true
  WHEN dept = 'Engineering' THEN true
  ELSE false
END;
```

### 4. Attach the policy

```sql
ALTER TABLE employees ADD ROW ACCESS POLICY rap_engineering ON (department);
```

The `ON (department)` clause maps the table column `department` to the policy argument `dept`.

### 5. Query the table

```sql
SELECT id, name, department FROM employees ORDER BY id;
```

**Result**

```sql
id | name    | department
---|---------|-------------
 1 | Alice   | Engineering
 3 | Charlie | Engineering
```

## Read and Write Behavior

Row access policies are enforced on reads and on DML target-row matching. `UPDATE`, `DELETE`, and `MERGE` only affect rows visible through the policy; invisible rows are not matched or modified.

`INSERT` is different: it writes rows normally. If an inserted row does not satisfy the policy, it is stored but hidden from policy-protected reads and DML.

### Complete DML Example

The example below uses a policy that exposes only `sales` rows. It temporarily detaches the policy after each operation only to inspect the stored data.

```sql
SET enable_experimental_row_access_policy = 1;

DROP TABLE IF EXISTS rap_dml_orders;
DROP TABLE IF EXISTS rap_dml_src;
DROP ROW ACCESS POLICY IF EXISTS rap_sales_only;

CREATE ROW ACCESS POLICY rap_sales_only
AS (dept STRING)
RETURNS BOOLEAN -> dept = 'sales';

CREATE TABLE rap_dml_orders(id INT, dept STRING, amount INT);
ALTER TABLE rap_dml_orders ADD ROW ACCESS POLICY rap_sales_only ON (dept);

-- INSERT is not affected: both visible and invisible rows are stored.
INSERT INTO rap_dml_orders VALUES
    (1, 'sales', 100),
    (2, 'eng',   200),
    (3, 'sales', 300);

-- SELECT is affected: only policy-visible rows are returned.
SELECT id, dept, amount FROM rap_dml_orders ORDER BY id;

id | dept  | amount
---|-------|-------
 1 | sales |    100
 3 | sales |    300

-- Detach only for inspection: the inserted 'eng' row exists.
ALTER TABLE rap_dml_orders DROP ROW ACCESS POLICY rap_sales_only;
SELECT id, dept, amount FROM rap_dml_orders ORDER BY id;

id | dept  | amount
---|-------|-------
 1 | sales |    100
 2 | eng   |    200
 3 | sales |    300

ALTER TABLE rap_dml_orders ADD ROW ACCESS POLICY rap_sales_only ON (dept);

-- UPDATE is affected: only visible target rows are updated.
UPDATE rap_dml_orders SET amount = amount + 10;

ALTER TABLE rap_dml_orders DROP ROW ACCESS POLICY rap_sales_only;
SELECT id, dept, amount FROM rap_dml_orders ORDER BY id;

id | dept  | amount
---|-------|-------
 1 | sales |    110
 2 | eng   |    200
 3 | sales |    310

ALTER TABLE rap_dml_orders ADD ROW ACCESS POLICY rap_sales_only ON (dept);

-- DELETE is affected: invisible target rows are not deleted.
DELETE FROM rap_dml_orders WHERE dept = 'eng';

ALTER TABLE rap_dml_orders DROP ROW ACCESS POLICY rap_sales_only;
SELECT id, dept, amount FROM rap_dml_orders ORDER BY id;

id | dept  | amount
---|-------|-------
 1 | sales |    110
 2 | eng   |    200
 3 | sales |    310

ALTER TABLE rap_dml_orders ADD ROW ACCESS POLICY rap_sales_only ON (dept);

-- DELETE still affects visible target rows.
DELETE FROM rap_dml_orders WHERE id = 1;

ALTER TABLE rap_dml_orders DROP ROW ACCESS POLICY rap_sales_only;
SELECT id, dept, amount FROM rap_dml_orders ORDER BY id;

id | dept  | amount
---|-------|-------
 2 | eng   |    200
 3 | sales |    310

CREATE TABLE rap_dml_src(id INT, new_amount INT);
INSERT INTO rap_dml_src VALUES (2, 777), (3, 888);

ALTER TABLE rap_dml_orders ADD ROW ACCESS POLICY rap_sales_only ON (dept);

-- MERGE is affected: invisible target rows are not matched or updated.
MERGE INTO rap_dml_orders AS t
USING rap_dml_src AS s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.amount = s.new_amount;

ALTER TABLE rap_dml_orders DROP ROW ACCESS POLICY rap_sales_only;
SELECT id, dept, amount FROM rap_dml_orders ORDER BY id;

id | dept  | amount
---|-------|-------
 2 | eng   |    200
 3 | sales |    888

DROP TABLE rap_dml_src;
DROP TABLE rap_dml_orders;
DROP ROW ACCESS POLICY rap_sales_only;
```

To inspect or modify all rows, use a role that satisfies the policy or detach the policy.

## Multiple Arguments

A policy can depend on multiple columns. The columns in `ON (...)` bind to policy arguments by position, not by name.

```sql
CREATE ROW ACCESS POLICY rap_region_dept
AS (region STRING, dept STRING)
RETURNS BOOLEAN ->
  region = 'APAC' AND dept = 'Engineering';

ALTER TABLE employees ADD ROW ACCESS POLICY rap_region_dept ON (office_region, department);
```

## Managing Policies

### DESCRIBE ROW ACCESS POLICY

View metadata, including creation time, signature, return type, body, and comment.

```sql
DESC ROW ACCESS POLICY rap_engineering;
```

### DROP ROW ACCESS POLICY

Remove a policy definition you no longer need. Detach it from every table first.

```sql
ALTER TABLE employees DROP ROW ACCESS POLICY rap_engineering;
DROP ROW ACCESS POLICY rap_engineering;
```

### Drop All Row Access Policies From a Table

```sql
ALTER TABLE employees DROP ALL ROW ACCESS POLICIES;
```

## Limits and Requirements

- A table can have at most one row access policy at a time.
- Row access policies can only be attached to regular tables. Views, streams, and temporary tables do not allow `ADD ROW ACCESS POLICY`.
- Each policy argument must map to one table column with a compatible data type.
- A column can belong to at most one security policy, either masking or row access.
- `INSERT` is not filtered by row access policies. Inserted rows are stored even when they do not satisfy the policy predicate.
- `SELECT` is filtered by row access policies and only returns policy-visible rows.
- `UPDATE`, `DELETE`, and `MERGE` are filtered by row access policies when matching target rows. Invisible target rows are not updated, deleted, or merged.
- Drop or detach the policy before altering or dropping protected columns.
- `CREATE OR REPLACE ROW ACCESS POLICY` and `ALTER ROW ACCESS POLICY` are not supported.

## Privileges & References

- Grant `CREATE ROW ACCESS POLICY` on `*.*` to roles responsible for creating policies; the creator automatically owns the policy.
- Grant `ALTER` on the target table plus the global `APPLY ROW ACCESS POLICY` privilege or `APPLY ON ROW ACCESS POLICY <policy_name>` to roles that attach or detach policies via `ALTER TABLE`.
- Audit access with `SHOW GRANTS ON ROW ACCESS POLICY <policy_name>`.
- Find policy usage with [`POLICY_REFERENCES`](/tidb-cloud-lake/sql/policy-references.md): `POLICY_REFERENCES(POLICY_NAME => '<policy_name>')`.
- Additional references:
    - [User & Role](/tidb-cloud-lake/sql/user-role.md)
    - [CREATE ROW ACCESS POLICY](/tidb-cloud-lake/sql/create-row-access-policy.md)
    - [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#row-access-policy-operations)
    - [Row Access Policy Commands](/tidb-cloud-lake/sql/row-access-policy-overview.md)
