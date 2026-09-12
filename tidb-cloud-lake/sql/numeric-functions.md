---
title: 数值函数
summary: 本页按功能组织，全面概述了 {{{ .lake }}} 中的数值函数，便于参考。
---

# 数值函数

本页按功能组织，全面概述了 {{{ .lake }}} 中的数值函数，便于参考。

## 基本算术函数 {#basic-arithmetic-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [PLUS](/tidb-cloud-lake/sql/plus.md) / [ADD](/tidb-cloud-lake/sql/add.md) | 加法运算符 | `5 + 3` → `8` |
| [MINUS](/tidb-cloud-lake/sql/minus.md) / [SUBTRACT](/tidb-cloud-lake/sql/subtract.md) | 减法运算符 | `5 - 3` → `2` |
| [MULTIPLY](/tidb-cloud-lake/sql/multiply.md) | 乘法运算符 | `5 * 3` → `15` |
| [DIV](/tidb-cloud-lake/sql/div.md) | 除法运算符 | `10 / 2` → `5.0` |
| [DIV0](/tidb-cloud-lake/sql/div.md) | 除零时返回 0 而不是报错的除法 | `DIV0(10, 0)` → `0` |
| [DIVNULL](/tidb-cloud-lake/sql/divnull.md) | 除零时返回 NULL 而不是报错的除法 | `DIVNULL(10, 0)` → `NULL` |
| [INTDIV](/tidb-cloud-lake/sql/intdiv.md) | 整数除法 | `10 DIV 3` → `3` |
| [MOD](/tidb-cloud-lake/sql/mod.md) / [MODULO](/tidb-cloud-lake/sql/modulo.md) | 取模运算（余数） | `10 % 3` → `1` |
| [NEG](/tidb-cloud-lake/sql/neg.md) / [NEGATE](/tidb-cloud-lake/sql/negate.md) | 取负 | `-5` → `-5` |

## 舍入与截断函数 {#rounding-and-truncation-functions}

| 函数                                | 描述                                               | 示例                          |
|-----------------------------------------|-----------------------------------------------------------|----------------------------------|
| [ROUND](/tidb-cloud-lake/sql/round.md)                       | 将数字舍入到指定的小数位数               | `ROUND(123.456, 2)` → `123.46`   |
| [FLOOR](/tidb-cloud-lake/sql/floor.md)                       | 返回不大于参数的最大整数 | `FLOOR(123.456)` → `123`         |
| [CEIL](/tidb-cloud-lake/sql/ceil.md) / [CEILING](/tidb-cloud-lake/sql/ceiling.md) | 返回不小于参数的最小整数   | `CEIL(123.456)` → `124`          |
| [TRUNCATE](/tidb-cloud-lake/sql/truncate.md)                 | 将数字截断到指定的小数位数            | `TRUNCATE(123.456, 1)` → `123.4` |
| [TRUNC](/tidb-cloud-lake/sql/trunc.md)                       | 将数字截断到指定的小数位数            | `TRUNC(123.456, 1)` → `123.4`    |

## 指数与对数函数 {#exponential-and-logarithmic-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [EXP](/tidb-cloud-lake/sql/exp.md) | 返回 e 的 x 次幂 | `EXP(1)` → `2.718281828459045` |
| [POW](/tidb-cloud-lake/sql/pow.md) / [POWER](/tidb-cloud-lake/sql/power.md) | 返回 x 的 y 次幂 | `POW(2, 3)` → `8` |
| [SQRT](/tidb-cloud-lake/sql/sqrt.md) | 返回 x 的平方根 | `SQRT(16)` → `4` |
| [CBRT](/tidb-cloud-lake/sql/cbrt.md) | 返回 x 的立方根 | `CBRT(27)` → `3` |
| [LN](/tidb-cloud-lake/sql/ln.md) | 返回 x 的自然对数 | `LN(2.718281828459045)` → `1` |
| [LOG10](/tidb-cloud-lake/sql/log.md) | 返回 x 的以 10 为底的对数 | `LOG10(100)` → `2` |
| [LOG2](/tidb-cloud-lake/sql/log.md) | 返回 x 的以 2 为底的对数 | `LOG2(8)` → `3` |
| [LOGX](/tidb-cloud-lake/sql/log-x.md) | 返回以 x 为底 y 的对数 | `LOGX(2, 8)` → `3` |
| [LOGBX](/tidb-cloud-lake/sql/log-b-x.md) | 返回以 b 为底 x 的对数 | `LOGBX(8, 2)` → `3` |

## 三角函数 {#trigonometric-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [SIN](/tidb-cloud-lake/sql/sin.md) | 返回 x 的正弦值 | `SIN(0)` → `0` |
| [COS](/tidb-cloud-lake/sql/cos.md) | 返回 x 的余弦值 | `COS(0)` → `1` |
| [TAN](/tidb-cloud-lake/sql/tan.md) | 返回 x 的正切值 | `TAN(0)` → `0` |
| [COT](/tidb-cloud-lake/sql/cot.md) | 返回 x 的余切值 | `COT(1)` → `0.6420926159343306` |
| [ASIN](/tidb-cloud-lake/sql/asin.md) | 返回 x 的反正弦值 | `ASIN(1)` → `1.5707963267948966` |
| [ACOS](/tidb-cloud-lake/sql/acos.md) | 返回 x 的反余弦值 | `ACOS(1)` → `0` |
| [ATAN](/tidb-cloud-lake/sql/atan.md) | 返回 x 的反正切值 | `ATAN(1)` → `0.7853981633974483` |
| [ATAN2](/tidb-cloud-lake/sql/atan.md) | 返回 y/x 的反正切值 | `ATAN2(1, 1)` → `0.7853981633974483` |
| [DEGREES](/tidb-cloud-lake/sql/degrees.md) | 将弧度转换为角度 | `DEGREES(PI())` → `180` |
| [RADIANS](/tidb-cloud-lake/sql/radians.md) | 将角度转换为弧度 | `RADIANS(180)` → `3.141592653589793` |
| [PI](/tidb-cloud-lake/sql/pi.md) | 返回 π 的值 | `PI()` → `3.141592653589793` |

## 其他数值函数 {#other-numeric-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ABS](/tidb-cloud-lake/sql/abs.md) | 返回 x 的绝对值 | `ABS(-5)` → `5` |
| [SIGN](/tidb-cloud-lake/sql/sign.md) | 返回 x 的符号 | `SIGN(-5)` → `-1` |
| [FACTORIAL](/tidb-cloud-lake/sql/factorial.md) | 返回 x 的阶乘 | `FACTORIAL(5)` → `120` |
| [RAND](/tidb-cloud-lake/sql/rand.md) | 返回 0 到 1 之间的随机数 | `RAND()` → `0.123...`（随机） |
| [RANDN](/tidb-cloud-lake/sql/rand-n.md) | 返回服从标准正态分布的随机数 | `RANDN()` → `-0.123...`（随机） |
| [CRC32](/tidb-cloud-lake/sql/crc.md) | 返回字符串的 CRC32 校验和 | `CRC32('datalake')` → `2878859588` |