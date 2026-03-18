---
title: FUSE_COLUMN
summary: Returns the column information of the latest or specified snapshot of a table. For more information about what is block in Databend, see What are Snapshot, Segment, and Block?.
---
Returns the column information of the latest or specified snapshot of a table. For more information about what is block in Databend, see [What are Snapshot, Segment, and Block?](/tidb-cloud-lake/sql/optimize-table.md#databend-data-storage-snapshot-segment-and-block).


See Also:

- [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md)
- [FUSE_SEGMENT](/tidb-cloud-lake/sql/fuse-segment.md)
- [FUSE_BLOCK](/tidb-cloud-lake/sql/fuse-block.md)

## Syntax

```sql
FUSE_COLUMN('<database_name>', '<table_name>'[, '<snapshot_id>'])
```

## Examples

```sql
CREATE TABLE mytable(c int);
INSERT INTO mytable values(1);
INSERT INTO mytable values(2);

SELECT * FROM FUSE_COLUMN('default', 'mytable');

---
+----------------------------------+----------------------------+---------------------------------------------------------+------------+-----------+-----------+-------------+-------------+-----------+--------------+------------------+
| snapshot_id                      | timestamp                  | block_location                                          | block_size | file_size | row_count | column_name | column_type | column_id | block_offset | bytes_compressed |
+----------------------------------+----------------------------+---------------------------------------------------------+------------+-----------+-----------+-------------+-------------+-----------+--------------+------------------+
| 3faefc1a9b6a48f388a8b59228dd06c1 | 2023-07-18 03:06:30.276502 | 1/118746/_b/44df130c207745cb858928135d39c1c0_v2.parquet |          4 |       196 |         1 | c           | Int32       |         0 |            8 |               14 |
| 3faefc1a9b6a48f388a8b59228dd06c1 | 2023-07-18 03:06:30.276502 | 1/118746/_b/b6f8496d7e3f4f62a89c09572840cf70_v2.parquet |          4 |       196 |         1 | c           | Int32       |         0 |            8 |               14 |
+----------------------------------+----------------------------+---------------------------------------------------------+------------+-----------+-----------+-------------+-------------+-----------+--------------+------------------+
```