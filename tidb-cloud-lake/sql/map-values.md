---
title: MAP_VALUES
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.429"/>

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
