---
title: MySQL
summary: The MySQL data integration enables you to sync data from MySQL databases into {{{ .lake-short }}} in real-time, with support for full snapshot loads, continuous Change Data Capture (CDC), or a combination of both.
---

# MySQL

The MySQL data integration enables you to sync data from MySQL databases into {{{ .lake-short }}} in real-time, with support for full snapshot loads, continuous Change Data Capture (CDC), or a combination of both.

## Sync Modes

| Sync Mode      | Description                                                                                                  |
|----------------|--------------------------------------------------------------------------------------------------------------|
| Snapshot       | Performs a one-time full data load from the source table. Ideal for initial data migration or periodic bulk imports. |
| CDC Only       | Continuously captures real-time changes (inserts, updates, deletes) from MySQL binlog. Requires a primary key for merge operations. |
| Snapshot + CDC | First performs a full snapshot, then seamlessly transitions to continuous CDC. Recommended for most use cases. |

## Prerequisites

Before setting up MySQL data integration, ensure your MySQL instance meets the following requirements:

### Enable Binlog

MySQL binlog must be enabled with ROW format for CDC and Snapshot + CDC modes:

```ini title='my.cnf'
[mysqld]
server-id=1
log-bin=mysql-bin
binlog-format=ROW
binlog-row-image=FULL
```

After modifying the configuration, restart MySQL for the changes to take effect.

### Create a Dedicated User (Recommended)

Create a MySQL user with the necessary permissions for data replication:

```sql
CREATE USER 'databend_cdc'@'%' IDENTIFIED BY 'your_password';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'databend_cdc'@'%';
FLUSH PRIVILEGES;
```

### Network Access

Ensure the MySQL instance is accessible from {{{ .lake }}}. Check your firewall rules and security groups to allow inbound connections on the MySQL port.

## Creating a MySQL Data Source

1. Navigate to **Data** > **Data Sources** and click **Create Data Source**.

2. Select **MySQL - Credentials** as the service type, and fill in the connection details:

    | Field           | Required | Description                                                                 |
    |-----------------|----------|-----------------------------------------------------------------------------|
    | **Name**        | Yes      | A descriptive name for this data source                                     |
    | **Hostname**    | Yes      | MySQL server hostname or IP address                                         |
    | **Port Number** | Yes      | MySQL server port (default: 3306)                                           |
    | **DB Username** | Yes      | MySQL user with replication permissions                                     |
    | **DB Password** | Yes      | Password for the MySQL user                                                 |
    | **Database Name** | Yes    | The source database name                                                    |
    | **DB Charset**  | No       | Character set (default: utf8mb4)                                            |
    | **Server ID**   | No       | Unique binlog replication identifier. Auto-generated if not provided        |

    ![Create MySQL Data Source](/media/tidb-cloud-lake/databendcloud-dataintegration-create-mysql-source.png)

3. Click **Test Connectivity** to verify the connection. If the test succeeds, click **OK** to save the data source.

## Creating a MySQL Integration Task

### Step 1: Basic Info

1. Navigate to **Data** > **Data Integration** and click **Create Task**.

    ![Data Integration Page](/media/tidb-cloud-lake/dataintegration-page-with-create-button.png)

2. Configure the basic settings:

| Field                      | Required    | Description                                                                                      |
|----------------------------|-------------|--------------------------------------------------------------------------------------------------|
| **Data Source**             | Yes         | Select an existing MySQL data source from the dropdown                                           |
| **Name**                   | Yes         | A name for this integration task                                                                 |
| **Source Database**        | —           | Automatically displayed based on the selected data source                                        |
| **Source Table**           | Yes         | Select the table to sync from the MySQL database                                                 |
| **Sync Mode**             | Yes         | Choose from **Snapshot**, **CDC Only**, or **Snapshot + CDC**                                    |
| **Primary Key**          | Conditional | The unique identifier column for merge operations. Required for CDC Only and Snapshot + CDC modes |
| **Sync Interval**        | Yes         | Interval (in seconds) between write operations (default: 3)                                      |
| **Batch Size**            | No          | Number of rows per batch                                                                         |
| **Allow Delete**          | No          | Whether to permit DELETE operations in CDC. Available for CDC Only and Snapshot + CDC modes       |

![Create Task - Basic Info](/media/tidb-cloud-lake/create-mysql-task-step1-basic-info.png)

#### Snapshot Mode Options

When using **Snapshot** mode, additional options are available:

- **Snapshot WHERE Condition**: A SQL WHERE clause to filter data during the snapshot (e.g., `created_at > '2024-01-01'`). This allows you to load only a subset of the source data.

- **Archive Schedule**: Enable periodic archiving to automatically run snapshots on a recurring schedule. When enabled, the following fields appear:

| Field               | Description                                                              |
|---------------------|--------------------------------------------------------------------------|
| **Cron Expression** | Schedule in cron format (e.g., `0 1 * * *` for daily at 1:00 AM)        |
| **Timezone**        | Timezone for the schedule (default: UTC)                                 |
| **Mode**            | Archive frequency — **Daily**, **Weekly**, or **Monthly**                |
| **Time Column**     | The time-based column used for archive partitioning (e.g., `created_at`) |

### Step 2: Preview Data

After configuring the basic settings, click **Next** to preview the source data.

![Preview Data](/media/tidb-cloud-lake/create-mysql-task-preview-data-step.png)

The system fetches a sample row from the selected MySQL table and displays the column names and data types. Review the data to ensure the correct table and columns are selected before proceeding.

### Step 3: Set Target Table

Configure the destination in {{{ .lake-short }}}:

| Field               | Description                                                        |
|---------------------|--------------------------------------------------------------------|
| **Warehouse**       | Select the target {{{ .lake }}} warehouse for running the sync    |
| **Target Database** | Choose the target database in {{{ .lake-short }}}                             |
| **Target Table**    | The table name in {{{ .lake-short }}} (defaults to the source table name)     |

![Set Target Table](/media/tidb-cloud-lake/dataintegration-mysql-set-target-table.png)

The system automatically maps source columns to the target table schema. Review the column mappings, then click **Create** to finalize the integration task.

## Task Behavior by Sync Mode

| Sync Mode      | Behavior                                                                                          |
|----------------|---------------------------------------------------------------------------------------------------|
| Snapshot       | Runs once and automatically stops after the full data load is complete.                           |
| CDC Only       | Runs continuously, capturing real-time changes until manually stopped.                            |
| Snapshot + CDC | Completes the initial snapshot first, then transitions to continuous CDC until manually stopped.   |

For CDC tasks, the current binlog position is saved as a checkpoint when stopped, allowing the task to resume from where it left off when restarted.

## Sync Mode Details

### Snapshot

Snapshot mode performs a one-time full read of the source table and loads all data into the target table in {{{ .lake-short }}}.

**Use cases:**

- Initial data migration from MySQL to {{{ .lake-short }}}
- Periodic full data refresh
- One-time data imports with WHERE condition filtering

**Features:**

- Supports WHERE condition filtering to load a subset of data
- Supports periodic archive scheduling for recurring snapshots
- Task automatically stops after completion

### CDC (Change Data Capture)

CDC mode continuously monitors the MySQL binlog and captures real-time row-level changes (INSERT, UPDATE, DELETE) from the source table.

**Use cases:**

- Real-time data replication
- Keeping {{{ .lake-short }}} in sync with operational MySQL databases
- Event-driven data pipelines

**How it works:**

1. Connects to MySQL binlog using a unique server ID
2. Captures row-level changes in real-time
3. Writes changes to a raw staging table in {{{ .lake-short }}}
4. Periodically merges changes into the target table using the primary key
5. Saves checkpoint (binlog position) for crash recovery

> **Note:**
>
> CDC mode requires MySQL binlog to be enabled with ROW format, and a primary key (unique column) must be specified. The MySQL user must have `REPLICATION SLAVE` and `REPLICATION CLIENT` privileges.

### Snapshot + CDC

This mode combines both approaches: it first performs a full snapshot of the source table, then seamlessly transitions to CDC mode for continuous change capture. This is the recommended mode for most data integration scenarios, as it ensures a complete initial data load followed by ongoing real-time synchronization.

## Advanced Configuration

### Primary Key

The primary key specifies the unique identifier column used for MERGE operations during CDC. When a change event is captured, {{{ .lake-short }}} uses this key to determine whether to insert a new row or update an existing one. Typically, this should be the primary key of the source table.

### Sync Interval

The sync interval (in seconds) controls how frequently captured changes are merged into the target table. A shorter interval provides lower latency but may increase resource usage. The default value of 3 seconds is suitable for most workloads.

### Batch Size

Controls the number of rows processed per batch during data loading. Adjusting this value can help optimize throughput for large tables. Leave empty to use the system default.

### Allow Delete

When enabled (default for CDC modes), DELETE operations captured from MySQL binlog are applied to the target table in {{{ .lake-short }}}. When disabled, deletes are ignored, and the target table retains all historical records. This is useful for scenarios where you want to maintain a complete audit trail.

### Archive Schedule

For Snapshot mode, you can configure periodic archiving to automatically run snapshots on a recurring schedule. This is useful for scenarios where you need regular data refreshes without continuous CDC overhead.

- **Cron Expression**: Standard cron format for scheduling (e.g., `0 1 * * *` for daily at 1:00 AM)
- **Mode**: Choose **Daily**, **Weekly**, or **Monthly** archiving
- **Time Column**: Specify the column used for time-based partitioning (e.g., `created_at`)
- **Timezone**: Set the timezone for the schedule (default: UTC)
