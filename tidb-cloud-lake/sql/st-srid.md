---
title: ST_SRID
summary: Returns the SRID (spatial reference system identifier) of a GEOMETRY or GEOGRAPHY object.
---

# ST_SRID

> **Note:**
>
> Introduced or updated in v1.2.458.

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

> **Note:**
>
> - If the Geometry don't have a SRID, a default value `0` will be returned.
> - For Geography, the SRID is always `4326`.

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
│             0 │
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
