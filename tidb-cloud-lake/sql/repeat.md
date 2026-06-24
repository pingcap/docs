---
title: REPEAT
summary: Returns a string consisting of the string str repeated count times. If count is less than 1, returns an empty string. Returns NULL if str or count are NULL.
---

# REPEAT

Returns a string consisting of the string str repeated count times. If count is less than 1, returns an empty string. Returns NULL if str or count are NULL.

## Syntax

```sql
REPEAT(<str>, <count>)
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| `<str>`   | The string. |
| `<count>` | The number. |

## Examples

```sql
SELECT REPEAT('datalake', 3);
+--------------------------+
| REPEAT('datalake', 3)    |
+--------------------------+
| datalakedatalakedatalake |
+--------------------------+

SELECT REPEAT('datalake', 0);
+-----------------------+
| REPEAT('datalake', 0) |
+-----------------------+
|                       |
+-----------------------+

SELECT REPEAT('datalake', NULL);
+--------------------------+
| REPEAT('datalake', NULL) |
+--------------------------+
|                     NULL |
+--------------------------+
```
