---
title: ROWS BETWEEN
summary: Defines a window frame using row-based boundaries for window functions.
---

# ROWS BETWEEN

Defines a window frame using row-based boundaries for window functions.

## Overview

The `ROWS BETWEEN` clause specifies which rows to include in the window frame for window function calculations. It allows you to define sliding windows, cumulative calculations, and other row-based aggregations.

## Syntax

```sql
FUNCTION() OVER (
    [ PARTITION BY partition_expression ]
    [ ORDER BY sort_expression ]
    ROWS BETWEEN frame_start AND frame_end
)
```

### Frame Boundaries

| Boundary | Description | Example |
|----------|-------------|---------|
| `UNBOUNDED PRECEDING` | Start of partition | `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| `n PRECEDING` | n rows before current row | `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` |
| `CURRENT ROW` | Current row | `ROWS BETWEEN CURRENT ROW AND CURRENT ROW` |
| `n FOLLOWING` | n rows after current row | `ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING` |
| `UNBOUNDED FOLLOWING` | End of partition | `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` |

## ROWS vs RANGE

| Aspect | ROWS | RANGE |
|--------|------|-------|
| **Definition** | Physical row count | Logical value range |
| **Boundaries** | Row positions | Value-based positions |
| **Ties** | Each row independent | Tied values share same frame |
| **Performance** | Generally faster | May be slower with duplicates |
| **Use Case** | Moving averages, running totals | Value-based windows, percentile calculations |

## Examples

### Sample Data

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

### 1. Running Total (Cumulative Sum)

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

Result:

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

### 2. Moving Average (3-Day Window)

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

Result:

```
sale_date   | product | amount | moving_avg_3day
------------+---------+--------+----------------
2024-01-01  | A       | 100.00 | 100.00
2024-01-02  | A       | 150.00 | 125.00  -- (100+150)/2
2024-01-03  | A       | 200.00 | 150.00  -- (100+150+200)/3
2024-01-04  | A       | 250.00 | 200.00  -- (150+200+250)/3
2024-01-05  | A       | 300.00 | 250.00  -- (200+250+300)/3
```

### 3. Centered Window (Current + 1 Before + 1 After)

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

Result:

```
sale_date   | product | amount | centered_sum
------------+---------+--------+-------------
2024-01-01  | A       | 100.00 | 250.00  -- (100+150)
2024-01-02  | A       | 150.00 | 450.00  -- (100+150+200)
2024-01-03  | A       | 200.00 | 600.00  -- (150+200+250)
2024-01-04  | A       | 250.00 | 750.00  -- (200+250+300)
2024-01-05  | A       | 300.00 | 550.00  -- (250+300)
```

### 4. Future Looking Window

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

Result:

```
sale_date   | product | amount | min_next_3days
------------+---------+--------+---------------
2024-01-01  | A       | 100.00 | 100.00  -- min(100,150,200)
2024-01-02  | A       | 150.00 | 150.00  -- min(150,200,250)
2024-01-03  | A       | 200.00 | 200.00  -- min(200,250,300)
2024-01-04  | A       | 250.00 | 250.00  -- min(250,300)
2024-01-05  | A       | 300.00 | 300.00  -- min(300)
```

### 5. Full Partition Window

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

Result:

```
sale_date   | product | amount | max_in_partition | min_in_partition
------------+---------+--------+------------------+-----------------
2024-01-01  | A       | 100.00 | 300.00           | 100.00
2024-01-02  | A       | 150.00 | 300.00           | 100.00
2024-01-03  | A       | 200.00 | 300.00           | 100.00
2024-01-04  | A       | 250.00 | 300.00           | 100.00
2024-01-05  | A       | 300.00 | 300.00           | 100.00
```

## Common Patterns

### Running Calculations

**Syntax examples (not complete statements):**

```sql
-- Running total
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- Running average
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- Running count
COUNT(*) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

**Complete example:**

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

### Moving Windows

**Syntax examples:**

```sql
-- 3-period moving average
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- 5-period moving sum
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)

-- Centered 3-period window
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
```

**Complete example:**

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

### Bounded Windows

**Syntax examples:**

```sql
-- First 3 rows of partition
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN UNBOUNDED PRECEDING AND 2 FOLLOWING)

-- Last 3 rows of partition
SUM(column) OVER (ORDER BY sort_col ROWS BETWEEN 2 PRECEDING AND UNBOUNDED FOLLOWING)

-- Fixed window of 5 rows
AVG(column) OVER (ORDER BY sort_col ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING)
```

**Complete example:**

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

## Best Practices

1. **Use ROWS for physical row counts** when you need exact row-based windows
2. **Always include ORDER BY** when using ROWS BETWEEN (except for UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
3. **Consider performance** with large windows - smaller windows are more efficient
4. **Handle edge cases** - windows may be smaller at partition boundaries
5. **Combine with PARTITION BY** for per-group calculations
6. **Understand boundary behavior** - windows shrink at partition edges

### Boundary Behavior Examples

**Centered window at partition edges:**

```sql
-- For row 1: ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
-- Actual window: CURRENT ROW AND 1 FOLLOWING (no preceding row exists)

-- For last row: ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
-- Actual window: 1 PRECEDING AND CURRENT ROW (no following row exists)
```

**Moving average at start:**

```sql
-- For row 1: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-- Actual window: CURRENT ROW only (no preceding rows)

-- For row 2: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
-- Actual window: 1 PRECEDING AND CURRENT ROW (only 1 preceding row exists)
```

This is normal behavior - the window frame adapts to available rows at partition boundaries.

## Limitations

1. **n must be non-negative integer** - cannot use negative values or expressions
2. **ORDER BY required** for most window frames (except full partition)
3. **Frame boundaries must be ordered** - start_bound &lt;= end_bound
4. **Cannot mix PRECEDING and FOLLOWING arbitrarily** - must form valid window

## See Also

- [Window Functions Overview](/tidb-cloud-lake/sql/window-functions-overview.md)
- [RANGE BETWEEN](/tidb-cloud-lake/sql/range-between.md) - Value-based window frames
- [Aggregate Functions](/tidb-cloud-lake/sql/aggregate-functions.md) - Functions that can use window frames
- [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md) - Window function examples with frames
