---
title: MEDIAN_TDIGEST
summary: 使用 t-digest 算法计算数值数据序列的中位数。
---

# MEDIAN_TDIGEST

使用 [t-digest](https://github.com/tdunning/t-digest/blob/master/docs/t-digest-paper/histo.pdf) 算法计算数值数据序列的中位数。

> **注意：**
>
> NULL 值不参与计算。

## 语法 {#syntax}

```sql
MEDIAN_TDIGEST(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|--------------------------|
| `<expr>`  | 任意数值表达式 |

## 返回类型 {#return-type}

返回与输入值相同数据类型的值。

## 示例 {#examples}

```sql
-- Create a table and insert sample data
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

-- Calculate median exam score
SELECT MEDIAN_TDIGEST(score) AS median_score
FROM exam_scores;

|  median_score  |
|----------------|
|      85.0      |
```