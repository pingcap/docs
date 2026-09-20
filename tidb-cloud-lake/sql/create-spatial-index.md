---
title: CREATE SPATIAL INDEX
summary: "Creates a new spatial index in {{{ .lake }}}."
---

# CREATE SPATIAL INDEX

Creates a new spatial index in {{{ .lake }}}.

## Syntax

```sql
CREATE [ OR REPLACE ] SPATIAL INDEX [IF NOT EXISTS] <index>
    ON [<database>.]<table>( <geometry_column>[, <geometry_column> ...] )
```

| Parameter | Description |
|-----------|-------------|
| `[ OR REPLACE ]` | Replaces the existing index if it already exists. |
| `[ IF NOT EXISTS ]` | Creates the index only if an index with the same name does not already exist. |
| `<index>` | The name of the spatial index. |
| `[<database>.]<table>` | The table that owns the indexed columns. |
| `<geometry_column>` | A `GEOMETRY` column included in the index. Each listed column must be unique within the statement. |

## Usage Notes

- Spatial indexes are supported on Fuse tables only.
- Spatial indexes support `GEOMETRY` columns only. `GEOGRAPHY` columns are not supported.
- Multiple columns can be indexed in a single spatial index definition as long as all of them are `GEOMETRY` columns.
- For better pruning, it is recommended to physically cluster geospatial data with `CLUSTER BY` and `ST_HILBERT`, so nearby objects are more likely to be written into the same block.

## Examples

Create a table with a spatial column:

```sql
CREATE TABLE stores (
    store_id INT,
    store_name STRING,
    location GEOMETRY
) CLUSTER BY (
    ST_HILBERT(location, [-180, -90, 180, 90])
);
```

Create a spatial index on the `location` column:

```sql
CREATE SPATIAL INDEX stores_location_idx ON stores(location);
```

Inspect the table definition:

```sql
SHOW CREATE TABLE stores;

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ Table  │ Create Table                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ stores │ CREATE TABLE stores (                                                             │
│        │   store_id INT NULL,                                                              │
│        │   store_name VARCHAR NULL,                                                        │
│        │   location GEOMETRY NULL,                                                         │
│        │   SYNC SPATIAL INDEX stores_location_idx (location)                               │
│        │ ) ENGINE=FUSE CLUSTER BY linear(st_hilbert(location, [-180, -90, 180, 90]))       │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

Load a slightly richer dataset for spatial filtering, and run RECLUSTER command:

```sql
INSERT INTO stores VALUES
  (1, 'Starbucks', TO_GEOMETRY('POINT(10 10)')),
  (2, 'Costa', TO_GEOMETRY('POINT(11 11)')),
  (3, 'Gong Cha', TO_GEOMETRY('POINT(20 20)')),
  (4, 'Dunkin', TO_GEOMETRY('POINT(-10 -10)'));

ALTER TABLE stores RECLUSTER FINAL;
```

### Filter with `ST_WITHIN`, `ST_INTERSECTS`, and `ST_CONTAINS`

These predicates are common geofence-style filters and can benefit from the spatial index.

```sql
-- Rows whose locations are within a polygon
SELECT store_id, store_name
FROM stores
WHERE ST_WITHIN(
    location,
    TO_GEOMETRY('POLYGON((9 9, 9 12, 12 12, 12 9, 9 9))')
)
ORDER BY store_id;
```

```sql
-- Rows whose locations intersect a polygon
SELECT store_id, store_name
FROM stores
WHERE ST_INTERSECTS(
    location,
    TO_GEOMETRY('POLYGON((9 9, 9 12, 12 12, 12 9, 9 9))')
)
ORDER BY store_id;
```

```sql
-- Polygons that contain a point
SELECT store_id, store_name
FROM stores
WHERE ST_CONTAINS(
    TO_GEOMETRY('POLYGON((9 9, 9 12, 12 12, 12 9, 9 9))'),
    location
)
ORDER BY store_id;
```

### Filter with `ST_DWITHIN`

Use `ST_DWITHIN` for radius-style lookups. This is useful for "find nearby locations" queries.

```sql
SELECT store_id, store_name
FROM stores
WHERE ST_DWITHIN(
    location,
    TO_GEOMETRY('POINT(10 10)'),
    1.5
)
ORDER BY store_id;
```

### Filter with spatial joins

Spatial indexes are also useful in joins where the join condition is a supported spatial predicate.

```sql
CREATE TABLE districts (
    district_id INT,
    district_name STRING,
    geom GEOMETRY
) CLUSTER BY (
    ST_HILBERT(geom, [-180, -90, 180, 90])
);

INSERT INTO districts VALUES
  (1, 'Central', TO_GEOMETRY('POLYGON((8 8, 8 13, 13 13, 13 8, 8 8))')),
  (2, 'West', TO_GEOMETRY('POLYGON((-2 -2, -2 2, 2 2, 2 -2, -2 -2))'));
```

```sql
SELECT d.district_name, s.store_name
FROM districts AS d
JOIN stores AS s
  ON ST_WITHIN(s.location, d.geom)
ORDER BY d.district_name, s.store_name;
```
