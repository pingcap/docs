---
title: Amazon SQS (S3) Integration Task
summary: Learn how to create an Amazon SQS (S3) integration task that consumes S3 object creation events from an SQS queue and writes the corresponding object data into {{{ .lake }}}.
---

# Amazon SQS (S3) Integration Task

This page describes how to create an Amazon SQS (S3) integration task that consumes S3 object creation events from an SQS queue and writes the corresponding object data into {{{ .lake }}}.

This task is designed for S3 event-driven data ingestion. After an upstream system writes an object to S3, S3 sends an `ObjectCreated` event to SQS. {{{ .lake }}} consumes the SQS message through AssumeRole and writes data into {{{ .lake }}} based on the bucket and object key in the event.

If you need to create reusable SQS (S3) connection settings first, see [Amazon SQS (S3) - IAM Role (Beta)](/tidb-cloud-lake/guides/amazon-sqs-s3-iam-role.md).

## Use Cases

- Automatically ingest newly written S3 objects based on S3 `ObjectCreated` events
- Use S3 event notifications to drive data ingestion and reduce latency after new files arrive
- Avoid relying only on polling an S3 path to discover new files

## Workflow

1. An upstream system writes an object to an S3 bucket.
2. S3 Event Notification sends the `ObjectCreated` event to an SQS standard queue.
3. {{{ .lake }}} reads messages from the SQS queue through the IAM Role configured by the user.
4. The task parses the S3 event records in the message.
5. The task writes data into the {{{ .lake }}} target table based on the bucket, object key, and file format in the S3 event records.
6. After the write succeeds, the task deletes the processed SQS message from the queue.

> **Note:**
>
> S3 event notifications and SQS standard queues may both produce duplicate messages. {{{ .lake }}} handles failed retries. If your business logic requires strict deduplication, design downstream deduplication based on object information, event time, `sequencer`, or SQS message ID.

## Prerequisites

Before creating an SQS (S3) integration task, make sure:

- An **Amazon SQS (S3) - IAM Role** data source has already been created
- The S3 bucket has been configured with `ObjectCreated` event notification and sends events to the target SQS queue
- The SQS queue policy allows Amazon S3 to call `sqs:SendMessage`
- The user IAM Role allows {{{ .lake }}} platform roles to access it through `sts:AssumeRole`
- The user IAM Role has permissions to read the target S3 objects and consume the target SQS queue
- The SQS queue contains messages in the standard S3 Event Notification format
- The bucket, prefix, and suffix in the S3 notification match the data source configuration

## Creating an SQS (S3) Integration Task

### Step 1: Basic Info

1. Navigate to **Data** > **Data Integration** and click **Create Task**.
2. Select an SQS (S3) data source, then configure the basic parameters:

    | Field | Required | Description |
    |-------|----------|-------------|
    | **Data Source** | Yes | Select an existing **Amazon SQS (S3) - IAM Role** data source from the dropdown |
    | **Name** | Yes | Name of the integration task |
    | **File Format** | Yes | File format of the S3 objects, such as CSV, Parquet, or NDJSON |
    | **Object Key Prefix** | No | Only process object events with the specified prefix, such as `raw/events/`. This should match the data source and S3 notification filter |
    | **Object Key Suffix** | No | Only process object events with the specified suffix, such as `.json` or `.parquet`. This should match the data source and S3 notification filter |

    > **Tip:**
    >
    > We recommend configuring prefix or suffix filters in S3 Event Notification first, and keeping them consistent with the filters in the data source and task. This reduces unrelated messages entering SQS.

### Step 2: Preview Data

After completing the basic settings, click **Next** to preview the source data.

The preview result is the same as an [Amazon S3 Integration Task](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md). The system locates the corresponding S3 objects based on the SQS (S3) configuration, reads file content, and displays:

- Sample data with column names and data types
- The matched S3 object list and object sizes

> **Note:**
>
> If there are no previewable S3 objects in the current path scope, the preview page may not show sample data. Upload a test object that matches the target prefix / suffix, then retry the preview.

### Step 3: Set Target Table

Configure the target location in {{{ .lake }}}:

| Field | Description |
|-------|-------------|
| **Warehouse** | Select the {{{ .lake }}} warehouse used to run the SQS (S3) integration task |
| **Target Database** | Select the target database in {{{ .lake }}} |
| **Target Table** | Name of the target table to write data into |

The system infers column names and data types from the previewed S3 object content. Before continuing, you can review and edit the target table schema. If writing to an existing table, select the target table and verify the column mapping.

Click **Create** to create the integration task.

## Task Behavior

An SQS (S3) integration task is a continuously running task. After it starts, it periodically reads messages from the SQS queue and writes data into the target table until it is manually stopped.

| Scenario | Behavior |
|----------|----------|
| Messages exist in the queue | Reads messages, parses S3 event records, and writes data into the target table based on the object information in the events |
| Write succeeds | Deletes the corresponding SQS message to avoid duplicate processing |
| Write fails | Does not delete the corresponding SQS message, keeping it for later retry |
| Message format is not valid S3 Event Notification | Records the error and skips or stops processing |
| Task is stopped manually | Stops polling and saves the current task state |

## Difference from Amazon S3 Integration Task

| Task Type | Processed Object | Data Written to {{{ .lake }}} | Typical Use Case |
|-----------|------------------|--------------------------|------------------|
| Amazon S3 Integration Task | S3 file content | Business data from CSV, Parquet, or NDJSON files | File data import |
| Amazon SQS (S3) Integration Task | S3 ObjectCreated events in SQS | S3 object data corresponding to the events | Automatic ingestion of new objects, event-driven import |

If your goal is to periodically scan an S3 path and import file content, use an Amazon S3 Integration Task. If your goal is to trigger ingestion based on S3 ObjectCreated events, use an Amazon SQS (S3) Integration Task.
