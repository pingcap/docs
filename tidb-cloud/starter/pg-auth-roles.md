---
title: PostgreSQL Authentication and Roles
summary: Learn how to manage PostgreSQL-compatible database roles and privileges on PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL Authentication and Roles

PostgreSQL-compatible {{{ .starter }}} supports PostgreSQL-compatible database roles, role attributes, object privileges, and session role switching.

This page describes database-level authentication and authorization. TiDB Cloud organization, project, and instance access is managed separately through TiDB Cloud Identity and Access Management.


## Create a role

Use `CREATE ROLE ... LOGIN` to create a role that can connect to the database.

{{< copyable "sql" >}}

```sql
CREATE ROLE app_user
LOGIN
PASSWORD 'SecurePass1';
```

A role without `LOGIN` can be used as a group role for privilege management:

{{< copyable "sql" >}}

```sql
CREATE ROLE readonly;
```

Grant the group role to a login role:

{{< copyable "sql" >}}

```sql
GRANT readonly TO app_user;
```

## Alter a role

Change a role password:

{{< copyable "sql" >}}

```sql
ALTER ROLE app_user
PASSWORD 'NewSecurePass1';
```

Grant or revoke selected role attributes:

{{< copyable "sql" >}}

```sql
ALTER ROLE app_user CREATEDB;
ALTER ROLE app_user NOCREATEDB;

ALTER ROLE app_user BYPASSRLS;
ALTER ROLE app_user NOBYPASSRLS;
```

The following common role attributes are supported:

| Attribute | Description |
| --- | --- |
| `LOGIN` / `NOLOGIN` | Controls whether the role can connect. |
| `CREATEDB` / `NOCREATEDB` | Controls whether the role can create databases. |
| `BYPASSRLS` / `NOBYPASSRLS` | Controls whether the role bypasses row-level security policies. |

Grant `BYPASSRLS` only to trusted administrative or service roles.


## Grant table privileges

Grant one or more privileges on a table:

{{< copyable "sql" >}}

```sql
GRANT SELECT, INSERT
ON todos
TO app_user;
```

Grant all supported table privileges:

{{< copyable "sql" >}}

```sql
GRANT ALL
ON todos
TO app_user;
```

Grant privileges on all tables in a schema:

{{< copyable "sql" >}}

```sql
GRANT SELECT
ON ALL TABLES IN SCHEMA public
TO readonly;
```

## Revoke table privileges

Revoke privileges previously granted to a role:

{{< copyable "sql" >}}

```sql
REVOKE INSERT
ON todos
FROM app_user;
```

Revoke all privileges on a table:

{{< copyable "sql" >}}

```sql
REVOKE ALL
ON todos
FROM app_user;
```

## Grant schema privileges

Use `USAGE` to let a role access objects in a schema:

{{< copyable "sql" >}}

```sql
GRANT USAGE
ON SCHEMA analytics
TO app_user;
```

Grant permission to create objects in a schema:

{{< copyable "sql" >}}

```sql
GRANT CREATE
ON SCHEMA analytics
TO app_user;
```

Granting `USAGE` on a schema does not automatically grant privileges on tables in that schema. Grant the required table privileges separately.

For example:

{{< copyable "sql" >}}

```sql
GRANT USAGE
ON SCHEMA analytics
TO app_user;

GRANT SELECT
ON ALL TABLES IN SCHEMA analytics
TO app_user;
```

## Grant sequence privileges

Sequence privileges are enforced.

For example:

{{< copyable "sql" >}}

```sql
GRANT USAGE, SELECT
ON SEQUENCE order_seq
TO app_user;
```

The following sequence privileges are relevant:

| Privilege | Purpose |
| --- | --- |
| `USAGE` | Allows common sequence operations such as `nextval()`. |
| `SELECT` | Allows reading the current sequence value where applicable. |
| `UPDATE` | Required for operations that change the sequence value, such as `setval()`. |

For example, grant permission to reposition a sequence:

{{< copyable "sql" >}}

```sql
GRANT UPDATE
ON SEQUENCE order_seq
TO app_user;
```

> **Note:**
>
> `SERIAL` and `BIGSERIAL` defaults do not require a separate sequence grant when the role inserts into the table using the default value. Direct calls to sequence functions still require the corresponding sequence privileges.

## Grant privileges on future objects

Use `ALTER DEFAULT PRIVILEGES` to configure privileges for subsequently created objects.

For example, grant `SELECT` on future tables:

{{< copyable "sql" >}}

```sql
ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT SELECT ON TABLES TO readonly;
```

For explicitly created sequences:

{{< copyable "sql" >}}

```sql
ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO app_user;
```

Default privileges on sequences apply to sequences created explicitly with `CREATE SEQUENCE`. Sequences created implicitly by `SERIAL` or `BIGSERIAL` do not inherit these sequence default privileges.

`ALTER DEFAULT PRIVILEGES ... ON FUNCTIONS` is not supported.

## Manage role membership

Grant one role to another role:

{{< copyable "sql" >}}

```sql
GRANT readonly TO app_user;
```

Revoke membership:

{{< copyable "sql" >}}

```sql
REVOKE readonly FROM app_user;
```

## Switch roles in a session

Use `SET ROLE` to switch to a role that has been granted to the current session user:

{{< copyable "sql" >}}

```sql
SET ROLE app_user;
```

Return to the original authenticated role:

{{< copyable "sql" >}}

```sql
RESET ROLE;
```

Role switching is enforced. You cannot `SET ROLE` to a role that has not been granted to the current user.

Check the current and session roles:

{{< copyable "sql" >}}

```sql
SELECT CURRENT_USER, SESSION_USER;
```

## Inspect roles and privileges

List database roles:

{{< copyable "sql" >}}

```sql
SELECT
    rolname,
    rolcanlogin,
    rolcreatedb,
    rolbypassrls
FROM pg_roles
ORDER BY rolname;
```

List role memberships:

{{< copyable "sql" >}}

```sql
SELECT
    member_role.rolname AS member,
    granted_role.rolname AS granted_role
FROM pg_auth_members AS m
JOIN pg_roles AS member_role
    ON member_role.oid = m.member
JOIN pg_roles AS granted_role
    ON granted_role.oid = m.roleid
ORDER BY member_role.rolname, granted_role.rolname;
```

List table privileges:

{{< copyable "sql" >}}

```sql
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public'
ORDER BY table_name, grantee, privilege_type;
```

## Drop a role

Before dropping a role, revoke privileges and role memberships that depend on it.

For example:

{{< copyable "sql" >}}

```sql
REVOKE SELECT ON todos FROM app_user;
REVOKE USAGE ON SCHEMA public FROM app_user;
```

Then drop the role:

{{< copyable "sql" >}}

```sql
DROP ROLE app_user;
```

## Row-level security

Database roles can be referenced by row-level security policies.

For example:

{{< copyable "sql" >}}

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

CREATE POLICY app_user_todos
ON todos
FOR SELECT
TO app_user
USING (user_id = current_user);
```

For complete RLS syntax and behavior, see [PostgreSQL Row-Level Security](/tidb-cloud/starter/pg-row-level-security.md).