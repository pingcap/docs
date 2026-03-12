---
title: SHOW DROP DATABASES
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.658"/>

Lists all databases along with their deletion timestamps if they have been dropped, allowing users to review deleted databases and their details.

- Dropped databases can only be retrieved if they are within the data retention period.
- It is recommended to use an admin user, such as `root`. If you are using Databend Cloud, use a user with the `account_admin` role to query dropped databases.

See also: [system.databases_with_history](../../../00-sql-reference/31-system-tables/system-databases-with-history.md)

## Syntax

```sql
SHOW DROP DATABASES 
    [ FROM <catalog> ]
    [ LIKE '<pattern>' | WHERE <expr> ]
```

## Examples

```sql
-- Create a new database named my_db
CREATE DATABASE my_db;

-- Drop the database my_db
DROP DATABASE my_db;

-- If a database has been dropped, dropped_on shows the deletion time; 
-- If it is still active, dropped_on is NULL.
SHOW DROP DATABASES;

┌─────────────────────────────────────────────────────────────────────────────────┐
│ catalog │        name        │     database_id     │         dropped_on         │
├─────────┼────────────────────┼─────────────────────┼────────────────────────────┤
│ default │ default            │                   1 │ NULL                       │
│ default │ information_schema │ 4611686018427387906 │ NULL                       │
│ default │ my_db              │                 114 │ 2024-11-15 02:44:46.207120 │
│ default │ system             │ 4611686018427387905 │ NULL                       │
└─────────────────────────────────────────────────────────────────────────────────┘
```