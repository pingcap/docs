---
title: Schema Object Names
summary: Introduce schema object names in TiDB SQL statements.
aliases: ['/docs/dev/schema-object-names/','/docs/dev/reference/sql/language-structure/schema-object-names/']
---

# Schema Object Names

<!-- markdownlint-disable MD038 -->

This article introduces schema object names in TiDB SQL statements.

Schema object names are used to name all schema objects in TiDB, including database, table, index, column, alias, etc. You can quote these objects by identifiers in SQL statements.

You can use the backtick to enclose the identifier, ie `SELECT * FROM t` can also be written as`` SELECT * FROM `t` ``. But if there is at least one special character in the identifier, or it is a reserved keyword, it must be enclosed in the backtick to refer to the schema object it represents.

```sql
mysql> SELECT * FROM `table` WHERE `table`.id = 20;
```

If you set `ANSI_QUOTES` in SQL MODE, TiDB will recognize the string enclosed in double quotes `"` as identifier.

```sql
MySQL [test]> CREATE TABLE "test" (a varchar(10));
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 19 near ""test" (a varchar(10))" 

MySQL [test]> SET SESSION sql_mode='ANSI_QUOTES';
Query OK, 0 rows affected (0.000 sec)

MySQL [test]> CREATE TABLE "test" (a varchar(10));
Query OK, 0 rows affected (0.012 sec)
```

If you want to use the backtick character in the quoted identifier, you need to repeat the backtick twice, for example to create a table a`b:

```sql
mysql> CREATE TABLE `a``b` (a int);
```

In a `SELECT` statement, a quoted column alias can be specified using an identifier or a string quoting characters:

```sql
mysql> SELECT 1 AS `identifier`, 2 AS 'string';
+------------+--------+
| identifier | string |
+------------+--------+
|          1 |      2 |
+------------+--------+
1 row in set (0.00 sec)
```

For more information, see [MySQL Documentation](https://dev.mysql.com/doc/refman/5.7/en/identifiers.html).

## Identifier qualifiers

Object names can be unqualified or qualified. For example, the following statement creates a table using the unqualified name:

```sql
CREATE TABLE t (i int);
```

If you have not used the `USE` or connection parameter to set the database, the `ERROR 1046 (3D000): No database selected` is displayed. At this time you can specify the database qualified name:

```sql
CREATE TABLE test.t (i int);
```

There can be white spaces around `.`, and `table_name.col_name` and `table_name . col_name` are equivalent.

To quote this identifier, use:

```sql
`table_name`.`col_name`
```

Instead of：

```sql
`table_name.col_name`
```

For more information, see [MySQL Documentation](https://dev.mysql.com/doc/refman/5.7/en/identifier-qualifiers.html).
