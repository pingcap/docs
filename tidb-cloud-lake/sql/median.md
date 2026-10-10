---
title: MEDIAN
summary: MEDIAN() 関数。
---

# MEDIAN

`MEDIAN()` 関数は、数値データのシーケンスの中央値を計算します。

> **Note:**
>
> NULL 値はカウントされません。

## 構文 {#syntax}

```sql
MEDIAN(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|--------------------------|
| `<expr>`  | 任意の数値式 |

## 戻り値の型 {#return-type}

値の型です。

## 例 {#example}

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

**結果**

```sql
|  median_score  |
|----------------|
|      85.0      |
```