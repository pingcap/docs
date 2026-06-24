---
title: TRIM_TRAILING
summary: Removes all occurrences of the specified trim string from the end of the string.
---

# TRIM_TRAILING

Removes all occurrences of the specified trim string from the end of the string.

See also:

- [RTRIM](/tidb-cloud-lake/sql/rtrim.md)
- [TRIM_LEADING](/tidb-cloud-lake/sql/trim-leading.md)

## Syntax

```sql
TRIM_TRAILING(<string>, <trim_string>)
```

## Examples

```sql
SELECT TRIM_TRAILING('datalakexx', 'xxx'), TRIM_TRAILING('datalakexx', 'xx'), TRIM_TRAILING('datalakexx', 'x');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_trailing('datalakexx', 'xxx') │ trim_trailing('datalakexx', 'xx') │ trim_trailing('datalakexx', 'x') │
├────────────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ datalakexx                         │ datalake                          │ datalake                         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
