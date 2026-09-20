---
title: TRIM_LEADING
summary: Removes all occurrences of the specified trim string from the beginning of the string.
---

# TRIM_LEADING

Removes all occurrences of the specified trim string from the beginning of the string.

See also:

- [LTRIM](/tidb-cloud-lake/sql/ltrim.md)
- [TRIM_TRAILING](/tidb-cloud-lake/sql/trim-trailing.md)

## Syntax

```sql
TRIM_LEADING(<string>, <trim_string>)
```

## Examples

```sql
SELECT TRIM_LEADING('xxdatalake', 'xxx'), TRIM_LEADING('xxdatalake', 'xx'), TRIM_LEADING('xxdatalake', 'x');

┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_leading('xxdatalake', 'xxx') │ trim_leading('xxdatalake', 'xx') │ trim_leading('xxdatalake', 'x') │
├───────────────────────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ xxdatalake                        │ datalake                         │ datalake                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
