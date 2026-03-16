---
title: ST_AREA
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.555"/>

Returns the area of a GEOMETRY or GEOGRAPHY object. For GEOMETRY inputs, the function uses planar area based on the [shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula). For GEOGRAPHY inputs, the function measures geodesic area on an ellipsoidal model of the earth using the method described in [Karney (2013)](https://arxiv.org/pdf/1109.4448.pdf).

## Syntax

```sql
ST_AREA(<geometry_or_geography>)
```

## Arguments

| Arguments                 | Description                                                     |
|---------------------------|-----------------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY. |

## Return Type

Double.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_AREA(
    TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')
  ) AS area

┌──────┐
│ area │
├──────┤
│ 1.0  │
└──────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_AREA(
    TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')
  ) AS area

╭────────────────────╮
│        area        │
├────────────────────┤
│ 12308778361.469452 │
╰────────────────────╯
```
