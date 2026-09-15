---
title: STDDEV_POP
summary: 聚合函数。
---

# STDDEV_POP

聚合函数。

`STDDEV_POP()` 函数返回一个表达式的总体标准差（`VAR_POP()` 的平方根）。

> **Tip:**
>
> 也可以使用 `STD()` 或 `STDDEV()`，它们与 `STDDEV_POP()` 等价，但不是标准 SQL。

> **Note:**
>
> `NULL` 值不会被计入。

## 语法 {#syntax}

```sql
STDDEV_POP(<expr>)
STDDEV(<expr>)
STD(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|--------------------------|
| `<expr>`  | 任意数值表达式 |

## 返回类型 {#return-type}

double

## 示例 {#example}

**创建表并插入示例数据**

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

**查询演示：计算测试分数的总体标准差**

```sql
SELECT STDDEV_POP(score) AS test_score_stddev_pop
FROM test_scores;
```

**结果**

```sql
| test_score_stddev_pop |
|-----------------------|
|        7.07107        |
```