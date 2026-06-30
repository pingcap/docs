---
title: Data Integration Overview
summary: The Data Integration feature in {{{ .lake }}} provides a visual, no-code interface for importing or synchronizing data from external systems into {{{ .lake }}}.
---

# Data Integration Overview

The Data Integration feature in {{{ .lake }}} provides a visual, no-code interface for importing, synchronizing, or consuming data from external systems into {{{ .lake }}}. The feature centers around two key concepts: **data sources** and **integration tasks**.

## Key Concepts

| Concept | Description |
|---------|-------------|
| [Data Sources](/tidb-cloud-lake/guides/data-sources.md) | Reusable connection settings or credentials used to access external systems or send notifications, such as AWS Access Key / Secret Key, MySQL hostname / username / password, SQS (S3) queue URL, Kafka broker addresses, or a FeiShu bot webhook. |
| [Integration Tasks](/tidb-cloud-lake/guides/integration-tasks.md) | Executable tasks that define where data comes from, where the task writes data or how it saves results, which runtime parameters it uses, and how you start and monitor the task. |

Data sources do not move data by themselves. They only store the information required to access external systems. Integration tasks are the units that actually perform imports, snapshots, continuous synchronization, or message consumption.

<!-- Will add back this note after the service hosting pricing is finalized and published.

> **Note:**
>
> Running Data Integration tasks incurs service hosting fees. {{{ .lake }}} bills these fees per second based on the actual running time of the service. For details, see [Service Hosting Pricing](/tidb-cloud-lake/guides/pricing-billing.md#service-hosting-pricing).

-->

Not every data source corresponds to an ingestion task. For example, `FeiShuBot` is used for notifications rather than loading source data into {{{ .lake }}}.

## Supported Integration Task Types

| Task Type | Description |
|-----------|-------------|
| [Amazon S3](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) | Imports CSV, Parquet, or NDJSON files from Amazon S3 with support for one-time or continuous ingestion. |
| [Amazon SQS (S3) (Beta)](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md) | Consumes S3 object creation events from an SQS queue and writes the corresponding object data into {{{ .lake }}}. |
| [MySQL](/tidb-cloud-lake/guides/integrate-with-mysql.md) | Synchronizes table data from MySQL using `Snapshot`, `CDC Only`, or `Snapshot + CDC` modes. |
| [PostgreSQL](/tidb-cloud-lake/guides/integrate-with-postgresql.md) | Synchronizes table data from PostgreSQL using `Snapshot`, `CDC Only`, or `Snapshot + CDC` modes. |
| [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md) | Continuously consumes messages from Kafka topics and saves the message content to internal object storage. |

## Recommended Flow

1. Create and test reusable connection settings on the [Data Sources](/tidb-cloud-lake/guides/data-sources.md) page.
2. Review supported task types and their use cases on the [Integration Tasks](/tidb-cloud-lake/guides/integration-tasks.md) page.
3. Read the task-specific guide to configure the source, preview the data, and configure the result location or result viewing method.
4. Use the [Task Management](/tidb-cloud-lake/guides/task-management.md) page to start tasks, check status, and troubleshoot execution issues.

## Video Tour

<iframe width="853" height="505" class="iframe-video" src="https://www.youtube.com/embed/yfYAPVD-oHE?si=m1Gyp3KPinO1JQ17" title="YouTube video player" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" allowfullscreen></iframe>
