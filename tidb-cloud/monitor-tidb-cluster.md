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
| **AVAILABLE** | The cluster is healthy and available. |
| **CREATING** | The cluster is being created. The cluster is inaccessible while it is being created. |
| **IMPORTING** | Importing data into the cluster. |
| **MODIFYING** | The cluster is being modified. |
| **UNAVAILABLE** | The cluster has failed and TiDB cannot recover it. |
| **PAUSED** | The cluster is paused. |
| **RESUMING** | The cluster is resuming from a pause. |
| **RESTORING** | The cluster is currently being restored from a backup. |

### TiDB node status

> **Note:**
>
> The TiDB node status is only available for Dedicated Tier clusters.

| TiDB node status | Description |
|:--|:--|
| **Available** | The TiDB node is healthy and available. |
| **Creating** | The TiDB node is being created. |
| **Unavailable** | The TiDB node is not available. |
| **Deleting** | The TiDB node is being deleted. |

### TiKV node status

> **Note:**
>
> The TiKV node status is only available for Dedicated Tier clusters.

| TiKV node status | Description |
|:--|:--|
| **Available** | The TiKV node is healthy and available. |
| **Creating** | The TiKV node is being created. |
| **Unavailable** | The TiKV node is not available. |
| **Deleting** | The TiKV node is being deleted. |

## Monitoring metrics

In TiDB Cloud, you can view the commonly used metrics of a cluster from the following pages:

- Cluster overview page
- Cluster monitoring page

### Metrics on the cluster overview page

The cluster overview page provides general metrics of a cluster, including total QPS, query duration, active connections, TiDB CPU, TiKV CPU, TiFlash CPU, TiDB memory, TiKV memory, TiFlash memory, TiKV used storage size, and TiFlash used storage size.

> **Note:**
>
> Some of these metrics might be available only for Dedicated Tier clusters.

To view metrics on the cluster overview page, take the following steps:

1. Navigate to the **Clusters** page.

2. Click the name of a cluster to go to its cluster overview page.

### Metrics on the cluster monitoring page

The cluster monitoring page provides a full set of standard metrics of a cluster. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

> **Note:**
>
> Currently, the cluster monitoring page is unavailable for [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

To view metrics on the cluster monitoring page, take the following steps:

1. Navigate to the **Diagnosis** tab of a cluster.

2. Click the **Monitoring** tab.

For more information, see [Built-in Monitoring](/tidb-cloud/built-in-monitoring.md).
