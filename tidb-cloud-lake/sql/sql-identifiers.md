---
title: SQL Identifiers
summary: SQL identifiers are names used for different elements within {{{ .lake }}}, such as tables, views, and databases.
---

# SQL Identifiers

SQL identifiers are names used for different elements within {{{ .lake }}}, such as tables, views, and databases.

## Unquoted & Double-quoted Identifiers

Unquoted identifiers begin with a letter (A-Z, a-z) or underscore (“_”) and may consist of letters, underscores, numbers (0-9), or dollar signs (“$”).

```text title='Examples:'
mydatalake
MyDatalake1
My$datalake
_my_datalake
```

Double-quoted identifiers can include a wide range of characters, such as numbers (0-9), special characters (like period (.), single quote ('), exclamation mark (!), at symbol (@), number sign (#), dollar sign ($), percent sign (%), caret (^), and ampersand (&)), extended ASCII and non-ASCII characters, as well as blank spaces.

```text title='Examples:'
"MyDatalake"
"my.datalake"
"my datalake"
"My 'Datalake'"
"1_datalake"
"$Datalake"
```

Note that using double backticks (``) or double quotes (") is equivalent:

```text title='Examples:'
`MyDatalake`
`my.datalake`
`my datalake`
`My 'Datalake'`
`1_datalake`
`$Datalake`
```

## Identifier Casing Rules

{{{ .lake }}} stores unquoted identifiers by default in lowercase and double-quoted identifiers as they are entered. In other words, {{{ .lake }}} handles object names, such as databases, tables, and columns, as case-insensitive. If you want {{{ .lake }}} to handle them as case-sensitive, double-quote them.

> **Note:**
>
> By default, {{{ .lake }}} follows PostgreSQL-style identifier casing: unquoted identifiers are folded to lowercase, while double-quoted identifiers preserve their exact case and are case-sensitive. This behavior is controlled by two settings:
>
> - `unquoted_ident_case_sensitive`: Defaults to `0`, so unquoted identifiers are case-insensitive and folded to lowercase. Setting it to `1` preserves the case of unquoted identifiers, making them case-sensitive.
> - `quoted_ident_case_sensitive`: Defaults to `1`, so double-quoted identifiers preserve the case of characters and are case-sensitive. Setting it to `0` makes double-quoted identifiers case-insensitive.
>
> If you prefer MySQL-style behavior where identifiers are case-insensitive regardless of quoting, set both `unquoted_ident_case_sensitive` and `quoted_ident_case_sensitive` to `0`.

### Why `SELECT *` works but `SELECT <column>` fails

A common source of confusion is a table whose columns were created with case-preserving quotes (double quotes or backticks), for example `"Employee_ID"`. With the default settings, `SELECT *` returns data, but referencing a column by name fails no matter how you case it:

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

This happens because `unquoted_ident_case_sensitive` defaults to `0`, so both `Employee_ID` and `employee_id` are resolved as `employee_id`, which does not exist. To confirm the actual column casing, run `DESC xxxTable;` or `SHOW CREATE TABLE xxxTable;`.

To avoid this, either reference the column with double quotes using the exact case from creation time, or, better, use only lowercase letters, digits, and underscores (no quoting) when creating databases, tables, and columns.

The following example demonstrates how {{{ .lake }}} treats the casing of identifiers when creating and listing databases:

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

This example demonstrates how {{{ .lake }}} handles identifier casing for table and column names, highlighting its case-sensitivity by default and the use of double quotes to differentiate between identifiers with varying casing:

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

## String Identifiers

In {{{ .lake }}}, when managing string items like text and dates, it is essential to enclose them within single quotes (') as a standard practice.

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

By default, {{{ .lake }}} SQL dialect is `PostgreSQL`:

```sql
SHOW SETTINGS LIKE '%sql_dialect%';

name       |value     |default   |level  |description                                                                      |type  |
-----------+----------+----------+-------+---------------------------------------------------------------------------------+------+
sql_dialect|PostgreSQL|PostgreSQL|SESSION|Sets the SQL dialect. Available values include "PostgreSQL", "MySQL", and "Hive".|String|
```

You can change it to `MySQL` to enable double quotes (`"`):

```sql
SET sql_dialect='MySQL';

SELECT "demo";
+--------+
| 'demo' |
+--------+
| demo   |
+--------+
```
