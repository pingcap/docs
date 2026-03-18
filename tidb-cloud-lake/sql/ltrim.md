---
title: LTRIM
summary: Removes all occurrences of any character present in the specified trim string from the left side of the string.
---

> **Note:**
>
> Introduced or updated in v1.2.694.

Removes all occurrences of any character present in the specified trim string from the left side of the string.

See also: 

- [TRIM_LEADING](/tidb-cloud-lake/sql/trim-leading.md)
- [RTRIM](/tidb-cloud-lake/sql/rtrim.md)

## Syntax

```sql
LTRIM(<string>, <trim_string>)
```

## Examples

```sql
SELECT LTRIM('xxdatabend', 'xx'), LTRIM('xxdatabend', 'xy');

┌───────────────────────────────────────────────────────┐
│ ltrim('xxdatabend', 'xx') │ ltrim('xxdatabend', 'xy') │
├───────────────────────────┼───────────────────────────┤
│ databend                  │ databend                  │
└───────────────────────────────────────────────────────┘
```