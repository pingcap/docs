---
title: Sink to TiDB Cloud Serverless Tier clusters
Summary: Learn how to create a changefeed to stream data from TiDB Cloud Dedicated Tier clusters to TiDB Cloud Serverless Tier clusters.
---

# Sink to TiDB Cloud

This document describes how to stream data from TiDB Cloud Dedicated Tier clusters to TiDB Cloud Serverless Tier clusters.

> **Note:**
>
> To use the Changefeed feature, make sure that your TiDB cluster version is v6.4.0 or later.
>
> Currently, TiDB Cloud only allows up to 5 changefeeds per cluster.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 5 changefeeds.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.
- The **Sink to TiDB Cloud** feature is only available to TiDB Cloud Dedicated Tier clusters that are in the following AWS regions and created after November 9, 2022:

    - AWS Oregon (us-west-2)
    - AWS Frankfurt (eu-central-1)
    - AWS Singapore (ap-southeast-1)
    - AWS Tokyo (ap-northeast-1)

- The **Sink to TiDB Cloud** feature only supports network connection via private endpoints. When you create a changefeed to stream data from a TiDB Cloud Dedicated Tier cluster to a TiDB Cloud Serverless Tier cluster, TiDB Cloud will automatically set up the private endpoint network connection between the two clusters.

## Prerequisites

Before creating a changefeed, you need to complete the following prerequisites:

- [Export and load existing data to the target Serverless Tier cluster](#load-existing-data-recommended) (recommended).
- Create corresponding target tables in the destination Serverless Tier cluster if you do not load the existing data and only want to replicate incremental data to the destination Serverless Tier cluster.

### Load existing data (recommended)

The **Sink to TiDB Cloud** connector can only sink incremental data from a TiDB Cloud Dedicated Tier cluster to a Serverless Tier cluster after a certain [TSO](https://docs.pingcap.com/tidb/stable/glossary#tso). If you have existing data in your TiDB Cloud Dedicated Tier cluster, you can export and load them into the destination Serverless Tier cluster before enabling **Sink to TiDB Cloud**.

To load the existing data:

1. Extend the [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) to be longer than the total time of the following two operations, so that historical data during the time is not garbage collected by TiDB.

    - The time to export and import the existing data
    - The time to create **Sink to TiDB Cloud**

    For example:

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. [Export data](/tidb-cloud/export-data-from-tidb-cloud.md) from your TiDB Cloud Dedicated Tier cluster, then use community tools such as [mydumper/myloader](https://centminmod.com/mydumper.html) to load data to the destination Serverless Tier cluster.

3. From the [exported files of Dumpling](/dumpling-overview.md#format-of-exported-files), get the start position of TiDB Cloud sink from the metadata file:

    The following is a part of an example metadata file. The `Pos` of `SHOW MASTER STATUS` is the TSO of the existing data, which is also the start position of TiDB Cloud sink.

    ```
    Started dump at: 2023-03-28 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2023-03-28 10:40:20
    ```

### Create target tables in the destination Serverless Tier cluster

If you do not load the existing data, you need to create corresponding target tables in the destination Serverless Tier cluster manually to store the incremental data from the source Dedicated Tier cluster. Otherwise, the data will not be replicated.

## Create a TiDB Cloud sink

After completing the prerequisites, you can sink your data to the destination Serverless Tier cluster.

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.

2. Click **Create Changefeed**, and select **TiDB Cloud** as the destination.

3. In the **TiDB Cloud Connection** area, select the destination Serverless Tier cluster, and then fill in the user name and password of the destination cluster.

4. Click **Next** to establish the connection between the two TiDB clusters and test whether the changefeed can connect them successfully:

    - If yes, you are directed to the next step of configuration.
    - If not, a connectivity error is displayed, and you need to handle the error. After the error is resolved, click **Next** again.

5. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](/table-filter.md).

    - **Filter rules**: you can set filter rules in this column. By default, there is a rule `*. *`, which stands for replicating all tables. When you add a new rule, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules in the box on the right.
    - **Tables to be replicated**: this column shows the tables to be replicated. But it does not show the new tables to be replicated in the future or the schemas to be fully replicated.
    - **Tables without valid keys**: this column shows tables without unique and primary keys. For these tables, because no unique identifier can be used by the downstream system to handle duplicate events, their data might be inconsistent during replication. To avoid such issues, it is recommended that you add unique keys or primary keys to these tables before the replication, or set filter rules to filter out these tables. For example, you can filter out the table `test.tbl1` using "!test.tbl1".

6. In **Start Position**, configure the starting position for your TiDB Cloud sink.

    - If you have [loaded the existing data](#load-existing-data-optional) using Dumpling, select **Start replication from a specific TSO** and fill in the TSO that you get from Dumpling exported metadata files.

    <!--
    - If you do not have any data in the upstream TiDB cluster, select **Start replication from now on**.
    - Otherwise, you can customize the start time point by choosing **Start replication from a specific time**.
    -->

7. Click **Next** to configure your changefeed specification.

    - In the **Changefeed Specification** area, specify the number of Replication Capacity Units (RCUs) to be used by the changefeed.
    - In the **Changefeed Name** area, specify a name for the changefeed.

8. Click **Next** to review the Changefeed configuration.

    If you confirm all configurations are correct, check the compliance of cross-region replication, and click **Create**.

    If you want to modify some configurations, click **Previous** to go back to the previous configuration page.

9. The sink starts soon, and you can see the status of the sink changes from "**Creating**" to "**Running**".

    Click the Changefeed name, and you can see more details about the changefeed, such as the checkpoint, replication latency, and other metrics.

10. If you have [loaded the existing data](#load-existing-data-optional) using Dumpling, you need to restore the GC time to its original value (the default value is `10m`) after the sink is created:

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '10m';
    ```
