---
title: ST_GEOGFROMGEOHASH
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.402"/>

Returns a GEOGRAPHY object for the polygon that represents the boundaries of a [geohash](https://en.wikipedia.org/wiki/Geohash).

## Syntax

```sql
ST_GEOGFROMGEOHASH(<geohash>)
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
    ST_GEOGFROMGEOHASH(
      '9q60y60rhs'
    )
  ) AS pipeline_geography;

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                         pipeline_geography                                                                        │
│                                                                               String                                                                              │
├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ POLYGON((-120.66229462623596 35.30029535293579,-120.66229462623596 35.30030071735382,-120.66230535507202 35.30030071735382,-120.66230535507202 35.30029535293579… │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
