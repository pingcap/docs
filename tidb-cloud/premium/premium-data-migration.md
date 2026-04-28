---
title: Migrate Data to {{{ .premium }}} Using Data Migration
summary: Learn how to migrate data from MySQL-compatible databases to {{{ .premium }}} instances using the Data Migration feature in the TiDB Cloud console.
---

# Migrate Data to {{{ .premium }}} Using Data Migration

This document describes how to migrate data from a MySQL-compatible database to a {{{ .premium }}} instance using the Data Migration feature in the [TiDB Cloud console](https://tidbcloud.com/).

The Data Migration feature enables you to migrate existing MySQL data and continuously replicate ongoing changes (binlog) from your MySQL-compatible source database directly to a {{{ .premium }}} instance, reducing downtime and simplifying your migration to TiDB.

> **Note:**
>
> The Data Migration feature for {{{ .premium }}} is currently in Public Preview. During Public Preview, the source database must be reachable over a public network endpoint, and the source connection cannot be reused across migration jobs. For details, see [Limitations](#limitations).

## Supported source databases

The Data Migration feature supports any MySQL-compatible database with binary log replication enabled. The wizard exposes a single source-engine option (**MySQL**); to migrate from a managed MySQL service such as Amazon Aurora MySQL, Amazon RDS MySQL, Azure Database for MySQL - Flexible Server, Google Cloud SQL for MySQL, or Alibaba Cloud RDS MySQL, connect via the public endpoint of the managed instance.

Supported MySQL versions: 5.7 and 8.0.

## Migration modes

When you create a migration job, you choose one of the following modes:

- **Full + Incremental**: migrates existing data from the source database first, and then continuously replicates ongoing changes (binlog) to the target {{{ .premium }}} instance.
- **Incremental Data Only**: continuously replicates ongoing changes (binlog) from the source database to the target {{{ .premium }}} instance, starting from the current binlog position.

## Limitations

### Public Preview limitations

- Connectivity to the source database is currently public-only. Private Link connectivity to the source database is in development and not yet generally available.
- Source connection details cannot be saved or reused across migration jobs. Each migration job requires the source connection to be entered from scratch.
- Migration jobs created during Public Preview might be subject to additional restrictions as the feature matures. For up-to-date information, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

### General limitations

- The system databases `mysql`, `information_schema`, `performance_schema`, and `sys` are filtered out and not migrated, even if you select all databases.
- During existing data migration, if the target database already contains the table to be migrated and there are duplicate keys, the rows with duplicate keys are replaced.

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

The migration user on the source database must have privileges sufficient to read schema and data and to read the binary log, including (but not limited to) `SELECT`, `RELOAD`, `REPLICATION SLAVE`, and `REPLICATION CLIENT`. For managed MySQL services such as AWS RDS, Aurora, Azure Database for MySQL, Google Cloud SQL, and Alibaba Cloud RDS, additional service-specific permissions might be required. For details, see [Grant required privileges to the migration user in the source database](/tidb-cloud/migrate-from-mysql-using-data-migration.md#grant-required-privileges-to-the-migration-user-in-the-source-database).

On the target {{{ .premium }}} instance, the migration user must have privileges sufficient to create databases, create tables, and write data in the target schemas. For details, see [Grant required privileges to the migration user in the target database](/tidb-cloud/migrate-from-mysql-using-data-migration.md#grant-required-privileges-to-the-migration-user-in-the-target-database).

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

1. Select the **Migration Type**: **Full + Incremental** (default) or **Incremental Data Only**.
2. The wizard scans the source database and displays the available databases and tables. Select the databases and tables you want to migrate. The system databases (`mysql`, `information_schema`, `performance_schema`, `sys`) are filtered out automatically.
3. Click **Next**.

### Step 3: Precheck

The console runs prechecks against the source database, network connectivity, and the target {{{ .premium }}} instance. If any precheck fails, follow the displayed error messages to fix the issue, and then click **Recheck**. For common precheck errors and remediation, see [Precheck errors and solutions](/tidb-cloud/migrate-from-mysql-using-data-migration.md#precheck-errors-and-solutions).

When all prechecks pass, click **Next**.

### Step 4: Review and start migration

Review the configuration summary. When you are ready, click **Create Job and Start** to create the migration job. The console redirects to the job detail page, where the job status starts in **Creating** and transitions to **Running** when the migration begins.

## Manage a migration job

After a migration job is created, you can monitor and manage it from the **Data Migration** page of your {{{ .premium }}} instance.

### View job status and progress

The migration job list shows the **Name**, **Status**, **Mode**, **Target User**, and **Creation Time** for each job. Click a migration job to open its detail page, which shows:

- A **Summary** panel with the job name, ID, status, mode, data source, data target, migration objects, and creation time.
- A **Progress** panel that shows the migration progress once the job starts running.

### Pause, resume, or delete a migration job

From the migration job detail page or from the actions menu in the job list, you can take the following actions:

- **Pause**: temporarily pause a running migration job. You can resume it later from the same position.
- **Resume**: resume a paused migration job.
- **Delete**: delete the migration job and its metadata. This action does not affect data already migrated to the target instance.

## See also

- [Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md): the canonical Data Migration reference, including detailed prerequisites, source-specific configuration, and troubleshooting.
- [Migrate Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md): a focused guide for incremental-only migration scenarios.
- [Connect to Your {{{ .premium }}} Instance](/tidb-cloud/premium/connect-to-tidb-instance.md): network and connectivity options for {{{ .premium }}} instances.
