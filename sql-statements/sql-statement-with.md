---
title: WITH | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 WITH (Common Table Expression) 的概述。
---

# WITH

Common Table Expression (CTE) 是一个临时结果集，可以在 SQL 语句中多次引用，以提高语句的可读性和执行效率。你可以应用 `WITH` 语句来使用 Common Table Expressions。

## 概述

**WithClause:**

```ebnf+diagram
WithClause ::=
        "WITH" WithList
|       "WITH" "RECURSIVE" WithList
```

**WithList:**

```ebnf+diagram
WithList ::=
        WithList ',' CommonTableExpr
|       CommonTableExpr
```

**CommonTableExpr:**

```ebnf+diagram
CommonTableExpr ::=
        Identifier IdentListWithParenOpt "AS" SubSelect
```

**IdentListWithParenOpt:**

```ebnf+diagram
IdentListWithParenOpt ::=
( '(' IdentList ')' )?
```

## 示例

非递归 CTE：

```sql
WITH cte AS (SELECT 1, 2) SELECT * FROM cte t1, cte t2;
```

```
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
1 row in set (0.00 sec)
```

递归 CTE：

```sql
WITH RECURSIVE cte(a) AS (SELECT 1 UNION SELECT a+1 FROM cte WHERE a < 5) SELECT * FROM cte;
```

```
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)
```

## MySQL 兼容性

* 在严格模式下，当递归计算的数据长度超过种子部分的数据长度时，TiDB 会返回警告，而 MySQL 会返回错误。在非严格模式下，TiDB 的行为与 MySQL 一致。
* 递归 CTE 的数据类型由种子部分决定。在某些情况下（如函数），种子部分的数据类型与 MySQL 不完全一致。
* 在多个 `UNION` / `UNION ALL` 操作符的情况下，MySQL 不允许 `UNION` 后面跟 `UNION ALL`，而 TiDB 支持。
* 如果 CTE 的定义存在问题，TiDB 会报错，而如果 CTE 未被引用，MySQL 不会报错。

## 相关链接

* [Developer Guide: Common Table Expression](/develop/dev-guide-use-common-table-expression.md)
* [SELECT](/sql-statements/sql-statement-select.md)
* [INSERT](/sql-statements/sql-statement-insert.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [UPDATE](/sql-statements/sql-statement-update.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)