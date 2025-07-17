---
title: 数值类型
summary: 了解 TiDB 支持的数值数据类型。
---

# 数值类型

TiDB 支持所有 MySQL 数值类型，包括：

+ [整数类型](#integer-types)（精确值）
+ [浮点类型](#floating-point-types)（近似值）
+ [定点类型](#fixed-point-types)（精确值）

## 整数类型

TiDB 支持所有 MySQL 整数类型，包括 `INTEGER` / `INT`、`TINYINT`、`SMALLINT`、`MEDIUMINT` 和 `BIGINT`。更多信息请参见 [MySQL 中的整数数据类型语法](https://dev.mysql.com/doc/refman/8.0/en/integer-types.html)。

下表总结了字段描述：

<CustomContent platform="tidb">

> **Warning:**
>
> 从 v8.5.0 版本开始，整数显示宽度已被弃用（[`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length) 默认为 `true`）。不建议为整数类型指定显示宽度。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Warning:**
>
> 从 v8.5.0 版本开始，整数显示宽度已被弃用。不建议为整数类型指定显示宽度。

</CustomContent>

| 语法元素 | 描述 |
| -------- | ------------------------------- |
| M | 类型的显示宽度。可选。 |
| UNSIGNED | UNSIGNED。如果省略，则为 SIGNED。 |
| ZEROFILL | 如果为数字列指定 ZEROFILL，TiDB 会自动为该列添加 UNSIGNED 属性。 |

下表总结了 TiDB 支持的整数类型所需的存储空间和范围：

| 数据类型 | 所需存储空间（字节） | 最小值（有符号/无符号） | 最大值（有符号/无符号） |
| ------- | -------- | ----------- | ------------ |
| `TINYINT` | 1 | -128 / 0 | 127 / 255 |
| `SMALLINT` | 2 | -32768 / 0 | 32767 / 65535 |
| `MEDIUMINT` | 3 | -8388608 / 0 | 8388607 / 16777215 |
| `INT` | 4 | -2147483648 / 0 | 2147483647 / 4294967295 |
| `BIGINT` | 8 | -9223372036854775808 / 0 | 9223372036854775807 / 18446744073709551615 |

### `BIT` 类型

BIT 数据类型。类型为 BIT(M) 时，可以存储 M 位值。M 的取值范围为 1 到 64，默认值为 1：

```sql
BIT[(M)]
```

### `BOOLEAN` 类型

`BOOLEAN` 类型及其别名 `BOOL` 等价于 `TINYINT(1)`。如果值为 `0`，则视为 `False`；否则视为 `True`。与 MySQL 一样，`True` 为 `1`，`False` 为 `0`：

```sql
BOOLEAN
```

### `TINYINT` 类型

`TINYINT` 数据类型存储范围为有符号的 [-128, 127] 和无符号的 [0, 255]：

```sql
TINYINT[(M)] [UNSIGNED] [ZEROFILL]
```

### `SMALLINT` 类型

`SMALLINT` 数据类型存储范围为有符号的 [-32768, 32767] 和无符号的 [0, 65535]：

```sql
SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
```

### `MEDIUMINT` 类型

`MEDIUMINT` 数据类型存储范围为有符号的 [-8388608, 8388607] 和无符号的 [0, 16777215]：

```sql
MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
```

### `INTEGER` 类型

`INTEGER` 及其别名 `INT` 存储范围为有符号的 [-2147483648, 2147483647] 和无符号的 [0, 4294967295]：

```sql
INT[(M)] [UNSIGNED] [ZEROFILL]
```

也可以使用另一种形式：

```sql
INTEGER[(M)] [UNSIGNED] [ZEROFILL]
```

### `BIGINT` 类型

`BIGINT` 数据类型存储范围为有符号的 [-9223372036854775808, 9223372036854775807] 和无符号的 [0, 18446744073709551615]：

```sql
BIGINT[(M)] [UNSIGNED] [ZEROFILL]
```

## 浮点类型

TiDB 支持所有 MySQL 浮点类型，包括 `FLOAT` 和 `DOUBLE`。更多信息请参见 [Floating-Point Types (Approximate Value) - FLOAT, DOUBLE in MySQL](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)。

下表总结了字段描述：

| 语法元素 | 描述 |
| -------- | ------------------------------- |
| M | 数字的总位数 |
| D | 小数点后数字的位数 |
| UNSIGNED | UNSIGNED。如果省略，则为 SIGNED。 |
| ZEROFILL | 如果为数字列指定 ZEROFILL，TiDB 会自动为该列添加 UNSIGNED 属性。 |

下表总结了 TiDB 支持的浮点类型所需的存储空间：

| 数据类型 | 所需存储空间（字节）|
| ----------- |----------|
| `FLOAT` | 4 |
| `FLOAT(p)` | 如果 0 <= p <= 24，则为 4；如果 25 <= p <= 53，则为 8 |
| `DOUBLE` | 8 |

### `FLOAT` 类型

`FLOAT` 类型存储单精度浮点数。允许的值范围为 -3.402823466E+38 到 -1.175494351E-38，0，以及 1.175494351E-38 到 3.402823466E+38。这些是基于 IEEE 标准的理论极限。实际范围可能会因硬件或操作系统的不同而略小。

`FLOAT(p)` 可用来表示所需的精度（以位为单位）。TiDB 仅用此值来决定使用 `FLOAT` 还是 `DOUBLE` 作为结果数据类型。如果 p 在 0 到 24 之间，数据类型为没有 M 和 D 的 `FLOAT`；如果 p 在 25 到 53 之间，数据类型为没有 M 和 D 的 `DOUBLE`。结果列的范围与单精度 `FLOAT` 或双精度 `DOUBLE` 类型相同。

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
FLOAT(p) [UNSIGNED] [ZEROFILL]
```

> **Note:**
>
> 与 MySQL 一样，`FLOAT` 数据类型存储近似值。对于货币等值，建议使用 `DECIMAL` 类型。
>
> 在 TiDB 中，`FLOAT` 数据类型的默认精度为 8 位，而在 MySQL 中，默认精度为 6 位。例如，假设你在 TiDB 和 MySQL 中的 `FLOAT` 类型列插入 `123456789` 和 `1.23456789`，在查询对应值时，MySQL 返回 `123457000` 和 `1.23457`，而 TiDB 返回 `123456790` 和 `1.2345679`。

### `DOUBLE` 类型

`DOUBLE` 及其别名 `DOUBLE PRECISION` 存储双精度浮点数。允许的值范围为 -1.7976931348623157E+308 到 -2.2250738585072014E-308，0，以及 2.2250738585072014E-308 到 1.7976931348623157E+308。这些是基于 IEEE 标准的理论极限。实际范围可能会因硬件或操作系统的不同而略小。

```sql
DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
```

> **Warning:**
>
> 与 MySQL 一样，`DOUBLE` 数据类型存储近似值。对于货币等值，建议使用 `DECIMAL` 类型。

> **Note:**
>
> 当 TiDB 将科学计数法表示的双精度浮点数转换为 `CHAR` 类型时，显示结果与 MySQL 不一致。详情请参见 [Cast functions and operators](/functions-and-operators/cast-functions-and-operators.md)。

## 定点类型

TiDB 支持所有 MySQL 浮点类型，包括 `DECIMAL` 和 `NUMERIC`。更多信息请参见 [Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC in MySQL](https://dev.mysql.com/doc/refman/8.0/en/fixed-point-types.html)。

字段含义如下：

| 语法元素 | 描述 |
| -------- | ------------------------------- |
| M | 十进制数字的总位数 |
| D | 小数点后数字的位数 |
| UNSIGNED | UNSIGNED。如果省略，则为 SIGNED。 |
| ZEROFILL | 如果为数字列指定 ZEROFILL，TiDB 会自动为该列添加 UNSIGNED 属性。 |

### `DECIMAL` 类型

`DECIMAL` 及其别名 `NUMERIC` 存储打包的“精确”定点数。M 表示十进制数字的总位数（精度），D 表示小数点后数字的位数（标度）。小数点和（负数时的）负号不计入 M。如果 D 为 0，则值没有小数点或小数部分。DECIMAL 支持的最大数字位数（M）为 65，最大支持的小数位数（D）为 30。如果省略 D，默认为 0；如果省略 M，默认为 10。

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
```