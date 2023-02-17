---
title: TiDB Cloud Release Notes in 2023
summary: Learn about the release notes of TiDB Cloud in 2023.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2023

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2023.

## February 17, 2023

**CLI changes**

- Add new command [`ticloud connect`](/tidb-cloud/ticloud-connect.md)

    `ticloud connect` is a command that allows you to connect to a TiDB Cloud cluster from your local machine. You can use `ticloud connect` to connect to a TiDB Cloud cluster and execute SQL statements.

## February 2, 2023

**CLI changes**

- Introduce the TiDB Cloud CLI client [`ticloud`](/tidb-cloud/cli-reference.md).

    Using `ticloud`, you can easily manage your TiDB Cloud resources from a terminal or other automatic workflows with a few lines of commands. Especially for GitHub Actions, we have provided [`setup-tidbcloud-cli`](https://github.com/marketplace/actions/set-up-tidbcloud-cli) for you to easily set up `ticloud`.

    For more information, see [TiDB Cloud CLI Quick Start](/tidb-cloud/get-started-with-cli.md) and [TiDB Cloud CLI Reference](/tidb-cloud/cli-reference.md).

## January 18, 2023

**General changes**

* Support [signing up](https://tidbcloud.com/free-trial) TiDB Cloud with a Microsoft account.

## January 17, 2023

**General changes**

- Upgrade the default TiDB version of new [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters from [v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3) to [v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0).

- For new sign-up users, TiDB Cloud will automatically create a free [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) cluster so that you can quickly start a data exploration journey with TiDB Cloud.

- Support a new AWS region for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters: `Seoul (ap-northeast-2)`.

    The following features are enabled for this region:

    - [Migrate MySQL-compatible databases to TiDB Cloud using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    - [Stream data from TiDB Cloud to other data services using changefeed](/tidb-cloud/changefeed-overview.md)
    - [Back up and restore TiDB cluster data](/tidb-cloud/backup-and-restore.md)

## January 10, 2023

**General changes**

- Optimize the feature of importing data from local CSV files to TiDB to improve the user experience for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters.

    - To upload a CSV file, now you can simply drag and drop it to the upload area on the **Import** page.
    - When creating an import task, if your target database or table does not exist, you can enter a name to let TiDB Cloud create it for you automatically. For the target table to be created, you can specify a primary key or select multiple fields to form a composite primary key.
    - After the import is completed, you can explore your data with [AI-powered Chat2Query](/tidb-cloud/explore-data-with-chat2query.md) by clicking **Explore your data by Chat2Query** or clicking the target table name in the task list.

  For more information, see [Import local files to TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md).

**Console changes**

- Add the **Get Support** option for each cluster to simplify the process of requesting support for a specific cluster.

    You can request support for a cluster in either of the following ways:

    - On the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click **...** in the row of your cluster and select **Get Support**.
    - On your cluster overview page, click **...** in the upper-right corner and select **Get Support**.

## January 5, 2023

**Console changes**

- Rename SQL Editor (beta) to Chat2Query (beta) for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters and support generating SQL queries using AI.

  In Chat2Query, you can either let AI generate SQL queries automatically or write SQL queries manually, and run SQL queries against databases without a terminal.

  To access Chat2Query, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click your cluster name, and then click **Chat2Query** in the left navigation pane.

## January 4, 2023

**General changes**

- Support scaling up TiDB, TiKV, and TiFlash nodes by increasing the **Node Size(vCPU + RAM)** for TiDB Dedicated Tier clusters hosted on AWS and created after December 31, 2022.

    You can increase the node size [using the TiDB Cloud console](/tidb-cloud/scale-tidb-cluster.md#increase-node-size) or [using the TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster).

- Extend the metrics retention period on the [**Monitoring**](/tidb-cloud/built-in-monitoring.md) page to two days.

    Now you have access to metrics data of the last two days, giving you more flexibility and visibility into your cluster performance and trends.

    This improvement comes at no additional cost and can be accessed on the **Diagnosis** tab of the [**Monitoring**](/tidb-cloud/built-in-monitoring.md) page for your cluster. This will help you identify and troubleshoot performance issues and monitor the overall health of your cluster more effectively.

- Support customizing Grafana dashboard JSON for Prometheus integration.

    If you have [integrated TiDB Cloud with Prometheus](/tidb-cloud/monitor-prometheus-and-grafana-integration.md), you can now import a pre-built Grafana dashboard to monitor TiDB Cloud clusters and customize the dashboard to your needs. This feature enables easy and fast monitoring of your TiDB Cloud clusters and helps you identify any performance issues quickly.

    For more information, see [Use Grafana GUI dashboards to visualize the metrics](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics).

- Upgrade the default TiDB version of all [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters from [v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0) to [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0). The cold start issue after upgrading the default TiDB version of Serverless Tier clusters to v6.4.0 has been resolved.

**Console changes**

- Simplify the display of the [**Clusters**](https://tidbcloud.com/console/clusters) page and the cluster overview page.

    - You can click the cluster name on the [**Clusters**](https://tidbcloud.com/console/clusters) page to enter the cluster overview page and start operating the cluster.
    - Remove the **Connection** and **Import** panes from the cluster overview page. You can click **Connect** in the upper-right corner to get the connection information and click **Import** in the left navigation pane to import data.
