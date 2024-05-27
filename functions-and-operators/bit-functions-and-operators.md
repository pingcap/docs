---
title: Bit Functions and Operators
summary: ビット関数と演算子について学習します。
---

# ビット関数と演算子 {#bit-functions-and-operators}

TiDB は、MySQL 8.0 で利用可能な[ビット関数と演算子](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html)のすべてをサポートします。

**ビット関数と演算子:**

| 名前                                                                                             | 説明                  |
| :--------------------------------------------------------------------------------------------- | :------------------ |
| [`BIT_COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#function_bit-count) | 1に設定されているビットの数を返します |
| [＆](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-and)           | ビットAND              |
| [〜](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-invert)        | ビット反転               |
| [|](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-or)            | ビットOR               |
| [^](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-xor)           | ビット単位の排他的論理和        |
| [&lt;&lt;](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_left-shift)     | 左方移動                |
| [&gt;&gt;](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_right-shift)    | 右シフト                |

## MySQL 互換性 {#mysql-compatibility}

MySQL 8.0 と以前のバージョンの MySQL では、ビット関数と演算子の処理にいくつかの違いがあります。TiDB は、MySQL 8.0 の動作に従うことを目指しています。

## 既知の問題点 {#known-issues}

以下の場合、TiDB のクエリ結果はMySQL 5.7と同じですが、MySQL 8.0 とは異なります。

-   バイナリ引数を使用したビット演算。詳細については、 [＃30637](https://github.com/pingcap/tidb/issues/30637)参照してください。
-   `BIT_COUNT()`関数の結果。詳細については、 [＃44621](https://github.com/pingcap/tidb/issues/44621)を参照してください。
