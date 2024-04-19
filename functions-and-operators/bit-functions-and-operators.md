---
title: Bit Functions and Operators
summary: Learn about the bit functions and operators.
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

## MySQL compatibility

There are some differences between MySQL 8.0 and earlier versions of MySQL in handling bit functions and operators. TiDB aims to follow the behavior of MySQL 8.0.

## Known issues

In the following cases, the query results in TiDB are the same as MySQL 5.7 but different from MySQL 8.0.

- Bitwise operations with binary arguments. For more information, see [#30637](https://github.com/pingcap/tidb/issues/30637).
- The result of the `BIT_COUNT()` function. For more information, see [#44621](https://github.com/pingcap/tidb/issues/44621).
