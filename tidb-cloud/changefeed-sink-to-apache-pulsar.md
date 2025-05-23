---
title: Sink to Apache Pulsar
summary: This document explains how to create a changefeed to stream data from TiDB Cloud to Apache Pulsar. It includes restrictions, prerequisites, and steps to configure the changefeed for Apache Pulsar. The process involves setting up network connections, and configuring the changefeed specification.
---

# Sink to Apache Pulsar

This document describes how to create a changefeed to stream data from TiDB Cloud to Apache Pulsar.

> **Note:**
>
> - To use the changefeed feature to replicate to Pulsar, make sure that your TiDB Cloud Dedicated cluster version is v7.5.1 or later.
> - For [TiDB Cloud Serverless clusters](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless), the changefeed feature is unavailable.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 100 changefeeds.
- Currently, TiDB Cloud does not support uploading self-signed TLS certificates to connect to Pulsar brokers.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.
- Currently, TiCDC does not automically create Pulsar topics. When dispatching events to a topic, those topics should already exist on Pulsar.

## Prerequisites

Before creating a changefeed to stream data to Apache Pulsar, you need to complete the following prerequisites:

- Set up your network connection
- Add permissions for Pulsar ACL authorization
- Create Topics

### Network

Ensure that your TiDB cluster can connect to the Apache Pulsar service. You can choose one of the following connection methods:

- VPC Peering: requires planning to avoid potential VPC CIDR conflicts and consideration of security concerns.
- Public IP: suitable for setup when Pulsar advertises a public IP. Note recommended for production, requires careful consideration of security concerns.

<SimpleTab>
<div label="VPC Peering">

If your Apache Pulsar service is in an AWS VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Pulsar service and your TiDB cluster.
2. Modify the inbound rules of the security group that the Apache Pulsar service is associated with.

    You must add the CIDR of the region where your TiDB Cloud cluster is located to the inbound rules. The CIDR can be found on the **VPC Peering** page. Doing so allows the traffic to flow from your TiDB cluster to the Pulsar brokers.

3. If the Apache Pulsar URL contains hostnames, you need to allow TiDB Cloud to be able to resolve the DNS hostnames of the Apache Pulsar brokers.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-dns.html).
    2. Enable the **Accepter DNS resolution** option.

If your Apache Pulsar service is in a Google Cloud VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Pulsar service and your TiDB cluster.
2. Modify the ingress firewall rules of the VPC where Apache Pulsar is located.

    You must add the CIDR of the region where your TiDB Cloud cluster is located to the ingress firewall rules. The CIDR can be found on the **VPC Peering** page. Doing so allows the traffic to flow from your TiDB cluster to the Pulsar brokers.

</div>
<div label="Public IP">

If you want to provide Public IP access to your Apache Pulsar service, assign Public IP addresses to all your Pulsar brokers. 

It is **NOT** recommended to use Public IP in a production environment. 

</div>
</SimpleTab>

## Step 1. Open the changefeed page for Apache Pulsar

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Navigate to the cluster overview page of the TiDB cluster that will be the source of the Changefeed events, and then click **Changefeed** in the left navigation pane.
3. Click **Create Changefeed**.

## Step 2. Configure the changefeed destination

1. In **Destinaton**, select **Pulsar**.
2. In **Connection**, enter the connection information:

   - **Destination Protocol**: select **Pulsar**, or **Pulsar+SSL**
   - **Connectivity Method**: select **VPC Peering** or **Public IP**, depending on how you intende to connect to your Pulsar endpoint
   - **Pulsar Broker**: fill in your Pulsar brokers endpoint, use a colon to separate the port from the domain/IP, e.g. `example.org:6650`.

3. In **Authentication**, select the **Auth Type** option according to your Pulsar authentication configuration. Depending on your selection, enter the requested credential information.
4. The **Advanced Settings** section contains additional settings that may be optionally adjusted:

   - **Compression**: select an optional compression algorithm for the data in this changefeed.
   - **Max Messages per Batch** & **Max Publish Delay**: these are used to manage the batching of event messages sent to Pulsar. **Max Messages per Batch** sets the maximum number of messages in a single batch, while **Max Publish Delay** sets the maximum interval at which messages may be delayed by batching.
   - **Connection Timeout**: adjust the timeout for establishing a TCP connection to Pulsar.
   - **Operation Timeout**: adjust the timeout for the TiCDC Pulsar clients to initiate an operation.
   - **Send Timeout**: adjust the timeout for the TiCDC Pulsar producer to send a message.

5.  Click **Next** to test the network connection. If the test succeeds, you will be directed to the next page.

## Step 3. Configure the changefeed replication

1. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](/table-filter.md).

    - **Filter Rules**: you can set filter rules in this column. By default, there is a rule `*.*`, which stands for replicating all tables. When you add a new rule, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules in the box on the right. You can add up to 100 filter rules.
    - **Tables with valid keys**: this column displays the tables that have valid keys, including primary keys or unique indexes.
    - **Tables without valid keys**: this column shows tables that lack primary keys or unique keys. These tables present a challenge during replication because the absence of a unique identifier can result in inconsistent data when the downstream handles duplicate events. To ensure data consistency, it is recommended to add unique keys or primary keys to these tables before initiating the replication. Alternatively, you can add filter rules to exclude these tables. For example, you can exclude the table `test.tbl1` by using the rule `"!test.tbl1"`.

2. Customize **Event Filter** to filter the events that you want to replicate.

    - **Tables matching**: you can set which tables the event filter will be applied to in this column. The rule syntax is the same as that used for the preceding **Table Filter** area. You can add up to 10 event filter rules per changefeed.
    - **Ignored events**: you can set which types of events the event filter will exclude from the changefeed.

3. In the **Start Replication Position** area, select the desired starting point at which the changefeed should replicate your data to Pulsar:

   - **Start replication from now on**: the changefeed will begin replicating data from the current point onwards
   - **Start replication from a specific TSO**: the changefeed will begin replicating data from the specified [TSO](/tso.md) onwards. The specified TSO should be within the [garbage collection safe point](/read-historical-data.md#how-tidb-manages-the-data-versions).
   - **Start replication from a specific time**: the changefeed will begin replicating data from the specified timestamp onwards. The specified timestamp should be within the garbage collection safe point.

4. In the **Data Format** area, select your desired format of Pulsar messages.

    - Canal-JSON is a plain JSON text format, which is easy to parse. For more information, see [Canal-JSON data format](/ticdc/ticdc-canal-json.md).

    - Enable the **TiDB Extension** option if you want to add TiDB-extension fields to the Pulsar message body.

    For more information about TiDB-extension fields, see [TiDB extension fields in Canal-JSON data format](/ticdc/ticdc-canal-json.md#tidb-extension-field).

5. In the **Topic Distribution** area, select a distribution mode, and then fill in the topic name configurations according to the mode.

    The distribution mode controls how the changefeed distributes event messages to Pulsar topics, by sending all messages to one topic, or sending to specific topics by table or by database.

    > **Note:**
    >
    > When Pulsar is selected as a downstream, the changefeed does not automatically create the topics for you. The topics to be used should be created in advance.

    - **Send all changelogs to one specified Pulsar Topic**

        If you want the changefeed to send all messages to one Pulsar topic, choose this mode.You can define the topic name in the **Topic Name** field.

    - **Distribute changelogs by table to Pulsar Topics**

        If you want the changefeed to create a dedicated Pulsar topic for each table, choose this mode. Then, all Pulsar messages of a table are sent to a dedicated Pulsar topic. You can customize topic names for tables by setting the **Topic Prefix**, a **Separator** between a database name and table name, and a **Topic Suffix**. For example, if you set the separator as `_`, the topic names are in the format of `<Topic Prefix><DatabaseName>_<TableName><Topic Suffix>`. This topic should be created in advance on Pulsar.

        For changelogs of non-row events, such as Create Schema Event, you can specify a topic name in the **Default Topic Name** field. The changefeed will send the non-row events to this topic to collect such changelogs.

    - **Distribute changelogs by database to Pulsar Topics**

        If you want the changefeed to create a dedicated Pulsar topic for each database, choose this mode. Then, all Pulsar messages of a database are sent to a dedicated Pulsar topic. You can customize topic names of databases by setting the **Topic Prefix** and **Topic Suffix**.

        For changelogs of non-row events, such as Resolved Ts Event, you can specify a topic name in the **Default Topic Name** field. The changefeed will send the non-row events to this topic to collect such changelogs.

    As Pulsar is a multi-tenant solution, you may also set the **Pulsar Tenant** and **Pulsar Namespace** if they are different from the defaults.

6. In the **Partition Distribution** area, you can decide which partition a Pulsar message will be sent to. You can define **a single partition dispatcher for all tables**, or **different partition dispatchers for different tables**. TiDB Cloud provides four rule options to distribute change events to Pulsar partitions:

    - **Primary key or unique index**

        If you want the changefeed to send Pulsar messages of a table to different partitions, choose this distribution method. The primary key or index value of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures row-level orderliness.

    - **Table**

        If you want the changefeed to send Pulsar messages of a table to one Pulsar partition, choose this distribution method. The table name of a row changelog will determine which partition the changelog is sent to. This distribution method ensures table orderliness but might cause unbalanced partitions.

    - **Timestamp**

        If you want the changefeed to send Pulsar messages to different Pulsar partitions based on the timestamp, choose this distribution method. The commitTs of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures orderliness in each partition. However, multiple changes of a data item might be sent to different partitions and the consumer progress of different consumers might be different, which might cause data inconsistency. Therefore, the consumer needs to sort the data from multiple partitions by commitTs before consuming.

    - **Column value**

        If you want the changefeed to send Pulsar messages of a table to different partitions, choose this distribution method. The specified column values of a row changelog will determine which partition the changelog is sent to. This distribution method ensures orderliness in each partition and guarantees that the changelog with the same column values is send to the same partition.

7. Click **Next**.

## Step 4. Specification and Review

1. In the **Specification and Name** area
   
   - Specify the number of [Replication Capacity Units (RCUs)](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md) to be used by the changefeed.
   - Specify a name for the changefeed.

2. Review all the changefeed configurations for any issues.

If you find an issue, you can go back to the previous steps to resolve the problem. If there are no issues, you can click **Submit** to create the changefeed.
