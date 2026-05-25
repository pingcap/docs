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

## Masking Variant Sub-Fields

Use `object_delete` inside a masking policy to hide specific keys within a VARIANT column. All access paths (subscript, `json_path_query`, `get_path`, cast, `json_object_keys`) respect the mask—hidden keys return NULL or are absent from results.

### Step 1: Create a table with sample data

```sql
CREATE TABLE events (
  id INT,
  data VARIANT
);

INSERT INTO events VALUES
  (1, parse_json('{"name": "alice", "content": "secret data", "secret_key": "sk_123", "age": 30}')),
  (2, parse_json('{"name": "bob", "content": "private info", "secret_key": "sk_456", "age": 25}'));
```

### Step 2: Create roles

```sql
-- Role that sees full VARIANT data
CREATE ROLE data_admin;

-- Role that cannot see sensitive keys
CREATE ROLE data_reader;
```

### Step 3: Create the masking policy

```sql
-- Hide 'content' and 'secret_key' from users without data_admin role
CREATE MASKING POLICY mask_variant_sensitive
  AS (val VARIANT) RETURNS VARIANT ->
    CASE
      WHEN is_role_in_session('data_admin') OR is_role_in_session('account_admin') THEN val
      ELSE object_delete(val, 'content', 'secret_key')
    END;
```

> **Note:**
>
> `is_role_in_session` (available since v1.2.911) checks all roles granted to the user, regardless of which role is currently active. This is more secure than `current_role()` because users cannot bypass the mask by switching roles with `SET ROLE`.

### Step 4: Attach the policy to the VARIANT column

```sql
ALTER TABLE events MODIFY COLUMN data SET MASKING POLICY mask_variant_sensitive;
```

### Step 5: Grant access

```sql
GRANT SELECT ON default.events TO ROLE data_admin;
GRANT SELECT ON default.events TO ROLE data_reader;
GRANT ROLE data_admin TO USER 'admin_user';
GRANT ROLE data_reader TO USER 'normal_user';
```

### Step 6: Verify

```sql
-- As data_admin: full data visible
SET ROLE data_admin;
SELECT data FROM events;
-- {"age":30,"content":"secret data","name":"alice","secret_key":"sk_123"}
-- {"age":25,"content":"private info","name":"bob","secret_key":"sk_456"}

-- As data_reader: sensitive keys removed
SET ROLE data_reader;

SELECT data FROM events;
-- {"age":30,"name":"alice"}
-- {"age":25,"name":"bob"}

SELECT data['content'] FROM events;
-- NULL
-- NULL

SELECT data['name'] FROM events;
-- "alice"
-- "bob"

SELECT json_path_query_first(data, '$.content') FROM events;
-- NULL

SELECT data::STRING FROM events;
-- {"age":30,"name":"alice"}

SELECT json_object_keys(data) FROM events;
-- ["age","name"]

SELECT * FROM events WHERE data['content'] IS NOT NULL;
-- (empty result)
```

> **Tip:**
>
> For nested keys, use `delete_by_keypath`:
>
> ```sql
> ELSE delete_by_keypath(val, 'nested:secret')
> ```

## Privileges & References

- Grant `CREATE MASKING POLICY` on `*.*` to any role responsible for creating or replacing policies; the creator automatically owns the policy.
- Grant the global `APPLY MASKING POLICY` privilege or `APPLY ON MASKING POLICY <policy_name>` to roles that attach or detach policies via `ALTER TABLE`.
- Audit access with `SHOW GRANTS ON MASKING POLICY <policy_name>`.
- Additional references:
    - [User & Role](/tidb-cloud-lake/sql/user-role.md)
    - [CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md)
    - [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#column-operations)
    - [Masking Policy Commands](/tidb-cloud-lake/sql/masking-policy-sql.md)
