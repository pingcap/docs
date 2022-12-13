---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
aliases: ['/tidbcloud/beta/tidb-cloud-quickstart']
---

# TiDB Cloud Quick Start

*Estimated completion time: 20 minutes*

This tutorial guides you through an easy way to get started with your TiDB Cloud. The content includes how to create a cluster, try Playground, load your data, and try running SQL statements in the TiDB Cloud console.

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

6. After the creation is completed, perform security settings for your cluster:

    1. Click **Security Settings** in the upper-right corner of the cluster area.
    2. In the **Security Settings** dialog box, set a root password to connect to your cluster, and then click **Apply**. If you do not set a root password, you cannot connect to the cluster.

## Step 2. Try Playground

After your TiDB Cloud cluster is created, you can quickly start experimenting with TiDB using the pre-loaded sample data on TiDB Cloud.

On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click **Playground** to run queries instantly on TiDB Cloud.

## Step 3. Load sample data

After trying **Plaground**, you can load sample data to your TiDB Cloud cluster. We provide Capital Bikeshare sample data for you to easily import data and run sample queries.

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.

2. In the area of your newly created cluster, click **...** in the upper-right corner and select **Import Data**. The **Data Import** page is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the name of your newly created cluster on the **Clusters** page and click **Import Data** in the **Import** area.

3. Fill in the import parameters:

    - **Data Format**: select **SQL File**
    - **Location**: select **AWS**
    - **Bucket URI**: `s3://tidbcloud-samples/data-ingestion/`
    - **Role ARN**: `arn:aws:iam::385595570414:role/import-sample-access`

    If the region of the bucket is different from your cluster, confirm the compliance of cross region. Click **Next**.

4. Add the table filter rules if needed. For the sample data, you can skip this step. Click **Next**.

5. On the **Preview** page, confirm the data to be imported and then click **Start Import**.

The data import process will take several minutes. When the data import progress shows **Finished**, you have successfully imported the sample data and the database schema to your database in TiDB Cloud.

## Step 4. Try TiDB SQL editor (Beta)

After loading data to the cluster, you can try running SQL statements directly from the console.

1. Click **SQL Editor** on the left navigation bar. The SQL Editor page is displayed.

    In the SQL editor, you can edit and run SQL queries directly against your cluster without using a terminal.

    > **Note:**
    >
    > The SQL editor currently has limited support on SQL statements. DDLs such as `CREATE TABLE` or `DROP TABLE` are not supported yet.

2. In the editor, type in the following SQL statement:

    ```sql
    SHOW databases;
    ```

    To run the query, press **Control + Enter** or click <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run**. You can see the query log and results immediately on the bottom of the page.

3. To view the tables in the `bikeshare` database, type in the following SQL statements:

    ```sql
    USE bikeshare;
    SHOW tables;
    ```

    To run the two queries sequentially, you can do one of the following:

    * Press **Control + Shift + Enter**.
    * Select the two queries with your cursor and click **Run**.

    In the query log panel, you can see the two queries are executed one by one.

    If there are two or more queries in the editor, pressing **Control + Enter** or clicking **Run** only runs the query that is being highlighted in the editor.

4. To show the structure of the `trip` table and count how many records the table contains, run the two following SQL statements in the editor:

    ```sql
    DESCRIBE trips;
    SELECT COUNT(*) FROM trips;
    ```

You are now ready to use TiDB Cloud to build your applications.

## What's next

- For how to connect to your cluster via a SQL client, refer to [Connect to a TiDB Cluster](/tidb-cloud/connect-to-tidb-cluster.md).
- For more details on TiDB SQL usage, see [Explore SQL with TiDB](/basic-sql-operations.md).
- For production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing), refer to [Create a TiDB Cluster](/tidb-cloud/create-tidb-cluster.md) and create a Dedicated Tier cluster.
