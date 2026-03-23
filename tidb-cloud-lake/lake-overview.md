---
title: TiDB Cloud Lake Overview
summary: TiDB Cloud Lake is a cloud-native data warehouse service for analytics workloads. It separates compute from storage and supports ANSI SQL, semi-structured data processing, and AI-oriented workflows.
---

# TiDB Cloud Lake Overview

TiDB Cloud Lake is a cloud-native data warehouse service for analytics workloads. It separates compute from storage so you can provision warehouses independently, scale with workload changes, and store data cost-effectively in object storage.

TiDB Cloud Lake supports ANSI SQL, semi-structured data processing, vector search, and AI-oriented workflows in one platform. It is designed for teams that want a managed analytics experience without operating the underlying infrastructure themselves.

> **Private beta:** TiDB Cloud Lake is currently in private beta. Feature availability and service limits might change as we continue to improve the product.


## Why {{{ .lake }}}?

{{{ .lake }}} brings analytics, vector, search, and geo workloads together in one cloud-native platform. With storage-compute separation, ANSI SQL support, and managed infrastructure, teams can work on multi-modal data with better flexibility, performance, and cost efficiency.

| Feature | Description | Learn more |
|---|---|---|
| **Unified Engine** | Analytics, vector, search, and geo share one optimizer and runtime. | [TiDB Cloud Lake Architecture](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md) |
| **Unified Data** | Structured, semi-structured, unstructured, and vector data share object storage. | [TiDB Cloud Lake Architecture](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md) |
| **Analytics Native** | ANSI SQL, windowing, incremental aggregates, and streaming power BI run on the same platform. | [Worksheets](/tidb-cloud-lake/guides/worksheet.md) |
| **Vector Native** | Embeddings, vector indexes, and semantic retrieval all run in SQL. | [Vector Search](/tidb-cloud-lake/guides/vector-search-guide.md) |
| **Search Native** | Full-text search and inverted indexes power hybrid retrieval. | [Full-Text Index](/tidb-cloud-lake/guides/full-text-index.md) |
| **Geo Native** | Geospatial indexes and functions power map and location services. | [Geo Analytics](/tidb-cloud-lake/guides/geo-analytics.md) |



## Get Started

1. [**Quick Start**](/tidb-cloud-lake/lake-quick-start.md) - Create your account and run your first workflow.
2. [**Connect to TiDB Cloud Lake**](/tidb-cloud-lake/guides/connection-overview.md) - Choose the right client or driver for your workflow.
3. [**Learn the architecture**](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md) - Understand the metadata, compute, and storage layers.
4. [**Explore product features**](/tidb-cloud-lake/guides/vector-search-guide.md) - Start with analytics, vector, search, and geo capabilities.
