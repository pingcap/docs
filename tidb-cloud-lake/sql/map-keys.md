---
title: MAP_KEYS
summary: Returns the keys in a map.
---

> **Note:**
>
> Introduced or updated in v1.2.429.

Returns the keys in a map.

## Syntax

```sql
MAP_KEYS( <map> )
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<map>`   | The input map. |

## Return Type

Array.

## Examples

```sql
SELECT MAP_KEYS({'a':1,'b':2,'c':3});

┌───────────────────────────────┐
│ map_keys({'a':1,'b':2,'c':3}) │
├───────────────────────────────┤
│ ['a','b','c']                 │
└───────────────────────────────┘
```
