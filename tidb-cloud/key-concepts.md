---
title: 关键概念概览
summary: 了解 TiDB Cloud 的关键概念。
---

# 关键概念概览

本文档概述了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 的关键概念。理解这些概念有助于你更好地使用 TiDB Cloud 的功能和能力。

## 架构

TiDB Cloud 基于云原生分布式架构构建，实现了计算与存储分离，支持弹性扩展和高可用性。[了解更多 TiDB Cloud 架构相关内容](/tidb-cloud/architecture-concepts.md)。

## 数据库模式

TiDB Cloud 允许你通过数据库、数据表、列、索引和约束等对象来组织和结构化你的数据。同时还支持临时表、向量索引和缓存表等高级特性。[了解更多数据库模式相关内容](/tidb-cloud/database-schema-concepts.md)。

## 事务

TiDB 提供完整的分布式事务，并在 [Google Percolator](https://research.google.com/pubs/pub36726.html) 的基础上进行了部分优化。[了解更多事务相关内容](/tidb-cloud/transaction-concepts.md)。

## SQL

TiDB 高度兼容 MySQL 协议，以及 MySQL 5.7 和 MySQL 8.0 的常用特性和语法。[了解更多 TiDB Cloud 中的 SQL 相关内容](/tidb-cloud/sql-concepts.md)。

## AI 特性

TiDB Cloud 的 AI 特性使你能够充分利用先进技术进行数据探索、检索和集成。[了解更多 AI 特性相关内容](/tidb-cloud/ai-feature-concepts.md)。

## 数据服务（Beta）

数据服务允许你通过自定义 API 端点，以 HTTPS 请求方式访问 TiDB Cloud 数据。[了解更多数据服务相关内容](/tidb-cloud/data-service-concepts.md)。

## 可扩展性

TiDB Cloud Dedicated 允许你分别调整计算和存储资源，以适应数据量或工作负载的变化。[了解更多可扩展性相关内容](/tidb-cloud/scalability-concepts.md)。

## 高可用性

TiDB Cloud 在 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 集群中都能确保高可用性：

- [TiDB Cloud Serverless 的高可用性](/tidb-cloud/serverless-high-availability.md)
- [TiDB Cloud Dedicated 的高可用性](/tidb-cloud/high-availability-with-multi-az.md)

## 监控

TiDB Cloud 提供了全面的集群性能和健康状况监控能力。[了解更多监控相关内容](/tidb-cloud/monitoring-concepts.md)。

## 数据流

TiDB Cloud 允许你将 TiDB 集群中的数据变更流式传输到其他系统，如 Kafka、MySQL 和对象存储。[了解更多数据流相关内容](/tidb-cloud/data-streaming-concepts.md)。

## 备份与恢复

TiDB Cloud 提供自动化备份方案和时间点恢复（PITR）能力。[了解更多备份与恢复相关内容](/tidb-cloud/backup-and-restore-concepts.md)。

## 安全

TiDB Cloud 提供强大且灵活的安全框架，旨在保护数据、实施访问控制，并满足现代合规标准。[了解更多安全相关内容](/tidb-cloud/security-concepts.md)。