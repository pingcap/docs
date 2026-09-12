---
title: ROWS BETWEEN
summary: 使用基于行的边界为窗口函数定义窗口框架。
---

# ROWS BETWEEN

使用基于行的边界为窗口函数定义窗口框架。

## 概述 {#overview}

`ROWS BETWEEN` 子句用于指定在窗口函数计算中应包含哪些行到窗口框架中。它允许你定义滑动窗口、累积计算以及其他基于行的聚合。

## 语法 {#syntax}

```sql
FUNCTION() OVER (
    [ PARTITION BY partition_expression ]
    [ ORDER BY sort_expression ]
    ROWS BETWEEN frame_start AND frame_end
)
```

### 框架边界 {#frame-boundaries}

| 边界 | 描述 | 示例 |
|----------|-------------|---------|
| `UNBOUNDED PRECEDING` | 分区起始位置 | `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| `n PRECEDING` | 当前行之前的 n 行 | `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` |
| `CURRENT ROW` | 当前行 | `ROWS BETWEEN CURRENT ROW AND CURRENT ROW` |
| `n FOLLOWING` | 当前行之后的 n 行 | `ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING` |
| `UNBOUNDED FOLLOWING` | 分区结束位置 | `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` |

## ROWS 与 RANGE 的对比 {#rows-vs-range}

| 方面 | ROWS | RANGE |
|--------|------|-------|
| **定义** | 物理行数 | 逻辑值范围 |
| **边界** | 行位置 | 基于值的位置 |
| **并列值** | 每一行相互独立 | 相同值共享同一个框架 |
| **性能** | 通常更快 | 存在重复值时可能更慢 |
| **使用场景** | 移动平均、运行总计 | 基于值的窗口、百分位计算 |

## 示例 {#examples}

### 示例数据 {#sample-data}

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

### 1. 运行总计（累积求和） {#1-running-total-cumulative-sum}

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

结果：

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

### 2. 移动平均（3 天窗口） {#2-moving-average-3-day-window}

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

结果：

```
sale_date   | product | amount | moving_avg_3day
------------+---------+--------+----------------
2024-01-01  | A       | 100.00 | 100.00
2024-01-02  | A       | 150.00 | 125.00  -- (100+150)/2
2024-01-03  | A       | 200.00 | 150.00  -- (100+150+200)/3
2024-01-04  | A       | 250.00 | 200.00  -- (150+200+250)/3
2024-01-05  | A       | 300.00 | 250.00  -- (200+250+300)/3
```

### 3. 居中窗口（当前行 + 前 1 行 + 后 1 行） {#3-centered-window-current-1-before-1-after}

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

结果：

```
sale_date   | product | amount | centered_sum
------------+---------+--------+-------------
2024-01-01  | A       | 100.00 | 250.00  -- (100+150)
2024-01-02  | A       | 150.00 | 450.00  -- (100+150+200)
2024-01-03  | A       | 200.00 | 600.00  -- (150+200+250)
2024-01-04  | A       | 250.00 | 750.00  -- (200+250+300)
2024-01-05  | A       | 300.00 | 550.00  -- (250+300)
```

### 4. 面向未来的窗口 {#4-future-looking-window}

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

结果：

```
sale_date   | product | amount | min_next_3days
------------+---------+--------+---------------
2024-01-01  | A       | 100.00 | 100.00  -- min(100,150,200)
2024-01-02  | A       | 150.00 | 150.00  -- min(150,200,250)
2024-01-03  | A       | 200.00 | 200.00  -- min(200,250,300)
2024-01-04  | A       | 250.00 | 250.00  -- min(250,300)
2024-01-05  | A       | 300.00 | 300.00  -- min(300)
```

### 5. 完整分区窗口 {#5-full-partition-window}

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

结果：

```
sale_date   | product | amount | max_in_partition | min_in_partition
------------+---------+--------+------------------+-----------------
2024-01-01  | A       | 100.00 | 300.00           | 100.00
2024-01-02  | A       | 150.00 | 300.00           | 100.00
2024-01-03  | A       | 200.00 | 300.00           | 100.00
2024-01-04  | A       | 250.00 | 300.00           | 100.00
2024-01-05  | A       | 300.00 | 300.00           | 100.00
```

## 常见模式 {#common-patterns}

### 累积计算 {#running-calculations}

**语法示例（不是完整语句）：**

```sql
-- Running total
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- Running average
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- Running count
COUNT(*) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

**完整示例：**

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

### 滑动窗口 {#moving-windows}

**语法示例：**

```sql
-- 3-period moving average
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- 5-period moving sum
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)

-- Centered 3-period window
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
```

**完整示例：**

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

### 有界窗口 {#bounded-windows}

**语法示例：**

```sql
-- First 3 rows of partition
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND 2 FOLLOWING)

-- Last 3 rows of partition
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN 2 PRECEDING AND UNBOUNDED FOLLOWING)

-- Fixed window of 5 rows
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING)
```

**完整示例：**

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

## 最佳实践 {#best-practices}

1. 当你需要精确基于行的窗口时，**对物理行数使用 ROWS**
2. 使用 ROWS BETWEEN 时，**始终包含 ORDER BY**（UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING 除外）
3. 对于大窗口，**考虑性能** - 较小的窗口效率更高
4. **处理边界情况** - 在分区边界处，窗口可能会更小
5. **结合 PARTITION BY 使用**，以进行按组计算
6. **理解边界行为** - 在分区边缘，窗口会收缩

### 边界行为示例 {#boundary-behavior-examples}

**分区边缘处的居中窗口：**

```sql
-- For row 1: ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
-- Actual window: CURRENT ROW AND 1 FOLLOWING (no preceding row exists)

-- For last row: ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
-- Actual window: 1 PRECEDING AND CURRENT ROW (no following row exists)
```

**开始位置的移动平均值：**

```sql
-- For row 1: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-- Actual window: CURRENT ROW only (no preceding rows)

-- For row 2: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-- Actual window: 1 PRECEDING AND CURRENT ROW (only 1 preceding row exists)
```

这是正常行为 - 窗口框架会根据分区边界处可用的行进行调整。

## 限制 {#limitations}

1. **n 必须是非负整数型** - 不能使用负值或表达式
2. 大多数窗口框架都**需要 ORDER BY**（完整分区除外）
3. **框架边界必须有序** - start_bound &lt;= end_bound
4. **不能任意混用 PRECEDING 和 FOLLOWING** - 必须构成有效窗口

## 另请参阅 {#see-also}

- [窗口函数概览](/tidb-cloud-lake/sql/window-functions-overview.md)
- [RANGE BETWEEN](/tidb-cloud-lake/sql/range-between.md) - 基于值的窗口框架
- [聚合函数](/tidb-cloud-lake/sql/aggregate-functions.md) - 可使用窗口框架的聚合函数
- [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md) - 带框架的窗口函数示例