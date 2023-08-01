---
title: Data Types
summary: Learn about the data types supported in TiDB.
---

# データ型 {#data-types}

TiDB は、 `SPATIAL`のタイプを除く MySQL のすべてのデータ タイプをサポートします。これには、 [数値型](/data-type-numeric.md) 、 [文字列型](/data-type-string.md) 、 [日付と時刻のタイプ](/data-type-date-and-time.md) 、および[JSON タイプ](/data-type-json.md)がすべて含まれます。

データ型に使用される定義は`T(M[, D])`として指定されます。どこで:

-   `T`特定のデータ型を示します。
-   `M`整数型の最大表示幅を示します。浮動小数点型および固定小数点型の場合、格納できる合計桁数 (精度) は`M`です。文字列型の場合、最大長は`M`です。 M の最大許容値はデータ型によって異なります。
-   `D`は浮動小数点型と固定小数点型に適用され、小数点以下の桁数 (スケール) を示します。
-   `fsp` `TIME` 、 `DATETIME` 、および`TIMESTAMP`タイプに適用され、小数秒の精度を表します。 `fsp`値を指定する場合は、0 ～ 6 の範囲内である必要があります。値 0 は、小数部がないことを意味します。省略した場合、デフォルトの精度は 0 です。
