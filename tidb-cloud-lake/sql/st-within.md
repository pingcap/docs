---
title: ST_WITHIN
summary: Returns TRUE if the first GEOMETRY object is completely within the second GEOMETRY object.
---

# ST_WITHIN

> **Note:**
>
> Introduced or updated in v1.2.564.

Returns TRUE if the first GEOMETRY object is completely within the second GEOMETRY object.

## Syntax

```sql
ST_WITHIN(<geometry1>, <geometry2>)
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
SELECT ST_WITHIN(
  TO_GEOMETRY('POINT(1 1)'),
  TO_GEOMETRY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))')
) AS within;

╭─────────╮
│  within │
├─────────┤
│ true    │
╰─────────╯
```
