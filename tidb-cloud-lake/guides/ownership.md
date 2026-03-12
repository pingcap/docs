---
title: Ownership
---

Ownership is a specialized privilege that signifies the exclusive rights and responsibilities a role holds over a specific data object (currently including a database, table, UDF, and stage) within Databend. 

## Granting Ownership

An object's ownership is automatically granted to the role of the user who creates it and can be transferred between roles using the [GRANT](/sql/sql-commands/ddl/user/grant) command:

- Granting ownership of an object to a new role transfers full ownership to the new role, removing it from the previous role. For example, if Role A initially owns a table and you grant ownership to Role B, Role B will become the new owner, and Role A will no longer have ownership rights to that table.
- Granting ownership to the built-in role `public` is not recommended for security reasons. If a user is in the `public` role when creating a object, then all users will have ownership of the object because each user has the `public` role by default. Databend recommends creating and assigning customized roles to users instead of using the `public` role for clarified ownership management. For information about the built-in roles, see [Built-in Roles](02-roles.md).
- Ownership cannot be granted for tables in the `default` database, as it is owned by the built-in role `account_admin`.

## Revoking Ownership Not Allowed

Revoking ownership is *not* supported because every object must have an owner. 

- If an object is dropped, it will not retain its ownership by the original role. If the object is restored (if possible), ownership will not be automatically reassigned, and an `account_admin` will need to manually reassign ownership to a role.
- If a role that owns an object is deleted, an `account_admin` can transfer ownership of the object to another role.

## Examples

To grant ownership to a role, use the [GRANT](/sql/sql-commands/ddl/user/grant) command. These examples demonstrate granting ownership of different database objects to the role 'data_owner':

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

This example demonstrates the establishment of role-based ownership in Databend. Administrators create a role 'role1' and assign it to user 'u1'. Permissions to create tables in the 'db' schema are granted to 'role1'. Consequently, when 'u1' logs in, they possess the privileges of 'role1', allowing them to create and own tables under 'db'. However, access to tables not owned by 'role1' is restricted, as evidenced by the failed query on 'db.t_old_exists'.

```sql
-- Admin creates roles and assigns roles to corresponding users
CREATE ROLE role1;
CREATE USER u1 IDENTIFIED BY '123' WITH DEFAULT ROLE 'role1';
GRANT CREATE ON db.* TO ROLE role1;
GRANT ROLE role1 TO u1;

-- After u1 logs into atabend, role1 has been granted to u1, so u1 can create and own tables under db:
u1> CREATE TABLE db.t(id INT);
u1> INSERT INTO db.t VALUES(1);
u1> SELECT * FROM db.t;
u1> SELECT * FROM db.t_old_exists; -- Failed because the owner of this table is not role1
```

This example shows how to let a user create databases that are owned only by their role, so other users cannot see them unless explicitly granted access:

```sql
CREATE ROLE part1_role;
GRANT CREATE DATABASE ON *.* TO ROLE part1_role;
CREATE USER user1 IDENTIFIED BY 'abc123' WITH DEFAULT ROLE 'part1_role';
GRANT ROLE part1_role TO user1;

-- When user1 creates a database, ownership is assigned to part1_role.
-- Other users will not be able to see or access that database unless
-- privileges or ownership are granted to their roles.
```
