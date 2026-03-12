---
title: PERCENT_RANK
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.780"/>

Calculates the relative rank of each row as a percentage. Returns values between 0 and 1, where 0 represents the lowest rank and 1 represents the highest rank.

See also: [CUME_DIST](cume-dist.md)

## Syntax

```sql
PERCENT_RANK()
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**Arguments:**
- `PARTITION BY`: Optional. Divides rows into partitions
- `ORDER BY`: Required. Determines the ranking order
- `ASC | DESC`: Optional. Sort direction (default: ASC)

**Notes:**
- Returns values between 0 and 1 (inclusive)
- First row always has PERCENT_RANK of 0
- Last row always has PERCENT_RANK of 1
- Formula: (rank - 1) / (total_rows - 1)
- Multiply by 100 to get percentile values

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

**Calculate percent rank (showing percentile position):**

```sql
SELECT student, score,
       PERCENT_RANK() OVER (ORDER BY score DESC) AS percent_rank,
       ROUND(PERCENT_RANK() OVER (ORDER BY score DESC) * 100) AS percentile
FROM scores
ORDER BY score DESC, student;
```

Result:
```
student | score | percent_rank | percentile
--------+-------+--------------+-----------
Alice   |    95 |          0.0 |          0
Bob     |    87 |         0.25 |         25
Charlie |    87 |         0.25 |         25
David   |    82 |         0.75 |         75
Eve     |    78 |          1.0 |        100
```
