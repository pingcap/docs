---
title: Stream
---

This page provides a comprehensive overview of stream operations in Databend, organized by functionality for easy reference.

## Stream Management

| Command | Description |
|---------|-------------|
| [CREATE STREAM](create-stream.md) | Creates a new stream to track changes in a table |
| [DROP STREAM](drop-stream.md) | Removes a stream |

## Stream Information

| Command | Description |
|---------|-------------|
| [DESC STREAM](desc-stream.md) | Shows detailed information about a stream |
| [SHOW STREAMS](show-streams.md) | Lists all streams in the current or specified database |

## Related Topics

- [Tracking and Transforming Data via Streams](/guides/load-data/continuous-data-pipelines/stream)

:::note
Streams in Databend are used to track and capture changes to tables, enabling continuous data pipelines and real-time data processing.
:::