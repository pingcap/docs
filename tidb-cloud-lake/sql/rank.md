---
title: RANK
summary: 为分区内的每一行分配一个排名。值相等的行会获得相同的排名，后续排名会出现间隔。
---

# RANK

为分区内的每一行分配一个排名。值相等的行会获得相同的排名，后续排名会出现间隔。

## 语法 {#syntax}

```sql
RANK()
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**参数：**

- `PARTITION BY`：可选。将行划分为多个分区
- `ORDER BY`：必需。确定排名顺序
- `ASC | DESC`：可选。排序方向（默认值：ASC）

**说明：**

- 排名从 1 开始
- 相等的值会获得相同的排名
- 并列之后的排名序列会出现间隔
- 示例：1, 2, 2, 4, 5（而不是 1, 2, 2, 3, 4）

## 示例 {#examples}

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

**对所有分数进行排名（展示并列时带间隔的处理方式）：**

```sql
SELECT student, subject, score,
       RANK() OVER (ORDER BY score DESC) AS score_rank
FROM scores
ORDER BY score DESC, student, subject;
```

结果：

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

**在每个学生内部对分数进行排名（展示分区内的并列情况）：**

```sql
SELECT student, subject, score,
       RANK() OVER (PARTITION BY student ORDER BY score DESC) AS subject_rank
FROM scores
ORDER BY student, score DESC, subject;
```

结果：

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