---
title: ST_HAUSDORFFDISTANCE
summary: Returns the discrete Hausdorff distance between two GEOMETRY objects. This measures how far apart two geometries are by finding the greatest distance from any vertex in one object to the nearest vertex in the other.
---

# ST_HAUSDORFFDISTANCE

Returns the discrete Hausdorff distance between two GEOMETRY objects. This measures how far apart two geometries are by finding the greatest distance from any vertex in one object to the nearest vertex in the other.

## Syntax

```sql
ST_HAUSDORFFDISTANCE(<geometry1>, <geometry2>)
```

## Arguments

| Arguments     | Description                                          |
|---------------|------------------------------------------------------|
| `<geometry1>` | A GEOMETRY expression.                               |
| `<geometry2>` | A GEOMETRY expression.                               |

## Return Type

Double.

## Examples

```sql
SELECT ST_HAUSDORFFDISTANCE(
  TO_GEOMETRY('POINT(0 0)'),
  TO_GEOMETRY('POINT(0 1)')
);

┌────────┐
│ result │
├────────┤
│ 1.0    │
└────────┘

SELECT ST_HAUSDORFFDISTANCE(
  TO_GEOMETRY('LINESTRING(0 0, 1 0)'),
  TO_GEOMETRY('LINESTRING(0 1, 1 1)')
);

┌────────┐
│ result │
├────────┤
│ 1.0    │
└────────┘

SELECT ST_HAUSDORFFDISTANCE(
  TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'),
  TO_GEOMETRY('POLYGON((2 0, 3 0, 3 1, 2 1, 2 0))')
);

┌────────┐
│ result │
├────────┤
│ 2.0    │
└────────┘
```
