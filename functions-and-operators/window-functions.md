---
title: Window Functions
summary: This document introduces window functions supported in TiDB.
---

# ウィンドウ関数 {#window-functions}

TiDBでのウィンドウ関数の使用法は、MySQL8.0での使用法と似ています。詳細については、 [MySQLウィンドウ関数](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)を参照してください。

ウィンドウ関数はパーサーに追加の単語を予約するため、TiDBにはウィンドウ関数を無効にするオプションがあります。アップグレード後にSQLステートメントの解析中にエラーが発生した場合は、 `tidb_enable_window_function=0`を設定してみてください。

TiDBは、次のウィンドウ関数をサポートしています。

| 関数名                                                                                                                 | 機能の説明                                                                  |
| :------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------- |
| [`CUME_DIST()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_cume-dist)       | 値のグループ内の値の累積分布を返します。                                                   |
| [`DENSE_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_dense-rank)     | パーティション内の現在の行のランクを返します。ランクにはギャップがありません。                                |
| [`FIRST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_first-value)   | 現在のウィンドウの最初の行の式の値を返します。                                                |
| [`LAG()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lag)                   | パーティション内で現在の行の前にN行ある行から式の値を返します。                                       |
| [`LAST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_last-value)     | 現在のウィンドウの最後の行の式の値を返します。                                                |
| [`LEAD()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lead)                 | パーティション内で現在の行にN行続く行から式の値を返します。                                         |
| [`NTH_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_nth-value)       | 現在のウィンドウのN番目の行から式の値を返します。                                              |
| [`NTILE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_ntile)               | パーティションをN個のバケットに分割し、パーティション内の各行にバケット番号を割り当て、パーティション内の現在の行のバケット番号を返します。 |
| [`PERCENT_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_percent-rank) | 現在の行の値よりも小さいパーティション値のパーセンテージを返します。                                     |
| [`RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_rank)                 | パーティション内の現在の行のランクを返します。ランクにはギャップがあるかもしれません。                            |
| [`ROW_NUMBER()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_row-number)     | パーティション内の現在の行の番号を返します。                                                 |
