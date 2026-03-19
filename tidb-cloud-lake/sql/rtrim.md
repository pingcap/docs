---
title: RTRIM
summary: Removes all occurrences of any character present in the specified trim string from the right side of the string.
---

# RTRIM

> **Note:**
>
> Introduced or updated in v1.2.694.

Removes all occurrences of any character present in the specified trim string from the right side of the string.

See also:

- [TRIM_TRAILING](/tidb-cloud-lake/sql/trim-trailing.md)
- [LTRIM](/tidb-cloud-lake/sql/ltrim.md)

## Syntax

```sql
RTRIM(<string>, <trim_string>)
```

## Examples

```sql
SELECT RTRIM('databendxx', 'x'), RTRIM('databendxx', 'xy');

┌──────────────────────────────────────────────────────┐
│ rtrim('databendxx', 'x') │ rtrim('databendxx', 'xy') │
├──────────────────────────┼───────────────────────────┤
│ databend                 │ databend                  │
└──────────────────────────────────────────────────────┘
```
