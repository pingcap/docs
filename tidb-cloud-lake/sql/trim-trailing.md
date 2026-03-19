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
SELECT TRIM_TRAILING('databendxx', 'xxx'), TRIM_TRAILING('databendxx', 'xx'), TRIM_TRAILING('databendxx', 'x');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_trailing('databendxx', 'xxx') │ trim_trailing('databendxx', 'xx') │ trim_trailing('databendxx', 'x') │
├────────────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ databendxx                         │ databend                          │ databend                         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
