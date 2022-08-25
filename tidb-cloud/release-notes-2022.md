---
title: TiDB Cloud Release Notes in 2022
summary: Learn about the release notes of TiDB Cloud in 2022.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2022

This page lists the release notes of [TiDB Cloud](https://en.pingcap.com/tidb-cloud/) in 2022.

## August 24, 2022

**General changes**

* Support pausing or resuming a Dedicated Tier cluster.

    You can [pause or resume your Dedicated Tier cluster](/tidb-cloud/pause-or-resume-tidb-cluster.md) in TiDB Cloud. When a cluster is paused, Node Compute Cost will not be charged.

## August 23, 2022

**General changes**

* Upgrade the default TiDB version of new [Developer Tier](/tidb-cloud/select-cluster-tier.md#developer-tier) clusters from [v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) to [v6.2.0](https://docs.pingcap.com/tidb/v6.2/release-6.2.0).

**API changes**

* Introduce TiDB Cloud API as beta.

    Through this API, you can manage TiDB Cloud resources such as clusters automatically and efficiently. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

    Currently, TiDB Cloud API is still in beta and only available upon request. You can apply for API access by submitting a request:

    * Click **Help** in the lower-right corner of [TiDB Cloud console](https://tidbcloud.com/console/clusters).
    * In the dialog, fill in "Apply for TiDB Cloud API" in the **Description** field and click **Send**.

## August 16, 2022

* Add `2 vCPU, 8 GiB (Beta)` node size of TiDB and TiKV as beta.

    * For each `2 vCPU, 8 GiB (Beta)` TiKV node, the storage size is between 200 GiB and 500 GiB.

    * Suggested usage scenarios:

        * Low-workload production environments for SMB
        * PoC and staging environments
        * Development environments

* Introduce [Credits](/tidb-cloud/tidb-cloud-billing.md#credits) (previously named as trail points) for PoC users.

    You can now view information about your organization's credits on the **Credits** tab of the **Billing** page, the credits can be used to pay for TiDB Cloud fees. You can [contact us](https://en.pingcap.com/apply-for-poc/) to get credits.

## August 9, 2022

* Add the support of the GCP region `Osaka` for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster creation.

## August 2, 2022

* The `4 vCPU, 16 GiB` node size of TiDB and TiKV is now in General Availability (GA).

    * For each `4 vCPU, 16 GiB` TiKV node, the storage size is between 200 GiB and 2 TiB.
    * Suggested usage scenarios:

        * Low workload production environments for SMB
        * PoC and staging environments
        * Development environments

* Add a [Monitoring page](/tidb-cloud/built-in-monitoring.md) to the **Diagnosis** tab for [Dedicated Tier clusters](/tidb-cloud/select-cluster-tier.md#dedicated-tier).

    The Monitoring page provides a system-level entry for overall performance diagnosis. According to the top-down performance analysis methodology, the Monitoring page organizes TiDB performance metrics based on database time breakdown and displays these metrics in different colors. By checking these colors, you can identify performance bottlenecks of the entire system at the first glance, which significantly reduces performance diagnosis time and simplifies performance analysis and diagnosis.

* Add a switch to enable or disable **Custom Pattern** on the **Data Import** page for CSV and Parquet source files.

    The **Custom Pattern** feature is disabled by default. You can enable it when you are going to import CSV or Parquet files whose filenames match a certain pattern to a single target table.

    For more information, see [Import CSV Files](/tidb-cloud/import-csv-files.md) and [Import Apache Parquet Files](/tidb-cloud/import-parquet-files.md).

* Add TiDB Cloud Support Plans (Basic, Standard, Enterprise, and Premium) to meet different support needs of customers' organizations. For more information, see [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

* Optimize the UI of the [Clusters](https://tidbcloud.com/console/clusters) page and the cluster details page:

    * Add **Connect** and **Import data** buttons to the **Clusters** page.
    * Move **Connect** and **Import data** buttons to the upper-right corner on the cluster details page.

## July 28, 2022

* Add the **Allow Access from Anywhere** button to the **Security Quick Start** dialog, which allows your cluster to be accessible by any IP addresses. For more information, see [Configure Cluster Security Settings](/tidb-cloud/configure-security-settings.md).

## July 26, 2022

* Support [automatic hibernation and resuming](/tidb-cloud/select-cluster-tier.md#automatic-hibernation-and-resuming) for new [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier).

    A Developer Tier cluster will not be deleted after 7 days of inactivity so you can still use it at any time until the one-year free trial ends. After 24 hours of inactivity, the Developer Tier cluster will hibernate automatically. To resume the cluster, either send a new connection to the cluster or click the **Resume** button in the TiDB Cloud console. The cluster will be resumed within 50 seconds and back to service automatically.

* Add a user name prefix limitation for new [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier).

    Whenever you use or set a database user name, you must include the prefix for your cluster in the user name. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).

* Disable the backup and restore feature for [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier).

    The backup and restore feature (including both automatic backup and manual backup) is disabled for Developer Tier clusters. You can still use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export your data as a backup.

* Increase the storage size of a [Developer Tier](/tidb-cloud/select-cluster-tier.md#developer-tier) cluster from 500 MiB to 1 GiB.
* Add breadcrumbs to the TiDB Cloud console to improve the navigation experience.
* Support configuring multiple filter rules when you import data into TiDB Cloud.
* Remove the **Traffic Filters** page from **Project Settings**, and remove the **Add Rules from Default Set** button from the **Connect to TiDB** dialog.

## July 19, 2022

* Provide a new option for [TiKV node size](/tidb-cloud/size-your-cluster.md#tikv-node-size): `8 vCPU, 32 GiB`. You can choose either `8 vCPU, 32 GiB` or `8 vCPU, 64 GiB` for an 8 vCPU TiKV node.
* Support syntax highlighting in sample code provided in the [**Connect to TiDB**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) dialog to improve code readability. You can easily identify the parameters that you need to replace in the sample code.
* Support automatically validating whether TiDB Cloud can access your source data after you confirm the import task on the [**Data Import Task**](/tidb-cloud/import-sample-data.md) page.
* Change the theme color of the TiDB Cloud console to make it consistent with that of [PingCAP website](https://en.pingcap.com/).

## July 12, 2022

* Add the **Validate** button to the [**Data Import Task**](/tidb-cloud/import-sample-data.md) page for Amazon S3, which helps you detect data access issues before the data import starts.
* Add **Billing Profile** under the [**Payment Method**](/tidb-cloud/tidb-cloud-billing.md#payment-method) tab. By providing your tax registration number in **Billing Profile**, certain taxes might be exempted from your invoice. For more information, see [Edit billing profile information](/tidb-cloud/tidb-cloud-billing.md#edit-billing-profile-information).

## July 05, 2022

* The columnar storage [TiFlash](/tiflash/tiflash-overview.md) is now in General Availability (GA).

    - TiFlash makes TiDB essentially an Hybrid Transactional/Analytical Processing (HTAP) database. Your application data is first stored in TiKV and then replicated to TiFlash via the Raft consensus algorithm. So it is real time replication from the row storage to the columnar storage.
    - For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use either TiKV or TiFlash replicas based on the cost estimation.

    To experience the benefits brought by TiFlash, see [TiDB Cloud HTAP Quick Start Guide](/tidb-cloud/tidb-cloud-htap-quickstart.md).

* Support [increasing the storage size](/tidb-cloud/scale-tidb-cluster.md#increase-node-storage) of TiKV and TiFlash for a Dedicated Tier cluster.
* Support showing the memory information in the node size field.

## June 28, 2022

* Upgrade TiDB Cloud Dedicated Tier from [TiDB v5.4.1](https://docs.pingcap.com/tidb/stable/release-5.4.1) to [TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0).

## June 23, 2022

* Increase the maximum [storage capacity of TiKV](/tidb-cloud/size-your-cluster.md#tikv-node-storage) on TiDB Cloud.

    * 8 vCPU or 16 vCPU TiKV: support up to 4 TiB storage capacity.
    * 4 vCPU TiKV: support up to 2 TiB storage capacity.

## June 21, 2022

* Add the support of the GCP region `Taiwan` for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster creation.
* Support [updating user profiles](/tidb-cloud/manage-user-access.md#manage-user-profiles) on the TiDB Cloud console, including first name, last time, company name, country, and phone number.
* Provide the connection strings for MySQL, MyCLI, JDBC, Python, Go, and Node.js in the [**Connect to TiDB**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) dialog so you can easily connect to your TiDB cluster.
* Support obtaining bucket regions from bucket URLs automatically during data import to save your effort to fill in such information.

## June 16, 2022

* Simplify the [cluster creation process](/tidb-cloud/create-tidb-cluster.md).

    - When you create a cluster, TiDB Cloud provides a default cluster name. You can either use the default name or update it.
    - When you create a cluster, you do not need to set the password on the **Create a Cluster** page.
    - During or after the cluster creation, you can set the root password to access the cluster and also the IP addresses to connect to the cluster in the **Security Quick Start** dialog box.

## June 14, 2022

* Upgrade TiDB Cloud to [TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) for Developer Tier.
* Optimize the entrance of **Project Settings**. From the TiDB Cloud console, you can choose a target project and go to its settings easily by clicking the **Project Settings** tab.
* Optimize the experience of password expiration by providing expiration messages in the TiDB Cloud console.

## June 7, 2022

* Add the [Try Free](https://tidbcloud.com/free-trial) registration page to quickly sign up for TiDB Cloud.
* Remove the **Proof of Concept plan** option from the plan selection page. If you want to apply for a 14-day PoC trial for free, go to the [Apply for PoC](https://en.pingcap.com/apply-for-poc/) page. For more information, see [Perform a Proof of Concept (PoC) with TiDB Cloud](/tidb-cloud/tidb-cloud-poc.md).
* Improve the system security by prompting users who sign up for TiDB Cloud with emails and passwords to reset their passwords every 90 days. For more information, see [Manage user passwords](/tidb-cloud/manage-user-access.md#manage-user-passwords).

## May 24, 2022

* Support customizing TiDB port number when you [create](/tidb-cloud/create-tidb-cluster.md) or [restore](/tidb-cloud/backup-and-restore.md#restore) a Dedicated Tier cluster.

## May 19, 2022

* Add the support of the AWS region `Frankfurt` for [Developer Tier](/tidb-cloud/select-cluster-tier.md#developer-tier) cluster creation.

## May 18, 2022

* Support [signing up](https://tidbcloud.com/signup) TiDB Cloud with a GitHub account.

## May 13, 2022

* Support [signing up](https://tidbcloud.com/signup) TiDB Cloud with a Google account.

## May 1, 2022

* Support configuring vCPU size of TiDB, TiKV, and TiFlash when you [create](/tidb-cloud/create-tidb-cluster.md) or [restore](/tidb-cloud/backup-and-restore.md#restore) a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster.
* Add the support of the AWS region `Mumbai` for cluster creation.
* Update the compute, storage, and data transfer cost for [TiDB Cloud billing](/tidb-cloud/tidb-cloud-billing.md).

## April 7, 2022

* Upgrade TiDB Cloud to [TiDB v6.0.0](https://docs.pingcap.com/tidb/v6.0/release-6.0.0-dmr) for Developer Tier.

## March 31, 2022

TiDB Cloud is now in General Availability. You can [sign up](https://tidbcloud.com/signup) and select one of the following options:

* Get started with [Developer Tier](/tidb-cloud/select-cluster-tier.md#developer-tier) for free.
* Apply for [a 14-day PoC trial for free](https://en.pingcap.com/apply-for-poc/).
* Get full access with [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier).

## March 25, 2022

New feature:

* Support [TiDB Cloud built-in alerting](/tidb-cloud/monitor-built-in-alerting.md).

    With the TiDB Cloud built-in alerting feature, you can be notified by emails whenever a TiDB Cloud cluster in your project triggers one of TiDB Cloud built-in alert conditions.

## March 15, 2022

General changes:

* No cluster tier with the fixed cluster size any more. You can customize the [cluster size](/tidb-cloud/size-your-cluster.md) of TiDB, TiKV, and TiFlash easily.
* Support adding [TiFlash](/tiflash/tiflash-overview.md) nodes for an existing cluster without TiFlash.
* Support specifying the storage size (500 to 2048 GiB) when [creating a new cluster](/tidb-cloud/create-tidb-cluster.md). The storage size cannot be changed after the cluster is created.
* Introduce a new public region: `eu-central-1`.
* Deprecate 8 vCPU TiFlash and provide 16 vCPU TiFlash.
* Separate the price of CPU and storage (both have 30% public preview discount).
* Update the [billing information](/tidb-cloud/tidb-cloud-billing.md) and the [price table](https://en.pingcap.com/tidb-cloud/#pricing).

New features:

* Support [the Prometheus and Grafana integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).

    With the Prometheus and Grafana integration, you can configure a [Prometheus](https://prometheus.io/) service to read key metrics from the TiDB Cloud endpoint and view the metrics using [Grafana](https://grafana.com/).

* Support assigning a default backup time based on the selected region of your new cluster.

    For more information, see [Back up and Restore TiDB Cluster Data](/tidb-cloud/backup-and-restore.md).

## March 04, 2022

New feature:

* Support [the Datadog integration](/tidb-cloud/monitor-datadog-integration.md).

    With the Datadog integration, you can configure TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/). After that, you can view these metrics in your Datadog dashboards directly.

## February 15, 2022

General change:

* Upgrade TiDB Cloud to [TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0) for Developer Tier.

Improvement:

* Support using custom file names when importing [CSV files](/tidb-cloud/import-csv-files.md) or [Apache Parquet files](/tidb-cloud/import-parquet-files.md) into TiDB Cloud.

## January 11, 2022

General change:

* Upgrade TiDB Operator to [v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6).

Improvement:

* Add a suggested option `--connect-timeout 15` to the MySQL client on the [**Connect**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) page.

Bug fixes:

* Fix the issue that a user cannot create a cluster if the password contains a single quote.
* Fix the issue that even an organization only has one owner, the owner can be deleted or changed to another role.