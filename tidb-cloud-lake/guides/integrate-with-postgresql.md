---
title: PostgreSQL Integration Task
summary: This page describes how to create a PostgreSQL integration task that synchronizes data from a PostgreSQL database into {{{ .lake }}}.
---

# PostgreSQL Integration Task

This page describes how to create a PostgreSQL integration task that synchronizes data from a PostgreSQL database into {{{ .lake }}}. PostgreSQL tasks support full `Snapshot` loads, continuous `Change Data Capture (CDC)`, or a combination of both.

If you need to create reusable PostgreSQL connection settings first, see [PostgreSQL - Credentials](/tidb-cloud-lake/guides/postgresql-credentials.md).

## Sync Modes

| Sync Mode      | Description                                                                                                  |
|----------------|--------------------------------------------------------------------------------------------------------------|
| Snapshot       | Performs a one-time full data load from the source table. Ideal for initial data migration or periodic bulk imports. |
| CDC Only       | Continuously captures real-time changes (inserts, updates, deletes) via PostgreSQL logical replication. Requires a primary key for merge operations. |
| Snapshot + CDC | First performs a full snapshot, then seamlessly transitions to continuous CDC. Recommended for most use cases. |

## Prerequisites

Before setting up PostgreSQL data integration, ensure your PostgreSQL instance meets the following requirements:

- A **PostgreSQL - Credentials** data source has already been created
- The target PostgreSQL instance is reachable from {{{ .lake }}}
- PostgreSQL version 10 or later

### Enable Logical Replication

PostgreSQL WAL (Write-Ahead Log) must be configured with logical level for CDC and Snapshot + CDC modes:

```ini title='postgresql.conf'
wal_level = logical
max_replication_slots = 4
max_wal_senders = 4
```

After modifying the configuration, restart PostgreSQL for the changes to take effect.

### Create a Dedicated User (Recommended)

Create a PostgreSQL user with the necessary permissions for data replication:

```sql
CREATE USER lake_cdc WITH PASSWORD 'your_password' REPLICATION;
GRANT CONNECT ON DATABASE your_database TO lake_cdc;
GRANT USAGE ON SCHEMA public TO lake_cdc;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO lake_cdc;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO lake_cdc;
```

### Create Publication and Replication Slot (Required for CDC)

For CDC and Snapshot + CDC modes, a publication and replication slot must exist. Because `CREATE PUBLICATION ... FOR ALL TABLES` requires superuser privileges, and adding individual tables requires table ownership, these objects should be created by a database owner or superuser before starting the CDC task.

Run the following as a superuser or database owner:

```sql
-- Create a publication that includes the tables you want to replicate
CREATE PUBLICATION bend_cdc_pub FOR ALL TABLES;

-- Create a logical replication slot
SELECT * FROM pg_create_logical_replication_slot('bend_cdc_slot', 'pgoutput');

-- Grant the dedicated user permission to use the replication slot
ALTER ROLE lake_cdc WITH REPLICATION;
```

> **Note:**
>
> If you only need to replicate specific tables instead of all tables, you can use:
>
> ```sql
> CREATE PUBLICATION bend_cdc_pub FOR TABLE table1, table2;
> ```
>
> This avoids the superuser requirement but still requires ownership of the listed tables.

### Network Access

Ensure the PostgreSQL instance is accessible from {{{ .lake }}}. Check your firewall rules and security groups to allow inbound connections on the PostgreSQL port.

## Creating a PostgreSQL Integration Task

### Step 1: Basic Info

1. Navigate to **Data** > **Data Integration** and click **Create Task**.

2. Configure the basic settings:

    | Field                      | Required    | Description                                                                                      |
    |----------------------------|-------------|--------------------------------------------------------------------------------------------------|
    | **Data Source**             | Yes         | Select an existing **PostgreSQL - Credentials** data source from the dropdown                    |
    | **Name**                   | Yes         | A name for this integration task                                                                 |
    | **Source Database**        | —           | Automatically displayed based on the selected data source                                        |
    | **Source Table**           | Yes         | Select the table to sync from the PostgreSQL database                                            |
    | **Sync Mode**             | Yes         | Choose from **Snapshot**, **CDC Only**, or **Snapshot + CDC**                                    |
    | **Primary Key**          | Conditional | The unique identifier column for merge operations. Required for CDC Only and Snapshot + CDC modes |
    | **Sync Interval**        | Yes         | Interval (in seconds) between write operations (default: 3)                                      |
    | **Batch Size**            | No          | Number of rows per batch                                                                         |
    | **Allow Delete**          | No          | Whether to permit DELETE operations in CDC. Available for CDC Only and Snapshot + CDC modes       |

#### Snapshot Mode Options

When using **Snapshot** mode, an additional option is available:

- **Snapshot WHERE Condition**: A SQL WHERE clause to filter data during the snapshot (e.g., `created_at > '2024-01-01'`). This allows you to load only a subset of the source data.

### Step 2: Preview Data

After configuring the basic settings, click **Next** to preview the source data.

The system fetches a sample row from the selected PostgreSQL table and displays the column names and data types. Review the data to ensure the correct table and columns are selected before proceeding.

### Step 3: Set Target Table

Configure the destination in {{{ .lake }}}:

| Field               | Description                                                        |
|---------------------|--------------------------------------------------------------------|
| **Warehouse**       | Select the target {{{ .lake }}} warehouse for running the sync    |
| **Target Database** | Choose the target database in {{{ .lake }}}                             |
| **Target Table**    | The table name in {{{ .lake }}} (defaults to the source table name)     |

The system automatically maps source columns to the target table schema. Review the column mappings, then click **Create** to finalize the integration task.

## Task Behavior by Sync Mode

| Sync Mode      | Behavior                                                                                          |
|----------------|---------------------------------------------------------------------------------------------------|
| Snapshot       | Runs once and automatically stops after the full data load is complete.                           |
| CDC Only       | Runs continuously, capturing real-time changes until manually stopped.                            |
| Snapshot + CDC | Completes the initial snapshot first, then transitions to continuous CDC until manually stopped.   |

For CDC tasks, the current LSN (Log Sequence Number) is saved as a checkpoint when stopped, allowing the task to resume from where it left off when restarted.

## Sync Mode Details

### Snapshot

Snapshot mode performs a one-time full read of the source table and loads all data into the target table in {{{ .lake }}}.

**Use cases:**

- Initial data migration from PostgreSQL to {{{ .lake }}}
- Periodic full data refresh
- One-time data imports with WHERE condition filtering

**Features:**

- Supports WHERE condition filtering to load a subset of data
- Task automatically stops after completion

### CDC (Change Data Capture)

CDC mode continuously monitors the PostgreSQL WAL (Write-Ahead Log) via logical replication and captures real-time row-level changes (INSERT, UPDATE, DELETE) from the source table.

**Use cases:**

- Real-time data replication
- Keeping {{{ .lake }}} in sync with operational PostgreSQL databases
- Event-driven data pipelines

**How it works:**

1. Connects to PostgreSQL using a logical replication slot
2. Captures row-level changes in real-time via the `pgoutput` plugin
3. Writes changes to a raw staging table in {{{ .lake }}}
4. Periodically merges changes into the target table using the primary key
5. Saves checkpoint (LSN position) for crash recovery

> **Note:**
>
> CDC mode requires PostgreSQL WAL level set to `logical`, and a primary key (unique column) must be specified. The PostgreSQL user must have `REPLICATION` privilege.

### Snapshot + CDC

This mode combines both approaches: it first performs a full snapshot of the source table, then seamlessly transitions to CDC mode for continuous change capture. This is the recommended mode for most data integration scenarios, as it ensures a complete initial data load followed by ongoing real-time synchronization.

## Advanced Configuration

### Primary Key

The primary key specifies the unique identifier column used for MERGE operations during CDC. When a change event is captured, {{{ .lake }}} uses this key to determine whether to insert a new row or update an existing one. Typically, this should be the primary key of the source table.

### Sync Interval

The sync interval (in seconds) controls how frequently captured changes are merged into the target table. A shorter interval provides lower latency but may increase resource usage. The default value of 3 seconds is suitable for most workloads.

### Batch Size

Controls the number of rows processed per batch during data loading. Adjusting this value can help optimize throughput for large tables. Leave empty to use the system default.

### Allow Delete

When enabled (default for CDC modes), DELETE operations captured from PostgreSQL WAL are applied to the target table in {{{ .lake }}}. When disabled, deletes are ignored, and the target table retains all historical records. This is useful for scenarios where you want to maintain a complete audit trail.
