---
title: DROP SPATIAL INDEX
summary: "Removes a spatial index in {{{ .lake }}}."
---

# DROP SPATIAL INDEX

Removes a spatial index in {{{ .lake }}}.

## Syntax

```sql
DROP SPATIAL INDEX [IF EXISTS] <index> ON [<database>.]<table>
```

## Examples

```sql
CREATE TABLE stores (
    store_id INT,
    store_name STRING,
    location GEOMETRY,
    SPATIAL INDEX location_idx (location)
) ENGINE = FUSE;

DROP SPATIAL INDEX location_idx ON stores;
```
