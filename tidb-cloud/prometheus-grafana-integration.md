---
title: Integrate TiDB Cloud with Prometheus and Grafana (Preview)
summary: Learn how to monitor your TiDB Cloud instances with the Prometheus and Grafana integration.
---

# Integrate TiDB Cloud with Prometheus and Grafana (Preview)

TiDB Cloud provides a [Prometheus](https://prometheus.io/) API endpoint. If you have a Prometheus service, you can monitor key metrics of TiDB Cloud from the endpoint easily.

This document describes how to configure your Prometheus service to read key metrics from the TiDB Cloud endpoint and how to view the metrics using [Grafana](https://grafana.com/).

## Prerequisites

- To integrate TiDB Cloud with Prometheus, you must have a self-hosted or managed Prometheus service.

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` or `Instance Manager` access in TiDB Cloud. To view the integration page, you need at least the `Instance Viewer` role to access the target <CustomContent plan="essential">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent> under your Organization in TiDB Cloud.

## Limitation

<CustomContent plan="essential">

- Prometheus and Grafana integrations now are available for [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) clusters and [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) instances.
- Prometheus and Grafana integrations are not available when the cluster or instance status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

</CustomContent>

<CustomContent plan="premium">

- Prometheus and Grafana integrations now are available for [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) clusters, [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) instances, and [{{{ .premium }}}](https://docs-preview.pingcap.com/tidbcloud/tidb-cloud-intro/#deployment-options) instances.
- Prometheus and Grafana integrations are not available when the cluster or instance status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

</CustomContent>

## Steps

### Step 1. Get a `scrape_config` file for Prometheus

Before configuring your Prometheus service to read metrics of TiDB Cloud, you need to generate a `scrape_config` YAML file in TiDB Cloud first. The `scrape_config` file contains a unique bearer token that allows the Prometheus service to monitor your target <CustomContent plan="essential">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>.

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target <CustomContent plan="essential">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent> to go to its overview page.
2. In the left navigation pane, click **Integrations**>>**Integration to Prometheus**.
3. Click **Add File** to generate and show the `scrape_config` file for the current <CustomContent plan="essential">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>.
4. Make a copy of the `scrape_config` file content for later use.

> **Note:**
>
> - For security reasons, TiDB Cloud only shows a newly generated `scrape_config` file once. Ensure that you copy the content before closing the file window. 
> - If you forget, delete the `scrape_config` file in TiDB Cloud and generate a new one. To delete a `scrape_config` file, select the file, click **...**, and then click **Delete**.

### Step 2. Integrate with Prometheus

1. In the monitoring directory specified by your Prometheus service, locate the Prometheus configuration file.

    For example, `/etc/prometheus/prometheus.yml`.

2. In the Prometheus configuration file, locate the `scrape_configs` section, and then copy the `scrape_config` file content obtained from TiDB Cloud to the section.

3. In your Prometheus service, check **Status** > **Targets** to verify that the new `scrape_config` file has been read. If not, you might need to restart the Prometheus service.

### Step 3. Use Grafana GUI dashboards to visualize the metrics

After your Prometheus service reads metrics from TiDB Cloud, you can use Grafana GUI dashboards to visualize the metrics as follows:

<CustomContent plan="essential">

1. The link to download the Grafana dashboard JSON file of {{{ .essential }}} for Prometheus:[here](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-essential.json).

</CustomContent>

<CustomContent plan="premium">

1. The link to download the Grafana dashboard JSON file of {{{ .premium }}} for Prometheus:[here](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-premium.json).

</CustomContent>

2. [Import this JSON to your own Grafana GUI](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard) to visualize the metrics.

    > **Note:**
    >
    > If you are already using Prometheus and Grafana to monitor <CustomContent plan="essential">clusters</CustomContent><CustomContent plan="premium">instances</CustomContent> and want to incorporate the newly available metrics, it is recommended that you create a new dashboard instead of directly updating the JSON of the existing one.

3. (Optional) Customize the dashboard as needed by adding or removing panels, changing data sources, and modifying display options.

For more information about how to use Grafana, see [Grafana documentation](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/).

## Best practice of rotating `scrape_config`

To improve data security, periodically rotate `scrape_config` file bearer tokens.

1. Follow [Step 1](#step-1-get-a-scrape_config-file-for-prometheus) to create a new `scrape_config` file for Prometheus.
2. Add the content of the new file to your Prometheus configuration file.
3. Once you confirm that your Prometheus service can read from TiDB Cloud, remove the content of the old `scrape_config` file from your Prometheus configuration file.
4. On the **Integrations** page of your <CustomContent plan="essential">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>, delete the corresponding old `scrape_config` file to block anyone else from using it to read from the TiDB Cloud Prometheus endpoint.

## Metrics available to Prometheus

Prometheus tracks the following metric data for your <CustomContent plan="essential">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>. 

<CustomContent plan="essential">

> **Note:**
>
> {{{ .essential }}} does not support TiCDC components, so the `tidbcloud_changefeed_*` metrics are not available.

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidbcloud_db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of current connections in your TiDB server |
| `tidbcloud_db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of active connections |
| `tidbcloud_db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of clients disconnected by connection result |
| `tidbcloud_db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | A time model statistic that represents the sum of all process's CPU consumption plus the sum of non-idle wait time |
| `tidbcloud_db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of SQL statements executed per second, counted according to statement types |
| `tidbcloud_db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of error types (e.g., syntax errors, primary key conflicts) occurred when executing SQL statements per second |
| `tidbcloud_db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of commands processed by TiDB per second |
| `tidbcloud_db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of queries hitting the Execution Plan Cache per second |
| `tidbcloud_db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The duration between the time a network request is sent to TiDB and returned to the client |
| `tidbcloud_db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of transactions executed per second |
| `tidbcloud_db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The row-based (TiKV) storage size of the cluster in bytes |
| `tidbcloud_db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The columnar (TiFlash) storage size of the cluster in bytes. Returns 0 if TiFlash is not enabled. |
| `tidbcloud_resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total Resource Units (RU) consumed (Combined Read and Write RUs) |

</CustomContent>

<CustomContent plan="premium">

| Metric name | Metric type | Labels | Description |
|:--- |:--- |:--- |:--- |
| `tidbcloud_db_total_connection` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of current connections in your TiDB server |
| `tidbcloud_db_active_connections` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of active connections |
| `tidbcloud_db_disconnections` | gauge | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of clients disconnected by connection result |
| `tidbcloud_db_database_time` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | A time model statistic that represents the sum of all process's CPU consumption plus the sum of non-idle wait time |
| `tidbcloud_db_query_per_second` | gauge | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of SQL statements executed per second, counted according to statement types |
| `tidbcloud_db_failed_queries` | gauge | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of error types (e.g., syntax errors, primary key conflicts) occurred when executing SQL statements per second |
| `tidbcloud_db_command_per_second` | gauge | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of commands processed by TiDB per second |
| `tidbcloud_db_queries_using_plan_cache_ops` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The statistics of queries hitting the Execution Plan Cache per second |
| `tidbcloud_db_average_query_duration` | gauge | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The duration between the time a network request is sent to TiDB and returned to the client |
| `tidbcloud_db_transaction_per_second` | gauge | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The number of transactions executed per second |
| `tidbcloud_db_row_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The row-based (TiKV) storage size of the cluster in bytes |
| `tidbcloud_db_columnar_storage_used_bytes` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The columnar (TiFlash) storage size of the cluster in bytes. Returns 0 if TiFlash is not enabled. |
| `tidbcloud_resource_manager_resource_request_unit_total` | gauge | `instance_id: <instance id>`<br/>`instance_name: <instance name>` | The total Resource Units (RU) consumed (Combined Read and Write RUs) |
| `tidbcloud_changefeed_latency` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | The data replication latency between the upstream and the downstream of a changefeed |
| `tidbcloud_changefeed_status` | gauge | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | Changefeed status:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |

</CustomContent>

## FAQ

- Why does the same metric have different values on Grafana and the TiDB Cloud console at the same time?

    Grafana and TiDB Cloud use different aggregation calculation logic, so the displayed aggregated values might differ. You can adjust the `mini step` configuration in Grafana to get more fine-grained metric values.
