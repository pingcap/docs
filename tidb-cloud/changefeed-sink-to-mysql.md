---
title: Sink to MySQL
summary: This document explains how to stream data from TiDB Cloud to MySQL using the Sink to MySQL changefeed. It includes restrictions, prerequisites, and steps to create a MySQL sink for data replication. The process involves setting up network connections, loading existing data to MySQL, and creating target tables in MySQL. After completing the prerequisites, users can create a MySQL sink to replicate data to MySQL.
---

# Sink to MySQL

This document describes how to stream data from TiDB Cloud to MySQL using the **Sink to MySQL** changefeed.

<CustomContent plan="dedicated">

> **Note:**
>
> - To use the changefeed feature, make sure that your TiDB Cloud Dedicated cluster version is v6.1.3 or later.
> - For [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) and [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) clusters, the changefeed feature is unavailable.

</CustomContent>
<CustomContent plan="premium">

> **Note:**
>
> For [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) and [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) clusters, the changefeed feature is unavailable.

</CustomContent>

## Restrictions

- For each TiDB Cloud <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>, you can create up to 100 changefeeds.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.

## Prerequisites

Before creating a changefeed, you need to complete the following prerequisites:

- Set up your network connection
- Export and load the existing data to MySQL (optional)
- Create corresponding target tables in MySQL if you do not load the existing data and only want to replicate incremental data to MySQL

### Network

<CustomContent plan="dedicated">

Make sure that your TiDB Cloud cluster can connect to the MySQL service.

<SimpleTab>
<div label="VPC Peering">

If your MySQL service is in an AWS VPC that has no public internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.
2. Modify the inbound rules of the security group that the MySQL service is associated with.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) to the inbound rules. Doing so allows the traffic to flow from your TiDB Cluster to the MySQL instance.

3. If the MySQL URL contains a hostname, you need to allow TiDB Cloud to be able to resolve the DNS hostname of the MySQL service.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

If your MySQL service is in a Google Cloud VPC that has no public internet access, take the following steps:

1. If your MySQL service is Google Cloud SQL, you must expose a MySQL endpoint in the associated VPC of the Google Cloud SQL instance. You may need to use the [**Cloud SQL Auth proxy**](https://cloud.google.com/sql/docs/mysql/sql-proxy) which is developed by Google.
2. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.
3. Modify the ingress firewall rules of the VPC where MySQL is located.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) to the ingress firewall rules. Doing so allows the traffic to flow from your TiDB Cloud cluster to the MySQL endpoint.

</div>

<div label="Private Endpoint">

Private endpoints leverage **Private Link** or **Private Service Connect** technologies from cloud providers, enabling resources in your VPC to connect to services in other VPCs through private IP addresses, as if those services were hosted directly within your VPC.

You can connect your TiDB Cloud cluster to your MySQL service securely through a private endpoint. If the private endpoint is not available for your MySQL service, follow [Set Up Private Endpoint for Changefeeds](/tidb-cloud/set-up-sink-private-endpoint.md) to create one.

</div>

</SimpleTab>

</CustomContent>

<CustomContent plan="premium">

Make sure that your TiDB Cloud instance can connect to the MySQL service.

> **Note:**
>
> Currently, the VPC Peering feature for {{{ .premium }}} instances is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for VPC Peering for {{{ .premium }}} instance" in the **Description** field and click **Submit**.

Private endpoints leverage **Private Link** or **Private Service Connect** technologies from cloud providers, enabling resources in your VPC to connect to services in other VPCs through private IP addresses, as if those services were hosted directly within your VPC.

You can connect your TiDB Cloud instance to your MySQL service securely through a private endpoint. If the private endpoint is not available for your MySQL service, follow [Set Up Private Endpoint for Changefeeds](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md) to create one.

</CustomContent>

### Load existing data (optional)

<CustomContent plan="dedicated">

The **Sink to MySQL** connector can only sink incremental data from your TiDB cluster to MySQL after a certain timestamp. If you already have data in your TiDB cluster, you can export and load the existing data of your TiDB cluster into MySQL before enabling **Sink to MySQL**.

</CustomContent>
<CustomContent plan="premium">

The **Sink to MySQL** connector can only sink incremental data from your TiDB instance to MySQL after a certain timestamp. If you already have data in your TiDB instance, you can export and load the existing data of your TiDB instance into MySQL before enabling **Sink to MySQL**.

</CustomContent>

To load the existing data:

1. Extend the [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) to be longer than the total time of the following two operations, so that historical data during the time is not garbage collected by TiDB.

    - The time to export and import the existing data
    - The time to create **Sink to MySQL**

    For example:

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. Use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export data from your TiDB <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>, then use community tools such as [mydumper/myloader](https://centminmod.com/mydumper.html) to load data to the MySQL service.

3. From the [exported files of Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files), get the start position of MySQL sink from the metadata file:

    The following is a part of an example metadata file. The `Pos` of `SHOW MASTER STATUS` is the TSO of the existing data, which is also the start position of MySQL sink.

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

### Create target tables in MySQL

If you do not load the existing data, you need to create corresponding target tables in MySQL manually to store the incremental data from TiDB. Otherwise, the data will not be replicated.

## Create a MySQL sink

After completing the prerequisites, you can sink your data to MySQL.

1. Navigate to the overview page of the target TiDB <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>, and then click **Data** > **Changefeed** in the left navigation pane.

2. Click **Create Changefeed**, and select **MySQL** as **Destination**.

3. In **Connectivity Method**, choose the method to connect to your MySQL service.

    - If you choose **VPC Peering** or **Public IP**, fill in your MySQL endpoint.
    - If you choose **Private Link**, select the private endpoint that you created in the [Network](#network) section, and then fill in the MySQL port for your MySQL service.

4. In **Authentication**, fill in the MySQL user name and password of your MySQL service.

5. Click **Next** to test whether TiDB can connect to MySQL successfully:

    - If yes, you are directed to the next step of configuration.
    - If not, a connectivity error is displayed, and you need to handle the error. After the error is resolved, click **Next** again.

6. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](/table-filter.md).

    - **Case Sensitive**: you can set whether the matching of database and table names in filter rules is case-sensitive. By default, matching is case-insensitive.
    - **Filter Rules**: you can set filter rules in this column. By default, there is a rule `*.*`, which stands for replicating all tables. When you add a new rule, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules in the box on the right. You can add up to 100 filter rules.
    - **Tables with valid keys**: this column displays the tables that have valid keys, including primary keys or unique indexes.
    - **Tables without valid keys**: this column shows tables that lack primary keys or unique keys. These tables present a challenge during replication because the absence of a unique identifier can result in inconsistent data when the downstream handles duplicate events. To ensure data consistency, it is recommended to add unique keys or primary keys to these tables before initiating the replication. Alternatively, you can add filter rules to exclude these tables. For example, you can exclude the table `test.tbl1` by using the rule `"!test.tbl1"`.

7. Customize **Event Filter** to filter the events that you want to replicate.

    - **Tables matching**: you can set which tables the event filter will be applied to in this column. The rule syntax is the same as that used for the preceding **Table Filter** area. You can add up to 10 event filter rules per changefeed.
    - **Event Filter**: you can use the following event filters to exclude specific events from the changefeed:
        - **Ignore event**: excludes specified event types.
        - **Ignore SQL**: excludes DDL events that match specified expressions. For example, `^drop` excludes statements starting with `DROP`, and `add column` excludes statements containing `ADD COLUMN`.
        - **Ignore insert value expression**: excludes `INSERT` statements that meet specific conditions. For example, `id >= 100` excludes `INSERT` statements where `id` is greater than or equal to 100.
        - **Ignore update new value expression**: excludes `UPDATE` statements where the new value matches a specified condition. For example, `gender = 'male'` excludes updates that result in `gender` being `male`.
        - **Ignore update old value expression**: excludes `UPDATE` statements where the old value matches a specified condition. For example, `age < 18` excludes updates where the old value of `age` is less than 18.
        - **Ignore delete value expression**: excludes `DELETE` statements that meet a specified condition. For example, `name = 'john'` excludes `DELETE` statements where `name` is `'john'`.

8. In **Start Replication Position**, configure the starting position for your MySQL sink.

    - If you have [loaded the existing data](#load-existing-data-optional) using Dumpling, select **Start replication from a specific TSO** and fill in the TSO that you get from Dumpling exported metadata files.
    - If you do not have any data in the upstream TiDB <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>, select **Start replication from now on**.
    - Otherwise, you can customize the start time point by choosing **Start replication from a specific time**.

9. Click **Next** to configure your changefeed specification.

    - In the **Changefeed Specification** area, specify the number of <CustomContent plan="dedicated">Replication Capacity Units (RCUs)</CustomContent><CustomContent plan="premium">Changefeed Capacity Units (CCUs)</CustomContent> to be used by the changefeed.
    - In the **Changefeed Name** area, specify a name for the changefeed.

10. Click **Next** to review the changefeed configuration.

    If you confirm that all configurations are correct, check the compliance of cross-region replication, and click **Create**.

    If you want to modify some configurations, click **Previous** to go back to the previous configuration page.

11. The sink starts soon, and you can see the status of the sink changes from **Creating** to **Running**.

    Click the changefeed name, and you can see more details about the changefeed, such as the checkpoint, replication latency, and other metrics.

12. If you have [loaded the existing data](#load-existing-data-optional) using Dumpling, you need to restore the GC time to its original value (the default value is `10m`) after the sink is created:

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```
