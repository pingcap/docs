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

TiDB combines advanced distributed features with core database principles. This guide shows you how to systematically troubleshoot performance issues using proven methods.

Here are two effective ways to analyze TiDB performance:

- Database Time Analysis: Database Time Analysis uses statement summaries and metrics to provide multiple views of performance, helping you identify bottlenecks both inside and outside TiDB, and systematically trace issues from symptoms to root causes.
- Database CPU Analysis: This approach focuses on analyzing top CPU utilization patterns through Top SQL features, helping you understand resource-intensive top SQL statements. It's particularly effective for identifying read or write hotspots at the TiKV level.


## Database Time Analysis


## Database CPU Analysis