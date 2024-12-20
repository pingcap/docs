---
title: Data Types
summary: TiDB でサポートされているデータ型について学習します。
---

# データ型 {#data-types}

TiDB は、 `SPATIAL`型を除く MySQL のすべてのデータ型をサポートしています。これには、 [数値型](/data-type-numeric.md) 、 [文字列型](/data-type-string.md) 、 [日付と時刻の種類](/data-type-date-and-time.md) 、および[JSON型](/data-type-json.md)のすべてが含まれます。

データ型に使用される定義は`T(M[, D])`として指定されます。

-   `T`特定のデータ型を示します。
-   `M`整数型の最大表示幅を示します。浮動小数点型と固定小数点型の場合、 `M`格納できる合計桁数 (精度) です。文字列型の場合、 `M`最大長です。M の許容最大値はデータ型によって異なります。

<CustomContent platform="tidb">

> **警告：**
>
> v8.5.0 以降、整数の表示幅は非推奨です (デフォルトでは[`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length)が`true`です)。整数型の表示幅を指定することは推奨されません。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> v8.5.0 以降では、整数の表示幅は非推奨です。整数型の表示幅を指定することは推奨されません。

</CustomContent>

-   `D`浮動小数点型と固定小数点型に適用され、小数点以下の桁数 (スケール) を示します。
-   `fsp` `TIME` 、 `DATETIME` 、および`TIMESTAMP`型に適用され、小数秒の精度を表します。 `fsp`値を指定する場合、その範囲は 0 ～ 6 である必要があります。 0 の値は小数部がないことを意味します。省略した場合、デフォルトの精度は 0 です。
