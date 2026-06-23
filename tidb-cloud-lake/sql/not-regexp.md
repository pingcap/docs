---
title: NOT REGEXP
summary: Returns 1 if the string expr doesn't match the regular expression specified by the pattern pat, 0 otherwise.
---

# NOT REGEXP

Returns 1 if the string expr doesn't match the regular expression specified by the pattern pat, 0 otherwise.

## Syntax

```sql
<expr> NOT REGEXP <pattern>
```

## Examples

```sql
SELECT 'datalake' NOT REGEXP 'd*';
+------------------------------+
| ('datalake' not regexp 'd*') |
+------------------------------+
|                            0 |
+------------------------------+
```
