---
title: RANGE
---

Returns an array collected by [start, end).

## Syntax

```sql
RANGE( <start>, <end> )
```

## Examples

```sql
SELECT RANGE(1, 5);

┌───────────────┐
│  range(1, 5)  │
├───────────────┤
│ [1,2,3,4]     │
└───────────────┘
```