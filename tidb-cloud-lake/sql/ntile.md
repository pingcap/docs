---
title: NTILE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced: v1.1.50"/>

Divides rows into a specified number of buckets and assigns a bucket number to each row. Rows are distributed as evenly as possible across buckets.

## Syntax

```sql
NTILE(bucket_count)
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**Arguments:**
- `bucket_count`: Required. Number of buckets to create (must be positive integer)
- `PARTITION BY`: Optional. Divides rows into partitions
- `ORDER BY`: Required. Determines the distribution order
- `ASC | DESC`: Optional. Sort direction (default: ASC)

**Notes:**
- Bucket numbers range from 1 to `bucket_count`
- Rows are distributed as evenly as possible
- If rows don't divide evenly, earlier buckets get one extra row
- Useful for creating percentiles and equal-sized groups

## Examples

```sql
-- Create sample data
CREATE TABLE scores (
    student VARCHAR(20),
    subject VARCHAR(20),
    score INT
);

INSERT INTO scores VALUES
    ('Alice', 'Math', 95),
    ('Alice', 'English', 87),
    ('Alice', 'Science', 92),
    ('Bob', 'Math', 85),
    ('Bob', 'English', 85),
    ('Bob', 'Science', 80),
    ('Charlie', 'Math', 88),
    ('Charlie', 'English', 85),
    ('Charlie', 'Science', 85);
```

**Divide all scores into 3 buckets (tertiles):**

```sql
SELECT student, subject, score,
       NTILE(3) OVER (ORDER BY score DESC) AS score_bucket
FROM scores
ORDER BY score DESC, student, subject;
```

Result:
```
student | subject | score | score_bucket
--------+---------+-------+-------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 1
Charlie | Math    |    88 | 1
Alice   | English |    87 | 2
Bob     | English |    85 | 2
Bob     | Math    |    85 | 2
Charlie | English |    85 | 3
Charlie | Science |    85 | 3
Bob     | Science |    80 | 3
```

**Divide scores into quartiles within each student:**

```sql
SELECT student, subject, score,
       NTILE(2) OVER (PARTITION BY student ORDER BY score DESC) AS performance_half
FROM scores
ORDER BY student, score DESC, subject;
```

Result:
```
student | subject | score | performance_half
--------+---------+-------+-----------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 1
Alice   | English |    87 | 2
Bob     | English |    85 | 1
Bob     | Math    |    85 | 1
Bob     | Science |    80 | 2
Charlie | Math    |    88 | 1
Charlie | English |    85 | 2
Charlie | Science |    85 | 2