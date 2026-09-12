---
title: NTILE
summary: 将行划分到指定数量的存储桶中，并为每一行分配一个存储桶编号。行会尽可能均匀地分布到各个存储桶中。
---

# NTILE

> **注意：**
>
> 于 v1.1.50 中引入。

将行划分到指定数量的存储桶中，并为每一行分配一个存储桶编号。行会尽可能均匀地分布到各个存储桶中。

## 语法 {#syntax}

```sql
NTILE(bucket_count)
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**参数：**

- `bucket_count`：必需。要创建的存储桶数量（必须为正整数）
- `PARTITION BY`：可选。将行划分为分区
- `ORDER BY`：必需。确定分布顺序
- `ASC | DESC`：可选。排序方向（默认值：ASC）

**说明：**

- 存储桶编号范围为 1 到 `bucket_count`
- 行会尽可能均匀地分布
- 如果行数不能均匀划分，靠前的存储桶会多分配一行
- 适用于创建百分位和等大小分组

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

**将所有分数划分为 3 个存储桶（三等分）：**

```sql
SELECT student, subject, score,
       NTILE(3) OVER (ORDER BY score DESC) AS score_bucket
FROM scores
ORDER BY score DESC, student, subject;
```

结果：

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

**在每个学生内部将分数划分为四分位：**

```sql
SELECT student, subject, score,
       NTILE(2) OVER (PARTITION BY student ORDER BY score DESC) AS performance_half
FROM scores
ORDER BY student, score DESC, subject;
```

结果：

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
```