---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Migration Jobs
summary: Learn how to use migration jobs to migrate AWS Aurora, AWS RDS and MySQL hosted on a public cloud or on-premises to TiDB Cloud.
---

# Migrate MySQL-Compatible Databases to TiDB Cloud Using Migration Jobs

This document describes how to use a migration job to migrate on cloud or on-premises data to TiDB Cloud.

You can import data in CSV, Parquet, SQL, and Aurora Snapshot formats to TiDB Cloud, as described in [Migration Overview](/tidb-cloud/tidb-cloud-migration-overview.md). Many of these scenarios are offline data import scenarios. When importing such data, to ensure the consistency of upstream and downstream data, you need to stop the upstream business, then export the offline files from the database, and then import the data to TiDB Cloud. It will bring a long downtime to the business, which is unacceptable in some cases.

To solve this problem, TiDB Cloud provides the migration job feature, which supports full migration and incremental migration, allowing you to migrate your business from the upstream database to TiDB Cloud within a short downtime window.

A migration job supports the following data sources:

- MySQL 5.6-8.0 on premises or on a cloud. Note that MySQL 8.0 is still experimental and might have incompatible issues.
- AWS Aurora MySQL 5.6 and 5.7
- AWS RDS MySQL 5.7

A migration job supports the following network types:

- Public IP
- VPC Peering
- Private Link

A migration job supports data migration within the same region and cross regions.

## Limitations

- The system databases including `mysql`, `information_schema`, `information_schema` and `sys` will be filtered out during migration (even when you migrate the entire upstream MySQL instance), and will not be migrated to TiDB Cloud.

- Currently the migration job feature is only deployed on the us-west-2 region and the EKS provider, which means that the **Migration Job** tab will not be displayed in old clusters created on AWS.

- If the table to migrated already exists in the target database, TiDB Cloud appends the data to the target table directly. If the keys conflict, it will report an error.

- When you delete a cluster, all migration jobs in that cluster are automatically deleted, and the deleted migration jobs are not recoverable.

- Currently the migration job feature is still in public beta. During public beta, each account can create one migration job.

## Prerequisites

### Privileges for the upstream database

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
GRANT RELOAD, REPLICATION SLAVE, REPLICATION CLIENT, PROCESS ON *.* TO 'your_user'@'your_wildcard_of_host'
GRANT SELECT ON db1.* TO 'your_user'@'your_wildcard_of_host';
```

If you also need to migrate the data from other databases to TiDB Cloud, make sure the same privileges are granted to the user of the respective databases.

### Set up VPC Peering

If you use VPC Peering, you need to set it up in advance. See [Add VPC peering requests](/tidb-cloud/set-up-vpc-peering-connections.md#step-1-add-vpc-peering-requests)

## Step 1: Go to the **Data Migration** page

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters). Navigate to the **Clusters** page for your project.

2. On the **Clusters** page, click the name of your cluster, and click the **Data Migration** tab. The **Data Migration** page is displayed.

3. On the **Data Migration** page, click **Create Migration Job**. The **Create Migration Job** page is displayed.

## Step 2: Configure the source and target connection

On the **Create Migration Job** page, configure the source and target connection.

1. Create a job name. It must start with a letter, and can consist of letters (A-Z, a-z), numbers (0-9), underscores (_) and hyphens (-) with less than 60 characters.

2. Fill in the source connection profile.

   - **Data source**: the data source type. Currently, it supports MySQL, AWS Aurora MySQL, and AWS RDS MySQL.
   - **Region**: the region of the data source. If the source database is self-built, the parameter is optional.
   - **Connectivity method**: the connectivity method of the data source. Currently, it supports Public IP, VPC Peering and Private Link.
   - **Hostname or IP address** (for Public IP): the hostname or IP address of the data source.
   - **Service Name** (for Private Link and VPC Peering): the endpoint service name.
   - **Port**: the port of the data source.
   - **Username**: the username of the data source.
   - **Password**: the password of the username.
   - **SSL/TLS**: enable or disable the SSL/TLS configuration of the data source. If you enable SSL/TLS, you need to upload the certificate of the data source, including the CA certificate, client certificate, and client key.

3. Fill in the target connection profile.

   - **Username**: enter the username of the target cluster.
   - **Password**: enter the password of username.

4. Click **Validate Connection and Next** to validate the information you have entered.

5. A message is displayed.

    - If you use Public IP or  VPC Peering, you are prompted to add Data Migration service's IP addresses to the IP Access List of your source database and firewall (if any) to allow the Data Migration service to access your source database.
    - If you use Private Link, you are prompted to accept the endpoint request in your account.

## Step 3: Choose the objects to be migrated

1. You can choose to perform full data migration, incremental data migration, or both. If you want to migrate data to TiDB Cloud and switch to TiDB Cloud from now on, it is recommended to select both full data migration and incremental data migration to ensure data consistency between the source and target databases. If you only select the full data migration checkbox, the migration job only migrates the existing data of the source database.

2. On the **Choose Objects to Migrate** page, select the objects to be migrated. You can click **All** to select all objects, or click **Customize** and then click the checkbox next to the object name to select the object.

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
