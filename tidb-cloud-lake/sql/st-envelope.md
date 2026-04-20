---
title: ST_ENVELOPE
summary: Returns the minimum bounding rectangle of a GEOMETRY object as a polygon.
---

# ST_ENVELOPE

> **Note:**
>
> Introduced or updated in v1.2.895.

Returns the minimum bounding rectangle of a GEOMETRY object as a polygon.

This function only supports GEOMETRY values.

## Syntax

```sql
ST_ENVELOPE(<geometry>)
```

## Arguments

| Arguments    | Description                                            |
|--------------|--------------------------------------------------------|
| `<geometry>` | The argument must be an expression of type GEOMETRY. |

## Return Type

GEOMETRY.

## Examples

```sql
SELECT ST_ASWKT(ST_ENVELOPE(TO_GEOMETRY('LINESTRING(0 0, 2 3)')));

╭────────────────────────────────────────────────────────────╮
│ st_aswkt(st_envelope(to_geometry('LINESTRING(0 0, 2 3)'))) │
│                           String                           │
├────────────────────────────────────────────────────────────┤
│ POLYGON((0 0,2 0,2 3,0 3,0 0))                             │
╰────────────────────────────────────────────────────────────╯
```
