---
title: Sink to MySQL
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to MySQL.
---

# Sink to MySQL

This document describes how to stream data from TiDB Cloud to MySQL using the **Sink to MySQL** changefeed.

> **Note:**
>
> If you have want to use the Changefeed feature, make sure that your TiDB cluster version is at least v6.4.0 and the TiKV node size is at least 8 vCPU and 16 GiB.
>
> For [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta), the changefeed feature is unavailable.

## Prerequisites

### Network

Make sure that your TiDB Cluster can connect to the MySQL service.

If your MySQL service is in an AWS VPC that has no public internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.
2. Modify the inbound rules of the security group that the MySQL service is associated with. 

    You must add [the CIDR of the Region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr) to the inbound rules. Doing so allows the traffic to flow from your TiDB Cluster to the MySQL instance.

3. If the MySQL URL contains a hostname, you need to allow TiDB Cloud to be able to resolve the DNS hostname of the MySQL service. 

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

If your MySQL service is in a GCP VPC that has no public internet access, take the following steps:

1. If your MySQL service is Google Cloud SQL, you must expose a MySQL endpoint in the associated VPC of the Google Cloud SQL instance. You may need to use the [**Cloud SQL Auth proxy**](https://cloud.google.com/sql/docs/mysql/sql-proxy) which is developed by Google.
2. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster. 
3. Modify the ingress firewall rules of the VPC where MySQL is located.

    You must add [the CIDR of the Region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr) to the ingress firewall rules. Doing so allows the traffic to flow from your TiDB Cluster to the MySQL endpoint. 

### Full load data

The **Sink to MySQL** connector can only sink incremental data from your TiDB cluster to MySQL after a certain timestamp. If you already have data in your TiDB cluster, you must export and load the full load data of your TiDB cluster into MySQL before enabling **Sink to MySQL**:

1. Extend the [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) to be longer than the total time of the following two operations, so that historical data during the time is not garbage collected by TiDB.

    - The time to export and import the full load data
    - The time to create **Sink to MySQL**

    For example:

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. Use [Dumpling](/dumpling-overview.md#export-data-from-tidbmysql) to export data from your TiDB cluster, then use [TiDB Lightning logical import](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md) to load data to the MySQL service.

3. From the [exported files of Dumpling](/dumpling-overview.md#format-of-exported-files), get the start position of MySQL sink from the metadata file:

    The following is an example output. The "Pos" of "SHOW MASTER STATUS" is the TSO of the full load data, which is also the start position of MySQL sink.

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ``` 

## Create a Sink

After completing the prerequisites, you can sink your data to MySQL.

1. Navigate to the **Data Replication** > **Changefeed** tab of your TiDB cluster.

2. Click **Sink to MySQL**.

3. Fill in the MySQL Endpoints, user, and password in **MySQL Connection**.

4. Optionally, if you need to configure the following advanced options, you can click on **Show advanced configuration**.
    - In **Timezone**, you can select the timezone used to convert time type data, like `timestamp`.

5. Click **Next** to test connectivity
    - If the connectivity of MySQL is fine, it will go to the next step of configuration.
    - Otherwise, it will display the connectivity error, which you need to deal with the error before clicking **Next** again.

6. **Table Filter** provides a simple way to filter the tables that need to be replicated by customing [table filter rules](/table-filter.md).
    - Defaultlly there is a rule `*. *`, which stands for replicating all tables. Whenever you add a new rule, TiDB Cloud will query all the tables in TiDB and display the tables that can be replicated in the list box on the right.  **Note:** The list box on the right does not show the new tables to be replicated in the future, and the schema to be full replicated.
    - TiDB Cloud also lists tables that do not have unique and primary keys, and these tables may have inconsistent data in downstream during replication due to interrupt recovery. You can choose, not to replicate all tables that do not have unique and primary keys, or replicate these tables.

7. In **Start Position**, configure the starting position for your sink
    - If you do [Full load data](#full-load-data), you must fill in the TSO that Dumpling provides in **Start replication from a specific TSO**.
    - If you do not have any data in your TiDB Cluster, you can choose **Start replication from now on**.
    - Otherwise, you can custom the start time point by choosing **Start replica from a specific time**.

7. Click **Next** to Changefee Preview
    - if you want to modify some configurations, click **Previous** to go back to the previous page.
    - Othwise, Check the compliance of cross region replication prompt, and click **Create**.

8. After a while, the sink will begin its work, and the status of the sink will be changed to "**Running**".
    - Clicking on the Changefeed card, then you can see the Changfefeed running status in a pop-up window, including Checkpoint, replication latency, etc.

9. Optionally, after the operation is complete, set the GC time back (the default value is `10m`):

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## Delete a Sink

1. Navigate to the **Data Replication** > **Changefeed** tab of a cluster.
2. Clicking on the Changefeed card, then click **Delete**.

## Puase or Resume a Sink

1. Navigate to the **Data Replication** > **Changefeed** tab of a cluster.
2. Clicking on the Changefeed card, then click **Pause** or **Resume**.

## Query TCU

1. Navigate to the **Data Replication** > **Changefeed** tab of a cluster.
2. The current TiCDC Capacity Units are displayed in the upper right corner of the page.

## Restrictions

Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions).
