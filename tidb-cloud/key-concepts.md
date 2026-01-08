---
title: 关键概念概览
summary: 了解 TiDB Cloud 中的关键概念。
---

# 关键概念概览

本文档概述了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 中的关键概念。理解这些概念有助于你更好地使用 TiDB Cloud 的功能和能力。

## 架构

TiDB Cloud 基于云原生分布式架构构建，实现了计算与存储分离，支持弹性扩展和高可用。[了解更多 TiDB Cloud 架构](/tidb-cloud/architecture-concepts.md)。

## 数据库 schema

TiDB Cloud 允许你通过数据库、表、列、索引和约束等对象来组织和结构化你的数据。同时还支持临时表、向量索引、缓存表等高级功能。[了解更多数据库 schema](/tidb-cloud/database-schema-concepts.md)。

## 事务

TiDB 提供完整的分布式事务，并在 [Google Percolator](https://research.google.com/pubs/pub36726.html) 的基础上进行了部分优化。[了解更多事务相关内容](/tidb-cloud/transaction-concepts.md)。

## SQL

TiDB 高度兼容 MySQL 协议，以及 MySQL 5.7 和 MySQL 8.0 的常用功能和语法。[了解更多 TiDB Cloud 中的 SQL](/tidb-cloud/sql-concepts.md)。

## AI 功能

TiDB Cloud 的 AI 功能使你能够充分利用先进技术进行数据探索、搜索和集成。[了解更多 AI 功能](/tidb-cloud/ai-feature-concepts.md)。

## Data Service（Beta）

Data Service 允许你通过自定义 API 端点，使用 HTTPS request 访问 TiDB Cloud 数据。[了解更多 Data Service](/tidb-cloud/data-service-concepts.md)。

## 扩展性

TiDB Cloud Dedicated 支持你分别调整计算和存储资源，以适应数据量或负载的变化。[了解更多扩展性](/tidb-cloud/scalability-concepts.md)。

## 高可用

TiDB Cloud 在所有支持的方案中都保证高可用：

- 对于 <CustomContent plan="starter,essential">TiDB Cloud Starter 和 TiDB Cloud Essential</CustomContent> <CustomContent plan="premium">TiDB Cloud Starter、TiDB Cloud Essential 和 TiDB Cloud Premium</CustomContent>，参见 [TiDB Cloud 的高可用](/tidb-cloud/serverless-high-availability.md)。
- 对于 TiDB Cloud Dedicated，参见 [TiDB Cloud Dedicated 的高可用](/tidb-cloud/high-availability-with-multi-az.md)。

## 监控

TiDB Cloud 提供全面的集群性能与健康监控能力。[了解更多监控相关内容](/tidb-cloud/monitoring-concepts.md)。

## 数据流

TiDB Cloud 支持将 TiDB 集群中的数据变更流式传输到其他系统，如 Kafka、MySQL 和对象存储。[了解更多数据流](/tidb-cloud/data-streaming-concepts.md)。

## 备份与恢复

TiDB Cloud 提供自动化备份方案和时间点恢复（PITR）能力。[了解更多备份与恢复](/tidb-cloud/backup-and-restore-concepts.md)。

## 安全

TiDB Cloud 提供强大且灵活的安全框架，旨在保护数据、实施访问控制，并满足现代合规标准。[了解更多安全相关内容](/tidb-cloud/security-concepts.md)。