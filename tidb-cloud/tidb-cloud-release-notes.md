---
title: TiDB Cloud Release Notes in 2025
summary: Learn about the release notes of TiDB Cloud in 2025.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2025

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2025.

## October 14, 2025

**General changes**

- **TiDB Cloud Starter**

    - [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) no longer supports database audit logging.

        Currently, only [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) support database audit logging. Existing TiDB Cloud Starter clusters currently using database audit logging are not affected.

    - [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) removes the in-place restore feature, which means you can no longer restore a backup directly to the same cluster. This change helps prevent accidental overwrites of active production data and potential data loss.

        To restore your data, you can [restore the backup to a new cluster](/tidb-cloud/backup-and-restore-serverless.md#perform-the-restore). After validating the restored data, switch your application to the new cluster. Previously restored data in existing clusters remains intact, and no action is required unless you perform a new restore.

        For safer restore and migration workflows with more control and flexibility, consider using [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential).

    - The [**Metrics**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) page for [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) adds the following metrics for faster diagnosis and capacity planning:

        - `Lock-wait (P95/P99)`: monitors lock wait time percentiles to surface contention hotspots.
        - `Idle Connection Duration (P99 incl. not/in txn)`: identifies long-lived idle connections, both in-transaction and not-in-transaction, to adjust pooler limits and timeouts.

- **TiDB Cloud Essential**

    <CustomContent language="en,zh">

    - [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) is in public preview on AWS and Alibaba Cloud.

        For applications experiencing growing workloads and needing scalability in real time, TiDB Cloud Essential provides the flexibility and performance to keep pace with your business growth.

        For more information, see [TiDB Cloud Essential: Now Available on AWS and Alibaba Cloud](https://www.pingcap.com/blog/tidb-cloud-essential-now-available-public-preview-aws-alibaba-cloud/).

    </CustomContent>

    <CustomContent language="ja">

    - [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) is in public preview on AWS.

        For applications experiencing growing workloads and needing scalability in real time, TiDB Cloud Essential provides the flexibility and performance to keep pace with your business growth.

    </CustomContent>

    - Database audit logging is now available in the [TiDB Cloud console](https://tidbcloud.com) for TiDB Cloud Essential and supports customizing rotation settings.

        You can configure database audit logs to be stored in TiDB Cloud, Amazon S3, Google Cloud Storage, Azure Blob Storage, or Alibaba Cloud OSS.

        Currently, this feature is in beta. For more information, see [Database Audit Logging for TiDB Cloud Essential](/tidb-cloud/essential-database-audit-logging.md).

    - TiDB Cloud Essential adds a new event `ResourceLimitation` that notifies you when Request Capacity Units (RCUs) consumption of your cluster reaches the configured maximum multiple times within one hour.

        Usage exceeding the limit might be throttled. To avoid service impact, consider increasing the maximum RCU.

        For more information about events, see [TiDB Cloud Cluster Events](/tidb-cloud/tidb-cloud-events.md).

    - The [**Metrics**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) page for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) adds the following metrics for faster diagnosis and capacity planning:

        - `Capacity vs Usage (RU/s)`: visualizes provisioned Request Unit (RU) capacity versus actual RU consumption to spot headroom and tune autoscaling.
        - `Lock-wait (P95/P99)`: monitors lock wait time percentiles to surface contention hotspots.
        - `Idle Connection Duration (P99 incl. not/in txn)`: identifies long-lived idle connections, both in-transaction and not-in-transaction, to adjust pooler limits and timeouts.

      For more information, see [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md).

## September 30, 2025

**General changes**

- **TiDB Cloud Dedicated**

    - Datadog and New Relic integrations are now generally available (GA) for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.
  
        TiDB Cloud now manages Datadog and New Relic integrations at the cluster level, offering more granular control and configuration. This feature enables you to seamlessly ship the metrics of your [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster to Datadog or New Relic, allowing for advanced alerting in a unified platform.
  
        For integration steps, see [Integrate TiDB Cloud with Datadog](/tidb-cloud/monitor-datadog-integration.md) and [Integrate TiDB Cloud with New Relic](/tidb-cloud/monitor-new-relic-integration.md).
  
        To migrate existing Datadog and New Relic integrations to the cluster level, see [Migrate Datadog and New Relic Integrations](/tidb-cloud/migrate-metrics-integrations.md).

## September 23, 2025

**General changes**

- **TiDB Cloud Dedicated**

    - Support user-controlled splitting of `UPDATE` events in [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) changefeeds.
  
        In TiDB Cloud Dedicated clusters, you can configure whether to keep `UPDATE` events as raw events or split them into separate `DELETE` and `INSERT` events. This feature provides greater flexibility for advanced replication scenarios. 
  
        This feature is supported only for non-SQL destinations such as Apache Kafka and Amazon S3. For more information, see [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md), [Sink to Apache Pulsar](/tidb-cloud/changefeed-sink-to-apache-pulsar.md), and [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md).

        For more information about the splitting behavior, see [Split primary or unique key `UPDATE` events for non-MySQL sinks](https://docs.pingcap.com/tidb/stable/ticdc-split-update-behavior/#split-primary-or-unique-key-update-events-for-non-mysql-sinks).

    - Provide a new node size for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on Google Cloud: `32 vCPU, 64 GiB`.
  
        This new node size is available for TiDB nodes.

## September 16, 2025

**General changes**

- **TiDB Cloud Dedicated**

    - Encryption at Rest with Customer-Managed Encryption Keys (CMEK) is available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on Azure.
  
        This feature enables you to secure your data at rest by using an encryption key that you control. CMEK provides the following benefits:
  
        - Data security: you own and manage the encryption key, which ensures that your data is protected and under your control.
        - Compliance: using CMEK helps you meet regulatory and compliance requirements for data encryption.
        - Flexibility: you can enable CMEK when you create a project and complete CMEK configurations before you create a cluster.
  
      To enable this feature, perform the following steps:
  
        1. In the [TiDB Cloud console](https://tidbcloud.com), create a CMEK-enabled project.
        2. Complete the CMEK configuration for the project.
        3. Create a TiDB Cloud Dedicated cluster hosted on Azure in the same region as your CMEK configuration.
  
      For more information, see [Encryption at Rest Using Customer-Managed Encryption Keys on Azure](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md).

## September 9, 2025

**High availability changes**

- **TiDB Cloud Starter**

    - For newly created [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters, only zonal high availability is enabled, and it is not configurable.
    - For existing TiDB Cloud Starter clusters with regional high availability enabled before **September 9, 2025**, regional high availability remains supported and is not affected.

<CustomContent language="en,zh">

- **TiDB Cloud Essential**

    - For newly created [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) clusters, regional high availability is enabled by default, and you can change it to zonal high availability as needed during cluster creation.

  For more information, see [High Availability in TiDB Cloud Starter and Essential](/tidb-cloud/serverless-high-availability.md).

</CustomContent>

## September 2, 2025

**General changes**

<CustomContent language="en,zh">

- **TiDB Cloud Essential**

    - Support three new Alibaba Cloud regions for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) clusters: `Jakarta (ap-southeast-5)`, `Mexico (na-south-1)`, and `Tokyo (ap-northeast-1)`.

- **TiDB Cloud Dedicated**

    - Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.5.2](https://docs.pingcap.com/tidb/v8.5/release-8.5.2/) to [v8.5.3](https://docs.pingcap.com/tidb/v8.5/release-8.5.3/).

</CustomContent>

<CustomContent language="ja">

- **TiDB Cloud Dedicated**

    - Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.5.2](https://docs.pingcap.com/tidb/v8.5/release-8.5.2/) to [v8.5.3](https://docs.pingcap.com/tidb/v8.5/release-8.5.3/).

</CustomContent>

## August 26, 2025

**General changes**

- **TiDB Cloud Starter**

    - Introduce Auto Embedding (Beta) in [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless), making it simple to convert your text into vectors without additional setup. This feature enables faster development of semantic search, RAG, reranking, and classification in TiDB Cloud with less integration overhead.

        - **Auto Embedding with popular LLM providers**: Amazon Titan, OpenAI, Cohere, Gemini, Jina AI, Hugging Face, and NVIDIA NIM.
        - **Native integration with AWS Bedrock**: managed embedding models with a free quota, including Amazon Titan and Cohere text embedding models from AWS Bedrock.
        - **SQL and Python support**, with code examples for creating, storing, and querying embeddings.

      For more information, see [Auto Embedding](https://docs.pingcap.com/tidbcloud/vector-search-auto-embedding-overview/?plan=starter).

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) no longer supports the Index Insight (beta) feature.

        It is recommended that you use [Index Advisor](/index-advisor.md) instead, which is available for TiDB v8.5.0 and later versions. Index Advisor introduces the `RECOMMEND INDEX` SQL statement, which helps optimize your workload by recommending indexes that improve query performance.

    - You can now manually disable the Point-in-time Restore feature on [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters with weekly backups enabled.

        This enhancement helps reduce costs for clusters that do not require Point-in-time Restore for high RPO protection.

        For more information, see [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md).

## August 12, 2025

**General changes**

<CustomContent language="en,zh">

- **TiDB Cloud Starter**

    - Rename "TiDB Cloud Serverless" to "TiDB Cloud Starter".

        The auto-scaling entry plan is now named "TiDB Cloud Starter" to better reflect its role for new users. All features, pricing, and the free usage quota remain unchanged.

        Starting August 12, 2025 (PDT), your existing Serverless clusters will appear as Starter in the [TiDB Cloud console](https://tidbcloud.com). Your connection strings, endpoints, and data will remain unchanged, so you do not need to make any code changes or schedule downtime.

    - TiDB Cloud Starter is in preview on Alibaba Cloud.

- **TiDB Cloud Essential**

    [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) is in preview on Alibaba Cloud.

    TiDB Cloud Essential on Alibaba Cloud has been in a limited public preview since May 2025. This is the first time Essential is officially included in the release notes. At this stage, Essential on Alibaba Cloud offers a feature set aligned with Starter, available in the Alibaba Cloud Singapore region.

    How to try it:

    - From the [TiDB Cloud console](https://tidbcloud.com/), choose Alibaba Cloud as the cloud provider  when creating a cluster to view the Essential option.
    - You can also access Essential via the [Alibaba Cloud Marketplace listing](https://www.alibabacloud.com/en/marketplace/tidb?_p_lc=1).

  Next, we plan to expand region coverage on Alibaba Cloud and add AWS support.

    If you try Essential on Alibaba Cloud during this preview, you can share feedback through our web console or join our community on [Slack](https://tidbcommunity.slack.com/archives/CH7TTLL7P) or [Discord](https://discord.gg/ukhXbn69Nx).

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) on Google Cloud now supports more than 8 Google Private Service Connect (PSC) connections per region by optimizing the NAT subnet allocation strategy.

        For more information, see [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions).

    - Optimize [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) metrics:

        - In the [**Advanced**](/tidb-cloud/built-in-monitoring.md#advanced) category, add the **Affected Rows**, **Leader Count**, and **Region Count** metrics to improve diagnostics.
        - In the [**Server**](/tidb-cloud/built-in-monitoring.md#server) category, refine the **TiKV IO Bps** metric to improve accuracy and consistency.

      For more information, see [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md).

</CustomContent>

<CustomContent language="ja">

- **TiDB Cloud Starter**

    Rename "TiDB Cloud Serverless" to "TiDB Cloud Starter".

    The auto-scaling entry plan is now named "TiDB Cloud Starter" to better reflect its role for new users. All features, pricing, and the free usage quota remain unchanged.

    Starting August 12, 2025 (PDT), your existing Serverless clusters will appear as Starter in the [TiDB Cloud console](https://tidbcloud.com). Your connection strings, endpoints, and data will remain unchanged, so you do not need to make any code changes or schedule downtime.

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) on Google Cloud now supports more than 8 Google Private Service Connect (PSC) connections per region by optimizing the NAT subnet allocation strategy.

        For more information, see [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md#restrictions).

    - Optimize [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) metrics:

        - In the [**Advanced**](/tidb-cloud/built-in-monitoring.md#advanced) category, add the **Affected Rows**, **Leader Count**, and **Region Count** metrics to improve diagnostics.
        - In the [**Server**](/tidb-cloud/built-in-monitoring.md#server) category, refine the **TiKV IO Bps** metric to improve accuracy and consistency.

      For more information, see [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md).

</CustomContent>

**API changes**

- Introduce TiDB Cloud Dedicated API (v1beta1) for managing the following resources automatically and efficiently:

    - **Cluster**: manage your TiDB Cloud Dedicated clusters with greater flexibility.
    - **Region**: show all available cloud regions in which you can deploy your TiDB Cloud Dedicated cluster.
    - **Private endpoint connection**: set up secure and private connections for your clusters.
    - **Import**: manage data import tasks for your clusters.

  For more information, see [TiDB Cloud Dedicated API](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated/).

- Introduce TiDB Cloud Starter and Essential API (v1beta1) for managing the following resources automatically and efficiently:

    - **Cluster**: manage your TiDB Cloud Starter or Essential clusters with greater flexibility.
    - **Branch**: manage the branches of your clusters.
    - **Export**: manage data export tasks for your clusters.
    - **Import**: manage data import tasks for your clusters.

  For more information, see [TiDB Cloud Starter and Essential API](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless/).

- TiDB Cloud IAM API (v1beta1) supports role-based access control (RBAC) for API key management at both the organization and project levels.

    You can set API key roles at the organization level or project level to improve security and access control.

    For more information, see [TiDB Cloud IAM API](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam/).

## July 31, 2025

**General changes**

- Enhanced Datadog and New Relic integrations are now available for preview.

    Key enhancements:

    - Rebuild the integration backend with the optimized isolation architecture to minimize metric gaps.
    - Add more monitoring metrics based on user needs.
    - Refine metric rules for better consistency.

  These enhancements deliver more accurate monitoring and strengthen the reliability of Datadog and New Relic integrations.

  Rollout plan:

  This preview version is now available to organizations without existing Datadog or New Relic integrations. For organizations with existing Datadog or New Relic integrations, we will proactively reach out to you to coordinate a suitable migration plan and timeline next month.

  For more information, see [Integrate TiDB Cloud with Datadog (Preview)](/tidb-cloud/monitor-datadog-integration.md) and [Integrate TiDB Cloud with New Relic (Preview)](/tidb-cloud/monitor-new-relic-integration.md).

## July 22, 2025

**General changes**

- Provide a new node size for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on Google Cloud: `32 vCPU, 128 GiB`.

    This new size is available for TiDB, TiKV, and TiFlash nodes.

- Improve the TiKV scaling process in [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) to enhance cluster stability.

    When you [change the vCPU and RAM size](/tidb-cloud/scale-tidb-cluster.md#change-vcpu-and-ram) of TiKV nodes, TiDB Cloud automatically checks whether the cluster's internal service requires additional capacity to support the new configuration.

    - If an expansion is required, TiDB Cloud prompts you for confirmation before proceeding.
    - If the current internal service capacity is already larger than the required size after scaling, TiDB Cloud retains the existing configuration of the internal service to avoid unnecessary changes that might affect cluster stability.

**Console changes**

- Enhance the cloud storage data import experience for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters.

    The import process is now streamlined into a 3-step wizard with intelligent pre-checks. This new wizard guides you through connection setup, file mapping, and bucket scanning. With the scanning, TiDB Cloud shows you exactly which files will be imported and their target destinations before the import, significantly reducing configuration complexity and preventing import failures.

    For more information, see the following documentation:

    - [Import Sample Data into TiDB Cloud Serverless](/tidb-cloud/import-sample-data-serverless.md)
    - [Import CSV Files from Cloud Storage into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md)
    - [Import Apache Parquet Files from Cloud Storage into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md)

## July 15, 2025

**General changes**

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.1.2](https://docs.pingcap.com/tidb/stable/release-8.1.2/) to [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/).

    Compared with v8.1.2, v8.5.2 includes new features, improvements, and bug fixes released in [v8.2.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.2.0/), [v8.3.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.3.0/), [v8.4.0-DMR](https://docs.pingcap.com/tidb/stable/release-8.4.0/), [v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/), [v8.5.1](https://docs.pingcap.com/tidb/stable/release-8.5.1/), and [v8.5.2](https://docs.pingcap.com/tidb/stable/release-8.5.2/).

- Support auditing the `BackupCompleted` event to enhance console audit logging for backup activities.

    This enhancement lets you log backup completion activities to meet security and compliance requirements.

    For more information, see [Console Audit Logging](/tidb-cloud/tidb-cloud-console-auditing.md).

- Support filtering column values in [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) changefeeds.

    You can now use expressions to filter specific column values in changefeeds to exclude irrelevant data at the source. This feature enables fine-grained filtering of DML events, helping you reduce resource consumption and improve performance.

    For more information, see [Changefeed](/tidb-cloud/changefeed-overview.md).

## June 24, 2025

**General changes**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) database audit logging (beta) is now available upon request. This feature lets you record a history of user access details (such as any SQL statements executed) in logs.

    To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for TiDB Cloud Serverless database audit logging" in the Description field and click **Submit**.

    For more information, see [TiDB Cloud Serverless Database Audit Logging](/tidb-cloud/serverless-audit-logging.md).

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) supports user-controlled log redaction.

    You can now enable or disable log redaction for your TiDB Cloud Dedicated clusters to manage the redaction status of cluster logs by yourself.

    For more information, see [User-Controlled Log Redaction](/tidb-cloud/tidb-cloud-log-redaction.md).

- Encryption at Rest with Customer-Managed Encryption Keys (CMEK) is now generally available (GA) for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on AWS.

    This feature enables you to secure your data at rest by leveraging a symmetric encryption key that you manage through Key Management Service (KMS).

    For more information, see [Encryption at Rest Using Customer-Managed Encryption Keys on AWS](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md).

## June 17, 2025

**General changes**

- For [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters, the maximum storage size of TiKV nodes with 16 vCPU and 32 vCPU is changed from **6144 GiB** to **4096 GiB**. 

    For more information, see [TiKV node storage size](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size).

**Console changes**

- Revamp the left navigation pane to improve the overall navigation experience.
  
    - A new <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg> icon is now available in the upper-left corner, letting you easily hide or show the left navigation pane whenever you need.
    - A combo box is now available in the upper-left corner, letting you quickly switch between organizations, projects, and clusters, all from one central location.
  
        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    - The entries shown on the left navigation pane now dynamically adapt to your current selection in the combo box, helping you focus on the most relevant functionalities.
    - For your quick access, **Support**, **Notification**, and your account entries are now consistently displayed at the bottom of the left navigation pane on all console pages.

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

- Upgrade the TiDB version of [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters from [v7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3) to [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2).

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
