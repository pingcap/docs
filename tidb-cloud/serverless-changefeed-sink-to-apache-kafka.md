---
title: Sink Data from TiDB Cloud Serverless to Apache Kafka
summary: This document explains how to create a changefeed to stream data from TiDB Cloud Serverless to Apache Kafka. It includes restrictions, prerequisites, and steps to configure the changefeed for Apache Kafka. The process involves setting up network connections, adding permissions for Kafka ACL authorization, and configuring the changefeed specification.
---

# Sink Data from TiDB Cloud Serverless to Apache Kafka

This document describes how to create a changefeed to stream data from TiDB Cloud Serverless to Apache Kafka.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 100 changefeeds.
- Currently, TiDB Cloud does not support uploading self-signed TLS certificates to connect to Kafka brokers.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.

## Prerequisites

Before creating a changefeed to stream data to Apache Kafka, you need to complete the following prerequisites:

- Set up your network connection.
- Add permissions for Kafka ACL authorization.

### Network

Ensure that your TiDB cluster can connect to the Apache Kafka service. Currently, TiDB Serverless clusters can only connect to Apache Kafka through public IP addresses.

> **Note:**
>
> If you want to expose your Apache Kafka through a more secure method, such as Private Link or VPC peering, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in your request in the **Description** field and click **Submit**.

To enable public IP access to your Apache Kafka service, assign public IP addresses to all Kafka brokers.

### Kafka ACL authorization

To allow TiDB Cloud changefeeds to stream data to Apache Kafka and create Kafka topics automatically, ensure that the following permissions are added in Kafka:

- The `Create` and `Write` permissions are added for the topic resource type in Kafka.
- The `DescribeConfigs` permission is added for the cluster resource type in Kafka.

For example, if your Kafka cluster is in Confluent Cloud, you can see [Resources](https://docs.confluent.io/platform/current/kafka/authorization.html#resources) and [Adding ACLs](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls) in Confluent documentation for more information.

## Create a changefeed with TiDB Cloud CLI

To create a changefeed that streams data from TiDB Cloud to Apache Kafka, use the following TiDB Cloud CLI command:

```bash
ticloud serverless changefeed create --cluster-id <cluster-id> --name <changefeed-name> --type KAFKA --kafka <kafka-json> --filter <filter-json> --start-tso <start-tso>
```

- `<cluster-id>`: the ID of the TiDB Cloud cluster that you want to create the changefeed for.
- `<changefeed-name>` (optional): the name of the changefeed. If not specified, TiDB Cloud automatically generates a changefeed name.
- `type`: the changefeed type. To stream data to Apache Kafka, set it to `KAFKA`.
- `kafka`: a JSON string that contains the configuration for streaming data to Apache Kafka. For more information, see [Kafka configurations](#kafka-configurations).
- `filter`: a JSON string that specifies which tables and events to replicate. For more information, see [Filter configurations](#filter-configurations).
- `start-tso`: the TSO from which the changefeed starts to replicate data. If not specified, the current TSO is used by default. For more information, see [TSO in TiDB](https://docs.pingcap.com/tidb/stable/tso/).

### Filter configurations

You can specify `--filter <filter-json>` to filter tables and events that you want to replicate. 

To get a template of `filter` configurations, run the following TiDB Cloud CLI command:

```bash
ticloud serverless changefeed template
```

To view explanations of the template, run the following TiDB Cloud CLI command:

```bash
ticloud serverless changefeed template --explain
```

The following is an example `filter` configuration:

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

- `filterRule`: filters the tables to replicate. For the detailed rule syntax, see [Table Filter](https://docs.pingcap.com/tidb/stable/table-filter/).
- `eventFilterRule`: filters specific events for the matched tables. You can use the `matcher` field to specify the target tables, and use the `ignore_event` field to list the event types to skip. For supported event types, see [Event filter rules](https://docs.pingcap.com/tidb/stable/ticdc-filter/#event-filter-rules).
- `mode`: controls the behavior for unsupported tables. You can set it to one of the following:
  
   - `IGNORE_NOT_SUPPORT_TABLE`: skip tables that do not support replication (for example, tables without primary or unique keys).
   - `FORCE_SYNC`: force replication of all tables regardless of support status.

### Kafka configurations

You can specify `--kafka <kafka-json>` to configure how the changefeed streams data to Apache Kafka.

To get a template of `kafka` configurations, run the following TiDB Cloud CLI command:

```bash
ticloud serverless changefeed template
```

To view explanations of the template, run the following TiDB Cloud CLI command:

```bash
ticloud serverless changefeed template --explain
```

The following is an example `kafka` configuration:

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
                        "confluent_schema_registry": {
                                "endpoint": "",
                                "enable_http_auth": false,
                                "user_name": "",
                                "password": ""
                        },
                        "aws_glue_schema_registry": {
                                "region": "",
                                "name": "",
                                "access_key_id": "",
                                "secret_access_key": ""
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

The main configuration fields are as follows:

- `network_info`: currently, only the `PUBLIC` network type is supported. This means that the TiDB Cloud Serverless clusters can only connect to the Apache Kafka service through public IP addresses.

- `broker`: specifies the Kafka broker connection information.

    - `kafka_version`: the Kafka version. Supported values: `VERSION_2XX` or `VERSION_3XX`.
    - `broker_endpoints`: a comma-separated list of Kafka brokers.
    - `tls_enable`: whether to enable TLS for the connection.
    - `compression`: the message compression type. Supported values: `NONE`, `GZIP`, `LZ4`, `SNAPPY`, or `ZSTD`.

- `authentication`: specifies the Kafka authentication method. Supported values of `auth_type`: `DISABLE`, `SASL_PLAIN`, `SASL_SCRAM_SHA_256`, or `SASL_SCRAM_SHA_512`. If you set `auth_type` to `SASL_PLAIN`, `SASL_SCRAM_SHA_256`, or `SASL_SCRAM_SHA_512`, `user_name` and `password` are required.

- `data_format.protocol`: specifies the output format. 

    - `AVRO`: Avro is a compact, fast, and binary data format with rich data structures, which is widely used in various flow systems. For more information, see [Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol).
    - `CANAL_JSON`: Canal-JSON is a plain JSON text format, which is easy to parse. For more information, see [Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json).
    - `OPEN_PROTOCOL`: Open Protocol is a row-level data change notification protocol that provides data sources for monitoring, caching, full-text indexing, analysis engines, and primary-secondary replication between different databases. For more information, see [Open Protocol data format](https://docs.pingcap.com/tidb/stable/ticdc-open-protocol).

- `data_format.enable_tidb_extension`: controls whether to include TiDB-specific extension fields in Kafka messages when using the `AVRO` or `CANAL_JSON` format.

    For more information about TiDB extension fields, see [TiDB extension fields in Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields) and [TiDB extension fields in Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field).

- `data_format.avro_config`: if you select **Avro** as your data format, you need to set the Avro-specific configurations.

    - `decimal_handling_mode` and `bigint_unsigned_handling_mode`: controls how TiDB Cloud handles the decimal and unsigned bigint data types in Kafka messages.
    - `confluent_schema_registry`: the configuration for confluent schema registry. If authentication is required, set `enable_http_auth` to `true` and configure the `user_name` and `password`. For more information, see [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html).
    - `aws_glue_schema_registry`: the configuration for AWS Glue schema registry. If you want to use AWS Glue schema registry, set `region`, `name`, `access_key_id`, and `secret_access_key` accordingly. For more information, see [AWS Glue Schema Registry](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html).

        For more information about the Avro configurations, see [Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol).

- `topic_partition_config.dispatch_type`: controls how the changefeed creates Kafka topics. Supported values: `ONE_TOPIC`, `BY_TABLE`, or `BY_DATABASE`. If you use the `AVRO` data format, only the `BY_TABLE` dispatch type is supported.

    - `BY_TABLE`: distributes changelogs by table to Kafka topics.

        If you want the changefeed to create a dedicated Kafka topic for each table, set `dispatch_type` to `BY_TABLE`. Then, all Kafka messages of a table are sent to a dedicated Kafka topic. You can customize topic names for tables by setting a `topic_prefix`, a `separator` between a database name and table name, and a `topic_suffix`. For example, if you set the separator as `_`, the topic names are in the format of `<Prefix><DatabaseName>_<TableName><Suffix>`.

        For changelogs of non-row events, such as Create Schema Event, you can specify a topic name in the `default_topic` field. The changefeed will create a topic accordingly to collect such changelogs.

    - `BY_DATABASE`: distributes changelogs by database to Kafka topics.

        If you want the changefeed to create a dedicated Kafka topic for each database, set `dispatch_type` to `BY_DATABASE`. Then, all Kafka messages of a database are sent to a dedicated Kafka topic. You can customize topic names of databases by setting a `topic_prefix` and a `topic_suffix`.

        For changelogs of non-row events, such as Resolved Ts Event, you can specify a topic name in the `default_topic` field. The changefeed will create a topic accordingly to collect such changelogs.

    - `ONE_TOPIC`: sends all changelogs to one specified Kafka topic.

        If you want the changefeed to create one Kafka topic for all changelogs, set `dispatch_type` to `ONE_TOPIC`. Then, all Kafka messages in the changefeed will be sent to one Kafka topic. You can define the topic name in the `default_topic` field.

- `topic_partition_config.replication_factor`: controls how many Kafka brokers each Kafka message is replicated to. The valid value ranges from [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) to the total number of Kafka brokers.

- `topic_partition_config.partition_num`: controls how many partitions exist in a topic. The valid value range is `[1, 10 * the total number of Kafka brokers]`.

- `topic_partition_config.partition_dispatchers`: controls which partition a Kafka message will be sent to. Support values: `INDEX_VALUE`, `TABLE`, `TS` and `COLUMN`.

    - `INDEX_VALUE`: distributes changelogs by primary key or index value to Kafka partitions.

        If you want the changefeed to send Kafka messages of a table to different partitions, set `partition_type` to `INDEX_VALUE` and set the `index_name`. The primary key or index value of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures row-level orderliness.

    - `TABLE`: distributes changelogs by table to Kafka partitions.

        If you want the changefeed to send Kafka messages of a table to one Kafka partition, set `partition_type` to `TABLE`. The table name of a row changelog will determine which partition the changelog is sent to. This distribution method ensures table orderliness but might cause unbalanced partitions.

    - `TS`: distributes changelogs by timestamp to Kafka partitions.

        If you want the changefeed to send Kafka messages to different Kafka partitions randomly, set `partition_type` to `TS`. The commitTs of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures orderliness in each partition. However, multiple changes of a data item might be sent to different partitions and the consumer progress of different consumers might be different, which might cause data inconsistency. Therefore, the consumer needs to sort the data from multiple partitions by commitTs before consuming.

    - `COLUMN`: distributes changelogs by column value to Kafka partitions.

        If you want the changefeed to send Kafka messages of a table to different partitions, set `partition_type` to `COLUMN` and set the `columns`. The specified column values of a row changelog will determine which partition the changelog is sent to. This distribution method ensures orderliness in each partition and guarantees that the changelogs with the same column values are sent to the same partition.

    For more information about the matching rules, see [Partition dispatchers](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-kafka/#partition-dispatchers).

-  `column_selectors`: selects columns from events. TiDB Cloud only sends the data changes related to those columns to the downstream.

    - `matcher`: specifies which tables the column selector applies to. For tables that do not match any rule, all columns are sent.
    - `columns`: specifies which columns of the matched tables will be sent to the downstream.

    For more information about the matching rules, see [Column selectors](https://docs.pingcap.com/tidb/stable/ticdc-sink-to-kafka/#column-selectors).
