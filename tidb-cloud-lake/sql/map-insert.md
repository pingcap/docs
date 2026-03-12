---
title: MAP_INSERT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.654"/>

Returns a new MAP consisting of the input MAP with a new key-value pair inserted (an existing key updated with a new value).

## Syntax

```sql
MAP_INSERT( <map>, <key>, <value> [, <updateFlag> ] )
```

## Arguments

| Arguments      | Description                                                                                  |
|----------------|----------------------------------------------------------------------------------------------|
| `<map>`        | The input MAP.                                                                               |
| `<key>`        | The new key to insert into the MAP.                                                          |
| `<value>`      | The new value to insert into the MAP.                                                        |
| `<updateFlag>` | The boolean flag indicates whether an existing key can be overwritten. The default is FALSE. |

## Return Type

Map.

## Examples

```sql
SELECT MAP_INSERT({'a':1,'b':2,'c':3}, 'd', 4);
┌─────────────────────────────────────────┐
│ map_insert({'a':1,'b':2,'c':3}, 'd', 4) │
├─────────────────────────────────────────┤
│ {'a':1,'b':2,'c':3,'d':4}               │
└─────────────────────────────────────────┘

SELECT MAP_INSERT({'a':1,'b':2,'c':3}, 'a', 5, true);
┌───────────────────────────────────────────────┐
│ map_insert({'a':1,'b':2,'c':3}, 'a', 5, TRUE) │
├───────────────────────────────────────────────┤
│ {'a':5,'b':2,'c':3}                           │
└───────────────────────────────────────────────┘
```
