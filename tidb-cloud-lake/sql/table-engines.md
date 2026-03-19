---
title: Table Engines
summary: Databend provides several table engines so that you can balance performance and interoperability needs without moving data. Each engine is optimized for a specific scenario—ranging from Databend’s native Fuse storage to external data lake formats.
---

# Table Engines

Databend provides several table engines so that you can balance performance and interoperability needs without moving data. Each engine is optimized for a specific scenario—ranging from Databend’s native Fuse storage to external data lake formats.

## Available Engines

| Engine | Best For | Highlights |
| ------ | -------- | ---------- |
| [Fuse Engine Tables](/tidb-cloud-lake/sql/fuse-engine-tables.md) | Native Databend tables | Snapshot-based storage, automatic clustering, change tracking |
| [Apache Iceberg™ Tables](/tidb-cloud-lake/sql/apache-icebergtm-tables.md) | Lakehouse catalogs | Time-travel, schema evolution, REST/Hive/Storage catalogs |
| [Apache Hive Tables](/tidb-cloud-lake/sql/apache-hive-tables.md) | Hive metastore data | Query Hive-managed data stores through external tables |
| [Delta Lake Engine](/tidb-cloud-lake/sql/delta-lake-engine.md) | Delta Lake datasets | Read Delta tables in object storage with ACID guarantees |

## Choosing an Engine

- Use **Fuse** when you manage data directly inside Databend and want the best storage and query performance.
- Choose **Iceberg** when you already manage datasets through Iceberg catalogs and need tight lakehouse integration.
- Configure **Hive** when you rely on an existing Hive Metastore but want Databend’s query engine.
- Select **Delta** to analyse Delta Lake tables in place without ingesting them into Fuse.
