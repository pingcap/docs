---
title: Integration Tasks
summary: This page provides an overview of integration tasks in {{{ .lake }}}. Integration tasks define how data flows from external sources into {{{ .lake }}}, including source settings, target tables, and runtime parameters.
---

# Integration Tasks

An integration task in {{{ .lake }}} defines how data flows from a source into {{{ .lake }}}. Each task references an existing data source and specifies source settings, a target location or result viewing method, and runtime parameters that are specific to the task type.

Unlike data sources, integration tasks are the executable units that actually perform data movement, synchronization, or message consumption. Data sources store access settings, while tasks handle scheduling, ingestion, synchronization, consumption, stopping, resuming, and monitoring.

## Supported Task Types

| Task Type | Description |
|-----------|-------------|
| [Amazon S3](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) | Imports CSV, Parquet, or NDJSON files from Amazon S3 with support for one-time or continuous ingestion. |
| [Amazon SQS (S3) (Beta)](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md) | Consumes S3 object creation events from an SQS queue and writes the corresponding object data into {{{ .lake }}}. |
| [MySQL](/tidb-cloud-lake/guides/integrate-with-mysql.md) | Synchronizes table data from MySQL using `Snapshot`, `CDC Only`, or `Snapshot + CDC`. |
| [PostgreSQL](/tidb-cloud-lake/guides/integrate-with-postgresql.md) | Synchronizes table data from PostgreSQL using `Snapshot`, `CDC Only`, or `Snapshot + CDC`. |
| [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md) | Continuously consumes messages from Kafka topics and saves the message content to internal object storage. |

## Reading Guide

Recommended reading order:

1. Start with [Task Management](/tidb-cloud-lake/guides/task-management.md) to understand the task creation flow, start / stop behavior, status, and run history.
2. Then read the task-specific guide for the source type you want to configure.

## Task Type Differences

- S3 tasks are designed for file import scenarios and mainly focus on file path patterns, file formats, and ingestion behavior.
- SQS (S3) tasks are designed for S3 event-driven data ingestion and mainly focus on the SQS queue, S3 event filters, IAM Role, and target table.
- MySQL and PostgreSQL tasks are designed for table synchronization scenarios and mainly focus on sync modes, primary keys, incremental capture, and archive scheduling.
- Kafka Consumer tasks are designed for message consumption scenarios and mainly focus on topics, start position, batch size, batch wait interval, and tenant Stage queries.
