---
title: TiDB Data Type
summary: Learn about the data types supported in TiDB.
category: reference
---

# Numeric types

### Overview

TiDB supports all the MySQL numeric types, including:

+ Integer Types (Exact Value)
+ Floating-Point Types (Approximate Value)
+ Fixed-Point Types (Exact Value)

### Integer types (exact value)

TiDB supports all the MySQL integer types, including INTEGER/INT, TINYINT, SMALLINT, MEDIUMINT, and BIGINT. For more information, see [Numeric Type Overview in MySQL](https://dev.mysql.com/doc/refman/5.7/en/numeric-type-overview.html).

#### Type definition

Syntax:

```sql
BIT[(M)]
> The BIT data type. A type of BIT(M) enables storage of M-bit values. M can range from 1 to 64.

TINYINT[(M)] [UNSIGNED] [ZEROFILL]
> The TINYINT data type. The value range for signed: [-128, 127] and the range for unsigned is [0, 255].

BOOL, BOOLEAN
> BOOLEAN and is equivalent to TINYINT(1). If the value is "0", it is considered as False; otherwise, it is considered True. In TiDB, True is "1" and False is "0".


SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
> SMALLINT. The signed range is: [-32768, 32767], and the unsigned range is [0, 65535].

MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
> MEDIUMINT. The signed range is: [-8388608, 8388607], and the unsigned range is [0, 16777215].

INT[(M)] [UNSIGNED] [ZEROFILL]
> INT. The signed range is: [-2147483648, 2147483647], and the unsigned range is [0, 4294967295].

INTEGER[(M)] [UNSIGNED] [ZEROFILL]
> Same as INT.

BIGINT[(M)] [UNSIGNED] [ZEROFILL]
> BIGINT. The signed range is: [-9223372036854775808, 9223372036854775807], and the unsigned range is [0, 18446744073709551615].
```

The meaning of the fields:

| Syntax Element | Description |
| -------- | ------------------------------- |
| M | the display width of the type. Optional. |
| UNSIGNED | UNSIGNED. If omitted, it is SIGNED. |
| ZEROFILL | If you specify ZEROFILL for a numeric column, TiDB automatically adds the UNSIGNED attribute to the column. |

#### Storage and range

See the following for the requirements of the storage and minimum value/maximim value of each data type:

| Type | Storage Required (bytes) | Minimum Value (Signed/Unsigned) | Maximum Value (Signed/Unsigned) |
| ----------- |----------|-----------------------| --------------------- |
| `TINYINT` | 1 | -128 / 0 | 127 / 255 |
| `SMALLINT` | 2 | -32768 / 0 | 32767 / 65535 |
| `MEDIUMINT` | 3 | -8388608 / 0 | 8388607 / 16777215 |
| `INT` | 4 | -2147483648 / 0 | 2147483647 / 4294967295 |
| `BIGINT` | 8 | -9223372036854775808 / 0 | 9223372036854775807 / 18446744073709551615 |

### Floating-point types (approximate value)

TiDB supports all the MySQL floating-point types, including FLOAT, and DOUBLE. For more information, [Floating-Point Types (Approximate Value) - FLOAT, DOUBLE in MySQL](https://dev.mysql.com/doc/refman/5.7/en/floating-point-types.html).

#### Type definition

Syntax:

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
> A small (single-precision) floating-point number. Permissible values are -3.402823466E+38 to -1.175494351E-38, 0, and 1.175494351E-38 to 3.402823466E+38. These are the theoretical limits, based on the IEEE standard. The actual range might be slightly smaller depending on your hardware or operating system.

DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
> A normal-size (double-precision) floating-point number. Permissible values are -1.7976931348623157E+308 to -2.2250738585072014E-308, 0, and 2.2250738585072014E-308 to 1.7976931348623157E+308. These are the theoretical limits, based on the IEEE standard. The actual range might be slightly smaller depending on your hardware or operating system.
 
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
> Synonym for DOUBLE.

FLOAT(p) [UNSIGNED] [ZEROFILL]
> A floating-point number. p represents the precision in bits, but TiDB uses this value only to determine whether to use FLOAT or DOUBLE for the resulting data type. If p is from 0 to 24, the data type becomes FLOAT with no M or D values. If p is from 25 to 53, the data type becomes DOUBLE with no M or D values. The range of the resulting column is the same as for the single-precision FLOAT or double-precision DOUBLE data types described earlier in this section.
```

The meaning of the fields:

| Syntax Element | Description |
| -------- | ------------------------------- |
| M | the total number of digits |
| D | the number of digits following the decimal point |
| UNSIGNED | UNSIGNED. If omitted, it is SIGNED. |
| ZEROFILL | If you specify ZEROFILL for a numeric column, TiDB automatically adds the UNSIGNED attribute to the column. |

#### Storage

See the following for the requirements of the storage:

| Data Type | Storage Required (bytes)|
| ----------- |----------|
| `FLOAT` | 4 |
| `FLOAT(p)` | If 0 <= p <= 24, it is 4; if 25 <= p <= 53, it is 8|
| `DOUBLE` | 8 |


### Fixed-point types (exact value)

TiDB supports all the MySQL floating-point types, including DECIMAL, and NUMERIC. For more information, [Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC in MySQL](https://dev.mysql.com/doc/refman/5.7/en/fixed-point-types.html).

#### Type definition

Syntax

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
> A packed “exact” fixed-point number. M is the total number of digits (the precision), and D is the number of digits after the decimal point (the scale). The decimal point and (for negative numbers) the - sign are not counted in M. If D is 0, values have no decimal point or fractional part. The maximum number of digits (M) for DECIMAL is 65. The maximum number of supported decimals (D) is 30. If D is omitted, the default is 0. If M is omitted, the default is 10.

NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
> Synonym for DECIMAL.
```

The meaning of the fields:

| Syntax Element | Description |
| -------- | ------------------------------- |
| M | the total number of digits |
| D | the number of digits after the decimal point |
| UNSIGNED | UNSIGNED. If omitted, it is SIGNED. |
| ZEROFILL | If you specify ZEROFILL for a numeric column, TiDB automatically adds the UNSIGNED attribute to the column. |

