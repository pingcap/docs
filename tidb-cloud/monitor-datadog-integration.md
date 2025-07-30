---
title: Integrate TiDB Cloud with Datadog (Preview)
summary: Learn how to monitor your TiDB cluster with the Datadog integration.
---

# Integrate TiDB Cloud with Datadog (Preview)

TiDB Cloud supports Datadog integration (Preview). You can configure TiDB Cloud to send metrics about your TiDB clusters to [Datadog](https://www.datadoghq.com/). After that, you can view these metrics in your Datadog dashboards directly.

## Datadog integration version

TiDB Cloud has supported Datadog integration (Beta) since March 04, 2022. Starting from July 31, 2025, TiDB Cloud introduces an enhanced preview version of the integration.

- **Datadog integration (Preview)**: if Datadog and New Relic integrations do not exist in your organization on July 31, 2025, TiDB Cloud provides the preview version of Datadog integration for your organization to experience the latest enhancements.
- **Datadog integration (Beta)**: if any Datadog or New Relic integrations exist in your organization on July 31, 2025, TiDB Cloud retains both existing and new integrations in the beta version to avoid affecting current dashboards. We will also proactively reach out to you to discuss a suitable migration plan and timeline.

## Prerequisites

- To integrate TiDB Cloud with Datadog, you must have a Datadog account and a [Datadog API key](https://app.datadoghq.com/organization-settings/api-keys). Datadog grants you an API key when you first create a Datadog account.

    If you do not have a Datadog account, sign up at [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup).

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` or `Project Owner` access in TiDB Cloud. To view the integration page or access configured dashboards via the provided links, users need at least the `Project Viewer` role to access the target clusters under the project in TiDB Cloud.

## Limitation

- You cannot use the Datadog integration in [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters.

- Datadog integrations are not available when the cluster status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**. For clusters that were previously configured with metrics integrations, the associated integration services will be discontinued once the cluster is deleted.

- When a cluster with Datadog integration is deleted, its associated integration services are also removed.

## Steps

### Step 1. Integrate with your Datadog API Key

Depending on your [Datadog integration version](#datadog-integration-version), the steps to access the integration page are different.

<SimpleTab>
<div label="Datadog integration (Preview)">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Settings** > **Integrations**.
3. On the **Integrations** page, click **Integration to Datadog (PREVIEW)**.
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

Depending on your [Datadog integration version](#datadog-integration-version), the steps are different.

<SimpleTab>
<div label="Datadog integration (Preview)">

A new TiDB Cloud dashboard will be available in Datadog after the pending [PR](https://github.com/DataDog/integrations-extras/pull/2751) is merged by Datadog. Before that, you can manually import the dashboard to Datadog by taking the following steps:

1. Download the JSON file for the new dashboard [here](https://github.com/pingcap/diag/blob/integration/integration/dashboards/datadog-dashboard.json).
2. Log in to [Datadog](https://app.datadoghq.com), click **Dashboards** in the left navigation pane, and then click **+ New Dashboard** in the upper-right corner.
3. In the displayed dialog, click **New Dashboard** to create a new blank dashboard.
4. On the newly created dashboard page, click **Configure** in the upper-right corner, scroll down to the bottom of the displayed pane, and then click **Import dashboard JSON...**.
5. In the displayed dialog, upload the downloaded JSON file to complete the dashboard setup.

</div>
<div label="Datadog integration (Beta)">

1. Log in to [Datadog](https://app.datadoghq.com).
2. Go to the **TiDB Cloud Integration** page ([https://app.datadoghq.com/account/settings#integrations/tidb-cloud](https://app.datadoghq.com/account/settings#integrations/tidb-cloud)) in Datadog.
3. In the **Configuration** tab, click **Install Integration**. The [**TiDB Cloud Cluster Overview**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview) dashboard is displayed in your [**Dashboard List**](https://app.datadoghq.com/dashboard/lists).

</div>
</SimpleTab>

## View the pre-built dashboard

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the **Integrations** page.
2. Depending on your [Datadog integration version](#datadog-integration-version), do one of the following:

    - For Datadog integration (Beta), click the **Dashboard** link in the **Datadog** section.
    - For Datadog integration (Preview), click the **Dashboard** link in the **Datadog** section, and then click **TiDB Cloud Dynamic Tracker** to view the new dashboard with complete metrics.

   >**Note:**
   >
   > For Datadog integration (Preview), note the following:
   >
   > - Before the pending [PR](https://github.com/DataDog/integrations-extras/pull/2751) is merged by Datadog, the **Dashboard** link redirects to the legacy dashboard, which does not include the latest metrics introduced in the preview version.
   > - Once the pending [PR](https://github.com/DataDog/integrations-extras/pull/2751) is merged , the **Dashboard** link in the **Datadog** section will redirect to the new dashboard.

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

For Datadog integration (Preview), the following additional metrics are also available:

| Metric name  | Metric type | Labels | Description                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidbcloud.node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The available disk space in bytes for TiKV/TiFlash nodes |
| tidbcloud.disk_read_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The read latency in seconds per storage device |
| tidbcloud.disk_write_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The write latency in seconds per storage device |
| tidbcloud.kv_request_duration | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv`<br/>cluster_name: `<cluster name>`<br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | The duration in seconds of TiKV requests by type |
| tidbcloud.component_uptime | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tidb\|tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The uptime in seconds of TiDB components |
| tidbcloud.ticdc_owner_checkpoint_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>`| The checkpoint timestamp lag in seconds for changefeed owner. |
| tidbcloud.ticdc_owner_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | The resolved timestamp lag (in seconds) for the changefeed owner. |
| tidbcloud.changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | Changefeed status:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |
| tidbcloud.resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The read request units (RUs) consumed by Resource Manager. |
| tidbcloud.resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The write request units (RUs) consumed by Resource Manager. |
| tidb_cloud.dm_task_state | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | Task State of Data Migration:<br/>0: Invalid<br/>1: New<br/>2: Running<br/>3: Paused<br/>4: Stopped<br/>5: Finished<br/>15: Error |
| tidb_cloud.dm_syncer_replication_lag_bucket | gauge | instance: `instance`<br/>cluster_name: `<cluster name>` | Replicate lag(bucket) of Data Migration |
| tidb_cloud.dm_syncer_replication_lag_gauge | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | Replicate lag(gauge) of Data Migration |
| tidb_cloud.dm_relay_read_error_count | gauge | instance: `instance`<br/>cluster_name: `<cluster name>` | Fail to read binlog from master |
