---
title: MAP_VALUES
summary: Returns the values in a map.
---

> **Note:**
>
> Introduced or updated in v1.2.429.

Returns the values in a map.

## Syntax

```sql
MAP_VALUES( <map> )
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<map>`   | The input map. |

## Return Type

Array.

## Examples

```sql
SELECT MAP_VALUES({'a':1,'b':2,'c':3});

┌─────────────────────────────────┐
│ map_values({'a':1,'b':2,'c':3}) │
├─────────────────────────────────┤
│ [1,2,3]                         │
└─────────────────────────────────┘
```
