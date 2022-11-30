---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using AWS DMS
summary: Learn how to migrate data from MySQL-compatible databases into TiDB Cloud using AWS Database Migration Service (AWS DMS).
---

# Migrate MySQL-Compatible Databases to TiDB Cloud Using AWS DMS

AWS Database Migration Service (AWS DMS) is a cloud service that makes it easy to migrate relational databases, data warehouses, NoSQL databases, and other types of data stores. You can use AWS DMS to migrate your data into TiDB Cloud.

This document uses Amazon Relational Database Service (RDS) as an example to show how to migrate data to TiDB Cloud using AWS DMS. The procedure also applies to migrating data from self-built MySQL databases and Amazon Aurora.

In this example, the data source is Amazon RDS, and the data destination is a Dedicated Tier cluster in TiDB Cloud. Both upstream and downstream databases are in the same region.

## Prerequisites

Before you start the migration, make sure you have read the following:

- If the source database is Amazon RDS or Aurora, you need to set the `binlog_format` parameter to `ROW`. If the database uses the default parameter group, the `binlog_format` parameter is set to `MIXED` by default and cannot be modified. In this case, you need to [create a new parameter group](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.Prerequisites.html#CHAP_GettingStarted.Prerequisites.params), for example `newset`, and set `binlog_format` to `ROW`. Then, modify the default parameter group to `newset`. Note that modifying the parameter group will restart the database.
- The default collation for the utf8mb4 character set in TiDB is `utf8mb4_bin`, in MySQL 5.7 it is `utf8mb4_general_ci`, and in MySQL 8.0, it is `utf8mb4_0900_ai_ci`. If the default collation is used in the upstream MySQL, because TiDB is not compatible with it, AWS DMS cannot create the target table in TiDB and cannot migrate the data. If you encounter such a problem, you can modify the collation of the source database to `utf8mb4_bin`.
- TiDB contains the following system databases by default: `INFORMATION_SCHEMA`, `PERFORMANCE_SCHEMA`, `mysql`, `sys`, and `test`. Therefore, when you create an AWS DMS task, you need to filter out these system databases. That is, do not use the default `%` when selecting the migration object. It is recommended to fill in the specific database and table names. Otherwise, AWS DMS will try to migrate these system databases from the source database to the target TiDB, which will cause the task to fail.
- You need to add the public and private network IP whitelist of AWS DMS to the source and target databases, so that AWS DMS can access the source and target databases. It is recommended to add both. Otherwise network connection might fail in some scenarios.
- Use [VPC Peerings](/tidb-cloud/set-up-vpc-peering-connections.md#set-up-vpc-peering-connections) or [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) to connect AWS DMS and TiDB Cluster.
- It is recommended to use the same region for AWS DMS and TiDB Cluster to get better data writing performance.
- It is recommended to use AWS DMS t3.large (2c8g) or a higher specification. Small specifications will possibly cause out of memory (OOM) errors.
- AWS will automatically create the `awsdms_control` database in the target database.

## Limitation

AWS DMS does not support replicating `DROP TABLE`.

## Step 1: Create an AWS DMS replication instance

1. Log in to the [AWS DMS console](https://us-west-2.console.aws.amazon.com/dms/v2/home) and switch to the corresponding region. It is recommended to use the same region for AWS DMS and TiDB Cloud.

2. Click **Create replication instance**. In this document, the upstream and downstream databases and DMS instance are all in the **us-west-2** region.

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-instance.png)

3. Fill in the instance name, and select an appropriate instance class. It is recommended to use dms.t3.large or a higher class to get better performance.

    ![Fill name and choose class](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-choose-class.PNG)

4. Use default configurations. Select the VPC that you need. It is recommended to use the same VPC as the upstream database to simplify the network configuration. Select **Single-AZ** or **Multi-AZ** based on your business needs.

    ![Choose VPC](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-vpc.PNG)

5. Configure the **Advanced security and network configuration**, **Maintenance**, and **Tags** if needed. Click **Create** to finish the instance creation.

    ![Click the Create button](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-button.png)

## Step 2: Create the source database endpoint

1. In the [AWS DMS console](https://us-west-2.console.aws.amazon.com/dms/v2/home), click the replication instance that you just created. Copy the public and private network IP addresses as shown in the following screen shot.

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2. Configure the security group rules for Amazon RDS. In the example in this document, add the public and private IP addresses of the AWS DMS instance to the security group.

    ![Configure the security group rules](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-rules.png)

3. Click **Create endpoint** to create the source database endpoint.

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint.png)

4. In this example, click **Select RDS DB instance** and then select the source RDS instance. If the source database is a self-built MySQL, you can skip this step and fill in the information in the following steps.

    ![Select RDS DB instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-select-rds.png)

5. Fill in the following information:
   - **Endpoint identifier**: create a label for the source endpoint to help you identify it in the subsequent task configuration.
   - **Descriptive Amazon Resource Name (ARN) - optional**: create a friendly name for the default DMS ARN.
   - **Source engine**: select **MySQL**.
   - **Access to endpoint database**: select **Provide access information manually**.
   - **Server name**: fill in the server name. It is the name of the data server for the data provider. If the upstream is Amazon RDS or Amazon Aurora, it will be automatically filled in. You can copy it from the database console. If it is a self-built MySQL without a domain name, you can fill in the IP address.
   - Fill in the database **Port**, **Username**, and **Password**.
   - **Secure Socket Layer (SSL) mode**: you can enable SSL mode as needed.

    ![Fill in the endpoint configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-endpoint-config.png)

6. Use default values for **Endpoint settings**, **KMS key**, and **Tags**. In the **Test endpoint connection (optional)** section, it is recommended to select the same VPC as the source database to simplify the network configuration. Select the corresponding replication instance, and then click **Run test**. The status needs to be **successful**. Finally, click **Create endpoint**.

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-connection.png)

## Step 3: Create the target database endpoint

1. In the [AWS DMS console](https://us-west-2.console.aws.amazon.com/dms/v2/home), click the replication instance that you just created. Copy the public and private network IP addresses as shown in the following screen shot.

    ![Copy the public and private network IP addresses](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-copy-ip.png)

2. Go to the [TiDB Cloud console](https://tidbcloud.com/console/clusters), locate the target cluster, and click **Connect** to get the TiDB Cloud database connection information.

    ![Get the TiDB Cloud database connection information](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-connect.png)

3. Enter the public and private network IP addresses that you copied from the AWS DMS console and click **Update Filter**. It is recommended to add the Public IP address and Private IP address of the AWS DMS replication instance to the TiDB Cluster traffic filter at the same time. Otherwise AWS DMS might not be able to connect to the TiDB Cluster in some scenarios.

    ![Update the TiDB Cloud traffic filter](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-traffic-filter.png)

4. As shown in the following screen shot, you need to connect to the TiDB cluster through SSL. Click **Download TiDB cluster CA** to download the CA certificate. Record the `-u`, `-h`, and `-P` information highlighted in the following screen shot for subsequent connection with TiDB.

    ![Download TiDB cluster CA](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-ca.png)

5. Create VPC Peering for TiDB Cluster and AWS DMS.

    ![Create VPC Peering](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-vpc-peering.png)

6. Fill in the corresponding information. See [Set Up VPC Peering Connections](/tidb-cloud/set-up-vpc-peering-connections.md).

    ![Fill in the VPC Peering information](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-vpc-peering-info.png)

7. Configure the target endpoint for TiDB. Select **Target endpoint** for **Endpoint type**, and fill in a name for **Endpoint identifier**. Select **MySQL** for **Target engine**.

    ![Configure the target endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint.png)

8. Fill in the server name. You can copy it from the TiDB Cloud console. The port is 4000. Fill in the username and password. Select **Verify-ca** for SSL mode. Click **Add a new CA certificate** to upload the ca file downloaded in the previous step.

    ![Fill in the target endpoint information](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint2.png)

9. Upload the CA file.

    ![Upload CA](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-upload-ca.png)

10. Use the default values for **Endpoint settings**, **KMS key**, and **Tags**. In the **Test endpoint connection (optional)** section, select the same VPC as the source database. Select the corresponding replication instance, and then click **Run test**. The status needs to be **successful**. Finally, click **Create endpoint**.

    ![Click Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-target-endpoint3.png)

## Step 4: Create a database migration task

1. In the [AWS DMS console](https://us-west-2.console.aws.amazon.com/dms/v2/home), click **Database migration tasks** on the left navigation bar. Then click **Create task** in the upper right corner of the window.

    ![Create task](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2. Fill in the following task configurations:
    - **Task identifier**: fill in a name for the task. It is recommended to use a name that is easy to remember.
    - **Descriptive Amazon Resource Name (ARN) - optional**: create a friendly name for the default DMS ARN.
    - **Replication instance**: select the AWS DMS instance that you just created.
    - **Source database endpoint**: select the source database endpoint that you just created.
    - **Target database endpoint**: select the target database endpoint that you just created.
    - **Migration type**: select a migration type as needed. In this example, select **Migrate existing data and replicate ongoing changes**.

    ![Task configurations](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-config.png)

3. Fill in the following task settings:
    - **Editing mode**: select **Wizard**.
    - **Target table preparation mode**: select **Do nothing** or other options as needed. In this example, select **Do nothing**.
    - **Include LOB columns in replication**: select **Limited LOB mode**.
    - **Maximum LOB size in (KB)**: use the default value 32.
    - **Turn on validation**: leave it unchecked.
    - **Task logs**: select **Turn on CloudWatch logs** for troubleshooting in future.

    ![Task settings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-settings.png)

4. In the **Table mappings** section, specify the database to be migrated. The schema name is the database name in the Amazon RDS instance. The default value of the source name is "%", which means that all databases in the Amazon RDS will be migrated to TiDB. It will cause the system databases such as `mysql` and `sys` in Amazon RDS to be migrated to TiDB, and result in task failure. Therefore, it is recommended to fill in the specific database name, or filter out all system databases, as shown in the following screen shot, only the database named `franktest` and all the tables in that database will be migrated. Finally, click **Create task** in the lower right corner.

    ![Table mappings](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-table-mappings.png)

5. Go back to the **Data migration tasks** page. You can see the status and progress of the task.

    ![Tasks status](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-task-status.png)

If you encounter any issues or failures during the migration, you can check the log information in [CloudWatch](https://us-west-2.console.aws.amazon.com/cloudwatch/home) to troubleshoot the issues.

![Troubleshooting](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)
