---
title: MULTIPLY
---

The MULTIPLY function performs multiplication between two numbers. It is equivalent to using the `*` operator.

## Syntax

```sql
MULTIPLY(x, y)
-- Or using the operator syntax
x * y
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| x, y      | Numeric expressions to multiply together. |

## Return Type

Returns a numeric value with the appropriate data type based on the input arguments.

## Examples

```sql
-- Using the function syntax
SELECT MULTIPLY(5, 3);
+----------------+
| MULTIPLY(5, 3) |
+----------------+
|             15 |
+----------------+

-- Using the operator syntax
SELECT 5 * 3;
+-------+
| 5 * 3 |
+-------+
|    15 |
+-------+

-- With decimal numbers
SELECT MULTIPLY(2.5, 4);
+------------------+
| MULTIPLY(2.5, 4) |
+------------------+
|             10.0 |
+------------------+

-- With column references
SELECT number, MULTIPLY(number, 10) AS multiplied 
FROM numbers(5);
+--------+------------+
| number | multiplied |
+--------+------------+
|      0 |          0 |
|      1 |         10 |
|      2 |         20 |
|      3 |         30 |
|      4 |         40 |
+--------+------------+
```

## See Also

- [PLUS](plus.md) / [ADD](add.md)
- [MINUS](minus.md) / [SUBTRACT](subtract.md)
- [DIV](div.md)
