---
title: Data Types
summary: TiDB でサポートされているデータ型について学習します。
---

# データ型 {#data-types}

TiDBは[文字列型](/data-type-string.md) MySQLの`SPATIAL`型を除くすべてのデータ型をサポートしています。これには、 [数値型](/data-type-numeric.md) [日付と時刻の種類](/data-type-date-and-time.md)すべてが含ま[JSON型](/data-type-json.md)ます。

データ型に使用される定義は`T(M[, D])`として指定されます。

-   `T`特定のデータ型を示します。
-   整数型の場合、 `M`最大表示幅を示します。浮動小数点型と固定小数点型の場合、 `M`格納可能な桁数（精度）です。文字列型の場合、 `M`最大長です。Mの許容最大値はデータ型によって異なります。

<CustomContent platform="tidb">

> **警告：**
>
> バージョン8.5.0以降、整数の表示幅は非推奨となりました（デフォルトでは[`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length)が`true`なります）。整数型の表示幅の指定は推奨されません。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> バージョン8.5.0以降、整数の表示幅は非推奨となりました。整数型の表示幅の指定は推奨されません。

</CustomContent>

-   `D`浮動小数点型と固定小数点型に適用され、小数点以下の桁数 (スケール) を示します。
-   `fsp` `TIME` 、 `DATETIME` 、 `TIMESTAMP`型に適用され、小数秒の精度を表します。8 `fsp`指定する場合は、0から6の範囲でなければなりません。0 は小数部がないことを意味します。省略した場合、デフォルトの精度は0です。
