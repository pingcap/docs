---
title:  Migrate from Amazon RDS for Oracle to TiDB Cloud Using AWS DMS
summary: Learn how to migrate data from Amazon RDS for Oracle into TiDB Serverless using AWS Database Migration Service (AWS DMS).
---

# Migrate from Amazon RDS for Oracle to TiDB Cloud Using AWS DMS

This document describes a step-by-step example of how to migrate data from Amazon RDS for Oracle to [TiDB Serverless](https://tidbcloud.com/console/clusters/create-cluster) using AWS Database Migration Service (AWS DMS).

If you are interested in learning more about TiDB Cloud and AWS DMS, see the following:

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)
- [TiDB Developer Guide](https://docs.pingcap.com/tidbcloud/dev-guide-overview)
- [AWS DMS Documentation](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.html)

## Why use AWS DMS?

AWS DMS is a cloud service that makes it possible to migrate relational databases, data warehouses, NoSQL databases, and other types of data stores.

If you want to migrate data from heterogeneous databases, such as PostgreSQL, Oracle, and SQL Server to TiDB Cloud, it is recommended to use AWS DMS.

## Deployment architecture

At a high level, follow the following steps:

1. Set up the source Amazon RDS for Oracle.
2. Set up the target [TiDB Serverless](https://tidbcloud.com/console/clusters/create-cluster).
3. Set up data migration (full load) using AWS DMS.

The following diagram illustrates the high-level architecture.

![Architecture](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-0.png)

## Prerequisites

Read the following prerequisites before you get started:

- [AWS DMS Prerequisites](/tidb-cloud/migrate-from-mysql-using-aws-dms.md#prerequisites)
- [AWS Cloud Account](https://aws.amazon.com)
- [TiDB Cloud Account](https://tidbcloud.com)
- [DBeaver](https://dbeaver.io/)

Next, you will learn how to use AWS DMS to migrate data from Amazon RDS for Oracle into TiDB Cloud.

## Step 1. Create a VPC

Log in to the [AWS console](https://console.aws.amazon.com/vpc/home#vpcs:) and create an AWS VPC. You need to create Oracle RDS and DMS instances in this VPC later.

For instructions about how to create a VPC, see [Creating a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#Create-VPC).

![Create VPC](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-1.png)

## Step 2. Create an Oracle DB instance

Create an Oracle DB instance in the VPC you just created, and remember the password and grant it public access. You must enable public access to use the AWS Schema Conversion Tool. Note that granting public access in the production environment is not recommended.

For instructions about how to create an Oracle DB instance, see [Creating an Oracle DB instance and connecting to a database on an Oracle DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.Oracle.html).

![Create Oracle RDS](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-2.png)

## Step 3. Prepare the table data in Oracle

Using the following scripts to create and populate 10000 rows of data in the github_events table. You can use the github event dataset and download it from [GH Archive](https://gharchive.org/). It contains 10000 rows of data. Use the following SQL script to execute it in Oracle.

- [table_schema_oracle.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_table_schema.sql)
- [oracle_data.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_data.sql)

After you finish executing the SQL script, check the data in Oracle. The following example uses [DBeaver](https://dbeaver.io/) to query the data:

![Oracle RDS Data](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-3.png)

## Step 4. Create a TiDB Serverless cluster

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters).

2. [Create a TiDB Serverless cluster](/tidb-cloud/tidb-cloud-quickstart.md).

3. In the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the target cluster name to go to its overview page.

4. In the upper-right corner, click **Connect**.

5. Click **Generate Password** to generate a password and copy the generated password.

## Step 5. Create an AWS DMS replication instance

1. Go to the [Replication instances](https://console.aws.amazon.com/dms/v2/home#replicationInstances) page in the AWS DMS console, and switch to the corresponding region.

2. Create an AWS DMS replication instance with `dms.t3.large` in the VPC.

    ![Create AWS DMS Instance](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-8.png)


### Connectivity to TiDB Serverless cluster

You need to make sure the replication instance could connect to the TiDB Serverless cluster, otherwise there is an error like

```shell
Test Endpoint failed: Application-Status: 1020912, Application-Message: Cannot connect to ODBC provider ODBC general error., Application-Detailed-Message: RetCode: SQL_ERROR SqlState: HY000 NativeError: 2003 Message: [MySQL][ODBC 8.0(w) Driver]Can't connect to MySQL server on 'gateway01.eu-central-1.prod.aws.tidbcloud.com' (110)
```

If you are not familiar with AWS network configuration, please consult AWS support. We'll give several typical network settings.

1. To connect to TiDB Serverless public endpoint, you can deploy the replication instance to public subnets and enable `Public accessible` when creation. `Public accessible` is not available for serverless replication.

2. To connect to TiDB Serverless public endpoint, you can deploy the replication instance to private subnets and route the traffic to a public subnet. In this case, you need at least three subnets, two private subnets and one public subnet. The two private subnets forms a subnet group where the replication instance lives in. Then you need to create a NAT gateway in the public subnet and route traffic of the two private subnets to the NAT gateway.

3. To connect to TiDB Serverless private endpoint, [setup a private endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) first and deploy the replication instance to private subnets.

## Step 6. Create DMS endpoints

1. In the [AWS DMS console](https://console.aws.amazon.com/dms/v2/home), click the `Endpoints` menu item on the left pane.

2. Create the Oracle source endpoint. The following screenshot shows the configurations of the source endpoint.

    ![Create AWS DMS Source endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-9.png)

3. Create the TiDB target endpoint. The following screenshot shows the configurations of the target endpoint(using TiDB Serverless public endpoint).

    ![Create AWS DMS Target endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-15.png)

    If you are going to use public endpoint for the migration, we recommend setting `SSL mode` to `verify-full` to ensure security. The `CA certificate` is [ISRG Root X1 certificate](https://letsencrypt.org/certs/isrgrootx1.pem). You can learn more in [TLS Connections to TiDB Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md).

## Step 7. Migrate the schema

In this example, AWS DMS automatically handles the schema, since the schema definition is simple.

If you decide to migrate schema using the AWS Schema Conversion Tool, see [Installing AWS SCT](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Installing.html#CHAP_Installing.Procedure).

For more information, see [Migrating your source schema to your target database using AWS SCT](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SCT.html).

## Step 8. Create a database migration task

1. In the AWS DMS console, go to the [Data migration tasks](https://console.aws.amazon.com/dms/v2/home#tasks) page. Switch to your region. Then click **Create task** in the upper right corner of the window.

    ![Create task](/media/tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2. Create a database migration task and specify the **Selection rules**:

    ![Create AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-11.png)

    ![AWS DMS migration task selection rules](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-12.png)

3. Create the task, start it, and then wait for the task to finish.

4. Click the **Table statistics** to check the table. The schema name is `ADMIN`.

    ![Check AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-13.png)

## Step 9. Check data in the downstream TiDB cluster

Connect to the [TiDB Serverless cluster](https://tidbcloud.com/console/clusters/create-cluster) and check the `admin.github_event` table data. As shown in the following screenshot, DMS successfully migrated table `github_events` and 10000 rows of data.

![Check Data In TiDB](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-14.png)

## Summary

With AWS DMS, you can successfully migrate data from any upstream AWS RDS database following the example in this document.

If you encounter any issues or failures during the migration, you can check the log information in [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) to troubleshoot the issues.

![Troubleshooting](/media/tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## See also

- [Migrate from MySQL-Compatible Databases Using AWS DMS](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
