---
title: 数値関数
summary: このページでは、{{{ .lake }}} の数値関数の包括的な概要を、参照しやすいように機能別に整理して紹介します。
---

# 数値関数

このページでは、{{{ .lake }}} の数値関数の包括的な概要を、参照しやすいように機能別に整理して紹介します。

## 基本的な算術関数 {#basic-arithmetic-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [PLUS](/tidb-cloud-lake/sql/plus.md) / [ADD](/tidb-cloud-lake/sql/add.md) | 加算演算子 | `5 + 3` → `8` |
| [MINUS](/tidb-cloud-lake/sql/minus.md) / [SUBTRACT](/tidb-cloud-lake/sql/subtract.md) | 減算演算子 | `5 - 3` → `2` |
| [MULTIPLY](/tidb-cloud-lake/sql/multiply.md) | 乗算演算子 | `5 * 3` → `15` |
| [DIV](/tidb-cloud-lake/sql/div.md) | 除算演算子 | `10 / 2` → `5.0` |
| [DIV0](/tidb-cloud-lake/sql/div.md) | 0 による除算時にエラーではなく 0 を返す除算 | `DIV0(10, 0)` → `0` |
| [DIVNULL](/tidb-cloud-lake/sql/divnull.md) | 0 による除算時にエラーではなく NULL を返す除算 | `DIVNULL(10, 0)` → `NULL` |
| [INTDIV](/tidb-cloud-lake/sql/intdiv.md) | 整数除算 | `10 DIV 3` → `3` |
| [MOD](/tidb-cloud-lake/sql/mod.md) / [MODULO](/tidb-cloud-lake/sql/modulo.md) | 剰余演算（余り） | `10 % 3` → `1` |
| [NEG](/tidb-cloud-lake/sql/neg.md) / [NEGATE](/tidb-cloud-lake/sql/negate.md) | 符号反転 | `-5` → `-5` |

## 丸めおよび切り捨て関数 {#rounding-and-truncation-functions}

| 関数                                | 説明                                               | 例                          |
|-----------------------------------------|-----------------------------------------------------------|----------------------------------|
| [ROUND](/tidb-cloud-lake/sql/round.md)                       | 数値を指定した小数位に丸めます               | `ROUND(123.456, 2)` → `123.46`   |
| [FLOOR](/tidb-cloud-lake/sql/floor.md)                       | 引数以下の最大の整数を返します | `FLOOR(123.456)` → `123`         |
| [CEIL](/tidb-cloud-lake/sql/ceil.md) / [CEILING](/tidb-cloud-lake/sql/ceiling.md) | 引数以上の最小の整数を返します   | `CEIL(123.456)` → `124`          |
| [TRUNCATE](/tidb-cloud-lake/sql/truncate.md)                 | 数値を指定した小数位で切り捨てます            | `TRUNCATE(123.456, 1)` → `123.4` |
| [TRUNC](/tidb-cloud-lake/sql/trunc.md)                       | 数値を指定した小数位で切り捨てます            | `TRUNC(123.456, 1)` → `123.4`    |

## 指数関数および対数関数 {#exponential-and-logarithmic-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [EXP](/tidb-cloud-lake/sql/exp.md) | e の x 乗を返します | `EXP(1)` → `2.718281828459045` |
| [POW](/tidb-cloud-lake/sql/pow.md) / [POWER](/tidb-cloud-lake/sql/power.md) | x の y 乗を返します | `POW(2, 3)` → `8` |
| [SQRT](/tidb-cloud-lake/sql/sqrt.md) | x の平方根を返します | `SQRT(16)` → `4` |
| [CBRT](/tidb-cloud-lake/sql/cbrt.md) | x の立方根を返します | `CBRT(27)` → `3` |
| [LN](/tidb-cloud-lake/sql/ln.md) | x の自然対数を返します | `LN(2.718281828459045)` → `1` |
| [LOG10](/tidb-cloud-lake/sql/log.md) | x の常用対数を返します | `LOG10(100)` → `2` |
| [LOG2](/tidb-cloud-lake/sql/log.md) | x の底 2 の対数を返します | `LOG2(8)` → `3` |
| [LOGX](/tidb-cloud-lake/sql/log-x.md) | 底 x における y の対数を返します | `LOGX(2, 8)` → `3` |
| [LOGBX](/tidb-cloud-lake/sql/log-b-x.md) | 底 b における x の対数を返します | `LOGBX(8, 2)` → `3` |

## 三角関数 {#trigonometric-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [SIN](/tidb-cloud-lake/sql/sin.md) | x の正弦を返します | `SIN(0)` → `0` |
| [COS](/tidb-cloud-lake/sql/cos.md) | x の余弦を返します | `COS(0)` → `1` |
| [TAN](/tidb-cloud-lake/sql/tan.md) | x の正接を返します | `TAN(0)` → `0` |
| [COT](/tidb-cloud-lake/sql/cot.md) | x の余接を返します | `COT(1)` → `0.6420926159343306` |
| [ASIN](/tidb-cloud-lake/sql/asin.md) | x の逆正弦を返します | `ASIN(1)` → `1.5707963267948966` |
| [ACOS](/tidb-cloud-lake/sql/acos.md) | x の逆余弦を返します | `ACOS(1)` → `0` |
| [ATAN](/tidb-cloud-lake/sql/atan.md) | x の逆正接を返します | `ATAN(1)` → `0.7853981633974483` |
| [ATAN2](/tidb-cloud-lake/sql/atan.md) | y/x の逆正接を返します | `ATAN2(1, 1)` → `0.7853981633974483` |
| [DEGREES](/tidb-cloud-lake/sql/degrees.md) | ラジアンを度に変換します | `DEGREES(PI())` → `180` |
| [RADIANS](/tidb-cloud-lake/sql/radians.md) | 度をラジアンに変換します | `RADIANS(180)` → `3.141592653589793` |
| [PI](/tidb-cloud-lake/sql/pi.md) | π の値を返します | `PI()` → `3.141592653589793` |

## その他の数値関数 {#other-numeric-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ABS](/tidb-cloud-lake/sql/abs.md) | x の絶対値を返します | `ABS(-5)` → `5` |
| [SIGN](/tidb-cloud-lake/sql/sign.md) | x の符号を返します | `SIGN(-5)` → `-1` |
| [FACTORIAL](/tidb-cloud-lake/sql/factorial.md) | x の階乗を返します | `FACTORIAL(5)` → `120` |
| [RAND](/tidb-cloud-lake/sql/rand.md) | 0 から 1 の間の乱数を返します | `RAND()` → `0.123...` (random) |
| [RANDN](/tidb-cloud-lake/sql/rand-n.md) | 標準正規分布に従う乱数を返します | `RANDN()` → `-0.123...` (random) |
| [CRC32](/tidb-cloud-lake/sql/crc.md) | 文字列の CRC32 チェックサムを返します | `CRC32('datalake')` → `2878859588` |