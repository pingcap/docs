---
title: RTRIM
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.694"/>

Removes all occurrences of any character present in the specified trim string from the right side of the string.

See also: 

- [TRIM_TRAILING](trim-trailing.md)
- [LTRIM](ltrim.md)

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