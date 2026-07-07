---
title: Integrate TiDB Cloud with Datadog (Preview)
summary: Learn how to monitor your TiDB Cloud instances with the Datadog integration.
---

# Integrate TiDB Cloud with Datadog (Preview)

TiDB Cloud supports Datadog integration. You can configure TiDB Cloud to send metrics about your <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> instances to [Datadog](https://www.datadoghq.com/). After that, you can view these metrics in your Datadog dashboards directly.

## Prerequisites

- To integrate TiDB Cloud with Datadog, you must have a Datadog account and a [Datadog API key](https://app.datadoghq.com/organization-settings/api-keys). Datadog grants you an API key when you first create a Datadog account.

    If you do not have a Datadog account, sign up at [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup).

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner`, `Project Owner` or `Instance Manager` access in TiDB Cloud. To view the integration page, you need at least the `Project Viewer` or `Instance Viewer` role to access the target <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> instance under your Organization in TiDB Cloud.

## Limitation

- Datadog integration is not available for [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) instances.
- Datadog integration is not available when the status of your <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> instance is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

## Steps

### Step 1. Import the pre-built Datadog dashboard

Currently, the TiDB Cloud dashboard for <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> is not yet available in the Datadog integration marketplace. You need to manually download and import the dashboard JSON file into Datadog.

1. Download the Datadog dashboard JSON file for your instance type:

    <CustomContent plan="essential">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-datadog-integration-tidb-cloud-dynamic-tracker-essential.json>

    </CustomContent>

    <CustomContent plan="premium">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-datadog-integration-tidb-cloud-dynamic-tracker-premium.json>

    </CustomContent>

2. Log in to [Datadog](https://app.datadoghq.com), and then go to **Dashboards** > **Dashboard List**.

3. Click **+ New Dashboard** in the upper-right corner. Enter a dashboard name, and then select **Start from blank dashboard**.

4. In the new dashboard, click the gear icon (**Configure**) in the upper-right corner, and then select **Import dashboard JSON...**.

5. In the dialog that appears, paste the JSON content, or drag and drop the JSON file.

6. Click **Yes, Replace** to confirm the import.

### Step 2. Integrate with your Datadog API Key

<CustomContent plan="essential">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .essential }}} instance to go to its overview page.
2. In the left navigation pane, click **Integrations** > **Integration to Datadog(Preview)**.
3. Enter your Datadog API key and choose your Datadog Region.
4. Click **Test Integration**.

    - If the test succeeds, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

5. Click **Confirm** to complete the integration.

</CustomContent>

<CustomContent plan="premium">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .premium }}} instance to go to its overview page.
2. In the left navigation pane, click **Settings** > **Integrations** > **Integration to Datadog(Preview)**.
3. Enter your Datadog API key and choose your Datadog Region.
4. Click **Test Integration**.

    - If the test succeeds, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

5. Click **Confirm** to complete the integration.

</CustomContent>

## View the pre-built dashboard

To view the pre-built dashboard after the integration, go to **Dashboards** > **Dashboard List** in [Datadog](https://app.datadoghq.com), and then select the dashboard imported in [Step 1](#step-1-import-the-pre-built-datadog-dashboard). On the dashboard page, you can filter by your target instance name, and view the metrics.

You can also access the **Dashboard List** page of Datadog from the [TiDB Cloud console](https://tidbcloud.com/): go to the **Integrations** page of your target instance, click **Datadog(Preview)**, and then click **Dashboard**.

## Metrics available to Datadog

Datadog tracks the following metrics for your <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> instance.

<CustomContent plan="essential">

> **Note:**
>
> Currently, the changefeed feature for {{{ .premium }}} is only available upon request, and the `tidb_cloud.changefeed_*` metrics are currently not available.

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of current connections in your TiDB server |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of active connections |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of clients disconnected by connection result |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total time consumed by all SQL statements running in TiDB per second, including the CPU time of all processes and the non-idle waiting time |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of SQL statements executed per second, counted according to statement types |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of error types (for example, syntax errors, primary key conflicts) occurred when executing SQL statements per second |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of commands processed by TiDB per second |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of queries hitting the Execution Plan Cache per second |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The duration between the time a network request is sent to TiDB and returned to the client |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of transactions executed per second |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The row-based storage size of the {{{ .essential }}} instance in bytes |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The columnar storage size of the {{{ .essential }}} instance in bytes. Returns 0 if TiFlash is not enabled. |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total Request Units/s (RU/s) consumed |

</CustomContent>

<CustomContent plan="premium">

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of current connections in your TiDB server |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of active connections |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of clients disconnected by connection result |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total time consumed by all SQL statements running in TiDB per second, including the CPU time of all processes and the non-idle waiting time |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of SQL statements executed per second, counted according to statement types |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of error types (for example, syntax errors, primary key conflicts) occurred when executing SQL statements per second |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of commands processed by TiDB per second |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of queries hitting the Execution Plan Cache per second |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The duration between the time a network request is sent to TiDB and returned to the client |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of transactions executed per second |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The row-based storage size of the {{{ .premium }}} instance in bytes |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The columnar storage size of the {{{ .premium }}} instance in bytes |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total Request Units/s (RU/s) consumed |
| `tidb_cloud.changefeed_latency` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The data replication latency between the upstream and the downstream of a changefeed |
| `tidb_cloud.changefeed_status` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed status:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>
