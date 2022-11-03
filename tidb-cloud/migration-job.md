---
title: Migrate Data Using Migration Jobs
summary: Learn how to create migration jobs to migrate data into TiDB Cloud.
---

# Migrate Data Using Migration Jobs

This document describes how to create a migration job to migrate data into TiDB Cloud.

You can import data in CSV, Parquet, SQL, and Aurora Snapshot formats to TiDB Cloud. All these scenarios are offline data import scenarios. When importing these data, to ensure the consistency of upstream and downstream data, you need to stop the upstream business, then export the offline files from the database, and then import the data to TiDB Cloud, it will bring a long downtime to the business, which is unacceptable in some cases.

To solve this problem, TiDB Cloud provides the Migration Job feature, which supports full migration incremental migration, allowing you to migrate your business from the upstream database to TiDB Cloud within a short downtime window.

## Supported network types and data sources

A migration job supports the following network types:

- Public IP
- VPC peering
- Private Link

A migration job supports the following data sources:

- MySQL 5.6-8.0 on premises or on a cloud
- AWS Aurora MySQL 5.6 and 5.7
- AWS RDS MySQL 5.7 and 8.0
- Google Cloud MySQL 5.6, 5.7 and 8.0

A migration job supports data migration within the same region and cross regions.

Note that the system databases of `mysql`, `information_schema`, `information_schema` and `sys` will be filtered out during migration (even when you migrate the entire upstream MySQL instance), and will not be migrated to TiDB Cloud.

## Prerequisites

The username you use for the upstream database must have the following privileges:

| Privilege | Scope |
|:----|:----|
| `SELECT` | Tables |
| `RELOAD` | Global |
| `REPLICATION SLAVE` | Global |
| `REPLICATION CLIENT` | Global |
| `PROCESS` | Global |

For example, if you need to migrate the data from `db1` to TiDB Cloud, execute the following `GRANT` statement:

```sql
GRANT RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'your_user'@'your_wildcard_of_host'
GRANT SELECT ON db1.* TO 'your_user'@'your_wildcard_of_host';
```

If you also need to migrate the data from other databases into TiDB Cloud, make sure the same privileges are granted to the user of the respective databases.

## Step 1: Create a migration job

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters). Navigate to the **Clusters** page for your project.

2. Locate your target cluster, click **...** in the upper-right corner of the cluster area, and select **Data Migration**. The **Data Migration** page is displayed.

   Alternatively, you can also click the name of your cluster on the **Clusters** page and click **Data Migration** in the **Data Migration** area.

3. On the **Data Migration** page, click **Create Migration Job**. The **Create Migration Job** page is displayed.

## Step 1: Config source and target connection

On the **Create Migration Job** page, configure the source and target connection.

1. Create a job name. It must onsist of numbers and letters with less than 60 characters.

2. Fill in the source connection profile.

   - **Data source**: the data source type. Currently, it supports MySQL, AWS Aurora MySQL, AWS RDS MySQL and Google Cloud MySQL.
   - **Region**: the region of the data source. If the source database is a self-built, the parameter is empty.
   - **Connectivity method**: the connectivity method of the data source. Currently, it supports Public IP, VPC peering, and Private Link.
   - **Endpoint service name**: the hostname or IP address of the data source.
   - **Port**: the port of the data source.
   - **Username**: the username of the data source.
   - **Password**: the password of the data source.
   - **SSL/TLS** (Only for Public IP): enable or disable the SSL/TLS configuration of the data source. If you enable SSL/TLS, you need to upload the certificate of the data source, including the CA certificate, client certificate, and client key.

3. Fill in the target connection profile.

   - **Username**: enter the username of the target cluster.
   - **Password**: enter the password of the target cluster.

4. Click **Validate Connection and Next** to validate the information you have entered.

## Step 2: Choose the objects to be migrated

1. On the **Choose Objects to Migrate** page, select the objects to be migrated. You can click **All** to select all objects, or click **Customize** and then click the checkbox next to the object name to select the object.

2. Click **Next**.

## Step 3: Precheck

On the **Precheck** page, you can view the precheck results. If the precheck fails, you need to operate according to **Failed** or **Warning** details, and then click **Check again** to recheck.

If all check items show **Pass**, click **Next**.

## Step 4: Choose a spec and start migration

On the **Choose a Spec and Start Migration** page, select the migration spec. The migration spec determines the number of nodes and the number of CPU cores and memory of each node. Different specs have different migration performance and cost. The cost is shown at the bottom of the page. You can select the appropriate spec according to your business needs. For more information, see [TiDB Cloud Pricing](https://www.pingcap.com/tidb-cloud-pricing-details/).

After selecting the spec, click **Create Job and Start** to start the migration.

## Step 5: View the migration progress

After the migration job is created, you can view the migration progress on the **Migration Job Details** page. The migration progress is displayed in the **State and Status** area.
