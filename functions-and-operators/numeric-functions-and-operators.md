---
title: Numeric Functions and Operators
summary: Learn about the numeric functions and operators.
---

# 数値関数と演算子 {#numeric-functions-and-operators}

TiDB は、 MySQL 5.7で利用可能な[<a href="https://dev.mysql.com/doc/refman/5.7/en/numeric-functions.html">数値関数と演算子</a>](https://dev.mysql.com/doc/refman/5.7/en/numeric-functions.html)をサポートします。

## 算術演算子 {#arithmetic-operators}

| 名前                                                                                                                                                                                                 | 説明         |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_plus">`+`</a>](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_plus)               | 加算演算子      |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_minus">`-`</a>](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_minus)             | マイナス演算子    |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_times">`*`</a>](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_times)             | 乗算演算子      |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_divide">`/`</a>](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_divide)           | 除算演算子      |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_div">`DIV`</a>](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_div)               | 整数の除算      |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_mod">`%` 、 `MOD`</a>](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_mod)         | モジュロ演算子    |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_unary-minus">`-`</a>](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_unary-minus) | 引数の符号を変更する |

## 数学関数 {#mathematical-functions}

| 名前                                                                                                                                                                                                        | 説明                 |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_pow">`POW()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_pow)                | 指定された引数をべき乗して返します  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_power">`POWER()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_power)          | 指定された引数をべき乗して返します  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_exp">`EXP()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_exp)                | の累乗                |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sqrt">`SQRT()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sqrt)             | 引数の平方根を返します        |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ln">`LN()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ln)                   | 引数の自然対数を返します       |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log">`LOG()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log)                | 最初の引数の自然対数を返します。   |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log2">`LOG2()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log2)             | 引数の底 2 の対数を返します。   |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log10">`LOG10()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log10)          | 引数の底 10 の対数を返します。  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_pi">`PI()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_pi)                   | 円周率の値を返す           |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_tan">`TAN()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_tan)                | 引数のタンジェントを返します     |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_cot">`COT()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_cot)                | コタンジェントを返します       |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sin">`SIN()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sin)                | 引数の正弦を返します         |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_cos">`COS()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_cos)                | コサインを返します          |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_atan">`ATAN()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_atan)             | 逆正接を返します           |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_atan2">`ATAN2(), ATAN()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_atan2)  | 2 つの引数の逆正接を返します。   |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_asin">`ASIN()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_asin)             | 逆正弦を返します           |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_acos">`ACOS()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_acos)             | 逆余弦を返します           |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_radians">`RADIANS()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_radians)    | ラジアンに変換された引数を返します  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_degrees">`DEGREES()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_degrees)    | ラジアンを度に変換する        |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_mod">`MOD()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_mod)                | 残りを返してください         |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs">`ABS()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs)                | 絶対値を返す             |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil">`CEIL()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil)             | 引数以上の最小の整数値を返します。  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling">`CEILING()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling)    | 引数以上の最小の整数値を返します。  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor">`FLOOR()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor)          | 引数以下の最大の整数値を返します。  |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_round">`ROUND()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_round)          | 引数を丸める             |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_rand">`RAND()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_rand)             | ランダムな浮動小数点値を返します   |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sign">`SIGN()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sign)             | 引数の符号を返します         |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_conv">`CONV()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_conv)             | 異なる基数間で数値を変換する     |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_truncate">`TRUNCATE()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_truncate) | 指定した小数点以下の桁数で切り捨てる |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_crc32">`CRC32()`</a>](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_crc32)          | 巡回冗長検査値を計算する       |
