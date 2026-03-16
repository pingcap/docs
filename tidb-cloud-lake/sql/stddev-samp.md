---
title: STDDEV_SAMP
---

Returns the sample standard deviation (the square root of VAR_SAMP()) of an expression.

- NULL values are ignored.
- STDDEV_SAMP() returns `NULL` instead of `0` when there is only one input record.

## Syntax

```sql
STDDEV_SAMP(<expr>)
```

## Arguments

| Arguments | Description              |
| --------- | ------------------------ |
| `<expr>`  | Any numerical expression |

## Return Type

Double.

## Example

**Create a Table and Insert Sample Data**

```sql
CREATE TABLE height_data (
  id INT,
  person_id INT,
  height FLOAT
);

INSERT INTO height_data (id, person_id, height)
VALUES (1, 1, 5.8),
       (2, 2, 6.1),
       (3, 3, 5.9),
       (4, 4, 5.7),
       (5, 5, 6.3);
```

**Query Demo: Calculate Sample Standard Deviation of Heights**

```sql
SELECT STDDEV_SAMP(height) AS height_stddev_samp
FROM height_data;
```

**Result**

```sql
| height_stddev_samp |
|--------------------|
|      0.240         |
```
