---
title: ARRAY_AGG
summary: ARRAY_AGG 関数（別名 LIST とも呼ばれます）は、クエリ結果内の特定のカラムの値のうち、NULL を除くすべての値を配列に変換します。
---

# ARRAY_AGG

ARRAY_AGG 関数（別名 LIST とも呼ばれます）は、クエリ結果内の特定のカラムの値のうち、NULL を除くすべての値を配列に変換します。

## 構文 {#syntax}

```sql
ARRAY_AGG(<expr>) [ WITHIN GROUP ( <orderby_clause> ) ]

LIST(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------| -------------- |
| `<expr>`  | 任意の式 |

## オプション {#optional}

| オプション                            | 説明                                           |
|-------------------------------------|-------------------------------------------------------|
| WITHIN GROUP [&lt;orderby_clause&gt;](https://docs.pingcap.com/tidbcloudlake/select/#order-by-clause) | 順序付き集合集約における値の順序を定義します        |

## 戻り値の型 {#return-type}

元のデータと同じ型の要素を持つ [配列](/tidb-cloud-lake/sql/array.md) を返します。

## 例 {#examples}

次の例は、ARRAY_AGG 関数を使用してデータを集約し、扱いやすい配列形式で表示する方法を示しています。

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