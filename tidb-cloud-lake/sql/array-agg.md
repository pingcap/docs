---
title: ARRAY_AGG
summary: ARRAY_AGG 函数（也称其别名 LIST）将查询结果中特定列的所有值（不包括 NULL）转换为数组。
---

# ARRAY_AGG

ARRAY_AGG 函数（也称其别名 LIST）将查询结果中特定列的所有值（不包括 NULL）转换为数组。

## 语法 {#syntax}

```sql
ARRAY_AGG(<expr>) [ WITHIN GROUP ( <orderby_clause> ) ]

LIST(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------| -------------- |
| `<expr>`  | 任意表达式 |

## 可选项 {#optional}

| 可选项                            | 描述                                           |
|-------------------------------------|-------------------------------------------------------|
| WITHIN GROUP [&lt;orderby_clause&gt;](https://docs.pingcap.com/tidbcloudlake/select/#order-by-clause) | 定义有序集合聚合中值的顺序 |

## 返回类型 {#return-type}

返回一个 [数组](/tidb-cloud-lake/sql/array.md)，其元素与原始数据具有相同的类型。

## 示例 {#examples}

以下示例演示了如何使用 ARRAY_AGG 函数以便捷的数组格式聚合并展示数据：

```sql
-- Create a table and insert sample data
CREATE TABLE movie_ratings (
  id INT,
  movie_title VARCHAR,
  user_id INT,
  rating INT
);

INSERT INTO movie_ratings (id, movie_title, user_id, rating)
VALUES (1, 'Inception', 1, 5),
       (2, 'Inception', 2, 4),
       (3, 'Inception', 3, 5),
       (4, 'Interstellar', 1, 4),
       (5, 'Interstellar', 2, 3);

-- List all ratings for Inception in an array
SELECT movie_title, ARRAY_AGG(rating) AS ratings
FROM movie_ratings
WHERE movie_title = 'Inception'
GROUP BY movie_title;

| movie_title |  ratings   |
|-------------|------------|
| Inception   | [5, 4, 5]  |

-- List all ratings for Inception in an array Using `WITHIN GROUP`
SELECT movie_title, ARRAY_AGG(rating) WITHIN GROUP ( ORDER BY rating DESC ) AS ratings
FROM movie_ratings
WHERE movie_title = 'Inception'
GROUP BY movie_title;

| movie_title |  ratings   |
|-------------|------------|
| Inception   | [5, 5, 4]  |
```