---
title: TiDB Cloud Release Notes in 2026
summary: Learn about the release notes of TiDB Cloud in 2026.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2026

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2026.

## January 20, 2026

**General changes**

- **TiDB Cloud Starter**

    - Display real client IP addresses in the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) view and the [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) table (public preview)

        TiDB Cloud now supports client IP pass-through, enabling the Slow Query view and the `INFORMATION_SCHEMA.PROCESSLIST` table, to display the real client IP address instead of the Load Balancer (LB) IP. This feature helps accurately identify the true source of database requests for better troubleshooting and analysis. 

        Currently, this feature is in public preview and is available only in the AWS region `Frankfurt (eu-central-1)`.

        For more information, see [Analyze and Tune Performance](/tidb-cloud/tune-performance.md).

- **TiDB Cloud Essential**

    - Support data migration.

        Now you can use the Data Migration feature in the [TiDB Cloud console](https://tidbcloud.com) to seamlessly migrate data from any MySQL-compatible database to your [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) clusters.

        - Supported source databases include various MySQL-compatible systems, such as self-hosted MySQL, Amazon RDS, Alibaba Cloud RDS, and PolarDB.
        - Supported connection methods for data migration include public connection and PrivateLink to ensure both ease of use and enterprise-grade security:

            - **Public connection**: quickly connects to your source database over the internet using secure and encrypted channels.
            - **PrivateLink**: establishes a secure and private connection between your source VPC and TiDB Cloud, bypassing the public internet to ensure maximum data privacy and reduced network latency.

      Currently, the Data Migration feature only supports logical mode.
  
        For more information, see [Migrate Existing and Incremental Data Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) and [Migrate Incremental Data Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md).

    - Display real client IP addresses in the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) view and the [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) table (public preview)

        TiDB Cloud now supports client IP pass-through, enabling the Slow Query view and the `INFORMATION_SCHEMA.PROCESSLIST` table, to display the real client IP address instead of the Load Balancer (LB) IP. This feature helps accurately identify the true source of database requests for better troubleshooting and analysis. 

        Currently, this feature is in public preview and is available only in the AWS region `Frankfurt (eu-central-1)`.

        For more information, see [Database Audit Logging (Beta) for {{{ .essential }}}](/tidb-cloud/essential-database-audit-logging.md).    

**Console changes**

- Make support options plan-aware to improve the support experience

    To improve the support experience across different subscription plans, make the following improvements:

    - **Provide plan-aware support redirection**: **Get Support** in the **Actions** column on the cluster overview page now directs you to the most relevant resource based on your current subscription. It guides Basic plan users to the **Support Plan** panel and paid plan users to the **Support Portal**.    
    - **Refine the Help Center menu**: rename help menu items to **Support Options** and **Support Tickets** to better reflect available services. Add tooltips to clarify that technical support tickets are exclusive to paid plans.
    - **Provide visible community access**: clearly designate Slack and Discord as the primary technical support channels for free users in **Support Plan** options. Streamline the [Get Support](/tidb-cloud/tidb-cloud-support.md), [Connected Care Overview](/tidb-cloud/connected-care-overview.md), and [Connected Care Details](/tidb-cloud/connected-care-detail.md) documentation to provide clearer guidance on support channel policies and community access.   
    - **Redesign action-oriented Support Plan UI**: redesign the **Support Plan** window to prioritize your current support options over generic plan comparisons. This aims to help you focus directly on getting the help you need based on your active subscription.

  For more information, see [Connected Care Overview](/tidb-cloud/connected-care-overview.md).

## January 15, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.5.4](https://docs.pingcap.com/tidb/v8.5/release-8.5.4/) to [v8.5.5](https://docs.pingcap.com/tidb/v8.5/release-8.5.5/).