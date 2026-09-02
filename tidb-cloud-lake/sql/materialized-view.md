---
title: Materialized View
summary: A materialized view stores the result of a query physically. TiDB Cloud Lake enables change tracking on the source table when the materialized view is created.
---

# Materialized View

A materialized view stores the result of a query physically. It is defined on one persistent FUSE table in the `default` catalog. {{{ .lake }}} enables change tracking on the source table when the materialized view is created.

Unlike a logical view, a materialized view can be explicitly refreshed to persist the changes from its source table. Reads are consistent even when physical storage lags behind the source table. Before the first refresh, {{{ .lake }}} evaluates the definition against the source. When there are unrefreshed source changes, {{{ .lake }}} uses **read fix**: it unions the persisted materialized-view data with the required incremental source data at read time (and applies the view definition to that increment). The query therefore returns current results rather than stale materialized data.

## Limitations

- A definition must be a simple `SELECT ... FROM ... [WHERE ...] [GROUP BY ...]` query over exactly one base table. Joins, subqueries, set operations, and non-deterministic functions are not supported.
- Aggregations are supported only for `sum`, `min`, `max`, `avg`, `count`, and `approx_count_distinct`. `DISTINCT`, `FILTER`, window, and ordered aggregate forms are not supported.
- The source must be a persistent FUSE base table in the `default` catalog. A materialized view cannot use another view or a different table engine as its source.
- Materialized views are read-only. Use `REFRESH MATERIALIZED VIEW` to maintain their contents; `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, and ordinary `ALTER TABLE` operations are not supported.

## Create a materialized view

```sql
CREATE [ OR REPLACE ] MATERIALIZED VIEW [ IF NOT EXISTS ]
  [ <catalog_name>. ][ <database_name>. ]<view_name>
  [ ( <column_name>, ... ) ]
  [ CLUSTER BY ( <expr>, ... ) ]
  [ COMMENT = '<comment>' ]
  [ <fuse_table_option> = <value> ... ]
AS <query>
```

`CLUSTER BY` requires an explicit column list and can reference non-aggregate output columns or `GROUP BY` keys. The optional Fuse table options control the physical storage layout; see [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) for supported options.

Creation records the definition but does not synchronously populate physical storage. Run `REFRESH MATERIALIZED VIEW` to materialize the initial data.

```sql
CREATE TABLE orders (
  order_id INT,
  customer_id INT,
  amount DECIMAL(10, 2),
  paid BOOLEAN
);

CREATE MATERIALIZED VIEW paid_orders_by_customer
  (customer_id, total_amount, order_count)
  CLUSTER BY (customer_id)
  COMMENT = 'Paid-order totals by customer'
AS
SELECT customer_id, sum(amount), count(*)
FROM orders
WHERE paid
GROUP BY customer_id;

REFRESH MATERIALIZED VIEW paid_orders_by_customer;
```

`CREATE OR REPLACE` replaces an existing materialized view. `IF NOT EXISTS` is a no-op if the name already exists.

## Refresh a materialized view

```sql
REFRESH MATERIALIZED VIEW [ <catalog_name>. ][ <database_name>. ]<view_name>
```

The first refresh materializes the source data. Later refreshes process append-only changes incrementally. If the source has `UPDATE`, `DELETE`, or `TRUNCATE` changes, {{{ .lake }}} rebuilds the materialized view from the current source state so that the result remains correct.

## Change physical layout

Use dedicated `ALTER MATERIALIZED VIEW` syntax for supported maintenance operations:

```sql
ALTER MATERIALIZED VIEW <view_name> CLUSTER BY ( <expr>, ... );
ALTER MATERIALIZED VIEW <view_name> DROP CLUSTER KEY;
ALTER MATERIALIZED VIEW <view_name> RECLUSTER [ FINAL ] [ LIMIT <n> ];
ALTER MATERIALIZED VIEW <view_name> SET OPTIONS ( <option> = <value>, ... );
ALTER MATERIALIZED VIEW <view_name> UNSET OPTIONS ( <option>, ... );
ALTER MATERIALIZED VIEW <view_name> COMMENT = '<comment>';
```

For example, set a layout option before a refresh:

```sql
ALTER MATERIALIZED VIEW paid_orders_by_customer SET OPTIONS (row_per_block = 2);
REFRESH MATERIALIZED VIEW paid_orders_by_customer;
```

`RECLUSTER WHERE` is not supported for materialized views. To change the definition, use `CREATE OR REPLACE MATERIALIZED VIEW`; `ALTER VIEW` does not apply.

## View and remove definitions

```sql
SHOW MATERIALIZED VIEWS
  [ { FROM | IN } <database_name> ]
  [ LIKE '<pattern>' | WHERE <expr> ];

SHOW CREATE MATERIALIZED VIEW
  [ <catalog_name>. ][ <database_name>. ]<view_name>;

DROP MATERIALIZED VIEW [ IF EXISTS ]
  [ <catalog_name>. ][ <database_name>. ]<view_name>;
```

```sql
SHOW MATERIALIZED VIEWS LIKE 'paid_orders%';
SHOW CREATE MATERIALIZED VIEW paid_orders_by_customer;
DROP MATERIALIZED VIEW IF EXISTS paid_orders_by_customer;
```

## Access control requirements

To query, refresh, alter, show, or drop a materialized view, the user needs `SELECT` on its source table (or ownership that provides the equivalent access). Permissions are checked against the current source table identity, so source-table renames do not change this requirement.
