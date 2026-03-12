---
title: GRANT
sidebar_position: 9
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.845"/>

Grants privileges, roles, and ownership for a specific database object. This includes:

- Granting privileges to roles.
- Assigning roles to users or other roles.
- Transferring ownership to a role.

See also:

- [REVOKE](11-revoke.md)
- [SHOW GRANTS](22-show-grants.md)

> After changing privileges or roles with `GRANT`, run [SYSTEM FLUSH PRIVILEGES](../../50-administration-cmds/flush-privileges.md) to broadcast the updates to every query node immediately.

## Syntax

### Granting Privileges

To understand what a privilege is and how it works, see [Privileges](/guides/security/access-control/privileges).

:::note Important
CREATE-like privileges that create ownership objects cannot be granted directly to a user. These privileges must be granted to a role first, and then the role can be assigned to users. This includes:
- CREATE
- CREATE DATABASE
- CREATE WAREHOUSE
- CREATE CONNECTION
- CREATE SEQUENCE
- CREATE PROCEDURE
- CREATE MASKING POLICY
- CREATE ROW ACCESS POLICY

Since `ALL` includes these CREATE privileges, `GRANT ALL ... TO USER` will also fail. For example, `GRANT ALL ON *.* TO USER u1` or `GRANT CREATE DATABASE ON *.* TO USER u1` will fail. Instead, use:
```sql
GRANT ALL ON *.* TO ROLE r1;
GRANT ROLE r1 TO USER u1;
```
:::

```sql
GRANT { 
        schemaObjectPrivileges | ALL [ PRIVILEGES ] ON <privileges_level>
      }
TO ROLE <role_name>
```

Where:

```sql
schemaObjectPrivileges ::=
-- For TABLE
  { SELECT | INSERT }
  
-- For SCHEMA
  { CREATE | DROP | ALTER }
  
-- For USER
  { CREATE USER }
  
-- For ROLE
  { CREATE ROLE}
  
-- For STAGE
  { READ, WRITE }
           
-- For UDF
  { USAGE }

-- For MASKING POLICY (account-level privileges)
  { CREATE MASKING POLICY | APPLY MASKING POLICY }

-- For ROW ACCESS POLICY (account-level privileges)
  { CREATE ROW ACCESS POLICY | APPLY ROW ACCESS POLICY }
```

```sql
privileges_level ::=
    *.*
  | db_name.*
  | db_name.tbl_name
  | STAGE <stage_name>
  | UDF <udf_name>
  | MASKING POLICY <policy_name>
  | ROW ACCESS POLICY <policy_name>
```

### Granting Masking Policy Privileges

Use the following forms to manage access to individual masking policies:

```sql
GRANT APPLY ON MASKING POLICY <policy_name> TO ROLE <role_name>
GRANT ALL [ PRIVILEGES ] ON MASKING POLICY <policy_name> TO ROLE <role_name>
GRANT OWNERSHIP ON MASKING POLICY <policy_name> TO ROLE '<role_name>'
```

- `CREATE MASKING POLICY` allows a role to create new masking policies.
- `APPLY MASKING POLICY` lets grantees attach, detach, describe, or drop any masking policy when combined with the appropriate `ALTER TABLE` or policy commands.
- `GRANT APPLY ON MASKING POLICY ...` authorizes the grantee to manage a specific masking policy without granting global access.
- OWNERSHIP provides full control over the masking policy; Databend automatically grants OWNERSHIP on a new policy to the creator role and revokes it when the policy is dropped.

### Granting Row Access Policy Privileges

Use these forms to manage access to individual row access policies:

```sql
GRANT APPLY ON ROW ACCESS POLICY <policy_name> TO ROLE <role_name>
GRANT ALL [ PRIVILEGES ] ON ROW ACCESS POLICY <policy_name> TO ROLE <role_name>
GRANT OWNERSHIP ON ROW ACCESS POLICY <policy_name> TO ROLE '<role_name>'
```

- `CREATE ROW ACCESS POLICY` allows a role to create new row access policies.
- `APPLY ROW ACCESS POLICY` authorizes attaching or detaching any row access policy from tables, along with DESCRIBE/DROP commands.
- `GRANT APPLY ON ROW ACCESS POLICY ...` limits access to a specific row access policy.
- OWNERSHIP delivers full control over the row access policy; the creator role receives OWNERSHIP automatically and loses it when the policy is dropped.

### Granting Role

To understand what a role is and how it works, see [Roles](/guides/security/access-control/roles).

```sql
-- Grant a role to a user
GRANT ROLE <role_name> TO <user_name>

-- Grant a role to a role
GRANT ROLE <role_name> TO ROLE <role_name>
```

### Granting Ownership

To understand what ownership is and how it works, see [Ownership](/guides/security/access-control/ownership).

```sql
-- Grant ownership of a specific table within a database to a role
GRANT OWNERSHIP ON <database_name>.<table_name> TO ROLE '<role_name>'

-- Grant ownership of a stage to a role
GRANT OWNERSHIP ON STAGE <stage_name> TO ROLE '<role_name>'

-- Grant ownership of a user-defined function (UDF) to a role
GRANT OWNERSHIP ON UDF <udf_name> TO ROLE '<role_name>'
```

## Examples

### Example 1: Granting Privileges to a Role

Create a role:
```sql
CREATE ROLE user1_role;
```

Grant the `ALL` privilege on all existing tables in the `default` database to the role `user1_role`:
 
```sql
GRANT ALL ON default.* TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON 'default'.* TO ROLE 'user1_role'    |
+--------------------------------------------------+
```

Grant the `ALL` privilege on all databases to the role `user1_role`:

```sql
GRANT ALL ON *.* TO ROLE user1_role;
```
```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON 'default'.* TO ROLE 'user1_role'    |
| GRANT ALL ON *.* TO ROLE 'user1_role'            |
+--------------------------------------------------+
```

Grant the `ALL` privilege on the stage named `s1` to the role `user1_role`:

```sql
GRANT ALL ON STAGE s1 TO ROLE user1_role;
```
```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON STAGE s1 TO ROLE 'user1_role'       |
+--------------------------------------------------+
```

Grant the `ALL` privilege on the UDF named `f1` to the role `user1_role`:

```sql
GRANT ALL ON UDF f1 TO ROLE user1_role;
```
```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON UDF f1 TO ROLE 'user1_role'         |
+--------------------------------------------------+
```

### Example 2: Granting Specific Privileges to a Role

Grant the `SELECT` privilege on all existing tables in the `mydb` database to the role `role1`:

Create role:
```sql 
CREATE ROLE role1;
```

Grant privileges to the role:
```sql
GRANT SELECT ON mydb.* TO ROLE role1;
```

Show the grants for the role:
```sql
SHOW GRANTS FOR ROLE role1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT SELECT ON 'mydb'.* TO 'role1' |
+-------------------------------------+
```

### Example 3: Granting a Role to a User

Create a user:
```sql
CREATE USER user1 IDENTIFIED BY 'abc123' WITH DEFAULT_ROLE = 'role1';
```

Role `role1` grants are:
```sql
SHOW GRANTS FOR ROLE role1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT SELECT ON 'mydb'.* TO 'role1' |
+-------------------------------------+
```

Grant role `role1` to user `user1`:
```sql
 GRANT ROLE role1 TO user1;
```

Now, user `user1` grants are:
```sql
SHOW GRANTS FOR user1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT ROLE role1 TO 'user1'@'%'     |
+-------------------------------------+
```

### Example 4: Granting Ownership to a Role

```sql
-- Grant ownership of all tables in the 'finance_data' database to the role 'data_owner'
GRANT OWNERSHIP ON finance_data.* TO ROLE 'data_owner';

-- Grant ownership of the table 'transactions' in the 'finance_data' schema to the role 'data_owner'
GRANT OWNERSHIP ON finance_data.transactions TO ROLE 'data_owner';

-- Grant ownership of the stage 'ingestion_stage' to the role 'data_owner'
GRANT OWNERSHIP ON STAGE ingestion_stage TO ROLE 'data_owner';

-- Grant ownership of the user-defined function 'calculate_profit' to the role 'data_owner'
GRANT OWNERSHIP ON UDF calculate_profit TO ROLE 'data_owner';
```

### Example 5: Granting Masking Policy Privileges

```sql
-- Allow the current user to create masking policies
GRANT CREATE MASKING POLICY ON *.* TO ROLE security_admin;

-- Create a masking policy while assuming the security_admin role
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING -> '***';

-- Grant a role the ability to apply the policy when altering tables
GRANT APPLY ON MASKING POLICY email_mask TO ROLE pii_readers;

-- Review the masking policy privileges
SHOW GRANTS ON MASKING POLICY email_mask;
```

### Example 6: Granting Row Access Policy Privileges

```sql
-- Allow the current role to create row access policies
GRANT CREATE ROW ACCESS POLICY ON *.* TO ROLE row_policy_admin;

-- Define a row access policy while assuming the row_policy_admin role
CREATE ROW ACCESS POLICY rap_region AS (region STRING) RETURNS BOOLEAN -> region = 'APAC';

-- Allow a role to apply the policy when altering tables
GRANT APPLY ON ROW ACCESS POLICY rap_region TO ROLE apac_only;

-- Review the row access policy privileges
SHOW GRANTS ON ROW ACCESS POLICY rap_region;
```
