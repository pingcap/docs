---
title: _tidb_commit_ts
summary: Learn how to read the hidden _tidb_commit_ts column, use it in queries, and understand its read-only and plan-related limitations.
---

# `_tidb_commit_ts`

`_tidb_commit_ts` is a hidden system column that exposes the commit timestamp of a row in the local TiDB cluster. TiDB obtains this timestamp from the transaction's MVCC commit record and returns it as an unsigned `BIGINT` value. You cannot see this column with `SELECT *`, but you can reference it explicitly by name.

The value is useful when you need to compare row versions, inspect the order in which rows were committed, or remove rows based on a commit timestamp. A committed row normally has a positive timestamp. The value can be `NULL` for a row version that has not been committed yet inside TiDB.

## Read `_tidb_commit_ts`

You can select `_tidb_commit_ts` from a regular TiDB table without enabling a session feature:

```sql
CREATE TABLE t (
    id INT PRIMARY KEY,
    value VARCHAR(20)
);

INSERT INTO t VALUES (1, 'a'), (2, 'b');

SELECT id, _tidb_commit_ts > 0 AS has_commit_ts
FROM t
ORDER BY id;
```

```sql
+----+----------------+
| id | has_commit_ts  |
+----+----------------+
|  1 |              1 |
|  2 |              1 |
+----+----------------+
```

You can use the column in expressions and predicates, including joins and set operations:

```sql
SELECT id
FROM t
WHERE _tidb_commit_ts > 0
ORDER BY id;

SELECT _tidb_commit_ts > 0 AS has_commit_ts FROM t
UNION ALL
SELECT _tidb_commit_ts > 0 FROM t;
```

Reading `_tidb_commit_ts` does not depend on the value of `tidb_mview_enable`.

## Use `_tidb_commit_ts` with table and index scans

When a query reads `_tidb_commit_ts`, TiDB uses a coprocessor scan that can return the commit timestamp together with the row. For example, a primary-key lookup is planned as a table range scan:

```sql
EXPLAIN FORMAT = 'plan_tree'
SELECT _tidb_commit_ts FROM t WHERE id = 1;
```

The plan contains `TableRangeScan` under `TableReader`. For a secondary-index predicate, TiDB can use an index lookup:

```sql
ALTER TABLE t ADD INDEX idx_value (value);

EXPLAIN FORMAT = 'plan_tree'
SELECT _tidb_commit_ts
FROM t USE INDEX (idx_value)
WHERE value = 'a';
```

The plan contains `IndexLookUp`, and the query returns the commit timestamp for the matching row. TiDB does not convert these queries to `Point_Get`, `Batch_Point_Get`, or a single `IndexReader` plan because those operators cannot provide `_tidb_commit_ts`.

## Use `_tidb_commit_ts` in DML expressions

You can read the column while filtering or computing values in `UPDATE`, `INSERT ... SELECT`, and `DELETE` statements. Reading the column does not modify it:

```sql
UPDATE t
SET value = CONCAT(value, '-updated')
WHERE _tidb_commit_ts > 0;

CREATE TABLE t_copy (id INT, commit_ts BIGINT UNSIGNED);

INSERT INTO t_copy
SELECT id, _tidb_commit_ts
FROM t
WHERE _tidb_commit_ts > 0;

DELETE FROM t
WHERE _tidb_commit_ts = 0;
```

The last statement does not delete rows when no row has a zero commit timestamp. You can use a range predicate, such as `_tidb_commit_ts > 0`, to delete rows whose commit timestamps meet your retention condition.

## Restrictions

- `_tidb_commit_ts` is read-only. You cannot assign a value to it in `INSERT`, `REPLACE`, `UPDATE`, or `INSERT ... ON DUPLICATE KEY UPDATE` statements. An attempted write returns an error similar to `Usage of column name '_tidb_commit_ts' is not supported for now`.
- Do not define a user column with the name `_tidb_commit_ts`. The name is reserved for the hidden system column.
- Queries that read `_tidb_commit_ts` cannot use index merge. If you force an index-merge plan, TiDB returns an error because it cannot find a proper physical plan.
- `_tidb_commit_ts` is not supported when reading a table through the table cache. A query that combines the column with a cached table returns an error similar to `'_tidb_commit_ts' is unsupported on cache tables.`
- The timestamp is an MVCC commit timestamp, not a wall-clock time. To interpret it as a time, use the timestamp utilities appropriate for your TiDB deployment instead of treating the numeric value as Unix time.

## See also

- [Optimistic transactions](/optimistic-transaction.md)
- [Pessimistic transactions](/pessimistic-transaction.md)
- [TiCDC protocols](/ticdc/ticdc-avro-protocol.md)
