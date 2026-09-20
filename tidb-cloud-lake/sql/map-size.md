---
title: MAP_SIZE
summary: Returns the size of a MAP.
---

# MAP_SIZE

Returns the size of a MAP.

## Syntax

```sql
MAP_SIZE( <map> )
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<map>`   | The input map. |

## Return Type

UInt64.

## Examples

```sql
SELECT MAP_SIZE({'a':1,'b':2,'c':3});

┌───────────────────────────────┐
│ map_size({'a':1,'b':2,'c':3}) │
├───────────────────────────────┤
│ 3                             │
└───────────────────────────────┘
```
