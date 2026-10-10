---
title: ROWS BETWEEN
summary: ウィンドウ関数に対して、行ベースの境界を使用してウィンドウフレームを定義します。
---

# ROWS BETWEEN

ウィンドウ関数に対して、行ベースの境界を使用してウィンドウフレームを定義します。

## 概要 {#overview}

`ROWS BETWEEN` 句は、ウィンドウ関数の計算でウィンドウフレームに含める行を指定します。これにより、スライディングウィンドウ、累積計算、そのほかの行ベースの集計を定義できます。

## 構文 {#syntax}

```sql
FUNCTION() OVER (
    [ PARTITION BY partition_expression ]
    [ ORDER BY sort_expression ]
    ROWS BETWEEN frame_start AND frame_end
)
```

### フレーム境界 {#frame-boundaries}

| 境界 | 説明 | 例 |
|----------|-------------|---------|
| `UNBOUNDED PRECEDING` | パーティションの先頭 | `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| `n PRECEDING` | 現在の行より前の n 行 | `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` |
| `CURRENT ROW` | 現在の行 | `ROWS BETWEEN CURRENT ROW AND CURRENT ROW` |
| `n FOLLOWING` | 現在の行より後の n 行 | `ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING` |
| `UNBOUNDED FOLLOWING` | パーティションの末尾 | `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` |

## ROWS と RANGE の比較 {#rows-vs-range}

| 観点 | ROWS | RANGE |
|--------|------|-------|
| **定義** | 物理的な行数 | 論理的な値の範囲 |
| **境界** | 行位置 | 値ベースの位置 |
| **同値の扱い** | 各行は独立 | 同じ値は同じフレームを共有 |
| **パフォーマンス** | 一般的に高速 | 重複があると遅くなる場合がある |
| **ユースケース** | 移動平均、累積合計 | 値ベースのウィンドウ、パーセンタイル計算 |

## 例 {#examples}

### サンプルデータ {#sample-data}

```sql
CREATE OR REPLACE TABLE sales (
    sale_date DATE,
    product VARCHAR(20),
    amount DECIMAL(10,2)
);

INSERT INTO sales VALUES
    ('2024-01-01', 'A', 100.00),
    ('2024-01-02', 'A', 150.00),
    ('2024-01-03', 'A', 200.00),
    ('2024-01-04', 'A', 250.00),
    ('2024-01-05', 'A', 300.00),
    ('2024-01-01', 'B', 50.00),
    ('2024-01-02', 'B', 75.00),
    ('2024-01-03', 'B', 100.00),
    ('2024-01-04', 'B', 125.00),
    ('2024-01-05', 'B', 150.00);
```

### 1. 累積合計（累積和） {#1-running-total-cumulative-sum}

```sql
SELECT sale_date, product, amount,
       SUM(amount) OVER (
           PARTITION BY product
           ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM sales
ORDER BY product, sale_date;
```

結果:

```
sale_date   | product | amount | running_total
------------+---------+--------+--------------
2024-01-01  | A       | 100.00 | 100.00
2024-01-02  | A       | 150.00 | 250.00
2024-01-03  | A       | 200.00 | 450.00
2024-01-04  | A       | 250.00 | 700.00
2024-01-05  | A       | 300.00 | 1000.00
2024-01-01  | B       | 50.00  | 50.00
2024-01-02  | B       | 75.00  | 125.00
2024-01-03  | B       | 100.00 | 225.00
2024-01-04  | B       | 125.00 | 350.00
2024-01-05  | B       | 150.00 | 500.00
```

### 2. 移動平均（3日間ウィンドウ） {#2-moving-average-3-day-window}

```sql
SELECT sale_date, product, amount,
       AVG(amount) OVER (
           PARTITION BY product
           ORDER BY sale_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS moving_avg_3day
FROM sales
ORDER BY product, sale_date;
```

結果:

```
sale_date   | product | amount | moving_avg_3day
------------+---------+--------+----------------
2024-01-01  | A       | 100.00 | 100.00
2024-01-02  | A       | 150.00 | 125.00  -- (100+150)/2
2024-01-03  | A       | 200.00 | 150.00  -- (100+150+200)/3
2024-01-04  | A       | 250.00 | 200.00  -- (150+200+250)/3
2024-01-05  | A       | 300.00 | 250.00  -- (200+250+300)/3
```

### 3. 中央寄せウィンドウ（現在 + 前の 1 行 + 後の 1 行） {#3-centered-window-current-1-before-1-after}

```sql
SELECT sale_date, product, amount,
       SUM(amount) OVER (
           PARTITION BY product
           ORDER BY sale_date
           ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
       ) AS centered_sum
FROM sales
ORDER BY product, sale_date;
```

結果:

```
sale_date   | product | amount | centered_sum
------------+---------+--------+-------------
2024-01-01  | A       | 100.00 | 250.00  -- (100+150)
2024-01-02  | A       | 150.00 | 450.00  -- (100+150+200)
2024-01-03  | A       | 200.00 | 600.00  -- (150+200+250)
2024-01-04  | A       | 250.00 | 750.00  -- (200+250+300)
2024-01-05  | A       | 300.00 | 550.00  -- (250+300)
```

### 4. 先読みウィンドウ {#4-future-looking-window}

```sql
SELECT sale_date, product, amount,
       MIN(amount) OVER (
           PARTITION BY product
           ORDER BY sale_date
           ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING
       ) AS min_next_3days
FROM sales
ORDER BY product, sale_date;
```

結果:

```
sale_date   | product | amount | min_next_3days
------------+---------+--------+---------------
2024-01-01  | A       | 100.00 | 100.00  -- min(100,150,200)
2024-01-02  | A       | 150.00 | 150.00  -- min(150,200,250)
2024-01-03  | A       | 200.00 | 200.00  -- min(200,250,300)
2024-01-04  | A       | 250.00 | 250.00  -- min(250,300)
2024-01-05  | A       | 300.00 | 300.00  -- min(300)
```

### 5. 完全パーティションウィンドウ {#5-full-partition-window}

```sql
SELECT sale_date, product, amount,
       MAX(amount) OVER (
           PARTITION BY product
           ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS max_in_partition,
       MIN(amount) OVER (
           PARTITION BY product
           ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS min_in_partition
FROM sales
ORDER BY product, sale_date;
```

結果:

```
sale_date   | product | amount | max_in_partition | min_in_partition
------------+---------+--------+------------------+-----------------
2024-01-01  | A       | 100.00 | 300.00           | 100.00
2024-01-02  | A       | 150.00 | 300.00           | 100.00
2024-01-03  | A       | 200.00 | 300.00           | 100.00
2024-01-04  | A       | 250.00 | 300.00           | 100.00
2024-01-05  | A       | 300.00 | 300.00           | 100.00
```

## 一般的なパターン {#common-patterns}

### 累積計算 {#running-calculations}

**構文例（完全な文ではありません）:**

```sql
-- Running total
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- Running average
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- Running count
COUNT(*) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

**完全な例:**

```sql
-- Running total with actual table
SELECT sale_date, product, amount,
       SUM(amount) OVER (
           ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM sales
ORDER BY sale_date;
```

### 移動ウィンドウ {#moving-windows}

**構文例:**

```sql
-- 3-period moving average
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- 5-period moving sum
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)

-- Centered 3-period window
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
```

**完全な例:**

```sql
-- 3-day moving average
SELECT sale_date, amount,
       AVG(amount) OVER (
           ORDER BY sale_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS moving_avg_3day
FROM sales
ORDER BY sale_date;
```

### 境界付きウィンドウ {#bounded-windows}

**構文例:**

```sql
-- First 3 rows of partition
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND 2 FOLLOWING)

-- Last 3 rows of partition
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN 2 PRECEDING AND UNBOUNDED FOLLOWING)

-- Fixed window of 5 rows
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING)
```

**完全な例:**

```sql
-- Fixed 5-row window average
SELECT sale_date, amount,
       AVG(amount) OVER (
           ORDER BY sale_date
           ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
       ) AS avg_5row_window
FROM sales
ORDER BY sale_date;
```

## ベストプラクティス {#best-practices}

1. 正確な行ベースのウィンドウが必要な場合は、**物理的な行数のカウントには ROWS を使用**します
2. ROWS BETWEEN を使用する場合は、**常に ORDER BY を含める**ようにします（UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING を除く）
3. 大きなウィンドウでは**パフォーマンスを考慮**してください。小さいウィンドウのほうが効率的です
4. **エッジケースを処理**してください。パーティション境界ではウィンドウが小さくなる場合があります
5. グループごとの計算には **PARTITION BY と組み合わせて**使用します
6. **境界の動作を理解**してください。パーティションの端ではウィンドウが縮小します

### 境界動作の例 {#boundary-behavior-examples}

**パーティション端での中央寄せウィンドウ:**

```sql
-- For row 1: ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
-- Actual window: CURRENT ROW AND 1 FOLLOWING (no preceding row exists)

-- For last row: ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
-- Actual window: 1 PRECEDING AND CURRENT ROW (no following row exists)
```

**先頭での移動平均:**

```sql
-- For row 1: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-- Actual window: CURRENT ROW only (no preceding rows)

-- For row 2: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-- Actual window: 1 PRECEDING AND CURRENT ROW (only 1 preceding row exists)
```

これは通常の動作です。ウィンドウフレームは、パーティション境界で利用可能な行に応じて調整されます。

## 制限事項 {#limitations}

1. **n は非負の整数である必要があります**。負の値や式は使用できません
2. ほとんどのウィンドウフレームでは **ORDER BY が必要**です（完全パーティションを除く）
3. **フレーム境界は順序付けされている必要があります** - start_bound &lt;= end_bound
4. **PRECEDING と FOLLOWING を任意に混在させることはできません**。有効なウィンドウを構成する必要があります

## 関連情報 {#see-also}

- [ウィンドウ関数の概要](/tidb-cloud-lake/sql/window-functions-overview.md)
- [RANGE BETWEEN](/tidb-cloud-lake/sql/range-between.md) - 値ベースのウィンドウフレーム
- [集計関数](/tidb-cloud-lake/sql/aggregate-functions.md) - ウィンドウフレームを使用できる関数
- [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md) - フレームを使用したウィンドウ関数の例