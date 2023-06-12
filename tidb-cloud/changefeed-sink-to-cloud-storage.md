---
title: Sink to Cloud Storage
Summary: Learn how to create a changefeed to stream data from a TiDB Dedicated cluster to cloud storage, such as Amazon S3 etc.
---

# Sink to Cloud Storage

This document describes how to create a changefeed to stream data from TiDB Cloud to cloud storage. Currently, only Amazon S3 is supported.

> **Note:**
>
> To stream data to cloud storage, make sure that your TiDB cluster version is v7.1.0 or later.
>
> For [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta) clusters, the changefeed feature is unavailable.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 5 changefeeds.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.

## Create a changefeed

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.

2. Click **Create Changefeed**, and select **Amazon S3** as the destination.

3. Fill in the fields in the **S3 Endpoint** area: `S3 URI`, `Access Key ID` and  `Secret Access Key`.

    ![create changefeed to sink to s3](/media/tidb-cloud/changefeed/sink-to-s3-01-create-changefeed.jpg)

4. Click **Next** to establish the connection from the dedicated TiDB cluster to Amazaon S3, then test and verify if the connection is successful.

    - If yes, you are directed to the next step of configuration.
    - If not, a connectivity error is displayed, and you need to handle the error. After the error is resolved, click **Next** again.

5. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](https://docs.pingcap.com/tidb/stable/ticdc-filter#changefeed-log-filters).

    ![the table filter of changefeed](/media/tidb-cloud/changefeed/sink-to-s3-02-table-filter.jpg)

    - **Filter Rules**: you can set filter rules in this column. By default, there is a rule `*.*`, which stands for replicating all tables. When you add a new rule, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules in the box on the right.
    - **Tables with valid keys**: this column displays the tables that have valid keys, including primary keys or unique indexes.
    - **Tables without valid keys**: This column shows tables that lack primary keys or unique keys. These tables present a challenge during replication because the absence of a unique identifier can result in inconsistent data when handling duplicate events downstream. To ensure data consistency, it is recommended to add unique keys or primary keys to these tables before initiating the replication. Alternatively, you can employ filter rules to exclude these tables. For example, you can exclude the table `test.tbl1` by using the rule `"!test.tbl1"`.

6. In the **Start Replication Position** area, select one of the following replication positions:

    - Start replication from now on
    - Start replication from a specific [TSO](https://docs.pingcap.com/tidb/stable/glossary#tso)
    - Start replication from a specific time

7. In the **Data Format** area, select either the `CSV` or `Canal-JSON` format.

    <SimpleTab>
    <div label="Configure CSV Format">

    To configure the `CSV` format, fill in the following fields:

    ![the data format of CSV](/media/tidb-cloud/changefeed/sink-to-s3-02-data-format-csv-conf.jpg)

    - **Date Separator**: To rotate data based on the year, month, and day, or choose not to rotate at all.
    - **Delimiter**: Specify the character used to separate values in the CSV file. The comma (`,`) is the most commonly used delimiter.
    - **Quote**: Specify the character used to enclose values that contain the delimiter character or special characters. Typically, double quotes (`"`) are used as the quote character.
    - **Null/Empty Values**: Specify how null or empty values are represented in the CSV file. This can be important for proper handling and interpretation of the data.
    - **Include Commit Ts**

    </div>
    <div label="Configure Canal-JSON Format">

    Canal-JSON is a plain JSON text format. To configure it, fill in the following fields:

    ![the data format of Canal-JSON](/media/tidb-cloud/changefeed/sink-to-s3-02-data-format-canal-json.jpg)

    - **Date Separator**: To rotate data based on the year, month, and day, or choose not to rotate at all.
    - **Enable TiDB Extension**

    </div>
    </SimpleTab>

8. Click **Next** to configure your changefeed specification.

    - In the **Changefeed Specification** area, specify the number of replication capacity units (RCUs) to be used by the changefeed.
    - In the **Changefeed Name** area, specify a name for the changefeed.

9. Click **Next** to review the changefeed configuration.

    - If you have verified that all configurations are correct, click **Create** to proceed with the creation of the changefeed.

    - If you need to modify any configurations, click **Previous** to go back and make the necessary changes.

10. The sink will start shortly, and you will observe the status of the sink changing from **Creating** to **Running**.

11. Click on the name of the changefeed, and you will be able to view additional details about the changefeed. This includes information such as the checkpoint status, replication latency, and other relevant metrics associated with the changefeed.
