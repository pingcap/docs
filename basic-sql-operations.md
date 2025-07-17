---
title: 使用 TiDB 探索 SQL
summary: 了解 TiDB 数据库的基本 SQL 语句。
---

# 使用 TiDB 探索 SQL

TiDB 兼容 MySQL，在大多数情况下，你可以直接使用 MySQL 语句。对于不支持的功能，请参见 [Compatibility with MySQL](/mysql-compatibility.md#unsupported-features)。

<CustomContent platform="tidb">

为了试验 SQL 并测试 TiDB 与 MySQL 查询的兼容性，你可以尝试 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=basic-sql-operations)。你也可以先部署一个 TiDB 集群，然后在其中运行 SQL 语句。

</CustomContent>

本页面将引导你了解基本的 TiDB SQL 语句，如 DDL、DML 和 CRUD 操作。有关 TiDB 语句的完整列表，请参见 [SQL Statement Overview](/sql-statements/sql-statement-overview.md)。

## 分类

根据功能，SQL 被划分为以下 4 种类型：

- DDL（Data Definition Language，数据定义语言）：用于定义数据库对象，包括数据库、表、视图和索引。

- DML（Data Manipulation Language，数据操作语言）：用于操作应用相关的记录。

- DQL（Data Query Language，数据查询语言）：用于在条件过滤后查询记录。

- DCL（Data Control Language，数据控制语言）：用于定义访问权限和安全级别。

常见的 DDL 功能包括创建、修改和删除对象（如表和索引）。对应的命令是 `CREATE`、`ALTER` 和 `DROP`。

## 显示、创建和删除数据库

在 TiDB 中，数据库可以被视为一组对象的集合，例如表和索引。

要显示数据库列表，使用 `SHOW DATABASES` 语句：

```sql
SHOW DATABASES;
```

要使用名为 `mysql` 的数据库，使用以下语句：

```sql
USE mysql;
```

要显示某个数据库中的所有表，使用 `SHOW TABLES` 语句：

```sql
SHOW TABLES FROM mysql;
```

要创建数据库，使用 `CREATE DATABASE` 语句：

```sql
CREATE DATABASE db_name [options];
```

要创建名为 `samp_db` 的数据库，使用以下语句：

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

添加 `IF NOT EXISTS` 以防止数据库已存在时出现错误。

要删除数据库，使用 `DROP DATABASE` 语句：

```sql
DROP DATABASE samp_db;
```

## 创建、显示和删除表

要创建表，使用 `CREATE TABLE` 语句：

```sql
CREATE TABLE table_name column_name data_type constraint;
```

例如，要创建一个名为 `person` 的表，包含编号、姓名和生日等字段，使用以下语句：

```sql
CREATE TABLE person (
    id INT,
    name VARCHAR(255),
    birthday DATE
    );
```

要查看创建该表的语句（DDL），使用 `SHOW CREATE` 语句：

```sql
SHOW CREATE table person;
```

要删除表，使用 `DROP TABLE` 语句：

```sql
DROP TABLE person;
```

## 创建、显示和删除索引

索引用于加快对索引列的查询。对于值非唯一的列，创建索引使用 `CREATE INDEX` 语句：

```sql
CREATE INDEX person_id ON person (id);
```

也可以使用 `ALTER TABLE` 语句：

```sql
ALTER TABLE person ADD INDEX person_id (id);
```

对于值唯一的列，创建唯一索引使用 `CREATE UNIQUE INDEX` 语句：

```sql
CREATE UNIQUE INDEX person_unique_id ON person (id);
```

或者使用 `ALTER TABLE` 语句：

```sql
ALTER TABLE person ADD UNIQUE person_unique_id (id);
```

要显示表中的所有索引，使用 `SHOW INDEX` 语句：

```sql
SHOW INDEX FROM person;
```

要删除索引，可以使用 `DROP INDEX` 或 `ALTER TABLE` 语句。`DROP INDEX` 可以嵌套在 `ALTER TABLE` 中：

```sql
DROP INDEX person_id ON person;
```

```sql
ALTER TABLE person DROP INDEX person_unique_id;
```

> **Note:**
> 
> DDL 操作不是事务性操作。执行 DDL 时，无需运行 `COMMIT` 语句。

## 插入、更新和删除数据

常见的 DML 功能包括添加、修改和删除表中的记录。对应的命令是 `INSERT`、`UPDATE` 和 `DELETE`。

向表中插入数据，使用 `INSERT` 语句：

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

向表中插入部分字段的数据，使用 `INSERT` 语句：

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

更新表中某条记录的部分字段，使用 `UPDATE` 语句：

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

删除表中的数据，使用 `DELETE` 语句：

```sql
DELETE FROM person WHERE id=2;
```

> **Note:**
> 
> 不带 `WHERE` 条件的 `UPDATE` 和 `DELETE` 语句会操作整个表。

## 查询数据

DQL 用于从表或多个表中检索所需的数据行。

要查看表中的数据，使用 `SELECT` 语句：

```sql
SELECT * FROM person;
```

要查询特定列，添加列名到 `SELECT` 关键字后：

```sql
SELECT name FROM person;
```

```sql
+------+
| name |
+------+
| tom  |
+------+
1 rows in set (0.00 sec)
```

使用 `WHERE` 子句过滤所有符合条件的记录，然后返回结果：

```sql
SELECT * FROM person where id<5;
```

## 创建、授权和删除用户

DCL 通常用于创建或删除用户，以及管理用户权限。

要创建用户，使用 `CREATE USER` 语句。以下示例创建一个名为 `tiuser`，密码为 `123456` 的用户：

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

授予 `tiuser` 访问 `samp_db` 数据库中表的权限：

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

查看 `tiuser` 的权限：

```sql
SHOW GRANTS for tiuser@localhost;
```

删除 `tiuser`：

```sql
DROP USER 'tiuser'@'localhost';
```