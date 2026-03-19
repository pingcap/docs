---
title: _tidb_rowid
summary: Learn what `_tidb_rowid` is, when it is available, and how to use it safely.
---

# _tidb_rowid

`_tidb_rowid` is a hidden system column that TiDB uses as the row handle for tables that do not use a clustered index. You do not declare this column in the table schema, but you can reference it in SQL when the table uses `_tidb_rowid` as its handle.

In the current implementation, `_tidb_rowid` is an extra `BIGINT NOT NULL` handle column managed by TiDB.

> **Warning:**
>
> - Do not assume `_tidb_rowid` is globally unique in all cases. For partitioned tables that do not use clustered indexes, executing `ALTER TABLE ... EXCHANGE PARTITION` can leave different partitions with the same `_tidb_rowid` value.
> - If you need a stable unique identifier, define and use an explicit primary key instead of relying on `_tidb_rowid`.

## When `_tidb_rowid` is available

`_tidb_rowid` is available for tables whose row handle is not a clustered primary key. In practice, this means the following table types use `_tidb_rowid`:

- Tables without primary keys
- Tables with primary keys that are explicitly defined as `NONCLUSTERED`

`_tidb_rowid` is not available for tables that use a clustered index, including the following:

- Tables with integer primary keys that are clustered row handles
- Tables with clustered indexes on composite primary keys

The following example shows the difference:

```sql
CREATE TABLE t1 (a INT, b VARCHAR(20));
CREATE TABLE t2 (id BIGINT PRIMARY KEY NONCLUSTERED, a INT);
CREATE TABLE t3 (id BIGINT PRIMARY KEY CLUSTERED, a INT);
```

For `t1` and `t2`, you can query `_tidb_rowid`:

```sql
SELECT _tidb_rowid, a, b FROM t1;
SELECT _tidb_rowid, id, a FROM t2;
```

For `t3`, `_tidb_rowid` is unavailable because the clustered primary key is already the row handle:

```sql
SELECT _tidb_rowid, id, a FROM t3;
```

```sql
ERROR 1054 (42S22): Unknown column '_tidb_rowid' in 'field list'
```

## Read `_tidb_rowid`

You can use `_tidb_rowid` in `SELECT` statements for supported tables. This is useful for tasks such as pagination, troubleshooting, and batch processing.

Example:

```sql
CREATE TABLE t (a INT, b VARCHAR(20));
INSERT INTO t VALUES (1, 'x'), (2, 'y');

SELECT _tidb_rowid, a, b FROM t ORDER BY _tidb_rowid;
```

```sql
+-------------+---+---+
| _tidb_rowid | a | b |
+-------------+---+---+
|           1 | 1 | x |
|           2 | 2 | y |
+-------------+---+---+
```

To inspect the next value that TiDB will allocate for the row ID, use `SHOW TABLE ... NEXT_ROW_ID`:

```sql
SHOW TABLE t NEXT_ROW_ID;
```

```sql
+-----------------------+------------+-------------+--------------------+-------------+
| DB_NAME               | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID | ID_TYPE     |
+-----------------------+------------+-------------+--------------------+-------------+
| update_doc_rowid_test | t          | _tidb_rowid |              30001 | _TIDB_ROWID |
+-----------------------+------------+-------------+--------------------+-------------+
```

## Write `_tidb_rowid`

By default, TiDB does not allow `INSERT`, `REPLACE`, or `UPDATE` statements to write `_tidb_rowid` directly.

```sql
INSERT INTO t(_tidb_rowid, a, b) VALUES (101, 4, 'w');
```

```sql
ERROR 1105 (HY000): insert, update and replace statements for _tidb_rowid are not supported
```

If you need to preserve row IDs during data import or migration, enable the system variable [`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id) first:

```sql
SET @@tidb_opt_write_row_id = ON;
INSERT INTO t(_tidb_rowid, a, b) VALUES (100, 3, 'z');
SET @@tidb_opt_write_row_id = OFF;

SELECT _tidb_rowid, a, b FROM t WHERE _tidb_rowid = 100;
```

```sql
+-------------+---+---+
| _tidb_rowid | a | b |
+-------------+---+---+
|         100 | 3 | z |
+-------------+---+---+
```

> **Warning:**
>
> `tidb_opt_write_row_id` is intended for import and migration scenarios. It is not recommended for regular application writes.

## Restrictions

- You cannot create a user column named `_tidb_rowid`.
- You cannot rename an existing user column to `_tidb_rowid`.
- `_tidb_rowid` is an internal row handle. Do not treat it as a long-term business key.
- On partitioned non-clustered tables, `_tidb_rowid` values are not guaranteed to be unique across partitions. After you execute `EXCHANGE PARTITION`, different partitions can contain rows with the same `_tidb_rowid` value.
- Whether `_tidb_rowid` exists depends on the table layout. If a table uses a clustered index, use the primary key instead.

## Hotspot considerations

For tables that use `_tidb_rowid`, TiDB allocates row IDs in increasing order by default. In write-intensive workloads, this can create write hotspots.

To mitigate this issue for tables that rely on implicit row IDs, consider using [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) and, if needed, [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions).

Example:

```sql
CREATE TABLE t (
    id BIGINT PRIMARY KEY NONCLUSTERED,
    c INT
) SHARD_ROW_ID_BITS = 4;
```

`SHARD_ROW_ID_BITS` applies only to tables that use the implicit row ID path. It does not apply to clustered-index tables.

## Related statements and variables

- [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md): shows the next row ID that TiDB will allocate
- [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md): shards implicit row IDs to reduce hotspots
- [`Clustered Indexes`](/clustered-indexes.md): explains when a table uses the primary key instead of `_tidb_rowid`
- [`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id): controls whether writes to `_tidb_rowid` are allowed

## See also

- [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
- [`AUTO_INCREMENT`](/auto-increment.md)
- [Non-transactional DML](/non-transactional-dml.md)
