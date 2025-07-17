---
title: SHOW COLLATION | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 SHOW COLLATION 的概述。
---

# SHOW COLLATION

此语句提供了一个静态的字符集排序规则列表，旨在与 MySQL 客户端库保持兼容。

> **Note:**
>
> 当启用 ["new collation framework"](/character-set-and-collation.md#new-framework-for-collations) 时，`SHOW COLLATION` 的结果会有所不同。有关新字符集排序框架的详细信息，请参考 [Character Set and Collation](/character-set-and-collation.md)。

## 概要

```ebnf+diagram
ShowCollationStmt ::=
    "SHOW" "COLLATION" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

<CustomContent platform="tidb">

当 [启用新字符集排序框架](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)（默认设置）时，示例输出如下：

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
13 行结果（0.00 秒）
```

<CustomContent platform="tidb">

当禁用新字符集排序框架时，只列出二进制字符集。

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
6 行结果（0.00 秒）
```

</CustomContent>

可以通过添加 `WHERE` 子句来筛选字符集。

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
5 行结果（0.001 秒）
```

## MySQL 兼容性

TiDB 中 `SHOW COLLATION` 语句的用法与 MySQL 完全兼容。然而，TiDB 中的字符集可能与 MySQL 默认的排序规则不同。有关详细信息，请参考 [Compatibility with MySQL](/mysql-compatibility.md)。如果你发现任何兼容性差异，请 [report a bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [SHOW CHARACTER SET](/sql-statements/sql-statement-show-character-set.md)
* [Character Set and Collation](/character-set-and-collation.md)
