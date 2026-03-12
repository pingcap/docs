---
title: CUME_DIST
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced: v1.2.7"/>

Calculates the cumulative distribution of each row's value. Returns the fraction of rows with values less than or equal to the current row's value.

See also: [PERCENT_RANK](percent_rank.md)

## Syntax

```sql
CUME_DIST()
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**Arguments:**
- `PARTITION BY`: Optional. Divides rows into partitions
- `ORDER BY`: Required. Determines the distribution order
- `ASC | DESC`: Optional. Sort direction (default: ASC)

**Notes:**
- Returns values between 0 and 1 (exclusive of 0, inclusive of 1)
- Formula: (number of rows ≤ current value) / (total rows)
- Always returns 1.0 for the highest value(s)
- Useful for calculating percentiles and cumulative percentages

## Examples

```sql
-- Create sample data
CREATE TABLE scores (
    student VARCHAR(20),
    score INT
);

INSERT INTO scores VALUES
    ('Alice', 95),
    ('Bob', 87),
    ('Charlie', 87),
    ('David', 82),
    ('Eve', 78);
```

**Calculate cumulative distribution (showing what percentage of students scored at or below each score):**

```sql
SELECT student, score,
       CUME_DIST() OVER (ORDER BY score) AS cume_dist,
       ROUND(CUME_DIST() OVER (ORDER BY score) * 100) AS cumulative_percent
FROM scores
ORDER BY score;
```

Result:
```
student | score | cume_dist | cumulative_percent
--------+-------+-----------+-------------------
Eve     |    78 |       0.2 |                20
David   |    82 |       0.4 |                40
Bob     |    87 |       0.8 |                80
Charlie |    87 |       0.8 |                80
Alice   |    95 |       1.0 |               100