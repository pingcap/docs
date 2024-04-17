---
title: Bit Functions and Operators
summary: Learn about the bit functions and operators.
aliases: ['/docs/dev/functions-and-operators/bit-functions-and-operators/','/docs/dev/reference/sql/functions-and-operators/bit-functions-and-operators/']
---

# Bit Functions and Operators

TiDB supports all of the [bit functions and operators](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html) available in MySQL 8.0.

**Bit functions and operators:**

| Name | Description |
| :------| :------------- |
| [`BIT_COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#function_bit-count) | Return the number of bits that are set as 1 |
| [&](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-and) | Bitwise AND |
| [~](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-invert) | Bitwise inversion |
| [\|](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-or) | Bitwise OR |
| [^](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-xor) | Bitwise XOR |
| [<<](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_left-shift) | Left shift |
| [>>](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_right-shift) | Right shift |

# MySQL compatibility

There are some differences between MySQL 8.0 and earlier versions of MySQL in handling bit functions and operators. TiDB aims to follow the behavior of MySQL 8.0.

## Known issues

- [bitwise operations with binary args behavior changes between MySQL 5.7 and 8.0](https://github.com/pingcap/tidb/issues/30637)
- [function bit\_count result is Inconsistent with MySQL](https://github.com/pingcap/tidb/issues/44621)
