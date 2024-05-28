---
title: TiDB Cloud Release Notes in 2024
summary: Learn about the release notes of TiDB Cloud in 2024.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2024

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2024.

## May 28, 2024

**General changes**

- Google Cloud Taiwan (asia-east1) region supports Data Migration (DM)

    The [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters hosted in the Google Cloud Taiwan (asia-east1) region now support the Data Migration (DM) service. You can use this feature to migrate MySQL-compatible databases to a TiDB Dedicated cluster in this region, making the data migration service more efficient and streamlined.

- Provide a new [TiDB node size](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram) for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters hosted on AWS and Google Cloud: `16 vCPU, 64 GiB`

**API changes**

- Introduce TiDB Cloud Data Service API for managing the following resources automatically and efficiently:

    * **Data App**: a collection of endpoints that you can use to access data for a specific application.
    * **Data Source**: clusters linked to Data Apps for data manipulation and retrieval.
    * **Endpoint**: a web API that you can customize to execute SQL statements.
    * **Data API Key**: used for secure endpoint access.
    * **OpenAPI Specification**: Data Service supports generating the OpenAPI Specification 3.0 for each Data App, which enables you to interact with your endpoints in a standardized format.

  These TiDB Cloud Data Service API endpoints are released in TiDB Cloud API v1beta1, which is the latest API version of TiDB Cloud.

    For more information, refer to the [API documentation (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice).

## May 21, 2024

**General changes**

- Provide a new [TiDB node size](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram) for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters hosted on Google Cloud: `8 vCPU, 16 GiB`

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

    - [Export data from TiDB Serverless clusters](/tidb-cloud/serverless-export.md)
    - [Import data from local storage into TiDB Serverless clusters](/tidb-cloud/ticloud-import-start.md)
    - [Authenticate via OAuth](/tidb-cloud/ticloud-auth-login.md)
    - [Ask questions via TiDB Bot](/tidb-cloud/ticloud-ai.md)

  Before upgrading your TiDB Cloud CLI, note that this new CLI is incompatible with previous versions. For example, `ticloud cluster` in CLI commands is now updated to `ticloud serverless`. For more information, see [TiDB Cloud CLI reference](/tidb-cloud/cli-reference.md).

## April 9, 2024

**General changes**

- Provide a new [TiDB node size](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram) for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters hosted on AWS: `8 vCPU, 32 GiB`.

## April 2, 2024

**General changes**

- Introduce two service plans for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters: **Free** and **Scalable**.

    To meet different user requirements, TiDB Serverless offers the free and scalable service plans. Whether you are just getting started or scaling to meet the increasing application demands, these plans provide the flexibility and capabilities you need.

    For more information, see [Cluster plans](/tidb-cloud/select-cluster-tier.md#cluster-plans).

- Modify the throttling behavior for TiDB Serverless clusters upon reaching their usage quota. Now, once a cluster reaches its usage quota, it immediately denies any new connection attempts, thereby ensuring uninterrupted service for existing operations.

    For more information, see [Usage quota](/tidb-cloud/serverless-limitations.md#usage-quota).

## March 5, 2024

**General changes**

- Upgrade the default TiDB version of new [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters from [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0) to [v7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1).

**Console changes**

- Introduce the **Cost Explorer** tab on the [**Billing**](https://tidbcloud.com/console/org-settings/billing/payments) page, which provides an intuitive interface for analyzing and customizing cost reports for your organization over time.

    To use this feature, navigate to the **Billing** page of your organization and click the **Cost Explorer** tab.

    For more information, see [Cost Explorer](/tidb-cloud/tidb-cloud-billing.md#cost-explorer).

- [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) displays a **limit** label for [node-level resource metrics](/tidb-cloud/built-in-monitoring.md#server).

    The **limit** label shows the maximum usage of resources such as CPU, memory, and storage for each component in a cluster. This enhancement simplifies the process of monitoring the resource usage rate of your cluster.

    To access these metric limits, navigate to the **Monitoring** page of your cluster, and then check the **Server** category under the **Metrics** tab.

    For more information, see [Metrics for TiDB Dedicated clusters](/tidb-cloud/built-in-monitoring.md#server).

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

- TiDB Serverless users now have the capability to disable public endpoints for your clusters.

    For more information, see [Disable a Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md#disable-a-public-endpoint).

- [Data Service (beta)](https://tidbcloud.com/console/data-service) supports configuring a custom domain to access endpoints in a Data App.

    By default, TiDB Cloud Data Service provides a domain `<region>.data.tidbcloud.com` to access each Data App's endpoints. For enhanced personalization and flexibility, you can now configure a custom domain for your Data App instead of using the default domain. This feature enables you to use branded URLs for your database services and enhances security.

    For more information, see [Custom domain in Data Service](/tidb-cloud/data-service-custom-domain.md).

## January 3, 2024

**General changes**

- Support [Organization SSO](https://tidbcloud.com/console/preferences/authentication) to streamline enterprise authentication processes.

    With this feature, you can seamlessly integrate TiDB Cloud with any identity provider (IdP) using [Security Assertion Markup Language (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) or [OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/).

    For more information, see [Organization SSO Authentication](/tidb-cloud/tidb-cloud-org-sso-authentication.md).

- Upgrade the default TiDB version of new [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters from [v7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1) to [v7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0).

- The dual region backup feature for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) is now in General Availability (GA).

    By using this feature, you can replicate backups across geographic regions within AWS or Google Cloud. This feature provides an additional layer of data protection and disaster recovery capabilities.

    For more information, see [Dual region backup](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup).
