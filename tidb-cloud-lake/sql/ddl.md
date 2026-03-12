---
title: DDL (Data Definition Language) Commands
---

These topics provide reference information for the DDL (Data Definition Language) commands in Databend.

## Database & Table Management

| Component | Description |
|-----------|-------------|
| **[Database](00-database/index.md)** | Create, alter, and drop databases |
| **[Table](01-table/index.md)** | Create, alter, and manage tables |
| **[View](05-view/index.md)** | Create and manage virtual tables based on queries |

## Performance & Indexing

| Component | Description |
|-----------|-------------|
| **[Cluster Key](06-clusterkey/index.md)** | Define data clustering for query optimization |
| **[Aggregating Index](07-aggregating-index/index.md)** | Pre-compute aggregations for faster queries |
| **[Inverted Index](07-inverted-index/index.md)** | Full-text search index for text columns |
| **[Ngram Index](07-ngram-index/index.md)** | Substring search index for LIKE patterns |
| **[Virtual Column](07-virtual-column/index.md)** | Extract and index JSON fields as virtual columns |

## Security & Access Control

| Component | Description |
|-----------|-------------|
| **[User](02-user/index.md)** | Create and manage database users |
| **[Network Policy](12-network-policy/index.md)** | Control network access to databases |
| **[Mask Policy](12-mask-policy/index.md)** | Apply data masking for sensitive information |
| **[Password Policy](12-password-policy/index.md)** | Enforce password requirements and rotation |

## Data Integration & Processing

| Component | Description |
|-----------|-------------|
| **[Stage](03-stage/index.md)** | Define storage locations for data loading |
| **[Stream](04-stream/index.md)** | Capture and process data changes |
| **[Task](04-task/index.md)** | Schedule and automate SQL operations |
| **[Sequence](04-sequence/index.md)** | Generate unique sequential numbers |
| **[Connection](13-connection/index.md)** | Configure external data source connections |
| **[File Format](13-file-format/index.md)** | Define formats for data import/export |

## Functions & Procedures

| Component | Description |
|-----------|-------------|
| **[UDF](10-udf/index.md)** | Create custom functions in Python or JavaScript |
| **[External Function](11-external-function/index.md)** | Integrate external APIs as SQL functions |
| **[Procedure](18-procedure/index.md)** | Create stored procedures for complex logic |
| **[Notification](16-notification/index.md)** | Set up event notifications and webhooks |

## Resource Management

| Component | Description |
|-----------|-------------|
| **[Warehouse](19-warehouse/index.md)** | Manage compute resources for query execution |
| **[Workload Group](20-workload-group/index.md)** | Control resource allocation and priorities |
| **[Transaction](14-transaction/index.md)** | Manage database transactions |
| **[Variable](15-variable/index.md)** | Set and use session/global variables |
