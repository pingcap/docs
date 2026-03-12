---
title: Numeric Functions
---

This page provides a comprehensive overview of Numeric functions in Databend, organized by functionality for easy reference.

## Basic Arithmetic Functions

| Function | Description | Example |
|----------|-------------|---------|
| [PLUS](plus.md) / [ADD](add.md) | Addition operator | `5 + 3` → `8` |
| [MINUS](minus.md) / [SUBTRACT](subtract.md) | Subtraction operator | `5 - 3` → `2` |
| [MULTIPLY](multiply.md) | Multiplication operator | `5 * 3` → `15` |
| [DIV](div.md) | Division operator | `10 / 2` → `5.0` |
| [DIV0](div0.md) | Division that returns 0 instead of error for division by zero | `DIV0(10, 0)` → `0` |
| [DIVNULL](divnull.md) | Division that returns NULL instead of error for division by zero | `DIVNULL(10, 0)` → `NULL` |
| [INTDIV](intdiv.md) | Integer division | `10 DIV 3` → `3` |
| [MOD](mod.md) / [MODULO](modulo.md) | Modulo operation (remainder) | `10 % 3` → `1` |
| [NEG](neg.md) / [NEGATE](negate.md) | Negation | `-5` → `-5` |

## Rounding and Truncation Functions

| Function                                | Description                                               | Example                          |
|-----------------------------------------|-----------------------------------------------------------|----------------------------------|
| [ROUND](round.md)                       | Rounds a number to specified decimal places               | `ROUND(123.456, 2)` → `123.46`   |
| [FLOOR](floor.md)                       | Returns the largest integer not greater than the argument | `FLOOR(123.456)` → `123`         |
| [CEIL](ceil.md) / [CEILING](ceiling.md) | Returns the smallest integer not less than the argument   | `CEIL(123.456)` → `124`          |
| [TRUNCATE](truncate.md)                 | Truncates a number to specified decimal places            | `TRUNCATE(123.456, 1)` → `123.4` |
| [TRUNC](trunc.md)                       | Truncates a number to specified decimal places            | `TRUNC(123.456, 1)` → `123.4`    |

## Exponential and Logarithmic Functions

| Function | Description | Example |
|----------|-------------|---------|
| [EXP](exp.md) | Returns e raised to the power of x | `EXP(1)` → `2.718281828459045` |
| [POW](pow.md) / [POWER](power.md) | Returns x raised to the power of y | `POW(2, 3)` → `8` |
| [SQRT](sqrt.md) | Returns the square root of x | `SQRT(16)` → `4` |
| [CBRT](cbrt.md) | Returns the cube root of x | `CBRT(27)` → `3` |
| [LN](ln.md) | Returns the natural logarithm of x | `LN(2.718281828459045)` → `1` |
| [LOG10](log10.md) | Returns the base-10 logarithm of x | `LOG10(100)` → `2` |
| [LOG2](log2.md) | Returns the base-2 logarithm of x | `LOG2(8)` → `3` |
| [LOGX](logx.md) | Returns the logarithm of y to base x | `LOGX(2, 8)` → `3` |
| [LOGBX](logbx.md) | Returns the logarithm of x to base b | `LOGBX(8, 2)` → `3` |

## Trigonometric Functions

| Function | Description | Example |
|----------|-------------|---------|
| [SIN](sin.md) | Returns the sine of x | `SIN(0)` → `0` |
| [COS](cos.md) | Returns the cosine of x | `COS(0)` → `1` |
| [TAN](tan.md) | Returns the tangent of x | `TAN(0)` → `0` |
| [COT](cot.md) | Returns the cotangent of x | `COT(1)` → `0.6420926159343306` |
| [ASIN](asin.md) | Returns the arc sine of x | `ASIN(1)` → `1.5707963267948966` |
| [ACOS](acos.md) | Returns the arc cosine of x | `ACOS(1)` → `0` |
| [ATAN](atan.md) | Returns the arc tangent of x | `ATAN(1)` → `0.7853981633974483` |
| [ATAN2](atan2.md) | Returns the arc tangent of y/x | `ATAN2(1, 1)` → `0.7853981633974483` |
| [DEGREES](degrees.md) | Converts radians to degrees | `DEGREES(PI())` → `180` |
| [RADIANS](radians.md) | Converts degrees to radians | `RADIANS(180)` → `3.141592653589793` |
| [PI](pi.md) | Returns the value of π | `PI()` → `3.141592653589793` |

## Other Numeric Functions

| Function | Description | Example |
|----------|-------------|---------|
| [ABS](abs.md) | Returns the absolute value of x | `ABS(-5)` → `5` |
| [SIGN](sign.md) | Returns the sign of x | `SIGN(-5)` → `-1` |
| [FACTORIAL](factorial.md) | Returns the factorial of x | `FACTORIAL(5)` → `120` |
| [RAND](rand.md) | Returns a random number between 0 and 1 | `RAND()` → `0.123...` (random) |
| [RANDN](randn.md) | Returns a random number from standard normal distribution | `RANDN()` → `-0.123...` (random) |
| [CRC32](crc32.md) | Returns the CRC32 checksum of a string | `CRC32('Databend')` → `3899655467` |