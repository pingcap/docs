---
title: Control Flow Functions
summary: TiDBはMySQL 5.7で利用可能な制御フロー関数をサポートします。制御フロー関数には、CASE、IF()、IFNULL()、NULLIF()があります。それぞれケース演算子、If/elseコンストラクト、Null if/else構造、expr1 = expr2の場合はNULLを返します。
---

# 制御フロー関数 {#control-flow-functions}

TiDB は、 MySQL 5.7で利用可能な[制御フロー関数](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html)をサポートします。

| 名前                                                                                                | 説明                            |
| :------------------------------------------------------------------------------------------------ | :---------------------------- |
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)       | ケース演算子                        |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)         | If/else コンストラクト               |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | Null if/else 構造               |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | expr1 = expr2 の場合は NULL を返します |
