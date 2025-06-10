---
title: Monitor a TiDB Cluster
summary: Learn how to monitor your TiDB cluster.
---

# Monitor a TiDB Cluster

This document describes how to monitor a TiDB cluster on TiDB Cloud.

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

## Monitoring metrics

In TiDB Cloud, you can view the commonly used metrics of a cluster from the following pages:

- **Overview** page
- **Metrics** page

### Overview page

The **Overview** page provides general metrics of a cluster.

To view metrics on the cluster overview page, take the following steps:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Check the **Core Metrics** section.

### Metrics page

The **Metrics** page provides a full set of metrics of a cluster. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

To view metrics on the **Metrics** page, take the following steps:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. In the left navigation pane, click **Monitoring** > **Metrics**.

For more information, see [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md).
