---
title: Query Syntax
---

This page provides reference information for the query syntax in Databend. Each component can be used individually or combined to build powerful queries.

## Core Query Components

| Component | Description |
|-----------|-------------|
| **[SELECT](query-syntax/query-select)** | Retrieve data from tables - the foundation of all queries |
| **[FROM / JOIN](query-syntax/query-join)** | Specify data sources and combine multiple tables |
| **[WHERE](query-syntax/query-select#where-clause)** | Filter rows based on conditions |
| **[GROUP BY](query-syntax/query-group-by)** | Group rows and perform aggregations (SUM, COUNT, AVG, etc.) |
| **[HAVING](query-syntax/query-group-by#having-clause)** | Filter grouped results |
| **[ORDER BY](query-syntax/query-select#order-by-clause)** | Sort query results |
| **[LIMIT / TOP](query-syntax/top)** | Restrict the number of rows returned |

## Advanced Features

| Component | Description |
|-----------|-------------|
| **[WITH (CTE)](query-syntax/with-clause)** | Define reusable query blocks for complex logic |
| **[PIVOT](query-syntax/query-pivot)** | Convert rows to columns (wide format) |
| **[UNPIVOT](query-syntax/query-unpivot)** | Convert columns to rows (long format) |
| **[QUALIFY](query-syntax/qualify)** | Filter rows after window function calculations |
| **[VALUES](query-syntax/values)** | Create inline temporary data sets |

## Time Travel & Streaming

| Component | Description |
|-----------|-------------|
| **[AT](query-syntax/query-at)** | Query data at a specific point in time |
| **[CHANGES](query-syntax/changes)** | Track insertions, updates, and deletions |
| **[WITH CONSUME](query-syntax/with-consume)** | Process streaming data with offset management |
| **[WITH STREAM HINTS](query-syntax/with-stream-hints)** | Optimize stream processing behavior |

## Query Execution

| Component | Description |
|-----------|-------------|
| **[Settings](query-syntax/settings)** | Configure query optimization and execution parameters |

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