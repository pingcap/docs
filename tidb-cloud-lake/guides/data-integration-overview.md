---
title: Data Integration
summary: The Data Integration feature in Databend Cloud enables you to load data from external sources into Databend through a visual, no-code interface. You can create data sources, configure integration tasks, and monitor synchronization — all from the Databend Cloud console.
---
# Data Integration Overview

The Data Integration feature in Databend Cloud enables you to load data from external sources into Databend through a visual, no-code interface. You can create data sources, configure integration tasks, and monitor synchronization — all from the Databend Cloud console.

## Supported Data Sources

| Data Source          | Description                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------- |
| [MySQL](/tidb-cloud-lake/guides/integrate-with-mysql.md)  | Sync data from MySQL databases with support for Snapshot, CDC, and Snapshot + CDC modes. |
| [Amazon S3](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) | Import files from Amazon S3 buckets with support for CSV, Parquet, and NDJSON formats.   |

## Key Concepts

### Data Source

A data source represents a connection to an external system. It stores the credentials and connection details needed to access the source data. Once configured, a data source can be reused across multiple integration tasks.

Databend Cloud currently supports two types of data sources:

- **MySQL - Credentials**: Connection to a MySQL database (host, port, username, password, database).
- **AWS - Credentials**: Connection to Amazon S3 (Access Key and Secret Key).

### Integration Task

An integration task defines how data flows from a source to a target table in Databend. Each task specifies the source configuration, target warehouse and table, and operational parameters specific to the data source type.

## Managing Data Sources

![Data Sources Overview](/media/tidb-cloud-lake/databendcloud-dataintegration-datasource-overview.png)

To manage data sources, navigate to **Data** > **Data Sources** from the left sidebar. From this page you can:

- View all configured data sources
- Create new data sources
- Edit or delete existing data sources
- Test connectivity to verify credentials

> **Tip:**
>
> It is recommended to always test the connection before saving a data source. This helps catch common issues such as incorrect credentials or network restrictions early.

## Managing Tasks

### Starting and Stopping Tasks

After creation, a task is in a **Stopped** state. To begin data synchronization, click the **Start** button on the task.

![Task List](/media/tidb-cloud-lake/dataintegration-task-list-with-action-button.png)

To stop a running task, click the **Stop** button. The task will gracefully shut down and save its progress.

### Task Status

The Data Integration page displays all tasks with their current status:

| Status  | Description                   |
| ------- | ----------------------------- |
| Running | Task is actively syncing data |
| Stopped | Task is not running           |
| Failed  | Task encountered an error     |

### Viewing Run History

Click on a task to view its execution history. The run history includes:

- Execution start and end times
- Number of rows synced
- Error details (if any)

![Run History](/media/tidb-cloud-lake/dataintegration-run-history-page.png)

## Video Tour

<iframe width="853" height="505" class="iframe-video" src="https://www.youtube.com/embed/yfYAPVD-oHE?si=m1Gyp3KPinO1JQ17" title="YouTube video player" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" allowfullscreen></iframe>
