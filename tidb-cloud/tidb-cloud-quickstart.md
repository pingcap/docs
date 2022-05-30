---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
aliases: ['/tidbcloud/beta/tidb-cloud-quickstart']
---

# TiDB Cloud Quick Start

*Estimated completion time: 20 minutes*

This tutorial guides you through an easy way to get started with your TiDB Cloud. The content includes how to create a cluster, connect to a cluster, import data, and run queries.

## Step 1. Create a TiDB cluster

You can either create a free [Developer Tier (Dev Tier)](select-cluster-tier.md#developer-tier) cluster or a [Dedicated Tier](select-cluster-tier.md#dedicated-tier).

<SimpleTab>
<div label="Developer Tier">

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

    - For Google users, you can also sign up with Google. To do that, click **Sign up with Google** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by Google and cannot be changed using TiDB Cloud console.
    - For GitHub users, you can also sign up with GitHub. To do that, click **Sign up with GitHub** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by GitHub and cannot be changed using TiDB Cloud console.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

    The plan selection page is displayed by default.

3. On the plan selection page, click **Get Started for Free** in the **Developer Tier** plan.

4. On the **Create a Cluster (Dev Tier)** page, set up your cluster name and root password.

5. Note that the cloud provider of Developer Tier is AWS, and then select the region where you want to create your cluster.

6. View the cluster size of the Developer Tier, and then click **Create**.

Your TiDB Cloud cluster will be created in approximately 5 to 15 minutes.

</div>

<div label="Dedicated Tier">

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

    - For Google users, you can also sign up with Google. To do that, click **Sign up with Google** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by Google and cannot be changed using TiDB Cloud console.
    - For GitHub users, you can also sign up with GitHub. To do that, click **Sign up with GitHub** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by GitHub and cannot be changed using TiDB Cloud console.
    - For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

    The plan selection page is displayed by default.

3. On the plan selection page, click **Get Full Access Today** in the **On Demand** plan.

    > **Note:**
    >
    > If you want to get a 14-day free trial of TiDB Cloud first, click **Apply for a PoC Trial** in the **Proof of Concept** plan, fill in the application form, and then click **OK**. The PingCAP support team will get back to you in 48 hours. For more information, see [Perform a Proof of Concept (PoC) with TiDB Cloud](tidb-cloud-poc.md).

4. On the **Create a Cluster** page, set up your cluster name and root password, and then update the default port number `4000` if you cannot use `4000` for connection.

5. Choose a cloud provider and a region, and then click **Next**.

6. If this is the first cluster of your current project and CIDR has not been configured for this project, you need to set the project CIDR, and then click **Next**. If you do not see the **project CIDR** field, it means that CIDR has already been configured for this project.

    > **Note:**
    >
    > When setting the project CIDR, avoid any conflicts with the CIDR of the VPC where your application is located. The CIDR of a project cannot be modified once it is set.

7. Configure the [cluster size](size-your-cluster.md) for TiDB, TiKV, and TiFlash<sup>beta</sup> (optional) respectively, and then click **Next**.

8. Confirm the cluster information in the middle area and also the billing information in the right pane.

9. Click **Add Credit Card** in the right pane to add a credit card for your account.

10. Click **Create**.

Your TiDB Cloud cluster will be created in approximately 5 to 15 minutes.

</div>
</SimpleTab>

## Step 2. Connect to your TiDB cluster

1. Navigate to the TiDB Clusters page and click the name of your newly created cluster.

    The overview page of your newly created cluster is displayed.

2. Click **Connect**. The **Connect to TiDB** dialog box is displayed.

3. In **Step 1: Create traffic filter**, click **Add Your Current IP Address**, and then click **Create Filter**.

    The purpose of this step is to set up your traffic filter, which makes sure that the cluster accepts connections only from trusted IP addresses.

4. In **Step 2: Connect with a SQL client**, use an SQL client to connect to your cluster.

    TiDB Cloud is MySQL-compatible, so you can connect to your cluster using any MySQL client tools. We recommend using [mysql — The MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) or [mysql — The MySQL Command-Line Client from MariaDB](https://mariadb.com/kb/en/mysql-command-line-client/).

5. In the **Connect to TiDB** dialog box, copy the command provided in **Step 2: Connect with a SQL client**, and paste it into your Terminal interface.

    The format of the command line is as follows, but you need to customize your endpoint.

    {{< copyable "shell" >}}

    ```shell
    mysql -u root -h <endpoint> -P <port number> -p
    ```

6. Enter the root password you used when creating the cluster.

7. Validate the connection in the MySQL client:

    {{< copyable "sql" >}}

    ```sql
    SELECT TiDB_version();
    ```

    If you see the release version information, you are ready to play with the MySQL client on your TiDB Cloud cluster.

## Step 3. Import the sample data

We provide Capital Bikeshare sample data for you to easily import data and run sample queries.

1. Navigate to the TiDB Clusters page and click the name of your newly created cluster. The overview page of your cluster is displayed.

2. In the cluster information pane on the left, click **Import**. The **Data Import Task** page is displayed.

3. Depending on where your TiDB cluster is hosted, do one of the following:

    - If your TiDB cluster is hosted by AWS (the Dev Tier is hosted by AWS by default), select **AWS S3** as the data source type, enter the bucket URL of the sample data, and select the bucket region.

         **Your bucket URL and region should correspond to your target database region.** For example, if you create a cluster in US-West-2 (Oregon), you should choose the sample data URL of the bucket region of US-West-2 (Oregon) from the following list:

        - US-West-2 (Oregon): `s3://tidbcloud-samples-us-west-2/data-ingestion/`
        - US-East-1 (Virginia): `s3://tidbcloud-samples-us-east-1/data-ingestion/`
        - AP-Northeast-1 (Tokyo): `s3://tidbcloud-samples-ap-northeast-1/data-ingestion/`
        - AP-Southeast-1 (Singapore): `s3://tidbcloud-samples-ap-southeast-1/data-ingestion/`

    - If your TiDB cluster is hosted by GCP, select **Google Cloud Storage** for **Data Source Type**, enter the sample data URL `gcs://tidbcloud-samples-us-west1` in the **Bucket URL** field, and then select **US-West1 (Oregon)** for **Bucket Region**. The sample data bucket is hosted in the US-West1 (Oregon) for GCP.

4. Fill in the other import parameters.

    - Data Format: Select **TiDB Dumpling**.
    - Setup Credentials: Enter `arn:aws:iam::385595570414:role/import-sample-access` for Role-ARN.
    - Target Database:
        - Username: `root`.
        - Password: Enter your root password.
    - DB/Tables Filter: Leave this field blank.

5. Click **Import**.

    The data import process will take 5 to 10 minutes. When the data import progress bar shows **Success**, you successfully import the sample data and the database schema in your database.

## Step 4. Query data

When the process of importing data is completed, you can start to run some queries in your Terminal:

1. Use the `bikeshare` database and tables:

    {{< copyable "sql" >}}

    ```sql
    USE bikeshare;
    SHOW tables;
    ```

2. Check the structure of the `trip` table:

    {{< copyable "sql" >}}

    ```sql
    DESCRIBE trips;
    ```

3. Check how many records exist in the `trips` table:

    {{< copyable "sql" >}}

    ```sql
    SELECT COUNT(*) FROM trips;
    ```

4. Check the entire trip history where the start station is "8th & D St NW":

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM trips WHERE start_station_name = '8th & D St NW';
    ```

5. Show the least ten popular bicycle stations for picking up:

    {{< copyable "sql" >}}

    ```sql
    SELECT start_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name
    ORDER BY count ASC
    LIMIT 10;
    ```
