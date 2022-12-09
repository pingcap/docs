---
title:  Migrate from Amazon RDS for Oracle to TiDB Cloud Serverless Tier Using AWS DMS
summary: Learn how to migrate data from Amazon RDS for Oracle into TiDB Cloud using AWS Database Migration Service (AWS DMS).
---

# Migrate from Amazon RDS for Oracle to TiDB Cloud Serverless Tier Using AWS DMS

This document describes a step-by-step example of how to migrate data from Amazon RDS for Oracle to [TiDB Cloud Serverless Tier](https://tidbcloud.com/console/clusters/create-cluster) using AWS Database Migration Service (AWS DMS).

If you are interested in learning more about TiDB and AWS DMS, you can find some useful links as follows:

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)
- [TiDB Developer Guide](https://docs.pingcap.com/tidbcloud/dev-guide-overview)
- [AWS DMS Documentation](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.html)

## Why use AWS DMS?

AWS Database Migration Service (AWS DMS) is a cloud service that makes it possible to migrate relational databases, data warehouses, NoSQL databases, and other types of data stores.

If you want to migrate data from from heterogeneous databases, such as PostgreSQL, Oracle, and SQL Server to TiDB Cloud, it is recommended to use AWS Database Migration Service (AWS DMS).

## Deployment architecture

At a high level, follow the following steps:

1. Set up source Amazon RDS for Oracle.
2. Set up the target [TiDB Cloud (Serverless) Tier](https://tidbcloud.com/console/clusters/create-cluster).
3. Set up data migration (full load) using AWS DMS.

The following diagram illustrates the high-level architecture.

![Architecture](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-0.png)

## Prerequisites

You might need the following prerequisites:

- [AWS Cloud Account](https://aws.amazon.com)
- [TiDB Cloud Account](https://tidbcloud.com)
- [DBeaver](https://dbeaver.io/)

Next, you will learn how to use DMS tools to migrate data from Amazon RDS for Oracle into TiDB Cloud.

## Step 1. Create a VPC

Log in to the [AWS console](https://console.aws.amazon.com/vpc/home#vpcs:) and create an AWS VPC. You will need to create Oracle RDS and DMS instances in this VPC later.

For instructions about how to create a VPC, see [Creating a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#Create-VPC).

![Create VPC](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-1.png)

## Step 2. Create Oracle DB instanc

Create an Oracle DB instance in VPC, and remember the password and give it public access. You must enable public access to use the AWS Schema Conversion Tool. Note that giving public access in the product environment is not a best practice.

For instructions about how to create an Oracle DB instance, see [Creating an Oracle DB instance and connecting to a database on an Oracle DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.Oracle.html).

![Create Oracle RDS](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-2.png)

## Step 3. Prepare the table data in Oracle

In this step, insert some data into Oracle DB instance. Use the github event dataset, and you can download the data from [GH Archive](https://gharchive.org/). It contains 10000 rows of data. You can use following SQL script to execute in Oracle.

- [table_schema_oracle.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_table_schema.sql)
- [oracle_data.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_data.sql)

After you finish executing the SQL script, check the data in Oracle. The following example uses [DBeaver](https://dbeaver.io/) to query the data:

![Oracle RDS Data](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-3.png)

## Step 4. Create a TiDB Cloud Serverless Tier cluster

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters). Navigate to the **Clusters** page for your project.

2. Create a free serverless TiDB tier.

    ![Create TiDB Cloud Serverless Tier](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-4.png)

3. After the cluster is created, click **Security Settings** to set the user password.

    ![Set TiDB Cloud Serverless Tier Password](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-5.png)

    ![Set TiDB Cloud Serverless Tier Password](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-6.png)

4. Click the **Generate** button and copy to generate the password. Note down the generated password. Then click the **Submit** button.

5. Click the **Connect** button to connect the serverless TiDB:

    ![Connect to TiDB Cloud Serverless Tier](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-7.png)

## Step 5. Create AWS DMS replication instance

1. Go to the [Replication instances](https://console.aws.amazon.com/dms/v2/home#replicationInstances) page in the AWS DMS console, and switch to the corresponding region.

2. Create AWS DMS replication instance with `dms.t3.large` in VPC.

    ![Create AWS DMS Instance](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-8.png)

## Step 6. Create DMS endpoints

1. In the [AWS DMS console](https://console.aws.amazon.com/dms/v2/home), click the replication instance that you just created. 

2. Create the Oracle source endpoint and the TiDB target endpoint.

    ![Create AWS DMS Source endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-9.png)

    ![Create AWS DMS Target endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-10.png)

## Step 7. Migrate the schema

In this example, AWS DMS automatically handles the schema, since the schema definition is simple.

If you decide to migrate schema using the AWS Schema Conversion Tool, see [Installing AWS SCT](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Installing.html#CHAP_Installing.Procedure).

For more information, see [Migrating your source schema to your target database using AWS SCT](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SCT.html).

## Step 8. Create a database migration task

1. In the AWS DMS console, go to the [Data migration tasks](https://console.aws.amazon.com/dms/v2/home#tasks) page. Switch to your region. Then click **Create task** in the upper right corner of the window.

    ![Create task](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2. Create a database migration task and specify the **Selection rules**:

    ![Create AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-11.png)

    ![AWS DMS migration task selection rules](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-12.png)

3. Create the task, start it, and then wait for the task to finish.

4. Click the **Table statistics** to see the synced table. The schema name is ADMIN.

    ![Check AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-13.png)

## Step 9. Check data in the downstream TiDB cluster

Connect to [TiDB Cloud Serverless Tier](https://tidbcloud.com/console/clusters/create-cluster) and check the `admin.github_event` table data. As shown in the following screenshot, DMS successfully migrated table `github_events` and 10000 rows of data.

![Check Data In TiDB](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-14.png)

## Limitation

With AWS DMS, you can successfully migrate data from any upstream AWS RDS database following the example in this document. There is a limitation:

- When you migrate your schema, some character sets or collations are not supported in TiDB, such as `utf8mb4_0900_ai_ci`. For a complete list of TiDB supported charset/collation, see [Character Set and Collation](https://docs.pingcap.com/tidb/stable/character-set-and-collation).
