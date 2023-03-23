---
title: TiDB Cloud Built-in Alerting
summary: Learn how to monitor your TiDB cluster by getting alert notification emails from TiDB Cloud.
---

# TiDB Cloud Built-in Alerting

The TiDB Cloud built-in alerting feature provides you with an easy way to be notified by emails whenever a TiDB Cloud cluster in your project triggers one of TiDB Cloud built-in alert conditions.

This document describes how to subscribe to alert notification emails from TiDB Cloud and also provides the TiDB Cloud built-in alert conditions for your reference.

## Limitation

You cannot customize the TiDB Cloud built-in alerting. If you would like to configure different trigger conditions, thresholds, or frequency, or have alerts automatically trigger actions in downstream services like [PagerDuty](https://www.pagerduty.com/docs/guides/datadog-integration-guide/), consider using a third-party monitoring and alerting integration. Currently, TiDB Cloud supports the [Datadog integration](/tidb-cloud/monitor-datadog-integration.md) and the [Prometheus and Grafana integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).

## Subscribe to alert notification emails

If you are a member of a project and you want to get alert notification emails of clusters in your project, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. In the left navigation pane of the [**Clusters**](https://tidbcloud.com/console/clusters) page, do one of the following:

    - If you have multiple projects, switch to the target project, and then click **Admin** > **Alert Subscription**.
    - If you only have one project, click **Admin** > **Alert Subscription**.

3. Click **Add Subscriber**, enter your email address in the displayed dialog, and then click **Add**.

If an alert condition remains unchanged, the alert sends email notifications every 3 hours.

## Unsubscribe from alert notification emails

If you no longer want to receive alert notification emails of clusters in your project, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. In the left navigation pane of the [**Clusters**](https://tidbcloud.com/console/clusters) page, do one of the following:

    - If you have multiple projects, switch to the target project, and then click **Admin** > **Alert Subscription**.
    - If you only have one project, click **Admin** > **Alert Subscription**.

3. Locate your email address and click **Unsubscribe**.
4. Click **Delete** to confirm the unsubscription.

## TiDB Cloud built-in alert conditions

The following table provides the TiDB Cloud built-in alert conditions and the corresponding recommended actions.

> **Note:**
>
> Although these alert conditions do not necessarily mean there is a problem, they are often early warning indicators of emerging issues. Thus, taking the recommended action is advised.

| Condition | Recommended Action |
|:--- |:--- |
| Total TiDB node memory utilization across cluster exceeded 70% for 10 minutes | Total TiDB node memory utilization of cluster ABC in project XYZ has exceeded 70% for 10 minutes. Consider increasing the node number or node size for TiDB to reduce the memory usage percentage of the current workload. To monitor node memory utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Total TiKV node memory utilization across cluster exceeded 70% for 10 minutes | Total TiKV node memory utilization of cluster ABC in project XYZ has exceeded 70% for 10 minutes. Consider increasing the node number or node size for TiKV to reduce the memory usage percentage of the current workload. To monitor node memory utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Total TiFlash node memory utilization across cluster exceeded 70% for 10 minutes | Total TiFlash node memory utilization of cluster ABC in project XYZ has exceeded 70% for 10 minutes. Consider increasing the node number or node size for TiFlash to reduce the memory usage percentage of the current workload. To monitor node memory utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| At least one TiDB node in the cluster has run out of memory | At least one TiDB node in cluster ABC in project XYZ ran out of memory while executing a SQL statement. Consider increasing the memory available to queries using the `tidb_mem_quota_query` session variable. To monitor node memory utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). This alert will be removed in a future release. |
| Total TiDB node CPU utilization exceeded 80% for 10 minutes | Total TiDB node CPU utilization of cluster ABC in project XYZ has exceeded 80% for 10 minutes. Consider increasing the node number or node size for TiDB to reduce the CPU usage percentage of the current workload. To monitor node CPU utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Total TiKV node CPU utilization exceeded 80% for 10 minutes | Total TiKV node CPU utilization of cluster ABC in project XYZ has exceeded 80% for 10 minutes. Consider increasing the node number or node size for TiKV to reduce the CPU usage percentage of the current workload. To monitor node CPU utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| Total TiFlash node CPU utilization exceeded 80% for 10 minutes | Total TiFlash node CPU utilization of cluster ABC in project XYZ has exceeded 80% for 10 minutes. Consider increasing the node number or node size for TiFlash to reduce the CPU usage percentage of the current workload. To monitor node CPU utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| TiKV storage utilization exceeds 80% | Total TiKV storage utilization of cluster ABC in project XYZ exceeds 80%. Consider increasing the node number or node storage size for TiKV to increase your storage capacity. To monitor storage utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| TiFlash storage utilization exceeds 80% | Total TiFlash storage utilization of cluster ABC in project XYZ exceeds 80%. Consider increasing the node number or node storage size for TiFlash to increase your storage capacity. To monitor storage utilization, see [Monitoring metrics](/tidb-cloud/monitor-tidb-cluster.md#monitoring-metrics). |
| One or more cluster nodes are offline | Some or all nodes in cluster ABC in project XYZ are offline. The TiDB Cloud Operations team is aware and working to resolve the issue. Refer to [TiDB Cloud Status](https://status.tidbcloud.com/) for the latest information. To monitor node status, see [Cluster status and node status](/tidb-cloud/monitor-tidb-cluster.md#cluster-status-and-node-status). This alert will be removed in a future release.  |
| Data migration job met error during data export | Check the error and see [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help.  |
| Data migration job met error during data import | Check the error and see [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Data migration job met error during incremental migration | Check the error and see [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Data migration job has been paused for more than 6 hours during incremental migration | Data migration job has been paused for more than 6 hours during data incremental migration. The binlog in the upstream database might be purged (depending on your database binlog purge strategy) and might cause incremental migration to fail. See [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Replication lag is larger than 10 minutes and still increasing for more than 20 minutes | See [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |

> **Note:**
>
> - "cluster ABC" and "project XYZ" in the **Recommended Action** column are example names for reference.
