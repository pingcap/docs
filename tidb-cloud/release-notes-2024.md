---
title: TiDB Cloud Release Notes in 2024
summary: Learn about the release notes of TiDB Cloud in 2024.
---

# TiDB Cloud Release Notes in 2024

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2024.

## December 17, 2024

**General changes**

- TiDB Cloud Serverless backup and restore changes

    - Support restoring data to a new cluster, providing greater flexibility and ensuring your current cluster's operations remain uninterrupted.

    - Refine backup and restore strategies to align with your cluster plan. For more information, see [Back Up and Restore TiDB Cloud Serverless Data](/tidb-cloud/backup-and-restore-serverless.md#learn-about-the-backup-setting).

    - Apply the following compatibility policy to help you transition smoothly:

        - Backups created before 2024-12-17T10:00:00Z will follow the previous retention duration across all clusters.
        - The backup time of scalable clusters will retain the current configurations, while the backup time of free clusters will be reset to default settings.

## December 3, 2024

**General changes**

- Introduce the Recovery Group feature (beta) for disaster recovery of [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters deployed on AWS.

    This feature enables you to replicate your databases between TiDB Cloud Dedicated clusters, ensuring rapid recovery in the event of a regional disaster. If you are in the Project Owner role, you can enable this feature by creating a new recovery group and assigning databases to the group. By replicating databases with recovery groups, you can improve disaster readiness, meet stricter availability SLAs, and achieve more aggressive Recovery Point Objectives (RPO) and Recovery Time Objectives (RTO).
  
    For more information, see [Get started with recovery groups](/tidb-cloud/recovery-group-get-started.md).

## November 26, 2024

**General changes**

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4) to [v8.1.1](https://docs.pingcap.com/tidb/stable/release-8.1.1).

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) reduces costs for large data writes by up to 80% for the following scenarios:

    - When you perform write operations larger than 16 MiB in [autocommit mode](/transaction-overview.md#autocommit).
    - When you perform write operations larger than 16 MiB in [optimistic transaction model](/optimistic-transaction.md).
    - When you [import data into TiDB Cloud](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud).

  This improvement enhances the efficiency and cost-effectiveness of your data operations, providing greater savings as your workload scales.

## November 19, 2024

**General changes**

- [TiDB Cloud Serverless branching (beta)](/tidb-cloud/branch-overview.md) introduces the following improvements to branch management:

    - **Flexible branch creation**: When creating a branch, you can select a specific cluster or branch as the parent and specify a precise point in time to use from the parent. This gives you precise control over the data in your branch.

    - **Branch reset**: You can reset a branch to synchronize it with the latest state of its parent.

    - **Improved GitHub integration**: The [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) GitHub App introduces the [`branch.mode`](/tidb-cloud/branch-github-integration.md#branchmode) parameter, which controls the behavior during pull request synchronization. In the default mode `reset`, the app resets the branch to match the latest changes in the pull request.

  For more information, see [Manage TiDB Cloud Serverless Branches](/tidb-cloud/branch-manage.md) and [Integrate TiDB Cloud Serverless Branching (Beta) with GitHub](/tidb-cloud/branch-github-integration.md).

## November 12, 2024

**General changes**

- Add the pause duration limit for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

    TiDB Cloud Dedicated now limits the maximum pause duration to 7 days. If you do not manually resume the cluster within 7 days, TiDB Cloud will automatically resume it.

    This change applies only to **organizations created after November 12, 2024**. Organizations created on or before this date will gradually transition to the new pause behavior with prior notification.

    For more information, see [Pause or Resume a TiDB Cloud Dedicated Cluster](/tidb-cloud/pause-or-resume-tidb-cluster.md).

- [Datadog integration (beta)](/tidb-cloud/monitor-datadog-integration.md) adds support for a new region: `AP1` (Japan).

- Support a new AWS region for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters: `Mumbai (ap-south-1)`.

- Remove support for the AWS `São Paulo (sa-east-1)` region for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## October 29, 2024

**General changes**

- New metric: add `tidbcloud_changefeed_checkpoint_ts` for Prometheus integration.

    This metric tracks the checkpoint timestamp of a changefeed, representing the largest TSO (Timestamp Oracle) successfully written to the downstream. For more information on available metrics, see [Integrate TiDB Cloud with Prometheus and Grafana (Beta)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus).

## October 22, 2024

**General changes**

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3) to [v7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4).

## October 15, 2024

**API changes**

* [MSP](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp) is deprecated as of October 15, 2024, and will be removed in the future. If you are currently using the MSP API, migrate to the Partner Management API in [TiDB Cloud Partner](https://partner-console.tidbcloud.com/signin).

## September 24, 2024

**General changes**

- Provide a new [TiFlash vCPU and RAM size](/tidb-cloud/size-your-cluster.md#tiflash-vcpu-and-ram) for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on AWS: `32 vCPU, 128 GiB`

**CLI changes**

- Release [TiDB Cloud CLI v1.0.0-beta.2](https://github.com/tidbcloud/tidbcloud-cli/releases/tag/v1.0.0-beta.2).

    TiDB Cloud CLI provides the following new features:

    - Support SQL user management for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters via [`ticloud serverless sql-user`](/tidb-cloud/ticloud-serverless-sql-user-create.md).
    - Allow disabling the public endpoint for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters in [`ticloud serverless create`](/tidb-cloud/ticloud-cluster-create.md) and [`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md).
    - Add the [`ticloud auth whoami`](/tidb-cloud/ticloud-auth-whoami.md) command to get information about the current user when using OAuth authentication.
    - Support `--sql`, `--where`, and `--filter` flags in [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md) to choose source tables flexibly.
    - Support exporting data to CSV and Parquet files.
    - Support exporting data to Amazon S3 using role ARN as credentials, and also support exporting to Google Cloud Storage and Azure Blob Storage.
    - Support importing data from Amazon S3, Google Cloud Storage, and Azure Blob Storage.
    - Support creating a branch from a branch and a specific timestamp.

  TiDB Cloud CLI enhances the following features:

    - Improve debug logging. Now it can log credentials and user-agent.
    - Speed up local export file downloads from tens of KiB per second to tens of MiB per second.

  TiDB Cloud CLI replaces or removes the following features:

    - The `--s3.bucket-uri` flag is replaced by `--s3.uri` in [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md).
    - The `--database` and `--table` flags are removed in [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md). Instead, you can use `--sql`, `--where`, and `--filter` flags.
    - [`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md) cannot update the annotations field anymore.

## September 10, 2024

**General changes**

- Launch the TiDB Cloud Partner Web Console and Open API to enhance resource and billing management for TiDB Cloud partners.

    Managed Service Providers (MSPs) and resellers through AWS Marketplace Channel Partner Private Offer (CPPO) can now leverage the [TiDB Cloud Partner Web Console](https://partner-console.tidbcloud.com/) and Open API to streamline their daily operations.

    For more information, see [TiDB Cloud Partner Web Console](/tidb-cloud/tidb-cloud-partners.md).

## September 3, 2024

**Console changes**

- Support exporting data from TiDB Cloud Serverless clusters using the [TiDB Cloud console](https://tidbcloud.com/). 
  
    Previously, TiDB Cloud only supported exporting data using the [TiDB Cloud CLI](/tidb-cloud/cli-reference.md). Now, you can easily export data from TiDB Cloud Serverless clusters to local files and Amazon S3 in the [TiDB Cloud console](https://tidbcloud.com/). 
  
    For more information, see [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md) and [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md).

- Enhance the connection experience for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

    - Revise the **Connect** dialog interface to provide TiDB Cloud Dedicated users with a more streamlined and efficient connection experience.
    - Introduce a new cluster-level **Networking** page to simplify network configuration for your cluster.
    - Replace the **Security Settings** page with a new **Password Settings** page and move IP access list settings to the new **Networking** page.
  
  For more information, see [Connect to TiDB Cloud Dedicated](/tidb-cloud/connect-to-tidb-cluster.md).

- Enhance the data import experience for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters:

    - Refine the layout of the **Import** page with a clearer layout.
    - Unify the import steps for TiDB Cloud Serverless and TiDB Cloud Dedicated clusters.
    - Simplify the AWS Role ARN creation process for easier connection setup.

  For more information, see [Import data from files to TiDB Cloud](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud).

## August 20, 2024

**Console changes**

- Refine the layout of the **Create Private Endpoint Connection** page to improve the user experience for creating new private endpoint connections in [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

    For more information, see [Connect to a TiDB Cloud Dedicated Cluster via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections.md) and [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md).

## August 6, 2024

**General changes**

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) billing changes for load balancing on AWS.

    Starting from August 1, 2024, TiDB Cloud Dedicated bills include new AWS charges for public IPv4 addresses, aligned with [AWS pricing changes effective from February 1, 2024](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/). The charge for each public IPv4 address is $0.005 per hour, which will result in approximately $10 per month for each TiDB Cloud Dedicated cluster hosted on AWS.

    This charge will appear under the existing **TiDB Cloud Dedicated - Data Transfer - Load Balancing** service in your [billing details](/tidb-cloud/tidb-cloud-billing.md#billing-details).

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2) to [v7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3).

**Console changes**

- Enhance the cluster size configuration experience for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated).

    Refine the layout of the **Cluster Size** section on the [**Create Cluster**](/tidb-cloud/create-tidb-cluster.md) and [**Modify Cluster**](/tidb-cloud/scale-tidb-cluster.md) pages for TiDB Cloud Dedicated clusters. In addition, the **Cluster Size** section now includes links to node size recommendation documents, which helps you select an appropriate cluster size.

## July 23, 2024

**General changes**

- [Data Service (beta)](https://tidbcloud.com/project/data-service) supports automatically generating vector search endpoints.

    If your table contains [vector data types](/vector-search/vector-search-data-types.md), you can automatically generate a vector search endpoint that calculates vector distances based on your selected distance function.

    This feature enables seamless integration with AI platforms such as [Dify](https://docs.dify.ai/guides/tools) and [GPTs](https://openai.com/blog/introducing-gpts), enhancing your applications with advanced natural language processing and AI capabilities for more complex tasks and intelligent solutions.

    For more information, see [Generate an endpoint automatically](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically) and [Integrate a Data App with Third-Party Tools](/tidb-cloud/data-service-integrations.md).

- Introduce the budget feature to help you track actual TiDB Cloud costs against planned expenses, preventing unexpected costs.

    To access this feature, you must be in the `Organization Owner` or `Organization Billing Admin` role of your organization.

    For more information, see [Manage budgets for TiDB Cloud](/tidb-cloud/tidb-cloud-budget.md).

## July 9, 2024

**General changes**

- Enhance the [System Status](https://status.tidbcloud.com/) page to provide better insights into TiDB Cloud system health and performance.

    To access it, visit <https://status.tidbcloud.com/> directly, or navigate via the [TiDB Cloud console](https://tidbcloud.com) by clicking **?** in the lower-right corner and selecting **System Status**.

**Console changes**

- Refine the **VPC Peering** page layout to improve the user experience for [creating VPC Peering connections](/tidb-cloud/set-up-vpc-peering-connections.md) in [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

## July 2, 2024

**General changes**

- [Data Service (beta)](https://tidbcloud.com/project/data-service) provides an endpoint library with predefined system endpoints that you can directly add to your Data App, reducing the effort in your endpoint development.

    Currently, the library only includes the `/system/query` endpoint, which enables you to execute any SQL statement by simply passing the statement in the predefined `sql` parameter. This endpoint facilitates the immediate execution of SQL queries, enhancing flexibility and efficiency.

    For more information, see [Add a predefined system endpoint](/tidb-cloud/data-service-manage-endpoint.md#add-a-predefined-system-endpoint).

- Enhance slow query data storage.

    The slow query access on the [TiDB Cloud console](https://tidbcloud.com) is now more stable and does not affect database performance.

## June 25, 2024

**General changes**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) supports vector search (beta).

    The vector search (beta) feature provides an advanced search solution for performing semantic similarity searches across various data types, including documents, images, audio, and video. This feature enables developers to easily build scalable applications with generative artificial intelligence (AI) capabilities using familiar MySQL skills. Key features include:

    - [Vector data types](/vector-search/vector-search-data-types.md), [vector index](/vector-search/vector-search-index.md), and [vector functions and operators](/vector-search/vector-search-functions-and-operators.md).
    - Ecosystem integrations with [LangChain](/vector-search/vector-search-integrate-with-langchain.md), [LlamaIndex](/vector-search/vector-search-integrate-with-llamaindex.md), and [JinaAI](/vector-search/vector-search-integrate-with-jinaai-embedding.md).
    - Programming language support for Python: [SQLAlchemy](/vector-search/vector-search-integrate-with-sqlalchemy.md), [Peewee](/vector-search/vector-search-integrate-with-peewee.md), and [Django ORM](/vector-search/vector-search-integrate-with-django-orm.md).
    - Sample applications and tutorials: perform semantic searches for documents using [Python](/vector-search/vector-search-get-started-using-python.md) or [SQL](/vector-search/vector-search-get-started-using-sql.md).

  For more information, see [Vector search (beta) overview](/vector-search/vector-search-overview.md).

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) now offers weekly email reports for organization owners.

    These reports provide insights into the performance and activity of your clusters. By receiving automatic weekly updates, you can stay informed about your clusters and make data-driven decisions to optimize your clusters.

- Release Chat2Query API v3 endpoints and deprecate the Chat2Query API v1 endpoint `/v1/chat2data`.

    With Chat2Query API v3 endpoints, you can start multi-round Chat2Query by using sessions.

    For more information, see [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md).

**Console changes**

- Rename Chat2Query (beta) to SQL Editor (beta).

    The interface previously known as Chat2Query is renamed to SQL Editor. This change clarifies the distinction between manual SQL editing and AI-assisted query generation, enhancing usability and your overall experience.

    - **SQL Editor**: the default interface for manually writing and executing SQL queries in the TiDB Cloud console.
    - **Chat2Query**: the AI-assisted text-to-query feature, which enables you to interact with your databases using natural language to generate, rewrite, and optimize SQL queries.

  For more information, see [Explore your data with AI-assisted SQL Editor](/tidb-cloud/explore-data-with-chat2query.md).

## June 18, 2024

**General changes**

- Increase the maximum node storage of 16 vCPU TiFlash and 32 vCPU TiFlash for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from 2048 GiB to 4096 GiB.

    This enhancement increases the analytics data storage capacity of your TiDB Cloud Dedicated cluster, improves workload scaling efficiency, and accommodates growing data requirements.

    For more information, see [TiFlash node storage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage).

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1) to [v7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2).

## June 4, 2024

**General changes**

- Introduce the Recovery Group feature (beta) for disaster recovery of [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters deployed on AWS.

    This feature enables you to replicate your databases between TiDB Cloud Dedicated clusters, ensuring rapid recovery in the event of a regional disaster. If you are in the `Project Owner` role, you can enable this feature by creating a new recovery group and assigning databases to the group. By replicating databases with recovery groups, you can improve disaster readiness, meet stricter availability SLAs, and achieve more aggressive Recovery Point Objectives (RPO) and Recovery Time Objectives (RTO).

    For more information, see [Get started with recovery groups](/tidb-cloud/recovery-group-get-started.md).

- Introduce billing and metering (beta) for the [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) columnar storage [TiFlash](/tiflash/tiflash-overview.md).

    Until June 30, 2024, columnar storage in TiDB Cloud Serverless clusters remains free with a 100% discount. After this date, each TiDB Cloud Serverless cluster will include a free quota of 5 GiB for columnar storage. Usage beyond the free quota will be charged.

    For more information, see [TiDB Cloud Serverless pricing details](https://www.pingcap.com/tidb-serverless-pricing-details/#storage).

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) supports [Time to live (TTL)](/time-to-live.md).

## May 28, 2024

**General changes**

- Google Cloud `Taiwan (asia-east1)` region supports the [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) feature.

    The [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted in the Google Cloud `Taiwan (asia-east1)` region now support the Data Migration (DM) feature. If your upstream data is stored in or near this region, you can now take advantage of faster and more reliable data migration from Google Cloud to TiDB Cloud.

- Provide a new [TiDB node size](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram) for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on AWS and Google Cloud: `16 vCPU, 64 GiB`

**API changes**

- Introduce TiDB Cloud Data Service API for managing the following resources automatically and efficiently:

    * **Data App**: a collection of endpoints that you can use to access data for a specific application.
    * **Data Source**: clusters linked to Data Apps for data manipulation and retrieval.
    * **Endpoint**: a web API that you can customize to execute SQL statements.
    * **Data API Key**: used for secure endpoint access.
    * **OpenAPI Specification**: Data Service supports generating the OpenAPI Specification 3.0 for each Data App, which enables you to interact with your endpoints in a standardized format.

  These TiDB Cloud Data Service API endpoints are released in TiDB Cloud API v1beta1, which is the latest API version of TiDB Cloud.

    For more information, see [API documentation (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice).

## May 21, 2024

**General changes**

- Provide a new [TiDB node size](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram) for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on Google Cloud: `8 vCPU, 16 GiB`

## May 14, 2024

**General changes**

- Expand the selection of time zones in the [**Time Zone**](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization) section to better accommodate customers from diverse regions.

- Support [creating a VPC peering](/tidb-cloud/set-up-vpc-peering-connections.md) when your VPC is in a different region from the VPC of TiDB Cloud.

- [Data Service (beta)](https://tidbcloud.com/project/data-service) supports path parameters alongside query parameters.

    This feature enhances resource identification with structured URLs and improves user experience, search engine optimization (SEO), and client integration, offering developers more flexibility and better alignment with industry standards.

    For more information, see [Basic properties](/tidb-cloud/data-service-manage-endpoint.md#basic-properties).

## April 16, 2024

**CLI changes**

- Introduce [TiDB Cloud CLI 1.0.0-beta.1](https://github.com/tidbcloud/tidbcloud-cli), built upon the new [TiDB Cloud API](/tidb-cloud/api-overview.md). The new CLI brings the following new features:

    - [Export data from TiDB Cloud Serverless clusters](/tidb-cloud/serverless-export.md)
    - [Import data from local storage into TiDB Cloud Serverless clusters](/tidb-cloud/ticloud-import-start.md)
    - [Authenticate via OAuth](/tidb-cloud/ticloud-auth-login.md)
    - [Ask questions via TiDB Bot](/tidb-cloud/ticloud-ai.md)

  Before upgrading your TiDB Cloud CLI, note that this new CLI is incompatible with previous versions. For example, `ticloud cluster` in CLI commands is now updated to `ticloud serverless`. For more information, see [TiDB Cloud CLI reference](/tidb-cloud/cli-reference.md).

## April 9, 2024

**General changes**

- Provide a new [TiDB node size](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram) for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on AWS: `8 vCPU, 32 GiB`.

## April 2, 2024

**General changes**

- Introduce two service plans for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters: **Free** and **Scalable**.

    To meet different user requirements, TiDB Cloud Serverless offers the free and scalable service plans. Whether you are just getting started or scaling to meet the increasing application demands, these plans provide the flexibility and capabilities you need.

    For more information, see [Cluster plans](/tidb-cloud/select-cluster-tier.md).

- Modify the throttling behavior for TiDB Cloud Serverless clusters upon reaching their usage quota. Now, once a cluster reaches its usage quota, it immediately denies any new connection attempts, thereby ensuring uninterrupted service for existing operations.

    For more information, see [Usage quota](/tidb-cloud/serverless-limitations.md#usage-quota).

## March 5, 2024

**General changes**

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0) to [v7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1).

**Console changes**

- Introduce the **Cost Explorer** tab on the [**Billing**](https://tidbcloud.com/org-settings/billing/payments) page, which provides an intuitive interface for analyzing and customizing cost reports for your organization over time.

    To use this feature, navigate to the **Billing** page of your organization and click the **Cost Explorer** tab.

    For more information, see [Cost Explorer](/tidb-cloud/tidb-cloud-billing.md#cost-explorer).

- [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) displays a **limit** label for [node-level resource metrics](/tidb-cloud/built-in-monitoring.md#server).

    The **limit** label shows the maximum usage of resources such as CPU, memory, and storage for each component in a cluster. This enhancement simplifies the process of monitoring the resource usage rate of your cluster.

    To access these metric limits, navigate to the **Monitoring** page of your cluster, and then check the **Server** category under the **Metrics** tab.

    For more information, see [Metrics for TiDB Cloud Dedicated clusters](/tidb-cloud/built-in-monitoring.md#server).

## February 21, 2024

**General changes**

- Upgrade the TiDB version of [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters from [v6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0) to [v7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3).

## February 20, 2024

**General changes**

- Support creating more TiDB Cloud nodes on Google Cloud.

    - By [configuring a regional CIDR size](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) of `/19` for Google Cloud, you can now create up to 124 TiDB Cloud nodes within any region of a project.
    - If you want to create more than 124 nodes in any region of a project, you can contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for assistance in customizing an IP range size ranging from `/16` to `/18`.

## January 23, 2024

**General changes**

- Add 32 vCPU as a node size option for TiDB, TiKV, and TiFlash.

    For each `32 vCPU, 128 GiB` TiKV node, the node storage ranges from 200 GiB to 6144 GiB.

    It is recommended to use such nodes in the following scenarios:

    - High-workload production environments
    - Extremely high performance

## January 16, 2024

**General changes**

- Enhance CIDR configuration for projects.

    - You can directly set a region-level CIDR for each project.
    - You can choose your CIDR configurations from a broader range of CIDR values.

    Note: The previous global-level CIDR settings for projects are retired, but all existing regional CIDR in active state remain unaffected. There will be no impact on the network of existing clusters.

    For more information, see [Set a CIDR for a region](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region).

- TiDB Cloud Serverless users now have the capability to disable public endpoints for your clusters.

    For more information, see [Disable a Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md#disable-a-public-endpoint).

- [Data Service (beta)](https://tidbcloud.com/project/data-service) supports configuring a custom domain to access endpoints in a Data App.

    By default, TiDB Cloud Data Service provides a domain `<region>.data.tidbcloud.com` to access each Data App's endpoints. For enhanced personalization and flexibility, you can now configure a custom domain for your Data App instead of using the default domain. This feature enables you to use branded URLs for your database services and enhances security.

    For more information, see [Custom domain in Data Service](/tidb-cloud/data-service-custom-domain.md).

## January 3, 2024

**General changes**

- Support [Organization SSO](https://tidbcloud.com/org-settings/authentication) to streamline enterprise authentication processes.

    With this feature, you can seamlessly integrate TiDB Cloud with any identity provider (IdP) using [Security Assertion Markup Language (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) or [OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/).

    For more information, see [Organization SSO Authentication](/tidb-cloud/tidb-cloud-org-sso-authentication.md).

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1) to [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0).

- The dual region backup feature for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) is now in General Availability (GA).

    By using this feature, you can replicate backups across geographic regions within AWS or Google Cloud. This feature provides an additional layer of data protection and disaster recovery capabilities.

    For more information, see [Dual region backup](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup).
