---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration
summary: Learn how to seamlessly migrate your MySQL databases from Amazon Aurora MySQL, Amazon RDS, Azure Database for MySQL - Flexible Server, Google Cloud SQL for MySQL, or self-managed MySQL instances to TiDB Cloud with minimal downtime using the Data Migration feature.
aliases: ['/tidbcloud/migrate-data-into-tidb','/tidbcloud/migrate-incremental-data-from-mysql']
---

# Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration

This document guides you through migrating your MySQL databases from Amazon Aurora MySQL, Amazon RDS, Azure Database for MySQL - Flexible Server, Google Cloud SQL for MySQL, or self-managed MySQL instances to TiDB Cloud using the Data Migration feature in the [TiDB Cloud console](https://tidbcloud.com/).

This feature enables you to migrate your existing MySQL data and continuously replicate ongoing changes (binlog) from your MySQL-compatible source databases directly to TiDB Cloud, maintaining data consistency whether in the same region or across different regions. The streamlined process eliminates the need for separate dump and load operations, reducing downtime and simplifying your migration from MySQL to a more scalable platform.

If you only want to replicate ongoing binlog changes from your MySQL-compatible database to TiDB Cloud, see [Migrate Incremental Data from MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md).

## Limitations

### Availability

- The Data Migration feature is available only for **TiDB Cloud Dedicated** clusters.

- The Data Migration feature is only available to clusters that are created in [certain regions](https://www.pingcap.com/tidb-cloud-pricing-details/#dm-cost) after November 9, 2022. If your **project** was created before the date or if your cluster is in another region, this feature is not available to your cluster, and the **Data Migration** tab will not be displayed on the cluster overview page in the TiDB Cloud console.

- Amazon Aurora MySQL writer instances support both existing data and incremental data migration. Amazon Aurora MySQL reader instances only support existing data migration and do not support incremental data migration.

### Maximum number of migration jobs

You can create up to 200 migration jobs for each organization. To create more migration jobs, you need to [file a support ticket](/tidb-cloud/tidb-cloud-support.md).

### Filtered out and deleted databases

- The system databases will be filtered out and not migrated to TiDB Cloud even if you select all of the databases to migrate. That is, `mysql`, `information_schema`, `information_schema`, and `sys` will not be migrated using this feature.

- When you delete a cluster in TiDB Cloud, all migration jobs in that cluster are automatically deleted and not recoverable.

### Limitations of existing data migration

- During existing data migration, if the target database already contains the table to be migrated and there are duplicate keys, the rows with duplicate keys will be replaced.

- If your dataset size is smaller than 1 TiB, it is recommended that you use logical mode (the default mode). If your dataset size is larger than 1 TiB, or you want to migrate existing data faster, you can use physical mode. For more information, see [Migrate existing data and incremental data](#migrate-existing-data-and-incremental-data).

### Limitations of incremental data migration

- During incremental data migration, if the table to be migrated already exists in the target database with duplicated keys, an error is reported and the migration is interrupted. In this situation, you need to make sure whether the MySQL source data is accurate. If yes, click the "Restart" button of the migration job, and the migration job will replace the target TiDB Cloud cluster's conflicting records with the MySQL source records.

- During incremental replication (migrating ongoing changes to your cluster), if the migration job recovers from an abrupt error, it might open the safe mode for 60 seconds. During the safe mode, `INSERT` statements are migrated as `REPLACE`, `UPDATE` statements as `DELETE` and `REPLACE`, and then these transactions are migrated to the target TiDB Cloud cluster to make sure that all the data during the abrupt error has been migrated smoothly to the target TiDB Cloud cluster. In this scenario, for MySQL source tables without primary keys or not-null unique indexes, some data might be duplicated in the target TiDB Cloud cluster because the data might be inserted repeatedly into the target TiDB Cloud cluster.

- In the following scenarios, if the migration job takes longer than 24 hours, do not purge binary logs in the source database to ensure that Data Migration can get consecutive binary logs for incremental replication:

    - During the existing data migration.
    - After the existing data migration is completed and when incremental data migration is started for the first time, the latency is not 0ms.

## Prerequisites

Before migrating, check whether your data source is supported, enable binary logging in your MySQL-compatible database, ensure network connectivity, and grant required privileges for both the source database and the target TiDB Cloud cluster database.

### Make sure your data source and version are supported

Data Migration supports the following data sources and versions:

| Data source | Supported versions |
|:------------|:-------------------|
| Self-managed MySQL (on-premises or public cloud) | 8.0, 5.7, 5.6 |
| Amazon Aurora MySQL | 8.0, 5.7, 5.6 |
| Amazon RDS MySQL | 8.0, 5.7 |
| Azure Database for MySQL - Flexible Server | 8.0, 5.7 |
| Google Cloud SQL for MySQL | 8.0, 5.7, 5.6 |

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
<summary> Configure a self‑managed MySQL instance </summary>

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
    sudo systemctl restart mysqld`
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

<details>
<summary> Configure Azure Database for MySQL - Flexible Server </summary>

1. In the [Azure portal](https://portal.azure.com/), search for and select **Azure Database for MySQL servers**, click your instance name, and then click **Setting** > **Server parameters** in the left navigation pane.
2. Search for each parameter and update its value.

    Most changes take effect without a restart. If a restart is required, you will get a prompt from the portal.

3. Run the `SHOW VARIABLES` statement to verify the configuration.

For detailed instructions, see [Configure server parameters in Azure Database for MySQL - Flexible Server using the Azure portal](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-configure-server-parameters-portal) in the Microsoft Azure documentation.

</details>

<details>
<summary> Configure Google Cloud SQL for MySQL </summary>

1. In the [Google Cloud console](https://console.cloud.google.com/project/_/sql/instances), select the project that contains your instance, click your instance name, and then click **Edit**.
2. Add or modify the required flags (`log_bin`, `binlog_format`, `binlog_row_image`, `binlog_expire_logs_seconds`).
3. Click **Save**. If a restart is required, you will get a prompt from the console.
4. After the restart, run the `SHOW VARIABLES` statement to confirm the changes.

For detailed instructions, see [Configure database flags](https://cloud.google.com/sql/docs/mysql/flags) and [Use point-in-time recovery](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr) in Google Cloud documentation.

</details>

### Ensure network connectivity

Before creating a migration job, you need to plan and set up proper network connectivity between your source MySQL instance, the TiDB Cloud Data Migration (DM) service, and your target TiDB Cloud cluster.

The available connection methods are as follows:

| Connection method | Availability | Recommended for |
|:---------------------|:-------------|:----------------|
| Public endpoints or IP addresses | All cloud providers supported by TiDB Cloud | Quick proof-of-concept migrations, testing, or when private connectivity is unavailable |
| Private links or private endpoints | AWS and Azure only | Production workloads without exposing data to the public internet |
| VPC peering | AWS and Google Cloud only | Production workloads that need low-latency, intra-region connections and have non-overlapping VPC/VNet CIDRs |

Choose a connection method that best fits your cloud provider, network topology, and security requirements, and then follow the setup instructions for that method.

#### End-to-end encryption over TLS/SSL

Regardless of the connection method, it is strongly recommended to use TLS/SSL for end-to-end encryption. While private endpoints and VPC peering secure the network path, TLS/SSL secures the data itself and helps meet compliance requirements.

<details>
<summary> Download and store the cloud provider's certificates for TLS/SSL encrypted connections </summary>

- Amazon Aurora MySQL or Amazon RDS MySQL: [Using SSL/TLS to encrypt a connection to a DB instance or cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL.html)
- Azure Database for MySQL - Flexible Server: [Connect with encrypted connections](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-connect-tls-ssl)
- Google Cloud SQL for MySQL: [Manage SSL/TLS certificates](https://cloud.google.com/sql/docs/mysql/manage-ssl-instance)

</details>

#### Public endpoints or IP addresses

When using public endpoints, you can verify network connectivity and access both now and later during the DM job creation process. TiDB Cloud will provide specific egress IP addresses and prompt instructions at that time.

1. Identify and record the source MySQL instance's endpoint hostname (FQDN) or public IP address.
2. Ensure you have the required permissions to modify the firewall or security group rules for your database. Refer to your cloud provider’s documentation for guidance as follows:

    - Amazon Aurora MySQL or Amazon RDS MySQL: [Controlling access with security groups](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Overview.RDSSecurityGroups.html).
    - Azure Database for MySQL - Flexible Server: [Public Network Access](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-networking-public)
    - Google Cloud SQL for MySQL: [Authorized Networks](https://cloud.google.com/sql/docs/mysql/configure-ip#authorized-networks).

3. Optional: Verify connectivity to your source database from a machine with public internet access using the appropriate certificate for in-transit encryption:

    ```shell
    mysql -h <public-host> -P <port> -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. Later, during the Data Migration job setup, TiDB Cloud will provide an egress IP range. At that time, you need to add this IP range to your database's firewall or security‑group rules following the same procedure above.

#### Private link or private endpoint

If you use a provider-native private link or private endpoint, create a private endpoint for your source MySQL instance (RDS, Aurora, or Azure Database for MySQL).

<details>
<summary> Set up AWS PrivateLink and Private Endpoint for the MySQL source database </summary>

AWS does not support direct PrivateLink access to RDS or Aurora. Therefore, you need to create a Network Load Balancer (NLB) and publish it as an endpoint service associated with your source MySQL instance.

1. In the [Amazon EC2 console](https://console.aws.amazon.com/ec2/), create an NLB in the same subnet(s) as your RDS or Aurora writer. Configure the NLB with a TCP listener on port `3306` that forwards traffic to the database endpoint.

    For detailed instructions, see [Create a Network Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html) in AWS documentation.

2. In the [Amazon VPC console](https://console.aws.amazon.com/vpc/), click **Endpoint Services** in the left navigation pane, and then create an endpoint service. During the setup, select the NLB created in the previous step as the backing load balancer, and enable the **Require acceptance for endpoint** option. After the endpoint service is created, copy the service name (in the `com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx` format) for later use.

    For detailed instructions, see [Create an endpoint service](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html) in AWS documentation.

3. Optional: Test connectivity from a bastion or client inside the same VPC or VNet before starting the migration:

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. Later, when configuring TiDB Cloud DM to connect via PrivateLink, you will need to return to the AWS console and approve the pending connection request from TiDB Cloud to this private endpoint.

</details>

<details>
<summary> Set up Azure PrivateLink and private endpoint for the MySQL source database </summary>

Azure Database for MySQL - Flexible Server supports native private endpoints. You can either enable private access (VNet Integration) during MySQL instance creation or add a private endpoint later.

To add a new private endpoint, take the following steps:

1. In the [Azure portal](https://portal.azure.com/), search for and select **Azure Database for MySQL servers**, click your instance name, and then click **Setting** > **Networking** in the left navigation pane.
2. On the **Networking** page, scroll down to the **Private endpoints** section, click **+ Create private endpoint**, and then follow the on-screen instructions to set up the private endpoint.

    During the setup, select the virtual network and subnet that TiDB Cloud can access in the **Virtual Network** tab, and keep **Private DNS integration** enabled in the **DNS** tab. After the private endpoint is created and deployed, click **Go to resource**, click **Settings** > **DNS configuration** in the left navigation pane, and find the hostname to be used to connect with the instance in the **Customer Visible FQDNs** section. Typically, the hostname is in the `<your-instance-name>.mysql.database.azure.com` format.

    For detailed instructions, see [Create a private endpoint via Private Link Center](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-networking-private-link-portal#create-a-private-endpoint-via-private-link-center) in Azure documentation.

3. Optional: Test connectivity from a bastion or client inside the same VPC or VNet before starting the migration:

    ```shell
    mysql -h <private‑host> -P 3306 -u <user> -p --ssl-ca=<path-to-provider-ca.pem> -e "SELECT version();"
    ```

4. In the [Azure portal](https://portal.azure.com/), return to the overview page of your MySQL Flexible Server instance (not the private endpoint object), click **JSON View** for the **Essentials** section, and then copy the resource ID for later use. The resource ID is in the `/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>` format. You will use this resource ID (not the private endpoint ID) to configure TiDB Cloud DM.

5. Later, when configuring TiDB Cloud DM to connect via PrivateLink, you will need to return to the Azure portal and approve the pending connection request from TiDB Cloud to this private endpoint.

</details>

#### VPC peering

If you use AWS VPC peering or Google Cloud VPC network peering, see the following instructions to configure the network.

<details>
<summary> Set up AWS VPC peering</summary>

If your MySQL service is in an AWS VPC, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.

2. Modify the inbound rules of the security group that the MySQL service is associated with.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) to the inbound rules. Doing so allows the traffic to flow from your TiDB cluster to the MySQL instance.

3. If the MySQL URL contains a DNS hostname, you need to allow TiDB Cloud to be able to resolve the hostname of the MySQL service.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

</details>

<details>
<summary> Set up Google Cloud VPC network peering </summary>

If your MySQL service is in a Google Cloud VPC, take the following steps:

1. If it is a self-hosted MySQL, you can skip this step and proceed to the next step. If your MySQL service is Google Cloud SQL, you must expose a MySQL endpoint in the associated VPC of the Google Cloud SQL instance. You might need to use the [Cloud SQL Auth proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy) developed by Google.

2. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of your MySQL service and your TiDB cluster.

3. Modify the ingress firewall rules of the VPC where MySQL is located.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) to the ingress firewall rules. This allows the traffic to flow from your TiDB cluster to the MySQL endpoint.

</details>

### Grant required privileges for migration

Before starting migration, you need to set up appropriate database users with the required privileges on both the source and target databases. These privileges enable TiDB Cloud DM to read data from MySQL, replicate changes, and write to your TiDB Cloud cluster securely. Because the migration involves both full data dumps for existing data and binlog replication for incremental changes, your migration user requires specific permissions beyond basic read access.

#### Grant required privileges to the migration user in the source MySQL database

For testing purposes, you can use an administrative user (such as `root`) in your source MySQL database.

For production workloads, it is recommended to have a dedicated user for data dump and replication in the source MySQL database, and grant only the necessary privileges:

| Privilege | Scope | Purpose |
|:----------|:------|:--------|
| `SELECT` | Tables | Allows reading data from all tables |
| `LOCK TABLES` | Tables | Ensures consistent snapshots during full dump |
| `REPLICATION SLAVE` | Global | Enables binlog streaming for incremental replication |
| `REPLICATION CLIENT` | Global | Provides access to binlog position and server status |

For example, you can use the following `GRANT` statement in your source MySQL instance to grant corresponding privileges:

```sql
GRANT SELECT, LOCK TABLES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'dm_source_user'@'%';
```

#### Grant required privileges in the target TiDB Cloud cluster

For testing purposes, you can use the `root` account of your TiDB Cloud cluster.

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

For example, you can execute the following `GRANT` statement in your target TiDB Cloud cluster to grant corresponding privileges:

```sql
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE, ALTER, DROP, INDEX ON *.* TO 'dm_target_user'@'%';
```

## Step 1: Go to the **Data Migration** page

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click the name of your target cluster to go to its overview page, and then click **Data Migration** in the left navigation pane.

3. On the **Data Migration** page, click **Create Migration Job** in the upper-right corner. The **Create Migration Job** page is displayed.

## Step 2: Configure the source and target connections

On the **Create Migration Job** page, configure the source and target connections.

1. Enter a job name, which must start with a letter and must be less than 60 characters. Letters (A-Z, a-z), numbers (0-9), underscores (_), and hyphens (-) are acceptable.

2. Fill in the source connection profile.

   - **Data source**: the data source type.
   - **Connectivity method**: select a connection method for your data source based on your security requirements and cloud provider:
      - **Public IP**: available for all cloud providers (recommended for testing and proof-of-concept migrations).
      - **Private Link**: available for AWS and Azure only (recommended for production workloads requiring private connectivity).
      - **VPC Peering**: available for AWS and Google Cloud only (recommended for production workloads needing low-latency, intra-region connections with non-overlapping VPC/VNet CIDRs).
   - Based on the selected **Connectivity method**, do the following:
      - If **Public IP** or **VPC Peering** is selected, fill in the **Hostname or IP address** field with the hostname or IP address of the data source.
      - If **Private Link** is selected, fill in the following information:
         - **Endpoint Service Name** (available if **Data source** is from AWS): enter the VPC endpoint service name (format: `com.amazonaws.vpce-svc-xxxxxxxxxxxxxxxxx`) that you created for your RDS or Aurora instance.
         - **Private Endpoint Resource ID** (available if **Data source** is from Azure): enter the resource ID of your MySQL Flexible Server instance (format: `/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.DBforMySQL/flexibleServers/<server>`).
   - **Port**: the port of the data source.
   - **User Name**: the username of the data source.
   - **Password**: the password of the username.
   - **SSL/TLS**: enable SSL/TLS for end-to-end data encryption (highly recommended for all migration jobs). Upload the appropriate certificates based on your MySQL server's SSL configuration.
        <details>
        <summary> SSL/TLS configuration options </summary>

        - **Option 1: Server authentication only**
            - if your MySQL server is configured for server authentication only, upload only the **CA Certificate**.
            - In this option, the MySQL server presents its certificate to prove its identity, and TiDB Cloud verifies the server certificate against the CA.
            - The CA certificate protects against man-in-the-middle attacks and is required if the MySQL server is started with `require_secure_transport = ON`.
        - **Option 2: Client certificate authentication**
            - if your MySQL server is configured for client certificate authentication, upload **Client Certificate** and  **Client private key**.
            - In this option, TiDB Cloud presents its certificate to the MySQL server for authentication, but TiDB Cloud does not verify the MySQL server's certificate.
            - This option is typically used when the MySQL server is configured with options such as `REQUIRE SUBJECT '...'` or `REQUIRE ISSUER '...'` without `REQUIRE X509`, allowing it to check specific attributes of the client certificate without full CA validation of that client cert.
            - This option is often used when the MySQL server accepts client certificates in self-signed or custom PKI environments. Note that this configuration is vulnerable to man-in-the-middle attacks and is not recommended for production environments unless other network-level controls guarantee server authenticity.
        - **Option 3: Mutual TLS (mTLS) - highest security**
            - if your MySQL server is configured for mutual TLS (mTLS) authentication, upload **CA Certificate**, **Client Certificate**, and **Client private key**.
            - In this option, the MySQL server verifies TiDB Cloud's identity using the client certificate, and TiDB Cloud verifies MySQL server's identity using the CA certificate.
            - This option is required when the MySQL server has `REQUIRE X509` or `REQUIRE SSL` configured for the migration user.
            - This option is used when the MySQL server requires client certificates for authentication.
            - You can get the certificates from the following sources:
                - Download from your cloud provider (see [TLS certificate links](#end-to-end-encryption-over-tlsssl)).
                - Use your organization's internal CA certificates.
                - Self-signed certificates (for development/testing only).
        </details>

3. Fill in the target connection profile.

   - **User Name**: enter the username of the target cluster in TiDB Cloud.
   - **Password**: enter the password of the TiDB Cloud username.

4. Click **Validate Connection and Next** to validate the information you have entered.

5. Take action according to the message you see:

    - If you use **Public IP** or **VPC Peering** as the connectivity method, you need to add the Data Migration service's IP addresses to the IP Access List of your source database and firewall (if any).
    - If you use **Private Link** as the connectivity method, you are prompted to accept the endpoint request:
        - For AWS: go to the [AWS VPC console](https://us-west-2.console.aws.amazon.com/vpc/home), click **Endpoint services**, and accept the endpoint request from TiDB Cloud.
        - For Azure: go to the [Azure portal](https://portal.azure.com), search for your MySQL Flexible Server by name, click **Setting** > **Networking** in the left navigation pane, locate the **Private endpoint** section on the right side, and then approve the pending connection request from TiDB Cloud.

## Step 3: Choose migration job type

In the **Choose the objects to be migrated** step, you can choose existing data migration, incremental data migration, or both.

### Migrate existing data and incremental data

To migrate data to TiDB Cloud once and for all, choose both **Existing data migration** and **Incremental data migration**, which ensures data consistency between the source and target databases.

You can use **physical mode** or **logical mode** to migrate **existing data** and **incremental data**.

- The default mode is **logical mode**. This mode exports data from MySQL source databases as SQL statements and then executes them on TiDB. In this mode, the target tables before migration can be either empty or non-empty. But the performance is slower than physical mode.

- For large datasets, it is recommended to use **physical mode**. This mode exports data from MySQL source databases and encodes it as KV pairs, writing directly to TiKV to achieve faster performance. This mode requires the target tables to be empty before migration. For the specification of 16 RCUs (Replication Capacity Units), the performance is about 2.5 times faster than logical mode. The performance of other specifications can increase by 20% to 50% compared with logical mode. Note that the performance data is for reference only and might vary in different scenarios.

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
    - If you click **Customize** and select some databases, the migration job will migrate the existing data and migrate ongoing changes of the selected databases to TiDB Cloud. Note that it happens only if you have selected the **Existing data migration** and **Incremental data migration** checkboxes in the previous step.
    - If you click **Customize** and select some tables under a dataset name, the migration job will only migrate the existing data and migrate ongoing changes of the selected tables. Tables created afterwards in the same database will not be migrated.

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

Different migration specifications have different performances. Your performance requirements might vary at different stages as well. For example, during the existing data migration, you want the performance to be as fast as possible, so you choose a migration job with a large specification, such as 8 RCU. Once the existing data migration is completed, the incremental migration does not require such a high performance, so you can scale down the job specification, for example, from 8 RCU to 2 RCU, to save cost.

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
