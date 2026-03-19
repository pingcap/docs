---
title: DDL (Data Definition Language) Commands
summary: These topics provide reference information for the DDL (Data Definition Language) commands in Databend.
---

# DDL (Data Definition Language) Commands

These topics provide reference information for the DDL (Data Definition Language) commands in Databend.

## Database & Table Management

| Component | Description |
|-----------|-------------|
| **[Database](/tidb-cloud-lake/sql/ddl-database-overview.md)** | Create, alter, and drop databases |
| **[Table](/tidb-cloud-lake/sql/ddl-table-overview.md)** | Create, alter, and manage tables |
| **[View](/tidb-cloud-lake/sql/ddl-view-overview.md)** | Create and manage virtual tables based on queries |

## Performance & Indexing

| Component | Description |
|-----------|-------------|
| **[Cluster Key](/tidb-cloud-lake/sql/cluster-key.md)** | Define data clustering for query optimization |
| **[Aggregating Index](/tidb-cloud-lake/sql/aggregating-index-sql.md)** | Pre-compute aggregations for faster queries |
| **[Inverted Index](/tidb-cloud-lake/sql/inverted-index.md)** | Full-text search index for text columns |
| **[Ngram Index](/tidb-cloud-lake/sql/ngram-index-sql.md)** | Substring search index for LIKE patterns |
| **[Virtual Column](/tidb-cloud-lake/sql/virtual-column-overview.md)** | Extract and index JSON fields as virtual columns |

## Security & Access Control

| Component | Description |
|-----------|-------------|
| **[User](/tidb-cloud-lake/sql/user-role.md)** | Create and manage database users |
| **[Network Policy](/tidb-cloud-lake/sql/network-policy-sql.md)** | Control network access to databases |
| **[Mask Policy](/tidb-cloud-lake/sql/masking-policy-sql.md)** | Apply data masking for sensitive information |
| **[Password Policy](/tidb-cloud-lake/sql/password-policy-sql.md)** | Enforce password requirements and rotation |

## Data Integration & Processing

| Component | Description |
|-----------|-------------|
| **[Stage](/tidb-cloud-lake/sql/stage.md)** | Define storage locations for data loading |
| **[Stream](/tidb-cloud-lake/sql/stream.md)** | Capture and process data changes |
| **[Task](/tidb-cloud-lake/sql/task.md)** | Schedule and automate SQL operations |
| **[Sequence](/tidb-cloud-lake/sql/sequence.md)** | Generate unique sequential numbers |
| **[Connection](/tidb-cloud-lake/sql/connection.md)** | Configure external data source connections |
| **[File Format](/tidb-cloud-lake/sql/file-format.md)** | Define formats for data import/export |

## Functions & Procedures

| Component | Description |
|-----------|-------------|
| **[UDF](/tidb-cloud-lake/sql/user-defined-function.md)** | Create custom functions in Python or JavaScript |
| **[External Function](/tidb-cloud-lake/sql/external-function.md)** | Integrate external APIs as SQL functions |
| **[Procedure](/tidb-cloud-lake/sql/stored-procedure.md)** | Create stored procedures for complex logic |
| **[Notification](/tidb-cloud-lake/sql/notification.md)** | Set up event notifications and webhooks |

## Resource Management

| Component | Description |
|-----------|-------------|
| **[Warehouse](/tidb-cloud-lake/sql/warehouse-overview.md)** | Manage compute resources for query execution |
| **[Workload Group](/tidb-cloud-lake/sql/workload-group.md)** | Control resource allocation and priorities |
| **[Transaction](/tidb-cloud-lake/sql/transaction.md)** | Manage database transactions |
| **[Variable](/tidb-cloud-lake/sql/sql-variables.md)** | Set and use session/global variables |
