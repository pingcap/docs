---
title: Sink to Apache Kafka
summary: This document explains how to create a changefeed to stream data from TiDB Cloud to Apache Kafka. It includes restrictions, prerequisites, and steps to configure the changefeed for Apache Kafka. The process involves setting up network connections, adding permissions for Kafka ACL authorization, and configuring the changefeed specification.
---

# Sink to Apache Kafka

This document describes how to create a changefeed to stream data from TiDB Cloud to Apache Kafka.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 100 changefeeds.
- Currently, TiDB Cloud does not support uploading self-signed TLS certificates to connect to Kafka brokers.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.

## Prerequisites

Before creating a changefeed to stream data to Apache Kafka, you need to complete the following prerequisites:

- Set up your network connection
- Add permissions for Kafka ACL authorization

### Network

Ensure that your TiDB cluster can connect to the Apache Kafka service. Currently, TiDB cluster can only connect to Apache Kafka through the Public IP.

> **Note:**
>
> If you want to expose your Apache Kafka through a more secure method, such as private link or VPC peering, please contact us for help. To request it, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for TiDB Cloud Serverless database audit logging" in the **Description** field and click **Submit**.


To provide Public IP access to your Apache Kafka service, assign Public IP addresses to all your Kafka brokers. 

### Kafka ACL authorization

To allow TiDB Cloud changefeeds to stream data to Apache Kafka and create Kafka topics automatically, ensure that the following permissions are added in Kafka:

- The `Create` and `Write` permissions are added for the topic resource type in Kafka.
- The `DescribeConfigs` permission is added for the cluster resource type in Kafka.

For example, if your Kafka cluster is in Confluent Cloud, you can see [Resources](https://docs.confluent.io/platform/current/kafka/authorization.html#resources) and [Adding ACLs](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls) in Confluent documentation for more information.

## Create a changefeed sink to Apache Kafka with TiDB Cloud CLI

To create a changefeed to stream data from TiDB Cloud to Apache Kafka, using the TiDB Cloud CLI command:

```bash
ticloud serverless changefeed create --cluster-id <cluster-id> --name <changefeed-name> --type KAFKA --kafka <kafka-json> --filter <filter-json> --start-tso <start-tso>
```

- `<cluster-id>`: the ID of the TiDB Cloud cluster that you want to create the changefeed for.
- `<changefeed-name>`: the name of the changefeed, it is optional. If you do not specify a name, TiDB Cloud automatically generates a name for the changefeed.
- type: the type of the changefeed, which is `KAFKA` in this case.
- kafka: a JSON string that contains the configurations for the changefeed to stream data to Apache Kafka. See [Kafka configurations](#kafka-configurations) for more information about the configurations.
- filter: a JSON string that contains the configurations for the changefeed to filter tables and events. See [Filter configurations](#filter-configurations) for more information about the configurations.
- start-tso: the TSO from which the changefeed starts to replicate data. If you do not specify a TSO, the current TSO is used by default. To learn more about TSO, see [TSO in TiDB](https://docs.pingcap.com/tidb/stable/tso/). 

### Filter configurations

To get a template of `filter` configurations, using the TiDB Cloud CLI command:

```bash
ticloud serverless changefeed template
```

To get the explanation of the template, using the TiDB Cloud CLI command:

```bash
ticloud serverless changefeed template --explain
```

The configurations in the `filter` JSON string are used to filter tables and events that you want to replicate. Below is an example of a `filter` configuration:

<details>
<summary>Example filter configuration</summary>

```json
{
  "filterRule": ["test.t1", "test.t2"],
  "mode": "IGNORE_NOT_SUPPORT_TABLE",
  "eventFilterRule": [
    {
      "matcher": ["test.t1", "test.t2"],
      "ignore_event": ["all dml", "all ddl"]
    }
  ]
}
```
</details>

1. **Filter Rule**: you can set `filter rules` to filter the tables that you want to replicate. See [Table Filter](https://docs.pingcap.com/tidb/stable/table-filter/) for more information about the rule syntax.
2. **Event Filter Rule**: you can set the `matcher` and `ignore_event` to ignore some events matching the rules. See [Event filter rules](https://docs.pingcap.com/tidb/stable/ticdc-filter/#event-filter-rules) to get all the supported event types.
3. **mode**: set mode to `IGNORE_NOT_SUPPORT_TABLE` to ignore the tables that do not support replication, such as the tables that do not have primary keys or unique indexes. set mode to `FORCE_SYNC` to force the changefeed to replicate all tables.

### Kafka configurations

To get a template of `kafka` configurations, using the TiDB Cloud CLI command:

```bash
ticloud serverless changefeed template
```

To get the explanation of the template, using the TiDB Cloud CLI command:

```bash
ticloud serverless changefeed template --explain
```

The configurations in the `kafka` JSON string are used to configure how the changefeed streams data to Apache Kafka. Below is an example of a `filter` configuration:

<details>
<summary>Example filter configuration</summary>

```json
{
        "network_info": {
                "network_type": "PUBLIC"
        },
        "broker": {
                "kafka_version": "VERSION_2XX",
                "broker_endpoints": "broker1:9092,broker2:9092",
                "tls_enable": false,
                "compression": "NONE"
        },
        "authentication": {
                "auth_type": "DISABLE",
                "user_name": "",
                "password": ""
        },
        "data_format": {
                "protocol": "CANAL_JSON",
                "enable_tidb_extension": false,
                "avro_config": {
                        "decimal_handling_mode": "PRECISE",
                        "bigint_unsigned_handling_mode": "LONG",
                        "schema_registry": {
                                "schema_registry_endpoints": "",
                                "enable_http_auth": false,
                                "user_name": "",
                                "password": ""
                        }
                }
        },
        "topic_partition_config": {
                "dispatch_type": "ONE_TOPIC",
                "default_topic": "test-topic",
                "topic_prefix": "_prefix",
                "separator": "_",
                "topic_suffix": "_suffix",
                "replication_factor": 1,
                "partition_num": 1,
                "partition_dispatchers": [{
                        "partition_type": "TABLE",
                        "matcher": ["*.*"],
                        "index_name": "index1",
                        "columns": ["col1", "col2"]
                }]
        },
        "column_selectors": [{
                "matcher": ["*.*"],
                "columns": ["col1", "col2"]
        }]
}
```
</details>

The main configuration fields are as follows:

1. **network_info**: Only `PUBLIC` network type is supported for now. This means that the TiDB cluster can connect to the Apache Kafka service through the Public IP.
   
2. **broker**: Contains Kafka broker connection information:
   
    - `kafka_version`: The Kafka version, such as `VERSION_2XX`.
    - `broker_endpoints`: Comma-separated list of broker endpoints.
    - `tls_enable`: Whether to enable TLS for the connection.
    - `compression`: The compression type for messages, support `NONE`, `GZIP`, `LZ4`, `SNAPPY`, and `ZSTD`.

"DISABLE", "SASL_PLAIN", "SASL_SCRAM_SHA_256", "SASL_SCRAM_SHA_512"

3. **authentication**: Authentication settings for connecting to Kafka, support `DISABLE`, `SASL_PLAIN`, `SASL_SCRAM_SHA_256` and `SASL_SCRAM_SHA_512`. The `user_name` and `password` fields are required if you set the `auth_type` to `SASL_PLAIN`, `SASL_SCRAM_SHA_256`, or `SASL_SCRAM_SHA_512`.
   
4. **data_format.protocol**: Support `CANAL_JSON`, `AVRO`, and `OPEN_PROTOCOL`.

    - Avro is a compact, fast, and binary data format with rich data structures, which is widely used in various flow systems. For more information, see [Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol).
    - Canal-JSON is a plain JSON text format, which is easy to parse. For more information, see [Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json).
    - Open Protocol is a row-level data change notification protocol that provides data sources for monitoring, caching, full-text indexing, analysis engines, and primary-secondary replication between different databases. For more information, see [Open Protocol data format](https://docs.pingcap.com/tidb/stable/ticdc-open-protocol). 
    - Debezium is a tool for capturing database changes. It converts each captured database change into a message called an "event" and sends these events to Kafka. For more information, see [Debezium data format](https://docs.pingcap.com/tidb/stable/ticdc-debezium).

5. **data_format.enable_tidb_extension**: if you want to add TiDB-extension fields to the Kafka message body with `AVRO` or `CANAL_JSON` data format.

    For more information about TiDB-extension fields, see [TiDB extension fields in Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields) and [TiDB extension fields in Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field).

6. **data_format.avro_config**: If you select **Avro** as your data format, you need to set the Avro-specific configurations:

    - `decimal_handling_mode` and `bigint_unsigned_handling_mode`: specify how TiDB Cloud handles the decimal and unsigned bigint data types in Kafka messages.
    - `schema_registry`: the schema registry endpoint. If you enable `enable_http_auth`, the fields for user name and password are required.

7. **topic_partition_config.dispatch_type**: Support `ONE_TOPIC`, `BY_TABLE` and `BY_DATABASE`. Controls how the changefeed creates Kafka topics, by table, by database, or creating one topic for all changelogs.

    - **Distribute changelogs by table to Kafka Topics**

        If you want the changefeed to create a dedicated Kafka topic for each table, choose this mode. Then, all Kafka messages of a table are sent to a dedicated Kafka topic. You can customize topic names for tables by setting a `topic_prefix`, a `separator` and between a database name and table name, and a `topic_suffix`. For example, if you set the separator as `_`, the topic names are in the format of `<Prefix><DatabaseName>_<TableName><Suffix>`.

        For changelogs of non-row events, such as Create Schema Event, you can specify a topic name in the `default_topic` field. The changefeed will create a topic accordingly to collect such changelogs.

    - **Distribute changelogs by database to Kafka Topics**

        If you want the changefeed to create a dedicated Kafka topic for each database, choose this mode. Then, all Kafka messages of a database are sent to a dedicated Kafka topic. You can customize topic names of databases by setting a `topic_prefix` and a `topic_suffix`.

        For changelogs of non-row events, such as Resolved Ts Event, you can specify a topic name in the `default_topic` field. The changefeed will create a topic accordingly to collect such changelogs.

    - **Send all changelogs to one specified Kafka Topic**

        If you want the changefeed to create one Kafka topic for all changelogs, choose this mode. Then, all Kafka messages in the changefeed will be sent to one Kafka topic. You can define the topic name in the `default_topic` field.

> Note
>
> If you use `AVRO` data format, only `BY_TABLE` dispatch type is supported.

1. **topic_partition_config.default_topic**: The default topic name for non-row events, such as Create Schema Event and Resolved Ts Event. If you set the `dispatch_type` to `ONE_TOPIC`, this field is required.

    - `topic_prefix`: The prefix for the topic name.
    - `separator`: The separator between a database name and table name in the topic name.
    - `topic_suffix`: The suffix for the topic name.

2. **topic_partition_config.replication_factor**: controls how many Kafka servers each Kafka message is replicated to. The valid value ranges from [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) to the number of Kafka brokers.

3.  **topic_partition_config.partition_num**: controls how many partitions exist in a topic. The valid value range is `[1, 10 * the number of Kafka brokers]`.

4.  **topic_partition_config.partition_dispatchers**: decide which partition a Kafka message will be sent to. `partition_type` Support `TABLE`, `INDEX_VALUE`, `TS` and `COLUMN`.

    - **Distribute changelogs by primary key or index value to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to different partitions, set `partition_type` to `INDEX_VALUE` and set the `index_name`. The primary key or index value of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures row-level orderliness.

    - **Distribute changelogs by table to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to one Kafka partition, set `partition_type` to `TABLE`. The table name of a row changelog will determine which partition the changelog is sent to. This distribution method ensures table orderliness but might cause unbalanced partitions.

    - **Distribute changelogs by timestamp to Kafka partition**

        If you want the changefeed to send Kafka messages to different Kafka partitions randomly, set `partition_type` to `TS`.. The commitTs of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures orderliness in each partition. However, multiple changes of a data item might be sent to different partitions and the consumer progress of different consumers might be different, which might cause data inconsistency. Therefore, the consumer needs to sort the data from multiple partitions by commitTs before consuming.

    - **Distribute changelogs by column value to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to different partitions, set `partition_type` to `COLUMN` and set the `columns`. The specified column values of a row changelog will determine which partition the changelog is sent to. This distribution method ensures orderliness in each partition and guarantees that the changelog with the same column values is send to the same partition.

    For more information about the matching rules, see [Partition dispatchers](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-kafka/#partition-dispatchers).

5.  **column_selectors**: columns from events and send only the data changes related to those columns to the downstream.

    - `matcher`: specify which tables the column selector applies to. For tables that do not match any rule, all columns are sent.
    - `columns`: specify which columns of the matched tables will be sent to the downstream.

    For more information about the matching rules, see [Column selectors](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-kafka/#column-selectors).
