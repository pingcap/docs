---
title: ST_COVEREDBY
summary: Returns TRUE if no point in the first GEOMETRY object lies outside the second GEOMETRY object.
---

# ST_COVEREDBY

> **Note:**
>
> Introduced or updated in v1.2.911.

Returns TRUE if no point in the first GEOMETRY object lies outside the second GEOMETRY object.

See also: [ST_COVERS](/tidb-cloud-lake/sql/st-covers.md)

## Syntax

```sql
ST_COVEREDBY(<geometry1>, <geometry2>)
```

## Arguments

| Arguments     | Description                                          |
|---------------|------------------------------------------------------|
| `<geometry1>` | A GEOMETRY expression (the object being tested).     |
| `<geometry2>` | A GEOMETRY expression (the covering object).         |

## Return Type

Boolean.

## Examples

```sql
SELECT ST_COVEREDBY(
  TO_GEOMETRY('POINT(1 1)'),
  TO_GEOMETRY('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))')
);

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

SELECT ST_COVEREDBY(
  TO_GEOMETRY('POLYGON((1 1, 2 1, 2 2, 1 2, 1 1))'),
  TO_GEOMETRY('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))')
);

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

SELECT ST_COVEREDBY(
  TO_GEOMETRY('POINT(5 5)'),
  TO_GEOMETRY('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))')
);

┌────────┐
│ result │
├────────┤
│ false  │
└────────┘
```
