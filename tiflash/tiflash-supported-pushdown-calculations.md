---
title: Push-down calculations Supported by TiFlash
summary: Learn the push-down calculations supported by TiFlash.
---

# TiFlashがサポートするプッシュダウン計算 {#push-down-calculations-supported-by-tiflash}

このドキュメントでは、 TiFlashでサポートされているプッシュダウン計算について紹介します。

## プッシュダウン演算子 {#push-down-operators}

TiFlashは、次の演算子のプッシュダウンをサポートしています。

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
-   ウィンドウ関数: 現在、 TiFlashは row_number()、rank()、dense_rank()、lead()、および lag() をサポートしています。

TiDB では、オペレーターはツリー構造で編成されています。オペレータがTiFlashにプッシュされるには、次のすべての前提条件を満たす必要があります。

-   その子演算子はすべてTiFlashにプッシュできます。
-   演算子に式が含まれる場合 (ほとんどの演算子には式が含まれます)、演算子のすべての式をTiFlashにプッシュできます。

## 押し下げ式 {#push-down-expressions}

TiFlashは、次のプッシュダウン式をサポートしています。

-   数学関数: `+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32, greatest(int/real), least(int/real)`
-   論理関数: `and, or, not, case when, if, ifnull, isnull, in, like, coalesce, is`
-   ビット演算: `bitand, bitor, bigneg, bitxor`
-   文字列関数: `substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp, regexp, regexp_like, regexp_instr, regexp_substr`
-   日付関数： `date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add, date_sub, adddate, subdate, quarter, dayname, dayofmonth, dayofweek, dayofyear, last_day, monthname, to_seconds, to_days, from_days, weekofyear`
-   JSON 関数: `json_length, ->, ->>, json_extract`
-   変換関数： `cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string), cast(time as real)`
-   集計関数: `min, max, sum, count, avg, approx_count_distinct, group_concat`
-   その他の関数: `inetntoa, inetaton, inet6ntoa, inet6aton`

## 制限 {#restrictions}

-   Bit、Set、および Geometry タイプを含む式は、 TiFlashにプッシュダウンできません。

-   `date_add` 、 `date_sub` 、 `adddate` 、および`subdate`関数は、次の間隔タイプのみをサポートします。他の間隔タイプが使用されている場合、 TiFlashはエラーを報告します。

    -   日
    -   週
    -   月
    -   年
    -   時間
    -   分
    -   2番目

サポートされていないプッシュダウン計算がクエリで発生した場合、TiDB は残りの計算を完了する必要があり、 TiFlashアクセラレーション効果に大きな影響を与える可能性があります。現在サポートされていない演算子と式は、将来のバージョンでサポートされる可能性があります。

## 例 {#examples}

このセクションでは、演算子と式をTiFlashにプッシュ ダウンする例をいくつか示します。

### 例 1: オペレータをTiFlashにプッシュします {#example-1-push-operators-down-to-tiflash}

```sql
CREATE TABLE t(id INT PRIMARY KEY, a INT);
ALTER TABLE t SET TIFLASH REPLICA 1;

EXPLAIN SELECT * FROM t LIMIT 3;

+------------------------------+---------+--------------+---------------+--------------------------------+
| id                           | estRows | task         | access object | operator info                  |
+------------------------------+---------+--------------+---------------+--------------------------------+
| Limit_9                      | 3.00    | root         |               | offset:0, count:3              |
| └─TableReader_17             | 3.00    | root         |               | data:ExchangeSender_16         |
|   └─ExchangeSender_16        | 3.00    | mpp[tiflash] |               | ExchangeType: PassThrough      |
|     └─Limit_15               | 3.00    | mpp[tiflash] |               | offset:0, count:3              |
|       └─TableFullScan_14     | 3.00    | mpp[tiflash] | table:t       | keep order:false, stats:pseudo |
+------------------------------+---------+--------------+---------------+--------------------------------+
5 rows in set (0.18 sec)
```

前の例では、オペレータ`Limit`はデータをフィルタリングするためにTiFlashにプッシュ ダウンされます。これにより、ネットワーク経由で転送されるデータの量が減り、ネットワーク オーバーヘッドが削減されます。

### 例 2: 式をTiFlashにプッシュする {#example-2-push-expressions-down-to-tiflash}

```sql
CREATE TABLE t(id INT PRIMARY KEY, a INT);
ALTER TABLE t SET TIFLASH REPLICA 1;
INSERT INTO t(id,a) VALUES (1,2),(2,4),(11,2),(12,4),(13,4),(14,7);

EXPLAIN SELECT MAX(id + a) FROM t GROUP BY a;

+------------------------------------+---------+--------------+---------------+---------------------------------------------------------------------------+
| id                                 | estRows | task         | access object | operator info                                                             |
+------------------------------------+---------+--------------+---------------+---------------------------------------------------------------------------+
| TableReader_45                     | 4.80    | root         |               | data:ExchangeSender_44                                                    |
| └─ExchangeSender_44                | 4.80    | mpp[tiflash] |               | ExchangeType: PassThrough                                                 |
|   └─Projection_39                  | 4.80    | mpp[tiflash] |               | Column#3                                                                  |
|     └─HashAgg_37                   | 4.80    | mpp[tiflash] |               | group by:Column#9, funcs:max(Column#8)->Column#3                          |
|       └─Projection_46              | 6.00    | mpp[tiflash] |               | plus(test.t.id, test.t.a)->Column#8, test.t.a                             |
|         └─ExchangeReceiver_23      | 6.00    | mpp[tiflash] |               |                                                                           |
|           └─ExchangeSender_22      | 6.00    | mpp[tiflash] |               | ExchangeType: HashPartition, Hash Cols: [name: test.t.a, collate: binary] |
|             └─TableFullScan_21     | 6.00    | mpp[tiflash] | table:t       | keep order:false, stats:pseudo                                            |
+------------------------------------+---------+--------------+---------------+---------------------------------------------------------------------------+
8 rows in set (0.18 sec)
```

前の例では、式`id + a`が事前に計算のためにTiFlashにプッシュされます。これにより、ネットワークを介して転送されるデータの量が減るため、ネットワーク転送のオーバーヘッドが削減され、全体的な計算パフォーマンスが向上します。

### 例 3: プッシュダウンの制限 {#example-3-restrictions-for-pushdown}

```sql
CREATE TABLE t(id INT PRIMARY KEY, a INT);
ALTER TABLE t SET TIFLASH REPLICA 1;
INSERT INTO t(id,a) VALUES (1,2),(2,4),(11,2),(12,4),(13,4),(14,7);

EXPLAIN SELECT id FROM t WHERE TIME(now()+ a) < '12:00:00';

+-----------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------+
| id                          | estRows | task         | access object | operator info                                                                                    |
+-----------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------+
| Projection_4                | 4.80    | root         |               | test.t.id                                                                                        |
| └─Selection_6               | 4.80    | root         |               | lt(cast(time(cast(plus(20230110083056, test.t.a), var_string(20))), var_string(10)), "12:00:00") |
|   └─TableReader_11          | 6.00    | root         |               | data:ExchangeSender_10                                                                           |
|     └─ExchangeSender_10     | 6.00    | mpp[tiflash] |               | ExchangeType: PassThrough                                                                        |
|       └─TableFullScan_9     | 6.00    | mpp[tiflash] | table:t       | keep order:false, stats:pseudo                                                                   |
+-----------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------+
5 rows in set, 3 warnings (0.20 sec)
```

前の例は、 TiFlashで`TableFullScan`のみを実行します。他の関数は`root`で計算およびフィルタリングされ、 TiFlashにはプッシュされません。

次のコマンドを実行して、 TiFlashにプッシュダウンできない演算子と式を特定できます。

```sql
SHOW WARNINGS;

+---------+------+------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                            |
+---------+------+------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | Scalar function 'time'(signature: Time, return type: time) is not supported to push down to storage layer now.                     |
| Warning | 1105 | Scalar function 'cast'(signature: CastDurationAsString, return type: var_string(10)) is not supported to push down to tiflash now. |
| Warning | 1105 | Scalar function 'cast'(signature: CastDurationAsString, return type: var_string(10)) is not supported to push down to tiflash now. |
+---------+------+------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.18 sec)
```

関数`Time`と`Cast`をTiFlashにプッシュダウンできないため、前の例の式を完全にTiFlashにプッシュダウンすることはできません。
