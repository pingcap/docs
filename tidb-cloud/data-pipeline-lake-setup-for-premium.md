---
title: Set Up Data Pipeline from TiDB Cloud Premium to TiDB Cloud Lake
summary: Learn how to create, monitor, and manage a data pipeline that replicates data from a TiDB Cloud Premium instance to TiDB Cloud Lake.
---

# Set Up Data Pipeline from TiDB Cloud Premium to TiDB Cloud Lake

In TiDB Cloud, you can use Data Pipeline to replicate full data and incremental changes from your TiDB Cloud Premium instance to TiDB Cloud Lake, without requiring a third-party ETL tool. It first exports a full snapshot of the selected source data, and then can continuously replicate row changes so that the data in TiDB Cloud Lake stays up to date.

> **Note:**
>
> - Data Pipeline to TiDB Cloud Lake is currently in **private preview** for {{{ .premium }}} and is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com), and then click **Support Tickets** to go to the [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals). Create a ticket, enter "Apply for `Data Pipeline to TiDB Cloud Lake`" in the **Description** field, and then click **Submit**.
> - The Data Pipeline feature is built on TiCDC, so it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).

## Restrictions

- The TiDB Cloud Lake warehouse must be in the **same region** as your {{{ .premium }}} instance.
- Only tables with a **primary key** can be replicated incrementally. Tables without a primary key are listed in the **Filter results** panel during pipeline creation. If included in the sync scope, their incremental replication is skipped.
- You can create up to 100 changefeeds per {{{ .premium }}} instance. Each data pipeline with incremental replication consumes one changefeed slot.
- Deleting a data pipeline does **not** delete the data already written to TiDB Cloud Lake, nor the target databases and tables in your warehouse.

## Prerequisites

Before you begin, make sure that you have:

- A {{{ .premium }}} instance. Note the region in which it is deployed.
- A warehouse in TiDB Cloud Lake that is in the same region as your instance. If you do not have one yet, create it in the [TiDB Cloud Lake console](https://lake.tidbcloud.com/) first. Only warehouses in the same region as your instance can be selected when you create the data pipeline.
- An S3 bucket for the external stage. Create it in the same region as your instance. Currently, only Amazon S3 is supported.
- The user name and password of a TiDB database user that can read the source tables.

## Create a data pipeline

To create a data pipeline, you need to configure the destination, the external stage, and the replication settings.

### Step 1. Configure the destination

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the overview page of the target {{{ .premium }}} instance, click **Data** > **Data Pipeline** in the left navigation pane, and then click **Create Data Pipeline** in the upper-right corner.
2. In the **Destination** area, configure the following fields:

    - **Destination**: select **TiDB Cloud Lake**.
    - **Warehouse**: select the target warehouse. Only warehouses in the same region as your instance are listed. If no warehouse is available, create one in [TiDB Cloud Lake](https://lake.tidbcloud.com/) first, and then refresh the list.

3. (Optional) Configure the target naming convention in the **Database Prefix**, **Database Suffix**, **Table Prefix**, and **Table Suffix** fields. All four fields are empty by default, which means that the databases and tables created in TiDB Cloud Lake keep the same names as their sources:

    - Database name: `<database prefix><source database name><database suffix>`
    - Table name: `<table prefix><source table name><table suffix>`

### Step 2. Configure the external stage

An external stage is the object storage that bridges the two sides of a data pipeline: TiDB Cloud writes the exported snapshot and the captured row changes to the stage, and TiDB Cloud Lake loads the data from the stage into the target warehouse. For more information, see [Why does a data pipeline require an external stage?](/tidb-cloud/data-pipeline-lake-faq.md#why-does-a-data-pipeline-require-an-external-stage).

Before you configure the external stage, create an Amazon S3 bucket in the same region as your {{{ .premium }}} instance. Currently, only Amazon S3 is supported as the external stage.

1. In the **External Stage** area, enter the **Bucket URI** of your S3 bucket in the `s3://<bucket-name>/<path-to-data>/` format.

    Leave the other fields empty for now. You will fill them in after you configure bucket access using one of the methods described in the following sections.

2. To let TiDB Cloud write data to the external stage and TiDB Cloud Lake read data from it, configure the bucket access in the **Bucket Access** area. Select one of the following methods and complete the authorization accordingly.

    - Method 1: Use an AWS Role ARN (recommended)

        One IAM role is shared by TiDB Cloud (which writes to the stage) and TiDB Cloud Lake (which reads from the stage), so that you configure the authorization only once and no long-lived access key is stored. You can create the role with the CloudFormation template provided by TiDB Cloud, or set it up manually in AWS.

        For the complete AWS-side setup, see [Set Up External Stage for TiDB Cloud Data Pipeline](/tidb-cloud/data-pipeline-lake-configure-external-stage.md#aws). After the role is created, in the TiDB Cloud console, paste the `RoleARN` output value in the **Role ARN** field, and, if you also created an SQS queue, copy the queue URL into the **SQS Queue URL** field.

    - Method 2: Use an AWS access key

        > **Note:**
        >
        > Using an access key and secret key (AK/SK) requires manual credential management and rotation, which increases security risks. For stronger security, use **AWS Role ARN** instead.

        For the complete AWS-side setup, including the IAM user, its permissions, and the optional SQS queue, see [Bucket Access with Access Key](/tidb-cloud/data-pipeline-lake-configure-external-stage.md#option-3-bucket-access-with-access-key-not-recommended). Then, in the TiDB Cloud console, select **AWS Access Key**, and fill in **Access Key ID** and **Secret Access Key**.

    After you have filled in the required information for the method you selected, click **Test Connection** to verify that TiDB Cloud can access the bucket. If the check fails, verify the bucket region and the permissions granted to the role or the access key, and then test the connection again.

### Step 3. Configure replication

In the **Replication Data** area, configure how the data is replicated:

1. **Sync Mode**: select the synchronization mode.

    - **Full Data + Incremental Data** (default): exports a full snapshot of the selected source data, and then continuously replicates row changes. This is the recommended mode for ongoing synchronization.
    - **Full Data**: exports a one-time full snapshot of the selected source data only. No incremental data is replicated, and changes made to the source after the snapshot are ignored.

2. **Sync Interval**: the end-to-end latency target for the data pipeline. The changefeed flush cycle and the TiDB Cloud Lake polling cycle both contribute to the end-to-end latency. Shorter intervals reduce data latency but increase the number of API calls to cloud storage. The default value is shown in the console.

3. **Changefeed Capacity Units**: the processing power allocated for incremental replication, shown together with the maximum replication throughput it supports. For example, `2 CCUs (the maximum replication throughput is 5,000 rows/s)`.

    > **Note:**
    >
    > Changefeed Capacity Units measure the processing power allocated to data streaming. This setting configures the performance of incremental replication. If you select **Full Data** as the sync mode, no CCUs are consumed, because no incremental replication is performed.

4. **TiDB Username** and **TiDB Password**: fill in the user name and password of a TiDB database user. The data pipeline uses this account to export the full snapshot, so the account must have read access to the source tables. Incremental row changes are captured separately by the changefeed.

5. **Sync Objects**: select which objects are replicated.

    - **Customize** (default): specify explicit rules in **Table Filter Rules**. The rule syntax is the same as the [TiCDC table filter rules](https://docs.pingcap.com/tidb/stable/ticdc-filter#table-filter). By default, one `*.*` rule replicates all non-system tables. The **Filter results** panel shows the databases and tables that match the rules.
    - **All**: replicate all tables from all databases. The table filter rules configuration is hidden.

    Optionally, select **Case-sensitive** to make the matching of database and table names in the filter rules case-sensitive. By default, matching is case-insensitive.

    > **Note:**
    >
    > Only tables with a primary key can be replicated incrementally. Tables that lack a primary key are listed separately in the **Filter results** panel, and are skipped for incremental replication. Add a primary key to these tables before you create the data pipeline, or exclude them with filter rules such as `"!test.tbl1"`.

6. **Pipeline Name**: enter a name for the data pipeline.

7. Click **Create**.

    The pipeline enters **Creating** while the full snapshot is being exported. For **Full Data + Incremental Data**, the status changes to **Running** when incremental replication starts.

## Manage the data pipeline

### Edit a data pipeline

To edit a data pipeline, go to the **Data Pipeline** of your target {{{ .premium }}} instance, click **...** in the row of the pipeline, and then click **Edit**.

Editing is disabled while a data pipeline is `Running`. Pause the pipeline first, then edit it, and resume it afterwards to apply the changes.

The destination type and the sync mode cannot be changed after the pipeline is created.

> **Note:**
>
> Changing the table filter rules only affects incremental data going forward:
>
> - Tables that are excluded by the new rules no longer receive incremental data. Data that has already been written is kept.
> - Tables that are added by the new rules receive incremental data only. No historical data is backfilled for them.

### Pause and resume a data pipeline

- **Pause**: stops data replication and marks the pipeline as `Paused`. No data is lost, and the replication progress is preserved. A pipeline cannot be paused while it is being created or while the full snapshot is being exported.
- **Resume**: continues replication from where it was paused, including ingestion into TiDB Cloud Lake.

To pause and resume a data pipeline, go to the **Data Pipeline** of your target {{{ .premium }}} instance, click **...** in the row of the pipeline, and then click **Pause** or **Resume**.

### Delete a data pipeline

To delete a data pipeline, take the following steps:

1. Go to the **Data Pipeline** of your target {{{ .premium }}} instance, click **...** in the row of the pipeline, and then click **Delete**.
2. Read the warning and confirm the operation. Deleting a data pipeline:

    - Immediately stops all data replication.
    - Attempts to remove the TiDB Cloud Lake data source and integration task associated with the pipeline. If the removal fails, these resources might remain and require manual cleanup.
    - **Does not** delete the data already written to TiDB Cloud Lake.
    - **Does not** delete the target databases or tables in the warehouse.

This action cannot be undone.

## See also

- For frequently asked questions about Data Pipeline, see [Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md).
- For details on DDL, DML, and column type support, see [Data Pipeline Support Matrix](/tidb-cloud/data-pipeline-lake-support-matrix.md).
