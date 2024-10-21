---
title: TiDB Cloud Release Notes in 2024
summary: Learn about the release notes of TiDB Cloud in 2024.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2024

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2024.

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

- [Data Service (beta)](https://tidbcloud.com/console/data-service) supports automatically generating vector search endpoints.

    If your table contains [vector data types](/vector-search-data-types.md), you can automatically generate a vector search endpoint that calculates vector distances based on your selected distance function.

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

- [Data Service (beta)](https://tidbcloud.com/console/data-service) provides an endpoint library with predefined system endpoints that you can directly add to your Data App, reducing the effort in your endpoint development.

    Currently, the library only includes the `/system/query` endpoint, which enables you to execute any SQL statement by simply passing the statement in the predefined `sql` parameter. This endpoint facilitates the immediate execution of SQL queries, enhancing flexibility and efficiency.

    For more information, see [Add a predefined system endpoint](/tidb-cloud/data-service-manage-endpoint.md#add-a-predefined-system-endpoint).

- Enhance slow query data storage.

    The slow query access on the [TiDB Cloud console](https://tidbcloud.com) is now more stable and does not affect database performance.

## June 25, 2024

**General changes**

- [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) supports vector search (beta).

    The vector search (beta) feature provides an advanced search solution for performing semantic similarity searches across various data types, including documents, images, audio, and video. This feature enables developers to easily build scalable applications with generative artificial intelligence (AI) capabilities using familiar MySQL skills. Key features include:

    - [Vector data types](/vector-search-data-types.md), [vector index](/vector-search-index.md), and [vector functions and operators](/vector-search-functions-and-operators.md).
    - Ecosystem integrations with [LangChain](/vector-search-integrate-with-langchain.md), [LlamaIndex](/vector-search-integrate-with-llamaindex.md), and [JinaAI](/vector-search-integrate-with-jinaai-embedding.md).
    - Sample applications and tutorials: perform semantic searches for documents using [Python](/vector-search-get-started-using-python.md) or [SQL](/vector-search-get-started-using-sql.md).

  For more information, see [Vector search (beta) overview](/vector-search-overview.md).

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

- [Data Service (beta)](https://tidbcloud.com/console/data-service) supports path parameters alongside query parameters.

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

    For more information, see [Cluster plans](/tidb-cloud/select-cluster-tier.md#cluster-plans).

- Modify the throttling behavior for TiDB Cloud Serverless clusters upon reaching their usage quota. Now, once a cluster reaches its usage quota, it immediately denies any new connection attempts, thereby ensuring uninterrupted service for existing operations.

    For more information, see [Usage quota](/tidb-cloud/serverless-limitations.md#usage-quota).

## March 5, 2024

**General changes**

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0) to [v7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1).

**Console changes**

- Introduce the **Cost Explorer** tab on the [**Billing**](https://tidbcloud.com/console/org-settings/billing/payments) page, which provides an intuitive interface for analyzing and customizing cost reports for your organization over time.

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

- [Data Service (beta)](https://tidbcloud.com/console/data-service) supports configuring a custom domain to access endpoints in a Data App.

    By default, TiDB Cloud Data Service provides a domain `<region>.data.tidbcloud.com` to access each Data App's endpoints. For enhanced personalization and flexibility, you can now configure a custom domain for your Data App instead of using the default domain. This feature enables you to use branded URLs for your database services and enhances security.

    For more information, see [Custom domain in Data Service](/tidb-cloud/data-service-custom-domain.md).

## January 3, 2024

**General changes**

- Support [Organization SSO](https://tidbcloud.com/console/preferences/authentication) to streamline enterprise authentication processes.

    With this feature, you can seamlessly integrate TiDB Cloud with any identity provider (IdP) using [Security Assertion Markup Language (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) or [OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/).

    For more information, see [Organization SSO Authentication](/tidb-cloud/tidb-cloud-org-sso-authentication.md).

- Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1) to [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0).

- The dual region backup feature for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) is now in General Availability (GA).

    By using this feature, you can replicate backups across geographic regions within AWS or Google Cloud. This feature provides an additional layer of data protection and disaster recovery capabilities.

    For more information, see [Dual region backup](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup).
