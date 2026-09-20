---
title: TRIM_BOTH
summary: Removes all occurrences of the specified trim string from the beginning, end, or both sides of the string.
---

# TRIM_BOTH

Removes all occurrences of the specified trim string from the beginning, end, or both sides of the string.

See also: [TRIM](/tidb-cloud-lake/sql/trim.md)

## Syntax

```sql
TRIM_BOTH(<string>, <trim_string>)
```

## Examples

```sql
SELECT TRIM_BOTH('xxdatalakexx', 'xxx'), TRIM_BOTH('xxdatalakexx', 'xx'), TRIM_BOTH('xxdatalakexx', 'x');

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_both('xxdatalakexx', 'xxx') │ trim_both('xxdatalakexx', 'xx') │ trim_both('xxdatalakexx', 'x') │
├──────────────────────────────────┼─────────────────────────────────┼────────────────────────────────┤
│ xxdatalakexx                     │ datalake                        │ datalake                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
