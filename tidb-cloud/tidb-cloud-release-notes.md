---
title: TiDB Cloud Release Notes in 2025
summary: Learn about the release notes of TiDB Cloud in 2025.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2025

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2025.

## April 1, 2025

**General changes**

- The [TiDB Node Groups](/tidb-cloud/tidb-node-group-overview.md) feature is now generally available (GA) for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on AWS and Google Cloud.

    This feature enables **fine-grained computing resource isolation** within a single cluster, helping you optimize performance and resource allocation for multi-tenant or multi-workload scenarios.

    **Key benefits:**

    - **Resource isolation**:

        - Group TiDB nodes into logically isolated units, ensuring workloads in one group do not affect other groups.
        - Prevent resource contention between applications or business units.

    - **Simplified management**:

        - Manage all node groups within a single cluster, reducing operational overhead.
        - Scale groups independently based on demand.

  For more information about the benefits, see [the technical blog](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/). To get started, see [Manage TiDB Node Groups](/tidb-cloud/tidb-node-group-management.md).

- Introduce the [Standard storage](/tidb-cloud/size-your-cluster.md#standard-storage) type for TiKV nodes in [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on AWS.

    The Standard storage type is ideal for most workloads, providing a balance between performance and cost efficiency.

    **Key benefits:**

    - **Improved performance**: Reserves sufficient disk resources for Raft logs, reducing I/O contention between Raft and data storage, thereby improving both the read and write performance of TiKV.
    - **Enhanced stability**: Isolates critical Raft operations from data workloads, ensuring more predictable performance.
    - **Cost efficiency**: Delivers higher performance at a competitive price compared with the previous storage type.

    **Availability:**

    The Standard storage type is automatically applied to new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters created on or after April 1, 2025, hosted on AWS, with supported versions (versions >= 7.5.5, 8.1.2, or 8.5.0). Existing clusters still use the previous [Basic storage](/tidb-cloud/size-your-cluster.md#basic-storage) type, and no migration is needed.

    The price of the Standard storage differs from that of the Basic storage. For more information, see [Pricing](https://www.pingcap.com/tidb-dedicated-pricing-details/).

## March 25, 2025

**Console changes**

- Support firewall rules for public endpoints in [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters.

    You can now configure firewall rules for TiDB Cloud Serverless clusters to control access via public endpoints. Specify allowed IP addresses or ranges directly in the [TiDB Cloud console](https://tidbcloud.com/) to enhance security.

    For more information, see [Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md).

## March 18, 2025

**General changes**

- Support creating TiDB node groups for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters deployed on Google Cloud to enhance resource management flexibility.

    For more information, see [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md).

- Support storing database audit log files in TiDB Cloud for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters deployed on AWS.

    You can download these audit log files directly from TiDB Cloud. Note that this feature is only available upon request.

    For more information, see [Database Audit Logging](/tidb-cloud/tidb-cloud-auditing.md).

- Enhance TiDB Cloud account security by improving the management of multi-factor authentication (MFA). This feature applies to password-based logins for TiDB Cloud.

    For more information, see [Password Authentication](/tidb-cloud/tidb-cloud-password-authentication.md).

## February 18, 2025

**Console changes**

- Introduce Connected Care, the new support services for TiDB Cloud.

    The Connected Care services are designed to strengthen your connection with TiDB Cloud through modern communication tools, proactive support, and advanced AI capabilities, delivering a seamless and customer-centric experience.

    The Connected Care services introduce the following features:

    - **Clinic service**: Advanced monitoring and diagnostics to optimize performance.
    - **AI chat in IM**: Get immediate AI assistance through an instant message (IM) tool.
    - **IM subscription for alerts and ticket updates**: Stay informed with alerts and ticket progress via IM.
    - **IM interaction for support tickets**: Create and interact with support tickets through an IM tool.

  For more information, see [Connected Care Overview](/tidb-cloud/connected-care-overview.md).

- Support importing data from GCS and Azure Blob Storage into [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters.

    TiDB Cloud Serverless now supports importing data from Google Cloud Storage (GCS) and Azure Blob Storage. You can use a Google Cloud service account key or an Azure shared access signature (SAS) token to authenticate. This feature simplifies data migration to TiDB Cloud Serverless.

    For more information, see [Import CSV Files from Amazon S3, GCS, or Azure Blob Storage into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md) and [Import Apache Parquet Files from Amazon S3, GCS, or Azure Blob Storage into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md).

## January 21, 2025

**Console changes**

- Support importing a single local CSV file of up to 250 MiB per task to [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters, increased from the previous limit of 50 MiB.

    For more information, see [Import Local Files to TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md).

## January 14, 2025

**General changes**

- Support a new AWS region for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters: `Jakarta (ap-southeast-3)`.

- Introduce the [Notifications](https://tidbcloud.com/console/notifications) feature, which enables you to stay informed instantly with TiDB Cloud updates and alerts through the [TiDB Cloud console](https://tidbcloud.com/).

    For more information, see [Notifications](/tidb-cloud/notifications.md).

## January 2, 2025

**General changes**

- Support creating TiDB node groups for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters to enhance resource management flexibility. 

    For more information, see [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md).

- Support connecting [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters to generic Kafka in AWS and Google Cloud through Private Connect (beta).

    Private Connect leverages Private Link or Private Service Connect technologies from cloud providers to enable changefeeds in the TiDB Cloud VPC to connect to Kafka in customers' VPCs using private IP addresses, as if those Kafkas were hosted directly within the TiDB Cloud VPC. This feature helps prevent VPC CIDR conflicts and meets security compliance requirements.

    - For Apache Kafka in AWS, follow the instructions in [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) to configure the network connection.

    - For Apache Kafka in Google Cloud, follow the instructions in [Set Up Self-Hosted Kafka Private Service Connect in Google Cloud](/tidb-cloud/setup-gcp-self-hosted-kafka-private-service-connect.md) to configure the network connection.
  
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
