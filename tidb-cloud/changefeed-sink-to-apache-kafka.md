---
title: Sink to Apache Kafka
summary: This document explains how to create a changefeed to stream data from TiDB Cloud to Apache Kafka. It includes restrictions, prerequisites, and steps to configure the changefeed for Apache Kafka. The process involves setting up network connections, adding permissions for Kafka ACL authorization, and configuring the changefeed specification.
---

# Sink to Apache Kafka

This document describes how to create a changefeed to stream data from TiDB Cloud to Apache Kafka.

> **Note:**
>
> - To use the changefeed feature, make sure that your TiDB Cloud Dedicated cluster version is v6.1.3 or later.
> - For [TiDB Cloud Serverless clusters](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless), the changefeed feature is unavailable.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 100 changefeeds.
- Currently, TiDB Cloud does not support uploading self-signed TLS certificates to connect to Kafka brokers.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.
- If you choose Private Link or Private Service Connect as the network connectivity method, ensure that your TiDB cluster version meets the following requirements:

    - For v6.5.x: version v6.5.9 or later
    - For v7.1.x: version v7.1.4 or later
    - For v7.5.x: version v7.5.1 or later
    - For v8.1.x: all versions of v8.1.x and later are supported
- If you want to use Debezium as your data format, make sure the version of your TiDB cluster is v8.1.0 or later.
- For the partition distribution of Kafka messages, note the following:

    - If you want to distribute changelogs by primary key or index value to Kafka partition with a specified index name, make sure the version of your TiDB cluster is v7.5.0 or later.
    - If you want to distribute changelogs by column value to Kafka partition, make sure the version of your TiDB cluster is v7.5.0 or later.

## Prerequisites

Before creating a changefeed to stream data to Apache Kafka, you need to complete the following prerequisites:

- Set up your network connection
- Add permissions for Kafka ACL authorization

### Network

Ensure that your TiDB cluster can connect to the Apache Kafka service. You can choose one of the following connection methods:

- Private Connect: ideal for avoiding VPC CIDR conflicts and meeting security compliance, but incurs additional [Private Data Link Cost](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost).
- VPC Peering: suitable as a cost-effective option, but requires managing potential VPC CIDR conflicts and security considerations.
- Public IP: suitable for a quick setup.

<SimpleTab>
<div label="Private Connect">

Private Connect leverages **Private Link** or **Private Service Connect** technologies from cloud providers to enable resources in your VPC to connect to services in other VPCs using private IP addresses, as if those services were hosted directly within your VPC.

TiDB Cloud currently supports Private Connect only for self-hosted Kafka. It does not support direct integration with MSK, Confluent Kafka, or other Kafka SaaS services. To connect to these Kafka SaaS services via Private Connect, you can deploy a [kafka-proxy](https://github.com/grepplabs/kafka-proxy) as an intermediary, effectively exposing the Kafka service as self-hosted Kafka. For a detailed example, see [Set Up Self-Hosted Kafka Private Service Connect by Kafka-proxy in Google Cloud](/tidb-cloud/setup-gcp-self-hosted-kafka-private-service-connect.md#set-up-self-hosted-kafka-private-service-connect-by-kafka-proxy). This setup is similar across all Kafka SaaS services.

- If your Apache Kafka service is hosted in AWS, follow [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) to ensure that the network connection is properly configured. After setup, provide the following information in the TiDB Cloud console to create the changefeed:

    - The ID in Kafka Advertised Listener Pattern
    - The Endpoint Service Name
    - The Bootstrap Ports

- If your Apache Kafka service is hosted in Google Cloud, follow [Set Up Self-Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-gcp-self-hosted-kafka-private-service-connect.md) to ensure that the network connection is properly configured. After setup, provide the following information in the TiDB Cloud console to create the changefeed:

    - The ID in Kafka Advertised Listener Pattern
    - The Service Attachment
    - The Bootstrap Ports

- If your Apache Kafka service is hosted in Azure, follow [Set Up Self-Hosted Kafka Private Link Service in Azure](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md) to ensure that the network connection is properly configured. After setup, provide the following information in the TiDB Cloud console to create the changefeed:

    - The ID in Kafka Advertised Listener Pattern
    - The Alias of Private Link Service
    - The Bootstrap Ports

</div>
<div label="VPC Peering">

If your Apache Kafka service is in an AWS VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Kafka service and your TiDB cluster.
2. Modify the inbound rules of the security group that the Apache Kafka service is associated with.

    You must add the CIDR of the region where your TiDB Cloud cluster is located to the inbound rules. The CIDR can be found on the **VPC Peering** page. Doing so allows the traffic to flow from your TiDB cluster to the Kafka brokers.

3. If the Apache Kafka URL contains hostnames, you need to allow TiDB Cloud to be able to resolve the DNS hostnames of the Apache Kafka brokers.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-dns.html).
    2. Enable the **Accepter DNS resolution** option.

If your Apache Kafka service is in a Google Cloud VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Kafka service and your TiDB cluster.
2. Modify the ingress firewall rules of the VPC where Apache Kafka is located.

    You must add the CIDR of the region where your TiDB Cloud cluster is located to the ingress firewall rules. The CIDR can be found on the **VPC Peering** page. Doing so allows the traffic to flow from your TiDB cluster to the Kafka brokers.

</div>
<div label="Public IP">

If you want to provide Public IP access to your Apache Kafka service, assign Public IP addresses to all your Kafka brokers. 

It is **NOT** recommended to use Public IP in a production environment. 

</div>
</SimpleTab>

### Kafka ACL authorization

To allow TiDB Cloud changefeeds to stream data to Apache Kafka and create Kafka topics automatically, ensure that the following permissions are added in Kafka:

- The `Create` and `Write` permissions are added for the topic resource type in Kafka.
- The `DescribeConfigs` permission is added for the cluster resource type in Kafka.

For example, if your Kafka cluster is in Confluent Cloud, you can see [Resources](https://docs.confluent.io/platform/current/kafka/authorization.html#resources) and [Adding ACLs](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls) in Confluent documentation for more information.

## Step 1. Open the changefeed page for Apache Kafka

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.
3. Click **Create Changefeed**, and select **Kafka** as **Destination**.

## Step 2. Configure the changefeed target

The steps vary depending on the connectivity method you select.

<SimpleTab>
<div label="VPC Peering or Public IP">

1. In **Connectivity Method**, select **VPC Peering** or **Public IP**, fill in your Kafka brokers endpoints. You can use commas `,` to separate multiple endpoints.
2. Select an **Authentication** option according to your Kafka authentication configuration.

    - If your Kafka does not require authentication, keep the default option **Disable**.
    - If your Kafka requires authentication, select the corresponding authentication type, and then fill in the **user name** and **password** of your Kafka account for authentication.

3. Select your **Kafka Version**. If you do not know which one to use, use **Kafka v2**.
4. Select a **Compression** type for the data in this changefeed.
5. Enable the **TLS Encryption** option if your Kafka has enabled TLS encryption and you want to use TLS encryption for the Kafka connection.
6. Click **Next** to test the network connection. If the test succeeds, you will be directed to the next page.

</div>
<div label="Private Link (AWS)">

1. In **Connectivity Method**, select **Private Link**.
2. Authorize the [AWS Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts) of TiDB Cloud to create an endpoint for your endpoint service. The AWS Principal is provided in the tip on the web page.
3. Make sure you select the same **Number of AZs** and **AZ IDs of Kafka Deployment**, and fill the same unique ID in **Kafka Advertised Listener Pattern** when you [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) in the **Network** section.
4. Fill in the **Endpoint Service Name** which is configured in [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md).
5. Fill in the **Bootstrap Ports**. It is recommended that you set at least one port for one AZ. You can use commas `,` to separate multiple ports.
6. Select an **Authentication** option according to your Kafka authentication configuration.

    - If your Kafka does not require authentication, keep the default option **Disable**.
    - If your Kafka requires authentication, select the corresponding authentication type, and then fill in the **user name** and **password** of your Kafka account for authentication.

7. Select your **Kafka Version**. If you do not know which one to use, use **Kafka v2**.
8. Select a **Compression** type for the data in this changefeed.
9. Enable the **TLS Encryption** option if your Kafka has enabled TLS encryption and you want to use TLS encryption for the Kafka connection.
10. Click **Next** to test the network connection. If the test succeeds, you will be directed to the next page.
11. TiDB Cloud creates the endpoint for **Private Link**, which might take several minutes.
12. Once the endpoint is created, log in to your cloud provider console and accept the connection request.
13. Return to the [TiDB Cloud console](https://tidbcloud.com) to confirm that you have accepted the connection request. TiDB Cloud will test the connection and proceed to the next page if the test succeeds.

</div>
<div label="Private Service Connect">

1. In **Connectivity Method**, select **Private Service Connect**.    
2. Ensure that you fill in the same unique ID in **Kafka Advertised Listener Pattern** when you [Set Up Self-Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-gcp-self-hosted-kafka-private-service-connect.md) in the **Network** section.
3. Fill in the **Service Attachment** that you have configured in [Setup Self Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-gcp-self-hosted-kafka-private-service-connect.md)
4. Fill in the **Bootstrap Ports**. It is recommended that you provide more than one port. You can use commas `,` to separate multiple ports. 
5. Select an **Authentication** option according to your Kafka authentication configuration.

    - If your Kafka does not require authentication, keep the default option **Disable**.
    - If your Kafka requires authentication, select the corresponding authentication type, and then fill in the **user name** and **password** of your Kafka account for authentication.

6. Select your **Kafka Version**. If you do not know which one to use, use **Kafka v2**.
7. Select a **Compression** type for the data in this changefeed.
8. Enable the **TLS Encryption** option if your Kafka has enabled TLS encryption and you want to use TLS encryption for the Kafka connection.
9. Click **Next** to test the network connection. If the test succeeds, you will be directed to the next page.
10. TiDB Cloud creates the endpoint for **Private Service Connect**, which might take several minutes.
11. Once the endpoint is created, log in to your cloud provider console and accept the connection request.
12. Return to the [TiDB Cloud console](https://tidbcloud.com) to confirm that you have accepted the connection request. TiDB Cloud will test the connection and proceed to the next page if the test succeeds.

</div>
<div label="Private Link (Azure)">

1. In **Connectivity Method**, select **Private Link**.
2. Authorize the Azure subscription of TiDB Cloud or allow anyone with your alias to access your Private Link service before creating the changefeed. The Azure subscription is provided in the **Reminders before proceeding** tip on the web page. For more information about the visibility of Private Link service, see [Control service exposure](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview#control-service-exposure) in Azure documentation.
3. Make sure you fill in the same unique ID in **Kafka Advertised Listener Pattern** when you [Set Up Self-Hosted Kafka Private Link Service in Azure](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md) in the **Network** section.
4. Fill in the **Alias of Private Link Service** which is configured in [Set Up Self-Hosted Kafka Private Link Service in Azure](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md).
5. Fill in the **Bootstrap Ports**. It is recommended that you set at least one port for one AZ. You can use commas `,` to separate multiple ports.
6. Select an **Authentication** option according to your Kafka authentication configuration.

    - If your Kafka does not require authentication, keep the default option **Disable**.
    - If your Kafka requires authentication, select the corresponding authentication type, and then fill in the **user name** and **password** of your Kafka account for authentication.

7. Select your **Kafka Version**. If you do not know which one to use, use **Kafka v2**.
8. Select a **Compression** type for the data in this changefeed.
9. Enable the **TLS Encryption** option if your Kafka has enabled TLS encryption and you want to use TLS encryption for the Kafka connection.
10. Click **Next** to test the network connection. If the test succeeds, you will be directed to the next page.
11. TiDB Cloud creates the endpoint for **Private Link**, which might take several minutes.
12. Once the endpoint is created, log in to the [Azure portal](https://portal.azure.com/) and accept the connection request.
13. Return to the [TiDB Cloud console](https://tidbcloud.com) to confirm that you have accepted the connection request. TiDB Cloud will test the connection and proceed to the next page if the test succeeds.

</div>
</SimpleTab>

## Step 3. Set the changefeed

1. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](/table-filter.md).

    - **Filter Rules**: you can set filter rules in this column. By default, there is a rule `*.*`, which stands for replicating all tables. When you add a new rule, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules in the box on the right. You can add up to 100 filter rules.
    - **Tables with valid keys**: this column displays the tables that have valid keys, including primary keys or unique indexes.
    - **Tables without valid keys**: this column shows tables that lack primary keys or unique keys. These tables present a challenge during replication because the absence of a unique identifier can result in inconsistent data when the downstream handles duplicate events. To ensure data consistency, it is recommended to add unique keys or primary keys to these tables before initiating the replication. Alternatively, you can add filter rules to exclude these tables. For example, you can exclude the table `test.tbl1` by using the rule `"!test.tbl1"`.

2. Customize **Event Filter** to filter the events that you want to replicate.

    - **Tables matching**: you can set which tables the event filter will be applied to in this column. The rule syntax is the same as that used for the preceding **Table Filter** area. You can add up to 10 event filter rules per changefeed.
    - **Ignored events**: you can set which types of events the event filter will exclude from the changefeed.

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
    - In the **Schema Registry** area, fill in your schema registry endpoint. If you enable **HTTP Authentication**, the fields for user name and password are displayed and automatically filled in with your TiDB cluster endpoint and password.

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

        If you want the changefeed to send Kafka messages of a table to different partitions, choose this distribution method. The primary key or index value of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures row-level orderliness.

    - **Distribute changelogs by table to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to one Kafka partition, choose this distribution method. The table name of a row changelog will determine which partition the changelog is sent to. This distribution method ensures table orderliness but might cause unbalanced partitions.

    - **Distribute changelogs by timestamp to Kafka partition**

        If you want the changefeed to send Kafka messages to different Kafka partitions randomly, choose this distribution method. The commitTs of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures orderliness in each partition. However, multiple changes of a data item might be sent to different partitions and the consumer progress of different consumers might be different, which might cause data inconsistency. Therefore, the consumer needs to sort the data from multiple partitions by commitTs before consuming.

    - **Distribute changelogs by column value to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to different partitions, choose this distribution method. The specified column values of a row changelog will determine which partition the changelog is sent to. This distribution method ensures orderliness in each partition and guarantees that the changelog with the same column values is send to the same partition.

9. In the **Topic Configuration** area, configure the following numbers. The changefeed will automatically create the Kafka topics according to the numbers.

    - **Replication Factor**: controls how many Kafka servers each Kafka message is replicated to. The valid value ranges from [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) to the number of Kafka brokers.
    - **Partition Number**: controls how many partitions exist in a topic. The valid value range is `[1, 10 * the number of Kafka brokers]`.

10. Click **Next**.

## Step 4. Configure your changefeed specification

1. In the **Changefeed Specification** area, specify the number of Replication Capacity Units (RCUs) to be used by the changefeed.
2. In the **Changefeed Name** area, specify a name for the changefeed.
3. Click **Next** to check the configurations you set and go to the next page.

## Step 5. Review the configurations

On this page, you can review all the changefeed configurations that you set.

If you find any error, you can go back to fix the error. If there is no error, you can click the check box at the bottom, and then click **Create** to create the changefeed.
