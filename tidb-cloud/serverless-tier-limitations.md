---
title: Serverless Tier Limitations
summary: Learn about the limitations of TiDB Cloud Serverless Tier.
---

# Serverless Tier Limitations

<!-- markdownlint-disable MD026 -->

This document describes the limitations of Serverless Tier. 

We are constantly filling in the feature gaps between Serverless Tier and Dedicated Tier. If you require these features or capabilities in the gap, use [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) or [contact us](https://www.pingcap.com/contact-us/?from=en) for a feature request.

## General limitations

- For each TiDB Cloud account, you can create one complimentary Serverless Tier cluster during the beta phase. To create a new Serverless Tier cluster, you need to delete the existing one first.
- Each Serverless Tier cluster has the following limitations:
    - The storage size is limited to 5 GiB (logical size) of OLTP storage and 5 GiB (logical size) of OLAP storage.
    - The compute resource is limited to 1 vCPU and 1 GiB RAM.
    - **Note**: In the coming months, we intend to offer a usage-based billing plan for additional resources and higher performance, while still keeping offering the free starter plan. In the coming releases, the limitations of the free Serverless Tier might be changed.

## Connection

- Only [Standard Connection](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) can be used. You cannot use [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) or [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) to connect to Serverless Tier clusters. 
- No "IP Access List" support.

## Backup and Restore

- [Backup and Restore](/tidb-cloud/backup-and-restore.md) are not supported for Serverless Tier currently.

## Monitoring

- [Built-in Monitoring](/tidb-cloud/built-in-monitoring.md) is currently not available for Serverless Tier.
- [Third-party Monitoring integrations](/tidb-cloud/third-party-monitoring-integrations.md) are currently not available for Serverless Tier.

## Others

- [TiDB Cloud API](/tidb-cloud/api-overview.md) and [Terraform Integration](/tidb-cloud/terraform-tidbcloud-provider-overview.md) are currently not available for Serverless Tier.