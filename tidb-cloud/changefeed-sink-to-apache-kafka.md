---
title: Create a changefeed to stream data from TiDB Cloud to Apache Kafka
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to Apache Kafka. 
---

# Create a changefeed to stream data from TiDB Cloud to Apache Kafka

This document describes how to stream data from TiDB Cloud to Apache Kafka using the changefeed.

## Prerequisites

### Network

Make sure that your TiDB Cluster can connect to the Apache Kafka service.

If your Apache Kafka service is in an AWS VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Kafka service and your TiDB cluster. 
2. Modify the inbound rules of the security group that the Apache Kafka service is associated with. 

    You must add the CIDR of the region where your TiDB Cloud cluster is located to the inbound rules. The CIDR can be found on the VPC Peering page. Doing so allows the traffic to flow from your TiDB cluster to the Kafka brokers.

3. If the Apache Kafka URL contains hostnames, you need to allow TiDB Cloud to be able to resolve the DNS hostnames of the Apache Kafka brokers.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

If your Apache Kafka service is in a GCP VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Kafka service and your TiDB cluster. 
2. Modify the ingress firewall rules of the VPC where Apache Kafka is located. 

    You must add the CIDR of the Region where your TiDB Cloud cluster is located to the ingress firewall rules. The CIDR can be found on the VPC Peering page. Doing so allows the traffic to flow from your TiDB cluster to the Kafka brokers.

### Kafka ACL authorization

To write stream data to Apache Kafka, and create topics automatically, there are the minimum set of permissions required for TiDB Cloud Changefeed:

 - The Create and Write permissions for the Topic resource type.
 - The DescribeConfigs permission for the Cluster resource type.

## Step 1. Go to the creation wizard page

1. Navigate to the **Changefeed** tab of your TiDB cluster.
2. Click **Sink to Apache Kafka**.

## Step 2. Configure the changefeed target

1. Select the **Kafka** target in the **Target Type** field set, and then you can see the **Brokers Configuration** field set under the **Target Type** field set.
2. Fill the Kafka Endpoints. You can use commas(',') to separate multiple endpoints.
3. Select the Kafka Version. If you don't known what the version of Kafka is, you can use the Kafka V2.
4. Select the Kafka connection compression type.
5. Switch on the **TLS Encryption** option if you want to use TLS encryption. And the Kafka connection will be required to use TLS encryption.
6. Select the **Authentication** option you want to use.
   - Disable means that no authentication is required.
   - SASL/PLAIN means that the Kafka connection will be required to use SASL/PLAIN authentication.
   - SASL/SCRAM-SHA-256 means that the Kafka connection will be required to use SASL/SCRAM-SHA-256 authentication.
   - SASL/SCRAM-SHA-512 means that the Kafka connection will be required to use SASL/SCRAM-SHA-512 authentication.
7. Fill the **Username** and **Password** fields under the **Authentication** field set if you select the SASL/PLAIN, SASL/SCRAM-SHA-256 or SASL/SCRAM-SHA-512 authentication type.
8. Click **Next** to check the current input and go to the next page.
   
## Step 3. Set the changefeed

1. You can select the data format you want in **Date Format** field set.
   - Avro is a compact, fast, binary data format with the rich data structures. Widely used in various flow systems. Also see [Avro data format]()
   - Canal-JSON is a plain JSON text format, easy to parse. Also see [Canal-JSON Data format]()
2. You can switch on the TiDB Extension option if you want add some TiDB-extension fields to the message body. Alse see [TiDB extension fields in Avro data format]() and [TiDB extension fields in Canal-JSON data format]()
3. There are two another options when you use the Avro data format: Handle Decimal and Handle Bigint Unsigned option specified how to handle the decimal and Bigint data type.
4. You will see the **Schema Registry** field set under the **Data Format** field set when you use Avro data format. You should fill the schema registry endpoints and the username and password if you enable the HTTP Authentication.
5. In **Topic Distribution** field set, you can decide which topic a kafka message should be sent to:
   - Distribute changelogs by table to Kafka Topics. Kafka messages of a table will be sent to a Kafka topic. The topic name is depended on the prefix, separator, suffix you set and the name of table and database.
   - Distribute changelogs by database to Kafka Topics. Kafka messages of a database will be sent to a Kafka topic. The topic name is depended on the prefix, suffix you set and the name of database.
   - Send all changelogs to one specified Kafka Topic. All Kafka messages will be sent to the specified Kafka Topic.
6. In **Partition Distribution** field set, you can decide which partition a kafka message should be sent to:
   - Distribute changelogs by index value to Kafka partition. Kafka messages of a table will be sent to many diffierent partitions. The partition number is depended on the index value of the row changedlog. This kind of distribution method will get a better partition balance and ensures row-level orderliness.
   - Distribute changelogs by table to Kafka Partitions. Kafka messages of a table will be sent to one Kafka partition. The partition number is depended on the table name of the row changedlog. This kind of distribution method may cause partitions to be unbalanced, but better orderliness is guaranteed.
7. In **Topic Configuration** field set, this two fields are used to create the Kafka topic automatically by this changefeed.
   - The replication factor controls how many servers will replicate each message that is written. 
   - The partition number controls how many partitions exist.
8. Click **Next** to check the current input and go to the next page.

## Step 4. Review

In this page, you can review the configuration you have set. If there is any error, you can go back to the previous page to fix the error. If there is no error, you can click **Create** to create the changefeed.


## Restrictions

Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions).
