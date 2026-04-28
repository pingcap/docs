---
title: Migrate Data to {{{ .premium }}} Using Data Migration
summary: Learn how to migrate data from MySQL-compatible databases to {{{ .premium }}} instances using the Data Migration feature in the TiDB Cloud console.
---

# Migrate Data to {{{ .premium }}} Using Data Migration

This document describes how to migrate data from a MySQL-compatible database to a {{{ .premium }}} instance using the Data Migration feature in the [TiDB Cloud console](https://tidbcloud.com/).

The Data Migration feature enables you to migrate existing MySQL data and continuously replicate ongoing changes (binlog) from your MySQL-compatible source database directly to a {{{ .premium }}} instance, reducing downtime and simplifying your migration to TiDB.

> **Note:**
>
> The Data Migration feature for {{{ .premium }}} is currently in Public Preview. During Public Preview, the source database must be reachable over a public network endpoint, and you cannot reuse the source connection across migration jobs. For details, see [Limitations](#limitations).

## Supported source databases

The Data Migration feature supports any MySQL-compatible database with binary log replication enabled. The wizard exposes a single source-engine option (**MySQL**); to migrate from a managed MySQL service such as Amazon Aurora MySQL, Amazon RDS MySQL, Azure Database for MySQL - Flexible Server, Google Cloud SQL for MySQL, or Alibaba Cloud RDS MySQL, connect via the public endpoint of the managed instance.

Supported MySQL versions: 5.7 and 8.0.

## Migration modes

When you create a migration job, you choose a **Migration process** and an **Existing data migration mode**.

The **Migration process** determines what data is migrated:

- **Full + Incremental**: migrates existing data from the source database first, and then continuously replicates ongoing changes (binlog) to the target {{{ .premium }}} instance.
- **Incremental only**: continuously replicates ongoing changes (binlog) from the source database to the target {{{ .premium }}} instance, starting from the current binlog position.

The **Existing data migration mode** determines how the existing data load is performed when **Full + Incremental** is selected:

- **Logical** (default): exports rows from the source database and replays them as SQL `INSERT` statements on the target instance. Logical mode applies before any incremental replication starts. This mode consumes Request Capacity Units (RCUs) on the target instance during the data load.
- **Physical**: uses `IMPORT INTO` on the target instance to import data without RCU charges during the load. Use this mode for large datasets where load throughput and cost are priorities.

The **Existing data migration mode** does not apply to **Incremental only** migrations.

When you use physical mode, the following limitations apply:

- After the migration job has started, do **NOT** enable PITR (Point-in-time Recovery) or have any changefeed on the {{{ .premium }}} instance. Otherwise, the migration job stops. If you need to enable PITR or have any changefeed, use logical mode instead.
- You cannot create a second migration job or import task for the {{{ .premium }}} instance before the existing data migration is completed.

## Limitations

### Public Preview limitations

- Connectivity to the source database is currently public-only. Private Link connectivity to the source database is in development and not yet generally available.
- Source connection details cannot be saved or reused across migration jobs. Each migration job requires the source connection to be entered from scratch.
- Migration jobs created during Public Preview might be subject to additional restrictions as the feature matures. For up-to-date information, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

### General limitations

- The system databases `mysql`, `information_schema`, `performance_schema`, and `sys` are filtered out and not migrated, even if you select all databases.
- During existing data migration, if the target database already contains the table to be migrated and there are duplicate keys, TiDB Cloud replaces the rows with duplicate keys.
- During incremental data migration, if a migration job recovers from an abrupt error, it might enter safe mode for 60 seconds. During safe mode, TiDB Cloud migrates `INSERT` statements as `REPLACE`, and `UPDATE` statements as `DELETE` and `REPLACE`. For source tables without primary keys or non-null unique indexes, this can result in duplicated rows in the target instance.

For a complete list of Data Migration limitations across TiDB Cloud, see [Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md#limitations).

## Prerequisites

Before creating a migration job, make sure the following prerequisites are met.

### Enable binary logs on the source database

To replicate incremental changes from the source MySQL-compatible database to the target {{{ .premium }}} instance, configure the source database with the following settings:

| Configuration                    | Required value | Purpose |
|:---------------------------------|:---------------|:--------|
| `log_bin`                        | `ON`           | Enables binary logging, which Data Migration uses to replicate changes to TiDB. |
| `binlog_format`                  | `ROW`          | Captures all data changes accurately. |
| `binlog_row_image`               | `FULL`         | Includes all column values in events for safe conflict resolution. |
| `binlog_expire_logs_seconds`     | ≥ `86400` (1 day); `604800` (7 days) recommended | Ensures Data Migration can access consecutive logs during migration. |
| `binlog_transaction_compression` | `OFF`          | Data Migration does not support transaction compression. |

For detailed configuration steps for self-managed MySQL, AWS RDS, Aurora, Azure Database for MySQL, Google Cloud SQL, and Alibaba Cloud RDS, see [Enable binary logs in the source MySQL-compatible database for replication](/tidb-cloud/migrate-from-mysql-using-data-migration.md#enable-binary-logs-in-the-source-mysql-compatible-database-for-replication).

### Ensure network connectivity

The {{{ .premium }}} instance connects to the source database over the public internet during Public Preview. Make sure that:

- The source database accepts inbound connections from the public IP ranges used by the {{{ .premium }}} region.
- Any firewall, security group, or network ACL between the {{{ .premium }}} instance and the source database allows traffic on the source database port (typically `3306`).

The target {{{ .premium }}} instance must also be reachable. If the target cluster's public endpoint is disabled, enable it under **Settings** > **Networking** before creating the migration job. For more information, see [Connect via Public Endpoint](/tidb-cloud/premium/connect-to-premium-via-public-connection.md).

### Grant required privileges

The migration user on the source database must have privileges sufficient to read schema and data and to read the binary log, including (but not limited to) `SELECT`, `RELOAD`, `REPLICATION SLAVE`, `REPLICATION CLIENT`, and `PROCESS`. The pre-check step warns if the `PROCESS` privilege is missing, because Data Migration uses it to verify that the migration user does not exceed the source database's connection-concurrency limit.

For managed MySQL services such as AWS RDS, Aurora, Azure Database for MySQL, Google Cloud SQL, and Alibaba Cloud RDS, additional service-specific permissions might be required. For details, see [Grant required privileges to the migration user in the source MySQL database](/tidb-cloud/migrate-from-mysql-using-data-migration.md#grant-required-privileges-to-the-migration-user-in-the-source-mysql-database).

On the target {{{ .premium }}} instance, the migration user must have privileges sufficient to create databases, create tables, and write data in the target schemas. For details, see [Grant required privileges for migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md#grant-required-privileges-for-migration).

## Create a migration job

To create a migration job from a MySQL-compatible source database to a {{{ .premium }}} instance, take the following steps.

### Step 1: Configure source and target connection

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page.

   > **Tip:**
   >
   > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click the name of your target {{{ .premium }}} instance to go to its overview page, and then click **Data** > **Data Migration** in the left navigation pane.

3. On the **Data Migration** page, click **Create Migration Job** in the upper-right corner.

4. On the **Configure source and target connection** step, enter the following information:

    - **Job Name**: a name for the migration job. The default value is `migration_job_{timestamp}`. The name must start with a letter, can contain letters, numbers, underscores (`_`), and hyphens (`-`), and must be less than 60 characters.
    - **Source Connection Profile**:
        - **Data Source**: select **MySQL**.
        - **Connectivity Method**: select **Public**.
        - **Hostname or IP address**: enter the hostname or IP address of the source database.
        - **Port**: enter the source database port. The default is `3306`.
        - **User Name** and **Password**: enter the credentials for the migration user. This user must have the privileges listed in [Grant required privileges](#grant-required-privileges).
        - **SSL/TLS**: enabled by default. If your source database requires encrypted connections, upload the **CA Certificate**, **Client Certificate**, and **Client private key** as needed. If your source database does not require encrypted connections, turn off the **SSL/TLS** toggle.
    - **Target Connection Profile**: the **Region**, **Cluster ID**, and **Cluster Name** fields are auto-populated from the current {{{ .premium }}} instance. Enter the **User Name** and **Password** for a TiDB user that has sufficient privileges in the target instance.

5. Click **Validate Connection and Next**. The console validates both source and target connections. If validation fails, the wizard displays an error and remains on this step. Resolve the issue and try again.

### Step 2: Choose objects to be migrated

In the **Migration Type** section, configure how data is migrated:

- **Migration process**: select **Full + Incremental** (default) or **Incremental only**.
- **Existing data migration mode** (only applies to **Full + Incremental**): select **Logical** (default) or **Physical**. For details, see [Migration modes](#migration-modes).

In the **Select Objects to Migrate** section, choose:

- **All** (default): migrate every database and table on the source. TiDB Cloud automatically excludes the system databases (`mysql`, `information_schema`, `performance_schema`, `sys`).
- **Customize**: pick specific databases and tables. The wizard fetches the source schema and shows two panels, **Source Database** and **Selected Objects**. Use the arrow buttons between the panels to move databases or tables into the **Selected Objects** list.

Click **Next**.

### Step 3: Pre-check

The console runs the pre-check against the source database, network connectivity, and the target {{{ .premium }}} instance. The progress bar shows **Running {percentage}%** while checks execute, and **Finished 100%** when complete. The summary line reports the total number of items, including those that are completed, passed, with warnings, or failed.

The **Pre-check Result** table lists every item that did not pass, along with its reason and a suggested solution. To re-run the pre-check after fixing an item, click **Check Again**. To proceed without addressing a warning, you can dismiss it by selecting **Ignore** on the row.

If the pre-check completes with at least one warning and you click **Next**, the console shows a confirmation dialog with two options:

- **Check Again**: return to the **Pre-check Result** table and address the warnings.
- **Ignore warnings**: advance to the next step. Note that ignoring warnings may result in job failures or data inconsistencies.

When all checks pass (or you choose to ignore the remaining warnings), click **Next**.

### Step 4: Review and start migration

The review page shows three sections summarizing the migration job:

- **Job Configuration**: job name and migration type.
- **Source Connection Profile**: data source, host, port, connectivity method, username, SSL/TLS status, selected objects, and the existing data migration mode (shown as **Import Mode** on the review page).
- **Target Connection Profile**: region, cluster ID, cluster name, and target username.

Click **Previous** to revise any setting, or click **Create Job and Start** to create the migration job. The console redirects to the job detail page, where the job status starts in **Creating** and transitions to **Running** when the migration begins.

## Manage a migration job

After a migration job is created, you can monitor and manage it from the **Data Migration** page of your {{{ .premium }}} instance.

### View job status and progress

The migration job list shows the **Name**, **Status**, **Mode**, **Target User**, and **Creation Time** for each job. Click a migration job to open its detail page, which shows:

- A **Summary** panel with the job name, ID, status, mode, data source, data target, migration objects, and creation time.
- A **Progress** panel that shows the migration progress once the job starts running.

### Manage a migration job from the job list

To manage a migration job, click the `...` (more) button at the end of the migration job row on the **Data Migration** page. The actions menu shows different options depending on the job status:

- **View**: navigate to the job detail page.
- **Pause**: temporarily pause a running migration job. You can resume it later from the same position.
- **Resume**: resume a paused migration job.
- **Delete**: delete the migration job and its metadata. This action does not affect data already migrated to the target instance.

**Pause** and **Resume** are only available when the job is in a running or paused state. While the job is in the **Creating** state, only **View** and **Delete** are available.

## See also

- [Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md): the canonical Data Migration reference, including detailed prerequisites, source-specific configuration, and troubleshooting.
- [Migrate Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md): a focused guide for incremental-only migration scenarios.
- [Connect to Your {{{ .premium }}} Instance](/tidb-cloud/premium/connect-to-tidb-instance.md): network and connectivity options for {{{ .premium }}} instances.
