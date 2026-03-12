---
title: User & Role 
---

This page provides a comprehensive overview of user and role operations in Databend, organized by functionality for easy reference.

## User Management

| Command | Description |
|---------|-------------|
| [CREATE USER](01-user-create-user.md) | Creates a new user account |
| [ALTER USER](03-user-alter-user.md) | Modifies an existing user account |
| [DROP USER](02-user-drop-user.md) | Removes a user account |
| [DESC USER](01-user-desc-user.md) | Shows detailed information about a user |
| [SHOW USERS](02-user-show-users.md) | Lists all users in the system |

## Role Management

| Command | Description |
|---------|-------------|
| [CREATE ROLE](04-user-create-role.md) | Creates a new role |
| [DROP ROLE](05-user-drop-role.md) | Removes a role |
| [SET ROLE](04-user-set-role.md) | Sets the current active role for the session |
| [SET SECONDARY ROLES](04-user-set-2nd-roles.md) | Sets secondary roles for the session |
| [SHOW ROLES](04-user-show-roles.md) | Lists all roles in the system |

## Privilege Management

| Command | Description |
|---------|-------------|
| [GRANT](10-grant.md) | Assigns privileges to roles |
| [REVOKE](11-revoke.md) | Removes privileges from roles |
| [SHOW GRANTS](22-show-grants.md) | Shows role grants and role assignments |

:::note
Proper user and role management is essential for database security. Always follow the principle of least privilege when granting permissions.
:::
