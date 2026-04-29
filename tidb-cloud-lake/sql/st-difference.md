---
title: ST_DIFFERENCE
summary: Returns the part of the first GEOMETRY object that is not covered by the second GEOMETRY object.
---

# ST_DIFFERENCE

> **Note:**
>
> Introduced or updated in v1.2.895.

Returns the part of the first GEOMETRY object that is not covered by the second GEOMETRY object.

This function only supports GEOMETRY values.

## Syntax

```sql
ST_DIFFERENCE(<geometry1>, <geometry2>)
```

## Arguments

| Arguments     | Description                                            |
|---------------|--------------------------------------------------------|
| `<geometry1>` | The argument must be an expression of type GEOMETRY. |
| `<geometry2>` | The argument must be an expression of type GEOMETRY. |

> **Note:**
>
> The function reports an error if the two input GEOMETRY objects have different SRIDs.

## Return Type

GEOMETRY.

## Examples

```sql
SELECT ST_ASWKT(ST_DIFFERENCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)')));

╭───────────────────────────────────────────────────────────────────────────────╮
│ st_aswkt(st_difference(to_geometry('POINT(0 0)'), to_geometry('POINT(1 1)'))) │
├───────────────────────────────────────────────────────────────────────────────┤
│ POINT(0 0)                                                                    │
╰───────────────────────────────────────────────────────────────────────────────╯
```
