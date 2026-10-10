---
title: RANGE BETWEEN
summary: ウィンドウ関数に対して、値ベースの境界を使用してウィンドウフレームを定義します。
---

# RANGE BETWEEN

ウィンドウ関数に対して、値ベースの境界を使用してウィンドウフレームを定義します。

## 概要 {#overview}

`RANGE BETWEEN` 句は、物理的な行数ではなく論理的な値の範囲に基づいて、ウィンドウフレームに含める行を指定します。これは、時間ベースのウィンドウ、値ベースのグループ化、重複値の処理に特に役立ちます。

## 構文 {#syntax}

```sql
FUNCTION() OVER (
    [ PARTITION BY partition_expression ]
    [ ORDER BY sort_expression ]
    RANGE BETWEEN frame_start AND frame_end
)
```

### フレーム境界 {#frame-boundaries}

| 境界 | 説明 | 例 |
|----------|-------------|---------|
| `UNBOUNDED PRECEDING` | パーティションの先頭 | `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| `value PRECEDING` | 現在の行より前の値範囲 | `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW` |
| `CURRENT ROW` | 現在の行の値 | `RANGE BETWEEN CURRENT ROW AND CURRENT ROW` |
| `value FOLLOWING` | 現在の行より後の値範囲 | `RANGE BETWEEN CURRENT ROW AND INTERVAL '7' DAY FOLLOWING` |
| `UNBOUNDED FOLLOWING` | パーティションの末尾 | `RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` |

## RANGE と ROWS の比較 {#range-vs-rows}

| 観点 | RANGE | ROWS |
|--------|-------|------|
| **定義** | 論理的な値範囲 | 物理的な行数 |
| **境界** | 値ベースの位置 | 行位置 |
| **同順位値** | 同じ値は同じフレームを共有 | 各行は独立 |
| **パフォーマンス** | 重複があると遅くなる場合がある | 一般的に高速 |
| **ユースケース** | 時間ベースのウィンドウ、パーセンタイル計算 | 移動平均、累積合計 |

## RANGE で使用できる値の型 {#value-types-for-range}

### 1. 数値 {#1-numeric-values}

```sql
-- Include rows within ±10 units
RANGE BETWEEN 10 PRECEDING AND 10 FOLLOWING

-- Include rows with values up to 50 less than current
RANGE BETWEEN 50 PRECEDING AND CURRENT ROW
```

### 2. Interval 値（DATE/TIMESTAMP 用） {#2-interval-values-for-date-timestamp}

```sql
-- 7-day window
RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW

-- 1-hour window
RANGE BETWEEN INTERVAL '1' HOUR PRECEDING AND CURRENT ROW

-- 30-minute centered window
RANGE BETWEEN INTERVAL '15' MINUTE PRECEDING AND INTERVAL '15' MINUTE FOLLOWING
```

### 3. 値を指定しない場合（デフォルト） {#3-no-value-specified-default}

`PRECEDING` または `FOLLOWING` に値を指定しない場合、デフォルトは `CURRENT ROW` になります。

```sql
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  -- Default behavior
```

## 例 {#examples}

### サンプルデータ {#sample-data}

```sql
CREATE TABLE temperature_readings (
    reading_time TIMESTAMP,
    sensor_id VARCHAR(10),
    temperature DECIMAL(5,2)
);

INSERT INTO temperature_readings VALUES
    ('2024-01-01 00:00:00', 'S1', 20.5),
    ('2024-01-01 01:00:00', 'S1', 21.0),
    ('2024-01-01 02:00:00', 'S1', 20.8),
    ('2024-01-01 03:00:00', 'S1', 22.1),
    ('2024-01-01 04:00:00', 'S1', 21.5),
    ('2024-01-01 00:00:00', 'S2', 19.8),
    ('2024-01-01 01:00:00', 'S2', 20.2),
    ('2024-01-01 02:00:00', 'S2', 19.9),
    ('2024-01-01 03:00:00', 'S2', 21.0),
    ('2024-01-01 04:00:00', 'S2', 20.5);
```

### 1. 24 時間の移動平均 {#1-24-hour-rolling-average}

```sql
SELECT reading_time, sensor_id, temperature,
       AVG(temperature) OVER (
           PARTITION BY sensor_id
           ORDER BY reading_time
           RANGE BETWEEN INTERVAL '24' HOUR PRECEDING AND CURRENT ROW
       ) AS avg_24h
FROM temperature_readings
ORDER BY sensor_id, reading_time;
```

### 2. 値ベースのウィンドウ（±0.5 度以内） {#2-value-based-window-within-05-degrees}

```sql
SELECT reading_time, sensor_id, temperature,
       COUNT(*) OVER (
           PARTITION BY sensor_id
           ORDER BY temperature
           RANGE BETWEEN 0.5 PRECEDING AND 0.5 FOLLOWING
       ) AS similar_readings_count
FROM temperature_readings
ORDER BY sensor_id, temperature;
```

### 3. 重複値の処理 {#3-handling-duplicate-values}

```sql
CREATE TABLE sales_duplicates (
    sale_date DATE,
    amount DECIMAL(10,2)
);

INSERT INTO sales_duplicates VALUES
    ('2024-01-01', 100.00),
    ('2024-01-01', 100.00),  -- Duplicate date
    ('2024-01-02', 150.00),
    ('2024-01-03', 200.00),
    ('2024-01-03', 200.00);  -- Duplicate date

-- RANGE treats duplicate dates as the same "row" for window calculations
SELECT sale_date, amount,
       SUM(amount) OVER (
           ORDER BY sale_date
           RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total_range,
       SUM(amount) OVER (
           ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total_rows
FROM sales_duplicates
ORDER BY sale_date;
```

**結果の比較:**

```
sale_date   | amount | running_total_range | running_total_rows
------------+--------+---------------------+--------------------
2024-01-01  | 100.00 | 200.00              | 100.00
2024-01-01  | 100.00 | 200.00              | 200.00  -- ROWS: different
2024-01-02  | 150.00 | 350.00              | 350.00
2024-01-03  | 200.00 | 750.00              | 550.00
2024-01-03  | 200.00 | 750.00              | 750.00  -- ROWS: different
```

### 4. 時間ベースの中央寄せウィンドウ {#4-time-based-centered-window}

```sql
SELECT reading_time, sensor_id, temperature,
       AVG(temperature) OVER (
           PARTITION BY sensor_id
           ORDER BY reading_time
           RANGE BETWEEN INTERVAL '30' MINUTE PRECEDING
                     AND INTERVAL '30' MINUTE FOLLOWING
       ) AS avg_hour_centered
FROM temperature_readings
ORDER BY sensor_id, reading_time;
```

## 一般的なパターン {#common-patterns}

### 時間ベースのウィンドウ {#time-based-windows}

**構文例:**

```sql
-- 7-day rolling window
RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW

-- 1-hour centered window
RANGE BETWEEN INTERVAL '30' MINUTE PRECEDING AND INTERVAL '30' MINUTE FOLLOWING

-- Month-to-date (when ORDER BY is date)
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

**完全な例:**

```sql
-- 7-day rolling average
SELECT sale_date, amount,
       AVG(amount) OVER (
           ORDER BY sale_date
           RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW
       ) AS avg_7day
FROM sales_duplicates
ORDER BY sale_date;
```

### 値ベースのウィンドウ {#value-based-windows}

**構文例:**

```sql
-- Within ±10 units
RANGE BETWEEN 10 PRECEDING AND 10 FOLLOWING

-- Values up to 100 less than current
RANGE BETWEEN 100 PRECEDING AND CURRENT ROW

-- Note: Complex expressions like (current * 0.05) may not be supported
-- Use fixed values or simple expressions
```

**完全な例:**

```sql
-- Include rows within ±0.5 units
SELECT temperature, reading_time,
       COUNT(*) OVER (
           ORDER BY temperature
           RANGE BETWEEN 0.5 PRECEDING AND 0.5 FOLLOWING
       ) AS similar_readings
FROM temperature_readings
ORDER BY temperature;
```

### 重複値の扱い {#handling-duplicates}

**構文例:**

```sql
-- Include all duplicate values in same window
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

-- Value-based grouping (groups identical values)
RANGE BETWEEN 0 PRECEDING AND 0 FOLLOWING
```

**完全な例:**

```sql
-- RANGE treats duplicate dates as same window
SELECT sale_date, amount,
       SUM(amount) OVER (
           ORDER BY sale_date
           RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total_range
FROM sales_duplicates
ORDER BY sale_date;
```

## ベストプラクティス {#best-practices}

1. **値ベースのウィンドウには RANGE を使用する** - 行数ではなく論理的な値の範囲を重視する場合に適しています
2. **DATE/TIMESTAMP と組み合わせて使用する** - 時間ベースの計算に最適です
3. **重複値を意図的に扱う** - RANGE は重複する ORDER BY 値をグループ化します
4. **パフォーマンスを考慮する** - 重複が多い場合、RANGE は ROWS より遅くなることがあります
5. **間隔を明確に指定する** - 日付/時刻ウィンドウには明示的な INTERVAL 構文を使用します

## 制限事項 {#limitations}

1. **ORDER BY は数値型または時間型である必要がある** - RANGE ではソート可能な値が必要です
2. **ORDER BY カラムは 1 つのみ** - RANGE は単一カラムの並び替えで動作します
3. **値式には制限がある** - 複雑な式ではなく、単純な数値/interval 値のみ使用できます
4. **パフォーマンス上の考慮事項** - 重複値が多い場合、ROWS より遅くなることがあります
5. **フレーム境界には互換性が必要** - PRECEDING/FOLLOWING で同じ単位型を使用する必要があります

## 関連情報 {#see-also}

- [ウィンドウ関数の概要](/tidb-cloud-lake/sql/window-functions-overview.md)
- [ROWS BETWEEN](/tidb-cloud-lake/sql/rows-between.md) - 行ベースのウィンドウフレーム
- [集計関数](/tidb-cloud-lake/sql/aggregate-functions.md) - ウィンドウフレームを使用できる関数
- [日付と時刻の関数](/tidb-cloud-lake/sql/date-time-functions.md) - RANGE interval と組み合わせると便利です