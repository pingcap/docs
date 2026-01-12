---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Essential Using Data Migration
summary: Learn how to seamlessly migrate your MySQL databases from Amazon Aurora MySQL, Amazon RDS, Azure Database for MySQL - Flexible Server, Google Cloud SQL for MySQL, or self-managed MySQL instances to TiDB Cloud Essential with minimal downtime using the Data Migration feature.
---

# Migrate MySQL-Compatible Databases to TiDB Cloud Essential Using Data Migration

This document guides you through migrating your MySQL databases from Amazon Aurora MySQL, Amazon RDS, Azure Database for MySQL - Flexible Server, Google Cloud SQL for MySQL, or self-managed MySQL instances to TiDB Cloud Essential using the Data Migration feature in the [TiDB Cloud console](https://tidbcloud.com/).

This feature enables you to migrate your existing MySQL data and continuously replicate ongoing changes (binlog) from your MySQL-compatible source databases directly to TiDB Cloud Essential, maintaining data consistency whether in the same region or across different regions. The streamlined process eliminates the need for separate dump and load operations, reducing downtime and simplifying your migration from MySQL to a more scalable platform.

If you only want to replicate ongoing binlog changes from your MySQL-compatible database to TiDB Cloud Essential, see [Migrate Incremental Data from MySQL-Compatible Databases to TiDB Cloud Essential Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration-essential.md).

## Limitations

### Availability

- If you don't see the [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md#step-1-go-to-the-data-migration-page) entry for your TiDB Cloud Essential cluster in the [TiDB Cloud console](https://tidbcloud.com/), the feature might not be available in your region. To request support for your region, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

- Amazon Aurora MySQL writer instances support both existing data and incremental data migration. Amazon Aurora MySQL reader instances only support existing data migration and do not support incremental data migration.

### Maximum number of migration jobs

You can create up to 100 migration jobs for each organization. To create more migration jobs, you need to [file a support ticket](/tidb-cloud/tidb-cloud-support.md).

### Filtered out and deleted databases

- The system databases will be filtered out and not migrated to TiDB Cloud Essential even if you select all of the databases to migrate. That is, `mysql`, `information_schema`, `performance_schema`, and `sys` will not be migrated using this feature.

- When you delete a cluster in TiDB Cloud, all migration jobs in that cluster are automatically deleted and not recoverable.

### Limitations of Alibaba Cloud RDS

When using Alibaba Cloud RDS as a data source, every table must have an explicit primary key. For tables without one, RDS appends a hidden PK to the binlog, which leads to a schema mismatch with the source table and causes the migration to fail.

### Limitations of Alibaba Cloud PolarDB-X

During full data migration, PolarDB-X schemas may contain incompatible keywords that cause import to fail. This issue can be mitigated by pre-creating the target tables in the downstream database before initiating the migration process.

### Limitations of existing data migration

- During existing data migration, if the target database already contains the table to be migrated and there are duplicate keys, the rows with duplicate keys will be replaced.

- Only logical mode is supported for TiDB Cloud Essential now.

### Limitations of incremental data migration

- During incremental data migration, if the table to be migrated already exists in the target database with duplicate keys, an error is reported and the migration is interrupted. In this situation, you need to verify that the MySQL source data is accurate. If it is, click the "Restart" button of the migration job, and the migration job will replace the target TiDB Cloud cluster's conflicting records with the MySQL source records.

- During incremental replication (migrating ongoing changes to your cluster), if the migration job recovers from an abrupt error, it might open the safe mode for 60 seconds. During the safe mode, `INSERT` statements are migrated as `REPLACE`, `UPDATE` statements as `DELETE` and `REPLACE`, and then these transactions are migrated to the target TiDB Cloud cluster to ensure that all the data during the abrupt error has been migrated smoothly to the target TiDB Cloud cluster. In this scenario, for MySQL source tables without primary keys or non-null unique indexes, some data might be duplicated in the target TiDB Cloud cluster because the data might be inserted repeatedly into the target TiDB Cloud cluster.

- In the following scenarios, if the migration job takes longer than 24 hours, do not purge binary logs in the source database to ensure that Data Migration can get consecutive binary logs for incremental replication:

    - During the existing data migration.
    - After the existing data migration is completed and when incremental data migration is started for the first time, the latency is not 0 ms.

## Prerequisites

Before migrating, check whether your data source is supported, enable binary logging in your MySQL-compatible database, ensure network connectivity, and grant required privileges for both the source database and the target TiDB Cloud cluster database.

### Make sure your data source and version are supported

Data Migration supports the following data sources and versions:

| Data source                                      | Supported versions |
|:-------------------------------------------------|:-------------------|
| Self-managed MySQL (on-premises or public cloud) | 8.0, 5.7, 5.6      |
| Amazon Aurora MySQL                              | 8.0, 5.7, 5.6      |
| Amazon RDS MySQL                                 | 8.0, 5.7           |
| Alibaba Cloud RDS MySQL                          | 8.0, 5.7           |

### Enable binary logs in the source MySQL-compatible database for replication

To continuously replicate incremental changes from the source MySQL-compatible database to the TiDB Cloud target cluster using DM, you need the following configurations to enable binary logs in the source database:

| Configuration | Required value | Why |
|:--------------|:---------------|:----|
| `log_bin` | `ON` | Enables binary logging, which DM uses to replicate changes to TiDB |
| `binlog_format` | `ROW` | Captures all data changes accurately (other formats miss edge cases) |
| `binlog_row_image` | `FULL` | Includes all column values in events for safe conflict resolution |
| `binlog_expire_logs_seconds` | ≥ `86400` (1 day), `604800` (7 days, recommended) | Ensures DM can access consecutive logs during migration |

#### Check current values and configure the source MySQL instance

To check the current configurations, connect to the source MySQL instance and execute the following statement:

```sql
SHOW VARIABLES WHERE Variable_name IN
('log_bin','server_id','binlog_format','binlog_row_image',
'binlog_expire_logs_seconds','expire_logs_days');
```

If necessary, change the source MySQL instance configurations to match the required values.

<details>
<summary> Configure a self-managed MySQL instance </summary>

1. Open `/etc/my.cnf` and add the following:

    ```
    [mysqld]
    log_bin = mysql-bin
    binlog_format = ROW
    binlog_row_image = FULL
    binlog_expire_logs_seconds = 604800   # 7 days retention
    ```

2. Restart the MySQL service to apply the changes:

    ```
    sudo systemctl restart mysqld
    ```

3. Run the `SHOW VARIABLES` statement again to verify that the settings take effect.

For detailed instructions, see [MySQL Server System Variables](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html) and [The Binary Log](https://dev.mysql.com/doc/refman/8.0/en/binary-log.html) in MySQL documentation.

</details>

<details>
<summary> Configure AWS RDS or Aurora MySQL </summary>

1. In the AWS Management Console, open the [Amazon RDS console](https://console.aws.amazon.com/rds/), click **Parameter groups** in the left navigation pane, and then create or edit a custom parameter group.
2. Set the four parameters above to the required values.
3. Attach the parameter group to your instance or cluster, and then reboot to apply the changes.
4. After the reboot, connect to the instance and run the `SHOW VARIABLES` statement to verify the configuration.

For detailed instructions, see [Working with DB Parameter Groups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html) and [Configuring MySQL Binary Logging](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html) in AWS documentation.

</details>

### Ensure network connectivity

Before creating a migration job, you need to plan and set up proper network connectivity between your source MySQL instance, the TiDB Cloud Data Migration (DM) service, and your target TiDB Cloud Essential cluster.

The available connection methods are as follows:

| Connection method | Availability | Recommended for |
|:---------------------|:-------------|:----------------|
| Public endpoints or IP addresses | All cloud providers supported by TiDB Cloud | Quick proof-of-concept migrations, testing, or when private connectivity is unavailable |
| Private links or private endpoints | AWS and Azure only | Production workloads without exposing data to the public internet |

Choose a connection method that best fits your cloud provider, network topology, and security requirements, and then follow the setup instructions for that method.

#### End-to-end encryption over TLS/SSL

Regardless of the connection method, it is strongly recommended to use TLS/SSL for end-to-end encryption. While private endpoints and VPC peering secure the network path, TLS/SSL secures the data itself and helps meet compliance requirements.

<details>
<summary> Download and store the cloud provider's certificates for TLS/SSL encrypted connections </summary>

- Amazon Aurora MySQL or Amazon RDS MySQL: [Using SSL/TLS to encrypt a connection to a DB instance or cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html)

</details>

#### Public endpoints or IP addresses

When using public endpoints, you can verify network connectivity and access both now and later during the DM job creation process. TiDB Cloud will provide specific egress IP addresses and prompt instructions at that time.

1. Identify and record the source MySQL instance's endpoint hostname (FQDN) or public IP address.
2. Ensure you have the required permissions to modify the firewall or security group rules for your database. Refer to your cloud provider's documentation for guidance.
3. Optional: Verify connectivity to your source database from a machine with public internet access using the appropriate certificate for in-transit encryption:

    ```shell
    mysql -h <public-host> -P <port> -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. Later, during the Data Migration job setup, TiDB Cloud will provide an egress IP range. At that time, you need to add this IP range to your database's firewall or security-group rules following the same procedure above.

#### Private link or private endpoint

If you use a provider-native private link or private endpoint, create a [Private Link Connection](/tidb-cloud/serverless-private-link-connection.md) for your source MySQL instance.

### Grant required privileges for migration

Before starting migration, you need to set up appropriate database users with the required privileges on both the source and target databases. These privileges enable TiDB Cloud DM to read data from MySQL, replicate changes, and write to your TiDB Cloud cluster securely. Because the migration involves both full data dumps for existing data and binlog replication for incremental changes, your migration user requires specific permissions beyond basic read access.

#### Grant required privileges to the migration user in the source MySQL database

For testing purposes, you can use an administrative user (such as `root`) in your source MySQL database.

For production workloads, it is recommended to have a dedicated user for data dump and replication in the source MySQL database, and grant only the necessary privileges:

| Privilege | Scope | Purpose |
|:----------|:------|:--------|
| `SELECT` | Tables | Allows reading data from all tables |
| `RELOAD` | Global | Ensures consistent snapshots during full dump |
| `REPLICATION SLAVE` | Global | Enables binlog streaming for incremental replication |
| `REPLICATION CLIENT` | Global | Provides access to binlog position and server status |

For example, you can use the following `GRANT` statement in your source MySQL instance to grant corresponding privileges:

```sql
GRANT SELECT, RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'dm_source_user'@'%';
```

#### Grant required privileges in the target TiDB Cloud cluster

For testing purposes, you can use the `root` account of your TiDB Cloud Essential cluster.

For production workloads, it is recommended to have a dedicated user for replication in the target TiDB Cloud cluster and grant only the necessary privileges:

| Privilege | Scope | Purpose |
|:----------|:------|:--------|
| `CREATE` | Databases, Tables | Creates schema objects in the target |
| `SELECT` | Tables | Verifies data during migration |
| `INSERT` | Tables | Writes migrated data |
| `UPDATE` | Tables | Modifies existing rows during incremental replication |
| `DELETE` | Tables | Removes rows during replication or updates |
| `ALTER`  | Tables | Modifies table definitions when schema changes |
| `DROP`   | Databases, Tables | Removes objects during schema sync |
| `INDEX`  | Tables | Creates and modifies indexes |
| `CREATE VIEW`  | View | Create views used by migration |

For example, you can execute the following `GRANT` statement in your target TiDB Cloud cluster to grant corresponding privileges:

```sql
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE, ALTER, DROP, INDEX ON *.* TO 'dm_target_user'@'%';
```

## Step 1: Go to the Data Migration page

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Migration** in the left navigation pane.

3. On the **Data Migration** page, click **Create Migration Job** in the upper-right corner. The **Create Migration Job** page is displayed.

## Step 2: Configure the source and target connections

On the **Create Migration Job** page, configure the source and target connections.

1. Enter a job name, which must start with a letter and must be less than 60 characters. Letters (A-Z, a-z), numbers (0-9), underscores (_), and hyphens (-) are acceptable.

2. Fill in the source connection profile.

    - **Data source**: the data source type.
    - **Connectivity method**: select a connection method for your data source based on your security requirements and cloud provider:
        - **Public IP**: available for all cloud providers (recommended for testing and proof-of-concept migrations).
        - **Private Link**: available for AWS and Alibaba Cloud only (recommended for production workloads requiring private connectivity).
    - Based on the selected **Connectivity method**, do the following:
        - If **Public IP** is selected, fill in the **Hostname or IP address** field with the hostname or IP address of the data source.
        - If **Private Link** is selected, select the private link connection that you created in the [Private Link Connections](/tidb-cloud/serverless-private-link-connection.md) section.
    - **Port**: the port of the data source.
    - **User Name**: the username of the data source.
    - **Password**: the password of the username.
    - **SSL/TLS**: enable SSL/TLS for end-to-end data encryption (highly recommended for all migration jobs). Upload the appropriate certificates based on your MySQL server's SSL configuration.

        SSL/TLS configuration options:

        - Option 1: Server authentication only

            - If your MySQL server is configured for server authentication only, upload only the **CA Certificate**.
            - In this option, the MySQL server presents its certificate to prove its identity, and TiDB Cloud verifies the server certificate against the CA.
            - The CA certificate protects against man-in-the-middle attacks and is required if the MySQL server is started with `require_secure_transport = ON`.

        - Option 2: Client certificate authentication

            - If your MySQL server is configured for client certificate authentication, upload **Client Certificate** and **Client private key**.
            - In this option, TiDB Cloud presents its certificate to the MySQL server for authentication, but TiDB Cloud does not verify the MySQL server's certificate.
            - This option is typically used when the MySQL server is configured with options such as `REQUIRE SUBJECT '...'` or `REQUIRE ISSUER '...'` without `REQUIRE X509`, allowing it to check specific attributes of the client certificate without full CA validation of that client certificate.
            - This option is often used when the MySQL server accepts client certificates in self-signed or custom PKI environments. Note that this configuration is vulnerable to man-in-the-middle attacks and is not recommended for production environments unless other network-level controls guarantee server authenticity.

        - Option 3: Mutual TLS (mTLS) - highest security

            - If your MySQL server is configured for mutual TLS (mTLS) authentication, upload **CA Certificate**, **Client Certificate**, and **Client private key**.
            - In this option, the MySQL server verifies TiDB Cloud's identity using the client certificate, and TiDB Cloud verifies MySQL server's identity using the CA certificate.
            - This option is required when the MySQL server has `REQUIRE X509` or `REQUIRE SSL` configured for the migration user.
            - This option is used when the MySQL server requires client certificates for authentication.
            - You can get the certificates from the following sources:
                - Download from your cloud provider (see [TLS certificate links](#end-to-end-encryption-over-tlsssl)).
                - Use your organization's internal CA certificates.
                - Self-signed certificates (for development/testing only).

3. Fill in the target connection profile.

    - **User Name**: enter the username of the target cluster in TiDB Cloud.
    - **Password**: enter the password of the TiDB Cloud username.

4. Click **Validate Connection and Next** to validate the information you have entered.

5. Take action according to the message you see:

    - If you use **Public IP** as the connectivity method, you need to add the Data Migration service's IP addresses to the IP Access List of your source database and firewall (if any).

## Step 3: Choose migration job type

In the **Choose migration job type** step, you can choose existing data migration, incremental data migration, or both.

### Migrate existing data and incremental data

To migrate data to TiDB Cloud once and for all, choose both **Existing data migration** and **Incremental data migration**, which ensures data consistency between the source and target databases.

You can only use **logical mode** to migrate **existing data** and **incremental data**.

This mode exports data from MySQL source databases as SQL statements and then executes them on TiDB. In this mode, the target tables before migration can be either empty or non-empty.

### Migrate only incremental data

To migrate only the incremental data of the source database to TiDB Cloud, choose **Incremental data migration**. In this case, the migration job does not migrate the existing data of the source database to TiDB Cloud, but only migrates the ongoing changes of the source database that are explicitly specified by the migration job.

For detailed instructions about incremental data migration, see [Migrate Only Incremental Data from MySQL-Compatible Databases to TiDB Cloud Essential Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration-essential.md).

## Step 4: Choose the objects to be migrated

1. On the **Choose Objects to Migrate** page, select the objects to be migrated. You can click **All** to select all objects, or click **Customize** and then click the checkbox next to the object name to select the object.

    - If you click **All**, the migration job will migrate the existing data from the whole source database instance to TiDB Cloud and migrate ongoing changes after the full migration. Note that it happens only if you have selected the **Existing data migration** and **Incremental data migration** checkboxes in the previous step.
    - If you click **Customize** and select some databases, the migration job will migrate the existing data and migrate ongoing changes of the selected databases to TiDB Cloud. Note that it happens only if you have selected the **Existing data migration** and **Incremental data migration** checkboxes in the previous step.
    - If you click **Customize** and select some tables under a dataset name, the migration job will only migrate the existing data and migrate ongoing changes of the selected tables. Tables created afterwards in the same database will not be migrated.

2. Click **Next**.

## Step 5: Precheck

On the **Precheck** page, you can view the precheck results. If the precheck fails, you need to operate according to **Failed** or **Warning** details, and then click **Check again** to recheck.

If there are only warnings on some check items, you can evaluate the risk and consider whether to ignore the warnings. If all warnings are ignored, the migration job will automatically proceed to the next step.

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
