---
title: TiDB Cloud 中 TiProxy 概述
summary: 了解 TiDB Cloud 中 TiProxy 的使用场景。
---

# TiDB Cloud 中 TiProxy 概述

TiProxy 是 PingCAP 官方的代理组件。它位于客户端与 TiDB 服务器之间，为 TiDB 提供负载均衡、连接保持等功能。

更多信息，参见 [TiProxy 概述](https://docs.pingcap.com/tidb/stable/tiproxy-overview)。

> **注意：**
>
> TiProxy 目前处于 beta 阶段，仅适用于部署在 AWS 上的 TiDB Cloud Dedicated 集群。

## 场景

TiProxy 适用于以下场景：

- 连接保持：当 TiDB 服务器进行缩容、滚动升级或滚动重启时，客户端连接会断开，导致报错。如果客户端没有幂等的错误重试机制，则需要手动排查和修复错误，极大增加了运维开销。TiProxy 可以保持客户端连接，使客户端不会报错。
- 频繁缩容与扩容：应用的工作负载可能会周期性变化。为了节省成本，你可以在云上部署 TiDB，并根据工作负载自动缩容和扩容 TiDB 服务器。但缩容可能导致客户端断开连接，扩容可能导致负载不均。TiProxy 可以保持客户端连接，并实现负载均衡。
- CPU 负载不均：当后台任务消耗大量 CPU 资源，或不同连接的工作负载差异较大，导致 CPU 负载不均时，TiProxy 可以根据 CPU 使用率迁移连接，实现负载均衡。更多详情，参见 [基于 CPU 的负载均衡](https://docs.pingcap.com/tidb/stable/tiproxy-load-balance#cpu-based-load-balancing)。

更多场景，参见 [TiProxy 用户场景](https://docs.pingcap.com/tidb/stable/tiproxy-overview#user-scenarios)。

## 限制

在以下场景下，TiProxy 无法保持客户端连接：

- 升级 AWS EKS、Azure AKS、Google Cloud GKE 或阿里云 ACK。
- 禁用、缩容、升级或重启 TiProxy。
- 单条语句或事务运行超过 20 秒。如果你的应用需要更长的超时时间，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

更多场景，参见 [TiProxy 限制](https://docs.pingcap.com/tidb/stable/tiproxy-overview#limitations)。

## 计费

TiProxy 会引入两类成本：

- 节点成本。更多信息，参见 [节点成本](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)
- 数据传输成本。更多信息，参见 [数据传输成本](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost)。TiProxy 优先将流量路由到同一可用区（AZ）的 TiDB 节点。但如果 TiDB 工作负载不均，也会将流量路由到其他可用区，这可能会产生额外的数据传输成本。

你可以在 **Billing** 页面查看 TiProxy 账单。更多信息，参见 [查看 TiProxy 账单](/tidb-cloud/tiproxy-management.md#view-tiproxy-bills)。

## SLA 影响

TiProxy 对 SLA 没有影响。