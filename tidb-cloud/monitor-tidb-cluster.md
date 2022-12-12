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

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.

2. Click the name of a cluster to go to its cluster overview page.

### Metrics on the cluster monitoring page

The cluster monitoring page provides a full set of standard metrics of a cluster. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

> **Note:**
>
> Currently, the cluster monitoring page is unavailable for [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

To view metrics on the cluster monitoring page, take the following steps:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of the target cluster. The cluster overview page is displayed.
2. Click the <svg width="14" height="14" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.5421 6.5H3.58333C2.43274 6.5 1.5 5.56726 1.5 4.41667C1.5 3.26607 2.43274 2.33333 3.58333 2.33333H11.5421M6.45791 15.6667H14.4167C15.5673 15.6667 16.5 14.7339 16.5 13.5833C16.5 12.4327 15.5673 11.5 14.4167 11.5H6.45791M1.5 13.5833C1.5 15.1942 2.80584 16.5 4.41667 16.5C6.0275 16.5 7.33333 15.1942 7.33333 13.5833C7.33333 11.9725 6.0275 10.6667 4.41667 10.6667C2.80584 10.6667 1.5 11.9725 1.5 13.5833ZM16.5 4.41667C16.5 6.0275 15.1942 7.33333 13.5833 7.33333C11.9725 7.33333 10.6667 6.0275 10.6667 4.41667C10.6667 2.80584 11.9725 1.5 13.5833 1.5C15.1942 1.5 16.5 2.80584 16.5 4.41667Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg> icon on the left navigation.

For more information, see [Built-in Monitoring](/tidb-cloud/built-in-monitoring.md).
