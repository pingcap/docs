---
title: ST_UNION
summary: Returns the combined GEOMETRY made from two input GEOMETRY objects.
---

# ST_UNION

> **Note:**
>
> Introduced or updated in v1.2.895.

Returns the combined GEOMETRY made from two input GEOMETRY objects.

This function only supports GEOMETRY values.

## Syntax

```sql
ST_UNION(<geometry1>, <geometry2>)
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
SELECT ST_ASWKT(ST_UNION(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)')));

╭──────────────────────────────────────────────────────────────────────────╮
│ st_aswkt(st_union(to_geometry('POINT(0 0)'), to_geometry('POINT(1 1)'))) │
├──────────────────────────────────────────────────────────────────────────┤
│ MULTIPOINT(0 0,1 1)                                                      │
╰──────────────────────────────────────────────────────────────────────────╯
```
