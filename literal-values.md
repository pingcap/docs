---
title: Literal Values
summary: 本文介绍 TiDB SQL 语句中的字面值。
---

# Literal Values

TiDB 字面值包括字符字面值、数字字面值、时间和日期字面值、十六进制字面值、二进制字面值，以及 NULL 字面值。本文介绍这些字面值的用法。

本文描述字符串字面值、数字字面值、NULL 值、十六进制字面值、日期和时间字面值、布尔字面值以及位值字面值。

## String literals

字符串是由字节或字符组成的序列，括在单引号 `'` 或双引号 `"` 中。例如：

```
'example string'
"example string"
```

相邻的引号括起的字符串会连接成一个字符串。以下几行是等价的：

```
'a string'
'a' ' ' 'string'
"a" ' ' "string"
```

如果启用了 `ANSI_QUOTES` SQL MODE，则字符串字面值只能用单引号括起来，因为用双引号括起来的字符串会被解释为标识符。

字符串分为以下两类：

+ Binary string：由字节序列组成，字符集和排序规则均为 `binary`，在比较时以 **字节** 为单位。
+ Non-binary string：由字符序列组成，具有除 `binary` 之外的多种字符集和排序规则。在比较时以 **字符** 为单位。字符可能包含多个字节，取决于字符集。

字符串字面值可以有可选的 `character set introducer` 和 `COLLATE` 子句，用于指定使用特定字符集和排序规则的字符串。

```
[_charset_name]'string' [COLLATE collation_name]
```

例如：

```
SELECT _latin1'string';
SELECT _binary'string';
SELECT _utf8'string' COLLATE utf8_bin;
```

你可以使用 `N'literal'`（或 `n'literal'`）来创建使用国家字符集的字符串。以下语句等价：

```
SELECT N'some text';
SELECT n'some text';
SELECT _utf8'some text';
```

要在字符串中表示特殊字符，可以使用转义字符进行转义：

| 转义字符 | 含义 |
| :---------------- | :------ |
| \\0 | ASCII NUL（X'00'）字符 |
| \\' | 单引号 `'` 字符 |
| \\" | 双引号 `"` 字符 |
| \\b | 退格字符 |
| \\n | 换行符（换行）字符 |
| \\r | 回车字符 |
| \\t | 制表符 |
| \\z | ASCII 26（Ctrl + Z） |
| \\\\ | 反斜杠 `\` 字符 |
| \\% | `%` 字符 |
| \\_ | `_` 字符 |

如果要在用 `'` 包围的字符串中表示 `"`，或在用 `"` 包围的字符串中表示 `'`，则无需使用转义字符。

更多信息请参见 [String Literals in MySQL](https://dev.mysql.com/doc/refman/8.0/en/string-literals.html)。

## Numeric literals

数字字面值包括整数和 DECIMAL 字面值，以及浮点字面值。

整数可以包含 `.` 作为小数点。数字前可以有 `-` 或 `+` 表示负值或正值。

精确值数字字面值可以表示为 `1, .2, 3.4, -5, -6.78, +9.10`。

数字字面值也可以用科学计数法表示，例如 `1.2E3, 1.2E-3, -1.2E3, -1.2E-3`。

更多信息请参见 [Numeric Literals in MySQL](https://dev.mysql.com/doc/refman/8.0/en/number-literals.html)。

## Date and time literals

日期和时间字面值可以用多种格式表示，例如用引号括起来的字符串或数字。当 TiDB 期望是日期时，任何 `'2017-08-24'`、`'20170824'` 和 `20170824` 都会被解释为日期。

TiDB 支持以下日期格式：

* `'YYYY-MM-DD'` 或 `'YY-MM-DD'`：这里的 `-` 分隔符不严格，可以是任何标点。例如，`'2017-08-24'`、`'2017&08&24'`、`'2012@12^31'` 都是有效的日期格式。唯一特殊的标点是 `.`，被视为小数点，用于分隔整数和小数部分。日期和时间可以用 `T` 或空格分隔。例如，`2017-8-24 10:42:00` 和 `2017-8-24T10:42:00` 表示相同的日期和时间。
* `'YYYYMMDDHHMMSS'` 或 `'YYMMDDHHMMSS'`：例如，`'20170824104520'` 和 `'170824104520'` 被视为 `'2017-08-24 10:45:20'`。但如果提供超出范围的值，例如 `'170824304520'`，则不被视为有效日期。注意，格式错误的如 `YYYYMMDD HHMMSS`、`YYYYMMDD HH:MM:DD` 或 `YYYY-MM-DD HHMMSS` 会插入失败。
* `YYYYMMDDHHMMSS` 或 `YYMMDDHHMMSS`：注意这些格式没有单引号或双引号，而是数字。例如，`20170824104520` 被解释为 `'2017-08-24 10:45:20'`。

DATETIME 或 TIMESTAMP 值可以后跟小数部分，用于表示微秒精度（6 位数字）。小数部分应始终用小数点 `.` 与时间的其余部分隔开。

仅含两位数字的年份值是模糊的，建议使用四位年份格式。TiDB 根据以下规则解释两位年份：

* 如果年份在 `70-99` 之间，则转换为 `1970-1999`。
* 如果年份在 `00-69` 之间，则转换为 `2000-2069`。

月份或日期值小于 10 时，`'2017-8-4'` 与 `'2017-08-04'` 相同。时间也是如此。例如，`'2017-08-24 1:2:3'` 与 `'2017-08-24 01:02:03'` 相同。

当需要日期或时间值时，TiDB 根据值的长度选择指定的格式：

* 6 位数字：`YYMMDD`。
* 12 位数字：`YYMMDDHHMMSS`。
* 8 位数字：`YYYYMMDD`。
* 14 位数字：`YYYYMMDDHHMMSS`。

TiDB 支持以下时间值格式：

* `'D HH:MM:SS'`，或 `'HH:MM:SS'`、`'HH:MM'`、`'D HH:MM'`、`'D HH'`、`'SS'`：`D` 表示天，取值范围为 `0-34`。
* 以 `HHMMSS` 格式的数字：例如，`231010` 被解释为 `'23:10:10'`。
* 任何 `SS`、`MMSS` 和 `HHMMSS` 格式的数字都可以视为时间。

Time 类型的小数点也为 `.`，精度最高可达 6 位。

更多细节请参见 [MySQL date and time literals](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-literals.html)。

## Boolean Literals

常量 `TRUE` 和 `FALSE` 分别等于 1 和 0，且不区分大小写。

```sql
SELECT TRUE, true, tRuE, FALSE, FaLsE, false;
```

```
+------+------+------+-------+-------+-------+
| TRUE | true | tRuE | FALSE | FaLsE | false |
+------+------+------+-------+-------+-------+
|    1 |    1 |    1 |     0 |     0 |     0 |
+------+------+------+-------+-------+-------+
1 row in set (0.00 sec)
```

## Hexadecimal literals

十六进制字面值用 `X'val'` 或 `0xval` 表示，其中 `val` 包含十六进制数字。前导 `0x` 区分大小写，不能写成 `0X`。

合法的十六进制字面值：

```
X'ac12'
X'12AC'
x'ac12'
x'12AC'
0xac12
0x12AC
```

非法的十六进制字面值：

```
X'1z'（z 不是合法的十六进制数字）
0X12AC（0X 必须写成 0x）
```

用 `X'val'` 方式写的十六进制字面值必须包含偶数个数字。如果 `val` 长度为奇数（例如，`X'A'` 或 `X'11A'`），为了避免语法错误，应在前面补零：

```sql
mysql> select X'aff';
ERROR 1105 (HY000): line 0 column 13 near ""hex literal: invalid hexadecimal format, must even numbers, but 3 (total length 13)
mysql> select X'0aff';
+---------+
| X'0aff' |
+---------+
| 0x0aff  |
+---------+
1 row in set (0.00 sec)
```

默认情况下，十六进制字面值是二进制字符串。

要将字符串或数字转换为十六进制字符串，可以使用 `HEX()` 函数：

```sql
mysql> SELECT HEX('TiDB');
+-------------+
| HEX('TiDB') |
+-------------+
| 54694442    |
+-------------+
1 row in set (0.01 sec)

mysql> SELECT X'54694442';
+-------------+
| X'54694442' |
+-------------+
| TiDB        |
+-------------+
1 row in set (0.00 sec)
```

## Bit-value literals

位值字面值用 `b'val'` 或 `0bval` 表示。`val` 是由零和一组成的二进制值。前导 `0b` 区分大小写，不能写成 `0B`。

合法的位值字面值：

```
b'01'
B'01'
0b01
```

非法的位值字面值：

```
b'2'（2 不是二进制数字，必须是 0 或 1）
0B01（0B 必须写成 0b）
```

默认情况下，位值字面值是二进制字符串。

位值以二进制形式返回，可能在 MySQL 客户端显示不佳。可以用 `BIN()` 或 `HEX()` 等转换函数将位值转换为可打印的形式。

```sql
CREATE TABLE t (b BIT(8));
INSERT INTO t SET b = b'00010011';
INSERT INTO t SET b = b'1110';
INSERT INTO t SET b = b'100101';

mysql> SELECT b+0, BIN(b), HEX(b) FROM t;
+------+--------+--------+
| b+0  | BIN(b) | HEX(b) |
+------+--------+--------+
|   19 | 10011  | 13     |
|   14 | 1110   | E      |
|   37 | 100101 | 25     |
+------+--------+--------+
3 rows in set (0.00 sec)
```

## NULL Values

`NULL` 表示数据为空，不区分大小写，也等同于 `\N`（区分大小写）。

> **Note:**
>
> `NULL` 不等于 `0`，也不等于空字符串 `''`。