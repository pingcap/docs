---
title: Push-down calculations Supported by TiFlash
summary: Learn the push-down calculations supported by TiFlash.
---

# TiFlash がサポートするプッシュダウン計算 {#push-down-calculations-supported-by-tiflash}

このドキュメントでは、TiFlash でサポートされているプッシュダウン計算について紹介します。

## プッシュダウン演算子 {#push-down-operators}

TiFlash は、次の演算子のプッシュダウンをサポートしています。

-   TableScan: テーブルからデータを読み取ります。
-   選択: データをフィルタリングします。
-   HashAgg: [ハッシュ集計](/explain-aggregation.md#hash-aggregation)アルゴリズムに基づいてデータ集計を実行します。
-   StreamAgg: [ストリーム集計](/explain-aggregation.md#stream-aggregation)アルゴリズムに基づいてデータ集計を実行します。 SteamAgg は`GROUP BY`条件なしの集計のみをサポートします。
-   TopN: TopN 計算を実行します。
-   Limit: リミット計算を実行します。
-   Project: 投影計算を実行します。
-   HashJoin: [ハッシュ結合](/explain-joins.md#hash-join)アルゴリズムを使用して結合計算を実行しますが、次の条件があります。
    -   オペレーターは[MPP モード](/tiflash/use-tiflash-mpp-mode.md)でのみ押し下げることができます。
    -   サポートされている結合は、Inner Join、Left Join、Semi Join、Anti Semi Join、Left Semi Join、Anti Left Semi Join です。
    -   上記の結合は、等結合と非等結合 (デカルト結合) の両方をサポートしています。 Cartesian Join を計算する場合、Shuffle Hash Join アルゴリズムの代わりに Broadcast アルゴリズムが使用されます。
-   ウィンドウ関数: 現在、TiFlash は row_number()、rank()、dense_rank() をサポートしています。

TiDB では、オペレーターはツリー構造で編成されます。オペレータが TiFlash にプッシュされるには、次のすべての前提条件を満たす必要があります。

-   その子オペレーターはすべて TiFlash にプッシュダウンできます。
-   演算子に式が含まれている場合 (ほとんどの演算子には式が含まれています)、演算子のすべての式を TiFlash にプッシュできます。

## 押し下げ式 {#push-down-expressions}

TiFlash は、次のプッシュダウン式をサポートしています。

-   数学関数: `+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32, greatest(int/real), least(int/real)`
-   論理関数: `and, or, not, case when, if, ifnull, isnull, in, like, coalesce, is`
-   ビット演算: `bitand, bitor, bigneg, bitxor`
-   文字列関数: `substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp, regexp`
-   日付関数： `date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add, date_sub, adddate, subdate, quarter, dayname, dayofmonth, dayofweek, dayofyear, last_day, monthname, to_seconds, to_days, from_days, weekofyear`
-   JSON 関数: `json_length`
-   変換関数： `cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string), cast(time as real)`
-   集計関数: `min, max, sum, count, avg, approx_count_distinct, group_concat`
-   その他の関数: `inetntoa, inetaton, inet6ntoa, inet6aton`

## 制限 {#restrictions}

-   Bit、Set、および Geometry タイプを含む式は、TiFlash にプッシュダウンできません。

-   `date_add` 、 `date_sub` 、 `adddate` 、および`subdate`関数は、次の間隔タイプのみをサポートします。他の間隔タイプが使用されている場合、TiFlash はエラーを報告します。

    -   日
    -   週
    -   月
    -   年
    -   時間
    -   分
    -   2番目

サポートされていないプッシュダウン計算がクエリで発生した場合、TiDB は残りの計算を完了する必要があり、TiFlash アクセラレーション効果に大きな影響を与える可能性があります。現在サポートされていない演算子と式は、将来のバージョンでサポートされる可能性があります。
