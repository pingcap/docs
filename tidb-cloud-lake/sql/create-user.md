---
title: CREATE USER
sidebar_position: 1
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.703"/>

Creates a SQL user for connecting to Databend. Users must be granted appropriate privileges to access databases and perform operations.

See also:
- [GRANT](10-grant.md)
- [ALTER USER](03-user-alter-user.md)
- [DROP USER](02-user-drop-user.md)

## Syntax

```sql
CREATE [ OR REPLACE ] USER <name> IDENTIFIED [ WITH <auth_type> ] BY '<password>' 
[ WITH MUST_CHANGE_PASSWORD = true | false ]
[ WITH SET PASSWORD POLICY = '<policy_name>' ]
[ WITH SET NETWORK POLICY = '<policy_name>' ]
[ WITH DEFAULT_ROLE = '<role_name>' ]
[ WITH DISABLED = true | false ]
```

**Parameters:**
- `<name>`: Username (cannot contain single quotes, double quotes, backspace, or form feed characters)
- `<auth_type>`: Authentication type - `double_sha1_password` (default), `sha256_password`, or `no_password`
- `MUST_CHANGE_PASSWORD`: When `true`, user must change password at first login
- `DEFAULT_ROLE`: Sets default role (role must be explicitly granted to take effect)
- `DISABLED`: When `true`, user is created in disabled state and cannot log in

## Examples

### Example 1: Create User and Grant Database Privileges

Create a role, grant database privileges, and assign the role to a user:

```sql
-- Create a role and grant database privileges
CREATE ROLE data_analyst_role;
GRANT SELECT, INSERT ON default.* TO ROLE data_analyst_role;

-- Create a new user and assign the role
CREATE USER data_analyst IDENTIFIED BY 'secure_password123' WITH DEFAULT_ROLE = 'data_analyst_role';
GRANT ROLE data_analyst_role TO data_analyst;
```

Verify the role and permissions:
```sql
SHOW GRANTS FOR ROLE data_analyst_role;
+-----------------------------------------------------------------+
| Grants                                                          |
+-----------------------------------------------------------------+
| GRANT SELECT,INSERT ON 'default'.* TO ROLE  'data_analyst_role' |
+-----------------------------------------------------------------+
```

### Example 2: Create User and Grant Role

Create a user and assign a role with specific privileges:

```sql
-- Create a role with specific privileges
CREATE ROLE analyst_role;
GRANT SELECT ON *.* TO ROLE analyst_role;
GRANT INSERT ON default.* TO ROLE analyst_role;

-- Create user and grant the role
CREATE USER john_analyst IDENTIFIED BY 'secure_pass456';
GRANT ROLE analyst_role TO john_analyst;
```

Verify the role assignment:
```sql
SHOW GRANTS FOR john_analyst;
+------------------------------------------+
| Grants                                   |
+------------------------------------------+
| GRANT ROLE analyst_role TO 'john_analyst'@'%' |
+------------------------------------------+
```

### Example 3: Create Users with Different Authentication Types

```sql
-- Create user with default authentication
CREATE USER user1 IDENTIFIED BY 'abc123';

-- Create user with SHA256 authentication
CREATE USER user2 IDENTIFIED WITH sha256_password BY 'abc123';
```

### Example 4: Create Users with Special Configurations

```sql
-- Create user with password change requirement
CREATE USER new_employee IDENTIFIED BY 'temp123' WITH MUST_CHANGE_PASSWORD = true;

-- Create user in disabled state
CREATE USER temp_user IDENTIFIED BY 'abc123' WITH DISABLED = true;

-- Create user with default role (role must be granted separately)
CREATE USER manager IDENTIFIED BY 'abc123' WITH DEFAULT_ROLE = 'admin';
GRANT ROLE admin TO manager;
```
