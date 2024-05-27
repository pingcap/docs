---
title: Numeric Functions and Operators
summary: 数値関数と演算子について学びます。
---

# 数値関数と演算子 {#numeric-functions-and-operators}

TiDB は、MySQL 8.0 で利用可能な[数値関数と演算子](https://dev.mysql.com/doc/refman/8.0/en/numeric-functions.html)のすべてをサポートします。

## 算術演算子 {#arithmetic-operators}

| 名前                                                                                            | 説明         |
| :-------------------------------------------------------------------------------------------- | :--------- |
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)        | 加算演算子      |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus)       | マイナス演算子    |
| [`*`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_times)       | 乗算演算子      |
| [`/`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_divide)      | 除算演算子      |
| [`DIV`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_div)       | 整数除算       |
| [`%` 、 `MOD`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_mod) | モジュロ演算子    |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_unary-minus) | 引数の符号を変更する |

## 数学関数 {#mathematical-functions}

| 名前                                                                                                      | 説明                  |
| :------------------------------------------------------------------------------------------------------ | :------------------ |
| [`ABS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_abs)             | 絶対値を返す              |
| [`ACOS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_acos)           | 逆余弦を返す              |
| [`ASIN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_asin)           | アークサインを返す           |
| [`ATAN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_atan)           | 逆正接を返す              |
| [`ATAN2(), ATAN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_atan2) | 2つの引数の逆正接を返す        |
| [`CEIL()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_ceil)           | 引数より小さくない最小の整数値を返す  |
| [`CEILING()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_ceiling)     | 引数より小さくない最小の整数値を返す  |
| [`CONV()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_conv)           | 異なる基数間で数値を変換する      |
| [`COS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_cos)             | コサインを返す             |
| [`COT()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_cot)             | 余弦を返す               |
| [`CRC32()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_crc32)         | 巡回冗長検査値を計算する        |
| [`DEGREES()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_degrees)     | ラジアンを度に変換する         |
| [`EXP()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_exp)             | 累乗する                |
| [`FLOOR()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_floor)         | 引数より大きくない最大の整数値を返す  |
| [`LN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_ln)               | 引数の自然対数を返す          |
| [`LOG()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_log)             | 最初の引数の自然対数を返す       |
| [`LOG10()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_log10)         | 引数の10を底とする対数を返す     |
| [`LOG2()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_log2)           | 引数の2を底とする対数を返す      |
| [`MOD()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_mod)             | 残りを返す               |
| [`PI()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_pi)               | 円周率の値を返す            |
| [`POW()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_pow)             | 引数を指定された累乗で返す       |
| [`POWER()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_power)         | 引数を指定された累乗で返す       |
| [`RADIANS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_radians)     | ラジアンに変換された引数を返す     |
| [`RAND()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_rand)           | ランダムな浮動小数点値を返す      |
| [`ROUND()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_round)         | 議論を迂回する             |
| [`SIGN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_sign)           | 引数の符号を返す            |
| [`SIN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_sin)             | 引数の正弦を返す            |
| [`SQRT()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_sqrt)           | 引数の平方根を返す           |
| [`TAN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_tan)             | 引数の正接を返す            |
| [`TRUNCATE()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_truncate)   | 指定された小数点以下の桁数に切り捨てる |

## 関連するシステム変数 {#related-system-variables}

[`div_precision_increment`](/system-variables.md#div_precision_increment-new-in-v800) `/`演算子の精度を設定するために使用されます。
