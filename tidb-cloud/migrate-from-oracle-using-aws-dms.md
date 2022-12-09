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

## What is AWS DMS?

AWS Database Migration Service (AWS DMS) is a cloud service that makes it possible to migrate relational databases, data warehouses, NoSQL databases, and other types of data stores.

## Why use AWS DMS?

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

Next, you will learn how to use DMS tools to migrateAmazon RDS for Oracle data to TiDB.

## Step 1. Create a VPC

Create an AWS VPC. You will need to create Oracle RDS and DMS instances in this VPC later.

![Create VPC](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-1.png)

## Step 2. Create Oracle RDS

Create an AWS Oracle RDS in VPC, and remember the password and give it public access. You must enable public access to use the AWS Schema Conversion Tool. Note that giving public access in the product environment is not a best practice.

![Create Oracle RDS](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-2.png)

## Step 3. Prepare table data in Oracle

In this step, insert some data into Oracle RDS. Use the github event dataset, and you can download the data from [GH Archive](https://gharchive.org/). It contains 10000 rows of data and you can use following SQL script to execute in Oracle.

- [table_schema_oracle.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_table_schema.sql)
- [oracle_data.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_data.sql)

After you finish executed the SQL script, you can check the data in Oracle, Here we use [DBeaver](https://dbeaver.io/) to query the data:

![Oracle RDS Data](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-3.png)

## Step 4. Create TiDB Cloud Serverless Tier

After registering and logging in, you can create a free serverless TiDB tier.

![Create TiDB Cloud Serverless Tier](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-4.png)

After the cluster is created, you will see the following, and then click **Security Settings** to set the user password.

![Set TiDB Cloud Serverless Tier Password](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-5.png)

![Set TiDB Cloud Serverless Tier Password](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-6.png)

After you fill the password, click the generate and copy to generate password, and importantly remember the generated password. Then, click the submit button.

Next, click the Connect button, you can see how to connect the serverless TiDB:

![Connect to TiDB Cloud Serverless Tier](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-7.png)

## Step 5. Create AWS DMS Replication Instance

Create AWS DMS Replication instance with `dms.t3.large` in VPC.

![Create AWS DMS Instance](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-8.png)

## Step 6. Create DMS Endpoint

Create Oracle source endpoint and TiDB target endpoint.

![Create AWS DMS Source endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-9.png)

![Create AWS DMS Source endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-10.png)

## Step 7. Migrating Schema

As the [DMS official documentation](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SCT.html), we may need to migrate schema using [AWS Schema Conversion Tool](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Installing.html#CHAP_Installing.Procedure), but in this example we will let DMS auto handle the schema, since the schema definition is pretty simple.

## Step 8. Create DMS Database Migration Task

On AWS Management Console, Create DMS Migration Task and specify the **Selection rules**:

![Create AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-11.png)

![AWS DMS migration task selection rules](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-12.png)

Then create the task, start it, and then wait for the task to finish.

Then click the **Table statistics** to see the synced table, remember the schema name is ADMIN:

![Check AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-13.png)

## Step 9. Check data In Downstream TiDB Cloud Serverless Tier

Connect to [TiDB Cloud Serverless Tier](https://tidbcloud.com/console/clusters/create-cluster) and check the `admin.github_event` table data, as you can see, DMS successfully synced table github_events and 10000 rows data.

![Check Data In TiDB](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-14.png)

## Conclusion

With AWS DMS, you can successfully migrate data from ANY upstream AWS RDS database in this case we used Oracle to [TiDB Cloud Serverless Tier](https://tidbcloud.com/console/clusters/create-cluster) With the following exceptions:

- when you migrate your schema, some charset/collation is not supported in TiDB, such as `utf8mb4_0900_ai_ci`. A complete list of [TiDB supported charset/collation doc can be found here](https://docs.pingcap.com/tidb/v6.3/character-set-and-collation).
