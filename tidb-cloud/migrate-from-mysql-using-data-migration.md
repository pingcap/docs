---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: Learn how to seamlessly migrate your MySQL databases from Amazon Aurora MySQL, Amazon RDS, Azure Database for MySQL flexible servers, Google Cloud SQL for MySQL, or self-managed MySQL instances to TiDB Cloud with minimal downtime using the Data Migration feature.
aliases: ['/tidbcloud/migrate-data-into-tidb','/tidbcloud/migrate-incremental-data-from-mysql']
---

# Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration

This document guides you through migrating your MySQL databases from Amazon Aurora MySQL, Amazon RDS, Azure Database for MySQL flexible servers, Google Cloud SQL for MySQL, or self-managed MySQL instances to TiDB Cloud using the Data Migration feature in the console.

This feature enables you to migrate both your existing MySQL data and replicate ongoing changes (binlog) from your MySQL source databases directly to TiDB Cloud, maintaining consistency whether in the same region or across different regions. The streamlined process eliminates the need for separate dump and load operations, reducing downtime and simplifying your migration from MySQL to a more scalable platform.

If you only want to replicate ongoing binlog changes from your MySQL database to TiDB Cloud, see [Migrate Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md).

## Limitations

### Availability

- The Data Migration feature is available only for **TiDB Cloud Dedicated** clusters.

- The Data Migration feature is only available to clusters that are created in [certain regions](https://www.pingcap.com/tidb-cloud-pricing-details/#dm-cost) after November 9, 2022. If your **project** was created before the date or if your cluster is in another region, this feature is not available to your cluster and the **Data Migration** tab will not be displayed on the cluster overview page in the TiDB Cloud console.

- Amazon Aurora MySQL writer instances support both existing data and incremental data migration. Amazon Aurora MySQL reader instances only support existing data migration and do not support incremental data migration.

### Maximum number of migration jobs

You can create up to 200 migration jobs for each organization. To create more migration jobs, you need to [file a support ticket](/tidb-cloud/tidb-cloud-support.md).

### Filtered out and deleted databases

- The system databases will be filtered out and not migrated to TiDB Cloud even if you select all of the databases to migrate. That is, `mysql`, `information_schema`, `information_schema`, and `sys` will not be migrated using this feature.

- When you delete a cluster in TiDB Cloud, all migration jobs in that cluster are automatically deleted and not recoverable.

### Limitations of existing data migration

- During existing data migration, if the table to be migrated already exists in the target database with duplicated keys, the duplicate keys will be replaced.

- If your dataset size is smaller than 1 TiB, it is recommended that you use logical mode (the default mode). If your dataset size is larger than 1 TiB, or you want to migrate existing data faster, you can use physical mode. For more information, see [Migrate existing data and incremental data](#migrate-existing-data-and-incremental-data).

### Limitations of incremental data migration

- During incremental data migration, if the table to be migrated already exists in the target database with duplicated keys, an error is reported and the migration is interrupted. In this situation, you need to make sure whether the MySQL source data is accurate. If yes, click the "Restart" button of the migration job and the migration job will replace the target TiDB Cloud cluster conflicting records with the MySQL source records.

- During incremental replication (migrating ongoing changes to your cluster), if the migration job recovers from an abrupt error, it might open the safe mode for 60 seconds. During the safe mode, `INSERT` statements are migrated as `REPLACE`, `UPDATE` statements as `DELETE` and `REPLACE`, and then these transactions are migrated to the target TiDB Cloud cluster to make sure that all the data during the abrupt error has been migrated smoothly to the target TiDB Cloud cluster. In this scenario, for MySQL source tables without primary keys or not-null unique indexes, some data might be duplicated in the target TiDB Cloud cluster because the data might be inserted repeatedly to the target TiDB Cloud cluster.

- In the following scenarios, if the migration job takes longer than 24 hours, do not purge binary logs in the source database to ensure that Data Migration can get consecutive binary logs for incremental replication:

    - During existing data migration.
    - After the existing data migration is completed and when incremental data migration is started for the first time, the latency is not 0ms.

## Prerequisites

Before migrating, check supported data sources, set up network connections, and prepare privileges for the MySQL source and target TiDB Cloud cluster databases.

### Make sure your data source and version are supported

Data Migration supports the following data sources and versions:

- Self-managed MySQL instances MySQL 8.0, 5.7, and 5.6 local instances or on a public cloud provider. 
- Amazon Aurora MySQL (8.0, 5.7, and 5.6)
- Amazon RDS MySQL (8.0, and 5.7)
- Azure Database for MySQL flexible servers (8.0, and 5.7)
- Google Cloud SQL for MySQL (8.0, 5.7, and 5.6)

### Ensure network connectivity

Before creating a migration job, you need to plan and set up proper network connectivity between your source MySQL instance, TiDB Cloud DM (Data Migration) service, and your target TiDB Cloud cluster.

Your options are:

| Connectivity Pattern | Availability | Recommended for |
|:---------------------|:-------------|:----------------|
| Public Endpoints / IPs | All cloud providers | Quick proof-of-concept migrations, testing, or when private connectivity isn't available |
| Private Links / Endpoints | AWS and Azure only | Production workloads without exposing data to the public internet |
| VPC Peering | AWS and GCP only | Production workloads that need low-latency, intra-region connections and whose VPC/VNet CIDRs do not overlap |

Choose the connection method that best fits your security requirements, network topology, and cloud provider. Proceed with the setup for the chosen connectivity pattern.

#### End-to-end Encryption over TLS/SSL

In any case, TLS/SSL is highly recommended for end-to-end encryption. Private Link and VPC Peering protect the network path, but end‑to‑end encryption protects the data and satisfies compliance checks.

<details>
<summary> Download and store the provider's certificates for TLS/SSL encrypted connections </summary>

- [AWS RDS / Aurora using SSL/TLS to encrypt a connection to a DB instance or cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html)
- [Azure Database for MySQL Flexible Server - connect with encrypted connections](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-connect-tls-ssl)
- [GCP Cloud SQL - manage SSL/TLS certificates](https://cloud.google.com/sql/docs/mysql/manage-ssl-instance)

</details>

#### Public Endpoints / IPs

- If you use a Public Endpoint for your source MySQL database, get its IP address or Hostname (FQDN) and make sure that it can be connected through the public network. You may also need to configure firewall rules or security groups accordingly to your cloud provider guides.

- Identify and record the source MySQL instance endpoint hostname (FQDN) or public IP.  
- Add the TiDB Cloud DM egress IP range to the database's firewall/security‑group rules. See your provider’s docs for:
    - [AWS RDS / Aurora VPC security groups](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Overview.RDSSecurityGroups.html).
    - [Azure Database for MySQL Flexible Server Public Network Access](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-networking-public)
    - [Cloud SQL Authorized Networks](https://cloud.google.com/sql/docs/mysql/configure-ip#authorized-networks).
- Verify connectivity from your machine with public internet access using the certificates:

    ```shell
    mysql -h <public‑host> -P <port> -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

#### Private Link / Private Endpoint

If you use a provider-native Private Link, create a Private Endpoint for the source MySQL instance (RDS, Aurora, or Azure Database for MySQL). 

<details>
<summary> Set up AWS Private Link and Private Endpoint for the MySQL source database </summary>

Create a Network Load Balancer (NLB) and publish that NLB as an Endpoint Service associated with the source MySQL instance you want to migrate to TiDB Cloud. AWS doesn't expose RDS/Aurora directly through PrivateLink.

1. In the AWS web console, create an NLB in the same subnet(s) as your RDS/Aurora writer. Add a TCP listener on port `3306` that targets the DB instance endpoint.
2. Under VPC, Endpoint Services, create a service backed by the NLB and enable Require acceptance. Note the Service Name (format `com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx`).
3. Optionally, test connectivity from a bastion or client inside the same VPC/VNet before starting the migration: 

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. Later, when configuring TiDB Cloud DM to connect via PrivateLink, you will return to the AWS console to approve a Pending connection request from TiDB Cloud DM to this Private Endpoint. 

For detailed instructions, see [AWS guide to access VPC resources through PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-resources.html).

</details>

<details>
<summary> Set up Azure Private Link and Private Endpoint for the MySQL source database </summary>

Azure supports Private Endpoints natively on each MySQL Flexible Server instance. You can either create Private access (VNet Integration) during the MySQL instance creation or add a Private Endpoint later. To add a new Private Endpoint: 

1. In the Azure portal, open MySQL Flexible Server, Networking, Private Endpoints, and click on the "+ Create private endpoint" button.
2. Follow the wizard by selecting the VNet/subnet where TiDB Cloud can reach, keep Private DNS integration enabled, and finish the wizard. The hostname to be used to connect with the instance can be found under the Connect menu (typical format `<your-instance-name>.mysql.database.azure.com`).
3. Optionally, test connectivity from a bastion or client inside the same VPC/VNet before starting the migration:

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. Go back to the MySQL Flexible Server instance (not the private‑endpoint object), and note its resource ID. You can retrieve it in the MySQL Flexible Server instance JSON view (format `/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>`). You will use this resource ID (not the private endpoint) to configure TiDB Cloud DM.
5. Later, when configuring TiDB Cloud DM to connect via Private Link, you will return to the Azure portal to approve a Pending connection request from TiDB Cloud DM to this Private Endpoint. 

For detailed instructions, see [Azure guide to create a private endpoint via Private Link Center](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-networking-private-link-portal#create-a-private-endpoint-via-private-link-center)

</details>

- If you use AWS VPC Peering or Google Cloud VPC Network Peering, see the following instructions to configure the network.

<details>
<summary> Set up AWS VPC Peering</summary>

If your MySQL service is in an AWS VPC, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.

2. Modify the inbound rules of the security group that the MySQL service is associated with.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) to the inbound rules. Doing so allows the traffic to flow from your TiDB cluster to the MySQL instance.

3. If the MySQL URL contains a DNS hostname, you need to allow TiDB Cloud to be able to resolve the hostname of the MySQL service.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

</details>

<details>
<summary> Set up Google Cloud VPC Network Peering </summary>

If your MySQL service is in a Google Cloud VPC, take the following steps:

1. If it is a self-hosted MySQL, you can skip this step and proceed to the next step. If your MySQL service is Google Cloud SQL, you must expose a MySQL endpoint in the associated VPC of the Google Cloud SQL instance. You might need to use the [Cloud SQL Auth proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy) developed by Google.

2. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of your MySQL service and your TiDB cluster.

3. Modify the ingress firewall rules of the VPC where MySQL is located.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) to the ingress firewall rules. This allows the traffic to flow from your TiDB cluster to the MySQL endpoint.

</details>

### Grant required privileges in the source MySQL database

The username you use for migration in the source database must have all the following privileges:

| Privilege | Scope |
|:----|:----|
| `SELECT` | Tables |
| `LOCK` | Tables |
| `REPLICATION SLAVE` | Global |
| `REPLICATION CLIENT` | Global |

For example, you can use the following `GRANT` statement to grant corresponding privileges:

```sql
GRANT SELECT, LOCK TABLES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'your_user'@'your_IP_address_of_host'
```

### Grant required privileges in the target TiDB Cloud cluster

The username you use for the migration in the target TiDB Cloud cluster must have the following privileges:

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

For example, you can execute the following `GRANT` statement to grant corresponding privileges:

```sql
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE, ALTER, DROP, INDEX ON *.* TO 'your_user'@'your_IP_address_of_host'
```

To quickly test a migration job, you can use the `root` account of the TiDB Cloud cluster. The MySQL user hostname part also needs to allow connections from the TiDB Cloud DM service, and you can use `%` for simplification.

### Enable binary logs for replication

To enable replication from the source MySQL database to the TiDB Cloud target cluster using DM for continuously capturing incremental changes, you need these MySQL configurations:

| Configuration | Required value | Why |
|:--------------|:---------------|:----|
| `log_bin` | `ON` | Enables binary logging that DM reads to replay changes in TiDB |
| `binlog_format` | `ROW` | Captures all data changes accurately (other formats miss edge cases) |
| `binlog_row_image` | `FULL` | Includes all column values in events for safe conflict resolution |
| `binlog_expire_logs_seconds` | ≥ 86400 (1 day), 604800 (7 days) recommended | Ensures DM can access consecutive logs during migration |

#### Check current values and configure the source MySQL instance

To confirm the current configurations, connect to the source MySQL instance and run:

```sql
SHOW VARIABLES WHERE Variable_name IN 
('log_bin','server_id','binlog_format','binlog_row_image',
'binlog_expire_logs_seconds','expire_logs_days');
```

If necessary, change the source MySQL instance configurations to match the requirements.

<details>
<summary> Configure a self‑managed MySQL instance </summary>

1. Open `/etc/my.cnf` and add:

    ```toml
    [mysqld]
    log_bin = mysql-bin
    binlog_format = ROW
    binlog_row_image = FULL
    binlog_expire_logs_seconds = 604800   # 7 days retention
    ```

2. Restart: `sudo systemctl restart mysqld`

3. Run the `SHOW VARIABLES` query again to verify that the settings took effect.

</details>

<details>
<summary> Configure AWS RDS or Aurora MySQL </summary>

1. In the AWS console, open RDS, Parameter groups, and create (or edit) a custom parameter group.
2. Set the four parameters above to the required values.
3. Attach the parameter group to your instance/cluster and reboot to apply changes.
4. After the reboot, connect and run the `SHOW VARIABLES` query to confirm.

</details>

<details>
<summary> Configure Azure Database for MySQL ‑ Flexible Server </summary>

1. In the Azure portal, open MySQL Flexible Server, Server parameters.
2. Search for each setting and update the values.
Most changes apply without restart; the portal indicates if a reboot is needed.
3. Verify with the `SHOW VARIABLES` query.

</details>

<details>
<summary> Configure Google Cloud SQL for MySQL </summary>

1. In the Google Cloud console, go to Cloud SQL, `<your_instance>`, Flags.
2. Add or edit the necessary flags (`log_bin`, `binlog_format`, `binlog_row_image`, `binlog_expire_logs_seconds`).
3. Click Save. Cloud SQL prompts a restart if required.
4. After Cloud SQL restarts, run the `SHOW VARIABLES` query to confirm.

</details>

## Step 1: Go to the **Data Migration** page

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

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
    - If you use AWS Private Link, you are prompted to accept the endpoint request. Go to the [AWS VPC console](https://us-west-2.console.aws.amazon.com/vpc/home), and click **Endpoint services** to accept the endpoint request.

## Step 3: Choose migration job type

In the **Choose the objects to be migrated** step, you can choose existing data migration, incremental data migration, or both.

### Migrate existing data and incremental data

To migrate data to TiDB Cloud once and for all, choose both **Existing data migration** and **Incremental data migration**, which ensures data consistency between the source and target databases.

You can use **physical mode** or **logical mode** to migrate **existing data** and **incremental data**.

- The default mode is **logical mode**. This mode exports data from MySQL source databases as SQL statements, and then executes them on TiDB. In this mode, the target tables before migration can be either empty or non-empty. But the performance is slower than physical mode.

- For large datasets, it is recommended to use **physical mode**. This mode exports data from MySQL source databases and encodes it as KV pairs, writing directly to TiKV to achieve faster performance. This mode requires the target tables to be empty before migration. For the specification of 16 RCUs (Replication Capacity Units), the performance is about 2.5 times faster than logical mode. The performance of other specifications can increase by 20% to 50% compared with logical mode. Note that the performance data is for reference only and might vary in different scenarios.

Physical mode is available for TiDB clusters deployed on AWS and Google Cloud.

> **Note:**
>
> - When you use physical mode, you cannot create a second migration job or import task for the TiDB cluster before the existing data migration is completed.
> - When you use physical mode and the migration job has started, do **NOT** enable PITR (Point-in-time Recovery) or have any changefeed on the cluster. Otherwise, the migration job will be stuck. If you need to enable PITR or have any changefeed, use logical mode instead to migrate data.

Physical mode exports the MySQL source data as fast as possible, so [different specifications](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration) have different performance impacts on QPS and TPS of the MySQL source database during data export. The following table shows the performance regression of each specification.

| Migration specification |  Maximum export speed | Performance regression of the MySQL source database |
|---------|-------------|--------|
| 2 RCUs   | 80.84 MiB/s  | 15.6% |
| 4 RCUs   | 214.2 MiB/s  | 20.0% |
| 8 RCUs   | 365.5 MiB/s  | 28.9% |
| 16 RCUs | 424.6 MiB/s  | 46.7% |

### Migrate only existing data

To migrate only existing data of the source database to TiDB Cloud, choose **Existing data migration**.

You can only use logical mode to migrate existing data. For more information, see [Migrate existing data and incremental data](#migrate-existing-data-and-incremental-data).

### Migrate only incremental data

To migrate only the incremental data of the source database to TiDB Cloud, choose **Incremental data migration**. In this case, the migration job does not migrate the existing data of the source database to TiDB Cloud, but only migrates the ongoing changes of the source database that are explicitly specified by the migration job.

For detailed instructions about incremental data migration, see [Migrate Only Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md).

## Step 4: Choose the objects to be migrated

1. On the **Choose Objects to Migrate** page, select the objects to be migrated. You can click **All** to select all objects, or click **Customize** and then click the checkbox next to the object name to select the object.

    - If you click **All**, the migration job will migrate the existing data from the whole source database instance to TiDB Cloud and migrate ongoing changes after the full migration. Note that it happens only if you have selected the **Existing data migration** and **Incremental data migration** checkboxes in the previous step.

        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/migration-job-select-all.png" width="60%" />

    - If you click **Customize** and select some databases, the migration job will migrate the existing data and migrate ongoing changes of the selected databases to TiDB Cloud. Note that it happens only if you have selected the **Existing data migration** and **Incremental data migration** checkboxes in the previous step.

        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/migration-job-select-db.png" width="60%" />

    - If you click **Customize** and select some tables under a dataset name, the migration job only will migrate the existing data and migrate ongoing changes of the selected tables. Tables created afterwards in the same database will not be migrated.

        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/migration-job-select-tables.png" width="60%" />

    <!--
    - If you click **Customize** and select some databases, and then select some tables in the **Selected Objects** area to move them back to the **Source Database** area, (for example the `username` table in the following screenshots), then the tables will be treated as in a blocklist. The migration job will migrate the existing data but filter out the excluded tables (such as the `username` table in the screenshots), and will migrate ongoing changes of the selected databases to TiDB Cloud except the filtered-out tables.
        ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist1.png)
        ![Select Databases and Deselect Some Tables](/media/tidb-cloud/migration-job-select-db-blacklist2.png)
    -->

2. Click **Next**.

## Step 5: Precheck

On the **Precheck** page, you can view the precheck results. If the precheck fails, you need to operate according to **Failed** or **Warning** details, and then click **Check again** to recheck.

If there are only warnings on some check items, you can evaluate the risk and consider whether to ignore the warnings. If all warnings are ignored, the migration job will automatically go on to the next step.

For more information about errors and solutions, see [Precheck errors and solutions](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#precheck-errors-and-solutions).

For more information about precheck items, see [Migration Task Precheck](https://docs.pingcap.com/tidb/stable/dm-precheck).

If all check items show **Pass**, click **Next**.

## Step 6: Choose a spec and start migration

On the **Choose a Spec and Start Migration** page, select an appropriate migration specification according to your performance requirements. For more information about the specifications, see [Specifications for Data Migration](/tidb-cloud/tidb-cloud-billing-dm.md#specifications-for-data-migration).

After selecting the spec, click **Create Job and Start** to start the migration.

## Step 7: View the migration progress

After the migration job is created, you can view the migration progress on the **Migration Job Details** page. The migration progress is displayed in the **Stage and Status** area.

You can pause or delete a migration job when it is running.

If a migration job has failed, you can resume it after solving the problem.

You can delete a migration job in any status.

If you encounter any problems during the migration, see [Migration errors and solutions](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions).

## Scale a migration job specification

TiDB Cloud supports scaling up or down a migration job specification to meet your performance and cost requirements in different scenarios.

Different migration specifications have different performances. Your performance requirements might vary at different stages as well. For example, during the existing data migration, you want the performance to be as fast as possible, so you choose a migration job with a large specification, such as 8 RCU. Once the existing data migration is completed, the incremental migration does not require such a high performance, so you can scale down the job specification, for example, from 8 RCU to 2 RUC, to save cost.

When scaling a migration job specification, note the following:

- It takes about 5 to 10 minutes to scale a migration job specification.
- If the scaling fails, the job specification remains the same as it was before the scaling.

### Limitations

- You can only scale a migration job specification when the job is in the **Running** or **Paused** status.
- TiDB Cloud does not support scaling a migration job specification during the existing data export stage.
- Scaling a migration job specification will restart the job. If a source table of the job does not have a primary key, duplicate data might be inserted.
- During scaling, do not purge the binary log of the source database or increase `expire_logs_days` of the MySQL source database temporarily. Otherwise, the job might fail because it cannot get the continuous binary log position.

### Scaling procedure

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

2. Click the name of your target cluster to go to its overview page, and then click **Data Migration** in the left navigation pane.

3. On the **Data Migration** page, locate the migration job you want to scale. In the **Action** column, click **...** > **Scale Up/Down**.

4. In the **Scale Up/Down** window, select the new specification you want to use, and then click **Submit**. You can view the new price of the specification at the bottom of the window.
