---
title: Spatial Index
summary: Spatial indexes accelerate spatial predicate filtering on `GEOMETRY` columns.
---

# Spatial Index

Spatial indexes in {{{ .lake }}} accelerate spatial predicate filtering on `GEOMETRY` columns. They are designed for Fuse tables and help the optimizer prune blocks before evaluating exact spatial functions.

> **Tip:**
>
> Spatial indexes are maintained automatically for data written after the index is created. Use `REFRESH SPATIAL INDEX` when you create an index on a table that already contains data and need to backfill existing rows.

## Spatial Index Management

| Command | Description |
|---------|-------------|
| [CREATE SPATIAL INDEX](/tidb-cloud-lake/sql/create-spatial-index.md) | Creates a new spatial index on one or more `GEOMETRY` columns |
| [REFRESH SPATIAL INDEX](/tidb-cloud-lake/sql/refresh-spatial-index.md) | Backfills spatial index data for rows that existed before index creation |
| [DROP SPATIAL INDEX](/tidb-cloud-lake/sql/drop-spatial-index.md) | Removes a spatial index from a table |

## Supported Predicates

{{{ .lake }}} can use spatial indexes to accelerate queries built with these spatial predicates:

- `ST_CONTAINS`
- `ST_INTERSECTS`
- `ST_WITHIN`
- `ST_DWITHIN`

## Limitations

- Spatial indexes are supported on Fuse tables.
- Indexed columns must be of type `GEOMETRY`.
- `GEOGRAPHY` columns are not supported.

## Related Topics

- [Geospatial Functions](/tidb-cloud-lake/sql/geospatial-functions.md)
