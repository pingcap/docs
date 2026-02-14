---
title: Data Integration Overview
summary: Learn the overview of data integration scenarios.
---

# Data Integration Overview

Data integration means the flow, transfer, and consolidation of data among various data sources. As data grows exponentially in volume and data value is more profoundly explored, data integration has become increasingly popular and urgent. To avoid the situation that TiDB becomes data silos and to integrate data with different platforms, TiCDC offers the capability to replicate TiDB incremental data change logs to other data platforms. This document describes the data integration applications using TiCDC. You can choose an integration solution that suits your business scenarios.

## Integrate with Confluent Cloud and Snowflake

You can use TiCDC to replicate incremental data from TiDB to Confluent Cloud, and replicate the data to Snowflake, ksqlDB, and SQL Server via Confluent Cloud. For details, see [Integrate with Confluent Cloud and Snowflake](/ticdc/integrate-confluent-using-ticdc.md).

## Integrate with Apache Kafka and Apache Flink

You can use TiCDC to replicate incremental data from TiDB to Apache Kafka, and consume the data using Apache Flink. For details, see [Integrate with Apache Kafka and Apache Flink](/replicate-data-to-kafka.md).

## Integrate with Microsoft Fabric

You can use TiCDC to replicate incremental data from TiDB to Microsoft Fabric. With [open mirroring](https://learn.microsoft.com/en-us/fabric/mirroring/open-mirroring), TiCDC writes change data directly to a mirrored database in Fabric. This enables continuous, near real-time data replication from any TiDB deployment to Microsoft Fabric OneLake, making your data readily available for AI and analytics workloads.

For details, see this blog post [How to Replicate TiDB to a Mirrored Database in Microsoft Fabric with TiCDC](https://www.pingcap.com/blog/replicate-tidb-mirrored-database-microsoft-fabric-ticdc/).
