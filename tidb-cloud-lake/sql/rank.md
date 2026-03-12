---
title: RANK
---

Assigns a rank to each row within a partition. Rows with equal values receive the same rank, with gaps in subsequent rankings.

## Syntax

```sql
RANK() 
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
- Creates gaps in ranking sequence after ties
- Example: 1, 2, 2, 4, 5 (not 1, 2, 2, 3, 4)

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

**Rank all scores (showing tie handling with gaps):**

```sql
SELECT student, subject, score,
       RANK() OVER (ORDER BY score DESC) AS score_rank
FROM scores
ORDER BY score DESC, student, subject;
```

Result:
```
student | subject | score | score_rank
--------+---------+-------+-----------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Charlie | Math    |    88 | 3
Alice   | English |    87 | 4
Bob     | English |    85 | 5
Bob     | Math    |    85 | 5
Charlie | English |    85 | 5
Charlie | Science |    85 | 5
Bob     | Science |    80 | 9
```

**Rank scores within each student (showing ties within partitions):**

```sql
SELECT student, subject, score,
       RANK() OVER (PARTITION BY student ORDER BY score DESC) AS subject_rank
FROM scores
ORDER BY student, score DESC, subject;
```

Result:
```
student | subject | score | subject_rank
--------+---------+-------+-------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Alice   | English |    87 | 3
Bob     | English |    85 | 1
Bob     | Math    |    85 | 1
Bob     | Science |    80 | 3
Charlie | Math    |    88 | 1
Charlie | English |    85 | 2
Charlie | Science |    85 | 2
```
