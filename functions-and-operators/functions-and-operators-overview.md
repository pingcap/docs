---
title: Function and Operator Reference
summary: Learn how to use the functions and operators.
---

# Function and Operator Reference

TiDB 中函数和操作符的用法与 MySQL 类似。请参阅 [Functions and Operators in MySQL](https://dev.mysql.com/doc/refman/8.0/en/functions.html)。

在 SQL 语句中，表达式可以在 [`SELECT`](/sql-statements/sql-statement-select.md) 语句的 [`ORDER BY`] 和 [`HAVING`] 子句中使用，也可以在 [`SELECT`](/sql-statements/sql-statement-select.md)、[`DELETE`](/sql-statements/sql-statement-delete.md)、[`UPDATE`](/sql-statements/sql-statement-update.md) 语句的 `WHERE` 子句，以及 [`SET`](/sql-statements/sql-statement-set-variable.md) 语句中使用。

你可以使用字面量、列名、`NULL`、内置函数、操作符等来编写表达式。

- 关于 TiDB 支持下推到 TiKV 的表达式，请参阅 [List of expressions for pushdown](/functions-and-operators/expressions-pushed-down.md)。 
- 关于 TiDB 支持下推到 [TiFlash](/tiflash/tiflash-overview.md) 的表达式，请参阅 [Push-down expressions](/tiflash/tiflash-supported-pushdown-calculations.md#push-down-expressions)。