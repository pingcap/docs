---
title: HAVERSINE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.555"/>

Calculates the great circle distance in kilometers between two points on the Earth’s surface, using the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula). The two points are specified by their latitude and longitude in degrees.

## Syntax

```sql
HAVERSINE(<lat1>, <lon1>, <lat2>, <lon2>)
```

## Arguments

| Arguments | Description                        |
|-----------|------------------------------------|
| `<lat1>`  | The latitude of the first point.   |
| `<lon1>`  | The longitude of the first point.  |
| `<lat2>`  | The latitude of the second point.  |
| `<lon2>`  | The longitude of the second point. |

## Return Type

Double.

## Examples

```sql
SELECT
  HAVERSINE(40.7127, -74.0059, 34.0500, -118.2500) AS distance

┌────────────────┐
│    distance    │
├────────────────┤
│ 3936.390533556 │
└────────────────┘
```
