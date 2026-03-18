---
title: TiDB API 概览
summary: 了解 TiDB Cloud 和 TiDB Self-Managed 可用的 API。
---

# TiDB API 概览

TiDB 提供多种 API，用于查询和操作集群、管理数据副本、监控系统状态等。本文档概述了 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/) 和 [TiDB Self-Managed](https://docs.pingcap.com/tidb/stable/) 可用的 API。

## TiDB Cloud API（测试版）

[TiDB Cloud API](/api/tidb-cloud-api-overview.md) 是一种 [REST 接口](https://en.wikipedia.org/wiki/Representational_state_transfer)，为你提供以编程方式管理 TiDB Cloud 内部管理对象的能力，例如项目、集群、备份、恢复、导入、账单和 Data Service 资源。

| API | 描述 |
| --- | --- |
| [v1beta1](/api/tidb-cloud-api-v1beta1.md) | 管理 TiDB Cloud Starter、Essential 和 Dedicated 集群，以及账单、Data Service 和 IAM 资源。 |
| [v1beta](/api/tidb-cloud-api-v1beta.md) | 管理 TiDB Cloud 的项目、集群、备份、导入和恢复。 |

## TiDB Self-Managed API

TiDB Self-Managed 提供多种 API，供 TiDB 工具使用，帮助你管理集群组件、监控系统状态以及控制数据副本工作流。

| API | 描述 |
| --- | --- |
| [TiProxy API](/tiproxy/tiproxy-api.md) | 访问 TiProxy 配置、健康状态和监控数据。 |
| [Data Migration API](/dm/dm-open-api.md) | 管理 DM-master 和 DM-worker 节点、数据源及数据副本任务。 |
| [Monitoring API](/tidb-monitoring-api.md) | 获取 TiDB 服务器运行状态、表存储信息和 TiKV 集群详情。 |
| [TiCDC API](/ticdc/ticdc-open-api-v2.md) | 查询 TiCDC 节点状态并管理副本任务，包括创建、暂停、恢复和更新操作。 |
| [TiDB Operator API](https://github.com/pingcap/tidb-operator/blob/{{{.tidb-operator-version}}}/docs/api-references/docs.md) | 管理 Kubernetes 上的 TiDB 集群，包括部署、升级、扩缩容、备份和故障转移。 |