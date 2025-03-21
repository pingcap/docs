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

## Monitoring metrics

In TiDB Cloud, you can view the commonly used metrics of a cluster from the following pages:

- Cluster overview page
- Cluster metrics page

### Metrics on the cluster overview page

The cluster overview page provides general metrics of a cluster, including Request Units, Used Storage Size, Query Per Second, and Average Query Duration.

To view metrics on the cluster overview page, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.

2. Choose the target project and click the name of a cluster to go to its cluster overview page.

### Metrics on the cluster metrics page

The cluster metrics page provides a full set of standard metrics of a cluster. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

To view metrics on the cluster monitoring page, take the following steps:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page of the target project, click the name of the target cluster. The cluster overview page is displayed.
2. Click **Metrics** in the left navigation pane.

For more information, see [Built-in Monitoring](/tidb-cloud/built-in-monitoring.md).