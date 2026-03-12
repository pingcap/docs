---
title: MAP_DELETE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.547"/>

Returns an existing MAP with one or more keys removed.

## Syntax

```sql
MAP_DELETE( <map>, <key1> [, <key2>, ... ] )
MAP_DELETE( <map>, <array> )
```

## Arguments

| Arguments | Description                                            |
|-----------|--------------------------------------------------------|
| `<map>`   | The MAP that contains the KEY to remove.               |
| `<keyN>`  | The KEYs to be omitted from the returned MAP.          |
| `<array>` | The Array of KEYs to be omitted from the returned MAP. |

:::note
- The types of the key expressions and the keys in the map must be the same.
- Key values not found in the map will be ignored.
:::

## Return Type

Map.

## Examples

```sql
SELECT MAP_DELETE({'a':1,'b':2,'c':3}, 'a', 'c');
┌───────────────────────────────────────────┐
│ map_delete({'a':1,'b':2,'c':3}, 'a', 'c') │
├───────────────────────────────────────────┤
│ {'b':2}                                   │
└───────────────────────────────────────────┘

SELECT MAP_DELETE({'a':1,'b':2,'c':3}, ['a', 'b']);
┌─────────────────────────────────────────────┐
│ map_delete({'a':1,'b':2,'c':3}, ['a', 'b']) │
├─────────────────────────────────────────────┤
│ {'c':3}                                     │
└─────────────────────────────────────────────┘
```
