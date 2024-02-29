---
title: Sink to TiDB Cloud
summary: This document explains how to stream data from a TiDB Dedicated cluster to a TiDB Serverless cluster. There are restrictions on the number of changefeeds and regions available for the feature. Prerequisites include extending tidb_gc_life_time, backing up data, and obtaining the start position of TiDB Cloud sink. To create a TiDB Cloud sink, navigate to the cluster overview page, establish the connection, customize table and event filters, fill in the start replication position, specify the changefeed specification, review the configuration, and create the sink. Finally, restore tidb_gc_life_time to its original value.
---

# Sink to TiDB Cloud

This document describes how to stream data from a TiDB Dedicated cluster to a TiDB Serverless cluster.

> **Note:**
>
> To use the Changefeed feature, make sure that your TiDB Dedicated cluster version is v6.1.3 or later.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 100 changefeeds.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.
- The **Sink to TiDB Cloud** feature is only available to TiDB Dedicated clusters that are in the following AWS regions and created after November 9, 2022:

    - AWS Oregon (us-west-2)
    - AWS Frankfurt (eu-central-1)
    - AWS Singapore (ap-southeast-1)
    - AWS Tokyo (ap-northeast-1)
    - AWS São Paulo (sa-east-1)

- The source TiDB Dedicated cluster and the destination TiDB Serverless cluster must be in the same project and the same region.
- The **Sink to TiDB Cloud** feature only supports network connection via private endpoints. When you create a changefeed to stream data from a TiDB Dedicated cluster to a TiDB Serverless cluster, TiDB Cloud will automatically set up the private endpoint connection between the two clusters.

## Prerequisites

The **Sink to TiDB Cloud** connector can only sink incremental data from a TiDB Dedicated cluster to a TiDB Serverless cluster after a certain [TSO](https://docs.pingcap.com/tidb/stable/glossary#tso).

Before creating a changefeed, you need to export existing data from the source TiDB Dedicated cluster and load the data to the destination TiDB Serverless cluster.

1. Extend the [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) to be longer than the total time of the following two operations, so that historical data during the time is not garbage collected by TiDB.

    - The time to export and import the existing data
    - The time to create **Sink to TiDB Cloud**

    For example:

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. [Back up data](/tidb-cloud/backup-and-restore.md#backup) from your TiDB Dedicated cluster, then use community tools such as [mydumper/myloader](https://centminmod.com/mydumper.html) to load data to the destination TiDB Serverless cluster.

3. From the [exported files of Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files), get the start position of TiDB Cloud sink from the metadata file:

    The following is a part of an example metadata file. The `Pos` of `SHOW MASTER STATUS` is the TSO of the existing data, which is also the start position of TiDB Cloud sink.

    ```
    Started dump at: 2023-03-28 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2023-03-28 10:40:20
    ```

## Create a TiDB Cloud sink

After completing the prerequisites, you can sink your data to the destination TiDB Serverless cluster.

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.

2. Click **Create Changefeed**, and select **TiDB Cloud** as the destination.

3. In the **TiDB Cloud Connection** area, select the destination TiDB Serverless cluster, and then fill in the user name and password of the destination cluster.

4. Click **Next** to establish the connection between the two TiDB clusters and test whether the changefeed can connect them successfully:

    - If yes, you are directed to the next step of configuration.
    - If not, a connectivity error is displayed, and you need to handle the error. After the error is resolved, click **Next** again.

5. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](/table-filter.md).

    - **Filter Rules**: you can set filter rules in this column. By default, there is a rule `*.*`, which stands for replicating all tables. When you add a new rule, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules in the box on the right. You can add up to 100 filter rules.
    - **Tables with valid keys**: this column displays the tables that have valid keys, including primary keys or unique indexes.
    - **Tables without valid keys**: this column shows tables that lack primary keys or unique keys. These tables present a challenge during replication because the absence of a unique identifier can result in inconsistent data when the downstream handles duplicate events. To ensure data consistency, it is recommended to add unique keys or primary keys to these tables before initiating the replication. Alternatively, you can add filter rules to exclude these tables. For example, you can exclude the table `test.tbl1` by using the rule `"!test.tbl1"`.

6. Customize **Event Filter** to filter the events that you want to replicate.

    - **Tables matching**: you can set which tables the event filter will be applied to in this column. The rule syntax is the same as that used for the preceding **Table Filter** area. You can add up to 10 event filter rules per changefeed.
    - **Ignored events**: you can set which types of events the event filter will exclude from the changefeed.

7. In the **Start Replication Position** area, fill in the TSO that you get from Dumpling exported metadata files.

8. Click **Next** to configure your changefeed specification.

    - In the **Changefeed Specification** area, specify the number of Replication Capacity Units (RCUs) to be used by the changefeed.
    - In the **Changefeed Name** area, specify a name for the changefeed.

9. Click **Next** to review the changefeed configuration.

    If you confirm that all configurations are correct, check the compliance of cross-region replication, and click **Create**.

    If you want to modify some configurations, click **Previous** to go back to the previous configuration page.

10. The sink starts soon, and you can see the status of the sink changes from **Creating** to **Running**.

    Click the changefeed name, and you can see more details about the changefeed, such as the checkpoint, replication latency, and other metrics.

11. Restore [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) to its original value (the default value is `10m`) after the sink is created:

    ```sql
    SET GLOBAL tidb_gc_life_time = '10m';
    ```
