---
title: TiDB Cloud Release Notes in 2026
summary: Learn about the release notes of TiDB Cloud in 2026.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2026

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2026.

## February 10, 2026

**General changes**

- **TiDB Cloud Starter**

    - Upgrade the default TiDB version of new [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) clusters from [v7.5.6](https://docs.pingcap.com/tidb/stable/release-7.5.6) to [v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3).

- **TiDB Cloud Essential**

    - Support built-in alerting.

        Built-in alerting enables you to subscribe to receive instant alerts through email, Slack, Zoom, Flashduty, and PagerDuty. You can also customize alerts by defining specific thresholds for each alert type.

        For more information, see [TiDB Cloud Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md).

- **TiDB Cloud Dedicated**

    - Support Private Link connectivity for data imports from Azure Blob Storage.
  
        When importing data from Azure Blob Storage into a [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster, you can now select Private Link as the connectivity method to connect via an Azure private endpoint instead of the public internet. This feature enables secure, network-isolated data imports for storage accounts that restrict public access.

        For more information, see [Import Sample Data (SQL Files) from Cloud Storage](/tidb-cloud/import-sample-data.md), [Import CSV Files from Cloud Storage](/tidb-cloud/import-csv-files.md), and [Import Apache Parquet Files from Cloud Storage](/tidb-cloud/import-parquet-files.md).

    - Add "Enable/Disable Public Endpoint" events to the Console Audit Logging in TiDB Cloud for better security tracking.

## February 3, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Support sinking changefeed data to Azure Blob Storage.

        [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) now supports sinking changefeed data directly to Azure Blob Storage. This feature enables Azure-based users to archive change data efficiently for downstream analytics and long-term retention. It also reduces costs by eliminating the need for intermediate message queues and maintains format compatibility with existing Amazon S3 and Google Cloud Storage (GCS) sinks.

        For more information, see [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md).

## January 27, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Support Flashduty and PagerDuty as alert subscription channels.
  
        These integrations are designed to streamline your incident management process and improve operational reliability.
  
        For more information, see [Subscribe via Flashduty](/tidb-cloud/monitor-alert-flashduty.md) and [Subscribe via PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md).

## January 20, 2026

**General changes**

- **TiDB Cloud Starter**

    - Display real client IP addresses in the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) view and the [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) table (beta).

        TiDB Cloud now supports client IP pass-through, enabling the Slow Query view and the `INFORMATION_SCHEMA.PROCESSLIST` table, to display the real client IP address instead of the Load Balancer (LB) IP. This feature helps accurately identify the true source of database requests for better troubleshooting and analysis. 

        Currently, this feature is in beta and is available only in the AWS region `Frankfurt (eu-central-1)`.

- **TiDB Cloud Essential**

    - Support data migration (beta).

        Now you can use the Data Migration feature in the [TiDB Cloud console](https://tidbcloud.com) to seamlessly migrate data from any MySQL-compatible database to your [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) clusters.

        - Supported source databases include various MySQL-compatible systems, such as self-hosted MySQL, Amazon RDS, Alibaba Cloud RDS, and PolarDB.
        - Supported connection methods for data migration include public connection and PrivateLink to ensure both ease of use and enterprise-grade security:

            - **Public connection**: quickly connects to your source database over the internet using secure and encrypted channels.
            - **PrivateLink**: establishes a secure and private connection between your source VPC and TiDB Cloud, bypassing the public internet to ensure maximum data privacy and reduced network latency.

      Currently, the Data Migration feature only supports logical mode.
  
        For more information, see [Migrate Existing and Incremental Data Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) and [Migrate Incremental Data Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md).

    - Display real client IP addresses in the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) view, [DB audit logs](/tidb-cloud/essential-database-audit-logging.md), and the [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) table (beta)

        TiDB Cloud now supports client IP pass-through, enabling the Slow Query view, DB audit logs, and the `INFORMATION_SCHEMA.PROCESSLIST` table, to display the real client IP address instead of the Load Balancer (LB) IP. This feature helps accurately identify the true source of database requests for better troubleshooting and analysis. 

        Currently, this feature is in beta and is available only in the AWS region `Frankfurt (eu-central-1)`.

**Console changes**

- Improve the support experience with plan-aware support options.

    The [TiDB Cloud console](https://tidbcloud.com/) now offers plan-aware support options to enhance the support experience across all subscription plans. These updates include:

    - **Plan-aware support redirection**: on the cluster overview page, selecting **Get Support** in the **Actions** column directs you to the most relevant resource based on your subscription plan. Users on the Basic plan are guided to the **Support Plan** panel, and users on paid plans are directed to the **Support Portal**.
    - **Refined Help Center menu**: rename help menu items to **Support Options** and **Support Tickets** to better reflect available services. Add tooltips to clarify that technical support tickets are available only for paid plans.
    - **Clear community support access**: within the **Support Plan** options, Slack and Discord are clearly identified as the primary technical support channels for Basic plan users. The following documentation is streamlined to clarify support channel policies and community access: [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md), [Connected Care Overview](/tidb-cloud/connected-care-overview.md), and [Connected Care Details](/tidb-cloud/connected-care-detail.md).
    - **Action-oriented Support Plan UI**: redesign the **Support Plan** window to prioritize the support options available for your current subscription, rather than generic plan comparisons. This change helps you quickly identify how to get support based on your active plan.

  For more information, see [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## January 15, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.5.4](https://docs.pingcap.com/tidb/v8.5/release-8.5.4/) to [v8.5.5](https://docs.pingcap.com/tidb/v8.5/release-8.5.5/).
