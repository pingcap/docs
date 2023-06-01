---
title: Bit Functions and Operators
summary: Learn about the bit functions and operators.
---

# ビット関数と演算子 {#bit-functions-and-operators}

TiDB は、 MySQL 5.7で利用可能な[<a href="https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html">ビット関数と演算子</a>](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html)をサポートします。

**ビット関数と演算子:**

| 名前                                                                                                                                                                                         | 説明                  |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#function_bit-count">`BIT_COUNT()`</a>](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#function_bit-count) | 1に設定されているビット数を返します。 |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-and">&amp;</a>](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-and)     | ビットごとの AND          |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-invert">～</a>](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-invert)   | ビットごとの反転            |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-or">|</a>](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-or)           | ビットごとの OR           |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-xor">^</a>](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-xor)         | ビットごとの XOR          |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_left-shift">&lt;&lt;</a>](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_left-shift)    | 左方移動                |
| [<a href="https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_right-shift">&gt;&gt;</a>](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_right-shift)  | 右シフト                |
