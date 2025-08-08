---
title: Function and Operator Reference
summary: 関数と演算子の使い方を学びます。
---

# 関数と演算子のリファレンス {#function-and-operator-reference}

TiDBの関数と演算子の使い方はMySQLと似ています。1 [MySQLの関数と演算子](https://dev.mysql.com/doc/refman/8.0/en/functions.html)参照してください。

SQL 文では、 [`SELECT`](/sql-statements/sql-statement-select.md)文の`ORDER BY`と`HAVING`節、 [`SELECT`](/sql-statements/sql-statement-select.md) / [`DELETE`](/sql-statements/sql-statement-delete.md) / [`UPDATE`](/sql-statements/sql-statement-update.md)文の`WHERE`節、 [`SET`](/sql-statements/sql-statement-set-variable.md)文で式を使用できます。

リテラル、列名、 `NULL` 、組み込み関数、演算子などを使用して式を記述できます。

-   TiDB が TiKV へのプッシュダウンをサポートする式については、 [プッシュダウンの式のリスト](/functions-and-operators/expressions-pushed-down.md)参照してください。
-   TiDB が[TiFlash](/tiflash/tiflash-overview.md)へのプッシュダウンをサポートする式については、 [プッシュダウン式](/tiflash/tiflash-supported-pushdown-calculations.md#push-down-expressions)参照してください。
