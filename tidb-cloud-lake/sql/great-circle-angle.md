---
title: GREAT_CIRCLE_ANGLE
summary: Returns the central angle in degrees between two points on a sphere.
---

# GREAT_CIRCLE_ANGLE

Returns the central angle in degrees between two points on a sphere. The points are specified by longitude and latitude in degrees.

## Syntax

```sql
GREAT_CIRCLE_ANGLE(<lon1>, <lat1>, <lon2>, <lat2>)
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| `<lon1>` | Longitude of the first point in degrees. |
| `<lat1>` | Latitude of the first point in degrees. |
| `<lon2>` | Longitude of the second point in degrees. |
| `<lat2>` | Latitude of the second point in degrees. |

## Return Type

Float32.

## Examples

```sql
SELECT GREAT_CIRCLE_ANGLE(55.755831, 37.617673, -55.755831, -37.617673) AS angle;

╭───────────╮
│   angle   │
├───────────┤
│ 127.05919 │
╰───────────╯
```
