---
title: ST_GEOGPOINTFROMGEOHASH
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.413"/>

Returns a GEOGRAPHY object for the point that represents center of a [geohash](https://en.wikipedia.org/wiki/Geohash).

## Syntax

```sql
ST_GEOGPOINTFROMGEOHASH(<geohash>)
```

## Arguments

| Arguments   | Description                     |
|-------------|---------------------------------|
| `<geohash>` | The argument must be a geohash. |

## Return Type

Geography.

## Examples

```sql
SELECT
  ST_ASWKT(
    ST_GEOGPOINTFROMGEOHASH(
      's02equ0'
    )
  ) AS pipeline_geography;

╭──────────────────────────────────────────────╮
│              pipeline_geography              │
│                    String                    │
├──────────────────────────────────────────────┤
│ POINT(1.0004425048828125 2.0001983642578125) │
╰──────────────────────────────────────────────╯
```
