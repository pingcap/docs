---
title: Integrate TiDB Cloud with New Relic
summary: Learn how to monitor your TiDB cluster with the New Relic integration.
---

# Integrate TiDB Cloud with New Relic

TiDB Cloud supports New Relic integration. You can configure TiDB Cloud to send metrics of your TiDB clusters to [New Relic](https://newrelic.com/). After that, you can directly view these metrics in your New Relic dashboards.

## New Relic integration version

TiDB Cloud has supported the project-level New Relic integration (Beta) since April 11, 2023. Starting from July 31, 2025, TiDB Cloud introduces the cluster-level New Relic integration (Preview). Starting from September 30, 2025, the cluster-level New Relic integration becomes generally available (GA).

- **Cluster-level New Relic integration**: if no legacy project-level Datadog or New Relic integration remains undeleted within your organization by July 31, 2025, TiDB Cloud provides the cluster-level New Relic integration for your organization to experience the latest enhancements.
- **Legacy project-level New Relic integration (Beta)**: if at least one legacy project-level Datadog or New Relic integration remains undeleted within your organization by July 31, 2025, TiDB Cloud retains both existing and new integrations at the project level for your organization to avoid affecting current dashboards. Note that the legacy project-level New Relic integrations will be deprecated on October 31, 2025. If your organization is still using these legacy integrations, follow [Migrate Datadog and New Relic Integrations](/tidb-cloud/migrate-metrics-integrations.md) to migrate to the new cluster-level integrations and minimize disruptions to your metrics-related services.

## Prerequisites

- To integrate TiDB Cloud with New Relic, you must have a [New Relic](https://newrelic.com/) account and [create a New Relic API key](https://one.newrelic.com/admin-portal/api-keys/home?) of the `Ingest - License` type.

    If you do not have a New Relic account, sign up [here](https://newrelic.com/signup).

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` or `Project Owner` access in TiDB Cloud. To view the integration page or access configured dashboards via the provided links, you need at least the `Project Viewer` role to access the target clusters under your project in TiDB Cloud.

## Limitation

- New Relic integrations now are only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

- New Relic integrations are not available when the cluster status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

- When a cluster with New Relic integration is deleted, its associated integration services are also removed.

## Steps

### Step 1. Integrate with your New Relic API Key

Depending on your [New Relic integration version](#new-relic-integration-version), the steps to access the integration page are different.

<SimpleTab>
<div label="Cluster-level New Relic integration">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Settings** > **Integrations**.
3. On the **Integrations** page, click **Integration to New Relic**.
4. Enter your API key of New Relic and choose the site of New Relic.
5. Click **Test Integration**.

    - If the test succeeds, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

6. Click **Confirm** to complete the integration.

</div>
<div label="Legacy project-level New Relic integration (Beta)">

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Integrations**.
3. On the **Integrations** page, click **Integration to New Relic (BETA)**.
4. Enter your API key of New Relic and choose the site of New Relic.
5. Click **Test Integration**.

    - If the test succeeds, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

6. Click **Confirm** to complete the integration.

</div>
</SimpleTab>

### Step 2. Add TiDB Cloud dashboard in New Relic

Depending on your [New Relic integration version](#new-relic-integration-version), the steps are different.

<SimpleTab>
<div label="Cluster-level New Relic integration">

A new TiDB Cloud dashboard will be available in New Relic after the pending [PR](https://github.com/newrelic/newrelic-quickstarts/pull/2681) is merged by New Relic. Before that, you can manually import the dashboard to New Relic by taking the following steps:

1. Prepare the JSON file for the new dashboard.

    1. Download the template JSON file [here](https://github.com/pingcap/diag/blob/integration/integration/dashboards/newrelic-dashboard.json).
    2. In the JSON file, add `"permissions": "PUBLIC_READ_WRITE"` to line 4 as follows:

        ```json
        {
          "name": "TiDB Cloud Dynamic Tracker",
          "description": null,
          "permissions": "PUBLIC_READ_WRITE",
          ...
        }
        ```

    3. Add your New Relic account ID to all `"accountIds": []` fields in the JSON file.

        For example:

        ```json
        "accountIds": [
          1234567
        ],
        ```

        > **Note**:
        >
        > To avoid integration errors, make sure your account ID is added in all `"accountIds"` fields in the JSON file.

2. Log in to [New Relic](https://one.newrelic.com/), click **Dashboards** in the left navigation bar, and then click **Import dashboard** in the upper-right corner.
3. In the displayed dialog, paste all the content in the prepared JSON file to the text area, and then click **Import dashboard**.

</div>
<div label="Legacy project-level New Relic integration (Beta)">

1. Log in to [New Relic](https://one.newrelic.com/).
2. Click **Add Data**, search for `TiDB Cloud`, and then go to the **TiDB Cloud Monitoring** page. Alternatively, you can click the [link](https://one.newrelic.com/marketplace?state=79bf274b-0c01-7960-c85c-3046ca96568e) to directly access the page.
3. Choose your account ID and create the dashboard in New Relic.

</div>
</SimpleTab>

## View the pre-built dashboard

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the **Integrations** page.

2. Click the **Dashboard** link in the **New Relic** section to view the pre-built dashboard of your TiDB clusters.

3. Depending on your [New Relic integration version](#new-relic-integration-version), do one of the following:

    - For cluster-level New Relic integration, click **TiDB Cloud Dynamic Tracker** to view the new dashboard.
    - For legacy project-level New Relic integration (Beta), click **TiDB Cloud Monitoring** to view the legacy dashboard.

## Metrics available to New Relic

New Relic tracks the following metrics for your TiDB clusters.

| Metric name  | Metric type | Labels | Description                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidb_cloud.db_database_time| gauge | sql_type: Select\|Insert\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The total time consumed by all SQL statements running in TiDB per second, including the CPU time of all processes and the non-idle waiting time. |
| tidb_cloud.db_query_per_second| gauge | type: Select\|Insert\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The number of SQL statements executed per second on all TiDB instances, which is counted according to `SELECT`, `INSERT`, `UPDATE`, and other types of statements. |
| tidb_cloud.db_average_query_duration| gauge | sql_type: Select\|Insert\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The duration between the time that the client's network request is sent to TiDB and the time that the request is returned to the client after TiDB has executed it. |
| tidb_cloud.db_failed_queries| gauge | type: executor:xxxx\|parser:xxxx\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The statistics of error types (such as syntax errors and primary key conflicts) according to the SQL execution errors that occur per second on each TiDB instance. |
| tidb_cloud.db_total_connection| gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The number of current connections in your TiDB server. |
| tidb_cloud.db_active_connections| gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The number of active connections. |
| tidb_cloud.db_disconnections| gauge | result: ok\|error\|undetermined<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The number of disconnected clients. |
| tidb_cloud.db_command_per_second| gauge | type: Query\|StmtPrepare\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The number of commands processed by TiDB per second, which is classified according to the success or failure of command execution results. |
| tidb_cloud.db_queries_using_plan_cache_ops| gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The statistics of queries using [Plan Cache](/sql-prepared-plan-cache.md) per second. The execution plan cache only supports the prepared statement command. |
| tidb_cloud.db_transaction_per_second| gauge | txn_mode: pessimistic\|optimistic<br/><br/>type: abort\|commit\|...<br/><br/>cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…<br/><br/>component: `tidb` | The number of transactions executed per second. |
| tidb_cloud.node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/><br/>component: tikv\|tiflash | The disk usage of TiKV/TiFlash nodes, in bytes. |
| tidb_cloud.node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…<br/><br/>component: tikv\|tiflash | The disk capacity of TiKV/TiFlash nodes, in bytes. |
| tidb_cloud.node_cpu_seconds_total (Beta only) | count | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The CPU usage of TiDB/TiKV/TiFlash nodes. |
| tidb_cloud.node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The limit on CPU cores of TiDB/TiKV/TiFlash nodes. |
| tidb_cloud.node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The used memory of TiDB/TiKV/TiFlash nodes, in bytes. |
| tidb_cloud.node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The memory capacity of TiDB/TiKV/TiFlash nodes, in bytes. |

For cluster-level New Relic integrations, the following additional metrics are also available:

| Metric name  | Metric type | Labels | Description                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidb_cloud.node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tikv\|tiflash`<br/><br/>cluster_name: `<cluster name>` | The available disk space in bytes for TiKV or TiFlash nodes. |
| tidb_cloud.node_disk_read_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tikv\|tiflash`<br/><br/>cluster_name: `<cluster name>`<br/><br/>`device`: `nvme.*\|dm.*` | The read latency (in seconds) per storage device. |
| tidb_cloud.node_disk_write_latency | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tikv\|tiflash`<br/><br/>cluster_name: `<cluster name>`<br/><br/>`device`: `nvme.*\|dm.*` | The write latency (in seconds) per storage device. |
| tidb_cloud.db_kv_request_duration | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tikv`<br/><br/>cluster_name: `<cluster name>`<br/><br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | The duration (in seconds) of TiKV requests by type. |
| tidb_cloud.db_component_uptime | gauge | instance: `tidb-0\|tidb-1\|...`<br/><br/>component: `tidb\|tikv\|tiflash`<br/><br/>cluster_name: `<cluster name>` | The uptime (in seconds) of TiDB components. |
| tidb_cloud.cdc_changefeed_latency (AKA cdc_changefeed_checkpoint_ts_lag) | gauge | changefeed_id: `<changefeed-id>`<br/><br/>cluster_name: `<cluster name>`| The checkpoint timestamp lag (in seconds) for changefeed owner. |
| tidb_cloud.cdc_changefeed_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/><br/>cluster_name: `<cluster name>` | The resolved timestamp lag (in seconds) for the changefeed owner. |
| tidb_cloud.cdc_changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/><br/>cluster_name: `<cluster name>` | Changefeed status:<br/><br/>`-1`: Unknown<br/><br/>`0`: Normal<br/><br/>`1`: Warning<br/><br/>`2`: Failed<br/><br/>`3`: Stopped<br/><br/>`4`: Finished<br/><br/>`6`: Warning<br/><br/>`7`: Other |
| tidb_cloud.resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/><br/>resource_group: `<group-name>` | The read request units (RUs) consumed by Resource Manager. |
| tidb_cloud.resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/><br/>resource_group: `<group-name>` | The write request units (RUs) consumed by Resource Manager. |
| tidb_cloud.dm_task_state | gauge | instance: `instance`<br/><br/>task: `task`<br/><br/>cluster_name: `<cluster name>` | Task State of Data Migration:<br/><br/>`0`: Invalid<br/><br/>`1`: New<br/><br/>`2`: Running<br/><br/>`3`: Paused<br/><br/>`4`: Stopped<br/><br/>`5`: Finished<br/><br/>`15`: Error |
| tidb_cloud.dm_syncer_replication_lag_bucket | gauge | instance: `instance`<br/><br/>cluster_name: `<cluster name>` | Replicate lag (bucket) of Data Migration. |
| tidb_cloud.dm_syncer_replication_lag_gauge | gauge | instance: `instance`<br/><br/>task: `task`<br/><br/>cluster_name: `<cluster name>` | Replicate lag (gauge) of Data Migration. |
| tidb_cloud.dm_relay_read_error_count | gauge | instance: `instance`<br/><br/>cluster_name: `<cluster name>` | Fail to read binlog from master. |
| tidb_cloud.node_memory_available_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The available memory of TiDB/TiKV/TiFlash nodes, in bytes. |
| tidb_cloud.cdc_changefeed_replica_rows | gauge | changefeed_id: `<changefeed-id>`<br/><br/>cluster_name: `<cluster name>` | The number of events that TiCDC nodes write to the downstream per second. |
| tidb_cloud.node_cpu_seconds_total_rate | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The CPU usage of TiDB/TiKV/TiFlash nodes. |
