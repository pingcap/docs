---
title: Data Types
summary: Learn about the data types supported in TiDB.
---

# データ型 {#data-types}

TiDBは、 `SPATIAL`のタイプを除くMySQLのすべてのデータタイプをサポートします。これには、 [数値型](/data-type-numeric.md) 、および[文字列型](/data-type-string.md)のすべてが含ま[JSONタイプ](/data-type-json.md) [日付と時刻のタイプ](/data-type-date-and-time.md) 。

データ型に使用される定義は`T(M[, D])`として指定されます。どこで：

-   `T`は特定のデータ型を示します。
-   `M`は、整数型の最大表示幅を示します。浮動小数点型と固定小数点型の場合、 `M`は格納できる合計桁数（精度）です。文字列タイプの場合、 `M`が最大長です。 Mの最大許容値は、データ型によって異なります。
-   `D`は浮動小数点型と固定小数点型に適用され、小数点以下の桁数（スケール）を示します。
-   `fsp`は、 `TIME` 、および`DATETIME`タイプに適用され、秒の小数部の精度を表し`TIMESTAMP` 。 `fsp`の値は、指定されている場合、0〜6の範囲内である必要があります。値0は、小数部分がないことを意味します。省略した場合、デフォルトの精度は0です。
