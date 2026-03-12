---
title: TRIM_LEADING
---

Removes all occurrences of the specified trim string from the beginning of the string.

See also: 

- [LTRIM](ltrim.md)
- [TRIM_TRAILING](trim-trailing.md)

## Syntax

```sql
TRIM_LEADING(<string>, <trim_string>)
```

## Examples

```sql
SELECT TRIM_LEADING('xxdatabend', 'xxx'), TRIM_LEADING('xxdatabend', 'xx'), TRIM_LEADING('xxdatabend', 'x');

┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_leading('xxdatabend', 'xxx') │ trim_leading('xxdatabend', 'xx') │ trim_leading('xxdatabend', 'x') │
├───────────────────────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ xxdatabend                        │ databend                         │ databend                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```