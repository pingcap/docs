---
title: Push-down calculations Supported by TiFlash
summary: TiFlashは、TableScan、選択、HashAgg、StreamAgg、TopN、リミット、プロジェクト、HashJoin、ウィンドウ関数をサポートしています。TiFlashにプッシュダウンできる式のタイプには、数値関数、論理関数、ビット単位の演算、文字列関数、正規表現の関数、日付関数、JSON関数、変換関数、集計関数、その他の関数があります。ただし、TiFlashにプッシュダウンできない制限もあります。例えば、Bit、Set、Geometryタイプを含む式や一部の関数はTiFlashにプッシュダウンできません。また、ウィンドウ関数の一部もサポートされていません。
---

# TiFlashでサポートされるプッシュダウン計算 {#push-down-calculations-supported-by-tiflash}

このドキュメントでは、 TiFlashでサポートされているプッシュダウン計算を紹介します。

## プッシュダウン演算子 {#push-down-operators}

TiFlash は、次の演算子のプッシュダウンをサポートしています。

-   TableScan: テーブルからデータを読み取ります。
-   選択: データをフィルタリングします。
-   HashAgg: [ハッシュ集計](/explain-aggregation.md#hash-aggregation)アルゴリズムに基づいてデータの集計を実行します。
-   StreamAgg: [ストリーム集計](/explain-aggregation.md#stream-aggregation)アルゴリズムに基づいてデータの集計を実行します。 SteamAgg は`GROUP BY`条件なしの集計のみをサポートします。
-   TopN: TopN 計算を実行します。
-   リミット: リミット計算を実行します。
-   プロジェクト: 投影計算を実行します。
-   HashJoin: [ハッシュ結合](/explain-joins.md#hash-join)アルゴリズムを使用して結合計算を実行しますが、次の条件が適用されます。
    -   オペレータは[MPPモード](/tiflash/use-tiflash-mpp-mode.md)の場合のみ押下可能です。
    -   サポートされている結合は、内部結合、左結合、セミ結合、アンチセミ結合、左セミ結合、およびアンチ左セミ結合です。
    -   前述の結合は、等価結合と非等価結合 (デカルト結合またはヌル認識半結合) の両方をサポートしています。デカルト結合またはヌル認識セミ結合を計算する場合、シャッフル ハッシュ結合アルゴリズムの代わりにブロードキャスト アルゴリズムが使用されます。
-   [ウィンドウ関数](/functions-and-operators/window-functions.md) : 現在、 TiFlash は`ROW_NUMBER()` 、 `RANK()` 、 `DENSE_RANK()` 、 `LEAD()` 、 `LAG()` 、 `FIRST_VALUE()` 、および`LAST_VALUE()`をサポートしています。

TiDB では、オペレーターはツリー構造で編成されます。オペレーターをTiFlashにプッシュダウンするには、次の前提条件をすべて満たす必要があります。

-   その子オペレータはすべてTiFlashにプッシュダウンできます。
-   演算子に式が含まれている場合 (ほとんどの演算子には式が含まれています)、演算子のすべての式をTiFlashにプッシュダウンできます。

## プッシュダウン式 {#push-down-expressions}

TiFlash は、次のプッシュダウン式をサポートしています。

| 式のタイプ                                                                                                   | オペレーション                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| :------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)                                 | `+` `-` `/` `*` `%` `>=` `<=` `=` `!=` `<` `>` `ROUND()` `ABS()` `FLOOR(int)` `CEIL(int)` `CEILING(int)` `SQRT()` `LOG()` `LOG2()` `LOG10()` `LN()` `EXP()` `POW()` `SIGN()` `RADIANS()` `DEGREES()` `CONV()` `CRC32()` `GREATEST(int/real)` `LEAST(int/real)`                                                                                                                                                                                                                                                                                                                      |
| [論理関数](/functions-and-operators/control-flow-functions.md)と[演算子](/functions-and-operators/operators.md) | `AND` 、 `OR` 、 `NOT` 、 `CASE WHEN` 、 `IF()` 、 `IFNULL()` 、 `ISNULL()` 、 `IN` 、 `LIKE` 、 `ILIKE` 、 `COALESCE` 、 `IS`                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [ビット単位の演算](/functions-and-operators/bit-functions-and-operators.md)                                     | `&` (ビット数)、 `|` (bitor)、 `~` (bitneg)、 `^` (bitxor)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [文字列関数](/functions-and-operators/string-functions.md)                                                   | `SUBSTR()` `CHAR_LENGTH()` `REPLACE()` `CONCAT()` `CONCAT_WS()` `LEFT()` `RIGHT()` `ASCII()` `LENGTH()` `TRIM()` `LTRIM()` `RTRIM()` `POSITION()` `FORMAT()` `LOWER()` `UCASE()` `UPPER()` `SUBSTRING_INDEX()` `LPAD()` `RPAD()` `STRCMP()`                                                                                                                                                                                                                                                                                                                                         |
| [正規表現の関数と演算子](/functions-and-operators/string-functions.md)                                             | `REGEXP` `REGEXP_LIKE()` `REGEXP_INSTR()` `REGEXP_SUBSTR()` `REGEXP_REPLACE()` `RLIKE`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [日付関数](/functions-and-operators/date-and-time-functions.md)                                             | `DATE_FORMAT()` `TIMESTAMPDIFF()` `FROM_UNIXTIME()` `UNIX_TIMESTAMP(int)` `UNIX_TIMESTAMP(decimal)` `STR_TO_DATE(date)` `STR_TO_DATE(datetime)` `DATEDIFF()` `YEAR()` `MONTH()` `DAY()` `EXTRACT(datetime)` `DATE()` `HOUR()` `MICROSECOND()` `MINUTE()` `SECOND()` `SYSDATE()` `DATE_ADD/ADDDATE(datetime, int)` `DATE_ADD/ADDDATE(string, int/real)` `DATE_SUB/SUBDATE(datetime, int)` `DATE_SUB/SUBDATE(string, int/real)` `QUARTER()` `DAYNAME()` `DAYOFMONTH()` `DAYOFWEEK()` `DAYOFYEAR()` `LAST_DAY()` `MONTHNAME()` `TO_SECONDS()` `TO_DAYS()` `FROM_DAYS()` `WEEKOFYEAR()` |
| [JSON関数](/functions-and-operators/json-functions.md)                                                    | `JSON_LENGTH()` `->` `->>` `JSON_EXTRACT()`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [変換関数](/functions-and-operators/cast-functions-and-operators.md)                                        | `CAST(int AS DOUBLE), CAST(int AS DECIMAL)` 、 `CAST(int AS STRING)` 、 `CAST(int AS TIME)` 、 `CAST(double AS INT)` 、 `CAST(double AS DECIMAL)` 、 `CAST(double AS STRING)` 、 `CAST(double AS TIME)` 、 `CAST(string AS INT)` `CAST(string AS TIME)` `CAST(string AS DOUBLE), CAST(string AS DECIMAL)` `CAST(decimal AS INT)` 、 20 、 `CAST(decimal AS STRING)` 、 `CAST(decimal AS TIME)` 、 `CAST(time AS INT)` 、 `CAST(time AS DECIMAL)` 、 `CAST(time AS STRING)` 、 `CAST(time AS REAL)`                                                                                                |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)                                        | `MIN()` `MAX()` `SUM()` `COUNT()` `AVG()` `APPROX_COUNT_DISTINCT()` `GROUP_CONCAT()`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                                           | `INET_NTOA()` `INET_ATON()` `INET6_NTOA()` `INET6_ATON()`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

## 制限 {#restrictions}

-   Bit、Set、および Geometry タイプを含む式をTiFlashにプッシュダウンすることはできません。

-   `DATE_ADD()` 、 `DATE_SUB()` 、 `ADDDATE()` 、および`SUBDATE()`関数は、次の間隔タイプのみをサポートします。他の間隔タイプが使用されている場合、 TiFlash はエラーを報告します。

    -   日
    -   週
    -   月
    -   年
    -   時間
    -   分
    -   2番

クエリでサポートされていないプッシュダウン計算が発生した場合、TiDB は残りの計算を完了する必要があり、これはTiFlashアクセラレーション効果に大きな影響を与える可能性があります。現在サポートされていない演算子と式は、将来のバージョンでサポートされる可能性があります。

`MAX()`のような関数は、集計関数として使用される場合はプッシュダウンでサポートされますが、ウィンドウ関数としてはサポートされません。

## 例 {#examples}

このセクションでは、演算子と式をTiFlashにプッシュダウンする例をいくつか示します。

### 例 1: オペレーターをTiFlashにプッシュダウンする {#example-1-push-operators-down-to-tiflash}

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

前の例では、オペレーター`Limit`がデータをフィルタリングするためにTiFlashにプッシュダウンされます。これにより、ネットワーク上で転送されるデータ量が減り、ネットワークのオーバーヘッドが軽減されます。これは、 `Limit_15`演算子の行の`task`列の`mpp[tiflash]`値によって示されます。

### 例 2: 式をTiFlashにプッシュダウンする {#example-2-push-expressions-down-to-tiflash}

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

前の例では、式`id + a`がTiFlashにプッシュダウンされて事前に計算されます。これにより、ネットワーク上で転送されるデータ量が削減され、ネットワーク送信のオーバーヘッドが削減され、全体的な計算パフォーマンスが向上します。これは、 `operator`列の値が`plus(test.t.id, test.t.a)`である行の`task`列の値`mpp[tiflash]`によって示されます。

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

前の例では、 TiFlashに対して`TableFullScan`のみを実行します。他の関数は`root`で計算およびフィルタリングされ、 TiFlashにはプッシュされません。

次のコマンドを実行すると、 TiFlashにプッシュダウンできない演算子と式を特定できます。

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

関数`Time`と`Cast`をTiFlashにプッシュダウンできないため、前の例の式をTiFlashに完全にプッシュダウンすることはできません。

### 例 4: ウィンドウ関数 {#example-4-window-functions}

```sql
CREATE TABLE t(id INT PRIMARY KEY, c1 VARCHAR(100));
ALTER TABLE t SET TIFLASH REPLICA 1;
INSERT INTO t VALUES(1,"foo"),(2,"bar"),(3,"bar foo"),(10,"foo"),(20,"bar"),(30,"bar foo");

EXPLAIN SELECT id, ROW_NUMBER() OVER (PARTITION BY id > 10) FROM t;
+----------------------------------+----------+--------------+---------------+---------------------------------------------------------------------------------------------------------------+
| id                               | estRows  | task         | access object | operator info                                                                                                 |
+----------------------------------+----------+--------------+---------------+---------------------------------------------------------------------------------------------------------------+
| TableReader_30                   | 10000.00 | root         |               | MppVersion: 1, data:ExchangeSender_29                                                                         |
| └─ExchangeSender_29              | 10000.00 | mpp[tiflash] |               | ExchangeType: PassThrough                                                                                     |
|   └─Projection_7                 | 10000.00 | mpp[tiflash] |               | test.t.id, Column#5, stream_count: 4                                                                          |
|     └─Window_28                  | 10000.00 | mpp[tiflash] |               | row_number()->Column#5 over(partition by Column#4 rows between current row and current row), stream_count: 4  |
|       └─Sort_14                  | 10000.00 | mpp[tiflash] |               | Column#4, stream_count: 4                                                                                     |
|         └─ExchangeReceiver_13    | 10000.00 | mpp[tiflash] |               | stream_count: 4                                                                                               |
|           └─ExchangeSender_12    | 10000.00 | mpp[tiflash] |               | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: Column#4, collate: binary], stream_count: 4 |
|             └─Projection_10      | 10000.00 | mpp[tiflash] |               | test.t.id, gt(test.t.id, 10)->Column#4                                                                        |
|               └─TableFullScan_11 | 10000.00 | mpp[tiflash] | table:t       | keep order:false, stats:pseudo                                                                                |
+----------------------------------+----------+--------------+---------------+---------------------------------------------------------------------------------------------------------------+
9 rows in set (0.0073 sec)

```

この出力では、 `Window`オペレーションの`task`列の値が`mpp[tiflash]`であることがわかり、 `ROW_NUMBER() OVER (PARTITION BY id > 10)`オペレーションをTiFlashにプッシュダウンできることを示しています。

```sql
CREATE TABLE t(id INT PRIMARY KEY, c1 VARCHAR(100));
ALTER TABLE t SET TIFLASH REPLICA 1;
INSERT INTO t VALUES(1,"foo"),(2,"bar"),(3,"bar foo"),(10,"foo"),(20,"bar"),(30,"bar foo");

EXPLAIN SELECT id, MAX(id) OVER (PARTITION BY id > 10) FROM t;
+-----------------------------+----------+-----------+---------------+------------------------------------------------------------+
| id                          | estRows  | task      | access object | operator info                                              |
+-----------------------------+----------+-----------+---------------+------------------------------------------------------------+
| Projection_6                | 10000.00 | root      |               | test.t1.id, Column#5                                       |
| └─Shuffle_14                | 10000.00 | root      |               | execution info: concurrency:5, data sources:[Projection_8] |
|   └─Window_7                | 10000.00 | root      |               | max(test.t1.id)->Column#5 over(partition by Column#4)      |
|     └─Sort_13               | 10000.00 | root      |               | Column#4                                                   |
|       └─Projection_8        | 10000.00 | root      |               | test.t1.id, gt(test.t1.id, 10)->Column#4                   |
|         └─TableReader_10    | 10000.00 | root      |               | data:TableFullScan_9                                       |
|           └─TableFullScan_9 | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                             |
+-----------------------------+----------+-----------+---------------+------------------------------------------------------------+
7 rows in set (0.0010 sec)
```

この出力では、 `Window`オペレーションの`task`列の値が`root`であることがわかります。これは、 `MAX(id) OVER (PARTITION BY id > 10)`オペレーションをTiFlashにプッシュダウンできないことを示しています。これは、 `MAX()`は集計関数としてのプッシュダウンのみがサポートされており、ウィンドウ関数としてはサポートされていないためです。
