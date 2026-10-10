---
title: SUM
summary: 値の集合の合計を計算します。
---

# SUM

値の集合の合計を計算します。

- NULL 値は無視されます。
- 数値型および interval 型をサポートします。

## 構文 {#syntax}

```sql
SUM(<expr>)
```

## 戻り値の型 {#return-type}

入力型と同じです。

## 例 {#examples}

この例では、INTEGER、DOUBLE、および INTERVAL カラムを持つテーブルを作成し、データを挿入して、SUM を使用して各カラムの合計を計算する方法を示します。

```sql
-- Create a table with integer, double, and interval columns
CREATE TABLE sum_example (
    id INT,
    int_col INTEGER,
    double_col DOUBLE,
    interval_col INTERVAL
);

-- Insert data
INSERT INTO sum_example VALUES
(1, 10, 15.5, INTERVAL '2 days'),
(2, 20, 25.7, INTERVAL '3 days'),
(3, NULL, 5.2, INTERVAL '1 day'),
(4, 30, 40.1, INTERVAL '4 days');

-- Calculate the sum for each column
SELECT
    SUM(int_col) AS total_integer,
    SUM(double_col) AS total_double,
    SUM(interval_col) AS total_interval
FROM sum_example;
```

期待される出力:

```sql
-- NULL values are ignored.
-- SUM(interval_col) returns 240:00:00 (10 days).

┌──────────────────────────────────────────────────────────┐
│  total_integer  │    total_double   │   total_interval   │
├─────────────────┼───────────────────┼────────────────────┤
│              60 │              86.5 │ 240:00:00          │
└──────────────────────────────────────────────────────────┘
```