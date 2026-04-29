---
title: FUSE_TAG
summary: Returns the snapshot tags of a table. For more information about snapshot tags, see Snapshot Tags.
---

# FUSE_TAG

> **Note:**
>
> Introduced or updated in v1.2.894.

Returns the snapshot tags of a table. For more information about snapshot tags, see [Snapshot Tags](/tidb-cloud-lake/sql/table-versioning.md#snapshot-tags).

## Syntax

```sql
FUSE_TAG('<database_name>', '<table_name>')
```

## Output Columns

| Column              | Type               | Description                                                                 |
|---------------------|--------------------|-----------------------------------------------------------------------------|
| name                | STRING             | Tag name                                                                    |
| snapshot_location   | STRING             | Snapshot file the tag points to                                             |
| expire_at           | TIMESTAMP (nullable) | Expiration timestamp; set when `RETAIN` is used in CREATE SNAPSHOT TAG    |

## Examples

```sql
SET enable_experimental_table_ref = 1;

CREATE TABLE mytable(a INT, b INT);

INSERT INTO mytable VALUES(1, 1),(2, 2);

-- Create a snapshot tag
ALTER TABLE mytable CREATE TAG v1;

INSERT INTO mytable VALUES(3, 3);

-- Create another tag with expiration
ALTER TABLE mytable CREATE TAG temp RETAIN 2 DAYS;

SELECT * FROM FUSE_TAG('default', 'mytable');

---
| name | snapshot_location                                          | expire_at                  |
|------|------------------------------------------------------------|----------------------------|
| v1   | 1/319/_ss/a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4_v4.mpk        | NULL                       |
| temp | 1/319/_ss/f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3_v4.mpk        | 2025-06-15 10:30:00.000000 |
```
