---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
aliases: ['/tidbcloud/beta/tidb-cloud-quickstart']
---

# TiDB Cloud Quick Start

*Estimated completion time: 20 minutes*

This tutorial guides you through an easy way to get started with your TiDB Cloud. The content includes how to create a cluster, try playground, load your data, and connect to your cluster.

## Step 1. Create a TiDB cluster

TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) (Beta) is the best way to get started with TiDB Cloud. To create a free Serverless Tier cluster, take the following steps:

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/free-trial) to sign up for an account.

    For Google or GitHub users, you can also sign up with your Google or GitHub account. Your email address and password will be managed by Google or GitHub and cannot be changed using the TiDB Cloud console.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

    The plan selection page is displayed by default.

3. On the plan selection page, click **Get Started for Free** in the **Serverless Tier** plan.

4. On the **Create Cluster** page, **Serverless Tier** is selected by default. Update the default cluster name if necessary, and then select the region where you want to create your cluster.

5. Click **Create**.

    Your TiDB Cloud cluster will be created in several minutes.

6. During the creation process, perform security settings for your cluster:

    1. Click **Security Settings** in the upper-right corner of the cluster area.
    2. In the **Security Settings** dialog box, set a root password to connect to your cluster, and then click **Apply**. If you do not set a root password, you cannot connect to the cluster.

## Step 2. Try Playground

After your TiDB Cloud cluster is created, you can quickly start experimenting with TiDB using the pre-loaded sample data on TiDB Cloud.

On the **Clusters** page, click **Playground** to run queries instantly on TiDB Cloud.

## Step 3. Load sample data

After trying **Plaground**, you can load sample data to your TiDB Cloud cluster. We provide Capital Bikeshare sample data for you to easily import data and run sample queries.

1. Navigate to the **Clusters** page.

2. In the area of your newly created cluster, click **...** in the upper-right corner and select **Import Data**. The **Data Import** page is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the name of your newly created cluster on the **Clusters** page and click **Import Data** in the **Import** area.

3. Fill in the import parameters:

    - **Data Format**: select **SQL File**
    - **Location**: `AWS`
    - **Bucket URI**: `s3://tidbcloud-samples/data-ingestion/`
    - **Role ARN**: `arn:aws:iam::385595570414:role/import-sample-access`

    If the region of the bucket is different from your cluster, confirm the compliance of cross region. Click **Next**.

4. Add the table filter rules if needed. For the sample data, you can skip this step. Click **Next**.

5. On the **Preview** page, confirm the data to be imported and then click **Start Import**.

The data import process will take several minutes. When the data import progress shows **Finished**, you have successfully imported the sample data and the database schema to your database in TiDB Cloud.

## Step 4. Try TiDB SQL editor

After loading data to the cluster, you can try running SQL statements directly from the console.

1. Navigate to the **Clusters** page.

2. Click the name of your cluster to enter the cluster details page.

3. Hover on the left navigation bar and click **SQL Editor**. The SQL Editor page is displayed.

    In the SQL editor, you can edit and run SQL queries directly against your cluster without using a terminal.

    > **Note:**
    >
    > The SQL editor currently has limited support on SQL statements. DDLs such as `CREATE TABLE` or `DROP TABLE` are not supported yet.

4. In the drop-down list, select `bikeshare`. This is the database where the sample data is imported.

5. To view the tables in the `bikeshare` database, type in the following SQL statement in the editor:

    ```sql
    SHOW tables;
    ```

    To run the query, press **Ctrl + Enter** or click **Run**. You can see the query log and results immediately on the bottom of the page.

6. To show the structure of the `trip` table and count how many records the table contains, type in the two following SQL statements in the editor:

    ```sql
    DESCRIBE trips;
    SELECT COUNT(*) FROM trips;
    ```

    To run the two queries sequentially, you can do one of the following:

    * Press **Control + Shift + Enter**.
    * Select the two queries with your cursor and click **Run**.

    In the query log panel, you can see the two queries are executed one by one.

    If there are two or more queries in the editor, pressing **Control + Enter** or clicking **Run** only runs the query that is being highlighted in the editor.

You are now ready to use TiDB Cloud to build your applications.

## What's next

- For how to connect to your cluster via a SQL client, refer to [Connect to a TiDB Cluster](/tidb-cloud/connect-to-tidb-cluster.md).
- For more details on TiDB SQL usage, see [Explore SQL with TiDB](/basic-sql-operations.md).
- For production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing), refer to [Create a TiDB Cluster](/tidb-cloud/create-tidb-cluster.md) and create a Dedicated Tier cluster.
