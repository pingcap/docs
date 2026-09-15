---
title: RANGE BETWEEN
summary: 使用基于值的边界为窗口函数定义窗口框架。
---

# RANGE BETWEEN

使用基于值的边界为窗口函数定义窗口框架。

## 概述 {#overview}

`RANGE BETWEEN` 子句用于指定窗口框架中应包含哪些行，其依据是逻辑值范围，而不是物理行数。它特别适用于基于时间的窗口、基于值的分组以及处理重复值的场景。

## 语法 {#syntax}

```sql
FUNCTION() OVER (
    [ PARTITION BY partition_expression ]
    [ ORDER BY sort_expression ]
    RANGE BETWEEN frame_start AND frame_end
)
```

### 框架边界 {#frame-boundaries}

| 边界 | 描述 | 示例 |
|----------|-------------|---------|
| `UNBOUNDED PRECEDING` | 分区起始位置 | `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| `value PRECEDING` | 当前行之前的值范围 | `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW` |
| `CURRENT ROW` | 当前行的值 | `RANGE BETWEEN CURRENT ROW AND CURRENT ROW` |
| `value FOLLOWING` | 当前行之后的值范围 | `RANGE BETWEEN CURRENT ROW AND INTERVAL '7' DAY FOLLOWING` |
| `UNBOUNDED FOLLOWING` | 分区结束位置 | `RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` |

## RANGE 与 ROWS 的区别 {#range-vs-rows}

| 方面 | RANGE | ROWS |
|--------|-------|------|
| **定义** | 逻辑值范围 | 物理行数 |
| **边界** | 基于值的位置 | 行位置 |
| **并列值** | 相同值共享同一个框架 | 每一行彼此独立 |
| **性能** | 有重复值时可能更慢 | 通常更快 |
| **使用场景** | 基于时间的窗口、百分位数计算 | 移动平均、累计总和 |

## RANGE 的值类型 {#value-types-for-range}

### 1. 数值 {#1-numeric-values}

```sql
-- Include rows within ±10 units
RANGE BETWEEN 10 PRECEDING AND 10 FOLLOWING

-- Include rows with values up to 50 less than current
RANGE BETWEEN 50 PRECEDING AND CURRENT ROW
```

### 2. Interval 值（用于 DATE/TIMESTAMP） {#2-interval-values-for-date-timestamp}

```sql
-- 7-day window
RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW

-- 1-hour window
RANGE BETWEEN INTERVAL '1' HOUR PRECEDING AND CURRENT ROW

-- 30-minute centered window
RANGE BETWEEN INTERVAL '15' MINUTE PRECEDING AND INTERVAL '15' MINUTE FOLLOWING
```

### 3. 未指定值（默认） {#3-no-value-specified-default}

当 `PRECEDING` 或 `FOLLOWING` 未指定值时，默认值为 `CURRENT ROW`：

```sql
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  -- Default behavior
```

## 示例 {#examples}

### 示例数据 {#sample-data}

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

### 1. 24 小时滚动平均值 {#1-24-hour-rolling-average}

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

### 2. 基于值的窗口（在 ±0.5 度范围内） {#2-value-based-window-within-05-degrees}

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

### 3. 处理重复值 {#3-handling-duplicate-values}

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

**结果对比：**

```
sale_date   | amount | running_total_range | running_total_rows
------------+--------+---------------------+--------------------
2024-01-01  | 100.00 | 200.00              | 100.00
2024-01-01  | 100.00 | 200.00              | 200.00  -- ROWS: different
2024-01-02  | 150.00 | 350.00              | 350.00
2024-01-03  | 200.00 | 750.00              | 550.00
2024-01-03  | 200.00 | 750.00              | 750.00  -- ROWS: different
```

### 4. 基于时间的居中窗口 {#4-time-based-centered-window}

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

## 常见模式 {#common-patterns}

### 基于时间的窗口 {#time-based-windows}

**语法示例：**

```sql
-- 7-day rolling window
RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW

-- 1-hour centered window
RANGE BETWEEN INTERVAL '30' MINUTE PRECEDING AND INTERVAL '30' MINUTE FOLLOWING

-- Month-to-date (when ORDER BY is date)
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

**完整示例：**

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

### 基于值的窗口 {#value-based-windows}

**语法示例：**

```sql
-- Within ±10 units
RANGE BETWEEN 10 PRECEDING AND 10 FOLLOWING

-- Values up to 100 less than current
RANGE BETWEEN 100 PRECEDING AND CURRENT ROW

-- Note: Complex expressions like (current * 0.05) may not be supported
-- Use fixed values or simple expressions
```

**完整示例：**

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

### 处理重复值 {#handling-duplicates}

**语法示例：**

```sql
-- Include all duplicate values in same window
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

-- Value-based grouping (groups identical values)
RANGE BETWEEN 0 PRECEDING AND 0 FOLLOWING
```

**完整示例：**

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

## 最佳实践 {#best-practices}

1. **对基于值的窗口使用 RANGE** - 当你关注的是逻辑值范围而不是行数时
2. **与 DATE/TIMESTAMP 一起使用** - 非常适合基于时间的计算
3. **有意识地处理重复值** - RANGE 会将 `ORDER BY` 的重复值分组
4. **考虑性能** - 当存在大量重复值时，RANGE 可能比 ROWS 更慢
5. **清晰指定间隔** - 对日期/时间窗口使用显式的 INTERVAL 语法

## 限制 {#limitations}

1. **ORDER BY 必须是数值或时间类型** - RANGE 需要可排序的值
2. **仅支持一个 ORDER BY 列** - RANGE 适用于单列排序
3. **值表达式受限** - 支持简单的数值/间隔值，不支持复杂表达式
4. **性能注意事项** - 当存在大量重复值时，可能比 ROWS 更慢
5. **框架边界必须兼容** - PRECEDING/FOLLOWING 必须使用相同的单位类型

## 另请参阅 {#see-also}

- [窗口函数概览](/tidb-cloud-lake/sql/window-functions-overview.md)
- [ROWS BETWEEN](/tidb-cloud-lake/sql/rows-between.md) - 基于行的窗口框架
- [聚合函数](/tidb-cloud-lake/sql/aggregate-functions.md) - 可使用窗口框架的函数
- [日期与时间函数](/tidb-cloud-lake/sql/date-time-functions.md) - 与 RANGE 间隔配合使用很有帮助