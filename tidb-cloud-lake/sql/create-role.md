---
title: CREATE ROLE
sidebar_position: 5
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.703"/>

Creates a new role for access control. Roles are used to group privileges and can be assigned to users or other roles, providing a flexible way to manage permissions in Databend.

## Syntax

```sql
CREATE ROLE [ IF NOT EXISTS ] <name>
```

**Parameters:**

- `IF NOT EXISTS`: Create the role only if it doesn't exist (recommended to avoid errors)
- `<name>`: Role name (cannot contain single quotes, double quotes, backspace, or form feed characters)

## Examples

```sql
-- Create a basic role
CREATE ROLE analyst;

-- Create role only if it doesn't exist (recommended)
CREATE ROLE IF NOT EXISTS data_viewer;
```

## Common Usage Patterns

### Read-Only Analyst Role

Create a role for data analysts who need read access to sales data:

```sql
-- Create the analyst role
CREATE ROLE sales_analyst;

-- Grant read permissions
GRANT SELECT ON sales_db.* TO ROLE sales_analyst;

-- Assign to users
GRANT ROLE sales_analyst TO 'alice';
GRANT ROLE sales_analyst TO 'bob';
```

### Database Administrator Role

Create a role for administrators who need full control:

```sql
-- Create the admin role
CREATE ROLE sales_admin;

-- Grant full permissions on the database
GRANT ALL ON sales_db.* TO ROLE sales_admin;

-- Grant user management permissions
GRANT CREATE USER, CREATE ROLE ON *.* TO ROLE sales_admin;

-- Assign to admin users
GRANT ROLE sales_admin TO 'admin_user';
```

### Verification

```sql
-- Check what each role can do
SHOW GRANTS FOR ROLE sales_analyst;
SHOW GRANTS FOR ROLE sales_admin;

-- Check user permissions
SHOW GRANTS FOR 'alice';
SHOW GRANTS FOR 'admin_user';
```


## See Also

- [GRANT](10-grant.md) - Grant privileges and roles
- [SHOW GRANTS](22-show-grants.md) - View granted privileges
- [DROP ROLE](05-user-drop-role.md) - Drop roles
