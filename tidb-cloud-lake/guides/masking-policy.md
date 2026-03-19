---
title: Masking Policy
summary: Masking policies protect sensitive data by dynamically transforming column values during query execution. They enable role-based access to confidential information—authorized users see actual data, while others see masked values.
---

# Masking Policy

Masking policies protect sensitive data by dynamically transforming column values during query execution. They enable role-based access to confidential information—authorized users see actual data, while others see masked values.

## How Masking Works

Policies transform column data at query time, usually based on the caller’s role.

**Managers see actual values**
```sql
id | email           |
---|-----------------|
 2 | eric@example.com|
 1 | sue@example.com |
```

**Other roles see masked values**
```sql
id | email    |
---|----------|
 2 | *********|
 1 | *********|
```

### Key Traits

- **Query-time** – transformations only occur during SELECTs.
- **Role-aware** – expressions can reference `current_role()` or any condition.
- **Column-scoped** – attach a policy per column; reuse across tables.
- **Non-destructive** – stored data never changes.

## End-to-End Workflow

Follow this streamlined sequence to introduce masking on a column.

### 1. Create the target table

```sql
CREATE TABLE user_info (id INT, email STRING NOT NULL);
```

### 2. Define the masking policy

```sql
CREATE MASKING POLICY email_mask
AS (val STRING)
RETURNS STRING ->
CASE
  WHEN current_role() IN ('MANAGERS') THEN val
  ELSE '*********'
END;
```

### 3. Attach the policy

```sql
ALTER TABLE user_info MODIFY COLUMN email SET MASKING POLICY email_mask;
```

### 4. Insert and query data

```sql
INSERT INTO user_info VALUES (1, 'user@example.com');
SELECT * FROM user_info;
```

**Result**

```sql
id | email
---|----------
 1 | *********
```

## Read vs Write Behavior

Masking policies affect read paths only. Write statements always handle true values so applications can store and modify accurate data.

```sql
-- Write original data
INSERT INTO user_info VALUES (2, 'admin@example.com');

-- Read masked data
SELECT * FROM user_info WHERE id = 2;
```

**Result**

```sql
id | email
---|----------
 2 | *********
```

## Managing Policies

### DESCRIBE MASKING POLICY

View metadata, including creation time, signature, and definition.

```sql
DESCRIBE MASKING POLICY email_mask;
```

**Result**

```sql
Name       | Created On                  | Signature    | Return Type | Body                                                     | Comment
-----------+-----------------------------+--------------+-------------+----------------------------------------------------------+---------
email_mask | 2025-11-19 09:49:10.949 UTC | (val STRING) | STRING      | CASE WHEN current_role() IN('MANAGERS') THEN val ELSE... |
```

### DROP MASKING POLICY

Remove a policy definition you no longer need.

```sql
DROP MASKING POLICY [IF EXISTS] email_mask;
```

### Detach from a column

```sql
ALTER TABLE user_info MODIFY COLUMN email UNSET MASKING POLICY;
```

## Conditional Masking

Use the `USING` clause to reference additional columns when the masking logic depends on other values.

```sql
CREATE MASKING POLICY vip_mask
AS (val STRING, is_vip BOOLEAN)
RETURNS STRING ->
CASE
  WHEN is_vip = true THEN val
  ELSE '*********'
END;

ALTER TABLE user_info MODIFY COLUMN email SET MASKING POLICY vip_mask USING (email, is_vip);
INSERT INTO user_info (id, email, is_vip)
VALUES (1, 'vip@example.com', true), (2, 'normal@example.com', false);
SELECT * FROM user_info;
```

**Result**

```sql
id | email              | is_vip
---|--------------------|-------
 1 | vip@example.com    | true
 2 | *********          | false
```

## Privileges & References

- Grant `CREATE MASKING POLICY` on `*.*` to any role responsible for creating or replacing policies; the creator automatically owns the policy.
- Grant the global `APPLY MASKING POLICY` privilege or `APPLY ON MASKING POLICY <policy_name>` to roles that attach or detach policies via `ALTER TABLE`.
- Audit access with `SHOW GRANTS ON MASKING POLICY <policy_name>`.
- Additional references:
  - [User & Role](/tidb-cloud-lake/sql/user-role.md)
  - [CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md)
  - [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#column-operations)
  - [Masking Policy Commands](/tidb-cloud-lake/sql/masking-policy-sql.md)
