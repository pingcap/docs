---
title: Query Syntax
summary: This page provides reference information for the query syntax in Databend. Each component can be used individually or combined to build powerful queries.
---

# Query Syntax

This page provides reference information for the query syntax in Databend. Each component can be used individually or combined to build powerful queries.

## Core Query Components

| Component | Description |
|-----------|-------------|
| **[SELECT](/tidb-cloud-lake/sql/select.md)** | Retrieve data from tables - the foundation of all queries |
| **[FROM / JOIN](/tidb-cloud-lake/sql/join.md)** | Specify data sources and combine multiple tables |
| **[WHERE](/tidb-cloud-lake/sql/select.md#where-clause)** | Filter rows based on conditions |
| **[GROUP BY](/tidb-cloud-lake/sql/group-by.md)** | Group rows and perform aggregations (SUM, COUNT, AVG, etc.) |
| **[HAVING](/tidb-cloud-lake/sql/group-by.md)** | Filter grouped results |
| **[ORDER BY](/tidb-cloud-lake/sql/select.md#order-by-clause)** | Sort query results |
| **[LIMIT / TOP](/tidb-cloud-lake/sql/top.md)** | Restrict the number of rows returned |

## Advanced Features

| Component | Description |
|-----------|-------------|
| **[WITH (CTE)](/tidb-cloud-lake/sql/clause.md)** | Define reusable query blocks for complex logic |
| **[PIVOT](/tidb-cloud-lake/sql/pivot.md)** | Convert rows to columns (wide format) |
| **[UNPIVOT](/tidb-cloud-lake/sql/unpivot.md)** | Convert columns to rows (long format) |
| **[QUALIFY](/tidb-cloud-lake/sql/qualify.md)** | Filter rows after window function calculations |
| **[VALUES](/tidb-cloud-lake/sql/values.md)** | Create inline temporary data sets |

## Time Travel & Streaming

| Component | Description |
|-----------|-------------|
| **[AT](/tidb-cloud-lake/sql/at.md)** | Query data at a specific point in time |
| **[CHANGES](/tidb-cloud-lake/sql/changes.md)** | Track insertions, updates, and deletions |
| **[WITH CONSUME](/tidb-cloud-lake/sql/with-consume.md)** | Process streaming data with offset management |
| **[WITH STREAM HINTS](/tidb-cloud-lake/sql/stream-hints.md)** | Optimize stream processing behavior |

## Query Execution

| Component | Description |
|-----------|-------------|
| **[Settings](/tidb-cloud-lake/sql/settings-clause.md)** | Configure query optimization and execution parameters |

## Query Structure

A typical Databend query follows this structure:

```sql
[WITH cte_expressions]
SELECT [TOP n] columns
FROM table
[JOIN other_tables]
[WHERE conditions]
[GROUP BY columns]
[HAVING group_conditions]
[QUALIFY window_conditions]
[ORDER BY columns]
[LIMIT n]
```
