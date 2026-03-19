---
title: Data Migration Overview
summary: Select your source database and migration requirements to find the most suitable migration method to Databend.
---

# Data Migration Overview

Select your source database and migration requirements to find the most suitable migration method to Databend.

## MySQL to Databend

Databend supports two main migration approaches from MySQL:

| Migration Approach       | Recommended Tool             | Supported MySQL versions |
|--------------------------|------------------------------|--------------------------|
| Batch Loading            | bend-archiver                | All MySQL versions       |
| Continuous Sync with CDC | Debezium                     | All MySQL versions       |

### When to Choose Real-time Migration (CDC)

> **Recommendation**: For real-time migration, we recommend **Debezium** as the default choice.

- You need continuous data synchronization with minimal latency
- You need to capture all data changes (inserts, updates, deletes)

| Tool | Capabilities | Best For | Choose When |
|------|------------|----------|-------------|
| [Debezium](/tidb-cloud-lake/tutorials/migrate-from-mysql-with-debezium.md) | CDC, Full Load | Capturing row-level changes with minimal latency | You need complete CDC with all DML operations (INSERT/UPDATE/DELETE); You want binlog-based replication for minimal impact on source database |
| [Flink CDC](/tidb-cloud-lake/tutorials/migrate-from-mysql-with-flink-cdc.md) | CDC, Full Load, Transformation | Complex ETL with real-time transformation | You need to filter or transform data during migration; You need a scalable processing framework; You want SQL-based transformation capabilities |
| [Kafka Connect](/tidb-cloud-lake/tutorials/migrate-from-mysql-with-kafka-connect.md) | CDC, Incremental, Full Load | Existing Kafka infrastructure | You already use Kafka; You need simple configuration; You can use timestamp or auto-increment columns for incremental sync |

### When to Choose Batch Migration

> **Recommendation**: For batch migration, we recommend **bend-archiver** as the default choice.

- You need one-time or scheduled data transfers
- You have large volumes of historical data to migrate
- You don't need real-time synchronization

| Tool | Capabilities | Best For | Choose When |
|------|------------|----------|-------------|
| [bend-archiver](/tidb-cloud-lake/tutorials/migrate-from-mysql-with-bend-archiver.md) | Full Load, Incremental | Efficient historical data archiving | You have time-partitioned data; You need to archive historical data; You want a lightweight, focused tool |
| [DataX](/tidb-cloud-lake/tutorials/migrate-from-mysql-with-datax.md) | Full Load, Incremental | High-performance large dataset transfers | You need high throughput for large datasets; You want parallel processing capabilities; You need a mature, widely-used tool |
| [Addax](/tidb-cloud-lake/tutorials/migrate-from-mysql-with-addax.md) | Full Load, Incremental | Enhanced DataX with better performance | You need better error handling than DataX; You want improved monitoring capabilities; You need more recent updates and features |

## Snowflake to Databend

Migrating from Snowflake to Databend involves a three-step process:

1. **Configuring Snowflake Storage Integration for Amazon S3**: Set up secure access between Snowflake and S3
2. **Preparing & Exporting Data to Amazon S3**: Export your Snowflake data to S3 in Parquet format
3. **Loading Data into Databend**: Import the data from S3 into Databend

### When to Choose Snowflake Migration

| Tool | Capabilities | Best For | Choose When |
|------|------------|----------|-------------|
| [Snowflake Migration](/tidb-cloud-lake/tutorials/migrate-from-snowflake.md) | Full Load | Complete data warehouse transition | You need to migrate your entire Snowflake warehouse; You want to use Parquet format for efficient data transfer; You need to maintain schema compatibility between systems |
