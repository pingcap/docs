---
title: Monitor TiDB
summary: Learn how to monitor your TiDB Cloud cluster or instance.
---

# Monitor TiDB

This document describes how to monitor a <CustomContent plan="starter">{{{ .starter }}} instance</CustomContent><CustomContent plan="essential">{{{ .essential }}} instance</CustomContent><CustomContent plan="premium">{{{ .premium }}} instance</CustomContent><CustomContent plan="dedicated">{{{ .dedicated }}} cluster</CustomContent>.

<CustomContent plan="dedicated">

## Cluster status and node status

You can see the current status of each running cluster on the cluster page.

### Cluster status

| Cluster status | Description |
|:--|:--|
| **Available** | The cluster is healthy and available. |
| **Creating** | The cluster is being created. The cluster is inaccessible while it is being created. |
| **Importing** | Importing data into the cluster. |
| **Maintaining** | The cluster is in maintenance. |
| **Modifying** | The cluster is being modified. |
| **Unavailable** | The cluster has failed and TiDB cannot recover it. |
| **Pausing** | The cluster is being paused. |
| **Paused** | The cluster is paused. |
| **Resuming** | The cluster is being resumed from a pause. |
| **Restoring** | The cluster is currently being restored from a backup. |

### TiDB node status

> **Note:**
>
> The TiDB node status is only available for TiDB Cloud Dedicated clusters.

The node names starting with `tidb` are TiDB nodes, and those starting with `tiproxy` are TiProxy nodes.

| TiDB node status | Description |
|:--|:--|
| **Available** | The TiDB node is healthy and available. |
| **Creating** | The TiDB node is being created. |
| **Unavailable** | The TiDB node is not available. |
| **Deleting** | The TiDB node is being deleted. |

### TiKV node status

> **Note:**
>
> The TiKV node status is only available for TiDB Cloud Dedicated clusters.

| TiKV node status | Description |
|:--|:--|
| **Available** | The TiKV node is healthy and available. |
| **Creating** | The TiKV node is being created. |
| **Unavailable** | The TiKV node is not available. |
| **Deleting** | The TiKV node is being deleted. |

</CustomContent>

<CustomContent plan="starter,essential,premium">

## Instance status

On the [**My TiDB**](https://tidbcloud.com/tidbs) page, you can see the current status of each running TiDB Cloud instance in the **Status** column.

| Status | Description |
|:--|:--|
| **Active** | The instance is healthy and available. |
| **Creating** | The instance is being created. The instance is inaccessible while it is being created. |
| **Importing** | Importing data into the instance. |
| **Maintaining** | The instance is in maintenance. |
| **Modifying** | The instance is being modified. |
| **Unavailable** | The instance has failed and TiDB cannot recover it. |
| **Restoring** | The instance is currently being restored from a backup. |

</CustomContent>

## Monitoring metrics

In TiDB Cloud, you can view the commonly used metrics of a <CustomContent plan="starter">{{{ .starter }}} instance</CustomContent><CustomContent plan="essential">{{{ .essential }}} instance</CustomContent><CustomContent plan="premium">{{{ .premium }}} instance</CustomContent><CustomContent plan="dedicated">{{{ .dedicated }}} cluster</CustomContent> from the following pages:

- **Overview** page
- **Metrics** page

### Overview page

The **Overview** page provides general metrics of a cluster.

To view metrics on the cluster overview page, take the following steps:

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target resource to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and resources.

2. Check the **Core Metrics** section.

### Metrics page

The **Metrics** page provides a full set of metrics of a cluster. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

To view metrics on the **Metrics** page, take the following steps:

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target resource to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and resources.

2. In the left navigation pane, click **Monitoring** > **Metrics**.

For more information, see [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md).
