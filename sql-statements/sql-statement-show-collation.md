---
title: SHOW COLLATION | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW COLLATION for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-collation/','/docs/dev/reference/sql/statements/show-collation/']
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

When the [new collation framework](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#new_collations_enabled_on_first_bootstrap) is enabled, in addition to the binary collations, TiDB also supports the following collations:

- Seven case- and accent-insensitive collations, ending with `_ci`
- `utf8mb4_0900_bin`

```sql
SHOW COLLATION;
```

```
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 | PAD SPACE     |
| binary             | binary  |  63 | Yes     | Yes      |       1 | NO PAD        |
| gb18030_bin        | gb18030 | 249 |         | Yes      |       1 | PAD SPACE     |
| gb18030_chinese_ci | gb18030 | 248 | Yes     | Yes      |       1 | PAD SPACE     |
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
15 rows in set (0.000 sec)
```

If [the new collation framework](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#new_collations_enabled_on_first_bootstrap) is disabled, TiDB supports only binary collations.

```sql
SHOW COLLATION;
```

```
+-------------+---------+-----+---------+----------+---------+---------------+
| Collation   | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+-------------+---------+-----+---------+----------+---------+---------------+
| utf8mb4_bin | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| latin1_bin  | latin1  |  47 | Yes     | Yes      |       1 | PAD SPACE     |
| binary      | binary  |  63 | Yes     | Yes      |       1 | NO PAD        |
| ascii_bin   | ascii   |  65 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_bin    | utf8    |  83 | Yes     | Yes      |       1 | PAD SPACE     |
| gbk_bin     | gbk     |  87 | Yes     | Yes      |       1 | PAD SPACE     |
| gb18030_bin | gb18030 | 249 | Yes     | Yes      |       1 | PAD SPACE     |
+-------------+---------+-----+---------+----------+---------+---------------+
7 rows in set (0.00 sec)
```

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
