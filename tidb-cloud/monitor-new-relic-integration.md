---
title: Integrate TiDB Cloud with New Relic (Preview)
summary: Learn how to monitor your TiDB cluster with the New Relic integration.
---

# Integrate TiDB Cloud with New Relic (Preview)

TiDB Cloud supports New Relic integration (Preview). You can configure TiDB Cloud to send metrics of your TiDB clusters to [New Relic](https://newrelic.com/). After that, you can directly view these metrics in your New Relic dashboards.

## New Relic integration version

Based on your integration history, TiDB Cloud provides two versions of New Relic integration:

- **New Relic integration (Preview)**: if none of clusters in your organization were integrated with New Relic before July 29, 2025, TiDB Cloud provides the preview version of New Relic integration for you to experience the latest enhancements.
- **New Relic integration (Beta)**: if any clusters in your organization were integrated with New Relic before July 29, 2025, TiDB Cloud keeps both existing and new integrations at the beta version to avoid affecting current dashboards.

## Prerequisites

- To integrate TiDB Cloud with New Relic, you must have a New Relic account and a [New Relic API key](https://one.newrelic.com/admin-portal/api-keys/home?). New Relic grants you an API key when you first create a New Relic account.

    If you do not have a New Relic account, sign up [here](https://newrelic.com/signup).

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` access to your organization in TiDB Cloud. To view the integration page or access configured dashboards via the provided links, users only need the `Organization Member` access to your organization in TiDB Cloud.

## Limitation

- You cannot use the New Relic integration in [TiDB Cloud Serverless clusters](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless).

- New Relic integrations are not available when the cluster status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

## Steps

### Step 1. Integrate with your New Relic API Key

Depending on your [New Relic integration version](#new-relic-integration-version), the steps to access the integration page are different.

<SimpleTab>
<div label="New Relic integration (Preview)">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Settings** > **Integrations**.
3. On the **Integrations** page, click **Integration to New Relic (Preview)**.
4. Enter your API key of New Relic and choose the site of New Relic.
5. Click **Test Integration**.

    - If the test succeeds, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

6. Click **Confirm** to complete the integration.

</div>
<div label="New Relic integration (Beta)">

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

### Step 2. Add TiDB Cloud Dashboard in New Relic

1. Log in to [New Relic](https://one.newrelic.com/).
2. Click **Add Data**, search for `TiDB Cloud`, and then go to the **TiDB Cloud Monitoring** page. Alternatively, you can click the [link](https://one.newrelic.com/marketplace?state=79bf274b-0c01-7960-c85c-3046ca96568e) to directly access the page.
3. Choose your account ID and create the dashboard in New Relic.

## Pre-built dashboard

Click the **Dashboard** link in the **New Relic** card on the **Integrations** page. You can see the pre-built dashboard of your TiDB clusters.

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
| tidb_cloud.node_cpu_seconds_total | count | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The CPU usage of TiDB/TiKV/TiFlash nodes. |
| tidb_cloud.node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The limit on CPU cores of TiDB/TiKV/TiFlash nodes. |
| tidb_cloud.node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The used memory of TiDB/TiKV/TiFlash nodes, in bytes. |
| tidb_cloud.node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/><br/>instance: tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…<br/><br/>component: tidb\|tikv\|tiflash | The memory capacity of TiDB/TiKV/TiFlash nodes, in bytes. |

For New Relic integration (Preview), the following additional metrics are also available:

| Metric name  | Metric type | Labels | Description                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidbcloud.node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The available disk space in bytes for TiKV or TiFlash nodes. |
| tidbcloud.disk_read_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The read latency (in seconds) per storage device. |
| tidbcloud.disk_write_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The write latency (in seconds) per storage device. |
| tidbcloud.kv_request_duration | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv`<br/>cluster_name: `<cluster name>`<br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | The duration (in seconds) of TiKV requests by type |
| tidbcloud.component_uptime | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tidb\|tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The uptime (in seconds) of TiDB components |
| tidbcloud.changefeed_checkpoint_ts | gauge | changefeed_id | The checkpoint timestamp of a changefeed, representing the latest TSO (Timestamp Oracle) successfully written to the downstream. |
| tidbcloud.ticdc_owner_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | The resolved timestamp lag (in seconds) for the changefeed owner. |
| tidbcloud.changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | Changefeed status:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |
| tidbcloud.resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The read request units (RUs) consumed by Resource Manager. |
| tidbcloud.resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The write request units (RUs) consumed by Resource Manager. |
