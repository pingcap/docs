---
title: ST_DWITHIN
summary: Returns TRUE if two GEOMETRY objects are within the specified Euclidean distance.
---

# ST_DWITHIN

> **Note:**
>
> Introduced or updated in v1.2.895.

Returns TRUE if two GEOMETRY objects are within the specified Euclidean distance.

This function only supports GEOMETRY values.

## Syntax

```sql
ST_DWITHIN(<geometry1>, <geometry2>, <distance>)
```

## Arguments

| Arguments     | Description                                                  |
|---------------|--------------------------------------------------------------|
| `<geometry1>` | The argument must be an expression of type GEOMETRY.       |
| `<geometry2>` | The argument must be an expression of type GEOMETRY.       |
| `<distance>`  | The maximum Euclidean distance as a Float64-compatible value. |

> **Note:**
>
> The function reports an error if the two input GEOMETRY objects have different SRIDs.

## Return Type

Boolean.

## Examples

```sql
SELECT ST_DWITHIN(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)'), 1.5);

╭───────────────────────────────────────────────────────────────────────╮
│ st_dwithin(to_geometry('POINT(0 0)'), to_geometry('POINT(1 1)'), 1.5) │
├───────────────────────────────────────────────────────────────────────┤
│ true                                                                  │
╰───────────────────────────────────────────────────────────────────────╯
```

```sql
SELECT ST_DWITHIN(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('LINESTRING(2 0, 2 2)'), 1.9);

╭─────────────────────────────────────────────────────────────────────────────────╮
│ st_dwithin(to_geometry('POINT(0 0)'), to_geometry('LINESTRING(2 0, 2 2)'), 1.9) │
├─────────────────────────────────────────────────────────────────────────────────┤
│ false                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────╯
```
