---
title: Sink to Apache Kafka
summary: This document explains how to create a changefeed to stream data from TiDB Cloud to Apache Kafka. It includes restrictions, prerequisites, and steps to configure the changefeed for Apache Kafka. The process involves setting up network connections, adding permissions for Kafka ACL authorization, and configuring the changefeed specification.
---

# Sink to Apache Kafka

This document describes how to create a changefeed to stream data from TiDB Cloud to Apache Kafka.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 10 changefeeds.
- Currently, TiDB Cloud does not support uploading self-signed TLS certificates to connect to Kafka brokers.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.

## Prerequisites

Before creating a changefeed to stream data to Apache Kafka, you need to complete the following prerequisites:

- Set up your network connection
- Add permissions for Kafka ACL authorization

### Network

Ensure that your TiDB Cloud cluster can connect to the Apache Kafka service. You can choose one of the following connection methods:

- Public Access: suitable for a quick setup.
- Private Link Connection: meeting security compliance and ensuring network quality.

<SimpleTab>
<div label="Private Link Connection">

Private Link Connection leverages **Private Link** technologies from cloud providers to enable resources in your VPC to connect to services in other VPCs using private IP addresses, as if those services were hosted directly within your VPC.

TiDB Cloud currently supports Private Link Connection only for self-hosted Kafka and Confluent Cloud dedicated cluster. It does not support direct integration with MSK, or other Kafka SaaS services.

See the following instructions to set up a Private Link connection according to your Kafka deployment and cloud provider:

- [Connect to Confluent Cloud via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-aws-confluent.md)
- [Connect to AWS Self-Hosted Kafka via Private Link Connection](/tidbcloud/serverless-private-link-connection-to-self-hosted-kafka-in-aws.md)
- [Connect to Alibaba Cloud Self-Hosted Kafka via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-self-hosted-kafka-in-alicloud.md)

</div>

<div label="Public Network">

If you want to provide Public access to your Apache Kafka service, assign Public IP addresses or domain names to all your Kafka brokers. 

It is **NOT** recommended to use Public access in a production environment. 

</div>
</SimpleTab>

### Kafka ACL authorization

To allow TiDB Cloud changefeeds to stream data to Apache Kafka and create Kafka topics automatically, ensure that the following permissions are added in Kafka:

- The `Create` and `Write` permissions are added for the topic resource type in Kafka.
- The `DescribeConfigs` permission is added for the cluster resource type in Kafka.

For example, if your Kafka cluster is in Confluent Cloud, you can see [Resources](https://docs.confluent.io/platform/current/kafka/authorization.html#resources) and [Adding ACLs](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls) in Confluent documentation for more information.

## Step 1. Open the Changefeed page for Apache Kafka

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Navigate to the overview page of the target TiDB Cloud cluster, and then click **Data** > **Changefeed** in the left navigation pane.
3. Click **Create Changefeed**, and select **Kafka** as **Destination**.

## Step 2. Configure the changefeed target

The steps vary depending on the connectivity method you select.

<SimpleTab>
<div label="Public">

1. In **Connectivity Method**, select **Public**, fill in your Kafka brokers endpoints. You can use commas `,` to separate multiple endpoints.
2. Select an **Authentication** option according to your Kafka authentication configuration.

    - If your Kafka does not require authentication, keep the default option **Disable**.
    - If your Kafka requires authentication, select the corresponding authentication type, and then fill in the **user name** and **password** of your Kafka account for authentication.

3. Select your **Kafka Version**. If you do not know which one to use, use **Kafka v2**.
4. Select a **Compression** type for the data in this changefeed.
5. Enable the **TLS Encryption** option if your Kafka has enabled TLS encryption and you want to use TLS encryption for the Kafka connection.
6. Click **Next** to test the network connection. If the test succeeds, you will be directed to the next page.

</div>
<div label="Private Link">

1. In **Connectivity Method**, select **Private Link**.
2. In **Private Link Connection**, select the private link connection that you created in the [Network](#network) section. Make sure the AZs of the private link connection match the AZs of the Kafka deployment.
3. Fill in the **Bootstrap Port** that you obtained from the [Network](#network) section.
4. Select an **Authentication** option according to your Kafka authentication configuration.

    - If your Kafka does not require authentication, keep the default option **Disable**.
    - If your Kafka requires authentication, select the corresponding authentication type, and then fill in the **user name** and **password** of your Kafka account for authentication.
5. Select your **Kafka Version**. If you do not know which one to use, use **Kafka v2**.
6. Select a **Compression** type for the data in this changefeed.
7. Enable the **TLS Encryption** option if your Kafka has enabled TLS encryption and you want to use TLS encryption for the Kafka connection.
8. Input the **TLS Server Name** if your Kafka requires TLS SNI verification. For example, Confluent Cloud Dedicated clusters.
9. Click **Next** to test the network connection. If the test succeeds, you will be directed to the next page.

</div>
</SimpleTab>

## Step 3. Set the changefeed

1. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](https://docs.pingcap.com/tidb/stable/table-filter/#syntax).

    - **Replication Scope**: you can choose to only replicate tables with valid keys or replicate all selected tables.
    - **Filter Rules**: you can set filter rules in this column. By default, there is a rule `*.*`, which stands for replicating all tables. When you add a new rule and click `apply`, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules under the `Filter results`.
    - **Case Sensitive**: you can set whether the matching of database and table names in filter rules is case-sensitive. By default, matching is case-insensitive.
    - **Filter results with valid keys**: this column displays the tables that have valid keys, including primary keys or unique indexes.
    - **Filter results without valid keys**: this column shows tables that lack primary keys or unique keys. These tables present a challenge during replication because the absence of a unique identifier can result in inconsistent data when the downstream handles duplicate events. To ensure data consistency, it is recommended to add unique keys or primary keys to these tables before initiating the replication. Alternatively, you can add filter rules to exclude these tables. For example, you can exclude the table `test.tbl1` by using the rule `"!test.tbl1"`.

2. Customize **Event Filter** to filter the events that you want to replicate.

    - **Tables matching**: you can set which tables the event filter will be applied to in this column. The rule syntax is the same as that used for the preceding **Table Filter** area.
    - **Event Filter**: you can choose the events you want to ingnore.

3. Customize **Column Selector** to select columns from events and send only the data changes related to those columns to the downstream.

    - **Tables matching**: specify which tables the column selector applies to. For tables that do not match any rule, all columns are sent.
    - **Column Selector**: specify which columns of the matched tables will be sent to the downstream.

    For more information about the matching rules, see [Column selectors](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-kafka/#column-selectors).

4. In the **Data Format** area, select your desired format of Kafka messages.

    - Avro is a compact, fast, and binary data format with rich data structures, which is widely used in various flow systems. For more information, see [Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol).
    - Canal-JSON is a plain JSON text format, which is easy to parse. For more information, see [Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json).
    - Open Protocol is a row-level data change notification protocol that provides data sources for monitoring, caching, full-text indexing, analysis engines, and primary-secondary replication between different databases. For more information, see [Open Protocol data format](https://docs.pingcap.com/tidb/stable/ticdc-open-protocol). 
    - Debezium is a tool for capturing database changes. It converts each captured database change into a message called an "event" and sends these events to Kafka. For more information, see [Debezium data format](https://docs.pingcap.com/tidb/stable/ticdc-debezium).

5. Enable the **TiDB Extension** option if you want to add TiDB-extension fields to the Kafka message body.

    For more information about TiDB-extension fields, see [TiDB extension fields in Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields) and [TiDB extension fields in Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field).

6. If you select **Avro** as your data format, you will see some Avro-specific configurations on the page. You can fill in these configurations as follows:

    - In the **Decimal** and **Unsigned BigInt** configurations, specify how TiDB Cloud handles the decimal and unsigned bigint data types in Kafka messages.
    - In the **Schema Registry** area, fill in your schema registry endpoint. If you enable **HTTP Authentication**, the fields for user name and password are displayed to fill in.

7. In the **Topic Distribution** area, select a distribution mode, and then fill in the topic name configurations according to the mode.

    If you select **Avro** as your data format, you can only choose the **Distribute changelogs by table to Kafka Topics** mode in the **Distribution Mode** drop-down list.

    The distribution mode controls how the changefeed creates Kafka topics, by table, by database, or creating one topic for all changelogs.

    - **Distribute changelogs by table to Kafka Topics**

        If you want the changefeed to create a dedicated Kafka topic for each table, choose this mode. Then, all Kafka messages of a table are sent to a dedicated Kafka topic. You can customize topic names for tables by setting a topic prefix, a separator between a database name and table name, and a suffix. For example, if you set the separator as `_`, the topic names are in the format of `<Prefix><DatabaseName>_<TableName><Suffix>`.

        For changelogs of non-row events, such as Create Schema Event, you can specify a topic name in the **Default Topic Name** field. The changefeed will create a topic accordingly to collect such changelogs.

    - **Distribute changelogs by database to Kafka Topics**

        If you want the changefeed to create a dedicated Kafka topic for each database, choose this mode. Then, all Kafka messages of a database are sent to a dedicated Kafka topic. You can customize topic names of databases by setting a topic prefix and a suffix.

        For changelogs of non-row events, such as Resolved Ts Event, you can specify a topic name in the **Default Topic Name** field. The changefeed will create a topic accordingly to collect such changelogs.

    - **Send all changelogs to one specified Kafka Topic**

        If you want the changefeed to create one Kafka topic for all changelogs, choose this mode. Then, all Kafka messages in the changefeed will be sent to one Kafka topic. You can define the topic name in the **Topic Name** field.

8. In the **Partition Distribution** area, you can decide which partition a Kafka message will be sent to. You can define **a single partition dispatcher for all tables**, or **different partition dispatchers for different tables**. TiDB Cloud provides four types of dispatchers:

    - **Distribute changelogs by primary key or index value to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to different partitions, choose this distribution method. The primary key or index value of a row changelog will determine which partition the changelog is sent to. Keep the **Index Name** field empty if you want to use the primary key. This distribution method provides a better partition balance and ensures row-level orderliness.

    - **Distribute changelogs by table to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to one Kafka partition, choose this distribution method. The table name of a row changelog will determine which partition the changelog is sent to. This distribution method ensures table orderliness but might cause unbalanced partitions.

    - **Distribute changelogs by timestamp to Kafka partition**

        If you want the changefeed to send Kafka messages to different Kafka partitions randomly, choose this distribution method. The commitTs of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures orderliness in each partition. However, multiple changes of a data item might be sent to different partitions and the consumer progress of different consumers might be different, which might cause data inconsistency. Therefore, the consumer needs to sort the data from multiple partitions by commitTs before consuming.

    - **Distribute changelogs by column value to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to different partitions, choose this distribution method. The specified column values of a row changelog will determine which partition the changelog is sent to. This distribution method ensures orderliness in each partition and guarantees that the changelog with the same column values is send to the same partition.

9. In the **Topic Configuration** area, configure the following numbers. The changefeed will automatically create the Kafka topics according to the numbers.

    - **Replication Factor**: controls how many Kafka servers each Kafka message is replicated to. The valid value ranges from [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) to the number of Kafka brokers.
    - **Partition Number**: controls how many partitions exist in a topic. The valid value range is `[1, 10 * the number of Kafka brokers]`.

10. In the **Split Event** area, choose whether to split `UPDATE` events into separate `DELETE` and `INSERT` events or keep as raw `UPDATE` events. For more information, see [Split primary or unique key UPDATE events for non-MySQL sinks](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks).

11. Click **Next**.

## Step 4. Review and create your changefeed specification

1. In the **Changefeed Name** area, specify a name for the changefeed.
2. Review all the changefeed configurations that you set. Click **Previous** to go back to the previous configuration pages if you want to modify some configurations. Click **Submit** if all configurations are correct to create the changefeed.