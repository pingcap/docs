---
title: TiDB Cloud Release Notes in 2025
summary: Learn about the release notes of TiDB Cloud in 2025.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2025

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2025.

## January 2, 2025

**General changes**

- Support creating TiDB node groups for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters to enhance resource management flexibility. 

    For more information, see [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md).

- Support connecting [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters to generic Kafka in AWS and Google Cloud through Private Connect (beta).

    Private Connect leverages Private Link or Private Service Connect technologies from cloud providers to enable changefeeds in the TiDB Cloud VPC to connect to Kafka in customers' VPCs using private IP addresses, as if those Kafkas were hosted directly within the TiDB Cloud VPC. This feature helps prevent VPC CIDR conflicts and meets security compliance requirements.

    - For Apache Kafka in AWS, follow the instructions in [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-self-hosted-kafka-private-link-service.md) to configure the network connection.

    - For Apache Kafka in Google Cloud, follow the instructions in [Set Up Self-Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md) to configure the network connection.
  
  Note that using this feature incurs additional [Private Data Link costs](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost).

    For more information, see [Changefeed Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network).

- Introduce additional configurable options for Kafka changefeeds:

    - Support using the Debezium protocol. Debezium is a tool for capturing database changes. It converts each captured database change into a message called an event, and sends these events to Kafka. For more information, see [TiCDC Debezium Protocol](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium).

    - Support defining a single partition dispatcher for all tables, or different partition dispatchers for different tables. 

    - Introduce two new dispatcher types for the partition distribution of Kafka messages: timestamp and column value.

  For more information, see [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md).

- Enhance roles in TiDB Cloud:

    - Introduce the `Project Viewer` and `Organization Billing Viewer` roles to enhance granular access control on TiDB Cloud.

    - Rename the following roles:

        - `Organization Member` to `Organization Viewer`
        - `Organization Billing Admin` to `Organization Billing Manager`
        - `Organization Console Audit Admin` to `Organization Console Audit Manager`

  For more information, see [Identity Access Management](/tidb-cloud/manage-user-access.md#organization-roles).

- Regional high availability (beta) for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters.

    This feature is designed for workloads that require maximum infrastructure redundancy and business continuity. Key functions include:

    - Nodes are distributed across multiple availability zones to ensure high availability in the event of a zone failure.
    - Critical OLTP (Online Transactional Processing) components, such as PD and TiKV, are replicated across availability zones for redundancy.
    - Automatic failover minimizes service disruption during a primary zone failure.
  
  This feature is currently available only in the AWS Tokyo (ap-northeast-1) region and can be enabled only during cluster creation.
  
    For more information, see [High Availability in TiDB Cloud Serverless](/tidb-cloud/serverless-high-availability.md).

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1) to [v8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2).

**Console changes**

- Strengthen the data export service:

    - Support exporting data from [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) to Google Cloud Storage and Azure Blob Storage through the [TiDB Cloud console](https://tidbcloud.com/).

    - Support exporting data in Parquet files through the [TiDB Cloud console](https://tidbcloud.com/).

  For more information, see [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md) and [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md).
