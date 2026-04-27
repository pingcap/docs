---
title: REFRESH SPATIAL INDEX
summary: Refreshes a spatial index to backfill historical rows or update the index after data changes.
---

# REFRESH SPATIAL INDEX

{{{ .lake }}} automatically refreshes spatial indexes in `SYNC` mode whenever new data is written. Use `REFRESH SPATIAL INDEX` primarily to backfill rows that existed before the index was declared.

## Syntax

```sql
REFRESH SPATIAL INDEX <index> ON [<database>.]<table> [LIMIT <limit>]
```

| Parameter | Description |
|-----------|-------------|
| `<limit>` | Specifies the maximum number of rows to process during index refresh. If not specified, all rows in the table will be processed. |

## Examples

```sql
-- Existing table with data loaded before the index was declared
CREATE TABLE IF NOT EXISTS stores (
  store_id INT,
  location GEOMETRY
) ENGINE = FUSE;

INSERT INTO stores VALUES
  (1, TO_GEOMETRY('POINT(10 10)')),
  (2, TO_GEOMETRY('POINT(20 20)'));

-- Create the spatial index afterward
CREATE SPATIAL INDEX stores_location_idx ON stores(location);

-- Backfill historical rows so the index covers earlier inserts
REFRESH SPATIAL INDEX stores_location_idx ON stores;

-- Future inserts refresh automatically in SYNC mode
```
