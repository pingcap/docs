---
title: MAP_CONTAINS_KEY
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.464"/>

Determines whether the specified MAP contains the specified key.

## Syntax

```sql
MAP_CONTAINS_KEY( <map>, <key> )
```

## Arguments

| Arguments | Description             |
|-----------|-------------------------|
| `<map>`   | The map to be searched. |
| `<key>`   | The key to find.        |

## Return Type

Boolean.

## Examples

```sql
SELECT MAP_CONTAINS_KEY({'a':1,'b':2,'c':3}, 'c');
┌────────────────────────────────────────────┐
│ map_contains_key({'a':1,'b':2,'c':3}, 'c') │
├────────────────────────────────────────────┤
│ true                                       │
└────────────────────────────────────────────┘

SELECT MAP_CONTAINS_KEY({'a':1,'b':2,'c':3}, 'x');
┌────────────────────────────────────────────┐
│ map_contains_key({'a':1,'b':2,'c':3}, 'x') │
├────────────────────────────────────────────┤
│ false                                      │
└────────────────────────────────────────────┘
```
