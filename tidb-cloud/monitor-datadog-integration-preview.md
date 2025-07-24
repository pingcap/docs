---
title: Integrate TiDB Cloud with Datadog (Preview)
summary: Learn how to monitor your TiDB cluster with the Datadog integration.
---

# Integrate TiDB Cloud with Datadog (Preview)

TiDB Cloud supports Datadog integration (Preview). You can configure TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/). After that, you can view these metrics in your Datadog dashboards directly.

## Prerequisites

- To integrate TiDB Cloud with Datadog, you must have a Datadog account and a [Datadog API key](https://app.datadoghq.com/organization-settings/api-keys). Datadog grants you an API key when you first create a Datadog account.

    If you do not have a Datadog account, sign up at [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup).

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` access to your organization in TiDB Cloud, while other users have read-only access to the integration page and can access configured dashboards via the provided links.

## Limitation

- You cannot use the Datadog integration in [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters.

- Datadog integrations are not available when the cluster status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

## Steps

### Step 1. Integrate with your Datadog API Key

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the target cluster by clicking on it from the cluster list page.
2. After entering the target cluster details page, in the left navigation pane, click **Settings** > **Integrations**.
3. On the **Integrations** page, click **Integration to Datadog (Preview)**.
4. Enter your Datadog API key and choose your Datadog site.
5. Click **Test Integration**.

    - If the test successes, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

6. Click **Confirm** to complete the integration.

### Step 2. Install TiDB Cloud Integration in Datadog

1. Log in to [Datadog](https://app.datadoghq.com).
2. Go to the **TiDB Cloud Integration** page ([https://app.datadoghq.com/account/settings#integrations/tidb-cloud](https://app.datadoghq.com/account/settings#integrations/tidb-cloud)) in Datadog.
3. In the **Configuration** tab, click **Install Integration**. The [**TiDBCloud Cluster Overview**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview) dashboard is displayed in your [**Dashboard List**](https://app.datadoghq.com/dashboard/lists).

## Pre-built dashboard

Click the **Dashboard** link in the **Datadog** card of the integrations. You can see the pre-built dashboard of your TiDB clusters.

## Metrics available to Datadog

Datadog tracks the following metric data for your TiDB clusters.

| Metric name  | Metric type | Labels | Description                                   |
| :------------| :---------- | :------| :----------------------------------------------------- |
| tidb_cloud.db_database_time| gauge | sql_type: Select\|Insert\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The total time consumed by all SQL statements running in TiDB per second, including the CPU time of all processes and the non-idle waiting time. |
| tidb_cloud.db_query_per_second| gauge | type: Select\|Insert\|...<br/>cluster_name: `<cluster name>`<br/>instance: tidb-0\|tidb-1…<br/>component: `tidb` | The number of SQL statements executed per second on all TiDB instances, which is counted according to SELECT, INSERT, UPDATE, and other types of statements. |
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
| tidbcloud.node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The available disk space in bytes for TiKV/TiFlash nodes |
| tidbcloud.disk_read_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The read latency in seconds per storage device |
| tidbcloud.disk_write_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The write latency in seconds per storage device |
| tidbcloud.kv_request_duration | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv`<br/>cluster_name: `<cluster name>`<br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | The duration in seconds of TiKV requests by type |
| tidbcloud.component_uptime | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tidb\|tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The uptime in seconds of TiDB components |
| tidbcloud.changefeed_checkpoint_ts | gauge | changefeed_id | The checkpoint timestamp of a changefeed, representing the largest TSO (Timestamp Oracle) successfully written to the downstream |
| tidbcloud.ticdc_owner_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | The resolved timestamp lag in seconds for changefeed owner |
| tidbcloud.changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | Changefeed status:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |
| tidbcloud.resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The read request units consumed by Resource Manager |
| tidbcloud.resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The write request units consumed by Resource Manager |
