---
title: Continuous Data Pipelines
---

Build end-to-end change data capture (CDC) flows in Databend with two primitives:

- **Streams** capture every INSERT/UPDATE/DELETE until you consume them.
- **Tasks** run SQL on a schedule or when a stream reports new rows.

## Quick Navigation

- [Example 1: Append-Only Stream Copy](./01-stream.md#example-1-append-only-stream-copy) – capture inserts and consume them into another table.
- [Example 2: Standard Stream Updates](./01-stream.md#example-2-standard-stream-updates) – see how updates/deletes appear and why only one consumer can drain a stream.
- [Example 3: Incremental Stream Metrics](./01-stream.md#example-3-incremental-stream-metrics) – join multiple streams with `WITH CONSUME` to compute deltas batch by batch.
- [Example 1: Scheduled Copy Task](./02-task.md#example-1-scheduled-copy) – generate and load files with two recurring tasks.
- [Example 2: Stream-Triggered Merge](./02-task.md#example-2-stream-triggered-merge) – fire a task only when `STREAM_STATUS` is true.

## Why CDC in Databend

- **Lightweight** – streams keep the latest change set without duplicating full tables.
- **Transactional** – stream consumption succeeds or rolls back with your SQL statement.
- **Incremental** – rerun the same query with `WITH CONSUME` to process only new rows.
- **Schedulable** – tasks let you automate the copy, merge, or alert logic you already expressed in SQL.

Dive into the stream examples first, then combine them with tasks to automate your pipeline.
