---
title: TiDB Performance Tools Guidelines
summary: learn how to use performance tools in TiDB for efficiently performance troubleshooting 
---

# TiDB Performance Tools Guidelines

## Introduction

TiDB is a distributed database that needs systematic performance troubleshooting. While it has advanced features, it follows basic database principles that we can analyze step by step.

## Performance Troubleshooting Challenges

Performance issues in TiDB can stem from various sources:

- Application Layer Issues: Suboptimal connection management and improper batch processing
- Query Optimization Issues: Suboptimal execution plans and lack of appropriate indexes
- Resource Constraints: Undersized TiDB or TiKV servers
- Distributed System Challenges: Read or write Hot spot issues in TiKV

Each type of performance issue requires specific diagnostic approaches:

- Application issues: Application related metrics analysis
- Query issues: Execution plan analysis and index optimization
- Resource issues: Server metrics and capacity planning
- Distributed issues: Key Visualizer and hot spot analysis

Understanding which tools to use in each scenario is crucial for effective problem resolution.

## Common Challenges for New Users

Performance troubleshooting in distributed databases like TiDB presents unique challenges:

- **Tool Complexity**: The diverse set of diagnostic tools requires familiarity with multiple interfaces and approaches
- **Metric Volume**: Processing and correlating over 1000 metrics can be overwhelming
- **Complex Execution Plans**: Understanding query execution across distributed components requires specialized knowledge
- **Metric Correlation**: Identifying relationships between different performance indicators can be challenging

## Document Purpose

TiDB combines advanced distributed features with core database principles. This guide shows you how to systematically troubleshoot performance issues using proven methods. There are plenty resource available under the TiDB Performance [Tuning guide](/performance-tuning-overview.md), 

Here are two effective ways to analyze TiDB performance:

- Database Time Analysis: Using view [cluster_statements_summary view](/statement-summary-tables.md##the-cluster-tables-for-statement-summary) and performance metrics, this method helps pinpoint bottlenecks throughout your TiDB cluster and track down performance issues from high-level symptoms to root causes.
- Database CPU Analysis: This approach focuses on analyzing top CPU utilization patterns through [Top SQL feature](/dashboard/top-sql.md), helping you understand resource-intensive top SQL statements. It's particularly effective for identifying read or write hotspots at the TiKV level.


## Database Time Analysis

TiDB is constantly measuring and collecting SQL processing paths and database time. Therefore, it is easy to identify database performance bottlenecks in TiDB. Based on database time metrics and system views, you can achieve the following goals: 

- Walkthrough [TiDB Performance Tuning Overview](/performance-tuning-overview.md) to understand the basic concepts of performance tuning, especially about the user response time vs database time
- Determine whether the bottleneck is in TiDB by comparing the average SQL processing latency with the idle time of a TiDB connection in a transaction.
- If the bottleneck is in TiDB, you can identifying high-load sql and the bottleneck module of the TiDB cluster
    - The most efficient way to identify Resource-Intensive SQL is using `SQL Statements` panel in [`TiDB Dashboard`](/dashboard/dashboard-overview.md#show-a-list-of-execution-information-of-all-sql-statements). You can also use [TiDB SQL Tuning Best Practice for Beginners] to do sql tuning.
    - The most efficient way to leverage metrics, is to use [Performance Overview dashboard](/grafana-performance-overview-dashboard.md) and following database time based methods, [Performance Analysis and Tuning](/performance-tuning-methods.md), you can identify the exact module in the distributed system based on database time overview, color-based performance data, key metrics, resource utilization, and top-down latency breakdowns. [Performance Tuning Practices for OLTP Scenarios](/performance-tuning-practices.md) show real-world usage of these methods with CPU and heap profiles for TiDB. Besides the [Performance Overview dashboard](/grafana-performance-overview-dashboard.md), you can also use other grafana dashboards, [TiDB](/grafana-tidb-dashboard.md), [TiKV](/grafana-tikv-dashboard.md), [PD](/grafana-pd-dashboard.md) to identify the exact module in the distributed system.

## Database CPU Analysis

The database cpu analysis helps you identify top SQL statements that consume the most CPU in the TiDB or TiKV nodes. It's particularly effective for identifying read or write hotspots at the TiKV level. To apply this method, you can use the [Top SQL feature](/dashboard/top-sql.md) in TiDB Dashboard. 