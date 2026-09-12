---
title: CREATE STREAM
summary: 创建一个 stream。
---

# CREATE STREAM

创建一个 stream。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] STREAM [ IF NOT EXISTS ] [ <database_name>. ]<stream_name>
  ON TABLE [ <database_name>. ]<table_name>
  [ AT ( { TIMESTAMP => <timestamp> | SNAPSHOT => '<snapshot_id>' | STREAM => <existing_stream_name> } ) ]
  [ APPEND_ONLY = true | false ]
  [ COMMENT = '<comment>' ]
```

| 参数 | 描述 |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `< database_name >` | stream 会被视为属于某个特定数据库的对象，类似于表或视图。CREATE STREAM 允许 stream 与其关联表位于不同的数据库中。如果未显式指定数据库，则使用当前数据库作为所创建 stream 所属的数据库。 |
| AT                  | 当使用 `AT` 并跟随 `TIMESTAMP =>` 或 `SNAPSHOT =>` 时，可以基于时间戳或快照 ID 创建一个包含某个特定历史时间点之后数据变更的 stream；当 `AT` 跟随 `STREAM =>` 时，可以创建一个与现有 stream 相同的新 stream，并保留相同的已捕获数据变更。 |
| APPEND_ONLY         | 设置为 `true` 时，stream 以 `Append-Only` 模式运行；设置为 `false` 时，stream 以 `Standard` 模式运行。默认值为 `true`。有关 stream 运行模式的更多信息，请参见 [Stream 工作原理](/tidb-cloud-lake/sql/stream.md#stream-management)。 |

## 示例 {#examples}

以下示例演示如何创建一个名为 'order_changes' 的 stream，用于监控 'orders' 表中的变更：

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

以下示例使用 `AT` 参数创建一个名为 'order_changes_copy' 的新 stream，其中包含与 'order_changes' 相同的数据变更：

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

以下示例在 'orders' 表上创建了两个 stream。每个 stream 分别使用 `AT` 参数获取某个特定快照 ID 或时间戳之后的数据变更。

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