---
title: 使用 TiDB Cloud 探索兼容 PostgreSQL 的 SQL
summary: 了解兼容 PostgreSQL 的 TiDB Cloud Starter 支持的基本 SQL 语句。
---

# 使用 TiDB Cloud 探索兼容 PostgreSQL 的 SQL

兼容 PostgreSQL 的 {{{ .starter }}} 支持 PostgreSQL wire 协议和常见的 PostgreSQL 语法。你可以使用大多数 PostgreSQL 客户端、驱动和 ORM 来操作你的实例。

本页将带你了解基本的 SQL 操作，包括 DDL、DML、DQL、DCL 和事务控制。

如需了解不受支持或行为不同的 PostgreSQL 特性，请参见 [PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。

## 类别 {#categories}

SQL 语句可以根据其功能分为以下几类：

- **DDL（数据定义语言）**：定义和管理数据库对象，包括数据库、数据库模式、表、视图、索引、序列和类型。
- **DML（数据操作语言）**：插入、修改和删除表数据。
- **DQL（数据查询语言）**：使用 `SELECT`、过滤、连接、聚合、子查询、公用表表达式（CTE）以及其他查询特性来查询数据。
- **DCL（数据控制语言）**：管理权限和角色成员关系。
- **事务控制**：使用 `BEGIN`、`COMMIT`、`ROLLBACK` 和 `SAVEPOINT` 等语句管理事务。

常见的 DDL 操作包括创建、修改和删除对象。对应的命令分别是 `CREATE`、`ALTER` 和 `DROP`。

## 列出、创建和删除数据库 {#list-create-and-drop-databases}

要列出数据库，请查询 `pg_database` 系统目录：

```sql
SELECT datname
FROM pg_database
ORDER BY datname;
```

要创建一个名为 `samp_db` 的数据库，请使用 `CREATE DATABASE` 语句：

```sql
CREATE DATABASE samp_db;
```

使用 `psql` 时，要连接到该数据库，请使用 `\connect` 命令：

```text
\connect samp_db
```

> **Note:**
>
> `\connect` 是 `psql` 客户端命令，不是 SQL 语句。

要删除数据库，请先连接到另一个数据库：

```text
\connect postgres
```

然后使用 `DROP DATABASE` 语句：

```sql
DROP DATABASE samp_db;
```

## 创建、列出和删除表 {#create-list-and-drop-tables}

要创建表，请使用 `CREATE TABLE` 语句。

例如，创建一个名为 `person` 的表：

```sql
CREATE TABLE person (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE
);
```

要列出 `public` 数据库模式中的表：

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

要查看 `person` 表的列：

```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'person'
ORDER BY ordinal_position;
```

要删除该表，请使用 `DROP TABLE` 语句：

```sql
DROP TABLE person;
```

## 创建、列出和删除索引 {#create-list-and-drop-indexes}

索引可以提升对已建立索引列的查询性能。

要在 `name` 列上创建索引：

```sql
CREATE INDEX person_name_idx ON person (name);
```

要创建唯一索引：

```sql
CREATE UNIQUE INDEX person_name_unique_idx ON person (name);
```

要列出 `person` 表上的索引：

```sql
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'person'
ORDER BY indexname;
```

要删除索引，请使用 `DROP INDEX` 语句：

```sql
DROP INDEX person_name_idx;
```

有关支持的 PostgreSQL 索引方法及兼容性差异，请参见 [PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。

## 插入、修改和删除数据 {#insert-update-and-delete-data}

常见的 DML 操作使用 `INSERT`、`UPDATE` 和 `DELETE` 语句。

要向 `person` 表中插入一行：

```sql
INSERT INTO person (name, birthday)
VALUES ('Tom', DATE '1990-09-12');
```

要插入多行：

```sql
INSERT INTO person (name, birthday)
VALUES
    ('Alice', DATE '1992-05-01'),
    ('Bob', DATE '1993-08-08');
```

兼容 PostgreSQL 的 {{{ .starter }}} 支持 `RETURNING`。例如，插入一行后返回生成的 ID：

```sql
INSERT INTO person (name, birthday)
VALUES ('Carol', DATE '1994-03-15')
RETURNING id, name;
```

要修改一行：

```sql
UPDATE person
SET birthday = DATE '1990-10-12'
WHERE name = 'Tom';
```

要删除一行：

```sql
DELETE FROM person
WHERE name = 'Bob';
```

> **Note:**
>
> 不带 `WHERE` 子句的 `UPDATE` 和 `DELETE` 语句会作用于表中的所有行。

### Upsert 数据 {#upsert-data}

使用 `INSERT ... ON CONFLICT` 插入一行数据或处理唯一性冲突。

例如：

```sql
CREATE TABLE account (
    id BIGSERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT
);

INSERT INTO account (email, name)
VALUES ('alice@example.com', 'Alice')
ON CONFLICT (email)
DO UPDATE SET name = excluded.name;
```

## 查询数据 {#query-data}

使用 `SELECT` 语句查询数据。

查询所有列：

```sql
SELECT *
FROM person;
```

查询指定列：

```sql
SELECT id, name
FROM person;
```

使用 `WHERE` 子句过滤行：

```sql
SELECT id, name, birthday
FROM person
WHERE birthday >= DATE '1992-01-01'
ORDER BY birthday;
```

PostgreSQL-compatible {{{ .starter }}} 还支持 PostgreSQL 的常见查询特性，例如 join、子查询、CTE、递归 CTE、窗口函数和集合操作。

例如，使用 CTE 过滤数据：

```sql
WITH recent_people AS (
    SELECT id, name, birthday
    FROM person
    WHERE birthday >= DATE '1992-01-01'
)
SELECT *
FROM recent_people
ORDER BY birthday;
```

## 管理事务 {#manage-transactions}

使用 `BEGIN` 和 `COMMIT` 在一个事务中执行多条语句：

```sql
BEGIN;

UPDATE account
SET name = 'Alice Chen'
WHERE email = 'alice@example.com';

COMMIT;
```

要丢弃当前事务中的更改，请使用 `ROLLBACK`：

```sql
BEGIN;

DELETE FROM account
WHERE email = 'alice@example.com';

ROLLBACK;
```

也支持保存点：

```sql
BEGIN;

UPDATE account
SET name = 'Alice'
WHERE email = 'alice@example.com';

SAVEPOINT before_second_update;

UPDATE account
SET name = 'Alice Updated'
WHERE email = 'alice@example.com';

ROLLBACK TO SAVEPOINT before_second_update;

COMMIT;
```

有关支持的事务隔离级别以及与 PostgreSQL 的兼容性差异，请参见 [PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。

## 创建角色、为其授权并删除角色 {#create-grant-privileges-to-and-drop-a-role}

DCL 语句用于管理权限和角色成员关系。

创建一个可登录的角色：

```sql
CREATE ROLE app_user
LOGIN
PASSWORD 'SecurePass1';
```

为该角色授予对 `public` 数据库模式的访问权限，以及查询 `person` 表的权限：

```sql
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT ON person TO app_user;
```

检查授予该角色的表权限：

```sql
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE grantee = 'app_user'
ORDER BY table_schema, table_name, privilege_type;
```

回收这些权限：

```sql
REVOKE SELECT ON person FROM app_user;
REVOKE USAGE ON SCHEMA public FROM app_user;
```

删除该角色：

```sql
DROP ROLE app_user;
```