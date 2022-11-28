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

- If the source database is Amazon RDS or Aurora, you need to set the `binlog_format` parameter to `ROW`. If the database uses the default parameter group, the `binlog_format` parameter is set to `MIXED` by default and cannot be modified. In this case, you need to create a new parameter group, such as `newset`, and set `binlog_format` to `ROW`. Then, modify the default parameter group of the database to `newset`. Note that modifying the parameter group will restart the database.
- The default collation for the utf8mb4 character set in TiDB is `utf8mb4_bin`, in MySQL 5.7 it is `utf8mb4_general_ci`, and in MySQL 8.0, it is `utf8mb4_0900_ai_ci`. If the default collation is used in the upstream MySQL, because TiDB is not compatible with it, AWS DMS cannot create the target table in TiDB and cannot migrate the data. If you encounter such a problem, it is recommended to modify the collation of the source database to `utf8mb4_bin`.
- TiDB contains the following system databases by default: `INFORMATION_SCHEMA`, `PERFORMANCE_SCHEMA`, `mysql`, `sys`, and `test`. Therefore, when you create an AWS DMS task, you need to filter out these system databases. That is, do not use the default `%` when selecting the migration object. It is recommended to fill in the specific database and table names. Otherwise, AWS DMS will try to migrate these system databases from the source database to the target TiDB, which will cause the task to fail.
- You need to add the public and private network IP whitelist of AWS DMS to the source and target databases, so that AWS DMS can access the source and target databases. It is recommended to add both. Otherwise the network will not be connected in some scenarios.
- Use [VPC Peerings](/tidb-cloud/set-up-vpc-peering-connections.md#set-up-vpc-peering-connections) or [Private Link](/tidb-cloud/set-up-private-endpoint-connections.md) to connect AWS DMS and TiDB Cluster.
- It is recommended to use the same Region for AWS DMS and TiDB Cluster to get better data writing performance.
- It is recommended to use AWS DMS t3.large (2c8g) or a higher specification. Small specifications will possibly cause AWS DMS out of memory (OOM) errors.
- AWS will automatically create the `awsdms_control` database in the target database.

## Limitations

AWS DMS does not support replicating `DROP TABLE`.

## Step 1: Create an AWS DMS replication instance

1. Log in to the [AWS console](https://us-west-2.console.aws.amazon.com/dms/v2/home) and switch to the corresponding region. It is recommended to use the same Region for AWS DMS and TiDB Cloud.

2. Click **Create replication instance**. In this document, the upstream and downstream databases and DMS instance are all in the **us-west-2** region.

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-instance.png)

3. Fill in the instance name, and select an appropriate instance class. It is recommended to use dms.t3.large or a higher class to get better performance.

    ![Fill name and choose class](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-choose-class.png)

4. Use default configurations. Select the VPC that you need. It is recommended to use the same VPC as the upstream database to simplify the network configuration. Select **Single-AZ** or **Multi-AZ** based on your business needs.

    ![Choose VPC](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-choose-vpc.png)

5. Configure the **Advanced security and network configuration**, **Maintenance**, and **Tags** if needed. Click **Create** to finish the instance creation.

    ![Click the Create button](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-button.png)

## Step 2: Create the source database endpoint
