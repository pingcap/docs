---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: Learn how to migrate data from MySQL-compatible databases hosted in Amazon Aurora MySQL, Amazon Relational Database Service (RDS), or a local MySQL instance to TiDB Cloud using Data Migration.
---

# Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration

This document describes how to migrate data from a MySQL-compatible database on a cloud provider (Amazon Aurora MySQL or Amazon Relational Database Service (RDS)) or on-premises to TiDB Cloud using the Data Migration feature of the TiDB Cloud console.

This feature helps you migrate your database and its ongoing changes to TiDB Cloud (either in the same region or cross regions). Compared with solutions that require tools such as Dumpling and TiDB Lightning, this feature is easier to use. You do not need to manually dump data from the source database and then import it to TiDB Cloud. Instead, you can migrate data directly from the source database to TiDB Cloud in one go.

## Limitations

- The Data Migration feature is available only for **Dedicated Tier** clusters.

- The Data Migration feature is only available to clusters in the projects that are created in the following regions after November 9, 2022. If your **project** was created before the date or if your cluster is in another region, this feature is not available to your cluster and the **Data Migration** tab will not be displayed on the cluster overview page in the TiDB Cloud console.

    - AWS Oregon (us-west-2)
    - AWS N. Virginia (us-east-1)
    - AWS Mumbai (ap-south-1)
    - AWS Singapore (ap-southeast-1)
    - AWS Tokyo (ap-northeast-1)
    - AWS Frankfurt (eu-central-1)
    - AWS Seoul (ap-northeast-2)
- You can create up to 200 migration jobs for each organization. To create more migration jobs, you need to [file a support ticket](/tidb-cloud/tidb-cloud-support.md).

- The system databases will be filtered out and not migrated to TiDB Cloud even if you select all of the databases to migrate. That is, `mysql`, `information_schema`, `information_schema`, and `sys` will not be migrated using this feature.

- During full data migration, if the table to be migrated already exists in the target database with duplicated keys, the duplicate keys will be replaced.

- During incremental data migration, if the table to be migrated already exists in the target database with duplicated keys, an error is reported and the migration is interrupted. In this situation, you need to make sure whether the upstream data is accurate. If yes, click the "Restart" button of the migration job and the migration job will replace the downstream conflicting records with the upstream records.

- When you delete a cluster in TiDB Cloud, all migration jobs in that cluster are automatically deleted and not recoverable.

- During incremental replication (migrating ongoing changes to your cluster), if the migration job recovers from an abrupt error, it might open the safe mode for 60 seconds. During the safe mode, `INSERT` statements are replicated as `REPLACE`, `UPDATE` statements as `DELETE` and `REPLACE`, and then these transactions are replicated to the downstream cluster to make sure that all the data during the abrupt error has been migrated smoothly to the downstream cluster. For upstream tables without primary keys or not-null unique indexes, some data might be duplicated in the downstream cluster because the data might be inserted repeatedly to the downstream.

- When you use Data Migration, it is recommended to keep the size of your dataset smaller than 1 TiB. If the dataset size is larger than 1 TiB, the full data migration will take a long time due to limited specifications.

- In the following scenarios, if the migration job takes longer than 24 hours, do not purge binlogs in the source database to ensure that Data Migration can get consecutive binlogs for incremental replication:

    - During full data migration.
    - After the full data migration is completed and when incremental data migration is started for the first time, the latency is not 0ms.

## Prerequisites

Before performing the migration, you need to check the data sources, prepare privileges for upstream and downstream databases, and set up network connections.

### Make sure your data source and version are supported

Data Migration supports the following data sources and versions:

- MySQL 5.6, 5.7, and 8.0 local instances or on a public cloud provider. Note that MySQL 8.0 is still experimental on TiDB Cloud and might have incompatibility issues.
- Amazon Aurora (MySQL 5.6 and 5.7)
- Amazon RDS (MySQL 5.7)

### Grant required privileges to the upstream database

The username you use for the upstream database must have all the following privileges:

| Privilege | Scope |
|:----|:----|
| `SELECT` | Tables |
| `LOCK` | Tables |
| `REPLICATION SLAVE` | Global |
| `REPLICATION CLIENT` | Global |

For example, you can use the following `GRANT` statement to grant corresponding privileges:

```sql
GRANT SELECT,LOCK TABLES,REPLICATION SLAVE,REPLICATION CLIENT ON *.* TO 'your_user'@'your_IP_address_of_host'
```

### Grant required privileges to the downstream TiDB Cloud cluster

The username you use for the downstream TiDB Cloud cluster must have the following privileges:

| Privilege | Scope |
|:----|:----|
| `CREATE` | Databases, Tables |
| `SELECT` | Tables |
| `INSERT` | Tables |
| `UPDATE` | Tables |
| `DELETE` | Tables |
| `ALTER`  | Tables |
| `DROP`   | Databases, Tables |
| `INDEX`  | Tables |
| `TRUNCATE`  | Tables |

For example, you can execute the following `GRANT` statement to grant corresponding privileges:

```sql
GRANT CREATE,SELECT,INSERT,UPDATE,DELETE,ALTER,TRUNCATE,DROP,INDEX ON *.* TO 'your_user'@'your_IP_address_of_host'
```

To quickly test a migration job, you can use the `root` account of the TiDB Cloud cluster.

### Set up network connection

Before creating a migration job, set up the network connection according to your connection methods. See [Connect to Your TiDB Cluster](/tidb-cloud/connect-to-tidb-cluster.md).

- If you use public IP (this is, standard connection) for network connection, make sure that the upstream database can be connected through the public network.

- If you use AWS PrivateLink, set it up according to [Set Up Private Endpoint Connections](/tidb-cloud/set-up-private-endpoint-connections.md).

- If you use VPC Peering, see the following instructions to configure the network.

<details>
<summary> Set up VPC Peering</summary>

Make sure that your TiDB Cluster can connect to the MySQL service.

If your MySQL service is in an AWS VPC that has no public internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.
2. Modify the inbound rules of the security group that the MySQL service is associated with. 

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr) to the inbound rules. Doing so allows the traffic to flow from your TiDB Cluster to the MySQL instance.

3. If the MySQL URL contains a hostname, you need to allow TiDB Cloud to be able to resolve the DNS hostname of the MySQL service. 

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

If your MySQL service is in a GCP VPC that has no public internet access, take the following steps:

1. If your MySQL service is Google Cloud SQL, you must expose a MySQL endpoint in the associated VPC of the Google Cloud SQL instance. You may need to use the [**Cloud SQL Auth proxy**](https://cloud.google.com/sql/docs/mysql/sql-proxy) which is developed by Google.
2. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster. 
3. Modify the ingress firewall rules of the VPC where MySQL is located.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr) to the ingress firewall rules. Doing so allows the traffic to flow from your TiDB Cluster to the MySQL endpoint. 

</details>

### Enable binlogs

To perform incremental data migration, make sure you have enabled binlogs of the upstream database, and the binlogs have been kept for more than 24 hours.

## Step 1: Go to the **Data Migration** page

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can switch to the target project in the left navigation pane of the **Clusters** page.

2. Click the name of your target cluster to go to its overview page, and then click **Data Migration** in the left navigation pane.

3. On the **Data Migration** page, click **Create Migration Job** in the upper-right corner. The **Create Migration Job** page is displayed.

## Step 2: Configure the source and target connection

On the **Create Migration Job** page, configure the source and target connection.

1. Enter a job name, which must start with a letter and must be less than 60 characters. Letters (A-Z, a-z), numbers (0-9), underscores (_), and hyphens (-) are acceptable.

2. Fill in the source connection profile.

   - **Data source**: the data source type.
   - **Region**: the region of the data source, which is required for cloud databases only.
   - **Connectivity method**: the connection method for the data source. Currently, you can choose public IP, VPC Peering, or Private Link according to your connection method.
   - **Hostname or IP address** (for public IP and VPC Peering): the hostname or IP address of the data source.
   - **Service Name** (for Private Link): the endpoint service name.
   - **Port**: the port of the data source.
   - **Username**: the username of the data source.
   - **Password**: the password of the username.
   - **SSL/TLS**: if you enable SSL/TLS, you need to upload the certificates of the data source, including any of the following:
        - only the CA certificate
        - the client certificate and client key
        - the CA certificate, client certificate and client key

3. Fill in the target connection profile.

   - **Username**: enter the username of the target cluster in TiDB Cloud.
   - **Password**: enter the password of the TiDB Cloud username.

4. Click **Validate Connection and Next** to validate the information you have entered.

5. Take action according to the message you see:

    - If you use Public IP or VPC Peering, you need to add the Data Migration service's IP addresses to the IP Access List of your source database and firewall (if any).
    - If you use Private Link, you are prompted to accept the endpoint request. Go to the [AWS VPC console](https://us-west-2.console.aws.amazon.com/vpc/home), and click **Endpoint services** to accept the endpoint request.

## Step 3: Choose the objects to be migrated

1. Choose full data migration, incremental data migration, or both by choosing the checkboxes.

    > **Tip:**
    >
    > - To migrate data to TiDB Cloud once and for all, choose both **Full data migration** and **Incremental data migration**, which ensures data consistency between the source and target databases.
    > - To migrate only the existing data of the source database to TiDB Cloud, only choose the **Full data migration** checkbox.

2. On the **Choose Objects to Migrate** page, select the objects to be migrated. You can click **All** to select all objects, or click **Customize** and then click the checkbox next to the object name to select the object.

    - If you click **All**, the migration job will migrate the existing data from the whole source database instance to TiDB Cloud and replicate ongoing changes after the full migration. Note that it happens only if you have selected the **Full data migration** and **Incremental data migration** checkboxes in the previous step.

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-all.png" width="60%" />

    - If you click **Customize** and select some databases, the migration job will migrate the existing data and replicate ongoing changes of the selected databases to TiDB Cloud. Note that it happens only if you have selected the **Full data migration** and **Incremental data migration** checkboxes in the previous step.

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-db.png" width="60%" />

    - If you click **Customize** and select some tables under a dataset name, the migration job only will migrate the existing data and replicate ongoing changes of the selected tables. Tables created afterwards in the same database will not be migrated.

        <img src="https://download.pingcap.com/images/docs/tidb-cloud/migration-job-select-tables.png" width="60%" />

    <!--
    - If you click **Customize** and select some databases, and then select some tables in the **Selected Objects** area to move them back to the **Source Database** area, (for example the `username` table in the following screenshots), then the tables will be treated as in a blocklist. The migration job will migrate the existing data but filter out the excluded tables (such as the `username` table in the screenshots), and will replicate ongoing changes of the selected databases to TiDB Cloud except the filtered-out tables.
        ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist1.png)
        ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist2.png)
    -->

3. Click **Next**.

## Step 4: Precheck

On the **Precheck** page, you can view the precheck results. If the precheck fails, you need to operate according to **Failed** or **Warning** details, and then click **Check again** to recheck.

If there are only warnings on some check items, you can evaluate the risk and consider whether to ignore the warnings. If all warnings are ignored, the migration job will automatically go on to the next step.

For more information about warning and solutions, see [Precheck warnings and solutions](#precheck-warnings-and-solutions).

For more information about precheck items, see [Migration Task Precheck](https://docs.pingcap.com/tidb/stable/dm-precheck).

If all check items show **Pass**, click **Next**.

## Step 5: Choose a spec and start migration

On the **Choose a Spec and Start Migration** page, select an appropriate migration specification according to your performance requirements. For more information about the specifications, see [Specifications for Data Migration](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration).

After selecting the spec, click **Create Job and Start** to start the migration.

## Step 6: View the migration progress

After the migration job is created, you can view the migration progress on the **Migration Job Details** page. The migration progress is displayed in the **Stage and Status** area.

You can pause or delete a migration job when it is running.

If a migration job has failed, you can restart it after solving the problem.

You can delete a migration job in any status.

## Subscribe alerts

You can subscribe alerts to be informed in time when an alert occurs. TiDB Cloud sends an email to the subscribers in the following scenarios: 

- A migration job fails or hangs for more than 20 minutes.
- A TiCDC Changefeed task fails or hangs for more than 10 minutes.

To subscribe an alert, do the following:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. In the left navigation pane of the [**Clusters**](https://tidbcloud.com/console/clusters) page, do one of the following:

    - If you have multiple projects, switch to the target project, and then click **Admin** > **Alerts**.
    - If you only have one project, click **Admin** > **Alerts**.

3. Enter your email address, and then click **Subscribe**.

For more information about alerts, see [TiDB Cloud Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md).

## Precheck warnings and solutions

This section describes the precheck warnings and corresponding solutions.

### Check whether mysql server_id has been greater than 0

- Amazon Aurora MySQL or Amazon RDS: `server_id` is configured by default. You do not need to configure it.
- MySQL: to configure `server_id` for MySQL, see [Setting the Replication Source Configuration](https://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html).

### Check whether mysql binlog is enabled

- Amazon Aurora MySQL: see [How do I turn on binary logging for my Amazon Aurora MySQL-Compatible cluster?](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls).
- Amazon RDS: see [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).
- MySQL: see [Setting the Replication Source Configuration](https://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html).

### Check whether mysql binlog_format is ROW

- Amazon Aurora MySQL: see [How do I turn on binary logging for my Amazon Aurora MySQL-Compatible cluster?](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls).
- Amazon RDS: see [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).
- MySQL: execute 'set global binlog_format=ROW;'. See [Setting The Binary Log Format](https://dev.mysql.com/doc/refman/5.7/en/binary-log-setting.html)

### Check whether mysql binlog_row_image is FULL

- Amazon Aurora MySQL: `binlog_row_image` is not configurable.
- Amazon RDS: the process is similar to setting the `binlog_format`. The only difference is that the parameter you change is `binlog_row_image` instead of `binlog_format`. See [Configuring MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).
- MySQL:'set global binlog_row_image = FULL;'. See [Binary Logging Options and Variables](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_binlog_row_image).

### Check whether migrated dbs are in binlog_do_db/binlog_ignore_db

Make sure that binlog has been enabled in the upstream database. Then resolve the issue according to the messages:

- If the message is similar to `These dbs xxx are not in binlog_do_db xxx`, make sure all the databases that you want to migrate are in the list. See [--binlog-do-db=db_name](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#option_mysqld_binlog-do-db).
- If the message is similar to `these dbs xxx are in binlog_ignore_db xxx`, make sure all the databases that you want to migrate are not in the ignore list. See [--binlog-ignore-db=db_name](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#option_mysqld_binlog-ignore-db).

### Check if connetion concurrency exceeds database's maximum connection limit

If the error occurs in the upstream MySQL database, configure `max_connections` following the document [max_connections](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_max_connections).

If the error occurs in the TiDB Cloud cluster, configure `max_connections` following the document [max_connections](https://docs.pingcap.com/tidb/stable/system-variables#max_connections).

## Troubleshooting

If you encounter any problems during the migration, you can refer to the following solutions.

- Error message: "The required binary log for migration no longer exists on the source database. Please make sure binary log files are kept for long enough time for migration to succeed."

    This error means that the binlogs to be migrated has been cleaned up and can only be restored by creating a new task.

    Ensure that the binlogs required for incremental migration exist. It is recommended to configure `expire_logs_days` to extend the duration of binlogs. Do not use `purge binary log` to clean up binlogs if it's needed by some migration job.

- Error message: "Failed to connect to the source database using given parameters. Please make sure the source database is up and can be connected using the given parameters."

    This error means that the connection to the source database failed. Check whether the source database is started and can be connected to using the specified parameters. After confirming that the source database is available, you can try to recover the task by clicking **Restart**.

- The migration task is interrupted and contains the error "driver: bad connection" or "invalid connection"

    This error means that the connection to the downstream TiDB cluster failed. Check whether the downstream TiDB cluster is in `normal` state and can be connected with the username and password specified by the job. After confirming that the downstream TiDB cluster is available, you can try to resume the task by clicking **Restart**.

- Error message: "Failed to connect to the TiDB cluster using the given user and password. Please make sure TiDB Cluster is up and can be connected to using the given user and password."

    Failed to connect to TiDB cluster. It is recommended to check whether the TiDB cluster is in `normal` state and you can connect with the username and password specified by the job. After confirming that the TiDB cluster is available, you can try to resume the task by clicking **Restart**.

- Error message: "TiDB cluster storage is not enough. Please increase the node storage of TiKV."

    The TiDB cluster storage is running low. It is recommended to [increase the TiKV node storage](/tidb-cloud/scale-tidb-cluster.md#increase-node-storage) and then resume the task by clicking **Restart**.

- Error message: "Failed to connect to the source database. Please check whether the database is available or the maximum connections have been reached."

    Failed to connect to the source database. It is recommended to check whether the source database is started, the number of database connections has not reached the upper limit, and you can connect using the parameters specified by the job. After confirming that the source database is available, you can try to resume the job by clicking **Restart**.
