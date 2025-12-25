---
title: Sink to MySQL
summary: This document explains how to stream data from TiDB Cloud to MySQL using the Sink to MySQL changefeed. It includes restrictions, prerequisites, and steps to create a MySQL sink for data replication. The process involves setting up network connections, loading existing data to MySQL, and creating target tables in MySQL. After completing the prerequisites, users can create a MySQL sink to replicate data to MySQL.
---

# Sink to MySQL

This document describes how to stream data from TiDB Cloud to MySQL using the **Sink to MySQL** changefeed.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 10 changefeeds.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.

## Prerequisites

Before creating a changefeed, you need to complete the following prerequisites:

- Set up your network connection
- Export and load the existing data to MySQL (optional)
- Create corresponding target tables in MySQL if you do not load the existing data and only want to replicate incremental data to MySQL

### Network

Make sure that your TiDB Cloud cluster can connect to the MySQL service.

<SimpleTab>
<div label="Public Network">

If your MySQL service can be accessed over the public network, you can choose to connect to MySQL through a public IP or domain name.

</div>

<div label="Private Link Connection">

Private link connection leverage **Private Link** technologies from cloud providers, enabling resources in your VPC to connect to services in other VPCs through private IP addresses, as if those services were hosted directly within your VPC.

You can connect your TiDB Cloud cluster to your MySQL service securely through a private link connection. If the private link connection is not available for your MySQL service, follow [Connect to Amazon RDS via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-aws-rds.md) or [Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-alicloud-rds.md) to create one.

</div>

</SimpleTab>

### Load existing data (optional)

The **Sink to MySQL** connector can only sink incremental data from your TiDB Cloud cluster to MySQL after a certain timestamp. If you already have data in your TiDB Cloud cluster, you can export and load the existing data of your TiDB Cloud cluster into MySQL before enabling **Sink to MySQL**.

To load the existing data:

1. Extend the [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) to be longer than the total time of the following two operations, so that historical data during the time is not garbage collected by TiDB.

    - The time to export and import the existing data
    - The time to create **Sink to MySQL**

    For example:

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '72h';
    ```

2. Use [Export](/tidb-cloud/serverless-export.md) to export data from your TiDB Cloud cluster, then use community tools such as [mydumper/myloader](https://centminmod.com/mydumper.html) to load data to the MySQL service.

3. Use the snapshot time of [Export](/tidb-cloud/serverless-export.md) as the start position of MySQL sink.

### Create target tables in MySQL

If you do not load the existing data, you need to create corresponding target tables in MySQL manually to store the incremental data from TiDB. Otherwise, the data will not be replicated.

## Create a MySQL sink

After completing the prerequisites, you can sink your data to MySQL.

1. Navigate to the overview page of the target TiDB Cloud cluster, and then click **Data** > **Changefeed** in the left navigation pane.

2. Click **Create Changefeed**, and select **MySQL** as **Destination**.

3. In **Connectivity Method**, choose the method to connect to your MySQL service.

    - If you choose **Public**, fill in your MySQL endpoint.
    - If you choose **Private Link**, select the private link connection that you created in the [Network](#network) section, and then fill in the MySQL port for your MySQL service.

4. In **Authentication**, fill in the MySQL user name, password and TLS Encryption of your MySQL service. TiDB Cloud does not support self-signed certificates for MySQL TLS connections currently.

5. Click **Next** to test whether TiDB can connect to MySQL successfully:

    - If yes, you are directed to the next step of configuration.
    - If not, a connectivity error is displayed, and you need to handle the error. After the error is resolved, click **Next** again.

6. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](https://docs.pingcap.com/tidb/stable/table-filter/#syntax).

    - **Replication Scope**: you can choose to only replicate tables with valid keys or replicate all selected tables.
    - **Filter Rules**: you can set filter rules in this column. By default, there is a rule `*.*`, which stands for replicating all tables. When you add a new rule and click `apply`, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules under the `Filter results`.
    - **Case Sensitive**: you can set whether the matching of database and table names in filter rules is case-sensitive. By default, matching is case-insensitive.
    - **Filter results with valid keys**: this column displays the tables that have valid keys, including primary keys or unique indexes.
    - **Filter results without valid keys**: this column shows tables that lack primary keys or unique keys. These tables present a challenge during replication because the absence of a unique identifier can result in inconsistent data when the downstream handles duplicate events. To ensure data consistency, it is recommended to add unique keys or primary keys to these tables before initiating the replication. Alternatively, you can add filter rules to exclude these tables. For example, you can exclude the table `test.tbl1` by using the rule `"!test.tbl1"`.

7. Customize **Event Filter** to filter the events that you want to replicate.

    - **Tables matching**: you can set which tables the event filter will be applied to in this column. The rule syntax is the same as that used for the preceding **Table Filter** area.
    - **Event Filter**: you can choose the events you want to ingnore.

8. In **Start Replication Position**, configure the starting position for your MySQL sink.

    - If you have [loaded the existing data](#load-existing-data-optional) using Export, select **From Time** and fill in the snapshot time that you get from Export. Pay attention the time zone.
    - If you do not have any data in the upstream TiDB cluster, select **Start replication from now on**.

9. Click **Next** to configure your changefeed specification.

    - In the **Changefeed Name** area, specify a name for the changefeed.

10. If you confirm that all configurations are correct,  click **Submit**. If you want to modify some configurations, click **Previous** to go back to the previous configuration page.

11. The sink starts soon, and you can see the status of the sink changes from **Creating** to **Running**.

    Click the changefeed name, and you can see more details about the changefeed, such as the checkpoint, replication latency, and other metrics.

12. If you have [loaded the existing data](#load-existing-data-optional) using Export, you need to restore the GC time to its original value (the default value is `10m`) after the sink is created:

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```
