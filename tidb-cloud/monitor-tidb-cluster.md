---
title: 监控 TiDB 集群
summary: 了解如何监控你的 TiDB 集群。
---

# 监控 TiDB 集群

本文档介绍如何在 TiDB Cloud 上监控 TiDB 集群。

## 集群状态与节点状态

你可以在集群页面查看每个正在运行的集群的当前状态。

### 集群状态

| 集群状态 | 描述 |
|:--|:--|
| **Available** | 集群健康且可用。 |
| **Creating** | 集群正在创建中。创建期间集群不可访问。 |
| **Importing** | 正在向集群导入数据。 |
| **Maintaining** | 集群处于维护中。 |
| **Modifying** | 集群正在被修改。 |
| **Unavailable** | 集群发生故障且 TiDB 无法恢复。 |
| **Pausing** | 集群正在暂停中。 |
| **Paused** | 集群已暂停。 |
| **Resuming** | 集群正在从暂停状态恢复。 |
| **Restoring** | 集群正在从备份恢复。 |

### TiDB 节点状态

> **注意：**
>
> TiDB 节点状态仅适用于 TiDB Cloud Dedicated 集群。

以 `tidb` 开头的节点名称为 TiDB 节点，以 `tiproxy` 开头的为 TiProxy 节点。

| TiDB 节点状态 | 描述 |
|:--|:--|
| **Available** | TiDB 节点健康且可用。 |
| **Creating** | TiDB 节点正在创建中。 |
| **Unavailable** | TiDB 节点不可用。 |
| **Deleting** | TiDB 节点正在被删除。 |

### TiKV 节点状态

> **注意：**
>
> TiKV 节点状态仅适用于 TiDB Cloud Dedicated 集群。

| TiKV 节点状态 | 描述 |
|:--|:--|
| **Available** | TiKV 节点健康且可用。 |
| **Creating** | TiKV 节点正在创建中。 |
| **Unavailable** | TiKV 节点不可用。 |
| **Deleting** | TiKV 节点正在被删除。 |

## 监控统计/指标（信息）

在 TiDB Cloud 中，你可以通过以下页面查看集群的常用统计/指标（信息）：

- **Overview** 页面
- **Metrics** 页面

### Overview 页面

**Overview** 页面提供集群的总体统计/指标（信息）。

要在集群 Overview 页面查看统计/指标（信息），请按照以下步骤操作：

1. 在你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称，进入其 Overview 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 查看 **Core Metrics** 部分。

### Metrics 页面

**Metrics** 页面提供集群的完整统计/指标（信息）集。通过查看这些统计/指标（信息），你可以轻松识别性能问题，并判断当前数据库部署是否满足你的需求。

要在 **Metrics** 页面查看统计/指标（信息），请按照以下步骤操作：

1. 在你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称，进入其 Overview 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Monitoring** > **Metrics**。

更多信息，参见 [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md)。