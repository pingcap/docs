---
title: Bit Functions and Operators
summary: Learn about the bit functions and operators.
---

# ビット関数と演算子 {#bit-functions-and-operators}

TiDBは、 MySQL 5.7で利用可能な[ビット関数と演算子](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html)すべてをサポートします。

**ビット関数と演算子：**

| 名前                                                                                             | 説明                 |
| :--------------------------------------------------------------------------------------------- | :----------------- |
| [`BIT_COUNT()`](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#function_bit-count) | 1に設定されているビット数を返します |
| [＆](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-and)           | ビットごとのAND          |
| [〜](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-invert)        | ビット単位の反転           |
| [|](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-or)            | ビットごとのOR           |
| [^](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-xor)           | ビット単位のXOR          |
| [&lt;&lt;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_left-shift)     | 左方移動               |
| [&gt;&gt;](https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_right-shift)    | 右シフト               |
