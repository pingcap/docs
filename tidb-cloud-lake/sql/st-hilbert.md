---
title: ST_HILBERT
summary: Encodes a GEOMETRY or GEOGRAPHY object into a Hilbert curve index.
---

# ST_HILBERT

> **Note:**
>
> Introduced or updated in v1.2.885.

Encodes a GEOMETRY or GEOGRAPHY object into a Hilbert curve index. The function uses the center of the geometry's bounding box as the point to encode. When bounds are provided, the point is normalized into the specified bounding box before encoding.

## Syntax

```sql
ST_HILBERT(<geometry_or_geography>)
ST_HILBERT(<geometry_or_geography>, <bounds>)
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| `<geometry_or_geography>` | The argument must be an expression of type GEOMETRY or GEOGRAPHY. |
| `<bounds>` | Optional. An array `[xmin, ymin, xmax, ymax]` used to normalize the point before encoding. |

> **Note:**
>
> - Geometry: If no bounding box is provided, GEOMETRY coordinates are not normalized to a specific bounding box. Instead, the center point values are mapped to the full `float32` domain, and then encoded into the Hilbert index.
> - Geography: If no bounding box is provided, the default bounds are `[-180, -90, 180, 90]`.

## Return Type

UInt64.

## Examples

### GEOMETRY examples

```sql
SELECT ST_HILBERT(TO_GEOMETRY('POINT(1 2)')) AS hilbert1, ST_HILBERT(TO_GEOMETRY('POINT(5 5)')) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  3355443200 │  2155872256 │
╰───────────────────────────╯

SELECT ST_HILBERT(TO_GEOMETRY('POINT(1 2)'), [0, 0, 1, 1]) AS hilbert1, ST_HILBERT(TO_GEOMETRY('POINT(5 5)'), [0, 0, 5, 5]) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  2863311530 │  2863311530 │
╰───────────────────────────╯
```

### GEOGRAPHY examples

```sql
SELECT ST_HILBERT(TO_GEOGRAPHY('POINT(113.15 23.06)')) AS hilbert1, ST_HILBERT(TO_GEOGRAPHY('POINT(116.25 39.54)')) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  3070259060 │  3033451300 │
╰───────────────────────────╯

SELECT ST_HILBERT(TO_GEOGRAPHY('POINT(113.15 23.06)'), [73, 4, 135, 53]) AS hilbert1, ST_HILBERT(TO_GEOGRAPHY('POINT(116.25 39.54)'), [73, 4, 135, 53]) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  3533607194 │  2330429279 │
╰───────────────────────────╯
```
