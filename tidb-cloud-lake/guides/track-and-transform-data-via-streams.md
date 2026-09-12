---
title: 通过 Streams 跟踪和转换数据
summary: {{{ .lake }}} 中的 stream 是一种始终开启的变更表：每个已提交的 INSERT、UPDATE 或 DELETE 都会被捕获，直到你将其消费。本页保持简洁——先快速概览，再通过一个包含真实输出的实验帮助你直观了解 stream 的实际效果。
---

# 通过 Streams 跟踪和转换数据

{{{ .lake }}} 中的 stream 是一种始终开启的变更表：每个已提交的 INSERT、UPDATE 或 DELETE 都会被捕获，直到你将其消费。本页保持简洁——先快速概览，再通过一个包含真实输出的实验帮助你直观了解 stream 的实际效果。

## Stream 概览 {#stream-overview}

- Stream 不会复制表存储；在你消费之前，它会为每个受影响的行列出最新的变更。
- 消费（task、INSERT ... SELECT、`WITH CONSUME` 等）会清空 stream，同时保持其可继续接收新数据。
- `APPEND_ONLY` 默认为 `true`；仅当你必须捕获 UPDATE/DELETE 事件时，才将 `APPEND_ONLY = false`。

| 模式 | 捕获内容 | 典型用途 |
| --- | --- | --- |
| Standard (`APPEND_ONLY = false`) | INSERT + UPDATE + DELETE，并按每行折叠为最新状态。 | 缓慢变化维度、合规审计。 |
| Append-Only (`APPEND_ONLY = true`, default) | 仅 INSERT。 | 仅追加的事实/事件摄取。 |

## 示例 1：Append-Only Stream {#example-1-append-only-stream}

在任意 {{{ .lake }}} 部署（Cloud 工作区 (Worksheet) 或本地）中运行以下语句，查看默认 append-only 模式如何捕获并消费插入数据。

### 1. 创建表和 stream {#1-create-table-and-stream}

```sql
CREATE OR REPLACE TABLE sensor_readings (
    sensor_id INT,
    temperature DOUBLE
);

-- APPEND_ONLY defaults to true, so no extra clause is required.
CREATE OR REPLACE STREAM sensor_readings_stream
    ON TABLE sensor_readings;
```

### 2. 插入行并预览 {#2-insert-rows-and-preview}

```sql
INSERT INTO sensor_readings VALUES (1, 21.5), (2, 19.7);

SELECT sensor_id, temperature, change$action, change$is_update
FROM sensor_readings_stream;
```

输出：

```
┌────────────┬───────────────┬───────────────┬──────────────────┐
│ sensor_id  │ temperature   │ change$action │ change$is_update │
├────────────┼───────────────┼───────────────┼──────────────────┤
│          1 │ 21.5          │ INSERT        │ false            │
│          2 │ 19.7          │ INSERT        │ false            │
└────────────┴───────────────┴───────────────┴──────────────────┘
```

### 3. 消费（可选） {#3-consume-optional}

```sql
SELECT sensor_id, temperature
FROM sensor_readings_stream WITH CONSUME;

SELECT * FROM sensor_readings_stream; -- now empty
```

`WITH CONSUME` 会读取一次 stream 并清空增量，以便下一轮能够捕获新的 INSERT。

## 示例 2：Standard Stream（Updates 和 Deletes） {#example-2-standard-stream-updates-deletes}

当你必须对每个变异作出响应（包括 UPDATE 或 DELETE）时，请切换到 Standard 模式。

### 1. 创建 Standard stream {#1-create-a-standard-stream}

```sql
CREATE OR REPLACE STREAM sensor_readings_stream_std
    ON TABLE sensor_readings
    APPEND_ONLY = false;
```

### 2. 变异行并进行对比 {#2-mutate-rows-and-compare}

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

输出：

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

Standard stream 会结合上下文捕获每次变更：修改会在同一个 `sensor_id` 上显示为 DELETE+INSERT，而独立的删除/插入则会分别单独显示。Append-Only stream 会保持为空，因为它只跟踪插入。

## 示例 3：增量 Stream Join {#example-3-incremental-stream-join}

将多个 append-only stream 进行 join，以生成增量 KPI。由于 {{{ .lake }}} stream 会在数据被消费前一直保留新行，因此你可以在每次负载后运行同一个查询。每次执行都只会通过 [`WITH CONSUME`](/tidb-cloud-lake/sql/with-consume.md) 提取新的行，因此即使修改在不同时间到达，也仍会在下一次迭代中完成匹配。

### 1. 创建表和 stream {#1-create-tables-and-streams}

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

### 2. 加载第一批数据 {#2-load-the-first-batch}

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

### 3. 运行第一次增量查询 {#3-run-the-first-incremental-query}

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

这些 stream 现在已为空。当有更多行到达时，同一个查询将只捕获新数据。

### 4. 在下一批数据到达后再次运行 {#4-run-again-after-the-next-batch}

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

每个 stream 中的行会一直保留，直到运行 `WITH CONSUME`，因此即使插入在不同时间到达，也仍然会在下一次运行时被匹配到。当你预计还会有更多相关行到达时，可以先不消费这些 stream，然后重新运行查询以获取增量 delta。

## Stream 工作流说明 {#stream-workflow-notes}

**消费**

- Stream 会在事务内部被清空：`INSERT INTO target SELECT ... FROM stream` 只有在语句提交时才会清空 stream。
- 同一时间只能有一个消费者成功；其他并发语句会回滚。

**模式**

- Append-Only stream 仅捕获 INSERT，适合以追加为主的负载。
- Standard stream 会在你消费它们期间输出 update 和 delete；延迟到达的 update 会保留到下一次运行。

**隐藏列**

- Stream 会暴露 `change$action`、`change$is_update` 和 `change$row_id`；你可以使用它们来了解 {{{ .lake }}} 如何记录每一行。
- 基表会增加 `_origin_version`、`_origin_block_id`、`_origin_block_row_num`，用于调试行来源。

**集成**

- 将 stream 与 task 结合使用，并通过 `task_history('<name>', <limit>)` 实现按调度执行的增量 load。
- 当你只想清空最新的增量 delta 时，使用 [`WITH CONSUME`](/tidb-cloud-lake/sql/task.md)。
