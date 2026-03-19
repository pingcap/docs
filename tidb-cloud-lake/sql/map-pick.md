---
title: MAP_PICK
summary: Returns a new MAP containing the specified key-value pairs from an existing MAP.
---

# MAP_PICK

> **Note:**
>
> Introduced or updated in v1.2.654.

Returns a new MAP containing the specified key-value pairs from an existing MAP.

## Syntax

```sql
MAP_PICK( <map>, <key1> [, <key2>, ... ] )
MAP_PICK( <map>, <array> )
```

## Arguments

| Arguments | Description                                             |
|-----------|-------------------------------------------------------- |
| `<map>`   | The input MAP.                                          |
| `<keyN>`  | The KEYs to be included from the returned MAP.          |
| `<array>` | The Array of KEYs to be included from the returned MAP. |

> **Note:**
>
> - The types of the key expressions and the keys in the map must be the same.
> - Key values not found in the map will be ignored.

## Return Type

Map.

## Examples

```sql
SELECT MAP_PICK({'a':1,'b':2,'c':3}, 'a', 'c');
┌─────────────────────────────────────────┐
│ map_pick({'a':1,'b':2,'c':3}, 'a', 'c') │
├─────────────────────────────────────────┤
│ {'a':1,'c':3}                           │
└─────────────────────────────────────────┘

SELECT MAP_PICK({'a':1,'b':2,'c':3}, ['a', 'b']);
┌───────────────────────────────────────────┐
│ map_pick({'a':1,'b':2,'c':3}, ['a', 'b']) │
├───────────────────────────────────────────┤
│ {'a':1,'b':2}                             │
└───────────────────────────────────────────┘
```
