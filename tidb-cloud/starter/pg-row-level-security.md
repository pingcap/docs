---
title: PostgreSQL Row-Level Security
summary: Learn how to use row-level security policies on PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL Row-Level Security

PostgreSQL-compatible {{{ .starter }}} supports PostgreSQL-compatible Row-Level Security (RLS). RLS further restricts which rows a database role can view, insert, update, or delete, in addition to the role's table privileges.

RLS policies are evaluated by the database for each applicable query. This makes RLS useful for multi-tenant applications and other workloads that require row-specific access controls.

## Enable row-level security

Use `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`:

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;
```

When RLS is enabled and no applicable policy exists, access is denied by default for roles that do not bypass RLS.

To disable RLS:

```sql
ALTER TABLE todos DISABLE ROW LEVEL SECURITY;
```

## Force RLS for the table owner

By default, the table owner bypasses RLS policies.

Use `FORCE ROW LEVEL SECURITY` to make the table owner subject to the policies:

```sql
ALTER TABLE todos FORCE ROW LEVEL SECURITY;
```

To restore the default owner behavior:

```sql
ALTER TABLE todos NO FORCE ROW LEVEL SECURITY;
```

Roles with the `BYPASSRLS` attribute bypass RLS even when `FORCE ROW LEVEL SECURITY` is enabled.

## Create a policy

Use `CREATE POLICY` to define an RLS policy.

The general syntax is:

```sql
CREATE POLICY policy_name ON table_name
    [AS { PERMISSIVE | RESTRICTIVE }]
    [FOR { ALL | SELECT | INSERT | UPDATE | DELETE }]
    [TO role_name [, ...]]
    [USING (expression)]
    [WITH CHECK (expression)];
```

If `AS` is omitted, the policy is `PERMISSIVE`.

If `FOR` is omitted, the policy applies to all supported commands.

If `TO` is omitted, the policy applies to `PUBLIC`.

## `USING` and `WITH CHECK`

`USING` and `WITH CHECK` have different purposes:

| Clause | Purpose | Applies to |
| --- | --- | --- |
| `USING` | Determines which existing rows are visible or can be targeted. | `SELECT`, `UPDATE`, `DELETE` |
| `WITH CHECK` | Validates new or modified row values. | `INSERT`, `UPDATE` |

The clauses used for each operation are:

| Operation | `USING` | `WITH CHECK` |
| --- | --- | --- |
| `SELECT` | Used | Not used |
| `INSERT` | Not used | Used |
| `UPDATE` | Used | Used |
| `DELETE` | Used | Not used |

For an `UPDATE` policy, if `WITH CHECK` is omitted, the `USING` expression is also used to validate the updated row.

## Example: restrict rows by user

The following example allows each role to access only rows where `user_id` matches `current_user`.

Create a table:

```sql
CREATE TABLE todos (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    task TEXT NOT NULL,
    done BOOLEAN DEFAULT false
);
```

Enable RLS:

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;
```

Allow users to read their own rows:

```sql
CREATE POLICY user_select
ON todos
FOR SELECT
USING (user_id = current_user);
```

Allow users to insert rows for themselves:

```sql
CREATE POLICY user_insert
ON todos
FOR INSERT
WITH CHECK (user_id = current_user);
```

Allow users to update their own rows:

```sql
CREATE POLICY user_update
ON todos
FOR UPDATE
USING (user_id = current_user)
WITH CHECK (user_id = current_user);
```

Allow users to delete their own rows:

```sql
CREATE POLICY user_delete
ON todos
FOR DELETE
USING (user_id = current_user);
```

## Example: public and private rows

The following example allows roles that have SELECT privilege on the table to see published posts and authors to see their own unpublished posts.

Create the table and enable RLS:

```sql
CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    author TEXT,
    published BOOLEAN DEFAULT false,
    content TEXT
);

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

Create a policy for published posts:

```sql
CREATE POLICY see_published
ON posts
FOR SELECT
USING (published = true);
```

Create another policy for a user's own posts:

```sql
CREATE POLICY see_own
ON posts
FOR SELECT
USING (author = current_user);
```

Because both policies are permissive by default, a role with SELECT privilege can see a row if either applicable policy allows it.

## Permissive and restrictive policies

### Permissive policies

Multiple `PERMISSIVE` policies for the same command are combined with `OR`.

For example:

```text
permissive_policy_1 OR permissive_policy_2 OR ...
```

At least one applicable permissive policy must allow a row.

### Restrictive policies

Use `AS RESTRICTIVE` when every matching restrictive policy must pass:

```sql
CREATE POLICY must_be_published
ON posts
AS RESTRICTIVE
FOR SELECT
USING (published = true);
```

Restrictive policies are combined with `AND` and applied in addition to the permissive result:

```text
(permissive_policy_1 OR permissive_policy_2 OR ...)
AND restrictive_policy_1
AND restrictive_policy_2
AND ...
```

A restrictive policy does not grant access by itself. At least one applicable permissive policy must also allow the row.

## Apply policies to specific roles

Use `TO` to limit a policy to one or more roles.

For example:

```sql
CREATE POLICY support_read
ON tickets
FOR SELECT
TO support_agent
USING (status <> 'private');
```

A policy without an explicit `TO` clause applies to `PUBLIC`.

## Alter a policy

Use `ALTER POLICY` to change the roles or policy expressions:

```sql
ALTER POLICY see_own
ON posts
USING (author = current_user OR published = true);
```

## Drop a policy

Use `DROP POLICY`:

```sql
DROP POLICY see_own ON posts;
```

To avoid an error when the policy does not exist:

```sql
DROP POLICY IF EXISTS see_own ON posts;
```

## Bypass RLS

### `BYPASSRLS` role attribute

A role with `BYPASSRLS` bypasses RLS policies.

Create a login role with this attribute:

```sql
CREATE ROLE service_admin
LOGIN
PASSWORD 'SecurePass1'
BYPASSRLS;
```

Grant or revoke the attribute later:

```sql
ALTER ROLE service_admin BYPASSRLS;
ALTER ROLE service_admin NOBYPASSRLS;
```

Grant `BYPASSRLS` only to trusted administrative or service roles.

### Table owners

A table owner bypasses RLS by default. Use `FORCE ROW LEVEL SECURITY` if the owner should also be subject to policies.

### `SECURITY DEFINER` functions

A `SECURITY DEFINER` function executes with the privileges of its owner.

For example:

```sql
CREATE FUNCTION list_all_posts()
RETURNS SETOF posts
LANGUAGE SQL
SECURITY DEFINER
AS $$
    SELECT * FROM posts
$$;
```

If the function owner bypasses RLS, queries executed inside the function can also bypass RLS.

> **Warning:**
>
> Use `SECURITY DEFINER` functions carefully. Do not expose a function that can bypass RLS to untrusted roles unless the function strictly controls which operations and rows are accessible.

## Inspect RLS policies

Use `pg_policies` to list policies on a table:

```sql
SELECT
    policyname,
    cmd,
    permissive,
    roles,
    qual,
    with_check
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename = 'todos'
ORDER BY policyname;
```

Check whether RLS is enabled or forced:

```sql
SELECT
    relname,
    relrowsecurity,
    relforcerowsecurity
FROM pg_class
WHERE oid = 'public.todos'::regclass;
```

Check whether a role can bypass RLS:

```sql
SELECT
    rolname,
    rolbypassrls
FROM pg_roles
WHERE rolname = 'app_user';
```

## Security considerations

When using RLS:

- Use dedicated application roles instead of administrative roles for normal application traffic.
- Enable RLS before granting application roles access to protected tables.
- Create policies for every operation the application needs.
- Review both `USING` and `WITH CHECK` conditions for `UPDATE` policies.
- Grant `BYPASSRLS` only to trusted roles.
- Review `SECURITY DEFINER` functions carefully because they execute with the function owner's privileges.
- Test RLS behavior using the same role that the application uses.