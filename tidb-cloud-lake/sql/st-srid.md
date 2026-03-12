---
title: ST_SRID
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.458"/>

Returns the SRID (spatial reference system identifier) of a GEOMETRY or GEOGRAPHY object.

## Syntax

```sql
ST_SRID(<geometry_or_geography>)
```

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY. |

## Return Type

INT32.

:::note
If the Geometry don't have a SRID, a default value 4326 will be returned.
:::

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_SRID(
    TO_GEOMETRY(
      'POINT(-122.306100 37.554162)',
      1234
    )
  ) AS pipeline_srid;

┌───────────────┐
│ pipeline_srid │
├───────────────┤
│          1234 │
└───────────────┘

SELECT
  ST_SRID(
    ST_MAKEGEOMPOINT(
      37.5, 45.5
    )
  ) AS pipeline_srid;

┌───────────────┐
│ pipeline_srid │
├───────────────┤
│          4326 │
└───────────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_SRID(
    ST_GEOGFROMWKT(
      'POINT(1 2)'
    )
  ) AS pipeline_srid;

┌───────────────┐
│ pipeline_srid │
├───────────────┤
│          4326 │
└───────────────┘
```
