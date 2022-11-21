---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Migration Jobs
summary: Learn how to migrate data from MySQL-compatible databases hosted in AWS Aurora, AWS RDS, or a local MySQL instance to TiDB Cloud using Migration Jobs.
---

# Migrate MySQL-Compatible Databases to TiDB Cloud Using Migration Jobs

This document describes how to use Migration Jobs (MJ) to migrate data from a MySQL-compatible database on a cloud provider (AWS Aurora or AWS RDS) or on-premises to TiDB Cloud.

TiDB Cloud provides the Migration Jobs feature. It supports full migration and incremental migration, allowing you to migrate your business to TiDB Cloud within a short downtime window.

The Migration Jobs feature supports data migration within the same region and cross regions.

## Limitations

- Currently, the Migration Jobs feature is still in public beta and each organization can create only one migration job. To use the feature, you need to [file a ticket](/tidb-cloud/tidb-cloud-support.md).

- The system databases will be filtered out and not be migrated to TiDB Cloud even if you select all of the databases to migrate, that is, `mysql`, `information_schema`, `information_schema` and `sys`.

- The Migration Jobs feature is only available to clusters created in the `us-west-2` region after November 9, 2022. It means that the **Migration Job** tab will not be displayed in old clusters or clusters in other regions.

- If the table to migrate already exists in the target database, TiDB Cloud appends the data to the target table directly. If the keys conflict, an error is reported.

- When you delete a cluster, all migration jobs in that cluster are automatically deleted, and the deleted migration jobs are not recoverable.

- During incremental replication, if the migration job recovers from an error, it will enable safe mode. In this mode, the migration job applies the binlog which is up to 60 seconds before the breakpoint to the target database. But it changes `INSERT` to `REPLACE`, changes `UPDATE` to `DELETE` and `REPLACE`, and then applies these transactions to the downstream cluster to make sure all the data during the breakpoint has been migrated to the donwnstream cluster. When the table does not have primary keys or not-null unique indexes, it is possible that some data is duplicated due to being inserted repeatedly.

## Prerequisites

Before performing the migration, you need to check the data sources, prepare privileges for upstream and downstream databases, and set up network connection.

### Supported data sources and versions

The Migration Jobs feature supports the following data sources and versions:

- MySQL 5.6, 5.7, and 8.0 local instances or on a public cloud provider. Note that MySQL 8.0 is still experimental and might have incompatibility issues.
- AWS Aurora MySQL 5.6 and 5.7
- AWS RDS MySQL 5.7

### Privileges for the upstream database

The username for the upstream database must have all the following privileges:

| Privilege | Scope |
|:----|:----|
| `SELECT` | Tables |
| `RELOAD` | Global |
| `REPLICATION SLAVE` | Global |
| `REPLICATION CLIENT` | Global |

For example, you can execute the following `GRANT` statement to grant corresponding privileges:

```sql
GRANT SELECT,RELOAD,REPLICATION SLAVE,REPLICATION CLIENT,LOCK TABLES,PROCESS ON *.* TO 'your_user'@'your_IP_address_of_host'
```

### Privileges for the downstream TiDB Cloud cluster

The username you use for the downstream TiDB Cloud cluster must have the following privileges:

| Privilege | Scope |
|:----|:----|
| `CREATE` | Databases, Tables |
| `SELECT` | Tables |
| `INSERT` | Tables |
| `UPDATE` | Tables |
| `DELETE` | Tables |
| `ALTER`  | Tables |
| `DROP`   | Databases，Tables |
| `INDEX`  | Tables |

For example, you can execute the following `GRANT` statement to grant corresponding privileges:

```sql
GRANT CREATE,SELECT,INSERT,UPDATE,DELETE,ALTER,DROP,INDEX ON *.* TO 'your_user'@'your_IP_address_of_host'
```

If you want to quickly migrate the data, you can use the `root` account of the TiDB Cloud cluster to test the migration job quickly.

### Set up network connection

If you use Public IP as the connection type, you need to ensure that the upstream and downstream databases can be connected through the public network.

If you use VPC Peering, you need to set it up in advance. See [Add VPC peering requests](/tidb-cloud/set-up-vpc-peering-connections.md#step-1-add-vpc-peering-requests).

If you use Private Link, you need to set it up in advance. See [Set Up Private Endpoint Connections](/tidb-cloud/set-up-private-endpoint-connections.md).

### Binlog

If you perform incremental data migration, make sure you have enabled binlog, and the binlogs have been kept for more than 24 hours.

## Step 1: Go to the **Data Migration** page

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters). Navigate to the **Clusters** page for your project.

2. On the **Clusters** page, click the name of your cluster, and click the **Data Migration** tab. The **Data Migration** page is displayed.

3. On the **Data Migration** page, click **Create Migration Job**. The **Create Migration Job** page is displayed.

## Step 2: Configure the source and target connection

On the **Create Migration Job** page, configure the source and target connection.

1. Input a job name. It must start with a letter, and can consist of letters (A-Z, a-z), numbers (0-9), underscores (_) and hyphens (-) with less than 60 characters.

2. Fill in the source connection profile.

   - **Data source**: the data source type.
   - **Region**: the region of the data source, which is required for cloud databases only.
   - **Connectivity method**: the connectivity method for the data source. Currently, public IP, VPC Peering, or Private Private Link is supported.
   - **Hostname or IP address** (for Public IP and VPC Peering): the hostname or IP address of the data source.
   - **Service Name** (for Private Link): the endpoint service name.
   - **Port**: the port of the data source.
   - **Username**: the username of the data source.
   - **Password**: the password of the username.
   - **SSL/TLS**: whether to use SSL/TLS connection for the data source. If you enable SSL/TLS, you need to upload the certificates of the data source, including the CA certificate, client certificate, and client key.

3. Fill in the target connection profile.

   - **Username**: enter the username of the target cluster in TiDB Cloud.
   - **Password**: enter the password of the TiDB Cloud username.

4. Click **Validate Connection and Next** to validate the information you have entered.

5. Take action according to the message you see:

    - If you use Public IP or  VPC Peering, you are prompted to add Data Migration service's IP addresses to the IP Access List of your source database and firewall (if any) to allow the Data Migration service to access your source database.
    - If you use Private Link, you are prompted to accept the endpoint request in your account.

## Step 3: Choose the objects to be migrated

1. You can choose to perform full data migration, incremental data migration, or both. If you want to migrate data to TiDB Cloud and switch to TiDB Cloud from now on, it is recommended to select both full data migration and incremental data migration to ensure data consistency between the source and target databases. If you only select the full data migration checkbox, the migration job only migrates the existing data of the source database.

2. On the **Choose Objects to Migrate** page, select the objects to be migrated. You can click **All** to select all objects, or click **Customize** and then click the checkbox next to the object name to select the object.

    - If you click **All**, the migration job will migrate the existing data and replicate ongoing changes made after the full migration from the whole source database instance to TiDB Cloud.

    ![Select All Objects](/media/tidb-cloud/migration-job-select-all.png)

    - If you click **Customize** and select some databases, the migration job will migrate the existing data and replicate ongoing changes of the selected databases to TiDB Cloud.

    ![Select Databases](/media/tidb-cloud/migration-job-select-db.png)

    - If you click **Customize** and select some tables below a dabaset name, the migration job only will migrate the existing data and replicate ongoing changes of the selected tables. It will not migrate the tables that will be created in the same database in future.

    ![Select Tables](/media/tidb-cloud/migration-job-select-tables.png)

    - If you click **Customize** and select some databases, and then select some tables in the **Selected Objects** area to move them back to the **Source Database** area, (for example the `username` table in the following screenshots), then the tables will be treated as in a blocklist. The migration job will migrate the existing data but filter out the filtered out tables (such as the `username` table in the screenshots), and will replicate ongoing changes of the selected databases to TiDB Cloud except the filtered out tables.

    ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist1.jpg)

    ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist2.jpg)

3. Click **Next**.

## Step 4: Precheck

On the **Precheck** page, you can view the precheck results. If the precheck fails, you need to operate according to **Failed** or **Warning** details, and then click **Check again** to recheck.

If there are no failed check items, but only some warning items, you can evaluate the risk and ignore the warning items. If all warning items are ignored, the migration job will automatically go to the next step.

For more information about precheck items, see [Migration Task Precheck](https://docs.pingcap.com/tidb/stable/dm-precheck).

If all check items show **Pass**, click **Next**.

## Step 5: Choose a spec and start migration

On the **Choose a Spec and Start Migration** page, select the migration spec. During the public beta, the free migration job is limited to 3 TCUs.

After selecting the spec, click **Create Job and Start** to start the migration.

## Step 6: View the migration progress

After the migration job is created, you can view the migration progress on the **Migration Job Details** page. The migration progress is displayed in the **Stage and Status** area.

You can pause or delete a migration job when it is running. You can delete a migration job in any status.
