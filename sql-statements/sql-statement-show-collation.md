---
title: SHOW COLLATION | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW COLLATION for the TiDB database.
---

# SHOW COLLATION

This statement provides a static list of collations, and is included to provide compatibility with MySQL client libraries.

> **Note:**
>
> Results of `SHOW COLLATION` vary when the ["new collation framework"](/character-set-and-collation.md#new-framework-for-collations) is enabled. For new collation framework details, refer to [Character Set and Collation](/character-set-and-collation.md).

## Synopsis

```ebnf+diagram
ShowCollationStmt ::=
    "SHOW" "COLLATION" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Examples

<CustomContent platform="tidb">

When [the new collation framework](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) is enabled (the default), the example output is as follows:

</CustomContent>

```sql
SHOW COLLATION;
```

```
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 | PAD SPACE     |
| binary             | binary  |  63 | Yes     | Yes      |       1 | NO PAD        |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 | PAD SPACE     |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 | PAD SPACE     |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 | PAD SPACE     |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       8 | PAD SPACE     |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
13 rows in set (0.00 sec)
```

<CustomContent platform="tidb">

When the new collation framework is disabled, only binary collations are listed.

```sql
SHOW COLLATION;
```

```
+-------------+---------+----+---------+----------+---------+---------------+
| Collation   | Charset | Id | Default | Compiled | Sortlen | Pad_attribute |
+-------------+---------+----+---------+----------+---------+---------------+
| utf8mb4_bin | utf8mb4 | 46 | Yes     | Yes      |       1 | PAD SPACE     |
| latin1_bin  | latin1  | 47 | Yes     | Yes      |       1 | PAD SPACE     |
| binary      | binary  | 63 | Yes     | Yes      |       1 | NO PAD        |
| ascii_bin   | ascii   | 65 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_bin    | utf8    | 83 | Yes     | Yes      |       1 | PAD SPACE     |
| gbk_bin     | gbk     | 87 | Yes     | Yes      |       1 | PAD SPACE     |
+-------------+---------+----+---------+----------+---------+---------------+
6 rows in set (0.00 sec)
```

</CustomContent>

To filter on the character set, you can add a `WHERE` clause.

```sql
SHOW COLLATION WHERE Charset="utf8mb4";
```

```sql
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
5 rows in set (0.001 sec)
```

## MySQL compatibility

The usage of the `SHOW COLLATION` statement in TiDB is fully compatible with MySQL. However, charsets in TiDB might have different default collations compared with MySQL. For details, refer to [Compatibility with MySQL](/mysql-compatibility.md). If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [SHOW CHARACTER SET](/sql-statements/sql-statement-show-character-set.md)
* [Character Set and Collation](/character-set-and-collation.md)
