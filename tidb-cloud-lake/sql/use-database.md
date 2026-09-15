---
title: USE DATABASE
summary: 为当前会话选择一个数据库。该语句允许你指定并切换到另一个数据库。使用此命令设置当前数据库后，除非你主动更改，否则它会在整个会话期间保持不变。
---

# USE DATABASE

为当前会话选择一个数据库。该语句允许你指定并切换到另一个数据库。使用此命令设置当前数据库后，除非你主动更改，否则它会在整个会话期间保持不变。

## 语法 {#syntax}

```sql
USE <database_name>
```

## 重要说明 {#important-notes}

在某些情况下，执行 `USE <database>` 可能会比较慢。例如，当用户仅拥有部分表的所有权时，{{{ .lake }}} 需要扫描元信息以确定访问权限。

为了提升 `USE <database>` 语句的性能，尤其是在包含大量表或权限较复杂的数据库中，你可以将数据库上的 `USAGE` 权限授予某个角色，然后再将该角色分配给用户。

```sql
-- Grant USAGE privilege on the database to a role
GRANT USAGE ON <database_name>.* TO ROLE <role_name>;

-- Assign the role to a user
GRANT ROLE <role_name> TO <user_name>;
```

`USAGE` 权限允许用户进入数据库，但不会授予用户查看或访问任何表的能力。用户仍然需要适当的表级别权限（例如 `SELECT` 或 `OWNERSHIP`）才能查看或查询表。

## 示例 {#examples}

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