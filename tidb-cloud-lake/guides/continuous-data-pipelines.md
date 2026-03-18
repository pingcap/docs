---
title: Continuous Data Pipelines
summary: Build end-to-end change data capture (CDC) flows in Databend with two primitives.
---
Build end-to-end change data capture (CDC) flows in Databend with two primitives:

- **Streams** capture every INSERT/UPDATE/DELETE until you consume them.
- **Tasks** run SQL on a schedule or when a stream reports new rows.

## Quick Navigation

- [Example 1: Append-Only Stream Copy](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md#example-1-append-only-stream) – capture inserts and consume them into another table.
- [Example 2: Standard Stream Updates](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md#example-2-standard-stream-updates--deletes) – see how updates/deletes appear and why only one consumer can drain a stream.
- [Example 3: Incremental Stream Metrics](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md#example-3-incremental-stream-join) – join multiple streams with `WITH CONSUME` to compute deltas batch by batch.
- [Example 1: Scheduled Copy Task](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md#example-1-scheduled-copy) – generate and load files with two recurring tasks.
- [Example 2: Stream-Triggered Merge](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md#example-2-stream-triggered-merge) – fire a task only when `STREAM_STATUS` is true.

## Why CDC in Databend

- **Lightweight** – streams keep the latest change set without duplicating full tables.
- **Transactional** – stream consumption succeeds or rolls back with your SQL statement.
- **Incremental** – rerun the same query with `WITH CONSUME` to process only new rows.
- **Schedulable** – tasks let you automate the copy, merge, or alert logic you already expressed in SQL.

Dive into the stream examples first, then combine them with tasks to automate your pipeline.
