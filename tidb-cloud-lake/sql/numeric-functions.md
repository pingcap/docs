---
title: Numeric Functions
summary: This page provides a comprehensive overview of Numeric functions in Databend, organized by functionality for easy reference.
---
This page provides a comprehensive overview of Numeric functions in Databend, organized by functionality for easy reference.

## Basic Arithmetic Functions

| Function | Description | Example |
|----------|-------------|---------|
| [PLUS](/tidb-cloud-lake/sql/plus.md) / [ADD](/tidb-cloud-lake/sql/add.md) | Addition operator | `5 + 3` → `8` |
| [MINUS](/tidb-cloud-lake/sql/minus.md) / [SUBTRACT](/tidb-cloud-lake/sql/subtract.md) | Subtraction operator | `5 - 3` → `2` |
| [MULTIPLY](/tidb-cloud-lake/sql/multiply.md) | Multiplication operator | `5 * 3` → `15` |
| [DIV](/tidb-cloud-lake/sql/div.md) | Division operator | `10 / 2` → `5.0` |
| [DIV0](/tidb-cloud-lake/sql/div.md) | Division that returns 0 instead of error for division by zero | `DIV0(10, 0)` → `0` |
| [DIVNULL](/tidb-cloud-lake/sql/divnull.md) | Division that returns NULL instead of error for division by zero | `DIVNULL(10, 0)` → `NULL` |
| [INTDIV](/tidb-cloud-lake/sql/intdiv.md) | Integer division | `10 DIV 3` → `3` |
| [MOD](/tidb-cloud-lake/sql/mod.md) / [MODULO](/tidb-cloud-lake/sql/modulo.md) | Modulo operation (remainder) | `10 % 3` → `1` |
| [NEG](/tidb-cloud-lake/sql/neg.md) / [NEGATE](/tidb-cloud-lake/sql/negate.md) | Negation | `-5` → `-5` |

## Rounding and Truncation Functions

| Function                                | Description                                               | Example                          |
|-----------------------------------------|-----------------------------------------------------------|----------------------------------|
| [ROUND](/tidb-cloud-lake/sql/round.md)                       | Rounds a number to specified decimal places               | `ROUND(123.456, 2)` → `123.46`   |
| [FLOOR](/tidb-cloud-lake/sql/floor.md)                       | Returns the largest integer not greater than the argument | `FLOOR(123.456)` → `123`         |
| [CEIL](/tidb-cloud-lake/sql/ceil.md) / [CEILING](/tidb-cloud-lake/sql/ceiling.md) | Returns the smallest integer not less than the argument   | `CEIL(123.456)` → `124`          |
| [TRUNCATE](/tidb-cloud-lake/sql/truncate.md)                 | Truncates a number to specified decimal places            | `TRUNCATE(123.456, 1)` → `123.4` |
| [TRUNC](/tidb-cloud-lake/sql/trunc.md)                       | Truncates a number to specified decimal places            | `TRUNC(123.456, 1)` → `123.4`    |

## Exponential and Logarithmic Functions

| Function | Description | Example |
|----------|-------------|---------|
| [EXP](/tidb-cloud-lake/sql/exp.md) | Returns e raised to the power of x | `EXP(1)` → `2.718281828459045` |
| [POW](/tidb-cloud-lake/sql/pow.md) / [POWER](/tidb-cloud-lake/sql/power.md) | Returns x raised to the power of y | `POW(2, 3)` → `8` |
| [SQRT](/tidb-cloud-lake/sql/sqrt.md) | Returns the square root of x | `SQRT(16)` → `4` |
| [CBRT](/tidb-cloud-lake/sql/cbrt.md) | Returns the cube root of x | `CBRT(27)` → `3` |
| [LN](/tidb-cloud-lake/sql/ln.md) | Returns the natural logarithm of x | `LN(2.718281828459045)` → `1` |
| [LOG10](/tidb-cloud-lake/sql/log.md) | Returns the base-10 logarithm of x | `LOG10(100)` → `2` |
| [LOG2](/tidb-cloud-lake/sql/log.md) | Returns the base-2 logarithm of x | `LOG2(8)` → `3` |
| [LOGX](/tidb-cloud-lake/sql/log-x.md) | Returns the logarithm of y to base x | `LOGX(2, 8)` → `3` |
| [LOGBX](/tidb-cloud-lake/sql/log-b-x.md) | Returns the logarithm of x to base b | `LOGBX(8, 2)` → `3` |

## Trigonometric Functions

| Function | Description | Example |
|----------|-------------|---------|
| [SIN](/tidb-cloud-lake/sql/sin.md) | Returns the sine of x | `SIN(0)` → `0` |
| [COS](/tidb-cloud-lake/sql/cos.md) | Returns the cosine of x | `COS(0)` → `1` |
| [TAN](/tidb-cloud-lake/sql/tan.md) | Returns the tangent of x | `TAN(0)` → `0` |
| [COT](/tidb-cloud-lake/sql/cot.md) | Returns the cotangent of x | `COT(1)` → `0.6420926159343306` |
| [ASIN](/tidb-cloud-lake/sql/asin.md) | Returns the arc sine of x | `ASIN(1)` → `1.5707963267948966` |
| [ACOS](/tidb-cloud-lake/sql/acos.md) | Returns the arc cosine of x | `ACOS(1)` → `0` |
| [ATAN](/tidb-cloud-lake/sql/atan.md) | Returns the arc tangent of x | `ATAN(1)` → `0.7853981633974483` |
| [ATAN2](/tidb-cloud-lake/sql/atan.md) | Returns the arc tangent of y/x | `ATAN2(1, 1)` → `0.7853981633974483` |
| [DEGREES](/tidb-cloud-lake/sql/degrees.md) | Converts radians to degrees | `DEGREES(PI())` → `180` |
| [RADIANS](/tidb-cloud-lake/sql/radians.md) | Converts degrees to radians | `RADIANS(180)` → `3.141592653589793` |
| [PI](/tidb-cloud-lake/sql/pi.md) | Returns the value of π | `PI()` → `3.141592653589793` |

## Other Numeric Functions

| Function | Description | Example |
|----------|-------------|---------|
| [ABS](/tidb-cloud-lake/sql/abs.md) | Returns the absolute value of x | `ABS(-5)` → `5` |
| [SIGN](/tidb-cloud-lake/sql/sign.md) | Returns the sign of x | `SIGN(-5)` → `-1` |
| [FACTORIAL](/tidb-cloud-lake/sql/factorial.md) | Returns the factorial of x | `FACTORIAL(5)` → `120` |
| [RAND](/tidb-cloud-lake/sql/rand.md) | Returns a random number between 0 and 1 | `RAND()` → `0.123...` (random) |
| [RANDN](/tidb-cloud-lake/sql/rand-n.md) | Returns a random number from standard normal distribution | `RANDN()` → `-0.123...` (random) |
| [CRC32](/tidb-cloud-lake/sql/crc.md) | Returns the CRC32 checksum of a string | `CRC32('Databend')` → `3899655467` |