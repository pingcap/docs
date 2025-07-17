---
title: DO | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 DO 的概述。
---

# DO

`DO` 执行表达式，但不会返回任何结果。在大多数情况下，`DO` 等同于不返回结果的 `SELECT expr, ...`。

> **Note:**
>
> `DO` 仅执行表达式。它不能在所有可以使用 `SELECT` 的场景中使用。例如，`DO id FROM t1` 是无效的，因为它引用了表。

在 MySQL 中，一个常见的用例是执行存储过程或触发器。由于 TiDB 不提供存储过程或触发器，此功能的使用有限。

## 语法简介

```ebnf+diagram
DoStmt   ::= 'DO' ExpressionList

ExpressionList ::=
    Expression ( ',' Expression )*

Expression ::=
    ( singleAtIdentifier assignmentEq | 'NOT' | Expression ( logOr | 'XOR' | logAnd ) ) Expression
|   'MATCH' '(' ColumnNameList ')' 'AGAINST' '(' BitExpr FulltextSearchModifierOpt ')'
|   PredicateExpr ( IsOrNotOp 'NULL' | CompareOp ( ( singleAtIdentifier assignmentEq )? PredicateExpr | AnyOrAll SubSelect ) )* ( IsOrNotOp ( trueKwd | falseKwd | 'UNKNOWN' ) )?
```

## 示例

这个 SELECT 语句会暂停，但也会产生一个结果集。

```sql
mysql> SELECT SLEEP(5);
+----------+
| SLEEP(5) |
+----------+
|        0 |
+----------+
1 row in set (5.00 sec)
```

而 `DO`，则会暂停但不会产生结果集。

```sql
mysql> DO SLEEP(5);
Query OK, 0 rows affected (5.00 sec)

mysql> DO SLEEP(1), SLEEP(1.5);
Query OK, 0 rows affected (2.50 sec)
```

## MySQL 兼容性

TiDB 中的 `DO` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## 相关链接

* [SELECT](/sql-statements/sql-statement-select.md)