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

You can either create a free [Developer Tier](/tidb-cloud/select-cluster-tier.md#developer-tier) cluster or a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier).

<SimpleTab>
<div label="Developer Tier">

To create a free Developer Tier cluster, take the following steps:

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/free-trial) to sign up for an account.

    - For Google users, you can also sign up with Google. To do that, click **Sign up with Google** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by Google and cannot be changed using TiDB Cloud console.
    - For GitHub users, you can also sign up with GitHub. To do that, click **Sign up with GitHub** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by GitHub and cannot be changed using TiDB Cloud console.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

    The plan selection page is displayed by default.

3. On the plan selection page, click **Get Started for Free** in the **Developer Tier** plan.

4. On the **Create Cluster** page, **Developer Tier** is selected by default. Update the default cluster name if necessary, and then select the region where you want to create your cluster.

5. Click **Create**.

   The cluster creation process starts and the **Security Settings** dialog box is displayed.

6. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

    Your TiDB Cloud cluster will be created in approximately 5 to 15 minutes.

</div>

<div label="Dedicated Tier">

To create a Dedicated Tier cluster, take the following steps:

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

    - For Google users, you can also sign up with Google. To do that, click **Sign up with Google** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by Google and cannot be changed using TiDB Cloud console.
    - For GitHub users, you can also sign up with GitHub. To do that, click **Sign up with GitHub** on the [sign up](https://tidbcloud.com/signup) page. Your email address and password will be managed by GitHub and cannot be changed using TiDB Cloud console.
    - For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

    The plan selection page is displayed by default.

3. On the plan selection page, click **Get Full Access Today** in the **Dedicated Tier** plan.

4. On the **Create a Cluster** page, **Dedicated Tier** is selected by default. Update the default cluster name and port number if necessary, choose a cloud provider and a region, and then click **Next**.

    > **Note:**
    >
    > If you want to get a 14-day free trial of TiDB Cloud Dedicated Tier first, see [Perform a Proof of Concept (PoC) with TiDB Cloud](/tidb-cloud/tidb-cloud-poc.md).

5. If this is the first cluster of your current project and CIDR has not been configured for this project, you need to set the project CIDR, and then click **Next**. If you do not see the **project CIDR** field, it means that CIDR has already been configured for this project.

    > **Note:**
    >
    > When setting the project CIDR, avoid any conflicts with the CIDR of the VPC where your application is located. The CIDR of a project cannot be modified once it is set.

6. Configure the [cluster size](/tidb-cloud/size-your-cluster.md) for TiDB, TiKV, and TiFlash (optional) respectively, and then click **Next**.

7. Confirm the cluster information on the page and also the billing information in the lower-left corner.

8. Click **Add Credit Card** in the lower-right corner to add a credit card for your account.

9. Click **Create**.

   The cluster creation process starts and the **Security Settings** dialog box is displayed.

10. In the **Security Settings** dialog box, set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

    Your TiDB Cloud cluster will be created in approximately 5 to 15 minutes.

</div>
</SimpleTab>

## Step 2. Connect to your TiDB cluster

1. Navigate to the **Active Clusters** page.

2. In the area of your newly created cluster, click **Connect** in the upper-right corner. A connection dialog box is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the name of your newly created cluster on the **Active Clusters** page and click **Connect** in the upper-right corner.

3. Under **Step 2: Connect with a SQL client** in the dialog box, click the tab of your preferred connection method, and then connect to your cluster with the connection string.

    > **Note:**
    >
    > - For [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier), when you connect to your cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).
    > - TiDB Cloud is MySQL-compatible, so you can connect to your cluster using any MySQL client tools. We recommend using [mysql — The MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) or [mysql — The MySQL Command-Line Client from MariaDB](https://mariadb.com/kb/en/mysql-command-line-client/).

4. After logging into your TiDB cluster, you can use the following SQL statement to validate the connection:

    {{< copyable "sql" >}}

    ```sql
    SELECT TiDB_version();
    ```

    If you see the release version information, you are ready to use your TiDB cluster.

## Step 3. Import the sample data

We provide Capital Bikeshare sample data for you to easily import data and run sample queries.

1. Navigate to the **Active Clusters** page.
2. In the area of your newly created cluster, click **Import Data** in the upper-right corner. The **Data Import Task** page is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the name of your newly created cluster on the **Active Clusters** page and click **Import Data** in the upper-right corner.

3. Fill in the import parameters:

    <SimpleTab>
    <div label="AWS">

    If your TiDB cluster is hosted by AWS (the Developer Tier is hosted by AWS by default), fill in the following parameters:

    - **Data Source Type**: `AWS S3`.
    - **Bucket URL**: enter the sample data URL `s3://tidbcloud-samples/data-ingestion/`.
    - **Data Format**: select **TiDB Dumpling**.
    - **Setup Credentials**: enter `arn:aws:iam::385595570414:role/import-sample-access` for Role-ARN.
    - **Target Database**:
        - **Username**: `root`.
        - **Password**: enter your root password.
    - **DB/Tables Filter**: leave this field blank.

    </div>

    <div label="GCP">

    If your TiDB cluster is hosted by GCP, fill in the following parameters:

    - **Data Source Type**: `Google Cloud Stroage`.
    - **Bucket URL**: enter the sample data URL `gcs://tidbcloud-samples-us-west1`.
    - **Data Format**: select **TiDB Dumpling**.
    - **Target Database**:
        - **Username**: `root`.
        - **Password**: enter your root password.
    - **DB/Tables Filter**: leave this field blank.

    </div>
    </SimpleTab>

4. Click **Import**.

    A warning message about the database resource consumption is displayed. For a newly created cluster, you can ignore the warning message.

5. Click **Confirm**.

    TiDB Cloud starts validating whether it can access the sample data in the specified bucket URL. After the validation is completed and successful, the import task starts automatically.

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
