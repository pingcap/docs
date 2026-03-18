---
title: TiDB Cloud Built-in Alerting
summary: Learn how to monitor your TiDB cluster by getting alert notifications from TiDB Cloud.
---

# TiDB Cloud Built-in Alerting

TiDB Cloud provides you with an easy way to view alerts, edit alert rules, and subscribe to alert notifications.

This document describes how to do these operations and provides the TiDB Cloud built-in alert conditions for your reference.

> **Note:**
>
> Currently, alert subscription is available for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## View alerts

In TiDB Cloud, you can view both active and closed alerts on the **Alerts** page.

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of the target cluster. The cluster overview page is displayed.
3. Click **Alerts** in the left navigation pane.
4. The **Alerts** page displays the active alerts by default. You can view the information of each active alert such as the alert name, trigger time, and duration.
5. If you also want to view the closed alerts, just click the **Status** drop-down list and select **Closed** or **All**.

## Edit alert rules

In TiDB Cloud, you can edit the alert rules by disabling or enabling the alerts or updating the alert threshold.

1. On the **Alerts** page, click **Edit Rules**.
2. Disable or enable alert rules as needed.
3. Click **Edit** to update the threshold of an alert rule.

    > **Tip:**
    >
    > Currently, TiDB Cloud provides limited capabilities for alert rule editing. Some alert rules do not support editing. If you would like to configure different trigger conditions or frequency, or have alerts automatically trigger actions in downstream services like [PagerDuty](https://www.pagerduty.com/docs/guides/datadog-integration-guide/), consider using a [third-party monitoring and alerting integration](/tidb-cloud/third-party-monitoring-integrations.md).

## Subscribe to alert notifications

In TiDB Cloud, you can subscribe to alert notifications via one of the following methods:

- [Email](/tidb-cloud/monitor-alert-email.md)
- [Slack](/tidb-cloud/monitor-alert-slack.md)
- [Zoom](/tidb-cloud/monitor-alert-zoom.md)
- [Flashduty](/tidb-cloud/monitor-alert-flashduty.md)
- [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md)

## TiDB Cloud built-in alert conditions

The following table provides the TiDB Cloud built-in alert conditions and the corresponding recommended actions.

> **Note:**
>
> - While these alert conditions do not necessarily mean there is a problem, they are often early warning indicators of emerging issues. Therefore, taking the recommended action is advised.
> - You can edit the thresholds of the alerts on the TiDB Cloud console. 
> - Some alert rules are disabled by default. You can enable them as needed.

TiDB Cloud provides different alert rules for each cluster plan, based on the features available in that plan.

<CustomContent plan="dedicated">

### Resource usage alerts

| Condition | Recommended Action |
|:--- |:--- |
| Total TiDB node memory utilization across cluster exceeded 70% for 10 minutes | Consider increasing the node number or node size for TiDB to reduce the memory usage percentage of the current workload.|
| Total TiKV node memory utilization across cluster exceeded 70% for 10 minutes | Consider increasing the node number or node size for TiKV to reduce the memory usage percentage of the current workload. |
| Total TiFlash node memory utilization across cluster exceeded 70% for 10 minutes | Consider increasing the node number or node size for TiFlash to reduce the memory usage percentage of the current workload. |
| Total TiDB node CPU utilization exceeded 80% for 10 minutes | Consider increasing the node number or node size for TiDB to reduce the CPU usage percentage of the current workload.|
| Total TiKV node CPU utilization exceeded 80% for 10 minutes | Consider increasing the node number or node size for TiKV to reduce the CPU usage percentage of the current workload. |
| Total TiFlash node CPU utilization exceeded 80% for 10 minutes | Consider increasing the node number or node size for TiFlash to reduce the CPU usage percentage of the current workload. |
| TiKV storage utilization exceeds 80% | Consider increasing the node number or node storage size for TiKV to increase your storage capacity. |
| TiFlash storage utilization exceeds 80% | Consider increasing the node number or node storage size for TiFlash to increase your storage capacity. |
| Max memory utilization across TiDB nodes exceeded 70% for 10 minutes | Consider checking if there is any [hotspot](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues) in the cluster or increasing the node number or node size for TiDB to reduce the memory usage percentage of the current workload. |
| Max memory utilization across TiKV nodes exceeded 70% for 10 minutes | Consider checking if there is any [hotspot](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues) in the cluster or increasing the node number or node size for TiKV to reduce the memory usage percentage of the current workload. |
| Max CPU utilization across TiDB nodes exceeded 80% for 10 minutes | Consider checking if there is any [hotspot](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues) in the cluster or increasing the node number or node size for TiDB to reduce the CPU usage percentage of the current workload. |
| Max CPU utilization across TiKV nodes exceeded 80% for 10 minutes | Consider checking if there is any [hotspot](/tidb-cloud/tidb-cloud-sql-tuning-overview.md#hotspot-issues) in the cluster or increasing the node number or node size for TiKV to reduce the CPU usage percentage of the current workload. |

### Data migration alerts

| Condition | Recommended Action |
|:--- |:--- |
| Data migration job met error during data export | Check the error and see [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Data migration job met error during data import | Check the error and see [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Data migration job met error during incremental migration | Check the error and see [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Data migration job has been paused for more than 6 hours during incremental migration | Data migration job has been paused for more than 6 hours during data incremental migration. The binlog in the upstream database might be purged (depending on your database binlog purge strategy) and might cause incremental migration to fail. See [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |
| Replication lag is larger than 10 minutes and still increasing for more than 20 minutes | See [Troubleshoot data migration](/tidb-cloud/tidb-cloud-dm-precheck-and-troubleshooting.md#migration-errors-and-solutions) for help. |

### Changefeed alerts for {{{ .dedicated }}}

| Condition                                   | Recommended Action                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| The changefeed latency exceeds 600 seconds. | Check the changefeed status on the **Changefeed** page and **Changefeed Detail** page of the TiDB Cloud console, where you can find some error messages to help diagnose this issue. <br/> Possible reasons that can trigger this alert include:<ul><li>The overall traffic in the upstream has increased, causing the existing changefeed specification to be insufficient to handle it. If the traffic increase is temporary, the changefeed latency will automatically recover after the traffic returns to normal. If the traffic increase is continuous, you need to scale up the changefeed.</li><li>The downstream or network is abnormal. In this case, resolve this abnormality first.</li><li>Tables lack indexes if the downstream is RDS, which might cause low write performance and high latency. In this case, you need to add the necessary indexes to the upstream or downstream.</li></ul>If the problem cannot be fixed from your side, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for further assistance. |
| The changefeed status is `FAILED`.                 | Check the changefeed status on the **Changefeed** page and **Changefeed Detail** page of the TiDB Cloud console, where you can find some error messages to help diagnose this issue. <br/> If the problem cannot be fixed from your side, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for further assistance.|
| The changefeed status is `WARNING`.              | Check the changefeed status on the **Changefeed** page and **Changefeed Detail** page of the TiDB Cloud console, where you can find some error messages to help diagnose this issue. <br/> If the problem cannot be fixed from your side, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for further assistance.|

</CustomContent>

<CustomContent plan="essential">

### Performance overview alerts

| Condition | Recommended Action |
|:--- |:--- |
| Request units per second (RU/s) exceed 80% of the maximum RCU | <ol><li>Review RU metrics to determine whether the increase is gradual or a sudden spike.</li><li>If the increase is gradual, check whether query duration has increased. If so, the current maximum RCU might be insufficient.</li><li>Scale capacity by manually increasing the maximum RCU in the TiDB Cloud console.</li></ol><br/>If you cannot resolve the issue, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).|
| QPS drops by 80% | <ol><li>Check whether the drop is caused by increasing query latency.</li><li>Verify that your application is operating normally. If the drop is intentional, ignore this alert. If the drop is unintentional and you cannot identify the root cause, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) immediately.</li></ol>|
| Query P99 latency exceeds 200 ms | <ol><li>Investigate slow queries: go to the Slow Query page and filter by a recent time range to identify newly introduced or slower-running queries.</li><li>Review recent changes, such as application deployments, schema changes, or data import jobs, that might have affected traffic patterns.</li></ol><br/>If you cannot identify the root cause, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) immediately.|
| Query P95 latency exceeds 200 ms | <ol><li>Investigate slow queries: go to the Slow Query page and filter by a recent time range to identify newly introduced or slower-running queries.</li><li>Review recent changes, such as application deployments, schema changes, or data import jobs, that might have affected traffic patterns.</li></ol><br/>If you cannot identify the root cause, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) immediately.|
| Request error rate exceeds 10%  | Review recent errors and the overall statement execution status for the cluster.|

### Changefeed alerts for {{{ .essential }}}

| Condition                                   | Recommended Action                   |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| The changefeed latency exceeds 600 seconds. | Check the changefeed status on the **Changefeed** page and **Changefeed Detail** page of the TiDB Cloud console, where you can find some error messages to help diagnose this issue. <br/> Possible reasons that can trigger this alert include:<ul><li>The overall traffic in the upstream has increased, causing the existing changefeed specification to be insufficient to handle it. If the traffic increase is temporary, the changefeed latency will automatically recover after the traffic returns to normal. If the traffic increase is continuous, you need to scale up the changefeed.</li><li>The downstream or network is abnormal. In this case, resolve this abnormality first.</li><li>Tables lack indexes if the downstream is RDS, which might cause low write performance and high latency. In this case, you need to add the necessary indexes to the upstream or downstream.</li></ul>If the problem cannot be fixed from your side, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for further assistance. |
| The changefeed status is `FAILED`.                 | Check the changefeed status on the **Changefeed** page and **Changefeed Detail** page of the TiDB Cloud console, where you can find some error messages to help diagnose this issue. <br/> If the problem cannot be fixed from your side, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for further assistance.|
| The changefeed status is `WARNING`.              | Check the changefeed status on the **Changefeed** page and **Changefeed Detail** page of the TiDB Cloud console, where you can find some error messages to help diagnose this issue. <br/> If the problem cannot be fixed from your side, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for further assistance.|

</CustomContent>
