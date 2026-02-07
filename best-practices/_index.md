---
title: TiDB Best Practices
summary: Learn the best practices for deploying, configuring, and using TiDB effectively.
---

# TiDB Best Practices

By following best practices for deploying, configuring, and using TiDB, you can optimize the performance, reliability, and scalability of your TiDB deployments. This document provides an overview of the best practices for using TiDB.

## Overview

Get started with basic principles and general recommendations for using TiDB effectively.

| Best practice topic | Description |
| ------------------- | ----------- |
| [Use TiDB](/best-practices/tidb-best-practices.md) | A comprehensive overview of best practices for using TiDB. |

## Schema design

Learn best practices for designing schemas in TiDB, including managing DDL operations, choosing primary keys, and designing and maintaining indexes to balance performance, scalability, and maintainability.

| Best practice topic | Description |
| ------------------- | ----------- |
| [Manage DDL](/best-practices/ddl-introduction.md) | Best practices for managing Data Definition Language (DDL) operations in TiDB. |
| [Use UUIDs as Primary Keys](/best-practices/uuid.md) | Best practices for storing and indexing UUIDs (Universally Unique Identifiers) efficiently when using UUIDs as primary keys. |
| [Optimize Multi-Column Indexes](/best-practices/multi-column-index-best-practices.md) | Best practices for designing and using multi-column indexes in TiDB to improve query performance. |
| [Manage Indexes and Identify Unused Indexes](/best-practices/index-management-best-practices.md) | Best practices for managing and optimizing indexes, identifying and removing unused indexes in TiDB to optimize performance. |

## Deployment

Explore recommended deployment patterns for different scenarios, such as deployment on public cloud and multi-data center setups, to ensure high availability and efficient resource usage.

| Best practice topic | Description |
| ------------------- | ----------- |
| [Deploy TiDB on Public Cloud](/best-practices/best-practices-on-public-cloud.md) | Best practices for deploying TiDB on public cloud to maximize performance, cost efficiency, reliability, and scalability of your TiDB deployment. |
| [Three-Node Hybrid Deployment](/best-practices/three-nodes-hybrid-deployment.md) | Best practices for a cost-effective, hybrid three-node deployment while maintaining stability. |
| [Local Reads in Three-Data-Center Deployments](/best-practices/three-dc-local-read.md) | Best practices for reducing cross-center latency by using Stale Read. |

## Operations

Find operational best practices for running TiDB in production, such as traffic routing, load balancing, and monitoring, to ensure system stability and observability.

| Best practice topic | Description |
| ------------------- | ----------- |
| [Use HAProxy for Load Balancing](/best-practices/haproxy-best-practices.md) | Best practices for configuring HAProxy to distribute application traffic across multiple TiDB nodes. |
| [Use Read-Only Storage Nodes](/best-practices/readonly-nodes.md) | Best practices for using read-only nodes to isolate analytical or heavy read workloads from OLTP traffic. |
| [Monitor TiDB Using Grafana](/best-practices/grafana-monitor-best-practices.md) | Best practices for using key metrics and dashboard configurations for proactive troubleshooting. |

## Performance tuning

Understand how to tune TiDB components such as TiKV and PD, and how to use features like read-only storage nodes to improve performance under different workloads.

| Best practice topic | Description |
| ------------------- | ----------- |
| [Handle Millions of Tables in SaaS Multi-Tenant Scenarios](/best-practices/saas-best-practices.md) | Best practices for using TiDB in SaaS (Software as a Service) multi-tenant environments, especially in scenarios where the number of tables in a single cluster exceeds one million. |
| [Handle High-Concurrency Writes](/best-practices/high-concurrency-best-practices.md) | Best practices for handling high-concurrency write-heavy workloads in TiDB to avoid write hotspots and optimize performance. |
| [Tune TiKV Performance with Massive Regions](/best-practices/massive-regions-best-practices.md) | Best practices for optimizing TiKV performance and reducing heartbeat overhead when managing millions of Regions. |
| [Tune PD Scheduling](/best-practices/pd-scheduling-best-practices.md) | Best practices for adjusting PD policies to balance load and speed up failure recovery. |
