---
title: TiDB Cloud Dedicated 限制与配额
summary: 了解 TiDB Cloud 中的限制与配额。
---

# TiDB Cloud Dedicated 限制与配额

TiDB Cloud 限制了你在一个 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群中可以创建的各类组件数量，以及 TiDB 的常见使用限制。此外，还存在一些组织级别的配额，用于限制用户创建的资源总量，以防止你创建超出实际需求的资源。下表列出了相关的限制与配额。

> **注意：**
>
> 如果这些限制或配额对你的组织造成困扰，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 集群限制

| 组件 | 限制 |
|:-|:-|
| 每个 [data region](/tidb-cloud/tidb-cloud-glossary.md#region) 的副本数 | 3 |
| 跨可用区部署的可用区数量 | 3 |

> **注意：**
>
> 如果你想了解 TiDB 的常见使用限制，请参考 [TiDB Limitations](https://docs.pingcap.com/tidb/stable/tidb-limitations)。

## 集群配额

| 组件 | 配额（默认） |
|:-|:-|
| 你所在组织所有集群的 TiDB 节点总数上限 | 10 |
| 你所在组织所有集群的 TiKV 节点总数上限 | 15 |
| 你所在组织所有集群的 TiFlash 节点总数上限 | 5 |
| 你所在组织所有集群的 TiProxy 节点总数上限 | 10 |

> **注意：**
>
> 如果这些限制或配额对你的组织造成困扰，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。