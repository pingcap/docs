---
title: TRIM_BOTH
summary: Removes all occurrences of the specified trim string from the beginning, end, or both sides of the string.
---
Removes all occurrences of the specified trim string from the beginning, end, or both sides of the string.

See also: [TRIM](/tidb-cloud-lake/sql/trim.md)

## Syntax

```sql
TRIM_BOTH(<string>, <trim_string>)
```

## Examples

```sql
SELECT TRIM_BOTH('xxdatabendxx', 'xxx'), TRIM_BOTH('xxdatabendxx', 'xx'), TRIM_BOTH('xxdatabendxx', 'x');

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_both('xxdatabendxx', 'xxx') │ trim_both('xxdatabendxx', 'xx') │ trim_both('xxdatabendxx', 'x') │
├──────────────────────────────────┼─────────────────────────────────┼────────────────────────────────┤
│ xxdatabendxx                     │ databend                        │ databend                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```