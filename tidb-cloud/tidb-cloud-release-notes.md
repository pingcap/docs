---
title: TiDB Cloud Release Notes in 2025
summary: Learn about the release notes of TiDB Cloud in 2025.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2025

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2025.

## June 4, 2025

**General changes**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) on Microsoft Azure is now available in public preview. 
  
    With this launch, TiDB Cloud now supports all three major public cloud platforms — AWS, Google Cloud, and Azure, which enables you to deploy TiDB Cloud Dedicated clusters wherever best fits your business needs and cloud strategy.
  
    - All core features available on AWS and Google Cloud are fully supported on Azure.
    - Azure support is currently available in three regions: East US 2, Japan East, and Southeast Asia, with more regions coming soon.
    - TiDB Cloud Dedicated clusters on Azure require TiDB version v7.5.3 or later.
  
  To quickly get started with TiDB Cloud Dedicated on Azure, see the following documentation:
  
    - [Create a TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/create-tidb-cluster.md)
    - [Connect a TiDB Cloud Dedicated Cluster via Azure Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md) 
    - [Import Data into TiDB Cloud Dedicated Cluster on Azure](/tidb-cloud/import-csv-files.md)

- The Prometheus integration provides more metrics to enhance monitoring capabilities of [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.
  
    Now you can integrate additional metrics, such as `tidbcloud_disk_read_latency` and `tidbcloud_kv_request_duration`, into Prometheus to track more aspects of your TiDB Cloud Dedicated performance.
  
    For more information on available metrics and how to enable them for both existing and new users, see [Integrate TiDB Cloud with Prometheus and Grafana (Beta)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus).

- TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) and [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) storage pricing is officially released.

    The discount period ends from **00:00 UTC on June 5, 2025**. After that, the price returns to the standard price. For more information about TiDB Cloud Dedicated prices, see [TiDB Cloud Dedicated Pricing Details](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost).

**Console changes**

- Enhance the interactive experience when configuring the size of TiFlash nodes of [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

    You can now use a toggle switch to control the TiFlash configuration when creating a TiDB Cloud Dedicated cluster, which makes the configuration experience more intuitive and seamless.

## May 27, 2025

**General changes**

- Support streaming data to [Apache Pulsar](https://pulsar.apache.org) with changefeeds for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

    This feature enables you to integrate your TiDB Cloud Dedicated cluster with a wider range of downstream systems, and accommodates additional data integration requirements. To use this feature, make sure that your TiDB Cloud Dedicated cluster version is v7.5.1 or later.

    For more information, see [Sink to Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md).

## May 13, 2025

**General changes**

- Full-text search (beta) now available in [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) for AI applications.

    TiDB Cloud Serverless now supports full-text search (beta), enabling AI and Retrieval-Augmented Generation (RAG) applications to retrieve content by exact keywords. This complements vector search, which retrieves content by semantic similarity. Combining both methods significantly improves retrieval accuracy and answer quality in RAG workflows. Key features include:

    - Direct text search: query string columns directly without the need for embeddings.
    - Multilingual support: automatically detects and analyzes text in multiple languages, even within the same table, without requiring language specification.
    - Relevance-based ranking: results are ranked using the industry-standard BM25 algorithm for optimal relevance.
    - Native SQL compatibility: seamlessly use SQL features such as filtering, grouping, and joining with full-text search.

  To get started, see [Full Text Search with SQL](/tidb-cloud/vector-search-full-text-search-sql.md) or [Full Text Search with Python](/tidb-cloud/vector-search-full-text-search-python.md).

- Increase the maximum TiFlash node storage for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster:

    - For 8 vCPU TiFlash, from 2048 GiB to 4096 GiB
    - For 32 vCPU TiFlash, from 4096 GiB to 8192 GiB

  This enhancement increases the analytics data storage capacity of your TiDB Cloud Dedicated cluster, improves workload scaling efficiency, and accommodates growing data requirements.

    For more information, see [TiFlash node storage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage).

- Enhance the maintenance window configuration experience by providing intuitive options to configure and reschedule maintenance tasks.

    For more information, see [Configure maintenance window](/tidb-cloud/configure-maintenance-window.md).

- Extend the discount period for TiKV [Standard](/tidb-cloud/size-your-cluster.md#standard-storage) and [Performance](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage) storage types. The promotion now ends on June 5, 2025. After this date, pricing will return to the standard rate.

**Console changes**

- Refine the **Backup Setting** page layout to improve the backup configuration experience in [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

    For more information, see [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md).

## April 22, 2025

**General changes**

- Data export to Alibaba Cloud OSS is now supported. 

    [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters now support exporting data to [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/en/product/object-storage-service) using an [AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair).

    For more information, see [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md#alibaba-cloud-oss).

## April 15, 2025

**General changes**

- Support importing data from [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/en/product/object-storage-service) into [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters.

    This feature simplifies data migration to TiDB Cloud Serverless. You can use an AccessKey pair to authenticate.

    For more information, see the following documentation:

    - [Import CSV Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [Import Apache Parquet Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

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

- Introduce the Notification feature, which enables you to stay informed instantly with TiDB Cloud updates and alerts through the [TiDB Cloud console](https://tidbcloud.com/).

    For more information, see [Notifications](/tidb-cloud/notifications.md).

## January 2, 2025

**General changes**

- Support creating TiDB node groups for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters to enhance resource management flexibility. 

    For more information, see [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md).

- Support connecting [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters to generic Kafka in AWS and Google Cloud through Private Connect (beta).

    Private Connect leverages Private Link or Private Service Connect technologies from cloud providers to enable changefeeds in the TiDB Cloud VPC to connect to Kafka in customers' VPCs using private IP addresses, as if those Kafkas were hosted directly within the TiDB Cloud VPC. This feature helps prevent VPC CIDR conflicts and meets security compliance requirements.

    - For Apache Kafka in AWS, follow the instructions in [Set Up Self-Hosted Kafka Private Link Service in AWS](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md) to configure the network connection.

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
