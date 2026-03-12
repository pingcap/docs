---
title: ARRAY_AGG
title_includes: LIST
---

The ARRAY_AGG function (also known by its alias LIST) transforms all the values, excluding NULL, of a specific column in a query result into an array.

## Syntax

```sql
ARRAY_AGG(<expr>) [ WITHIN GROUP ( <orderby_clause> ) ]

LIST(<expr>)
```

## Arguments

| Arguments | Description    |
|-----------| -------------- |
| `<expr>`  | Any expression |

## Optional

| Optional                            | Description                                           |
|-------------------------------------|-------------------------------------------------------|
| WITHIN GROUP [&lt;orderby_clause&gt;](https://docs.databend.com/sql/sql-commands/query-syntax/query-select#order-by-clause) | Defines the order of values in ordered set aggregates        |

## Return Type

Returns an [Array](../../00-sql-reference/10-data-types/array.md) with elements that are of the same type as the original data.

## Examples

This example demonstrates how the ARRAY_AGG function can be used to aggregate and present data in a convenient array format:

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
