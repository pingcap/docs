---
title: STDDEV_POP
summary: 集約関数。
---

# STDDEV_POP

集約関数。

`STDDEV_POP()` 関数は、式の母標準偏差（`VAR_POP()` の平方根）を返します。

> **Tip:**
>
> `STD()` または `STDDEV()` も使用できます。これらは同等ですが、標準 SQL ではありません。

> **Note:**
>
> `NULL` 値はカウントされません。

## 構文 {#syntax}

```sql
STDDEV_POP(<expr>)
STDDEV(<expr>)
STD(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|--------------------------|
| `<expr>`  | 任意の数値式 |

## 戻り値の型 {#return-type}

double

## 例 {#example}

**Create a Table and Insert Sample Data**

```sql
CREATE TABLE test_scores (
  id INT,
  student_id INT,
  score FLOAT
);

INSERT INTO test_scores (id, student_id, score)
VALUES (1, 1, 80),
       (2, 2, 85),
       (3, 3, 90),
       (4, 4, 95),
       (5, 5, 100);
```

**Query Demo: Calculate Population Standard Deviation of Test Scores**

```sql
SELECT STDDEV_POP(score) AS test_score_stddev_pop
FROM test_scores;
```

**結果**

```sql
| test_score_stddev_pop |
|-----------------------|
|        7.07107        |
```