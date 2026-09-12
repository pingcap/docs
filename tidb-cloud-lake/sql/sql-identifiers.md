---
title: SQL 标识符
summary: SQL 标识符是在 {{{ .lake }}} 中用于不同元素的名称，例如表、视图和数据库。
---

# SQL 标识符

SQL 标识符是在 {{{ .lake }}} 中用于不同元素的名称，例如表、视图和数据库。

## 不带引号和双引号标识符 {#unquoted-double-quoted-identifiers}

不带引号的标识符以字母（A-Z、a-z）或下划线（“_”）开头，并且可以由字母、下划线、数字（0-9）或美元符号（“$”）组成。

```text title='Examples:'
mydatalake
MyDatalake1
My$datalake
_my_datalake
```

双引号标识符可以包含更广泛的字符，例如数字（0-9）、特殊字符（如句点（.）、单引号（'）、感叹号（!）、at 符号（@）、井号（#）、美元符号（$）、百分号（%）、插入符号（^）和与号（&））、扩展 ASCII 和非 ASCII 字符，以及空格。

```text title='Examples:'
"MyDatalake"
"my.datalake"
"my datalake"
"My 'Datalake'"
"1_datalake"
"$Datalake"
```

请注意，使用双反引号（``）或双引号（"）是等价的：

```text title='Examples:'
`MyDatalake`
`my.datalake`
`my datalake`
`My 'Datalake'`
`1_datalake`
`$Datalake`
```

## 标识符大小写规则 {#identifier-casing-rules}

默认情况下，{{{ .lake }}} 会将不带引号的标识符以小写形式存储，而双引号标识符则按输入时的形式存储。换句话说，{{{ .lake }}} 默认将数据库、表和列等对象名称视为大小写不敏感。如果你希望 {{{ .lake }}} 将它们视为大小写敏感，请使用双引号。

> **注意：**
>
> 默认情况下，{{{ .lake }}} 遵循 PostgreSQL 风格的标识符大小写规则：不带引号的标识符会折叠为小写，而双引号标识符会保留其精确大小写并且大小写敏感。此行为由以下两个设置控制：
>
> - `unquoted_ident_case_sensitive`：默认值为 `0`，因此不带引号的标识符大小写不敏感，并会折叠为小写。将其设置为 `1` 会保留不带引号标识符的大小写，使其变为大小写敏感。
> - `quoted_ident_case_sensitive`：默认值为 `1`，因此双引号标识符会保留字符大小写并且大小写敏感。将其设置为 `0` 会使双引号标识符变为大小写不敏感。
>
> 如果你更希望使用 MySQL 风格的行为，即无论是否加引号标识符都大小写不敏感，请将 `unquoted_ident_case_sensitive` 和 `quoted_ident_case_sensitive` 都设置为 `0`。

### 为什么 `SELECT *` 可以工作，而 `SELECT <column>` 会失败 {#why-select-works-but-select-fails}

一个常见的困惑来源是：某个表的列是在保留大小写的引号（双引号或反引号）下创建的，例如 `"Employee_ID"`。在默认设置下，`SELECT *` 可以返回数据，但按列名引用时，无论你使用什么大小写形式都会失败：

```sql
-- Columns created with the case preserved
CREATE TABLE xxxTable ("Employee_ID" INT, "Department" VARCHAR);
INSERT INTO xxxTable VALUES (1, 'Eng');

-- Works: no column is referenced by name
SELECT * FROM xxxTable;

-- Fails: unquoted names are folded to lowercase (employee_id / department),
-- which do not match the stored "Employee_ID" / "Department"
SELECT Employee_ID FROM xxxTable;
SELECT employee_id FROM xxxTable;

-- Works: double quotes preserve the case and match the stored column name
SELECT "Employee_ID" FROM xxxTable;
```

这是因为 `unquoted_ident_case_sensitive` 的默认值为 `0`，因此 `Employee_ID` 和 `employee_id` 都会被解析为 `employee_id`，而该列并不存在。要确认列名的实际大小写，请运行 `DESC xxxTable;` 或 `SHOW CREATE TABLE xxxTable;`。

为避免这种情况，你可以在引用列时使用与创建时完全一致大小写的双引号；或者更推荐的做法是，在创建数据库、表和列时仅使用小写字母、数字和下划线（不加引号）。

以下示例演示了 {{{ .lake }}} 在创建和列出数据库时如何处理标识符的大小写：

```sql
-- Create a database named "datalake"
CREATE DATABASE datalake;

-- Attempt to create a database named "Datalake"
CREATE DATABASE Datalake;

>> SQL Error [1105] [HY000]: DatabaseAlreadyExists. Code: 2301, Text = Database 'datalake' already exists.

-- Create a database named "Datalake"
CREATE DATABASE "Datalake";

-- List all databases
SHOW DATABASES;

databases_in_default|
--------------------+
Datalake            |
datalake            |
default             |
information_schema  |
system              |
```

以下示例演示了 {{{ .lake }}} 如何处理表名和列名的大小写，突出显示了其默认的大小写敏感行为，以及如何使用双引号区分大小写不同的标识符：

```sql
-- Create a table named "datalake"
CREATE TABLE datalake (a INT);
DESC datalake;

Field|Type|Null|Default|Extra|
-----+----+----+-------+-----+
a    |INT |YES |NULL   |     |

-- Attempt to create a table named "Datalake"
CREATE TABLE Datalake (a INT);

>> SQL Error [1105] [HY000]: TableAlreadyExists. Code: 2302, Text = Table 'datalake' already exists.

-- Attempt to create a table with one column named "a" and the other one named "A"
CREATE TABLE "Datalake" (a INT, A INT);

>> SQL Error [1105] [HY000]: BadArguments. Code: 1006, Text = Duplicated column name: a.

-- Double quote the column names
CREATE TABLE "Datalake" ("a" INT, "A" INT);
DESC "Datalake";

Field|Type|Null|Default|Extra|
-----+----+----+-------+-----+
a    |INT |YES |NULL   |     |
A    |INT |YES |NULL   |     |
```

## 字符串标识符 {#string-identifiers}

在 {{{ .lake }}} 中，处理文本和日期等字符串项时，标准做法是将它们用单引号（'）括起来。

```sql
INSERT INTO weather VALUES ('San Francisco', 46, 50, 0.25, '1994-11-27');

SELECT 'Datalake';

'datalake'|
----------+
Datalake  |

SELECT "Datalake";

>> SQL Error [1105] [HY000]: SemanticError. Code: 1065, Text = error:
  --> SQL:1:73
  |
1 | /* ApplicationName=DBeaver 23.2.0 - SQLEditor <Script-12.sql> */ SELECT "Datalake"
  |                                                                         ^^^^^^^^^^ column Datalake doesn't exist, do you mean 'Datalake'?
```

默认情况下，{{{ .lake }}} 的 SQL 方言为 `PostgreSQL`：

```sql
SHOW SETTINGS LIKE '%sql_dialect%';

name       |value     |default   |level  |description                                                                      |type  |
-----------+----------+----------+-------+---------------------------------------------------------------------------------+------+
sql_dialect|PostgreSQL|PostgreSQL|SESSION|Sets the SQL dialect. Available values include "PostgreSQL", "MySQL", and "Hive".|String|
```

你可以将其更改为 `MySQL` 以启用双引号（`"`）：

```sql
SET sql_dialect='MySQL';

SELECT "demo";
+--------+
| 'demo' |
+--------+
| demo   |
+--------+
```