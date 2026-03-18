---
title: Window Functions
summary: Window functions perform calculations across a set of related rows while returning one result per input row. Unlike aggregate functions, window functions don't collapse rows into a single output.
---
## Overview

Window functions perform calculations across a set of related rows while returning one result per input row. Unlike aggregate functions, window functions don't collapse rows into a single output.

**Key characteristics:**

- Operate on a "window" of rows related to the current row
- Return one value per input row (no grouping/collapsing)
- Can access values from other rows in the window
- Support partitioning and ordering for flexible calculations

**Note on SQL examples in this documentation:**

- ✅ **Complete SQL statements** have been validated against Databend
- ⚠️ **Syntax examples** show window frame patterns (not complete statements)
- 📋 All examples use standard SQL syntax supported by Databend
- 🔍 Examples marked as "Complete example" are fully executable

## Window Function Categories

Databend supports two main categories of window functions:

### 1. Dedicated Window Functions

These functions are specifically designed for window operations.

**Ranking Functions:**

| Function | Description | Ties Handling | Example Output |
|----------|-------------|---------------|----------------|
| [ROW_NUMBER](/tidb-cloud-lake/sql/row-number.md) | Sequential numbering | Always unique | `1, 2, 3, 4, 5` |
| [RANK](/tidb-cloud-lake/sql/rank.md) | Ranking with gaps | Same rank, gaps after | `1, 2, 2, 4, 5` |
| [DENSE_RANK](/tidb-cloud-lake/sql/dense-rank.md) | Ranking without gaps | Same rank, no gaps | `1, 2, 2, 3, 4` |

**Distribution Functions:**

| Function | Description | Range | Example Output |
|----------|-------------|-------|----------------|
| [PERCENT_RANK](/tidb-cloud-lake/sql/percent-rank.md) | Relative rank as percentage | 0.0 to 1.0 | `0.0, 0.25, 0.5, 0.75, 1.0` |
| [CUME_DIST](/tidb-cloud-lake/sql/cume-dist.md) | Cumulative distribution | 0.0 to 1.0 | `0.2, 0.4, 0.6, 0.8, 1.0` |
| [NTILE](/tidb-cloud-lake/sql/ntile.md) | Divide into N buckets | 1 to N | `1, 1, 2, 2, 3, 3` |

**Value Access Functions:**

| Function | Description | Use Case |
|----------|-------------|----------|
| [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md) | First value in window | Get highest/earliest value |
| [LAST_VALUE](/tidb-cloud-lake/sql/last-value.md) | Last value in window | Get lowest/latest value |
| [NTH_VALUE](/tidb-cloud-lake/sql/nth-value.md) | Nth value in window | Get specific positioned value |
| [LAG](/tidb-cloud-lake/sql/lag.md) | Previous row value | Compare with previous |
| [LEAD](/tidb-cloud-lake/sql/lead.md) | Next row value | Compare with next |

**Aliases:**

| Function | Alias For |
|----------|----------|
| [FIRST](/tidb-cloud-lake/sql/first.md) | FIRST_VALUE |
| [LAST](/tidb-cloud-lake/sql/last.md) | LAST_VALUE |

### 2. Aggregate Functions Used as Window Functions

These are standard aggregate functions that can be used with the OVER clause to perform window operations.

| Function | Description | Window Frame Support | Example |
|----------|-------------|---------------------|---------|  
| [SUM](/tidb-cloud-lake/sql/sum.md) | Calculates sum over window | ✓ | `SUM(sales) OVER (PARTITION BY region ORDER BY date)` |
| [AVG](/tidb-cloud-lake/sql/avg.md) | Calculates average over window | ✓ | `AVG(score) OVER (ORDER BY id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` |
| [COUNT](/tidb-cloud-lake/sql/count.md) | Counts rows over window | ✓ | `COUNT(*) OVER (PARTITION BY department)` |
| [MIN](/tidb-cloud-lake/sql/min.md) | Returns minimum value in window | ✓ | `MIN(price) OVER (PARTITION BY category)` |
| [MAX](/tidb-cloud-lake/sql/max.md) | Returns maximum value in window | ✓ | `MAX(price) OVER (PARTITION BY category)` |
| [ARRAY_AGG](/tidb-cloud-lake/sql/array-agg.md) | Collects values into array | | `ARRAY_AGG(product) OVER (PARTITION BY category)` |
| [STDDEV_POP](/tidb-cloud-lake/sql/stddev-pop.md) | Population standard deviation | ✓ | `STDDEV_POP(value) OVER (PARTITION BY group)` |
| [STDDEV_SAMP](/tidb-cloud-lake/sql/stddev-samp.md) | Sample standard deviation | ✓ | `STDDEV_SAMP(value) OVER (PARTITION BY group)` |
| [MEDIAN](/tidb-cloud-lake/sql/median.md) | Median value | ✓ | `MEDIAN(response_time) OVER (PARTITION BY server)` |

**Conditional Variants**

| Function | Description | Window Frame Support | Example |
|----------|-------------|---------------------|---------|
| [COUNT_IF](/tidb-cloud-lake/sql/count-if.md) | Conditional count | ✓ | `COUNT_IF(status = 'complete') OVER (PARTITION BY dept)` |
| [SUM_IF](/tidb-cloud-lake/sql/sum-if.md) | Conditional sum | ✓ | `SUM_IF(amount, status = 'paid') OVER (PARTITION BY customer)` |
| [AVG_IF](/tidb-cloud-lake/sql/avg-if.md) | Conditional average | ✓ | `AVG_IF(score, passed = true) OVER (PARTITION BY class)` |
| [MIN_IF](/tidb-cloud-lake/sql/min-if.md) | Conditional minimum | ✓ | `MIN_IF(temp, location = 'outside') OVER (PARTITION BY day)` |
| [MAX_IF](/tidb-cloud-lake/sql/max-if.md) | Conditional maximum | ✓ | `MAX_IF(speed, vehicle = 'car') OVER (PARTITION BY test)` |

## Basic Syntax

All window functions follow this pattern:

```sql
FUNCTION() OVER (
    [ PARTITION BY column ]
    [ ORDER BY column ]
    [ window_frame ]
)
```

- **PARTITION BY**: Divides data into groups
- **ORDER BY**: Sorts rows within each partition
- **window_frame**: Defines which rows to include (optional)

## Window Frame Specification

The window frame defines which rows are included in the calculation for each row. Databend supports two types of window frames:

### 1. ROWS BETWEEN
Defines a window frame using physical row counts.

**Syntax:**
```sql
ROWS BETWEEN frame_start AND frame_end
```

**Examples:**
- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` - Running total
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` - 3-day moving average
- `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` - Centered window

For detailed examples and usage, see [ROWS BETWEEN](/tidb-cloud-lake/sql/rows-between.md).

### 2. RANGE BETWEEN  
Defines a window frame using logical value ranges.

**Syntax:**
```sql
RANGE BETWEEN frame_start AND frame_end
```

**Examples:**
- `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` - Cumulative by value
- `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW` - 7-day window

For detailed examples and usage, see [RANGE BETWEEN](/tidb-cloud-lake/sql/range-between.md).

## Common Use Cases

- **Ranking**: Create leaderboards and top-N lists
- **Analytics**: Calculate running totals, moving averages, percentiles
- **Comparison**: Compare current vs previous/next values
- **Grouping**: Divide data into buckets without losing detail

For detailed syntax and examples, see individual function documentation above.
