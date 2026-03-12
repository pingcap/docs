---
title: USE DATABASE
sidebar_position: 3
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.721"/>

Selects a database for the current session. This statement allows you to specify and switch to a different database. Once you set the current database using this command, it remains the same until the end of the session unless you choose to change it.

## Syntax

```sql
USE <database_name>
```

## Important Notes

In some cases, executing `USE <database>` can be slow—for example, when the user has ownership of only a subset of tables, and Databend needs to scan metadata to determine access rights.

To improve the performance of the `USE <database>` statement—especially in databases with many tables or complex permissions—you can grant the `USAGE` privilege on the database to a role, and then assign that role to users.

```sql
-- Grant USAGE privilege on the database to a role
GRANT USAGE ON <database_name>.* TO ROLE <role_name>;

-- Assign the role to a user
GRANT ROLE <role_name> TO <user_name>;
```

The `USAGE` privilege allows users to enter the database but does not grant visibility or access to any tables. Users still need appropriate table-level privileges such as `SELECT` or `OWNERSHIP` to see or query tables.

## Examples

```sql
-- Create two databases
CREATE DATABASE database1;
CREATE DATABASE database2;

-- Select and use "database1" as the current database
USE database1;

-- Create a new table "table1" in "database1"
CREATE TABLE table1 (
  id INT,
  name VARCHAR(50)
);

-- Insert data into "table1"
INSERT INTO table1 (id, name) VALUES (1, 'John');
INSERT INTO table1 (id, name) VALUES (2, 'Alice');

-- Query all data from "table1"
SELECT * FROM table1;

-- Switch to "database2" as the current database
USE database2;

-- Create a new table "table2" in "database2"
CREATE TABLE table2 (
  id INT,
  city VARCHAR(50)
);

-- Insert data into "table2"
INSERT INTO table2 (id, city) VALUES (1, 'New York');
INSERT INTO table2 (id, city) VALUES (2, 'London');

-- Query all data from "table2"
SELECT * FROM table2;
```