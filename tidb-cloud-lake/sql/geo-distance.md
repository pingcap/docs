---
title: GEO_DISTANCE
summary: Returns the approximate distance in meters between two points on Earth.
---

# GEO_DISTANCE

Returns the approximate distance in meters between two points on Earth. The points are specified by longitude and latitude in degrees and the distance is computed using a WGS84-based approximation.

## Syntax

```sql
GEO_DISTANCE(<lon1>, <lat1>, <lon2>, <lat2>)
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
SELECT GEO_DISTANCE(55.755831, 37.617673, -55.755831, -37.617673) AS distance;

╭────────────╮
│  distance  │
├────────────┤
│ 14128353.0 │
╰────────────╯
```
