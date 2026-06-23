---
title: Task Management
summary: This page describes common operations for integration tasks, including the task creation flow, start and stop behavior, task states, and run history. For source-specific configuration, see the detailed task guides.
---

# Task Management

This page describes common operations for integration tasks, including the task creation flow, start and stop behavior, task states, and run history. For source-specific configuration, see the detailed task guides.

## General Task Creation Flow

1. Navigate to **Data** > **Data Integration** and click **Create Task**.
2. Select an existing data source.
3. Fill in source-side parameters based on the task type, such as file path, source table, sync mode, topic, or filter conditions.
4. Preview the source data and verify the schema, field types, or message content.
5. Depending on the task type, select the target warehouse and target database / table, or configure how to view results.
6. Create the task and start it when needed.

## Starting and Stopping Tasks

After a task is created, its initial state is **Stopped**. To begin synchronization, ingestion, or consumption, click **Start** on the task.

To stop a running task, click **Stop**. The task will shut down gracefully and save its current progress.

## Task Status

The Data Integration page shows all tasks and their current status:

| Status | Description |
|--------|-------------|
| Running | The task is actively synchronizing, importing, or consuming data |
| Stopped | The task is currently not running |
| Failed | The task encountered an error during execution |

## Viewing Run History

Click a task to view its execution history. The run history includes:

- Execution start or end time
- Number of rows imported or synchronized, or message objects written
- Error details, if any

## Runtime Behavior by Task Type

- S3 tasks can run once or continuously poll for new files.
- MySQL `Snapshot` tasks usually stop automatically after the full load completes.
- MySQL `CDC Only` and `Snapshot + CDC` tasks continue running until manually stopped.
- PostgreSQL `Snapshot` tasks usually stop automatically after the full load completes.
- PostgreSQL `CDC Only` and `Snapshot + CDC` tasks continue running until manually stopped.
- SQS (S3) tasks continuously poll the SQS queue, consume S3 object creation events, and write data into the target table until manually stopped.
- Kafka Consumer tasks continuously consume Kafka topics and save message content to internal object storage until manually stopped.

For field-level configuration and detailed behavior, continue with the relevant task guide:

- [Amazon S3 Integration Task](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md)
- [Amazon SQS (S3) Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md)
- [MySQL Integration Task](/tidb-cloud-lake/guides/integrate-with-mysql.md)
- [PostgreSQL Integration Task](/tidb-cloud-lake/guides/integrate-with-postgresql.md)
- [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md)
