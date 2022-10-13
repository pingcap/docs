---
title: Cast Functions and Operators
summary: Learn about the cast functions and operators.
---

# キャスト関数と演算子 {#cast-functions-and-operators}

TiDB は、 MySQL 5.7で利用可能な[キャスト関数と演算子](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html)をすべてサポートします。

| 名前                                                                                          | 説明                 |
| ------------------------------------------------------------------------------------------- | ------------------ |
| [`BINARY`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#operator_binary)     | 文字列をバイナリ文字列にキャストする |
| [`CAST()`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_cast)       | 値を特定の型としてキャストする    |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_convert) | 値を特定の型としてキャストする    |

キャスト関数とキャスト演算子を使用すると、あるデータ型から別のデータ型に値を変換できます。
