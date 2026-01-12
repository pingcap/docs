---
title: Integrate TiDB Cloud with Datadog
summary: Learn how to monitor your TiDB cluster with the Datadog integration.
---

# Integrate TiDB Cloud with Datadog

TiDB Cloud supports Datadog integration. You can configure TiDB Cloud to send metrics about your TiDB clusters to [Datadog](https://www.datadoghq.com/). After that, you can view these metrics in your Datadog dashboards directly.

## Datadog integration version

TiDB Cloud has supported the project-level Datadog integration (Beta) since March 4, 2022. Starting from July 31, 2025, TiDB Cloud introduces the cluster-level Datadog integration (Preview). Starting from September 30, 2025, the cluster-level Datadog integration becomes generally available (GA).

- **Cluster-level Datadog integration**: if no legacy project-level Datadog or New Relic integration remains undeleted within your organization by July 31, 2025, TiDB Cloud provides the cluster-level Datadog integration for your organization to experience the latest enhancements.
- **Legacy project-level Datadog integration (Beta)**: if at least one legacy project-level Datadog or New Relic integration remains undeleted within your organization by July 31, 2025, TiDB Cloud retains both existing and new integrations at the project level for your organization to avoid affecting current dashboards. Note that the legacy project-level Datadog integrations will be deprecated on October 31, 2025. If your organization is still using these legacy integrations, follow [Migrate Datadog and New Relic Integrations](/tidb-cloud/migrate-metrics-integrations.md) to migrate to the new cluster-level integrations and minimize disruptions to your metrics-related services.

## Prerequisites

- To integrate TiDB Cloud with Datadog, you must have a Datadog account and a [Datadog API key](https://app.datadoghq.com/organization-settings/api-keys). Datadog grants you an API key when you first create a Datadog account.

    If you do not have a Datadog account, sign up at [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup).

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` or `Project Owner` access in TiDB Cloud. To view the integration page or access configured dashboards via the provided links, you need at least the `Project Viewer` role to access the target clusters under your project in TiDB Cloud.

## Limitation

- Datadog integrations are now only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

- Datadog integrations are not available when the cluster status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

- When a cluster with Datadog integration is deleted, its associated integration services are also removed.

## Steps

### Step 1. Integrate with your Datadog API Key

Depending on your [Datadog integration version](#datadog-integration-version), the steps to access the integration page are different.

<SimpleTab>
<div label="Cluster-level Datadog integration">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Settings** > **Integrations**.
3. On the **Integrations** page, click **Integration to Datadog**.
4. Enter your Datadog API key and choose your Datadog site.
5. Click **Test Integration**.

    - If the test succeeds, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

6. Click **Confirm** to complete the integration.

</div>
<div label="Datadog integration (Beta)">

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Integrations**.
3. On the **Integrations** page, click **Integration to Datadog (BETA)**.
4. Enter your Datadog API key and choose your Datadog site.
5. Click **Test Integration**.

    - If the test succeeds, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

6. Click **Confirm** to complete the integration.

</div>
</SimpleTab>

### Step 2. Install TiDB Cloud Integration in Datadog

> **Note:**
>
> If you have already installed the TiDB Cloud integration in Datadog, you can skip the following steps in this section. The [**TiDB Cloud Dynamic Tracker**](https://app.datadoghq.com/dash/integration/32021/tidb-cloud-dynamic-tracker) or [**TiDB Cloud Cluster Overview**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview) dashboard is automatically available in your Datadog [**Dashboard List**](https://app.datadoghq.com/dashboard/lists).

1. Log in to [Datadog](https://app.datadoghq.com).
2. Go to the [**TiDB Cloud Integration** page](https://app.datadoghq.com/account/settings#integrations/tidb-cloud) in Datadog.
3. On the **Configuration** tab, click **Install Integration**.

    - For cluster-level Datadog integration, the [**TiDB Cloud Dynamic Tracker**](https://app.datadoghq.com/dash/integration/32021/tidb-cloud-dynamic-tracker) dashboard appears in your [**Dashboard List**](https://app.datadoghq.com/dashboard/lists).
    - For legacy project-level Datadog integration (Beta), the [**TiDB Cloud Cluster Overview**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview) dashboard appears in your [**Dashboard List**](https://app.datadoghq.com/dashboard/lists).

## View the pre-built dashboard

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the **Integrations** page.
2. Click the **Dashboard** link in the **Datadog** section.

    - For cluster-level Datadog integration, the **Dashboard** link opens the new dashboard, which includes the latest metrics introduced in the enhanced version.
    - For legacy project-level Datadog integration (Beta), the **Dashboard** link opens the legacy dashboard, which does not include the latest metrics introduced in the cluster-level Datadog integration.

## Metrics available to Datadog

Datadog tracks the following metrics for your TiDB clusters.

| Metric name  | Metric type | Labels | Description                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidb_cloud.db_database_time| gauge | sql_type: Select\|Insert\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The total time consumed by all SQL statements running in TiDB per second, including the CPU time of all processes and the non-idle waiting time. |
| tidb_cloud.db_query_per_second| gauge | type: Select\|Insert\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The number of SQL statements executed per second on all TiDB instances, counted by the statement type (`SELECT`, `INSERT`, or `UPDATE`). |
| tidb_cloud.db_average_query_duration| gauge | sql_type: Select\|Insert\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The duration between the time that the client's network request is sent to TiDB and the time that the request is returned to the client after TiDB has executed it. |
| tidb_cloud.db_failed_queries| gauge | type: executor:xxxx\|parser:xxxx\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The statistics of error types (such as syntax errors and primary key conflicts) according to the SQL execution errors that occur per second on each TiDB instance. |
| tidb_cloud.db_total_connection| gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The number of current connections in your TiDB server. |
| tidb_cloud.db_active_connections| gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The number of active connections. |
| tidb_cloud.db_disconnections| gauge | result: ok\|error\|undetermined<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The number of disconnected clients. |
| tidb_cloud.db_command_per_second| gauge | type: Query\|StmtPrepare\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The number of commands processed by TiDB per second, which is classified according to the success or failure of command execution results. |
| tidb_cloud.db_queries_using_plan_cache_ops| gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The statistics of queries using [Plan Cache](/sql-prepared-plan-cache.md) per second. The execution plan cache only supports the prepared statement command. |
| tidb_cloud.db_transaction_per_second| gauge | txn_mode: pessimistic\|optimistic<br/>type: abort\|commit\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The number of transactions executed per second. |
| tidb_cloud.node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/>component: tikv\|tiflash | The disk usage of TiKV/TiFlash nodes, in bytes. |
| tidb_cloud.node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/>component: tikv\|tiflash | The disk capacity of TiKV/TiFlash nodes, in bytes. |
| tidb_cloud.node_cpu_seconds_total | count | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/>component: tidb\|tikv\|tiflash | The CPU usage of TiDB/TiKV/TiFlash nodes. |
| tidb_cloud.node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/>component: tidb\|tikv\|tiflash | The limit on CPU cores of TiDB/TiKV/TiFlash nodes. |
| tidb_cloud.node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/>component: tidb\|tikv\|tiflash | The used memory of TiDB/TiKV/TiFlash nodes, in bytes. |
| tidb_cloud.node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/>component: tidb\|tikv\|tiflash | The memory capacity of TiDB/TiKV/TiFlash nodes, in bytes. |

For cluster-level Datadog integration, the following additional metrics are also available:

| Metric name  | Metric type | Labels | Description                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidb_cloud.node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The available disk space in bytes for TiKV/TiFlash nodes. |
| tidb_cloud.node_disk_read_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The read latency in seconds per storage device. |
| tidb_cloud.node_disk_write_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The write latency in seconds per storage device. |
| tidb_cloud.db_kv_request_duration | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv`<br/>cluster_name: `<cluster name>`<br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | The duration in seconds of TiKV requests by type. |
| tidb_cloud.db_component_uptime | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tidb\|tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The uptime (in seconds) of TiDB components. |
| tidb_cloud.cdc_changefeed_latency (AKA cdc_changefeed_checkpoint_ts_lag) | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>`| The checkpoint timestamp lag (in seconds) for changefeed owner. |
| tidb_cloud.cdc_changefeed_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | The resolved timestamp lag (in seconds) for the changefeed owner. |
| tidb_cloud.cdc_changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | Changefeed status:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |
| tidb_cloud.resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The read request units (RUs) consumed by Resource Manager. |
| tidb_cloud.resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The write request units (RUs) consumed by Resource Manager. |
| tidb_cloud.dm_task_state | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | Task State of Data Migration:<br/>0: Invalid<br/>1: New<br/>2: Running<br/>3: Paused<br/>4: Stopped<br/>5: Finished<br/>15: Error |
| tidb_cloud.dm_syncer_replication_lag_bucket | gauge | instance: `instance`<br/>cluster_name: `<cluster name>` | Replicate lag (bucket) of Data Migration. |
| tidb_cloud.dm_syncer_replication_lag_gauge | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | Replicate lag (gauge) of Data Migration. |
| tidb_cloud.dm_relay_read_error_count | gauge | instance: `instance`<br/>cluster_name: `<cluster name>` | Fail to read binlog from master. |
| tidb_cloud.node_memory_available_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/>component: tidb\|tikv\|tiflash | The available memory of TiDB/TiKV/TiFlash nodes, in bytes. |
| tidb_cloud.cdc_changefeed_replica_rows | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | The number of events that TiCDC nodes write to the downstream per second. |
