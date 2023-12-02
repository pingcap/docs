---
title: Cast Functions and Operators
summary: Learn about the cast functions and operators.
---

# キャスト関数と演算子 {#cast-functions-and-operators}

キャスト関数と演算子を使用すると、あるデータ型から別のデータ型に値を変換できます。 TiDB は、 MySQL 5.7で利用可能な[キャスト関数と演算子](https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html)をサポートします。

## キャスト関数と演算子のリスト {#list-of-cast-functions-and-operators}

| 名前                                                                                          | 説明                  |
| ------------------------------------------------------------------------------------------- | ------------------- |
| [`BINARY`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary)     | 文字列をバイナリ文字列にキャストします |
| [`CAST()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast)       | 値を特定の型としてキャストする     |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) | 値を特定の型としてキャストする     |

> **注記：**
>
> TiDB と MySQL では、 `SELECT CAST(MeN AS CHAR)` (または同等の形式`SELECT CONVERT(MeM, CHAR)` ) に対して一貫性のない結果が表示されます。ここで、 `MeN`は科学表記法の倍精度浮動小数点数を表します。 MySQL は、 `-15 <= N <= 14`場合は完全な数値を表示し、 `N < -15`または`N > 14`の場合は科学表記法を表示します。ただし、TiDB では常に完全な数値が表示されます。たとえば、MySQL は`SELECT CAST(3.1415e15 AS CHAR)`の結果を`3.1415e15`と表示しますが、TiDB は結果を`3141500000000000`と表示します。
