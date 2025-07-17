---
title: Schema Object Names
summary: 了解 TiDB SQL 语句中的 schema object names。
---

# Schema Object Names

<!-- markdownlint-disable MD038 -->

本文介绍 TiDB SQL 语句中的 schema object names。

schema object names 用于命名 TiDB 中的所有 schema 对象，包括 database、table、index、column 和 alias。你可以在 SQL 语句中使用标识符对这些对象进行引用。

你可以使用反引号将标识符括起来。例如，`SELECT * FROM t` 也可以写成 `` SELECT * FROM `t` ``。但如果标识符包含一个或多个特殊字符或是保留关键字，则必须用反引号括起来以引用它所代表的 schema 对象。

```sql
SELECT * FROM `table` WHERE `table`.id = 20;
```

如果在 SQL MODE 中设置了 `ANSI_QUOTES`，TiDB 会将用双引号 `"` 包含的字符串识别为标识符。

```sql
CREATE TABLE "test" (a varchar(10));
```

```sql
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 19 near ""test" (a varchar(10))" 
```

```sql
SET SESSION sql_mode='ANSI_QUOTES';
```

```sql
Query OK, 0 rows affected (0.000 sec)
```

```sql
CREATE TABLE "test" (a varchar(10));
```

```sql
Query OK, 0 rows affected (0.012 sec)
```

如果你想在引用的标识符中使用反引号字符，可以将反引号重复写两次。例如，创建一个表 a`b：

```sql
CREATE TABLE `a``b` (a int);
```

在 `SELECT` 语句中，你可以使用标识符或字符串来指定别名：

```sql
SELECT 1 AS `identifier`, 2 AS 'string';
```

```sql
+------------+--------+
| identifier | string |
+------------+--------+
|          1 |      2 |
+------------+--------+
1 row in set (0.00 sec)
```

更多信息请参见 [MySQL Schema Object Names](https://dev.mysql.com/doc/refman/8.0/en/identifiers.html)。

## Identifier qualifiers

对象名称可以是未限定的或限定的。例如，以下语句创建了一个没有限定名的表：

```sql
CREATE TABLE t (i int);
```

如果你没有使用 `USE` 语句或连接参数配置数据库，则会显示 `ERROR 1046 (3D000): No database selected` 错误。此时，你可以指定数据库限定名：

```sql
CREATE TABLE test.t (i int);
```

在 `.` 两边可以存在空白字符。`table_name.col_name` 和 `table_name . col_name` 是等价的。

要引用此标识符，请使用：

```sql
`table_name`.`col_name`
```

而不是：

```sql
`table_name.col_name`
```

更多信息请参见 [MySQL Identifier Qualifiers](https://dev.mysql.com/doc/refman/8.0/en/identifier-qualifiers.html)。