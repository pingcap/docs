---
title: Cast Functions and Operators
summary: Learn about the cast functions and operators.
aliases: ['/docs/dev/functions-and-operators/cast-functions-and-operators/','/docs/dev/reference/sql/functions-and-operators/cast-functions-and-operators/']
---

# Cast Functions and Operators

Cast functions and operators enable conversion of values from one data type to another. TiDB supports all of the [cast functions and operators](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html) available in MySQL 8.0.

| Name                                     | Description                      |
| ---------------------------------------- | -------------------------------- |
| [`BINARY`](#binary) | Cast a string to a binary string |
| [`CAST()`](#cast) | Cast a value as a certain type   |
| [`CONVERT()`](#convert) | Cast a value as a certain type   |

> **Note:**
>
> TiDB and MySQL display inconsistent results for `SELECT CAST(MeN AS CHAR)` (or its equivalent form `SELECT CONVERT(MeM, CHAR)`), where `MeN` represents a double-precision floating-point number in scientific notation. MySQL displays the complete numeric value when `-15 <= N <= 14` and the scientific notation when `N < -15` or `N > 14`. However, TiDB always displays the complete numeric value. For example, MySQL displays the result of `SELECT CAST(3.1415e15 AS CHAR)` as `3.1415e15`, while TiDB displays the result as `3141500000000000`.

## BINARY

The [`BINARY`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary) operator has been deprecated since MySQL 8.0.27. It is recommended to use `CAST(... AS BINARY)` instead both in TiDB and MySQL.

## CAST

The [`CAST()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast) function is used to cast an expression to a specific type.

This function is also used to create [Multi-valued indexes](/sql-statements/sql-statement-create-index.md#multi-valued-indexes).

Example:

```sql
SELECT CAST(0x54694442 AS CHAR);
```

```
+--------------------------+
| CAST(0x54694442 AS CHAR) |
+--------------------------+
| TiDB                     |
+--------------------------+
1 row in set (0.0002 sec)
```

## CONVERT

The [`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) function is used to convert between [character sets](/character-set-and-collation.md).

Example:

```sql
SELECT CONVERT(0x616263 USING utf8mb4);
```

```
+---------------------------------+
| CONVERT(0x616263 USING utf8mb4) |
+---------------------------------+
| abc                             |
+---------------------------------+
1 row in set (0.0004 sec)
```

# MySQL compatibility

- TiDB does not support cast operations on spatial types. For more information, see [#6347](https://github.com/pingcap/tidb/issues/6347).
- TiDB does not support `AT TIME ZONE` for `CAST()`. For more information, see [#51742](https://github.com/pingcap/tidb/issues/51742).
- `CAST(24 AS YEAR)` returns 2 digits in TiDB and 4 digits in MySQL. For more information, see [#29629](https://github.com/pingcap/tidb/issues/29629).
