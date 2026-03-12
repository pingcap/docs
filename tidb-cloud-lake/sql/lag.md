---
title: LAG
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.45"/>

Returns the value from a previous row in the result set.

See also: [LEAD](lead.md)

## Syntax

```sql
LAG(
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
- `offset`: Number of rows before the current row (default: 1)
- `default`: Value to return when no previous row exists (default: NULL)

**Notes:**
- Negative offset values work like LEAD function
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

**Get previous test score for each student:**

```sql
SELECT student, test_date, score,
       LAG(score) OVER (PARTITION BY student ORDER BY test_date) AS previous_score
FROM scores
ORDER BY student, test_date;
```

Result:
```
student | test_date  | score | previous_score
--------+------------+-------+---------------
Alice   | 2024-01-01 |    85 | NULL
Alice   | 2024-02-01 |    90 | 85
Alice   | 2024-03-01 |    88 | 90
Bob     | 2024-01-01 |    78 | NULL
Bob     | 2024-02-01 |    82 | 78
Bob     | 2024-03-01 |    85 | 82
```

**Get score from 2 tests ago:**

```sql
SELECT student, test_date, score,
       LAG(score, 2, 0) OVER (PARTITION BY student ORDER BY test_date) AS score_2_tests_ago
FROM scores
ORDER BY student, test_date;
```

Result:
```
student | test_date  | score | score_2_tests_ago
--------+------------+-------+------------------
Alice   | 2024-01-01 |    85 | 0
Alice   | 2024-02-01 |    90 | 0
Alice   | 2024-03-01 |    88 | 85
Bob     | 2024-01-01 |    78 | 0
Bob     | 2024-02-01 |    82 | 0
Bob     | 2024-03-01 |    85 | 78
```