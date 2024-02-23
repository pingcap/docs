---
title: TiDB Cloud Release Notes in 2024
summary: Learn about the release notes of TiDB Cloud in 2024.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2024

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2024.

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
