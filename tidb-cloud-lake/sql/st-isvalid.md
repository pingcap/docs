---
title: ST_ISVALID
summary: Returns TRUE if the GEOMETRY object is geometrically valid as defined by the OGC specification.
---

# ST_ISVALID

> **Note:**
>
> Introduced or updated in v1.2.911.

Returns TRUE if the GEOMETRY object is geometrically valid as defined by the OGC specification.

## Syntax

```sql
ST_ISVALID(<geometry>)
```

## Arguments

| Arguments    | Description                                          |
|--------------|------------------------------------------------------|
| `<geometry>` | A GEOMETRY expression.                               |

## Return Type

Boolean.

## Examples

```sql
SELECT ST_ISVALID(TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'));

┌──────────────────────────────────────────────────────────┐
│ st_isvalid(to_geometry('polygon((0 0, 1 0, 1 1, 0 1, 0 0))')) │
├──────────────────────────────────────────────────────────┤
│ true                                                          │
└──────────────────────────────────────────────────────────┘

-- Self-intersecting polygon (bowtie shape) is invalid
SELECT ST_ISVALID(TO_GEOMETRY('POLYGON((0 0, 2 2, 2 0, 0 2, 0 0))'));

┌──────────────────────────────────────────────────────────────┐
│ st_isvalid(to_geometry('polygon((0 0, 2 2, 2 0, 0 2, 0 0))')) │
├──────────────────────────────────────────────────────────────┤
│ false                                                             │
└──────────────────────────────────────────────────────────────┘
```
