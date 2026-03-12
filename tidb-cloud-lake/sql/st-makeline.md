---
title: ST_MAKELINE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.391"/>

Constructs a GEOMETRY or GEOGRAPHY object that represents a line connecting the points in the input two GEOMETRY or GEOGRAPHY objects.

## Syntax

```sql
ST_MAKELINE(<geometry_or_geography1>, <geometry_or_geography2>)
```

## Aliases

- [ST_MAKE_LINE](st-make-line.md)

## Arguments

| Arguments     | Description                                                                                                 |
|---------------|-------------------------------------------------------------------------------------------------------------|
| `<geometry_or_geography1>` | A GEOMETRY or GEOGRAPHY object containing the points to connect. This object must be a Point, MultiPoint, or LineString. |
| `<geometry_or_geography2>` | A GEOMETRY or GEOGRAPHY object containing the points to connect. This object must be a Point, MultiPoint, or LineString. |

## Return Type

Geometry.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_MAKELINE(
    ST_GEOMETRYFROMWKT(
      'POINT(-122.306100 37.554162)'
    ),
    ST_GEOMETRYFROMWKT(
      'POINT(-104.874173 56.714538)'
    )
  ) AS pipeline_line;

┌───────────────────────────────────────────────────────┐
│                     pipeline_line                     │
├───────────────────────────────────────────────────────┤
│ LINESTRING(-122.3061 37.554162,-104.874173 56.714538) │
└───────────────────────────────────────────────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_MAKELINE(
    ST_GEOGFROMWKT(
      'POINT(-122.306100 37.554162)'
    ),
    ST_GEOGFROMWKT(
      'POINT(-104.874173 56.714538)'
    )
  ) AS pipeline_line;

╭───────────────────────────────────────────────────────╮
│                     pipeline_line                     │
├───────────────────────────────────────────────────────┤
│ LINESTRING(-122.3061 37.554162,-104.874173 56.714538) │
╰───────────────────────────────────────────────────────╯
```
