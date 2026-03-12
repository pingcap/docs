---
title: ST_LENGTH
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.555"/>

Returns the Euclidean length of the LineString(s) in a GEOMETRY or GEOGRAPHY object.

## Syntax

```sql
ST_LENGTH(<geometry_or_geography>)
```

## Arguments

| Arguments    | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY containing linestrings. |

:::note
- If `<geometry_or_geography>` is not a `LineString`, `MultiLineString`, or `GeometryCollection` containing linestrings, returns 0.
- If `<geometry_or_geography>` is a `GeometryCollection`, returns the sum of the lengths of the linestrings in the collection.
:::

## Return Type

Double.

## Examples

### GEOMETRY examples

```sql
SELECT
  ST_LENGTH(TO_GEOMETRY('POINT(1 1)')) AS length

┌─────────┐
│  length │
├─────────┤
│       0 │
└─────────┘

SELECT
  ST_LENGTH(TO_GEOMETRY('LINESTRING(0 0, 1 1)')) AS length

┌─────────────┐
│    length   │
├─────────────┤
│ 1.414213562 │
└─────────────┘

SELECT
  ST_LENGTH(
    TO_GEOMETRY('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))')
  ) AS length

┌─────────┐
│  length │
├─────────┤
│       0 │
└─────────┘
```

### GEOGRAPHY examples

```sql
SELECT
  ST_LENGTH(
    ST_GEOGFROMWKT(
      'LINESTRING(0 0, 1 0)'
    )
  ) AS length

╭──────────────────╮
│      length      │
├──────────────────┤
│ 111319.490793274 │
╰──────────────────╯
```
