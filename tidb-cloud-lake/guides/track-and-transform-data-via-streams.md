---
title: Tracking and Transforming Data via Streams
sidebar_label: Stream
---

import StepsWrap from '@site/src/components/StepsWrap';
import StepContent from '@site/src/components/Steps/step-content';

A stream in Databend is an always-on change table: every committed INSERT, UPDATE, or DELETE is captured until you consume it. This page stays lean—first a quick overview, then one lab with real outputs so you can see streams in action.

## Stream Overview

- Streams don’t duplicate table storage; they list the latest change for each affected row until you consume it.
- Consumption (task, INSERT ... SELECT, `WITH CONSUME`, etc.) clears the stream while keeping it ready for new data.
- `APPEND_ONLY` defaults to `true`; set `APPEND_ONLY = false` only when you must capture UPDATE/DELETE events.

| Mode | Captures | Typical use |
| --- | --- | --- |
| Standard (`APPEND_ONLY = false`) | INSERT + UPDATE + DELETE, collapsed to the latest state per row. | Slowly changing dimensions, compliance audits. |
| Append-Only (`APPEND_ONLY = true`, default) | INSERT only. | Append-only fact/event ingestion. |

## Example 1: Append-Only Stream

Run the statements below in any Databend deployment (Cloud worksheet or local) to see how the default append-only mode captures and consumes inserts.

### 1. Create table and stream

```sql
CREATE OR REPLACE TABLE sensor_readings (
    sensor_id INT,
    temperature DOUBLE
);

-- APPEND_ONLY defaults to true, so no extra clause is required.
CREATE OR REPLACE STREAM sensor_readings_stream
    ON TABLE sensor_readings;
```

### 2. Insert rows and preview

```sql
INSERT INTO sensor_readings VALUES (1, 21.5), (2, 19.7);

SELECT sensor_id, temperature, change$action, change$is_update
FROM sensor_readings_stream;
```

Output:

```
┌────────────┬───────────────┬───────────────┬──────────────────┐
│ sensor_id  │ temperature   │ change$action │ change$is_update │
├────────────┼───────────────┼───────────────┼──────────────────┤
│          1 │ 21.5          │ INSERT        │ false            │
│          2 │ 19.7          │ INSERT        │ false            │
└────────────┴───────────────┴───────────────┴──────────────────┘
```

### 3. Consume (optional)

```sql
SELECT sensor_id, temperature
FROM sensor_readings_stream WITH CONSUME;

SELECT * FROM sensor_readings_stream; -- now empty
```

`WITH CONSUME` reads the stream once and clears the delta so the next round can capture fresh INSERTs.

## Example 2: Standard Stream (Updates & Deletes)

Switch to Standard mode when you must react to every mutation, including UPDATE or DELETE.

### 1. Create a Standard stream

```sql
CREATE OR REPLACE STREAM sensor_readings_stream_std
    ON TABLE sensor_readings
    APPEND_ONLY = false;
```

### 2. Mutate rows and compare

```sql
DELETE FROM sensor_readings WHERE sensor_id = 1;     -- remove old reading
INSERT INTO sensor_readings VALUES (1, 22);         -- same sensor, new value
DELETE FROM sensor_readings WHERE sensor_id = 2;     -- pure deletion
INSERT INTO sensor_readings VALUES (3, 18.5);        -- brand-new sensor

SELECT * FROM sensor_readings_stream; -- still empty (Append-Only ignores non-inserts)

SELECT sensor_id, temperature, change$action, change$is_update
FROM sensor_readings_stream_std
ORDER BY change$row_id;
```

Output:

```
┌────────────┬───────────────┬───────────────┬──────────────────┐
│ sensor_id  │ temperature   │ change$action │ change$is_update │
├────────────┼───────────────┼───────────────┼──────────────────┤
│          1 │ 21.5          │ DELETE        │ true             │
│          1 │ 22            │ INSERT        │ true             │
│          2 │ 19.7          │ DELETE        │ false            │
│          3 │ 18.5          │ INSERT        │ false            │
└────────────┴───────────────┴───────────────┴──────────────────┘
```

 Standard streams capture each change with context: updates show up as DELETE+INSERT on the same `sensor_id`, while standalone deletions/insertions appear individually. Append-Only streams stay empty because they track inserts only.

## Example 3: Incremental Stream Join

Join multiple append-only streams to produce incremental KPIs. Because Databend streams keep new rows until they are consumed, you can run the same query after each load. Every execution drains only the new rows via [`WITH CONSUME`](/sql/sql-commands/query-syntax/with-consume), so updates that arrive at different times are still matched on the next iteration.

### 1. Create tables and streams

```sql
CREATE OR REPLACE TABLE customers (
    customer_id INT,
    segment VARCHAR,
    city VARCHAR
);

CREATE OR REPLACE TABLE orders (
    order_id INT,
    customer_id INT,
    amount DOUBLE
);

CREATE OR REPLACE STREAM customers_stream ON TABLE customers;
CREATE OR REPLACE STREAM orders_stream ON TABLE orders;
```

### 2. Load the first batch

```sql
INSERT INTO customers VALUES
    (101, 'VIP', 'Seattle'),
    (102, 'Standard', 'Austin'),
    (103, 'VIP', 'Austin');

INSERT INTO orders VALUES
    (5001, 101, 199.0),
    (5002, 101, 59.0),
    (5003, 102, 89.0);
```

### 3. Run the first incremental query

```sql
WITH
    orders_delta AS (
        SELECT customer_id, amount
        FROM orders_stream WITH CONSUME
    ),
    customers_delta AS (
        SELECT customer_id, segment
        FROM customers_stream WITH CONSUME
    )
SELECT
    o.customer_id,
    c.segment,
    SUM(o.amount) AS incremental_sales
FROM orders_delta AS o
JOIN customers_delta AS c
    ON o.customer_id = c.customer_id
GROUP BY o.customer_id, c.segment
ORDER BY o.customer_id;
```

```
┌──────────────┬───────────┬────────────────────┐
│ customer_id  │ segment   │ incremental_sales  │
├──────────────┼───────────┼────────────────────┤
│          101 │ VIP       │ 258.0              │
│          102 │ Standard  │  89.0              │
└──────────────┴───────────┴────────────────────┘
```

The streams are now empty. When more rows arrive, the same query will capture only the new data.

### 4. Run again after the next batch

```sql
-- New data arrives later
INSERT INTO customers VALUES (104, 'Standard', 'Denver');
INSERT INTO orders VALUES
    (5004, 101, 40.0),
    (5005, 104, 120.0);

-- Same incremental query as before
WITH
    orders_delta AS (
        SELECT customer_id, amount
        FROM orders_stream WITH CONSUME
    ),
    customers_delta AS (
        SELECT customer_id, segment
        FROM customers_stream WITH CONSUME
    )
SELECT
    o.customer_id,
    c.segment,
    SUM(o.amount) AS incremental_sales
FROM orders_delta AS o
JOIN customers_delta AS c
    ON o.customer_id = c.customer_id
GROUP BY o.customer_id, c.segment
ORDER BY o.customer_id;
```

```
┌──────────────┬───────────┬────────────────────┐
│ customer_id  │ segment   │ incremental_sales  │
├──────────────┼───────────┼────────────────────┤
│          101 │ VIP       │ 40.0               │
│          104 │ Standard  │ 120.0              │
└──────────────┴───────────┴────────────────────┘
```

Rows stay in each stream until `WITH CONSUME` runs, so inserts that arrive at different times are still matched on the next run. Leave the streams unconsumed when you expect more related rows, then rerun the query to pick up the incremental delta.

## Stream Workflow Notes

**Consumption**
- Streams are drained inside a transaction: `INSERT INTO target SELECT ... FROM stream` empties the stream only when the statement commits.
- Only one consumer can succeed at a time; other concurrent statements roll back.

**Modes**
- Append-Only streams capture INSERTs only and are ideal for append-heavy workloads.
- Standard streams emit updates and deletes as long as you consume them; late-arriving updates remain until the next run.

**Hidden Columns**
- Streams expose `change$action`, `change$is_update`, and `change$row_id`; use them to understand how Databend recorded each row.
- Base tables gain `_origin_version`, `_origin_block_id`, `_origin_block_row_num` for debugging row provenance.

**Integrations**
- Pair streams with tasks using `task_history('<name>', <limit>)` for scheduled incremental loads.
- Use [`WITH CONSUME`](02-task.md) when you want to drain only the latest delta.

