---
title: TiDB Cloud Release Notes in 2023
summary: Learn about the release notes of TiDB Cloud in 2023.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2023

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2023.

## April 4, 2023

**General changes**

- Remove the following two alerts from [TiDB Cloud built-in alerts](/tidb-cloud/monitor-built-in-alerting.md#tidb-cloud-built-in-alert-conditions) to prevent false positives. This is because temporary offline or out-of-memory (OOM) issues on one of the nodes do not significantly affect the overall health of a cluster.

    - At least one TiDB node in the cluster has run out of memory.
    - One or more cluster nodes are offline.

**Console changes**

- Introduce the [Alerts](/tidb-cloud/monitor-built-in-alerting.md) page for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters, which provides both active and closed alerts for each Dedicated Tier cluster.

    The **Alerts** page provides the following:

    - An intuitive and user-friendly user interface. You can view alerts for your clusters on this page even if you have not subscribed to the alert notification emails.
    - Advanced filtering options to help you quickly find and sort alerts based on their severity, status, and other attributes. It also allows you to view the historical data for the last 7 days, which eases the alert history tracking.
    - The **Edit Rule** feature. You can customize alert rule settings to meet your cluster's specific needs.

  For more information, see [TiDB Cloud built-in alerts](/tidb-cloud/monitor-built-in-alerting.md).

- Consolidate the help-related information and actions of TiDB Cloud into a single place.

    Now, you can get all the [TiDB Cloud help information](/tidb-cloud/tidb-cloud-support.md#get-help-information) and contact support by clicking **?** in the lower-right corner of the TiDB Cloud console.

- Introduce the [Getting Started](https://tidbcloud.com/console/getting-started) page to help you learn about TiDB Cloud.

    The **Getting Started** page provides you with interactive tutorials, essential guides, and useful links. By following interactive tutorials, you can easily explore TiDB Cloud features and HTAP capabilities with pre-built industry-specific datasets (Steam Game Dataset and S&P 500 Dataset).

    To access the **Getting Started** page, click <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.9998L9 11.9998M12 14.9998C13.3968 14.4685 14.7369 13.7985 16 12.9998M12 14.9998V19.9998C12 19.9998 15.03 19.4498 16 17.9998C17.08 16.3798 16 12.9998 16 12.9998M9 11.9998C9.53214 10.6192 10.2022 9.29582 11 8.04976C12.1652 6.18675 13.7876 4.65281 15.713 3.59385C17.6384 2.53489 19.8027 1.98613 22 1.99976C22 4.71976 21.22 9.49976 16 12.9998M9 11.9998H4C4 11.9998 4.55 8.96976 6 7.99976C7.62 6.91976 11 7.99976 11 7.99976M4.5 16.4998C3 17.7598 2.5 21.4998 2.5 21.4998C2.5 21.4998 6.24 20.9998 7.5 19.4998C8.21 18.6598 8.2 17.3698 7.41 16.5898C7.02131 16.2188 6.50929 16.0044 5.97223 15.9878C5.43516 15.9712 4.91088 16.1535 4.5 16.4998Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Getting Started** in the left navigation bar of the [TiDB Cloud console](https://tidbcloud.com/). On this page, you can click **Query Sample Dataset** to open the interactive tutorials or click other links to explore TiDB Cloud. Alternatively, you can click **?** in the lower-right corner and click **Interactive Tutorials**.

## March 29, 2023

**General changes**

- [Data Service (beta)](/tidb-cloud/data-service-overview.md) supports more fine-grained access control for Data Apps.

    On the Data App details page, now you can link clusters to your Data App and specify the role for each API key. The role controls whether the API key can read or write data to the linked clusters and can be set to `ReadOnly` or `ReadAndWrite`. This feature provides cluster-level and permission-level access control for Data Apps, giving you more flexibility to control the access scope according to your business needs.

    For more information, see [Manage linked clusters](/tidb-cloud/data-service-manage-data-app.md#manage-linked-clusters) and [Manage API keys](/tidb-cloud/data-service-api-key.md).

## March 28, 2023

**General changes**

- Add 2 RCUs, 4 RCUs, and 8 RCUs specifications for [changefeeds](/tidb-cloud/changefeed-overview.md), and support choosing your desired specification when you [create a changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed).

    Using these new specifications, the data replication costs can be reduced by up to 87.5% compared to scenarios where 16 RCUs were previously required.

- Support scaling up or down specifications for [changefeeds](/tidb-cloud/changefeed-overview.md) created after March 28, 2023.

    You can improve replication performance by choosing a higher specification or reduce replication costs by choosing a lower specification.

    For more information, see [Scale a changefeed](/tidb-cloud/changefeed-overview.md#scale-a-changefeed).

- Support replicating incremental data in real-time from a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster in AWS to a [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) cluster in the same project and same region.

    For more information, see [Sink to TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md).

- Support two new GCP regions for the [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) feature of [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters: `Singapore (asia-southeast1)` and `Oregon (us-west1)`.

    With these new regions, you have more options for migrating your data to TiDB Cloud. If your upstream data is stored in or near these regions, you can now take advantage of faster and more reliable data migration from GCP to TiDB Cloud.

    For more information, see [Migrate MySQL-compatible databases to TiDB Cloud using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md).

**Console changes**

- Release a new native web infrastructure for the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) page of [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters.

    With this new infrastructure, you can easily navigate through the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) page and access the necessary information in a more intuitive and efficient manner. The new infrastructure also resolves many problems on UX, making the SQL diagnosis process more user-friendly.

## March 21, 2023

**General changes**

- Introduce [Data Service (beta)](https://tidbcloud.com/console/data-service) for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters, which enables you to access data via an HTTPS request using a custom API endpoint.

    With Data Service, you can seamlessly integrate TiDB Cloud with any application or service that is compatible with HTTPS. The following are some common scenarios:

    - Access the database of your TiDB cluster directly from a mobile or web application.
    - Use serverless edge functions to call endpoints and avoid scalability issues caused by database connection pooling.
    - Integrate TiDB Cloud with data visualization projects by using Data Service as a data source.
    - Connect to your database from an environment that MySQL interface does not support.

    In addition, TiDB Cloud provides the [Chat2Query API](/tidb-cloud/use-chat2query-api.md), a RESTful interface that allows you to generate and execute SQL statements using AI.

    To access Data Service, navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page in the left navigation pane. For more information, see the following documentation:

    - [Data Service Overview](/tidb-cloud/data-service-overview.md)
    - [Get Started with Data Service](/tidb-cloud/data-service-get-started.md)
    - [Get Started with Chat2Query API](/tidb-cloud/use-chat2query-api.md)

- Support decreasing the size of TiDB, TiKV, and TiFlash nodes to scale in a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster that is hosted on AWS and created after December 31, 2022.

    You can decrease the node size [via the TiDB Cloud console](/tidb-cloud/scale-tidb-cluster.md#change-node-size) or [via the TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster).

- Support a new GCP region for the [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) feature of [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters: `Tokyo (asia-northeast1)`.

    The feature can help you migrate data from MySQL-compatible databases in Google Cloud Platform (GCP) to your TiDB cluster easily and efficiently.

    For more information, see [Migrate MySQL-compatible databases to TiDB Cloud using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md).

**Console changes**

- Introduce the **Events** page for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters, which provides the records of main changes to your cluster.

    On this page, you can view the event history for the last 7 days and track important details such as the trigger time and the user who initiated an action. For example, you can view events such as when a cluster was paused or who modified the cluster size.

    For more information, see [TiDB Cloud cluster events](/tidb-cloud/tidb-cloud-events.md).

- Add the **Database Status** tab to the **Monitoring** page for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters, which displays the following database-level metrics:

    - QPS Per DB
    - Average Query Duration Per DB
    - Failed Queries Per DB

  With these metrics, you can monitor the performance of individual databases, make data-driven decisions, and take actions to improve the performance of your applications.

  For more information, see [Monitoring metrics for Serverless Tier clusters](/tidb-cloud/built-in-monitoring.md).

## March 14, 2023

**General changes**

- Upgrade the default TiDB version of new [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters from [v6.5.0](https://docs.pingcap.com/tidb/v6.5/release-6.5.0) to [v6.5.1](https://docs.pingcap.com/tidb/v6.5/release-6.5.1).

- Support modifying column names of the target table to be created by TiDB Cloud when uploading a local CSV file with a header row.

    When importing a local CSV file with a header row to a [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) cluster, if you need TiDB Cloud to create the target table and the column names in the header row do not follow the TiDB Cloud column naming conventions, you will see a warning icon next to the corresponding column name. To resolve the warning, you can move the cursor over the icon and follow the message to edit the existing column names or enter new column names.

    For information about column naming conventions, see [Import local files](/tidb-cloud/tidb-cloud-import-local-files.md#import-local-files).

## March 7, 2023

**General changes**

- Upgrade the default TiDB version of all [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters from [v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0) to [v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0).

## February 28, 2023

**General changes**

- Add the [SQL Diagnosis](/tidb-cloud/tune-performance.md) feature for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters.

    With SQL Diagnosis, you can gain deep insights into SQL-related runtime status, which makes the SQL performance tuning more efficient. Currently, the SQL Diagnosis feature for Serverless Tier only provides slow query data.

    To use SQL Diagnosis, click **SQL Diagnosis** on the left navigation bar of your Serverless Tier cluster page.

**Console changes**

- Optimize the left navigation.

    You can navigate pages more efficiently, for example:

    - You can hover the mouse in the upper-left corner to quickly switch between clusters or projects.
    - You can switch between the **Clusters** page and the **Admin** page.

**API changes**

- Release several TiDB Cloud API endpoints for data import：

    - List all import tasks
    - Get an import task
    - Create an import task
    - Update an import task
    - Upload a local file for an import task
    - Preview data before starting an import task
    - Get the role information for import tasks

  For more information, refer to the [API documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import).

## February 22, 2023

**General changes**

- Support using the [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md) feature to track various activities performed by members within your organization in the [TiDB Cloud console](https://tidbcloud.com/).

    The console audit logging feature is only visible to users with the `Owner` or `Audit Admin` role and is disabled by default. To enable it, click <MDSvgIcon name="icon-top-organization" /> **Organization** > **Console Audit Logging** in the upper-right corner of the [TiDB Cloud console](https://tidbcloud.com/).

    By analyzing console audit logs, you can identify suspicious operations performed within your organization, thereby improving the security of your organization's resources and data.

    For more information, see [Console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md).

**CLI changes**

- Add a new command [`ticloud cluster connect-info`](/tidb-cloud/ticloud-cluster-connect-info.md) for [TiDB Cloud CLI](/tidb-cloud/cli-reference.md).

    `ticloud cluster connect-info` is a command that allows you to get the connection string of a cluster. To use this command, [update `ticloud`](/tidb-cloud/ticloud-update.md) to v0.3.2 or a later version.

## February 21, 2023

**General changes**

- Support using the AWS access keys of an IAM user to access your Amazon S3 bucket when importing data to TiDB Cloud.

    This method is simpler than using Role ARN. For more information, refer to [Configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

- Extend the [monitoring metrics retention period](/tidb-cloud/built-in-monitoring.md#metrics-retention-policy) from 2 days to a longer period:

    - For Dedicated Tier clusters, you can view metrics data for the past 7 days.
    - For Serverless Tier clusters, you can view metrics data for the past 3 days.

  By extending the metrics retention period, now you have access to more historical data. This helps you identify trends and patterns of the cluster for better decision-making and faster troubleshooting.

**Console changes**

- Release a new native web infrastructure on the Monitoring page of [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters.

    With the new infrastructure, you can easily navigate through the Monitoring page and access the necessary information in a more intuitive and efficient manner. The new infrastructure also resolves many problems on UX, making the monitoring process a lot more user-friendly.

## February 17, 2023

**CLI changes**

- Add a new command [`ticloud connect`](/tidb-cloud/ticloud-connect.md) for [TiDB Cloud CLI](/tidb-cloud/cli-reference.md).

    `ticloud connect` is a command that allows you to connect to your TiDB Cloud cluster from your local machine without installing any SQL clients. After connecting to your TiDB Cloud cluster, you can execute SQL statements in the TiDB Cloud CLI.

## February 14, 2023

**General changes**

- Support decreasing the number of TiKV and TiFlash nodes to scale in a TiDB [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster.

    You can decrease the node number [via the TiDB Cloud console](/tidb-cloud/scale-tidb-cluster.md#change-node-number) or [via the TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster).

**Console changes**

- Introduce the **Monitoring** page for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters.

    The **Monitoring** page provides a range of metrics and data, such as the number of SQL statements executed per second, the average duration of queries, and the number of failed queries, which helps you better understand the overall performance of SQL statements in your Serverless Tier cluster.

    For more information, see [TiDB Cloud built-in monitoring](/tidb-cloud/built-in-monitoring.md).

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

    You can increase the node size [using the TiDB Cloud console](/tidb-cloud/scale-tidb-cluster.md#change-node-size) or [using the TiDB Cloud API (beta)](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster).

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
