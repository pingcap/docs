---
title: TiDB Cloud Release Notes in 2023
summary: Learn about the release notes of TiDB Cloud in 2023.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2023

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2023.

## January 4, 2023

**General changes**

- Support scaling up TiDB, TiKV, and TiFlash nodes by increasing the **Node Size(vCPU + RAM)** for TiDB Dedicated Tier clusters hosted on AWS and created after December 31, 2022.

    You can increase the node size [using the TiDB Cloud console](/tidb-cloud/scale-tidb-cluster.md#increase-node-size) or [using the TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster).

- Extend the metrics retention period on the [**Monitoring**](/tidb-cloud/built-in-monitoring.md) page to 2 days.

    Now you are able to access and analyze metrics data from the past 2 days, giving you more flexibility and visibility into your cluster performance and trends.

    This feature is available at no extra cost and can be accessed on the **Diagnosis** tab of the [**Monitoring**](/tidb-cloud/built-in-monitoring.md) page for your cluster, which helps you identify and troubleshoot performance issues and monitor the overall health of your cluster more effectively.

- Support customizing Grafana dashboard JSON for Prometheus integration.

  If you have [integrated TiDB Cloud with Prometheus](/tidb-cloud/monitor-prometheus-and-grafana-integration.md), you can now import a pre-built Grafana dashboard that is designed for monitoring TiDB Cloud clusters and customize the dashboard to your needs, which helps you monitor your TiDB Cloud clusters easier and quickly identify any performance issues.

  For more information, see [Use Grafana GUI dashboards to visualize the metrics](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics).

**Console changes**

- Simplify the display of the [**Clusters**](https://tidbcloud.com/console/clusters) page and cluster overview page.

    - You can click the cluster name on the [**Clusters**](https://tidbcloud.com/console/clusters) page to enter the cluster overview page and start operating the cluster.
    - Remove the **Connection** pane from the cluster overview page. You can click **Connect** in the upper-right corner to get the connection information.
    - Remove the **Import** pane from the cluster overview page. You can click **Import** in the left navigation pane to import data.

- Introduce Chat2Query (beta), an AI-powered SQL editor for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters.

  In Chat2Query (previously named as SQL editor), you can either let AI generate SQL queries automatically or write SQL queries manually using the pre-built sample dataset, and run SQL queries against databases without a terminal.

  To access Chat2Query, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click your cluster name, and then click **Chat2Query** in the left navigation pane.