---
title: DROP SNAPSHOT TAG
summary: Drops a named snapshot tag from a FUSE table, allowing the referenced snapshot to be garbage collected if no other tags or retention policies protect it.
---

# DROP SNAPSHOT TAG

> **Note:**
>
> Introduced or updated in v1.2.891.

Drops a named snapshot tag from a FUSE table. Once dropped, the referenced snapshot becomes eligible for garbage collection if no other tags or retention policies protect it.

> **Note:**
>
> - This is an **experimental** feature. Enable it first before use: `SET enable_experimental_table_ref = 1;`.
> - Only supported on FUSE engine tables.

## Syntax

```sql
ALTER TABLE [<database_name>.]<table_name> DROP TAG <tag_name>
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| tag_name  | The name of the snapshot tag to drop. An error is returned if the tag does not exist. |

## Examples

```sql
SET enable_experimental_table_ref = 1;

CREATE TABLE t1(a INT, b STRING);
INSERT INTO t1 VALUES (1, 'a'), (2, 'b');

-- Create and then drop a tag
ALTER TABLE t1 CREATE TAG v1_0;
ALTER TABLE t1 DROP TAG v1_0;

-- Querying a dropped tag returns an error
SELECT * FROM t1 AT (TAG => v1_0);
-- Error: tag 'v1_0' not found
```
