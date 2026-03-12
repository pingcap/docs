---
title: CREATE STREAM
sidebar_position: 1
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.391"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='STREAM'/>

Creates a stream.

## Syntax

```sql
CREATE [ OR REPLACE ] STREAM [ IF NOT EXISTS ] [ <database_name>. ]<stream_name> 
  ON TABLE [ <database_name>. ]<table_name> 
  [ AT ( { TIMESTAMP => <timestamp> | SNAPSHOT => '<snapshot_id>' | STREAM => <existing_stream_name> } ) ]
  [ APPEND_ONLY = true | false ]
  [ COMMENT = '<comment>' ]
```

| Parameter           | Description                                                                                                                                                                                                                                                                                                                    |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `< database_name >` | A stream is treated as an object belonging to a specific database, similar to a table or a view. CREATE STREAM allows for different databases between the stream and the associated table. If a database is not explicitly specified, the current database is applied as the database for the stream you create.               |
| AT                  | When using `AT` followed by `TIMESTAMP =>`or `SNAPSHOT =>` , you can create a stream containing data changes after a specific historical point by the timestamp or snapshot ID; When `AT` is followed by `STREAM =>` , it allows for the creation of a new stream identical to an existing one, preserving the same captured data changes. |
| APPEND_ONLY         | When set to `true`, the stream operates in `Append-Only` mode; when set to `false`, it operates in `Standard` mode. Defaults to `true`. For additional details on stream operation modes, see [How Stream Works](/guides/load-data/continuous-data-pipelines/stream#how-stream-works).                                        |

## Examples

This example demonstrates creating a stream named 'order_changes' to monitor changes within the 'orders' table:

```sql
-- Create a table named 'orders'
CREATE TABLE orders (
    order_id INT,
    product_name VARCHAR,
    quantity INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a stream named 'order_changes' for the table 'orders'
CREATE STREAM order_changes ON TABLE orders;

-- Insert order 1001 to the table 'orders'
INSERT INTO orders (order_id, product_name, quantity) VALUES (1001, 'Product A', 10);

-- Insert order 1002 to the table 'orders'
INSERT INTO orders (order_id, product_name, quantity) VALUES (1002, 'Product B', 20);

-- Retrieve all records from the 'order_changes' stream
SELECT * FROM order_changes;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     order_id    │   product_name   │     quantity    │         order_date         │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼──────────────────┼─────────────────┼────────────────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│            1002 │ Product B        │              20 │ 2024-03-28 03:24:16.629135 │ INSERT        │ false            │ acb58bd6bb4243a4bf0832bf570b38c2000000 │
│            1001 │ Product A        │              10 │ 2024-03-28 03:24:16.539178 │ INSERT        │ false            │ b93a15e694db4134ab5a23afa8c92b20000000 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The following example creates a new stream named 'order_changes_copy' with the `AT` parameter, containing the same data changes as 'order_changes':

```sql
-- Create a stream 'order_changes_copy' on the 'orders' table, copying data changes from 'order_changes'
CREATE STREAM order_changes_copy ON TABLE orders AT (STREAM => order_changes);

-- Retrieve all records from the 'order_changes_copy' stream
SELECT * FROM order_changes_copy;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     order_id    │   product_name   │     quantity    │         order_date         │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼──────────────────┼─────────────────┼────────────────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│            1002 │ Product B        │              20 │ 2024-03-28 03:24:16.629135 │ INSERT        │ false            │ acb58bd6bb4243a4bf0832bf570b38c2000000 │
│            1001 │ Product A        │              10 │ 2024-03-28 03:24:16.539178 │ INSERT        │ false            │ b93a15e694db4134ab5a23afa8c92b20000000 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example creates two streams on the 'orders' table. Each stream utilizes the `AT` parameter to obtain data changes after a specific snapshot ID or timestamp, respectively.

```sql
-- Retrieve snapshot and timestamp information from the 'orders' table
SELECT snapshot_id, timestamp from FUSE_SNAPSHOT('default','orders');

┌───────────────────────────────────────────────────────────────┐
│            snapshot_id           │          timestamp         │
├──────────────────────────────────┼────────────────────────────┤
│ f7f57c7d07f445a68e4aa53fa2578bbb │ 2024-03-28 03:24:16.633721 │
│ 11b9d81eabc94c7da648908f0ba313a1 │ 2024-03-28 03:24:16.611835 │
└───────────────────────────────────────────────────────────────┘

-- Create a stream 'order_changes_after_snapshot' on the 'orders' table, capturing data changes after a specific snapshot
CREATE STREAM order_changes_after_snapshot ON TABLE orders AT (SNAPSHOT => '11b9d81eabc94c7da648908f0ba313a1');

-- Query the 'order_changes_after_snapshot' stream to view data changes captured after the specified snapshot
SELECT * FROM order_changes_after_snapshot;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     order_id    │   product_name   │     quantity    │         order_date         │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼──────────────────┼─────────────────┼────────────────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│            1002 │ Product B        │              20 │ 2024-03-28 03:24:16.629135 │ INSERT        │ false            │ acb58bd6bb4243a4bf0832bf570b38c2000000 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Create a stream 'order_changes_after_timestamp' on the 'orders' table, capturing data changes after a specific timestamp
CREATE STREAM order_changes_after_timestamp ON TABLE orders AT (TIMESTAMP => '2024-03-28 03:24:16.611835'::TIMESTAMP);

-- Query the 'order_changes_after_timestamp' stream to view data changes captured after the specified timestamp
SELECT * FROM order_changes_after_timestamp;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     order_id    │   product_name   │     quantity    │         order_date         │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼──────────────────┼─────────────────┼────────────────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│            1002 │ Product B        │              20 │ 2024-03-28 03:24:16.629135 │ INSERT        │ false            │ acb58bd6bb4243a4bf0832bf570b38c2000000 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
