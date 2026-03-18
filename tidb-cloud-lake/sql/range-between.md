---
title: RANGE BETWEEN
summary: Defines a window frame using value-based boundaries for window functions.
---
Defines a window frame using value-based boundaries for window functions.

## Overview

The `RANGE BETWEEN` clause specifies which rows to include in the window frame based on logical value ranges rather than physical row counts. It's particularly useful for time-based windows, value-based groupings, and handling duplicate values.

## Syntax

```sql
FUNCTION() OVER (
    [ PARTITION BY partition_expression ]
    [ ORDER BY sort_expression ]
    RANGE BETWEEN frame_start AND frame_end
)
```

### Frame Boundaries

| Boundary | Description | Example |
|----------|-------------|---------|
| `UNBOUNDED PRECEDING` | Start of partition | `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| `value PRECEDING` | Value range before current row | `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW` |
| `CURRENT ROW` | Current row value | `RANGE BETWEEN CURRENT ROW AND CURRENT ROW` |
| `value FOLLOWING` | Value range after current row | `RANGE BETWEEN CURRENT ROW AND INTERVAL '7' DAY FOLLOWING` |
| `UNBOUNDED FOLLOWING` | End of partition | `RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` |

## RANGE vs ROWS

| Aspect | RANGE | ROWS |
|--------|-------|------|
| **Definition** | Logical value range | Physical row count |
| **Boundaries** | Value-based positions | Row positions |
| **Ties** | Tied values share same frame | Each row independent |
| **Performance** | May be slower with duplicates | Generally faster |
| **Use Case** | Time-based windows, percentile calculations | Moving averages, running totals |

## Value Types for RANGE

### 1. Numeric Values
```sql
-- Include rows within ±10 units
RANGE BETWEEN 10 PRECEDING AND 10 FOLLOWING

-- Include rows with values up to 50 less than current
RANGE BETWEEN 50 PRECEDING AND CURRENT ROW
```

### 2. Interval Values (for DATE/TIMESTAMP)
```sql
-- 7-day window
RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW

-- 1-hour window  
RANGE BETWEEN INTERVAL '1' HOUR PRECEDING AND CURRENT ROW

-- 30-minute centered window
RANGE BETWEEN INTERVAL '15' MINUTE PRECEDING AND INTERVAL '15' MINUTE FOLLOWING
```

### 3. No Value Specified (Default)
When no value is specified with `PRECEDING` or `FOLLOWING`, it defaults to `CURRENT ROW`:
```sql
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  -- Default behavior
```

## Examples

### Sample Data

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

### 1. 24-Hour Rolling Average

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

### 2. Value-Based Window (Within ±0.5 degrees)

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

### 3. Handling Duplicate Values

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

**Result comparison:**
```
sale_date   | amount | running_total_range | running_total_rows
------------+--------+---------------------+--------------------
2024-01-01  | 100.00 | 200.00              | 100.00
2024-01-01  | 100.00 | 200.00              | 200.00  -- ROWS: different
2024-01-02  | 150.00 | 350.00              | 350.00
2024-01-03  | 200.00 | 750.00              | 550.00
2024-01-03  | 200.00 | 750.00              | 750.00  -- ROWS: different
```

### 4. Time-Based Centered Window

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

## Common Patterns

### Time-Based Windows
**Syntax examples:**
```sql
-- 7-day rolling window
RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW

-- 1-hour centered window
RANGE BETWEEN INTERVAL '30' MINUTE PRECEDING AND INTERVAL '30' MINUTE FOLLOWING

-- Month-to-date (when ORDER BY is date)
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

**Complete example:**
```sql
-- 7-day rolling average
SELECT sale_date, amount,
       AVG(amount) OVER (
           ORDER BY sale_date 
           RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW
       ) AS avg_7day
FROM sales
ORDER BY sale_date;
```

### Value-Based Windows
**Syntax examples:**
```sql
-- Within ±10 units
RANGE BETWEEN 10 PRECEDING AND 10 FOLLOWING

-- Values up to 100 less than current
RANGE BETWEEN 100 PRECEDING AND CURRENT ROW

-- Note: Complex expressions like (current * 0.05) may not be supported
-- Use fixed values or simple expressions
```

**Complete example:**
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

### Handling Duplicates
**Syntax examples:**
```sql
-- Include all duplicate values in same window
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

-- Value-based grouping (groups identical values)
RANGE BETWEEN 0 PRECEDING AND 0 FOLLOWING
```

**Complete example:**
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

## Best Practices

1. **Use RANGE for value-based windows** - When you care about logical value ranges rather than row counts
2. **Use with DATE/TIMESTAMP** - Perfect for time-based calculations
3. **Handle duplicates intentionally** - RANGE groups duplicate ORDER BY values
4. **Consider performance** - RANGE can be slower than ROWS with many duplicates
5. **Specify intervals clearly** - Use explicit INTERVAL syntax for date/time windows

## Limitations

1. **ORDER BY must be numeric or temporal** - RANGE requires sortable values
2. **Only one ORDER BY column** - RANGE works with single column ordering
3. **Value expressions limited** - Simple numeric/interval values, not complex expressions
4. **Performance considerations** - May be slower than ROWS with many duplicate values
5. **Frame boundaries must be compatible** - Same unit type for PRECEDING/FOLLOWING

## See Also

- [Window Functions Overview](/tidb-cloud-lake/sql/window-functions-overview.md)
- [ROWS BETWEEN](/tidb-cloud-lake/sql/rows-between.md) - Row-based window frames
- [Aggregate Functions](/tidb-cloud-lake/sql/aggregate-functions.md) - Functions that can use window frames
- [Date and Time Functions](/tidb-cloud-lake/sql/date-time-functions.md) - Useful with RANGE intervals