---
title: POINT_IN_ELLIPSES
summary: Returns 1 if the point lies inside any of the provided ellipses, otherwise returns 0.
---

# POINT_IN_ELLIPSES

Returns 1 if the point lies inside any of the provided ellipses, otherwise returns 0. Each ellipse is defined by a center point and its semi-major and semi-minor axes.

## Syntax

```sql
POINT_IN_ELLIPSES(x, y, x1, y1, a1, b1 [, x2, y2, a2, b2, ...])
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| `x`, `y` | Coordinates of the point to test. |
| `x1`, `y1` | Center of the first ellipse. |
| `a1`, `b1` | Semi-major and semi-minor axis lengths of the first ellipse. |
| `x2`, `y2`, `a2`, `b2`, ... | Optional additional ellipses, defined the same way. |

## Return Type

UInt8 (1 for true, 0 for false).

## Examples

```sql
SELECT POINT_IN_ELLIPSES(10, 10, 10, 9.1, 1, 0.9999) AS inside;

╭────────╮
│ inside │
├────────┤
│      1 │
╰────────╯
```
