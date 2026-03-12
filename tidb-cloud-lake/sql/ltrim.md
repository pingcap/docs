---
title: LTRIM
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.694"/>

Removes all occurrences of any character present in the specified trim string from the left side of the string.

See also: 

- [TRIM_LEADING](trim-leading.md)
- [RTRIM](rtrim.md)

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