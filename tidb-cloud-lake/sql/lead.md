---
title: LEAD
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.45"/>

Returns the value from a subsequent row in the result set.

See also: [LAG](lag.md)

## Syntax

```sql
LEAD(
    expression 
    [, offset ]
    [, default ]
) 
OVER (
    [ PARTITION BY partition_expression ] 
    ORDER BY sort_expression
)
```

**Arguments:**
- `expression`: The column or expression to evaluate
- `offset`: Number of rows after the current row (default: 1)
- `default`: Value to return when no next row exists (default: NULL)

**Notes:**
- Negative offset values work like LAG function
- Returns NULL if the offset goes beyond partition boundaries

## Examples

```sql
-- Create sample data
CREATE TABLE scores (
    student VARCHAR(20),
    test_date DATE,
    score INT
);

INSERT INTO scores VALUES
    ('Alice', '2024-01-01', 85),
    ('Alice', '2024-02-01', 90),
    ('Alice', '2024-03-01', 88),
    ('Bob', '2024-01-01', 78),
    ('Bob', '2024-02-01', 82),
    ('Bob', '2024-03-01', 85);
```

**Get next test score for each student:**

```sql
SELECT student, test_date, score,
       LEAD(score) OVER (PARTITION BY student ORDER BY test_date) AS next_score
FROM scores
ORDER BY student, test_date;
```

Result:
```
student | test_date  | score | next_score
--------+------------+-------+-----------
Alice   | 2024-01-01 |    85 | 90
Alice   | 2024-02-01 |    90 | 88
Alice   | 2024-03-01 |    88 | NULL
Bob     | 2024-01-01 |    78 | 82
Bob     | 2024-02-01 |    82 | 85
Bob     | 2024-03-01 |    85 | NULL
```

**Get score from 2 tests later:**

```sql
SELECT student, test_date, score,
       LEAD(score, 2, 0) OVER (PARTITION BY student ORDER BY test_date) AS score_2_tests_later
FROM scores
ORDER BY student, test_date;
```

Result:
```
student | test_date  | score | score_2_tests_later
--------+------------+-------+--------------------
Alice   | 2024-01-01 |    85 | 88
Alice   | 2024-02-01 |    90 | 0
Alice   | 2024-03-01 |    88 | 0
Bob     | 2024-01-01 |    78 | 85
Bob     | 2024-02-01 |    82 | 0
Bob     | 2024-03-01 |    85 | 0
```