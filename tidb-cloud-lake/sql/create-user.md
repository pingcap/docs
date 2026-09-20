---
title: CREATE USER
summary: Creates a SQL user for connecting to {{{ .lake }}}. Users must be granted appropriate privileges to access databases and perform operations.
---

# CREATE USER

Creates a SQL user for connecting to {{{ .lake }}}. Users must be granted appropriate privileges to access databases and perform operations.

See also:

- [GRANT](/tidb-cloud-lake/sql/grant.md)
- [ALTER USER](/tidb-cloud-lake/sql/alter-user.md)
- [DROP USER](/tidb-cloud-lake/sql/drop-user.md)

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

### Example 1: Full Access Across All Databases

Create a user with full read/write access across all databases:

```sql
-- Create a role with global access
CREATE ROLE full_access_role;
GRANT ALL ON *.* TO ROLE full_access_role;

-- Create the user and assign the role
CREATE USER admin_user IDENTIFIED BY 'SecurePass456!' WITH DEFAULT_ROLE = 'full_access_role';
GRANT ROLE full_access_role TO admin_user;
```

### Example 2: Read-Only Access Across All Databases

Create a user that can only query data, suitable for dashboards or BI tools:

```sql
-- Create a read-only role
CREATE ROLE readonly_role;
GRANT SELECT ON *.* TO ROLE readonly_role;

-- Create the user
CREATE USER readonly_user IDENTIFIED BY 'ReadOnly789!' WITH DEFAULT_ROLE = 'readonly_role';
GRANT ROLE readonly_role TO readonly_user;
```

### Example 3: Single-Database Access

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

### Example 4: Create Users with Different Authentication Types

```sql
-- Create user with default authentication
CREATE USER user1 IDENTIFIED BY 'abc123';

-- Create user with SHA256 authentication
CREATE USER user2 IDENTIFIED WITH sha256_password BY 'abc123';
```
