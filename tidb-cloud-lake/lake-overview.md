---
title: TiDB Cloud Lake Overview
summary: TiDB Cloud Lake is a cloud-native data warehouse service for analytics workloads. It separates compute and storage, and supports ANSI SQL, semi-structured data processing, and AI-oriented workflows.
---

# TiDB Cloud Lake Overview

TiDB Cloud Lake is a cloud-native data warehouse service for analytics workloads. It separates compute and storage, allowing you to provision warehouses independently, scale with workload changes, and store data cost-effectively in object storage.

TiDB Cloud Lake supports ANSI SQL, semi-structured data processing, vector search, and AI-oriented workflows in one platform. It is designed for teams that want a managed analytics experience without operating the underlying infrastructure themselves.

> **Warning:**
>
> TiDB Cloud Lake is currently in **public preview**. Feature availability and service limits might change as we continue to improve the product.

## Why {{{ .lake }}}? {#why-lake}

{{{ .lake }}} brings analytics, data engineering, search, and AI workloads together in one cloud-native platform. It combines independently scalable compute, object-storage-based data management, SQL access, and built-in multimodal capabilities in a managed service.

### Scale compute independently from storage

{{{ .lake }}} separates compute from storage. Data is stored in durable, cost-effective object storage, while warehouses provide independently managed compute resources. You can choose a warehouse size for each workload, resize it as demand changes, and use separate warehouses for data loading and query execution. This architecture lets you scale compute without moving or duplicating the underlying data.

For more information, see [TiDB Cloud Lake Architecture](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md) and [Warehouses](/tidb-cloud-lake/guides/warehouse.md).

### Keep costs transparent and predictable

The main cost components are straightforward:

- **Warehouse compute** is billed per second while a warehouse is running. By default, a warehouse automatically suspends after five minutes of inactivity. A suspended warehouse does not consume compute resources.
- **Storage** is billed according to the amount of data stored in object storage.
- **Cloud services** are billed according to API request usage.
- **Service hosting** for data integration services is billed per second while they are running.

Administrators can set a monthly spending limit. You can monitor usage and billing history. For details, see [TiDB Cloud Lake Pricing & Billing](/tidb-cloud-lake/guides/pricing-billing.md) and [Managing Costs](/tidb-cloud-lake/guides/manage-costs.md).

### Run high-performance analytics at scale

{{{ .lake }}} is designed for analytical workloads such as interactive dashboards, ad hoc exploration, large-scale scans, and concurrent queries. Its optimizer uses techniques such as predicate pushdown, join reordering, and scan pruning to reduce unnecessary work.

For workload-specific optimization, you can use cluster keys to organize related data into adjacent storage blocks, materialized views to persist recurring query results, and specialized indexes and result caching to accelerate common access patterns. The appropriate strategy depends on your query filters, data distribution, and update patterns.

For more information, see [Performance Optimization](/tidb-cloud-lake/guides/performance-optimization.md), [Cluster Key](/tidb-cloud-lake/guides/cluster-key-performance.md), and [Materialized View](/tidb-cloud-lake/sql/materialized-view.md).

### Build data pipelines in the platform

{{{ .lake }}} provides built-in primitives for data ingestion and incremental processing:

- [Stages](/tidb-cloud-lake/guides/stage-overview.md) provide managed locations and interfaces for loading, querying, and unloading files.
- [Streams](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md) capture table changes for incremental processing.
- [Tasks](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md) run SQL on a schedule or when a stream contains new rows.
- [Data integration](/tidb-cloud-lake/guides/data-integration-overview.md) provides a visual interface for importing or continuously synchronizing data from supported external systems.

Together, these capabilities support batch ingestion, change data capture (CDC), incremental ETL, scheduled transformations, and downstream analytical tables without requiring every pipeline to rely on separate orchestration tooling.

### Work with structured and semi-structured data

You can use SQL to store, query, clean, and transform relational and semi-structured data in the same platform. The `VARIANT` data type preserves nested **JSON** structures, while JSON path expressions let you access nested fields, virtual columns accelerate frequently queried paths, and inverted indexes support text search.

This is useful for application events, logs, user activity data, API payloads, and AI agent traces, which often have evolving schemas and can be costly to flatten up front.

To protect sensitive data, you can apply row access policies (an experimental feature) to filter rows at query time and masking policies to redact column values, including selected keys in `VARIANT` data. For more information, see [JSON & Search](/tidb-cloud-lake/guides/json-search.md), [Row Access Policy](/tidb-cloud-lake/guides/row-access-policy.md), and [Masking Policy](/tidb-cloud-lake/guides/masking-policy.md).

### Combine analytics, search, and AI workloads

Full-text search, [vector search](/tidb-cloud-lake/guides/vector-search-guide.md), [geospatial analysis](/tidb-cloud-lake/guides/geo-analytics.md), and SQL analytics run on the same data platform. You can use [full-text indexes](/tidb-cloud-lake/guides/full-text-index.md) (inverted indexes) for keyword-oriented retrieval, vector indexes for semantic similarity search, and SQL predicates and joins to combine retrieval results with structured business data.

This unified approach supports use cases such as product and business analytics, application-event analysis, search and recommendations, retrieval-augmented generation (RAG), and AI-agent trace analysis without requiring a separate data copy for each workload. For an end-to-end example, see [Multimodal Data Analytics](/tidb-cloud-lake/guides/multimodal-data-analytics.md).

## Get Started

1. [**Quick Start**](/tidb-cloud-lake/lake-quick-start.md): Create your account and run your first workflow.
2. [**Connect to TiDB Cloud Lake**](/tidb-cloud-lake/guides/connection-overview.md): Choose the right client or driver for your workflow.
3. [**Learn the architecture**](/tidb-cloud-lake/guides/tidb-cloud-lake-architecture.md): Understand the metadata, compute, and storage layers.
4. [**Explore product features**](/tidb-cloud-lake/guides/vector-search-guide.md): Start with analytics, vector, search, and geo capabilities.
