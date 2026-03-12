---
title: MAP_CAT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.459"/>

Returns the concatenatation of two MAPs.

## Syntax

```sql
MAP_CAT( <map1>, <map2> )
```

## Arguments

| Arguments | Description                     |
|-----------|---------------------------------|
| `<map1>`  | The source MAP.                 |
| `<map2>`  | The MAP to be appended to map1. |

:::note
- If both map1 and map2 have a value with the same key, then the output map contains the value from map2.
- If either argument is NULL, the function returns NULL without reporting any error.
:::

## Return Type

Map.

## Examples

```sql
SELECT MAP_CAT({'a':1,'b':2,'c':3}, {'c':5,'d':6});
┌─────────────────────────────────────────────┐
│ map_cat({'a':1,'b':2,'c':3}, {'c':5,'d':6}) │
├─────────────────────────────────────────────┤
│ {'a':1,'b':2,'c':5,'d':6}                   │
└─────────────────────────────────────────────┘
```
