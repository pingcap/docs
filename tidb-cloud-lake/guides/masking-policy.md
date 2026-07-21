---
title: Masking Policy
summary: Masking policies protect sensitive data by dynamically transforming column values during query execution. They enable role-based access to confidential information—authorized users see actual data, while others see masked values.
---

# Masking Policy

Masking policies transform column values at query time. Authorized roles see real data; others see redacted values. Stored data never changes.

To hide entire rows instead of redacting columns, use a [Row Access Policy](/tidb-cloud-lake/guides/row-access-policy.md).

## When to Use

- Customer support — agents see orders, IDs show as `3201**********1234`
- Analytics — email shows as `***@***.com` without breaking aggregates
- VARIANT logs — hide JSON keys like `secret_key` / `token` from non-admins
- Partial redaction — show last 4 digits of a card for verification

## Quick Start

```sql
CREATE TABLE user_info (id INT, email STRING NOT NULL);

CREATE MASKING POLICY email_mask
AS (val STRING)
RETURNS STRING ->
CASE
  WHEN is_role_in_session('managers') THEN val
  ELSE '*********'
END;

ALTER TABLE user_info MODIFY COLUMN email SET MASKING POLICY email_mask;

INSERT INTO user_info VALUES (1, 'user@example.com');
SELECT * FROM user_info;
```

```
id | email
---|----------
 1 | *********
```

**How it works**

- Query-time only — `SELECT` is masked; `INSERT` / `UPDATE` / `DELETE` use true values
- Column-scoped — one policy per column; reusable across tables
- Prefer `is_role_in_session()` over `current_role()` so users cannot bypass with `SET ROLE`

## Examples

### Conditional masking (`USING`)

Mask based on another column:

```sql
CREATE MASKING POLICY vip_mask
AS (val STRING, is_vip BOOLEAN)
RETURNS STRING ->
CASE
  WHEN is_vip = true THEN val
  ELSE '*********'
END;

ALTER TABLE user_info
MODIFY COLUMN email SET MASKING POLICY vip_mask USING (email, is_vip);

INSERT INTO user_info (id, email, is_vip) VALUES
  (1, 'vip@example.com', true),
  (2, 'normal@example.com', false);

SELECT * FROM user_info;
```

```
id | email           | is_vip
---|-----------------|-------
 1 | vip@example.com | true
 2 | *********       | false
```

Only add columns to `USING` when the policy body needs them.

### VARIANT sub-field masking

Hide specific JSON keys with `object_delete`. All access paths honor the mask (subscript, path functions, cast, `json_object_keys`).

```sql
CREATE TABLE events (id INT, data VARIANT);

INSERT INTO events VALUES
  (1, parse_json('{"name":"alice","content":"secret data","secret_key":"sk_123","age":30}')),
  (2, parse_json('{"name":"bob","content":"private info","secret_key":"sk_456","age":25}'));

CREATE ROLE data_admin;
CREATE ROLE data_reader;

CREATE MASKING POLICY mask_variant_sensitive
AS (val VARIANT) RETURNS VARIANT ->
CASE
  WHEN is_role_in_session('data_admin') OR is_role_in_session('account_admin') THEN val
  ELSE object_delete(val, 'content', 'secret_key')
END;

ALTER TABLE events MODIFY COLUMN data SET MASKING POLICY mask_variant_sensitive;

GRANT SELECT ON default.events TO ROLE data_admin;
GRANT SELECT ON default.events TO ROLE data_reader;
```

| As `data_admin` | As `data_reader` |
|-----------------|------------------|
| full JSON | `content` / `secret_key` removed |

```sql
SET ROLE data_reader;

SELECT data FROM events;
-- {"age":30,"name":"alice"}

SELECT data['content'] FROM events;                 -- NULL
SELECT data['name'] FROM events;                    -- "alice"
SELECT json_path_query_first(data, '$.content');    -- NULL
SELECT data::STRING FROM events;                    -- {"age":30,"name":"alice"}
SELECT json_object_keys(data) FROM events;          -- ["age","name"]
SELECT * FROM events WHERE data['content'] IS NOT NULL;
-- empty
```

Nested keys:

```sql
ELSE delete_by_keypath(val, 'nested:secret')
```

## Read / Write Behavior

| Operation | Effect |
|-----------|--------|
| `SELECT` | Masked values |
| `INSERT` / `UPDATE` / `DELETE` | True values (writes are not masked) |

```sql
INSERT INTO user_info VALUES (2, 'admin@example.com');  -- stores real email
SELECT * FROM user_info WHERE id = 2;                   -- returns *********
```

## Manage Policies

```sql
DESCRIBE MASKING POLICY email_mask;

ALTER TABLE user_info MODIFY COLUMN email UNSET MASKING POLICY;
DROP MASKING POLICY IF EXISTS email_mask;
```

Unbind every column before `DROP MASKING POLICY`. Find bindings with `POLICY_REFERENCES(POLICY_NAME => 'email_mask')`.

## Masking vs Row Access

| | Masking Policy | Row Access Policy |
|---|---|---|
| Scope | Column values | Entire rows |
| Return type | Must match column type | Always BOOLEAN |
| Per table | One per column | One per table |
| Affects | `SELECT` | `SELECT`, `UPDATE`, `DELETE`, `MERGE` |

A column cannot have both policies at once. Mask when the row should stay visible; use row access when the row should disappear.

## Limits

- One masking policy per column
- Return type must match the column type
- Unset policy before altering or dropping the column
- Cannot drop a policy still referenced by any table
- No `CREATE OR REPLACE MASKING POLICY` — drop and recreate
- Not supported on temporary tables, views, or streams
- Policy names are globally unique across masking and row access policies
- Policy argument names are lowercased at create time

## Best Practices

1. Prefer `is_role_in_session()` over `current_role()`.
2. Keep `USING` minimal — only columns the body needs.
3. Return type-consistent placeholders (`***@***.com` for emails) if apps call `LENGTH` / `LIKE`.
4. For VARIANT, use `object_delete` / `delete_by_keypath` instead of masking the whole value.
5. Unbind before drop; verify with a restricted role after attach.

## Privileges & References

- `CREATE MASKING POLICY` on `*.*` to create policies (creator gets OWNERSHIP)
- Global `APPLY MASKING POLICY` or `APPLY ON MASKING POLICY <name>` to attach/detach
- Audit: `SHOW GRANTS ON MASKING POLICY <name>`

Also see:

- [User & Role](/tidb-cloud-lake/sql/user-role.md)
- [CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md)
- [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#column-operations)
- [Masking Policy Commands](/tidb-cloud-lake/sql/masking-policy-sql.md)
- [Row Access Policy](/tidb-cloud-lake/guides/row-access-policy.md)
