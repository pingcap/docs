---
title: TiFlash 支持的下推计算
summary: 了解 TiFlash 支持的下推计算。
---

# TiFlash 支持的下推计算

本文档介绍了 TiFlash 支持的下推计算。

## 下推操作符

TiFlash 支持以下操作符的下推：

* TableScan：读取表中的数据。
* Selection：筛选数据。
* HashAgg：基于 [Hash Aggregation](/explain-aggregation.md#hash-aggregation) 算法进行数据聚合。
* StreamAgg：基于 [Stream Aggregation](/explain-aggregation.md#stream-aggregation) 算法进行数据聚合。StreamAgg 仅支持无 `GROUP BY` 条件的聚合。
* TopN：执行 TopN 计算。
* Limit：执行 Limit 计算。
* Project：执行投影计算。
* HashJoin：使用 [Hash Join](/explain-joins.md#hash-join) 算法进行连接计算，但有以下条件：
    * 该操作符仅在 [MPP mode](/tiflash/use-tiflash-mpp-mode.md) 下可以下推。
    * 支持的连接类型包括 Inner Join、Left Join、Semi Join、Anti Semi Join、Left Semi Join 和 Anti Left Semi Join。
    * 以上连接支持 Equi Join 和 Non-Equi Join（笛卡尔积连接或 Null-aware Semi Join）。在计算笛卡尔积连接或 Null-aware Semi Join 时，使用广播算法，而非 Shuffle Hash Join 算法。
* [Window functions](/functions-and-operators/window-functions.md)：目前，TiFlash 支持 `ROW_NUMBER()`、`RANK()`、`DENSE_RANK()`、`LEAD()`、`LAG()`、`FIRST_VALUE()` 和 `LAST_VALUE()`。

在 TiDB 中，操作符以树结构组织。要将操作符下推到 TiFlash，必须满足以下所有前提条件：

+ 它的所有子操作符都可以下推到 TiFlash。
+ 如果操作符包含表达式（大多数操作符都包含表达式），那么该操作符的所有表达式都可以下推到 TiFlash。

## 下推表达式

TiFlash 支持以下下推表达式：

| 表达式类型 | 支持的操作 |
| :-------------- | :------------------------------------- |
| [数值函数和操作符](/functions-and-operators/numeric-functions-and-operators.md) | `+`, `-`, `/`, `*`, `%`, `>=`, `<=`, `=`, `!=`, `<`, `>`, `ROUND()`, `ABS()`, `FLOOR(int)`, `CEIL(int)`, `CEILING(int)`, `SQRT()`, `LOG()`, `LOG2()`, `LOG10()`, `LN()`, `EXP()`, `POW()`, `POWER()`, `SIGN()`, `RADIANS()`, `DEGREES()`, `CONV()`, `CRC32()`, `GREATEST(int/real)`, `LEAST(int/real)` |
| [逻辑函数](/functions-and-operators/control-flow-functions.md) 和 [操作符](/functions-and-operators/operators.md) | `AND`, `OR`, `NOT`, `CASE WHEN`, `IF()`, `IFNULL()`, `ISNULL()`, `IN`, `LIKE`, `ILIKE`, `COALESCE`, `IS` |
| [位操作](/functions-and-operators/bit-functions-and-operators.md) | `&` (位与), <code>\|</code> (位或), `~` (位取反), `^` (位异或) |
| [字符串函数](/functions-and-operators/string-functions.md) | `SUBSTR()`, `CHAR_LENGTH()`, `REPLACE()`, `CONCAT()`, `CONCAT_WS()`, `LEFT()`, `RIGHT()`, `ASCII()`, `LENGTH()`, `TRIM()`, `LTRIM()`, `RTRIM()`, `POSITION()`, `FORMAT()`, `LOWER()`, `UCASE()`, `UPPER()`, `SUBSTRING_INDEX()`, `LPAD()`, `RPAD()`, `STRCMP()` |
| [正则表达式函数和操作符](/functions-and-operators/string-functions.md) | `REGEXP`, `REGEXP_LIKE()`, `REGEXP_INSTR()`, `REGEXP_SUBSTR()`, `REGEXP_REPLACE()`, `RLIKE` |
| [日期函数](/functions-and-operators/date-and-time-functions.md) | `DATE_FORMAT()`, `TIMESTAMPDIFF()`, `FROM_UNIXTIME()`, `UNIX_TIMESTAMP(int)`, `UNIX_TIMESTAMP(decimal)`, `STR_TO_DATE(date)`, `STR_TO_DATE(datetime)`, `DATEDIFF()`, `YEAR()`, `MONTH()`, `DAY()`, `EXTRACT(datetime)`, `DATE()`, `HOUR()`, `MICROSECOND()`, `MINUTE()`, `SECOND()`, `SYSDATE()`, `DATE_ADD/ADDDATE(datetime, int)`, `DATE_ADD/ADDDATE(string, int/real)`, `DATE_SUB/SUBDATE(datetime, int)`, `DATE_SUB/SUBDATE(string, int/real)`, `QUARTER()`, `DAYNAME()`, `DAYOFMONTH()`, `DAYOFWEEK()`, `DAYOFYEAR()`, `LAST_DAY()`, `MONTHNAME()`, `TO_SECONDS()`, `TO_DAYS()`, `FROM_DAYS()`, `WEEKOFYEAR()` |
| [JSON 函数](/functions-and-operators/json-functions.md) | `JSON_LENGTH()`, `->`, `->>`, `JSON_EXTRACT()`, `JSON_ARRAY()`, `JSON_DEPTH()`, `JSON_VALID()`, `JSON_KEYS()`, `JSON_CONTAINS_PATH()`, `JSON_UNQUOTE()` |
| [向量函数](/vector-search/vector-search-functions-and-operators.md) | `VEC_L2_DISTANCE`, `VEC_COSINE_DISTANCE`, `VEC_NEGATIVE_INNER_PRODUCT`, `VEC_L1_DISTANCE`, `VEC_DIMS`, `VEC_L2_NORM`, `VEC_AS_TEXT` |
| [转换函数](/functions-and-operators/cast-functions-and-operators.md) | `CAST(int AS DOUBLE), CAST(int AS DECIMAL)`, `CAST(int AS STRING)`, `CAST(int AS TIME)`, `CAST(double AS INT)`, `CAST(double AS DECIMAL)`, `CAST(double AS STRING)`, `CAST(double AS TIME)`, `CAST(string AS INT)`, `CAST(string AS DOUBLE), CAST(string AS DECIMAL)`, `CAST(string AS TIME)`, `CAST(decimal AS INT)`, `CAST(decimal AS STRING)`, `CAST(decimal AS TIME)`, `CAST(decimal AS DOUBLE)`, `CAST(time AS INT)`, `CAST(time AS DECIMAL)`, `CAST(time AS STRING)`, `CAST(time AS REAL)`, `CAST(json AS JSON)`, `CAST(json AS STRING)`, `CAST(int AS JSON)`, `CAST(real AS JSON)`, `CAST(decimal AS JSON)`, `CAST(string AS JSON)`, `CAST(time AS JSON)`, `CAST(duration AS JSON)` |
| [聚合函数](/functions-and-operators/aggregate-group-by-functions.md) | `MIN()`, `MAX()`, `SUM()`, `COUNT()`, `AVG()`, `APPROX_COUNT_DISTINCT()`, `GROUP_CONCAT()` |
| [其他函数](/functions-and-operators/miscellaneous-functions.md) | `INET_NTOA()`, `INET_ATON()`, `INET6_NTOA()`, `INET6_ATON()` |

## 限制条件

* 包含 Bit、Set 和 Geometry 类型的表达式不能下推到 TiFlash。

* `DATE_ADD()`、`DATE_SUB()`、`ADDDATE()` 和 `SUBDATE()` 函数仅支持以下时间间隔类型。如果使用其他时间间隔类型，TiFlash 会报错。

    * DAY
    * WEEK
    * MONTH
    * YEAR
    * HOUR
    * MINUTE
    * SECOND

如果查询遇到不支持下推的计算，TiDB 需要完成剩余的计算，这可能会大大影响 TiFlash 的加速效果。目前不支持的操作符和表达式，未来版本可能会支持。

像 `MAX()` 这样的函数在作为聚合函数使用时支持下推，但作为窗口函数则不支持。

## 示例

本节提供一些将操作符和表达式下推到 TiFlash 的示例。

### 示例 1：将操作符下推到 TiFlash

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
```

在上述示例中，操作符 `Limit` 被下推到 TiFlash 进行数据筛选，有助于减少需要传输的数据量，降低网络开销。这由 `task` 列中 `mpp[tiflash]` 的值在 `Limit_15` 操作符行中体现。

### 示例 2：将表达式下推到 TiFlash

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
```

在上述示例中，表达式 `id + a` 被提前下推到 TiFlash 进行计算。这有助于减少网络传输的数据量，从而降低网络传输开销并提升整体计算性能。这由 `task` 列中 `mpp[tiflash]` 和 `operator` 列中的 `plus(test.t.id, test.t.a)` 表达式体现。

### 示例 3：下推限制

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
```

上述示例仅在 TiFlash 上执行了 `TableFullScan`。其他函数在 `root` 上计算和筛选，没有下推到 TiFlash。

你可以通过运行以下命令，识别不能下推到 TiFlash 的操作符和表达式：

```sql
SHOW WARNINGS;

+---------+------+------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                            |
+---------+------+------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | Scalar function 'time'(signature: Time, return type: time) 目前不支持下推到存储层。                                              |
| Warning | 1105 | Scalar function 'cast'(signature: CastDurationAsString, return type: var_string(10)) 目前不支持下推到 tiflash。                |
| Warning | 1105 | Scalar function 'cast'(signature: CastDurationAsString, return type: var_string(10)) 目前不支持下推到 tiflash。                |
+---------+------+------------------------------------------------------------------------------------------------------------------------------------+
```

上述示例中的表达式不能完全下推到 TiFlash，因为 `Time` 和 `Cast` 函数不能下推。

### 示例 4：窗口函数

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
```

在此输出中，可以看到 `Window` 操作的 `task` 列值为 `mpp[tiflash]`，表示 `ROW_NUMBER() OVER (PARTITION BY id > 10)` 操作可以下推到 TiFlash。

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
```

在此输出中，可以看到 `Window` 操作的 `task` 列值为 `root`，表示 `MAX(id) OVER (PARTITION BY id > 10)` 操作不能下推到 TiFlash。这是因为 `MAX()` 仅作为聚合函数支持下推，而不支持作为窗口函数。