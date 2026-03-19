---
title: Editions
summary: Databend Cloud comes in three editions Personal, Business, and Dedicated, that you can choose from to serve a wide range of needs and ensure optimal performance for different use cases.
---

# Editions

Databend Cloud comes in three editions: **Personal**, **Business**, and **Dedicated**, that you can choose from to serve a wide range of needs and ensure optimal performance for different use cases.

For the pricing information, see [Pricing & Billing](/tidb-cloud-lake/guides/pricing-billing.md). For the detailed feature list among these editions, see [Feature Lists](#feature-lists).

## Feature Lists

The following are feature lists of Databend Cloud among editions:

### Release Management

| Features | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| Early access to weekly new releases, which can be used for additional testing/validation before each release is deployed to your production accounts. | | ✓ | ✓ |

### Security & Governance

| Features | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| SOC 2 Type II certification. | ✓ | ✓ | ✓ |
| GDPR | ✓ | ✓ | ✓ |
| Automatic encryption of all data. | ✓ | ✓ | ✓ |
| Object-level access control. | ✓ | ✓ | ✓ |
| Standard Time Travel (up to 1 day) for accessing/restoring modified and deleted data. | ✓ | ✓ | ✓ |
| Disaster recovery of modified/deleted data (for 7 days beyond Time Travel) through Fail-safe. | ✓ | ✓ | ✓ |
| **Extended Time Travel**. | | 90 days | 90 days |
| Column-level Security to apply masking policies to columns in tables or views. | ✓ | ✓ | ✓ |
| Audit the user access history through the Account Usage ACCESS_HISTORY view. | ✓ | ✓ | ✓ |
| **Support for private connectivity to the Databend Cloud service using AWS PrivateLink**. | | ✓ | ✓ |
| **Dedicated metadata store and pool of compute resources (used in virtual warehouses)**. | | | ✓ |

### Compute Resource

| Features | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| Virtual warehouses, separate compute clusters for isolating query and data loading workloads. | ✓ | ✓ | ✓ |
| Multi-cluster scaling | | ✓ | ✓ |
| Resource monitors for monitoring virtual warehouse credit usage. | ✓ | ✓ | ✓ |

### SQL Support

| Features | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| Standard SQL, including most DDL and DML defined in SQL:1999. | ✓ | ✓ | ✓ |
| Advanced DML such as multi-table INSERT, MERGE, and multi-merge. | ✓ | ✓ | ✓ |
| Broad support for standard data types. | ✓ | ✓ | ✓ |
| Native support for semi-structured data (JSON, ORC, Parquet). | ✓ | ✓ | ✓ |
| Native support for geospatial data. | ✓ | ✓ | ✓ |
| Native support for unstructured data. | ✓ | ✓ | ✓ |
| Collation rules for string/text data in table columns. | ✓ | ✓ | ✓ |
| Multi-statement transactions. | ✓ | ✓ | ✓ |
| User-defined functions (UDFs) with support for JavaScript, Python, and WebAssembly. | | ✓ | ✓ |
| External functions for extending Databend Cloud to other development platforms. | ✓ | ✓ | ✓ |
| Amazon API Gateway private endpoints for external functions. | ✓ | ✓ | ✓ |
| External tables for referencing data in a cloud storage data lake. | ✓ | ✓ | ✓ |
| Support for clustering data in very large tables to improve query performance, with automatic maintenance of clustering. | ✓ | ✓ | ✓ |
| Search optimization for point lookup queries, with automatic maintenance. | ✓ | ✓ | ✓ |
| Materialized views, with automatic maintenance of results. | ✓ | ✓ | ✓ |
| Iceberg tables for referencing data in a cloud storage data lake. | ✓ | ✓ | ✓ |
| Schema detection for automatically detecting the schema in a set of staged semi-structured data files and retrieving the column definitions. | ✓ | ✓ | ✓ |
| Schema evolution for automatically evolving tables to support the structure of new data received from the data sources. | ✓ | ✓ | ✓ |
| Support for <a href="/sql/sql-commands/ddl/table/ddl-create-table-external-location" target="_self">creating table with external location</a>. | ✓ | ✓ | ✓ |
| Supports for <a href="/sql/sql-commands/ddl/table/attach-table" target="_self">ATTACH TABLE</a>. | ✓ | ✓ | ✓ |

### Interfaces & Tools

| Features | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| The next-generation SQL worksheet for advanced query development, data analysis, and visualization. | ✓ | ✓ | ✓ |
| BendSQL, a command line client for building/testing queries, loading/unloading bulk data, and automating DDL operations. | ✓ | ✓ | ✓ |
| Programmatic interfaces for Rust, Python, Java, Node.js, .js, PHP, and Go. | ✓ | ✓ | ✓ |
| Native support for JDBC. | ✓ | ✓ | ✓ |
| Extensive ecosystem for connecting to ETL, BI, and other third-party vendors and technologies. | ✓ | ✓ | ✓ |

### Data Import & Export

| Features | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| Bulk loading from delimited flat files (CSV, TSV, etc.) and semi-structured data files (JSON, ORC, Parquet). | ✓ | ✓ | ✓ |
| Bulk unloading to delimited flat files and JSON files. | ✓ | ✓ | ✓ |
| Continuous micro-batch loading. | ✓ | ✓ | ✓ |
| Streaming for low-latency loading of streaming data. | ✓ | ✓ | ✓ |
| Databend Cloud Connector for Kafka for loading data from Apache Kafka topics. | ✓ | ✓ | ✓ |

### Data Pipelines

| Features | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| Streams for tracking table changes. | ✓ | ✓ | ✓ |
| Tasks for scheduling the execution of SQL statements, often in conjunction with table streams. | ✓ | ✓ | ✓ |

### Customer Support

| Features | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| Logging and tracking support tickets. | ✓ | ✓ | ✓ |
| 4/7 coverage and 1-hour response window for Severity 1 issues. | ✓ | ✓ | ✓ |
| **Response to non-severity-1 issues in hours**. | 8h | 4h | 1h |
