---
title: TiDB Cloud Release Notes in 2025
summary: Learn about the release notes of TiDB Cloud in 2025.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2025

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2025.

## January 2, 2025

**General changes**

- Support creating TiDB node groups for TiDB Cloud Dedicated clusters to enhance resource management flexibility. For more information, see [Overview of TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md).

- Enhance roles in TiDB Cloud:

    - Introduce the `Project Viewer` and `Organization Billing Viewer` roles to enhance granular access control on TiDB Cloud.

    - Rename the following roles:

        - `Organization Member` to `Organization Viewer`
        - `Organization Billing Admin` to `Organization Billing Manager`
        - `Organization Console Audit Admin` to `Organization Console Audit Manager`

  For more information, see [Identity Access Management](/tidb-cloud/manage-user-access.md#organization-roles).

- Regional high availability (beta) for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters.

    This feature is designed for workloads that require maximum infrastructure redundancy and business continuity. Key features include:

        - Nodes are distributed across multiple availability zones to ensure high availability in the event of a zone failure.
        - Critical OLTP (Online Transactional Processing) components, such as PD and TiKV, are replicated across availability zones for redundancy.
        - Automatic failover minimizes service disruption during a primary zone failure.
  
    This feature is currently available only in the AWS Tokyo (ap-northeast-1) region and can be enabled only during cluster creation.
  
    For more information, see [High Availability in TiDB Cloud Serverless](/tidb-cloud/serverless-high-availability.md).

**Console changes**

- Strengthen the data export service:

    - Support exporting data from [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) to Google Cloud Storage and Azure Blob Storage through the [TiDB Cloud console](https://tidbcloud.com/).

    - Support exporting data in Parquet files through the [TiDB Cloud console](https://tidbcloud.com/).

  For more information, see [Export Data from TiDB Cloud Serverless](/tidb-cloud/serverless-export.md) and [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md).