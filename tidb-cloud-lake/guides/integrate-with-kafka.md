---
title: Kafka Consumer Integration Task (Beta)
summary: Create a Kafka Consumer task to continuously consume messages from Kafka topics and save the message content to internal object storage (tenant Stage).
---

# Kafka Consumer Integration Task (Beta)

This page describes how to create a Kafka Consumer task that continuously consumes messages from Kafka topics and saves the message content to internal object storage (tenant Stage).

Unlike S3, MySQL, or PostgreSQL integration tasks, a Kafka Consumer task does not write directly to a regular target table. After the task is created and started, you can use the `@kafka_consumer/<task_name>/` stage path to view saved message objects and query their content with SQL.

If you need to create reusable Kafka connection settings first, see [Kafka - Credentials (Beta)](/tidb-cloud-lake/guides/kafka-credentials.md).

## Use Cases

- Continuously ingest JSON messages from Kafka topics
- Land Kafka messages in internal object storage first, then query or process them with downstream SQL
- Preserve raw Kafka message objects for real-time or near-real-time data pipelines

## Workflow

1. An upstream system writes messages to Kafka topics.
2. The Kafka Consumer task reads messages from the specified topics.
3. The task saves messages in batches to internal object storage (tenant Stage).
4. Users view generated objects through `@kafka_consumer/<task_name>/`.
5. Users query message content from the stage and perform downstream loading or transformation as needed.

> **Note:**
>
> Kafka Consumer tasks save object files that contain Kafka message content. If you need to write messages into a business table, run downstream `INSERT INTO ... SELECT`, `COPY INTO`, or other processing based on the stage query results.

## Prerequisites

Before creating a Kafka Consumer task, make sure:

- A **Kafka - Credentials** data source has already been created
- Platform can access the Kafka brokers over the network
- The authentication method, TLS settings, and account information in the Kafka data source are correct
- The Kafka user has permission to read the target topics
- Messages in the target topics match the **Data Format** selected in the task

## Creating a Kafka Consumer Task

### Step 1: Basic Info

1. Navigate to **Data** > **Data Integration** and click **Create Task**.
2. Select a Kafka data source, then configure the basic parameters:

    | Field | Required | Description |
    |-------|----------|-------------|
    | **Data Source** | Yes | Select an existing **Kafka - Credentials** data source from the dropdown |
    | **Name** | Yes | Name of the Kafka Consumer task |
    | **Topics** | Yes | Kafka topics to consume. Separate multiple topics with commas, for example `topic-1,topic-2` |
    | **Data Format** | Yes | Kafka message data format. Currently, this is **JSON** |
    | **Start Position** | Yes | Start position when no committed offset exists. Supports **Latest** and **Earliest** |
    | **Max Batch Bytes** | No | Maximum data size per batch. The default value is **16 MiB** |
    | **Max Batch Wait Interval** | No | Maximum wait time per batch. The default value is **1 Minute** |

    > **Note:**
    >
    > **Latest** consumes only new messages, while **Earliest** starts from the earliest retained messages in Kafka. This setting applies only when the Consumer Group has no committed offset and does not reset existing offsets.

### Step 2: Preview Data

After completing the basic settings, click **Next** to enter **Preview Data Info**.

The system attempts to read sample messages from the specified Kafka topics. If messages are available, the page displays 1 to 2 JSON messages so you can verify the topics, data format, and message structure.

If no previewable messages are available, the page displays **No sample data available**. You can still continue creating the task, but we recommend checking whether the topics already contain messages and whether the selected **Start Position** can read sample data.

### Step 3: Result Viewing

In the **Result Viewing** step, select the **Warehouse** used to run the Kafka Consumer task.

After the task starts, Kafka messages are read and saved to internal object storage (tenant Stage). The page provides SQL examples. You can use `LIST @kafka_consumer/<task_name>/` to view generated objects and use stage queries to read message content.

```sql
-- List stage objects:
LIST @kafka_consumer/<task_name>/;

-- Query object data (replace with the correct PATTERN path):
SELECT $1
FROM @kafka_consumer (
    FILE_FORMAT=>'ndjson',
    PATTERN=>'<task_name>/year=YYYY/month=MM/day=DD/hour=HH/.*[.]ndjson'
);
```

Click **Create** to create the task.

## Task Behavior

A Kafka Consumer task is a continuously running task. After it starts, it consumes messages from the specified topics and saves the messages in batches as object files in internal object storage until it is manually stopped.

| Scenario | Behavior |
|----------|----------|
| New messages exist in the topics | Reads messages and writes them to the tenant Stage |
| Max Batch Bytes is reached | Writes the current batch to object storage |
| Max Batch Wait Interval is reached | Writes the current batch to object storage even if the batch size limit has not been reached |
| Write succeeds | Saves the consumption progress for later continuation |
| Task is stopped manually | Stops consuming and keeps the saved message objects |

## Query Saved Messages

Kafka Consumer tasks save message objects under the `@kafka_consumer/<task_name>/` path. After the task starts and writes objects, open the task details page and switch to the **Data Browsing** tab to view the object count and object list by UTC hour.

You can also use SQL to list objects first, then query their content based on the actual path:

```sql
LIST @kafka_consumer/<task_name>/;
```

```sql
SELECT $1
FROM @kafka_consumer (
    FILE_FORMAT=>'ndjson',
    PATTERN=>'<task_name>/year=YYYY/month=MM/day=DD/hour=HH/.*[.]ndjson'
);
```

If you need to write messages into a business table, continue with downstream transformation or loading based on the query result.

## Advanced Configuration

### Runtime Size

Kafka Consumer tasks support changing the runtime size. Before changing Runtime Size, stop the task, then open the edit page from the **Edit** menu, select an appropriate runtime size in the **Runtime Size** section, and save the change. After you restart the task, it runs with the new runtime size.

> **Note:**
>
> The available runtime sizes and prices depend on your billing plan. Use the options shown in the console and the pricing documentation as the source of truth.
