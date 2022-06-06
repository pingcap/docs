---
title: Cast Functions and Operators
summary: Learn about the cast functions and operators.
---

# キャスト関数と演算子 {#cast-functions-and-operators}

TiDBは、MySQL5.7で利用可能な[キャスト関数と演算子](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html)すべてをサポートします。

| 名前                                                                                          | 説明                  |
| ------------------------------------------------------------------------------------------- | ------------------- |
| [`BINARY`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#operator_binary)     | 文字列をバイナリ文字列にキャストします |
| [`CAST()`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_cast)       | 特定のタイプとして値をキャストする   |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_convert) | 特定のタイプとして値をキャストする   |

キャスト関数と演算子を使用すると、あるデータ型から別のデータ型に値を変換できます。
