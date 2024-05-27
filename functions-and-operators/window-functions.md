---
title: Window Functions
summary: このドキュメントでは、TiDB でサポートされているウィンドウ関数について説明します。
---

# ウィンドウ関数 {#window-functions}

TiDB でのウィンドウ関数の使用方法は、MySQL 8.0 の場合と同様です。詳細については、 [MySQL ウィンドウ関数](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)を参照してください。

ウィンドウ関数はパーサーで追加の単語を予約するため、TiDB ではウィンドウ関数を無効にするオプションが用意されています。アップグレード後に SQL ステートメントの解析エラーが発生する場合は、 `tidb_enable_window_function=0`設定してみてください。

ウィンドウ関数[ここに記載](/tiflash/tiflash-supported-pushdown-calculations.md) TiFlashにプッシュダウンできます。

`GROUP_CONCAT()`と`APPROX_PERCENTILE()`を除き、 TiDB は[`GROUP BY`集計関数](/functions-and-operators/aggregate-group-by-functions.md)すべてをサポートします。さらに、 TiDB は次のウィンドウ関数をサポートします。

| 関数名                                                                                                                 | 機能の説明                                                                    |
| :------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------- |
| [`CUME_DIST()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_cume-dist)       | 値のグループ内の値の累積分布を返します。                                                     |
| [`DENSE_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_dense-rank)     | パーティション内の現在の行のランクを返します。ランクにはギャップはありません。                                  |
| [`FIRST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_first-value)   | 現在のウィンドウの最初の行の式の値を返します。                                                  |
| [`LAG()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lag)                   | パーティション内の現在の行の N 行前の行から式の値を返します。                                         |
| [`LAST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_last-value)     | 現在のウィンドウの最後の行の式の値を返します。                                                  |
| [`LEAD()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lead)                 | パーティション内の現在の行から N 行後の行の式の値を返します。                                         |
| [`NTH_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_nth-value)       | 現在のウィンドウの N 行目から式の値を返します。                                                |
| [`NTILE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_ntile)               | パーティションを N 個のバケットに分割し、パーティション内の各行にバケット番号を割り当て、パーティション内の現在の行のバケット番号を返します。 |
| [`PERCENT_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_percent-rank) | 現在の行の値より小さいパーティション値の割合を返します。                                             |
| [`RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_rank)                 | パーティション内の現在の行のランクを返します。ランクにはギャップがある場合があります。                              |
| [`ROW_NUMBER()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_row-number)     | パーティション内の現在の行番号を返します。                                                    |
