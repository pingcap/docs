---
title: Performance Optimization
summary: Databend primarily accelerates query performance through various indexing technologies, including data clustering, result caching, and specialized indexes, helping you significantly improve query response times.
---
Databend primarily accelerates query performance through **various indexing technologies**, including data clustering, result caching, and specialized indexes, helping you significantly improve query response times.

## Optimization Features

| Feature | Purpose | When to Use |
|---------|---------|------------|
| [**Cluster Key**](/tidb-cloud-lake/sql/cluster-key.md) | Automatically organize data physically for optimal query performance | When you have large tables with frequent filtering on specific columns, especially time-series or categorical data |
| [**Query Result Cache**](/tidb-cloud-lake/guides/query-result-cache.md) | Automatically store and reuse results of identical queries | When your applications run the same analytical queries repeatedly, such as in dashboards or scheduled reports |
| [**Virtual Column**](/tidb-cloud-lake/guides/virtual-column.md) | Automatically accelerate access to fields within JSON/VARIANT data | When you frequently query specific paths within semi-structured data and need sub-second response times |
| [**Aggregating Index**](/tidb-cloud-lake/guides/aggregating-index.md) | Precompute and store common aggregation results | When your analytical workloads frequently run SUM, COUNT, AVG queries on large datasets |
| [**Full-Text Index**](/tidb-cloud-lake/guides/full-text-index.md) | Enable lightning-fast semantic text search capabilities | When you need advanced text search functionality like relevance scoring and fuzzy matching |
| [**Ngram Index**](/tidb-cloud-lake/guides/ngram-index.md) | Accelerate pattern matching with wildcards | When your queries use LIKE operators with wildcards (especially '%keyword%') on large text columns |

## Feature Availability

| Feature | Community | Enterprise | Cloud |
|---------|-----------|------------|-------|
| Cluster Key | ✅ | ✅ | ✅ |
| Query Result Cache | ✅ | ✅ | ✅ |
| Virtual Column | ❌ | ✅ | ✅ |
| Aggregating Index | ✅ | ✅ | ✅ |
| Full-Text Index | ✅ | ✅ | ✅ |
| Ngram Index | ✅ | ✅ | ✅ |
