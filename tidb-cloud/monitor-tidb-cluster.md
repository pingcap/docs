---
title: 监控 TiDB
summary: 了解如何监控你的 TiDB Cloud 资源。
---

# 监控 TiDB

本文档介绍如何监控 <CustomContent plan="starter">{{{ .starter }}} 实例</CustomContent><CustomContent plan="essential">{{{ .essential }}} 实例</CustomContent><CustomContent plan="premium">{{{ .premium }}} 实例</CustomContent><CustomContent plan="dedicated">{{{ .dedicated }}} 集群</CustomContent>。

<CustomContent plan="dedicated">

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

</CustomContent>

<CustomContent plan="starter,essential,premium">

## Instance status

在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，你可以在 **Status** 列中查看每个正在运行的 TiDB Cloud 实例的当前状态。

| Status | Description |
|:--|:--|
| **Active** | 实例健康且可用。 |
| **Creating** | 实例正在创建中。实例在创建期间不可访问。 |
| **Importing** | 正在将数据导入实例。 |
| **Maintaining** | 实例正在维护中。 |
| **Modifying** | 实例正在被修改。 |
| **Unavailable** | 实例发生故障，TiDB 无法恢复。 |
| **Restoring** | 实例当前正在从备份恢复。 |

</CustomContent>

## 监控统计/指标（信息）

在 TiDB Cloud 中，你可以通过以下页面查看集群的常用统计/指标（信息）：

- **Overview** 页面
- **Metrics** 页面

### Overview 页面

**Overview** 页面提供你的 TiDB Cloud 资源的总体统计/指标（信息）。

要在 Overview 页面查看统计/指标（信息），请按照以下步骤操作：

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击目标资源名称，进入其 Overview 页面。

    > **提示：**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 查看 **Core Metrics** 部分。

## Monitoring metrics

在 TiDB Cloud 中，你可以从以下页面查看 <CustomContent plan="starter">{{{ .starter }}} 实例</CustomContent><CustomContent plan="essential">{{{ .essential }}} 实例</CustomContent><CustomContent plan="premium">{{{ .premium }}} 实例</CustomContent><CustomContent plan="dedicated">{{{ .dedicated }}} 集群</CustomContent> 的常用统计/指标（信息）：

- **Overview** 页面
- **Metrics** 页面
