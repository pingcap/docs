---
title: Integrate TiDB Cloud with Prometheus and Grafana
summary: Learn how to monitor your TiDB cluster with the Prometheus and Grafana integration.
---

# Integrate TiDB Cloud with Prometheus and Grafana

TiDB Cloud provides a [Prometheus](https://prometheus.io/) API endpoint. If you have a Prometheus service, you can monitor key metrics of TiDB Cloud from the endpoint easily.

This document describes how to configure your Prometheus service to read key metrics from the TiDB Cloud endpoint and how to view the metrics using [Grafana](https://grafana.com/).

## Prometheus integration version

TiDB Cloud has supported the project-level Prometheus integration (Beta) since March 15, 2022. Starting from October 21, 2025, TiDB Cloud introduces the cluster-level Prometheus integration (Preview).

- **Cluster-level Prometheus integration (Preview)**: if no legacy project-level Prometheus integration remains undeleted within your organization by October 21, 2025, TiDB Cloud provides the cluster-level Prometheus integration (Preview) for your organization to experience the latest enhancements.

    > **Note**
    >
    > Currently, cluster-level Prometheus integrations (Preview) are available only for TiDB Cloud Dedicated clusters hosted on AWS and Google Cloud.

- **Legacy project-level Prometheus integration (Beta)**: if at least one legacy project-level Prometheus integration remains undeleted within your organization by October 21, 2025, TiDB Cloud retains both existing and new integrations at the project level for your organization to avoid affecting current dashboards.

## Prerequisites

- To integrate TiDB Cloud with Prometheus, you must have a self-hosted or managed Prometheus service.

- To set up third-party metrics integration for TiDB Cloud, you must have the `Organization Owner` or `Project Owner` access in TiDB Cloud. To view the integration page, you need at least the `Project Viewer` role to access the target clusters under your project in TiDB Cloud.

## Limitation

- Prometheus and Grafana integrations now are only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.
- Prometheus and Grafana integrations are not available when the cluster status is **CREATING**, **RESTORING**, **PAUSED**, or **RESUMING**.

## Steps

### Step 1. Get a scrape_config file for Prometheus

Before configuring your Prometheus service to read metrics of TiDB Cloud, you need to generate a `scrape_config` YAML file in TiDB Cloud first. The `scrape_config` file contains a unique bearer token that allows the Prometheus service to monitor your target clusters.

Depending on your [Prometheus integration version](#prometheus-integration-version), the steps to get the `scrape_config` file for Prometheus and access the integration page are different.

<SimpleTab>
<div label="Cluster-level Prometheus integration (Preview)">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Settings** > **Integrations**.
3. On the **Integrations** page, click **Integration to Prometheus (Preview)**.
4. Click **Add File** to generate and show the `scrape_config` file for the current cluster.
5. Make a copy of the `scrape_config` file content for later use.

</div>
<div label="Legacy project-level Prometheus integration (Beta)">

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target project using the combo box in the upper-left corner.
2. In the left navigation pane, click **Project Settings** > **Integrations**.
3. On the **Integrations** page, click **Integration to Prometheus (BETA)**.
4. Click **Add File** to generate and show the scrape_config file for the current project.
5. Make a copy of the `scrape_config` file content for later use.

</div>
</SimpleTab>

> **Note:**
>
> For security reasons, TiDB Cloud only shows a newly generated `scrape_config` file once. Ensure that you copy the content before closing the file window. If you forget to do so, you need to delete the `scrape_config` file in TiDB Cloud and generate a new one. To delete a `scrape_config` file, select the file, click **...**, and then click **Delete**.

### Step 2. Integrate with Prometheus

1. In the monitoring directory specified by your Prometheus service, locate the Prometheus configuration file.

    For example, `/etc/prometheus/prometheus.yml`.

2. In the Prometheus configuration file, locate the `scrape_configs` section, and then copy the `scrape_config` file content obtained from TiDB Cloud to the section.

3. In your Prometheus service, check **Status** > **Targets** to confirm that the new `scrape_config` file has been read. If not, you might need to restart the Prometheus service.

### Step 3. Use Grafana GUI dashboards to visualize the metrics

After your Prometheus service is reading metrics from TiDB Cloud, you can use Grafana GUI dashboards to visualize the metrics as follows:

1. Depending on your [Prometheus integration version](#prometheus-integration-version), the link to download the Grafana dashboard JSON of TiDB Cloud for Prometheus is different.

    - For cluster-level Prometheus integration (Preview), download the Grafana dashboard JSON file [here](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker.json).
    - For legacy project-level Prometheus integration (Beta), download the Grafana dashboard JSON file [here](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json).

2. [Import this JSON to your own Grafana GUI](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard) to visualize the metrics.

    > **Note:**
    >
    > If you are already using Prometheus and Grafana to monitor TiDB Cloud and want to incorporate the newly available metrics, it is recommended that you create a new dashboard instead of directly updating the JSON of the existing one.

3. (Optional) Customize the dashboard as needed by adding or removing panels, changing data sources, and modifying display options.

For more information about how to use Grafana, see [Grafana documentation](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/).

## Best practice of rotating scrape_config

To improve data security, it is a general best practice to periodically rotate `scrape_config` file bearer tokens.

1. Follow [Step 1](#step-1-get-a-scrape_config-file-for-prometheus) to create a new `scrape_config` file for Prometheus.
2. Add the content of the new file to your Prometheus configuration file.
3. Once you have confirmed that your Prometheus service is still able to read from TiDB Cloud, remove the content of the old `scrape_config` file from your Prometheus configuration file.
4. On the **Integrations** page of your project or cluster, delete the corresponding old `scrape_config` file to block anyone else from using it to read from the TiDB Cloud Prometheus endpoint.

## Metrics available to Prometheus

Prometheus tracks the following metric data for your TiDB clusters.

| Metric name |  Metric type  | Labels | Description |
|:--- |:--- |:--- |:--- |
| tidbcloud_db_queries_total| count | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | The total number of statements executed |
| tidbcloud_db_failed_queries_total | count | type: `planner:xxx\|executor:2345\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | The total number of execution errors |
| tidbcloud_db_connections | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | Current number of connections in your TiDB server |
| tidbcloud_db_query_duration_seconds | histogram | sql_type: `Select\|Insert\|...`<br/>cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…`<br/>component: `tidb` | The duration histogram of statements |
| tidbcloud_changefeed_latency | gauge | changefeed_id | The data replication latency between the upstream and the downstream of a changefeed |
| tidbcloud_changefeed_checkpoint_ts | gauge | changefeed_id | The checkpoint timestamp of a changefeed, representing the largest TSO (Timestamp Oracle) successfully written to the downstream |
| tidbcloud_changefeed_replica_rows | gauge | changefeed_id | The number of replicated rows that a changefeed writes to the downstream per second |
| tidbcloud_node_storage_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | The disk usage bytes of TiKV/TiFlash nodes |
| tidbcloud_node_storage_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>component: `tikv\|tiflash` | The disk capacity bytes of TiKV/TiFlash nodes |
| tidbcloud_node_cpu_seconds_total | count | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | The CPU usage of TiDB/TiKV/TiFlash nodes |
| tidbcloud_node_cpu_capacity_cores | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | The CPU limit cores of TiDB/TiKV/TiFlash nodes |
| tidbcloud_node_memory_used_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | The used memory bytes of TiDB/TiKV/TiFlash nodes |
| tidbcloud_node_memory_capacity_bytes | gauge | cluster_name: `<cluster name>`<br/>instance: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>component: `tidb\|tikv\|tiflash` | The memory capacity bytes of TiDB/TiKV/TiFlash nodes |
| tidbcloud_node_storage_available_bytes | gauge | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The available disk space in bytes for TiKV/TiFlash nodes |
| tidbcloud_disk_read_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The read latency in seconds per storage device |
| tidbcloud_disk_write_latency | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv\|tiflash`<br/>cluster_name: `<cluster name>`<br/>`device`: `nvme.*\|dm.*` | The write latency in seconds per storage device |
| tidbcloud_kv_request_duration | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tikv`<br/>cluster_name: `<cluster name>`<br/>`type`: `BatchGet\|Commit\|Prewrite\|...` | The duration in seconds of TiKV requests by type |
| tidbcloud_component_uptime | histogram | instance: `tidb-0\|tidb-1\|...`<br/>component: `tidb\|tikv\|tiflash`<br/>cluster_name: `<cluster name>` | The uptime in seconds of TiDB components |
| tidbcloud_ticdc_owner_resolved_ts_lag | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | The resolved timestamp lag in seconds for changefeed owner |
| tidbcloud_changefeed_status | gauge | changefeed_id: `<changefeed-id>`<br/>cluster_name: `<cluster name>` | Changefeed status:<br/>`-1`: Unknown<br/>`0`: Normal<br/>`1`: Warning<br/>`2`: Failed<br/>`3`: Stopped<br/>`4`: Finished<br/>`6`: Warning<br/>`7`: Other |
| tidbcloud_resource_manager_resource_unit_read_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The read request units consumed by Resource Manager |
| tidbcloud_resource_manager_resource_unit_write_request_unit | gauge | cluster_name: `<cluster name>`<br/>resource_group: `<group-name>` | The write request units consumed by Resource Manager |

For cluster-level Prometheus integration, the following additional metrics are also available:

| Metric name |  Metric type  | Labels | Description |
|:--- |:--- |:--- |:--- |
| tidbcloud_dm_task_status | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | Task state of Data Migration:<br/>0: Invalid<br/>1: New<br/>2: Running<br/>3: Paused<br/>4: Stopped<br/>5: Finished<br/>15: Error |
| tidbcloud_dm_syncer_replication_lag_bucket | gauge | instance: `instance`<br/>cluster_name: `<cluster name>` | Replicate lag (bucket) of Data Migration. |
| tidbcloud_dm_syncer_replication_lag_gauge | gauge | instance: `instance`<br/>task: `task`<br/>cluster_name: `<cluster name>` | Replicate lag (gauge) of Data Migration. |
| tidbcloud_dm_relay_read_error_count | count | instance: `instance`<br/>cluster_name: `<cluster name>` | The number of failed attempts to read binlog from the master. |

## FAQ

- Why does the same metric have different values on Grafana and the TiDB Cloud console at the same time?

    The aggregation calculation logic is different between Grafana and TiDB Cloud, so the displayed aggregated values might differ. You can adjust the `mini step` configuration in Grafana to get more fine-grained metric values.
