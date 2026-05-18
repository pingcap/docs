---
title: ST_COVERS
summary: Returns TRUE if no point in the second GEOMETRY object lies outside the first GEOMETRY object.
---

# ST_COVERS

> **Note:**
>
> Introduced or updated in v1.2.911.

Returns TRUE if no point in the second GEOMETRY object lies outside the first GEOMETRY object.

See also: [ST_COVEREDBY](/tidb-cloud-lake/sql/st-coveredby.md)

## Syntax

```sql
ST_COVERS(<geometry1>, <geometry2>)
```

## Arguments

| Arguments     | Description                                          |
|---------------|------------------------------------------------------|
| `<geometry1>` | A GEOMETRY expression (the covering object).         |
| `<geometry2>` | A GEOMETRY expression (the object being tested).     |

## Return Type

Boolean.

## Examples

```sql
-- A polygon covers a smaller polygon inside it
SELECT ST_COVERS(
  TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'),
  TO_GEOMETRY('POLYGON((-1 0, 0 1, 1 0, -1 0))')
);

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

-- A polygon covers a linestring on its boundary
SELECT ST_COVERS(
  TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'),
  TO_GEOMETRY('LINESTRING(-1 1, 0 2, 1 1)')
);

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

-- A point outside the polygon is not covered
SELECT ST_COVERS(
  TO_GEOMETRY('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))'),
  TO_GEOMETRY('POINT(5 5)')
);

┌────────┐
│ result │
├────────┤
│ false  │
└────────┘
```
