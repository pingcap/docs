---
title: Push-down calculations Supported by TiFlash
summary: TiFlashでサポートされているプッシュダウン計算について学習します。
---

# TiFlashでサポートされるプッシュダウン計算 {#push-down-calculations-supported-by-tiflash}

このドキュメントでは、 TiFlashでサポートされているプッシュダウン計算について説明します。

## プッシュダウン演算子 {#push-down-operators}

TiFlash は次の演算子のプッシュダウンをサポートしています。

-   TableScan: テーブルからデータを読み取ります。
-   選択: データをフィルタリングします。
-   HashAgg: [ハッシュ集計](/explain-aggregation.md#hash-aggregation)アルゴリズムに基づいてデータ集約を実行します。
-   StreamAgg: [ストリーム集計](/explain-aggregation.md#stream-aggregation)アルゴリズムに基づいてデータ集約を実行します。SteamAgg は`GROUP BY`条件なしの集約のみをサポートします。
-   TopN: TopN 計算を実行します。
-   制限: 制限計算を実行します。
-   投影: 投影計算を実行します。
-   HashJoin: [ハッシュ結合](/explain-joins.md#hash-join)アルゴリズムを使用して結合計算を実行しますが、次の条件が適用されます。
    -   演算子は[MPPモード](/tiflash/use-tiflash-mpp-mode.md)でのみ押すことができます。
    -   サポートされている結合は、Inner Join、Left Join、Semi Join、Anti Semi Join、Left Semi Join、および Anti Left Semi Join です。
    -   上記の結合は、Equi Join と Non-Equi Join（Cartesian Join または Null 対応 Semi Join）の両方をサポートしています。Cartesian Join または Null 対応 Semi Join を計算する際には、Shuffle Hash Join アルゴリズムではなく、Broadcast アルゴリズムが使用されます。
-   [ウィンドウ関数](/functions-and-operators/window-functions.md) : 現在、 TiFlash は`ROW_NUMBER()` 、 `RANK()` 、 `DENSE_RANK()` 、 `LEAD()` 、 `LAG()` 、 `FIRST_VALUE()` 、 `LAST_VALUE()`をサポートしています。

TiDBでは、演算子はツリー構造で編成されます。演算子をTiFlashにプッシュダウンするには、以下のすべての前提条件を満たす必要があります。

-   その子演算子はすべてTiFlashにプッシュダウンできます。
-   演算子に式が含まれている場合 (ほとんどの演算子には式が含まれています)、演算子のすべての式をTiFlashにプッシュダウンできます。

## プッシュダウン式 {#push-down-expressions}

TiFlash は次のプッシュダウン式をサポートしています。

| 表現の種類                                                                                                      | オペレーション                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :--------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)                                    | `+` `-` `/` `*` `%` `>=` `<=` `=` `!=` `<` `>` `ROUND()` `ABS()` `FLOOR(int)` `CEIL(int)` `CEILING(int)` `SQRT()` `LOG()` `LOG2()` `LOG10()` `LN()` `EXP()` `POW()` `POWER()` `SIGN()` `RADIANS()` `DEGREES()` `CONV()` `CRC32()` `GREATEST(int/real)` `LEAST(int/real)`                                                                                                                                                                                                                                                                                                                                                                                          |
| [論理関数](/functions-and-operators/control-flow-functions.md)と[オペレーター](/functions-and-operators/operators.md) | `AND` `OR` `NOT` `CASE WHEN` `IF()` `IFNULL()` `ISNULL()` `IN` `LIKE` `ILIKE` `COALESCE` `IS`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [ビット演算](/functions-and-operators/bit-functions-and-operators.md)                                           | `&` (ビット数)、 `|` (bitor)、 `~` (bitneg)、 `^` (bitxor)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| [文字列関数](/functions-and-operators/string-functions.md)                                                      | `SUBSTR()` `CHAR_LENGTH()` `REPLACE()` `CONCAT()` `CONCAT_WS()` `LEFT()` `RIGHT()` `ASCII()` `LENGTH()` `TRIM()` `LTRIM()` `RTRIM()` `POSITION()` `FORMAT()` `LOWER()` `UCASE()` `UPPER()` `SUBSTRING_INDEX()` `LPAD()` `RPAD()` `STRCMP()`                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [正規表現関数と演算子](/functions-and-operators/string-functions.md)                                                 | `REGEXP` `REGEXP_LIKE()` `REGEXP_INSTR()` `REGEXP_SUBSTR()` `REGEXP_REPLACE()` `RLIKE`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [日付関数](/functions-and-operators/date-and-time-functions.md)                                                | `DATE_FORMAT()` `TIMESTAMPDIFF()` `FROM_UNIXTIME()` `UNIX_TIMESTAMP(int)` `UNIX_TIMESTAMP(decimal)` `STR_TO_DATE(date)` `STR_TO_DATE(datetime)` `DATEDIFF()` `YEAR()` `MONTH()` `DAY()` `EXTRACT(datetime)` `DATE()` `HOUR()` `MICROSECOND()` `MINUTE()` `SECOND()` `SYSDATE()` `DATE_ADD/ADDDATE(datetime, int)` `DATE_ADD/ADDDATE(string, int/real)` `DATE_SUB/SUBDATE(datetime, int)` `DATE_SUB/SUBDATE(string, int/real)` `QUARTER()` `DAYNAME()` `DAYOFMONTH()` `DAYOFWEEK()` `DAYOFYEAR()` `LAST_DAY()` `MONTHNAME()` `TO_SECONDS()` `TO_DAYS()` `FROM_DAYS()` `WEEKOFYEAR()`                                                                               |
| [JSON関数](/functions-and-operators/json-functions.md)                                                       | `JSON_LENGTH()` `->` `->>` `JSON_EXTRACT()` `JSON_ARRAY()` `JSON_DEPTH()` `JSON_VALID()` `JSON_KEYS()` `JSON_CONTAINS_PATH()` `JSON_UNQUOTE()`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [ベクトル関数](/vector-search/vector-search-functions-and-operators.md)                                          | `VEC_L2_DISTANCE` `VEC_COSINE_DISTANCE` `VEC_NEGATIVE_INNER_PRODUCT` `VEC_L1_DISTANCE` `VEC_DIMS` `VEC_L2_NORM` `VEC_AS_TEXT`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [変換関数](/functions-and-operators/cast-functions-and-operators.md)                                           | `CAST(int AS DOUBLE), CAST(int AS DECIMAL)` `CAST(int AS STRING)` `CAST(int AS TIME)` `CAST(double AS INT)` `CAST(double AS DECIMAL)` `CAST(double AS STRING)` `CAST(double AS TIME)` `CAST(string AS INT)` `CAST(string AS DOUBLE), CAST(string AS DECIMAL)` `CAST(string AS TIME)` `CAST(decimal AS INT)` `CAST(decimal AS STRING)` `CAST(decimal AS TIME)` `CAST(decimal AS DOUBLE)` `CAST(time AS INT)` `CAST(time AS DECIMAL)` `CAST(time AS STRING)` `CAST(time AS REAL)` `CAST(json AS JSON)` `CAST(json AS STRING)` `CAST(int AS JSON)` `CAST(real AS JSON)` `CAST(decimal AS JSON)` `CAST(string AS JSON)` `CAST(time AS JSON)` `CAST(duration AS JSON)` |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)                                           | `MIN()` `MAX()` `SUM()` `COUNT()` `AVG()` `APPROX_COUNT_DISTINCT()` `GROUP_CONCAT()`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                                              | `INET_NTOA()` `INET_ATON()` `INET6_NTOA()` `INET6_ATON()`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

## 制限 {#restrictions}

-   Bit、Set、Geometry 型を含む式はTiFlashにプッシュダウンできません。

-   `DATE_ADD()` `SUBDATE()` `ADDDATE()` `DATE_SUB()`以下の間隔タイプのみをサポートします。他の間隔タイプを使用した場合、 TiFlash はエラーを報告します。

    -   日
    -   週
    -   月
    -   年
    -   時間
    -   分
    -   2番

クエリがサポートされていないプッシュダウン計算に遭遇した場合、TiDBは残りの計算を完了する必要があり、 TiFlashの高速化効果に大きく影響する可能性があります。現在サポートされていない演算子と式は、将来のバージョンでサポートされる可能性があります。

`MAX()`ような関数は、集計関数として使用する場合はプッシュダウンがサポートされますが、ウィンドウ関数として使用する場合はサポートされません。

## 例 {#examples}

このセクションでは、演算子と式をTiFlashにプッシュダウンする例をいくつか示します。

### 例1:演算子をTiFlashにプッシュダウンする {#example-1-push-operators-down-to-tiflash}

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

上の例では、演算子`Limit`データのフィルタリングのためにTiFlashにプッシュダウンされており、これによりネットワーク経由で転送されるデータ量が削減され、ネットワークのオーバーヘッドが削減されます。これは、演算子`Limit_15`行の列`task`の値が`mpp[tiflash]`であることで示されています。

### 例2: 式をTiFlashにプッシュダウンする {#example-2-push-expressions-down-to-tiflash}

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

上の例では、式`id + a`計算のために事前にTiFlashにプッシュダウンされています。これにより、ネットワーク経由で転送されるデータ量が削減され、ネットワーク転送のオーバーヘッドが削減され、全体的な計算パフォーマンスが向上します。これは、 `operator`列目に`plus(test.t.id, test.t.a)`値が入った行の`task`列目に`mpp[tiflash]`値が入っていることで示されています。

### 例3: プッシュダウンの制限 {#example-3-restrictions-for-pushdown}

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

上記の例では、 TiFlashに対して`TableFullScan`実行します。その他の関数は`root`で計算およびフィルタリングされ、 TiFlashにはプッシュダウンされません。

次のコマンドを実行すると、 TiFlashにプッシュダウンできない演算子と式を識別できます。

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

前の例の式は、関数`Time`と`Cast` TiFlashにプッシュダウンできないため、 TiFlashに完全にプッシュダウンすることはできません。

### 例4: ウィンドウ関数 {#example-4-window-functions}

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

この出力では、 `Window`操作の`task`列の値が`mpp[tiflash]`であることがわかり、 `ROW_NUMBER() OVER (PARTITION BY id > 10)`操作をTiFlashにプッシュダウンできることがわかります。

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

この出力では、 `Window`操作の`task`列の値が`root`あることがわかります。これは、 `MAX(id) OVER (PARTITION BY id > 10)`操作をTiFlashにプッシュダウンできないことを示しています。これは、 `MAX()`プッシュダウンで集計関数としてのみサポートされており、ウィンドウ関数としてはサポートされていないためです。
