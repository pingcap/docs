---
title: Window Functions
summary: This document introduces window functions supported in TiDB.
---

# ウィンドウ関数 {#window-functions}

TiDB でのウィンドウ関数の使用法は、MySQL 8.0 での使用法と似ています。詳細は[MySQL ウィンドウ関数](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)を参照してください。

ウィンドウ関数はパーサー内に追加の単語を予約するため、TiDB はウィンドウ関数を無効にするオプションを提供します。アップグレード後に SQL ステートメントの解析中にエラーが発生した場合は、 `tidb_enable_window_function=0`を設定してみてください。

ウィンドウ関数[ここにリストされています](/tiflash/tiflash-supported-pushdown-calculations.md) TiFlashにプッシュダウンできます。

`GROUP_CONCAT()`と`APPROX_PERCENTILE()`を除く、TiDB は[`GROUP BY`集計関数](/functions-and-operators/aggregate-group-by-functions.md)すべてサポートします。さらに、TiDB は次のウィンドウ関数をサポートします。

| 関数名                                                                                                                 | 機能の説明                                                                    |
| :------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------- |
| [`CUME_DIST()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_cume-dist)       | 値のグループ内の値の累積分布を返します。                                                     |
| [`DENSE_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_dense-rank)     | パーティション内の現在の行のランクを返します。ランクにはギャップがありません。                                  |
| [`FIRST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_first-value)   | 現在のウィンドウの最初の行の式の値を返します。                                                  |
| [`LAG()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lag)                   | パーティション内で現在の行から N 行前にある行から式の値を返します。                                      |
| [`LAST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_last-value)     | 現在のウィンドウの最後の行の式の値を返します。                                                  |
| [`LEAD()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lead)                 | パーティション内の現在の行から N 行後の行から式の値を返します。                                        |
| [`NTH_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_nth-value)       | 現在のウィンドウの N 行目の式の値を返します。                                                 |
| [`NTILE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_ntile)               | パーティションを N 個のバケットに分割し、パーティション内の各行にバケット番号を割り当て、パーティション内の現在の行のバケット番号を返します。 |
| [`PERCENT_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_percent-rank) | 現在の行の値より小さいパーティション値の割合を返します。                                             |
| [`RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_rank)                 | パーティション内の現在の行のランクを返します。ランクには誤差がある場合がございます。                               |
| [`ROW_NUMBER()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_row-number)     | パーティション内の現在の行の番号を返します。                                                   |
