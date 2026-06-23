---
title: CONCAT
summary: Returns the string that results from concatenating the arguments. May have one or more arguments. If all arguments are nonbinary strings, the result is a nonbinary string. If the arguments include any binary strings, the result is a binary string. A numeric argument is converted to its equivalent nonbinary string form.
---

# CONCAT

Returns the string that results from concatenating the arguments. May have one or more arguments. If all arguments are nonbinary strings, the result is a nonbinary string. If the arguments include any binary strings, the result is a binary string. A numeric argument is converted to its equivalent nonbinary string form.

## Syntax

```sql
CONCAT(<expr1>, ...)
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| `<expr1>` | string      |

## Return Type

A `VARCHAR` data type value Or `NULL` data type.

## Examples

```sql
SELECT CONCAT('data', 'lake');
+------------------------+
| concat('data', 'lake') |
+------------------------+
| datalake               |
+------------------------+

SELECT CONCAT('data', NULL, 'lake');
+------------------------------+
| CONCAT('data', NULL, 'lake') |
+------------------------------+
|                         NULL |
+------------------------------+

SELECT CONCAT('14.3');
+----------------+
| concat('14.3') |
+----------------+
| 14.3           |
+----------------+
```
