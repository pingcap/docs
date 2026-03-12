---
title: SHOW GRANTS
sidebar_position: 10
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.845"/>

Lists privileges granted to roles, role assignments for users, or privileges on a specific object.

See also:

- [SHOW_GRANTS](/sql/sql-functions/table-functions/show-grants)
- [GRANT](10-grant.md)
- [REVOKE](11-revoke.md)

## Syntax

```sql
-- List grants for a user
SHOW GRANTS FOR <user_name> [ LIKE '<pattern>' | WHERE <expr> | LIMIT <limit> ]

-- List privileges granted to a role
SHOW GRANTS FOR ROLE <role_name> [ LIKE '<pattern>' | WHERE <expr> | LIMIT <limit> ]

-- List privileges granted on an object
SHOW GRANTS ON { STAGE | TABLE | DATABASE | UDF | MASKING POLICY | ROW ACCESS POLICY } <object_name> [ LIKE '<pattern>' | WHERE <expr> | LIMIT <limit> ]

-- Lists all users and roles that have been directly granted role_name.
SHOW GRANTS OF ROLE <role_name>
     
```

## Examples

This example illustrates how to list grants for a user, privileges granted to a role, and privileges on a specific object.

```sql
-- Create a new user
CREATE USER 'user1' IDENTIFIED BY 'password';

-- Create a new role
CREATE ROLE analyst;

-- Grant the analyst role to the user
GRANT ROLE analyst TO 'user1';

-- Create a database
CREATE DATABASE my_db;

-- Grant privileges on the database to the role
GRANT OWNERSHIP ON my_db.* TO ROLE analyst;

-- List privileges granted to the user
SHOW GRANTS FOR user1;


┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ privileges │ object_name │     object_id    │ grant_to │  name  │                       grants                         │
├────────────┼─────────────┼──────────────────┼──────────┼────────┼──────────────────────────────────────────────────────┤
│ ROLE       │ NULL        │             NULL │ USER     │ user1  │ GRANT ROLE analyst TO 'user1'@'%'                    │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- List privileges granted to the role
SHOW GRANTS FOR ROLE analyst;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ privileges │ object_name │     object_id    │ grant_to │   name  │                          grants                          │
├────────────┼─────────────┼──────────────────┼──────────┼─────────┼──────────────────────────────────────────────────────────┤
│ OWNERSHIP  │ my_db       │               16 │ ROLE     │ analyst │ GRANT OWNERSHIP ON 'default'.'my_db'.* TO ROLE `analyst` │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
-- List privileges granted on the database
SHOW GRANTS ON DATABASE my_db;

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ privileges │ object_name │     object_id    │ grant_to │   name  │      grants      ├────────────┼─────────────┼──────────────────┼──────────┼─────────┼──────────────────┤
│ OWNERSHIP  │ my_db       │               16 │ ROLE     │ analyst │                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

-- Lists all users and roles that have been directly granted role_name.  
-- This command displays only the direct grantees of role_name. 
-- This means it lists users and roles that have explicitly received the role through a GRANT ROLE role_name TO <user_or_role> statement. 
-- It does not show users or roles that acquire role_name indirectly via role hierarchies or inheritance.
SHOW GRANTS OF ROLE analyst

╭─────────────────────────────────────╮
│   role  │ granted_to │ grantee_name │
│  String │   String   │    String    │
├─────────┼────────────┼──────────────┤
│ analyst │ USER       │ user1        │
╰─────────────────────────────────────╯

SHOW GRANTS ON MASKING POLICY email_mask;

-- Inspect row access policy privileges
SHOW GRANTS ON ROW ACCESS POLICY rap_region;
```
