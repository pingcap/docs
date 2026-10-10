---
title: GENERATE_SERIES
summary: 指定した開始点から別の指定した終了点まで、必要に応じて増分値を指定してデータセットを生成します。GENERATE_SERIES 関数は、以下のデータ型で動作します。
---

# GENERATE_SERIES

指定した開始点から別の指定した終了点まで、必要に応じて増分値を指定してデータセットを生成します。GENERATE_SERIES 関数は、以下のデータ型で動作します。

- Integer
- Date
- Timestamp

## 構文 {#syntax}

```sql
GENERATE_SERIES(<start>, <stop>[, <step_interval>])
```

## 引数 {#arguments}

| 引数 | 説明 |
|--------------- |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| start          | 開始値です。シーケンス内の最初の数値、日付、または timestamp を表します。 |
| stop           | 終了値です。シーケンス内の最後の数値、日付、または timestamp を表します。 |
| step_interval  | ステップ間隔です。シーケンス内で隣接する値の差を決定します。整数シーケンスのデフォルト値は 1 です。日付シーケンスのデフォルトのステップ間隔は 1 日です。timestamp シーケンスのデフォルトのステップ間隔は 1 マイクロ秒です。 |

> **Note:**
>
> GENERATE_SERIES や RANGE のような関数を扱う際、重要な違いは境界の特性にあります。GENERATE_SERIES は左端と右端の両方を含みますが、RANGE は左端のみを含みます。たとえば、RANGE(1, 11) を使用することは GENERATE_SERIES(1, 10) と同等です。

## 戻り値の型 {#return-type}

*start* から *stop* までの連続した数値、日付、または timestamp のシーケンスを含むリストを返します。

## 例 {#examples}

### 例 1: 数値、日付、Timestamp データの生成 {#example-1-generating-numeric-date-and-timestamp-data}

```sql
SELECT * FROM GENERATE_SERIES(1, 10, 2);

generate_series|
---------------+
              1|
              3|
              5|
              7|
              9|

SELECT * FROM GENERATE_SERIES('2023-03-20'::date, '2023-03-27'::date);

generate_series|
---------------+
     2023-03-20|
     2023-03-21|
     2023-03-22|
     2023-03-23|
     2023-03-24|
     2023-03-25|
     2023-03-26|
     2023-03-27|

SELECT * FROM GENERATE_SERIES('2023-03-26 00:00'::timestamp, '2023-03-27 12:00'::timestamp, 86400000000);

generate_series    |
-------------------+
2023-03-26 00:00:00|
2023-03-27 00:00:00|
```

### 例 2: クエリ結果の欠損を埋める {#example-2-filling-query-result-gaps}

この例では、GENERATE_SERIES 関数と left join 演算子を使用して、特定の範囲で情報が欠落していることによって生じるクエリ結果の欠損を処理します。

```sql
CREATE TABLE t_metrics (
  date Date,
  value INT
);

INSERT INTO t_metrics VALUES
  ('2020-01-01', 200),
  ('2020-01-01', 300),
  ('2020-01-04', 300),
  ('2020-01-04', 300),
  ('2020-01-05', 400),
  ('2020-01-10', 700);

SELECT date, SUM(value), COUNT() FROM t_metrics GROUP BY date ORDER BY date;

date      |sum(value)|count()|
----------+----------+-------+
2020-01-01|       500|      2|
2020-01-04|       600|      2|
2020-01-05|       400|      1|
2020-01-10|       700|      1|
```

2020 年 1 月 1 日から 2020 年 1 月 10 日までの欠損を埋めるには、次のクエリを使用します。

```sql
SELECT t.date, COALESCE(SUM(t_metrics.value), 0), COUNT(t_metrics.value)
FROM generate_series(
  '2020-01-01'::Date,
  '2020-01-10'::Date
) AS t(date)
LEFT JOIN t_metrics ON t_metrics.date = t.date
GROUP BY t.date ORDER BY t.date;

date      |coalesce(sum(t_metrics.value), 0)|count(t_metrics.value)|
----------+---------------------------------+----------------------+
2020-01-01|                              500|                     2|
2020-01-02|                                0|                     0|
2020-01-03|                                0|                     0|
2020-01-04|                              600|                     2|
2020-01-05|                              400|                     1|
2020-01-06|                                0|                     0|
2020-01-07|                                0|                     0|
2020-01-08|                                0|                     0|
2020-01-09|                                0|                     0|
2020-01-10|                              700|                     1|
```