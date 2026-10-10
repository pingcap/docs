---
title: MEDIAN_TDIGEST
summary: t-digest アルゴリズムを使用して、数値データのシーケンスの中央値を計算します。
---

# MEDIAN_TDIGEST

[t-digest](https://github.com/tdunning/t-digest/blob/master/docs/t-digest-paper/histo.pdf) アルゴリズムを使用して、数値データのシーケンスの中央値を計算します。

> **Note:**
>
> NULL 値は計算に含まれません。

## 構文 {#syntax}

```sql
MEDIAN_TDIGEST(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|--------------------------|
| `<expr>`  | 任意の数値式 |

## 戻り値の型 {#return-type}

入力値と同じデータ型の値を返します。

## 例 {#examples}

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