---
title: ST_CONVEXHULL
summary: Returns the convex hull of a GEOMETRY object.
---

# ST_CONVEXHULL

> **Note:**
>
> Introduced or updated in v1.2.564.

Returns the convex hull of a GEOMETRY object.

## Syntax

```sql
ST_CONVEXHULL(<geometry>)
```

## Arguments

| Arguments   | Description                                           |
|-------------|-------------------------------------------------------|
| `<geometry>` | The argument must be an expression of type GEOMETRY. |

## Return Type

GEOMETRY.

## Examples

```sql
SELECT ST_ASTEXT(
  ST_CONVEXHULL(
    TO_GEOMETRY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))')
  )
) AS hull;

╭────────────────────────────────╮
│              hull              │
├────────────────────────────────┤
│ POLYGON((2 0,2 2,0 2,0 0,2 0)) │
╰────────────────────────────────╯
```
