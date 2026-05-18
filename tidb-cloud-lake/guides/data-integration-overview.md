---
title: Data Integration Overview
summary: The Data Integration feature in {{{ .lake }}} provides a visual, no-code interface for importing or synchronizing data from external systems into {{{ .lake }}}.
---

# Data Integration Overview

The Data Integration feature in {{{ .lake }}} provides a visual, no-code interface for importing or synchronizing data from external systems into {{{ .lake }}}. The feature centers around two key concepts: **data sources** and **integration tasks**.

## Key Concepts

| Concept | Description |
|---------|-------------|
| [Data Sources](/tidb-cloud-lake/guides/data-sources.md) | Reusable connection settings or credentials used to access external systems or send notifications, such as AWS Access Key / Secret Key, MySQL hostname / username / password, or a FeiShu bot webhook. |
| [Integration Tasks](/tidb-cloud-lake/guides/integration-tasks.md) | Executable tasks that define where data comes from, which {{{ .lake }}} table it is written to, which runtime parameters are used, and how the task is started and monitored. |

Data sources do not move data by themselves. They only store the information required to access external systems. Integration tasks are the units that actually perform imports, snapshots, and continuous synchronization.

Not every data source corresponds to an ingestion task. For example, `FeiShuBot` is used for notifications rather than loading source data into {{{ .lake }}}.

## Supported Integration Task Types

| Task Type | Description |
|-----------|-------------|
| [Amazon S3](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) | Imports CSV, Parquet, or NDJSON files from Amazon S3 with support for one-time or continuous ingestion. |
| [MySQL](/tidb-cloud-lake/guides/integrate-with-mysql.md) | Synchronizes table data from MySQL using `Snapshot`, `CDC Only`, or `Snapshot + CDC` modes. |

## Recommended Flow

1. Create and test reusable connection settings on the [Data Sources](/tidb-cloud-lake/guides/data-sources.md) page.
2. Review supported task types and their use cases on the [Integration Tasks](/tidb-cloud-lake/guides/integration-tasks.md) page.
3. Read the task-specific guide to configure the source, preview the data, and set the target table.
4. Use the [Task Management](/tidb-cloud-lake/guides/task-management.md) page to start tasks, check status, and troubleshoot execution issues.

## Video Tour

<iframe width="853" height="505" class="iframe-video" src="https://www.youtube.com/embed/yfYAPVD-oHE?si=m1Gyp3KPinO1JQ17" title="YouTube video player" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" allowfullscreen></iframe>
