---
title: TiDB Cloud Built-in Alerting
summary: Learn how to monitor your TiDB cluster by getting alert notification emails from TiDB Cloud.
---

# TiDB Cloud Built-in Alerting

The TiDB Cloud built-in alerting feature provides you with an easy way to view the alerts or be notified by emails whenever a TiDB Cloud cluster in your project triggers one of TiDB Cloud built-in alert conditions.

This document describes how to view alerts on TiDB Cloud, how to subscribe to alert notification emails and also provides the TiDB Cloud built-in alert conditions for your reference.

## View active alerts and alert history 

The Alerts page allows you to view TiDB Cloud alerts for Dedicated clusters.
To view the active alerts on the Alerts page, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can switch to the target project from the ☰ hover menu in the upper-left corner.

2. Click the name of the target cluster. The cluster overview page is displayed.
3. Click **Alerts** in the left navigation pane.
4. You can view the Alert Name, Severity, Status , Current value, Trigger time ,Duration for each active alerts. 

To view the closed alerts on the Alerts page, take the following steps:
1. In the **Alerts** page , click the "Status" filter, select "Closed" or "All". 
2. You can view the Alert Name, Severity, Status , Trigger time ,Duration for each closed alerts. 

## Edit Alert Rules

TiDB Cloud allows you to edit the rules for the Build-in Alerts. You can disable/enable the alerts or update the threshold. 

To edit the alert rules on the Alerts page, take the following steps:
1. In the **Alerts** page , click the "Edit Rules" button. 
2. Click Switch button to disable or enable alert rules.
3. Click the "Edit" button to update the threshold of alert rules. 

    > **Tip:**
    >
    > TiDB Cloud provide limited capability for alert rule editing . Some alert rules does not support to edit. If you would like to configure different trigger conditions, thresholds, or frequency, or have alerts automatically trigger actions in downstream services like [PagerDuty](https://www.pagerduty.com/docs/guides/datadog-integration-guide/), consider using a third-party monitoring and alerting integration. Currently, TiDB Cloud supports the [Datadog integration](/tidb-cloud/monitor-datadog-integration.md) and the [Prometheus and Grafana integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).

## Subscribe to alert notification emails

If you are a member of a project and you want to get alert notification emails of clusters in your project, take the following steps:

1. In the **Alerts** page , click the "Subscribe Alerts" button. 
2. Enter your email address, and then click **Subscribe**. 
    > **Tip:**
    >
    > The alert subscription is for all the alerts in current project. If you have multiple clusters in the project, you just need to subscribe once. 

You can also add the subscription from the Alert Subscription page, take the following steps: 

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
| Total TiDB node memory utilization across cluster exceeded 70% for 10 minutes | Total TiDB node memory utilization of cluster ABC in project XYZ has exceeded 70% for 10 minutes. Consider increasing the node number or node size for TiDB to reduce the memory usage percentage of the current workload.|
| Total TiKV node memory utilization across cluster exceeded 70% for 10 minutes | Total TiKV node memory utilization of cluster ABC in project XYZ has exceeded 70% for 10 minutes. Consider increasing the node number or node size for TiKV to reduce the memory usage percentage of the current workload. |
| Total TiFlash node memory utilization across cluster exceeded 70% for 10 minutes | Total TiFlash node memory utilization of cluster ABC in project XYZ has exceeded 70% for 10 minutes. Consider increasing the node number or node size for TiFlash to reduce the memory usage percentage of the current workload. |
| Total TiDB node CPU utilization exceeded 80% for 10 minutes | Total TiDB node CPU utilization of cluster ABC in project XYZ has exceeded 80% for 10 minutes. Consider increasing the node number or node size for TiDB to reduce the CPU usage percentage of the current workload.|
| Total TiKV node CPU utilization exceeded 80% for 10 minutes | Total TiKV node CPU utilization of cluster ABC in project XYZ has exceeded 80% for 10 minutes. Consider increasing the node number or node size for TiKV to reduce the CPU usage percentage of the current workload. |
| Total TiFlash node CPU utilization exceeded 80% for 10 minutes | Total TiFlash node CPU utilization of cluster ABC in project XYZ has exceeded 80% for 10 minutes. Consider increasing the node number or node size for TiFlash to reduce the CPU usage percentage of the current workload. |
| TiKV storage utilization exceeds 80% | Total TiKV storage utilization of cluster ABC in project XYZ exceeds 80%. Consider increasing the node number or node storage size for TiKV to increase your storage capacity. |
| TiFlash storage utilization exceeds 80% | Total TiFlash storage utilization of cluster ABC in project XYZ exceeds 80%. Consider increasing the node number or node storage size for TiFlash to increase your storage capacity. |
| Data migration job met error during data export | Check the error and see [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help.  |
| Data migration job met error during data import | Check the error and see [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Data migration job met error during incremental migration | Check the error and see [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Data migration job has been paused for more than 6 hours during incremental migration | Data migration job has been paused for more than 6 hours during data incremental migration. The binlog in the upstream database might be purged (depending on your database binlog purge strategy) and might cause incremental migration to fail. See [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Replication lag is larger than 10 minutes and still increasing for more than 20 minutes | See [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |

> **Note:**
>
> - "cluster ABC" and "project XYZ" in the **Recommended Action** column are example names for reference.
