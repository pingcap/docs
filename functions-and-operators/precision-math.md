---
title: Precision Math
summary: 了解 TiDB 中的精确数学支持。
---

# Precision Math

TiDB 中的精确数学支持与 MySQL 一致。更多信息请参见 [Precision Math in MySQL](https://dev.mysql.com/doc/refman/8.0/en/precision-math.html)。

## Numeric types

用于精确值操作的精确数学范围包括精确值数据类型（整数和 DECIMAL 类型）以及精确值数字字面量。近似值数据类型和数字字面量作为浮点数处理。

精确值数字字面量具有整数部分或小数部分，或两者皆有。它们可以带符号。示例：`1`、`.2`、`3.4`、`-5`、`-6.78`、`+9.10`。

近似值数字字面量以科学计数法（以 10 为底的幂）表示，包含尾数和指数。两部分或其中一部分可以带符号。示例：`1.2E3`、`1.2E-3`、`-1.2E3`、`-1.2E-3`。

两个看似相似的数字可能会被不同处理。例如，`2.34` 是一个精确值（定点）数字，而 `2.34E0` 是一个近似值（浮点）数字。

DECIMAL 数据类型是固定点类型，计算结果是精确的。FLOAT 和 DOUBLE 数据类型是浮点类型，计算结果是近似的。

## DECIMAL data type characteristics

本节讨论 DECIMAL 数据类型（及其同义词）的以下特性：

- 最大位数
- 存储格式
- 存储需求

DECIMAL 列的声明语法为 `DECIMAL(M,D)`。参数的取值范围如下：

- M 是最大位数（精度）。1 <= M <= 65。
- D 是小数点右侧的位数（刻度）。1 <= D <= 30，且 D 不能大于 M。

M 最大值为 65，意味着对 DECIMAL 值的计算精度最高为 65 位数字。这个 65 位的限制也适用于精确值数字字面量。

DECIMAL 列的值采用二进制格式存储，将 9 个十进制数字打包成 4 字节。每个值的整数部分和小数部分的存储需求分别确定。每 9 位数字需要 4 字节，剩余的数字则根据下表所示占用部分字节。

| 剩余数字 | 字节数 |
| --- | --- |
| 0   | 0 |
| 1–2 | 1 |
| 3–4 | 2 |
| 5–6 | 3 |
| 7–9 | 4 |

例如，`DECIMAL(18,9)` 列在小数点两边各有 9 位数字，因此整数部分和小数部分各需要 4 字节。`DECIMAL(20,6)` 列有 14 个整数位和 6 个小数位。整数部分的 9 位数字需要 4 字节，剩余的 5 位数字需要 3 字节。6 个小数位需要 3 字节。

DECIMAL 列不存储前导 `+` 字符或 `-` 字符，也不存储前导的 `0` 数字。如果你在 `DECIMAL(5,1)` 列中插入 `+0003.1`，存储时会变成 `3.1`。对于负数，不会存储字面量中的 `-` 字符。

DECIMAL 列不允许存储超出列定义范围的值。例如，`DECIMAL(3,0)` 列支持的范围是 `-999` 到 `999`。`DECIMAL(M,D)` 列最多允许在小数点左侧有 `M - D` 位数字。

关于 DECIMAL 值的内部格式的更多信息，请参见 TiDB 源码中的 [`mydecimal.go`](https://github.com/pingcap/tidb/blob/release-8.5/pkg/types/mydecimal.go)。

## Expression handling

对于带有精确数学的表达式，TiDB 在可能的情况下使用原始的精确值数字。例如，在比较中使用的数字会原样使用，不会改变值。在严格 SQL 模式下，如果你将精确数据类型插入到列中，数字会以其精确值插入（如果在列范围内）。检索时，值与插入时相同。如果未启用严格 SQL 模式，TiDB 允许在 INSERT 时进行截断。

如何处理数字表达式取决于表达式的值：

- 如果表达式包含任何近似值，结果为近似值。TiDB 使用浮点运算评估表达式。
- 如果表达式不包含近似值（仅包含精确值），且任何精确值包含小数部分，则使用 DECIMAL 精确算术进行评估，精度为 65 位数字。
- 否则，表达式仅包含整数值。该表达式是精确的。TiDB 使用整数运算评估，精度与 BIGINT（64 位）相同。

如果数字表达式包含字符串，字符串会被转换为双精度浮点值，表达式的结果为近似值。

对数字列的插入受到 SQL 模式的影响。以下讨论提到严格模式和 `ERROR_FOR_DIVISION_BY_ZERO`。你可以通过使用 `TRADITIONAL` 模式开启所有限制，该模式包括严格模式值和 `ERROR_FOR_DIVISION_BY_ZERO`：

```sql
SET sql_mode = 'TRADITIONAL`;
```

如果将数字插入到精确类型列（DECIMAL 或整数）中，只要在列范围内，数字会以其精确值插入。对于该数字：

- 如果小数部分位数过多，会发生四舍五入并生成警告。
- 如果整数部分位数过多，数值过大，处理方式如下：
    - 如果未启用严格模式，数值会被截断到最接近的合法值，并生成警告。
    - 如果启用严格模式，则会发生溢出错误。

将字符串插入数字列时，如果字符串包含非数字内容，TiDB 的处理方式如下：

- 在严格模式下，不以数字开头的字符串（包括空字符串）不能用作数字。会产生错误或警告。
- 以数字开头的字符串可以转换，但尾部非数字部分会被截断。在严格模式下，如果截断部分包含除空格外的内容，会产生错误或警告。

默认情况下，除以 0 的结果为 NULL 且无警告。通过设置 SQL 模式，可以限制除以 0 的行为。如果启用 `ERROR_FOR_DIVISION_BY_ZERO` SQL 模式，TiDB 处理除以 0 的方式如下：

- 在严格模式下，插入和更新被禁止，发生错误。
- 如果不在严格模式下，则会产生警告。

在以下 SQL 语句中：

```sql
INSERT INTO t SET i = 1/0;
```

不同 SQL 模式下返回的结果如下：

| `sql_mode` Value | Result |
| :--- | :--- |
| '' | 无警告，无错误；i 被设置为 NULL。|
| strict | 无警告，无错误；i 被设置为 NULL。 |
| `ERROR_FOR_DIVISION_BY_ZERO` | 警告，无错误；i 被设置为 NULL。 |
| strict, `ERROR_FOR_DIVISION_BY_ZERO` | 错误；不插入任何行。 |

## Rounding behavior

`ROUND()` 函数的结果取决于其参数是精确值还是近似值：

- 对于精确值数字，`ROUND()` 使用“五舍六入”规则。
- 对于近似值数字，TiDB 中的结果与 MySQL 不同：

    ```sql
    TiDB > SELECT ROUND(2.5), ROUND(25E-1);
    +------------+--------------+
    | ROUND(2.5) | ROUND(25E-1) |
    +------------+--------------+
    |          3 |            3 |
    +------------+--------------+
    1 row in set (0.00 sec)
    ```

对 DECIMAL 或整数列的插入，四舍五入采用 [round half away from zero](https://en.wikipedia.org/wiki/Rounding#Round_half_away_from_zero)。

```sql
TiDB > CREATE TABLE t (d DECIMAL(10,0));
Query OK, 0 rows affected (0.01 sec)

TiDB > INSERT INTO t VALUES(2.5),(2.5E0);
Query OK, 2 rows affected, 2 warnings (0.00 sec)

TiDB > SELECT d FROM t;
+------+
| d    |
+------+
|    3 |
|    3 |
+------+
2 rows in set (0.00 sec)
```