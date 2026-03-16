---
title: DENSE_RANK
---

Assigns a rank to each row within a partition. Rows with equal values receive the same rank, with no gaps in subsequent rankings.

## Syntax

```sql
DENSE_RANK() 
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
- Ranks start from 1
- Equal values get the same rank
- No gaps in ranking sequence after ties
- Example: 1, 2, 2, 3, 4 (not 1, 2, 2, 4, 5 like RANK)

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

**Dense rank all scores (showing no gaps after ties):**

```sql
SELECT student, subject, score,
       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM scores
ORDER BY score DESC, student, subject;
```

Result:
```
student | subject | score | dense_rank
--------+---------+-------+-----------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Charlie | Math    |    88 | 3
Alice   | English |    87 | 4
Bob     | English |    85 | 5
Bob     | Math    |    85 | 5
Charlie | English |    85 | 5
Charlie | Science |    85 | 5
Bob     | Science |    80 | 6
```

**Dense rank scores within each student:**

```sql
SELECT student, subject, score,
       DENSE_RANK() OVER (PARTITION BY student ORDER BY score DESC) AS subject_dense_rank
FROM scores
ORDER BY student, score DESC, subject;
```

Result:
```
student | subject | score | subject_dense_rank
--------+---------+-------+-------------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Alice   | English |    87 | 3
Bob     | English |    85 | 1
Bob     | Math    |    85 | 1
Bob     | Science |    80 | 2
Charlie | Math    |    88 | 1
Charlie | English |    85 | 2
Charlie | Science |    85 | 2
```

