---
title: CREATE SNAPSHOT TAG
summary: Creates a named snapshot tag on a FUSE table, allowing you to bookmark and query specific points in the table's history.
---

# CREATE SNAPSHOT TAG

> **Note:**
>
> Introduced or updated in v1.2.891.

Creates a named snapshot tag on a FUSE table. A snapshot tag bookmarks a specific point-in-time state of the table, allowing you to query that state later with the [AT](/tidb-cloud-lake/sql/at.md) clause.

> **Note:**
>
> - This is an **experimental** feature. Enable it first before use: `SET enable_experimental_table_ref = 1;`.
> - Only supported on FUSE engine tables. Memory engine tables and temporary tables are not supported.

## Syntax

```sql
ALTER TABLE [<database_name>.]<table_name> CREATE TAG <tag_name>
    [ AT (
        SNAPSHOT => '<snapshot_id>' |
        TIMESTAMP => <timestamp> |
        STREAM => <stream_name> |
        OFFSET => <time_interval> |
        TAG => <tag_name>
    ) ]
    [ RETAIN <n> { DAYS | SECONDS } ]
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| tag_name  | The name of the tag. Must be unique within the table. |
| AT        | Specifies which snapshot the tag references. If omitted, the tag references the current (latest) snapshot. Supports the same options as the [AT](/tidb-cloud-lake/sql/at.md) clause, plus `TAG` to copy from an existing tag. |
| RETAIN    | Sets an automatic expiration period. After the specified duration, the tag is removed during the next [VACUUM](/tidb-cloud-lake/sql/vacuum-table.md) operation. Without `RETAIN`, the tag persists until explicitly dropped. |

## Examples

### Tag the Current Snapshot

```sql
SET enable_experimental_table_ref = 1;

CREATE TABLE t1(a INT, b STRING);
INSERT INTO t1 VALUES (1, 'a'), (2, 'b'), (3, 'c');

-- Create a tag at the current snapshot
ALTER TABLE t1 CREATE TAG v1_0;

-- Insert more data
INSERT INTO t1 VALUES (4, 'd'), (5, 'e');

-- Query the tagged snapshot (returns 3 rows, not 5)
SELECT * FROM t1 AT (TAG => v1_0) ORDER BY a;
```

### Tag from an Existing Reference

```sql
-- Copy from an existing tag
ALTER TABLE t1 CREATE TAG v1_0_copy AT (TAG => v1_0);

-- Tag a specific snapshot
ALTER TABLE t1 CREATE TAG before_migration
    AT (SNAPSHOT => 'aaa4857c5935401790db2c9f0f2818be');

-- Tag the state from 1 hour ago
ALTER TABLE t1 CREATE TAG hourly_checkpoint AT (OFFSET => -3600);
```

### Tag with Automatic Expiration

```sql
-- Tag expires after 7 days
ALTER TABLE t1 CREATE TAG temp_tag RETAIN 7 DAYS;

-- Tag expires after 3600 seconds
ALTER TABLE t1 CREATE TAG debug_snapshot RETAIN 3600 SECONDS;
```
