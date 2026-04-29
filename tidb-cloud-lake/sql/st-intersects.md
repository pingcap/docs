---
title: ST_INTERSECTS
summary: Returns TRUE if two GEOMETRY objects share any portion of space.
---

# ST_INTERSECTS

> **Note:**
>
> Introduced or updated in v1.2.564.

Returns TRUE if two GEOMETRY objects share any portion of space.

## Syntax

```sql
ST_INTERSECTS(<geometry1>, <geometry2>)
```

## Arguments

| Arguments     | Description                                           |
|---------------|-------------------------------------------------------|
| `<geometry1>` | The argument must be an expression of type GEOMETRY. |
| `<geometry2>` | The argument must be an expression of type GEOMETRY. |

> **Note:**
>
> The function reports an error if the two input GEOMETRY objects have different SRIDs.

## Return Type

Boolean.

## Examples

```sql
SELECT ST_INTERSECTS(
  TO_GEOMETRY('LINESTRING(0 0, 2 2)'),
  TO_GEOMETRY('LINESTRING(0 2, 2 0)')
) AS intersects;

╭────────────╮
│ intersects │
├────────────┤
│ true       │
╰────────────╯

SELECT ST_INTERSECTS(
  TO_GEOMETRY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'),
  TO_GEOMETRY('POINT(3 3)')
) AS intersects;

╭────────────╮
│ intersects │
├────────────┤
│ false      │
╰────────────╯
```
