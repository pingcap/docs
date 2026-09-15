---
title: CUME_DIST
summary: 计算每一行值的累积分布。返回值小于或等于当前行值的行所占的比例。
---

# CUME_DIST

> **注意：**
>
> 于 v1.2.7 引入。

计算每一行值的累积分布。返回值小于或等于当前行值的行所占的比例。

另请参阅：[PERCENT_RANK](/tidb-cloud-lake/sql/percent-rank.md)

## 语法 {#syntax}

```sql
CUME_DIST()
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**参数：**

- `PARTITION BY`：可选。将行划分为分区
- `ORDER BY`：必需。确定分布的排序顺序
- `ASC | DESC`：可选。排序方向（默认值：ASC）

**说明：**

- 返回介于 0 和 1 之间的值（不包括 0，包括 1）
- 公式：（小于或等于当前值的行数）/（总行数）
- 对于最大值，始终返回 1.0
- 适用于计算百分位数和累计百分比

## 示例 {#examples}

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

**计算累积分布（显示每个分数及以下分数的学生所占百分比）：**

```sql
SELECT student, score,
       CUME_DIST() OVER (ORDER BY score) AS cume_dist,
       ROUND(CUME_DIST() OVER (ORDER BY score) * 100) AS cumulative_percent
FROM scores
ORDER BY score;
```

结果：

```
student | score | cume_dist | cumulative_percent
--------+-------+-----------+-------------------
Eve     |    78 |       0.2 |                20
David   |    82 |       0.4 |                40
Bob     |    87 |       0.8 |                80
Charlie |    87 |       0.8 |                80
Alice   |    95 |       1.0 |               100
```