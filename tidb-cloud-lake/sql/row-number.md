---
title: ROW_NUMBER
---

Assigns a sequential number to each row within a partition, starting from 1.

## Syntax

```sql
ROW_NUMBER() 
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**Arguments:**
- `PARTITION BY`: Optional. Divides rows into partitions
- `ORDER BY`: Required. Determines the row numbering order
- `ASC | DESC`: Optional. Sort direction (default: ASC)

**Notes:**
- Returns sequential integers starting from 1
- Each partition restarts numbering from 1
- Commonly used for ranking and pagination

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
    ('Bob', 'Math', 78),
    ('Bob', 'English', 85),
    ('Bob', 'Science', 80),
    ('Charlie', 'Math', 88),
    ('Charlie', 'English', 90),
    ('Charlie', 'Science', 85);
```

**Number all rows sequentially (even with tied scores):**

```sql
SELECT student, subject, score,
       ROW_NUMBER() OVER (ORDER BY score DESC, student, subject) AS row_num
FROM scores
ORDER BY score DESC, student, subject;
```

Result:
```
student | subject | score | row_num
--------+---------+-------+--------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Charlie | English |    90 | 3
Charlie | Math    |    88 | 4
Alice   | English |    87 | 5
Bob     | English |    85 | 6
Charlie | Science |    85 | 7
Bob     | Science |    80 | 8
Bob     | Math    |    78 | 9
```

**Number rows within each student (for pagination/top-N):**

```sql
SELECT student, subject, score,
       ROW_NUMBER() OVER (PARTITION BY student ORDER BY score DESC) AS subject_rank
FROM scores
ORDER BY student, score DESC;
```

Result:
```
student | subject | score | subject_rank
--------+---------+-------+-------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Alice   | English |    87 | 3
Bob     | English |    85 | 1
Bob     | Science |    80 | 2
Bob     | Math    |    78 | 3
Charlie | English |    90 | 1
Charlie | Math    |    88 | 2
Charlie | Science |    85 | 3