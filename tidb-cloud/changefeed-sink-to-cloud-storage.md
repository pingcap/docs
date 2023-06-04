---
title: Sink to Cloud Storage
Summary: Learn how to create a changefeed to stream data from a TiDB Dedicated cluster to cloud storage, such as Amazon S3 etc.
---

# Sink to Cloud Storage

This document describes how to stream data from a TiDB Dedicated cluster to cloud storage, such as Amazon S3 etc.


> ## Limitations
> 
> - To use the Changefeed feature, please ensure that your TiDB cluster is running version v6.5.0 or a later version.
> - Each dedicated cluster supports the creation of up to 5 changefeeds.
> - As TiDB Cloud utilizes TiCDC for establishing changefeeds, it inherits the > identical [limitations of TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
> - Replicating data without a primary key or a non-null unique key constraint poses the risk of data redundancy, especially in certain retry scenarios where statements like INSERT and REPLACE are not reentrant.


## Create a changefeed to Cloud Storage

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.

2. Click **Create Changefeed**, and select **Amazon S3** as the destination. Fill in the fields in the **S3 Endpoint** area: `S3 URI`, `Access Key ID` and  `Secret Access Key`.
    ![create changefeed to sink to s3](/media/tidb-cloud/changefeed/sink-to-s3-01-create-changefeed.jpg)


3. Click **Next** to establish the connection from the dedicated TiDB cluster to Amazaon S3, then test and verify if it is successful. If yes, you are directed to the next step of configuration. If not, a connectivity error is displayed, and you need to handle the error. After the error is resolved, click **Next** again.

4. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](https://docs.pingcap.com/tidb/stable/ticdc-filter#changefeed-log-filters).
![the table filter of changefeed](/media/tidb-cloud/changefeed/sink-to-s3-02-table-filter.jpg)

    - **Filter rules**: You can configure filter rules in this column. The default rule is *. *, which means all tables will be replicated. When you add a new rule, TiDB Cloud will query all the tables in TiDB and display only the tables that match the specified rules in the right-hand box.
    - **Tables with valid keys**: This column displays the tables that have valid keys, including primary keys or unique indexes.
    - **Tables without valid keys**: This column shows tables that lack primary keys or unique keys. These tables present a challenge during replication because the absence of a unique identifier can result in inconsistent data when handling duplicate events downstream. To ensure data consistency, it is recommended to add unique keys or primary keys to these tables before initiating replication. Alternatively, you can employ filter rules to exclude these tables. For example, you can exclude the table `test.tbl1` by using the rule "!test.tbl1".


5. In the **Start Replication Position** area, select one of the following replication positions:
    - Start replication from now on
    - Start replication from a specific [TSO](https://docs.pingcap.com/tidb/stable/glossary#tso)
    - Start replication from a specific time

6. In the **Data Format** area, select either the `CSV` or `Canal-JSON` format.

<SimpleTab>
<div label="Configure CSV Format">
To configure the `CSV` format:

![the data format of CSV](/media/tidb-cloud/changefeed/sink-to-s3-02-data-format-csv-conf.jpg)

- **Data Separator**: To rotate data based on the year, month, and day, or choose not to rotate at all.
- **Delimiter**: Specify the character used to separate values in the CSV file. The comma (,) is the most commonly used delimiter.
- **Quote**: Specify the character used to enclose values that contain the delimiter character or special characters. Typically, double quotes (") are used as the quote character.
- **Null/Empty Values**: Specify how null or empty values are represented in the CSV file. This can be important for proper handling and interpretation of the data.
- **Include Commit Ts**

</div>
<div label="Configure Canal-JSON Format">
Canal-JSON is a plain JSON text format, to configure it: 

![the data format of Canal-JSON](/media/tidb-cloud/changefeed/sink-to-s3-02-data-format-canal-json.jpg)

- **Data Separator**: To rotate data based on the year, month, and day, or choose not to rotate at all.
- **Enable TiDB Extention** 

</div>
</SimpleTab>

7. Click **Next** to configure your changefeed specification.

    - In the **Changefeed Specification** area, specify the number of Replication Capacity Units (RCUs) to be used by the changefeed.
    - In the **Changefeed Name** area, specify a name for the changefeed.

8. Click **Next** to review the changefeed configuration. 

    - If you have verified that all configurations are correct, click **Create** to proceed with the creation of the changefeed.

    - If you need to modify any configurations, click **Previous** to go back and make the necessary changes.

9. The sink will start shortly, and you will observe the status of the sink changing from **Creating** to **Running**.


10. Click on the name of the changefeed, and you will be able to view additional details about the changefeed. This includes information such as the checkpoint status, replication latency, and other relevant metrics associated with the changefeed.
