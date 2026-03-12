---
title: Kafka
---

[Apache Kafka](https://kafka.apache.org/) is an open-source distributed event streaming platform that allows you to publish and subscribe to streams of records. It is designed to handle high-throughput, fault-tolerant, and real-time data feeds. Kafka enables seamless communication between various applications, making it an ideal choice for building data pipelines and streaming data processing applications.

Databend provides the following plugins and tools for data ingestion from Kafka topics:

- [databend-kafka-connect](#databend-kafka-connect)
- [bend-ingest-kafka](#bend-ingest-kafka)

## databend-kafka-connect

The [databend-kafka-connect](https://github.com/databendcloud/databend-kafka-connect) is a Kafka Connect sink connector plugin designed specifically for Databend. This plugin enables seamless data transfer from Kafka topics directly into Databend tables, allowing for real-time data ingestion with minimal configuration. Key features of databend-kafka-connect include:

- Automatically creates tables in Databend based on the data schema.
- Supports both **Append Only** and **Upsert** write modes.
- Automatically adjusts the schema of Databend tables as the structure of incoming data changes.

To download databend-kafka-connect and learn more about the plugin, visit the [GitHub repository](https://github.com/databendcloud/databend-kafka-connect) and refer to the README for detailed instructions.

## bend-ingest-kafka

[bend-ingest-kafka](https://github.com/databendcloud/bend-ingest-kafka) is a high-performance data ingestion tool specifically designed to efficiently load data from Kafka topics into Databend tables. It supports two primary modes of operation: JSON Transform Mode and Raw Mode, catering to different data ingestion requirements. Key features of bend-ingest-kafka include:

- Supports two modes: **JSON Transform Mode**, which maps Kafka JSON data directly to Databend tables based on the data schema, and **Raw Mode**, which ingests raw Kafka data while capturing complete Kafka record metadata.
- Provides configurable batch processing settings for size and interval, ensuring efficient and scalable data ingestion.

To download bend-ingest-kafka and learn more about the tool, visit the [GitHub repository](https://github.com/databendcloud/bend-ingest-kafka) and refer to the README for detailed instructions.

## Tutorials

- [Loading from Kafka with bend-ingest-kafka](/tutorials/ingest-and-stream/kafka-bend-ingest-kafka)
- [Loading from Kafka with databend-kafka-connect](/tutorials/ingest-and-stream/kafka-databend-kafka-connect)
