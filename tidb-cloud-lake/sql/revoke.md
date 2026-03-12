---
title: REVOKE
sidebar_position: 11
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.845"/>

Revokes privileges, roles, and ownership of a specific database object. This includes:

- Revoking privileges from roles.
- Removing roles from users or other roles.

See also:

- [GRANT](10-grant.md)
- [SHOW GRANTS](22-show-grants.md)

## Syntax

### Revoking Privileges

```sql
REVOKE { 
        schemaObjectPrivileges | ALL [ PRIVILEGES ] ON <privileges_level>
       }
FROM ROLE <role_name>
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

### Revoking Masking Policy Privileges

```sql
REVOKE APPLY ON MASKING POLICY <policy_name> FROM ROLE <role_name>
REVOKE ALL [ PRIVILEGES ] ON MASKING POLICY <policy_name> FROM ROLE <role_name>
REVOKE OWNERSHIP ON MASKING POLICY <policy_name> FROM ROLE '<role_name>'
```

Use these forms to remove access to individual masking policies. Global `CREATE MASKING POLICY` and `APPLY MASKING POLICY` privileges are revoked using the standard syntax with `ON *.*`.

### Revoking Row Access Policy Privileges

```sql
REVOKE APPLY ON ROW ACCESS POLICY <policy_name> FROM ROLE <role_name>
REVOKE ALL [ PRIVILEGES ] ON ROW ACCESS POLICY <policy_name> FROM ROLE <role_name>
REVOKE OWNERSHIP ON ROW ACCESS POLICY <policy_name> FROM ROLE '<role_name>'
```

Use these forms to revoke access to specific row access policies. Revoke global `CREATE ROW ACCESS POLICY` and `APPLY ROW ACCESS POLICY` privileges with the standard syntax against `ON *.*`.

### Revoking Role

```sql
-- Revoke a role from a user
REVOKE ROLE <role_name> FROM <user_name>

-- Revoke a role from a role
REVOKE ROLE <role_name> FROM ROLE <role_name>
```

## Examples

### Example 1: Revoking Privileges from a Role

Create a role:
```sql
CREATE ROLE user1_role;
```

Grant the `SELECT,INSERT` privilege on all existing tables in the `default` database to the role `user1_role`:
 
```sql
GRANT SELECT,INSERT ON default.* TO ROLE user1_role;
```
```sql
SHOW GRANTS FOR ROLE user1_role;
+---------------------------------------------------------+
| Grants                                                  |
+---------------------------------------------------------+
| GRANT SELECT,INSERT ON 'default'.* TO ROLE 'user1_role' |
+---------------------------------------------------------+
```

Revoke `INSERT` privilege from role `user1_role`:
```sql
REVOKE INSERT ON default.* FROM ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+---------------------------------------------------+
| Grants                                            |
+---------------------------------------------------+
| GRANT SELECT ON 'default'.* TO 'user1_role'       |
+---------------------------------------------------+
```

### Example 2: Revoking Privileges from Another Role

Grant the `SELECT,INSERT` privilege on all existing tables in the `mydb` database to the role `role1`:

Create role:
```sql
CREATE ROLE role1;
```

Grant privileges to the role:
```sql
GRANT SELECT,INSERT ON mydb.* TO ROLE role1;
```

Show the grants for the role:
```sql
SHOW GRANTS FOR ROLE role1;
+--------------------------------------------+
| Grants                                     |
+--------------------------------------------+
| GRANT SELECT,INSERT ON 'mydb'.* TO 'role1' |
+--------------------------------------------+
```

Revoke `INSERT` privilege from role `role1`:
```sql
REVOKE INSERT ON mydb.* FROM ROLE role1;
```

```sql
SHOW GRANTS FOR ROLE role1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT SELECT ON 'mydb'.* TO 'role1' |
+-------------------------------------+
```

### Example 3: Revoking a Role from a User

```sql
REVOKE ROLE role1 FROM USER user1;
```

```sql
SHOW GRANTS FOR user1;
```

### Example 4: Revoking Masking Policy Privileges

```sql
-- Remove per-policy access from a role
REVOKE APPLY ON MASKING POLICY email_mask FROM ROLE pii_readers;

-- Revoke the ability to create masking policies at the account level
REVOKE CREATE MASKING POLICY ON *.* FROM ROLE security_admin;
```

### Example 5: Revoking Row Access Policy Privileges

```sql
-- Remove per-policy access from a role
REVOKE APPLY ON ROW ACCESS POLICY rap_region FROM ROLE apac_only;

-- Revoke the ability to create row access policies globally
REVOKE CREATE ROW ACCESS POLICY ON *.* FROM ROLE row_policy_admin;
```
