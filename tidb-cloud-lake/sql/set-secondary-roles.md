---
title: SET SECONDARY ROLES
sidebar_position: 6
---

Activates all secondary roles for the current session. This means that all secondary roles granted to the user will be active, extending the user's privileges. For more information about the active role and secondary roles, see [Active Role & Secondary Roles](/guides/security/access-control/roles#active-role--secondary-roles).

See also: [SET ROLE](04-user-set-role.md)

## Syntax

```sql
SET SECONDARY ROLES { ALL | NONE }
```

| Parameter | Default | Description                                                                                                                                                                                     |
|-----------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ALL       | Yes     | Activates all secondary roles granted to the user for the current session, in addition to the active role. This enables the user to utilize the privileges associated with all secondary roles. |
| NONE      | No      | Deactivates all secondary roles for the current session, meaning only the active role's privileges are active. This restricts the user's privileges to those granted by the active role alone.  |

## Examples

This example shows how secondary roles work and how to active/deactivate them.

1. Creating roles as user root.

First, let's create two roles, `admin` and `analyst`:

```sql
CREATE ROLE admin;

CREATE ROLE analyst;
```

2. Granting privileges.

Next, let's grant some privileges to each role. For example, we'll grant the `admin` role the ability to create databases, and the `analyst` role the ability to select from tables:

```sql
GRANT CREATE DATABASE ON *.* TO ROLE admin;

GRANT SELECT ON *.* TO ROLE analyst;
```

3. Creating a user.

Now, let's create a user:

```sql
CREATE USER 'user1' IDENTIFIED BY 'password';
```

4. Assigning roles.

Assign both roles to the user:

```sql
GRANT ROLE admin TO 'user1';

GRANT ROLE analyst TO 'user1';
```

5. Setting active role. 

Now, let's log in to Databend as `user1`, the set the active role to `analyst`.

```sql
SET ROLE analyst;
```

All secondary roles are activated by default, so we can create a new database:

```sql
CREATE DATABASE my_db;
```

6. Deactivate secondary roles.

The active role `analyst` does not have the CREATE DATABASE privilege. When all secondary roles are deactivated, creating a new database will fail.

```sql
SET SECONDARY ROLES NONE;

CREATE DATABASE my_db2;
error: APIError: ResponseError with 1063: Permission denied: privilege [CreateDatabase] is required on *.* for user 'user1'@'%' with roles [analyst,public]
```