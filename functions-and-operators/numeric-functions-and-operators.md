---
title: Numeric Functions and Operators
summary: Learn about the numeric functions and operators.
---

# Numeric Functions and Operators

TiDB supports all of the [numeric functions and operators](https://dev.mysql.com/doc/refman/8.0/en/numeric-functions.html) available in MySQL 8.0.

## Arithmetic operators

| Name                                                                                          | Description                       |
|:----------------------------------------------------------------------------------------------|:----------------------------------|
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)        | Addition operator                 |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus)       | Minus operator                    |
| [`*`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_times)       | Multiplication operator           |
| [`/`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_divide)      | Division operator                 |
| [`DIV`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_div)       | Integer division                  |
| [`%`, `MOD`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_mod)  | Modulo operator                   |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_unary-minus) | Change the sign of the argument   |

## Mathematical functions

| Name                                                                                                      | Description                                                       |
|:----------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------|
| [`ABS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_abs)               | Return the absolute value                                         |
| [`ACOS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_acos)             | Return the arc cosine                                             |
| [`ASIN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_asin)             | Return the arc sine                                               |
| [`ATAN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_atan)             | Return the arc tangent                                            |
| [`ATAN2(), ATAN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_atan2)   | Return the arc tangent of the two arguments                       |
| [`CEIL()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_ceil)             | Return the smallest integer value not less than the argument      |
| [`CEILING()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_ceiling)       | Return the smallest integer value not less than the argument      |
| [`CONV()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_conv)             | Convert numbers between different number bases                    |
| [`COS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_cos)               | Return the cosine                                                 |
| [`COT()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_cot)               | Return the cotangent                                              |
| [`CRC32()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_crc32)           | Compute a cyclic redundancy check value                           |
| [`DEGREES()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_degrees)       | Convert radians to degrees                                        |
| [`EXP()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_exp)               | Raise to the power of                                             |
| [`FLOOR()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_floor)           | Return the largest integer value not greater than the argument    |
| [`LN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_ln)                 | Return the natural logarithm of the argument                      |
| [`LOG()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_log)               | Return the natural logarithm of the first argument                |
| [`LOG10()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_log10)           | Return the base-10 logarithm of the argument                      |
| [`LOG2()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_log2)             | Return the base-2 logarithm of the argument                       |
| [`MOD()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_mod)               | Return the remainder                                              |
| [`PI()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_pi)                 | Return the value of pi                                            |
| [`POW()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_pow)               | Return the argument raised to the specified power                 |
| [`POWER()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_power)           | Return the argument raised to the specified power                 |
| [`RADIANS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_radians)       | Return argument converted to radians                              |
| [`RAND()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_rand)             | Return a random floating-point value                              |
| [`ROUND()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_round)           | Round the argument                                                |
| [`SIGN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_sign)             | Return the sign of the argument                                   |
| [`SIN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_sin)               | Return the sine of the argument                                   |
| [`SQRT()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_sqrt)             | Return the square root of the argument                            |
| [`TAN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_tan)               | Return the tangent of the argument                                |
| [`TRUNCATE()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_truncate)     | Truncate to specified number of decimal places                    |

## Related system variables

[`div_precision_increment`](/system-variables.md#div_precision_increment-new-in-v800) is used to set the precision for the `/` operator.