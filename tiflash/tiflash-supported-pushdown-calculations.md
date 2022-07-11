---
title: Push-down calculations Supported by TiFlash
summary: Learn the push-down calculations supported by TiFlash.
---

# TiFlashでサポートされているプッシュダウン計算 {#push-down-calculations-supported-by-tiflash}

このドキュメントでは、TiFlashでサポートされているプッシュダウン計算を紹介します。

## プッシュダウン演算子 {#push-down-operators}

TiFlashは、次の演算子のプッシュダウンをサポートしています。

-   TableScan：テーブルからデータを読み取ります。
-   選択：データをフィルタリングします。
-   HashAgg： [ハッシュ集計](/explain-aggregation.md#hash-aggregation)アルゴリズムに基づいてデータ集約を実行します。
-   StreamAgg： [ストリーム集計](/explain-aggregation.md#stream-aggregation)のアルゴリズムに基づいてデータ集約を実行します。 SteamAggは、 `GROUP BY`の条件なしで集約のみをサポートします。
-   TopN：TopN計算を実行します。
-   制限：制限計算を実行します。
-   プロジェクト：投影計算を実行します。
-   HashJoin： [ハッシュ参加](/explain-joins.md#hash-join)アルゴリズムを使用して結合計算を実行しますが、次の条件があります。
    -   オペレーターは[MPPモード](/tiflash/use-tiflash-mpp-mode.md)でのみ押し下げることができます。
    -   サポートされている結合は、内部結合、左結合、半結合、反半結合、左半結合、および反左半結合です。
    -   上記の結合は、等式結合と非等式結合（デカルト結合）の両方をサポートします。デカルト結合を計算するときは、シャッフルハッシュ結合アルゴリズムの代わりにブロードキャストアルゴリズムが使用されます。
-   ウィンドウ関数：現在、TiFlashはrow_number（）、rank（）、dense_rank（）をサポートしています。

TiDBでは、演算子はツリー構造で編成されています。オペレーターをTiFlashにプッシュダウンするには、次のすべての前提条件が満たされている必要があります。

-   その子演算子はすべてTiFlashにプッシュダウンできます。
-   演算子に式が含まれている場合（ほとんどの演算子に式が含まれている場合）、演算子のすべての式をTiFlashにプッシュダウンできます。

## プッシュダウン式 {#push-down-expressions}

TiFlashは、次のプッシュダウン式をサポートしています。

-   数学関数： `+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32, greatest(int/real), least(int/real)`
-   論理関数： `and, or, not, case when, if, ifnull, isnull, in, like, coalesce, is`
-   ビット演算： `bitand, bitor, bigneg, bitxor`
-   文字列関数： `substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp, regexp`
-   日付関数： `date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add, date_sub, adddate, subdate, quarter, dayname, dayofmonth, dayofweek, dayofyear, last_day, monthname, to_seconds, to_days, from_days, weekofyear`
-   JSON関数： `json_length`
-   変換関数： `cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string), cast(time as real)`
-   集計関数： `min, max, sum, count, avg, approx_count_distinct, group_concat`
-   その他の関数： `inetntoa, inetaton, inet6ntoa, inet6aton`

## 制限 {#restrictions}

-   Bit、Set、およびGeometryタイプを含む式は、TiFlashにプッシュダウンできません。

-   `date_add` 、 `subdate` `date_sub`は、次の間隔タイプのみをサポートし`adddate` 。他の間隔タイプが使用されている場合、TiFlashはエラーを報告します。

    -   日
    -   週
    -   月
    -   年
    -   時間
    -   分
    -   2番目

クエリでサポートされていないプッシュダウン計算が発生した場合、TiDBは残りの計算を完了する必要があります。これは、TiFlashアクセラレーション効果に大きな影響を与える可能性があります。現在サポートされていない演算子と式は、将来のバージョンでサポートされる可能性があります。
