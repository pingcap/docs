---
title: Function and Operator Reference
summary: Learn how to use the functions and operators.
---

# Function and Operator Reference

The usage of the functions and operators in TiDB is similar to MySQL. See [Functions and Operators in MySQL](https://dev.mysql.com/doc/refman/8.0/en/functions.html).

In SQL statements, expressions can be used on the `ORDER BY` and `HAVING` clauses of the [`SELECT`](/sql-statements/sql-statement-select.md) statement, the `WHERE` clause of [`SELECT`](/sql-statements/sql-statement-select.md)/[`DELETE`](/sql-statements/sql-statement-delete.md)/[`UPDATE`](/sql-statements/sql-statement-update.md) statements, and [`SET`](/sql-statements/sql-statement-set-variable.md) statements.

You can write expressions using literals, column names, `NULL`, built-in functions, operators, and so on. 

- For expressions that TiDB supports pushing down to TiKV, see [List of expressions for pushdown](/functions-and-operators/expressions-pushed-down.md). 
- For expressions that TiDB supports pushing down to [TiFlash](/tiflash/tiflash-overview.md), see [Push-down expressions](/tiflash/tiflash-supported-pushdown-calculations.md#push-down-expressions).
