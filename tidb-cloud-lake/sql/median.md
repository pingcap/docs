---
title: MEDIAN
summary: `MEDIAN()` 函数。
---

# MEDIAN

`MEDIAN()` 函数用于计算一组数值数据序列的中位数。

> **注意：**
>
> 不统计 `NULL` 值。

## 语法 {#syntax}

```sql
MEDIAN(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|--------------------------|
| `<expr>`  | 任意数值表达式 |

## 返回类型 {#return-type}

该值的类型。

## 示例 {#example}

**Create a Table and Insert Sample Data**

```sql
CREATE TABLE exam_scores (
  id INT,
  student_id INT,
  score INT
);

INSERT INTO exam_scores (id, student_id, score)
VALUES (1, 1, 80),
       (2, 2, 90),
       (3, 3, 75),
       (4, 4, 95),
       (5, 5, 85);
```

**Query Demo: Calculate Median Exam Score**

```sql
SELECT MEDIAN(score) AS median_score
FROM exam_scores;
```

**结果**

```sql
|  median_score  |
|----------------|
|      85.0      |
```