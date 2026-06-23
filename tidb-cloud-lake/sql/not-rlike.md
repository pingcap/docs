---
title: NOT RLIKE
summary: Returns 1 if the string expr doesn't match the regular expression specified by the pattern pat, 0 otherwise.
---

# NOT RLIKE

Returns 1 if the string expr doesn't match the regular expression specified by the pattern pat, 0 otherwise.

## Syntax

```sql
<expr> NOT RLIKE <pattern>
```

## Examples

```sql
SELECT 'datalake' not rlike 'd*';
+-----------------------------+
| ('datalake' not rlike 'd*') |
+-----------------------------+
|                           0 |
+-----------------------------+
```
