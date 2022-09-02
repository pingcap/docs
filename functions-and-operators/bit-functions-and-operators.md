---
title: Bit Functions and Operators
summary: Learn about the bit functions and operators.
---

# ビット関数と演算子 {#bit-functions-and-operators}

TiDB は、 MySQL 5.7で利用可能な[ビット関数と演算子](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html)をすべてサポートします。

**ビット関数と演算子:**

| 名前                                                                                             | 説明                   |
| :--------------------------------------------------------------------------------------------- | :------------------- |
| [`BIT_COUNT()`](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#function_bit-count) | 1 に設定されているビットの数を返します |
| [&amp;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-and)       | ビット演算 AND            |
| [〜](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-invert)        | ビット反転                |
| [| |](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-or)          | ビットごとの OR            |
| [^](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-xor)           | ビット単位の XOR           |
| [&lt;&lt;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_left-shift)     | 左方移動                 |
| [&gt;&gt;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_right-shift)    | 右シフト                 |
