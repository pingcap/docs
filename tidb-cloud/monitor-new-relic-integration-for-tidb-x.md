---
title: Integrate TiDB Cloud with New Relic (PREVIEW)
summary: Learn how to monitor your TiDB Cloud instances with the New Relic integration.
---

# Integrate TiDB Cloud with New Relic (PREVIEW)

TiDB Cloud supports integration with New Relic. You can configure TiDB Cloud to send metrics for your <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> instances to [New Relic](https://newrelic.com/). After that, you can view these metrics in your New Relic dashboards directly.

## Prerequisites

- To integrate TiDB Cloud with New Relic, you must have a [New Relic](https://newrelic.com/) account and [create a New Relic API key](https://one.newrelic.com/admin-portal/api-keys/home?) of the `Ingest - License` type.

    If you do not have a New Relic account, sign up at [https://newrelic.com/signup](https://newrelic.com/signup).

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner`, `Project Owner`, or `Instance Manager` access in TiDB Cloud. To view the integration page, you need at least the `Project Viewer` or `Instance Viewer` role to access the target <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> instance under your organization in TiDB Cloud.

## Limitations

- New Relic integration is not available for [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) instances.
- New Relic integration is not available when the status of your <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> instance is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.
- When an instance with the New Relic integration is deleted, its associated integration service is also removed.

## Steps

### Step 1. Import the pre-built New Relic dashboard

Currently, the TiDB Cloud dashboard for <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> is not yet available in the New Relic marketplace. Before it is published, you need to manually download and import the dashboard JSON file into New Relic.

1. Download the New Relic dashboard JSON file for your instance type:

    <CustomContent plan="essential">

    - For TiDB Cloud Essential instances created on or after July 1, 2026, download this JSON file: <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-new-relic-integration-tidb-cloud-dynamic-tracker-essential-v2.json>. Note that the `v2` suffix indicates only the version of the dashboard JSON file.
    - For TiDB Cloud Essential instances created before July 1, 2026, download this JSON file: <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-new-relic-integration-tidb-cloud-dynamic-tracker-essential.json>.

    </CustomContent>

    <CustomContent plan="premium">

    <https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-new-relic-integration-tidb-cloud-dynamic-tracker-premium.json>

    </CustomContent>

2. In the JSON file, add your New Relic account ID to all `"accountIds": []` fields.

    For example:

    ```json
    "accountIds": [
      1234567
    ],
    ```

    > **Note:**
    >
    > To avoid integration errors, make sure your account ID is added in all `"accountIds"` fields in the JSON file.

3. Log in to [New Relic](https://one.newrelic.com/), click **Dashboards** in the left navigation bar, and then click **Import dashboard** in the upper-right corner.

4. In the displayed dialog, paste all the content in the prepared JSON file to the text area, and then click **Import dashboard**.

### Step 2. Integrate with your New Relic API key

<CustomContent plan="essential">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .essential }}} instance to go to its overview page.
2. In the left navigation pane, click **Integrations**.
3. On the **Integrations** page, locate the **New Relic** integration and click **Connect**.
4. Enter your New Relic API key, choose the site of New Relic, and then click **Test Integration**.

    - If the test succeeds, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

5. Click **Confirm** to complete the integration.

</CustomContent>

<CustomContent plan="premium">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .premium }}} instance to go to its overview page.
2. In the left navigation pane, click **Settings** > **Integrations**.
3. On the **Integrations** page, locate the **New Relic** integration and click **Connect**.
4. Enter your New Relic API key, choose the site of New Relic, and then click **Test Integration**.

    - If the test succeeds, the **Confirm** button is displayed.
    - If the test fails, an error message is displayed. Follow the message for troubleshooting and retry the integration.

5. Click **Confirm** to complete the integration.

</CustomContent>

## View the pre-built dashboard

To view the pre-built dashboard after the integration, go to **Dashboards** > **Dashboard List** in [New Relic](https://one.newrelic.com/), and then select the dashboard imported in [Step 1](#step-1-import-the-pre-built-new-relic-dashboard). On the dashboard page, you can filter by your target instance name or instance ID, and then view the metrics.

You can also access the **Dashboard List** page in New Relic from the [TiDB Cloud console](https://tidbcloud.com/): go to the **Integrations** page of your target instance, click **New Relic**, and then click **Dashboard**.

## Metrics available to New Relic

New Relic tracks the following metrics for your <CustomContent plan="essential">{{{ .essential }}}</CustomContent><CustomContent plan="premium">{{{ .premium }}}</CustomContent> instance.

<CustomContent plan="essential">

> **Note:**
>
> The `tidb_cloud.cdc_changefeed_*` metrics are available only for TiDB Cloud Essential instances created on or after July 1, 2026.

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of current connections in your TiDB server |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of active connections |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of clients disconnected by connection result |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total time consumed by all SQL statements running in TiDB per second, including the CPU time of all processes and the non-idle waiting time |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of SQL statements executed per second, counted according to statement types |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of error types (such as syntax errors and primary key conflicts) that occur per second when executing SQL statements |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of commands processed by TiDB per second |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of queries that hit the execution plan cache per second |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The duration between the time a network request is sent to TiDB and the time a response is returned to the client |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of transactions executed per second |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The row-based storage size of the {{{ .essential }}} instance in bytes |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The columnar storage size of the {{{ .essential }}} instance in bytes. Returns 0 if TiFlash is not enabled. |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total Request Units/s (RU/s) consumed |
| `tidb_cloud.cdc_changefeed_latency` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The data replication latency between the upstream and the downstream of a changefeed |
| `tidb_cloud.cdc_changefeed_status` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed status:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>

<CustomContent plan="premium">

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidb_cloud.db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of current connections in your TiDB server |
| `tidb_cloud.db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of active connections |
| `tidb_cloud.db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of clients disconnected by connection result |
| `tidb_cloud.db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total time consumed by all SQL statements running in TiDB per second, including the CPU time of all processes and the non-idle waiting time |
| `tidb_cloud.db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of SQL statements executed per second, counted according to statement types |
| `tidb_cloud.db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of error types (such as syntax errors and primary key conflicts) that occur per second when executing SQL statements |
| `tidb_cloud.db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of commands processed by TiDB per second |
| `tidb_cloud.db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of queries that hit the execution plan cache per second |
| `tidb_cloud.db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The duration between the time a network request is sent to TiDB and the time a response is returned to the client |
| `tidb_cloud.db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of transactions executed per second |
| `tidb_cloud.db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The row-based storage size of the {{{ .premium }}} instance in bytes |
| `tidb_cloud.db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The columnar storage size of the {{{ .premium }}} instance in bytes |
| `tidb_cloud.resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total Request Units/s (RU/s) consumed |
| `tidb_cloud.cdc_changefeed_latency` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The data replication latency between the upstream and the downstream of a changefeed |
| `tidb_cloud.cdc_changefeed_status` | gauge | `changefeed_id: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed status:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>
