---
title: User & Role
summary: This page provides a comprehensive overview of user and role operations in Databend, organized by functionality for easy reference.
---

# User & Role

This page provides a comprehensive overview of user and role operations in Databend, organized by functionality for easy reference.

## User Management

| Command | Description |
|---------|-------------|
| [CREATE USER](/tidb-cloud-lake/sql/create-user.md) | Creates a new user account |
| [ALTER USER](/tidb-cloud-lake/sql/alter-user.md) | Modifies an existing user account |
| [DROP USER](/tidb-cloud-lake/sql/drop-user.md) | Removes a user account |
| [DESC USER](/tidb-cloud-lake/sql/desc-user.md) | Shows detailed information about a user |
| [SHOW USERS](/tidb-cloud-lake/sql/show-users.md) | Lists all users in the system |

## Role Management

| Command | Description |
|---------|-------------|
| [CREATE ROLE](/tidb-cloud-lake/sql/create-role.md) | Creates a new role |
| [DROP ROLE](/tidb-cloud-lake/sql/drop-role.md) | Removes a role |
| [SET ROLE](/tidb-cloud-lake/sql/set-role.md) | Sets the current active role for the session |
| [SET SECONDARY ROLES](/tidb-cloud-lake/sql/set-secondary-roles.md) | Sets secondary roles for the session |
| [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) | Lists all roles in the system |

## Privilege Management

| Command | Description |
|---------|-------------|
| [GRANT](/tidb-cloud-lake/sql/grant.md) | Assigns privileges to roles |
| [REVOKE](/tidb-cloud-lake/sql/revoke.md) | Removes privileges from roles |
| [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md) | Shows role grants and role assignments |

> **Note:**
>
> Proper user and role management is essential for database security. Always follow the principle of least privilege when granting permissions.
