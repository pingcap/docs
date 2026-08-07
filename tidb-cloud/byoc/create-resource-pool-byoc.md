---
title: Create a Resource Pool
summary: Learn how to create a Resource Pool for TiDB Cloud BYOC.
---

# Create a Resource Pool

A Resource Pool is the management unit for the underlying physical resources, network, and capacity in a TiDB Cloud BYOC deployment. A Resource Pool can host one or more BYOC instances, and each BYOC instance belongs to one Resource Pool.

This document describes how to create a Resource Pool in the TiDB Cloud console.

## Before you begin

Before you create a Resource Pool, make sure that the following requirements are met:

- BYOC is enabled for your organization.
- The target cloud provider and region have completed BYOC deployment.
- You have the `Organization Owner` role. Only Organization Owners can create and manage Resource Pools.
- You have planned a dedicated CIDR range for the Resource Pool.
- Your cloud account has sufficient service quota for the Resource Pool capacity that you want to provision.

## Create a Resource Pool

To create a Resource Pool, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **BYOC Management** > **Resource Pools** in the left navigation pane.

2. On the **Resource Pools** page, click **Create Resource Pool**.

3. In the **Basic Settings** area, configure the following fields:

    - **Resource Pool Name**: enter a name for the Resource Pool. The name must be valid and unique.
    - **Cloud Provider**: select the cloud provider where the Resource Pool is created.
    - **Region**: select the region where the Resource Pool is created.

    You can create a Resource Pool only in a cloud provider and region where BYOC deployment has been completed. If the target region is not available, complete the BYOC deployment for that region first, and then create the Resource Pool. After the Resource Pool is created, you cannot change the cloud provider or region.

4. In the **Pool vCPU Limit** area, optionally enable and set a Pool vCPU Limit.

    The Pool vCPU Limit is the maximum total provisioned TiDB vCPU capacity allowed for all database-related resources in the Resource Pool, including but not limited to TiDB, TiKV, TiFlash, and PD. It does not include vCPUs used by Observability (O11Y) Nodes or Admin Nodes. If you do not set a limit, resource usage is unrestricted and billed based on consumption.

5. In the **Pool Capacity** area, configure the initial TiKV resources and optionally configure TiFlash resources:

    - **TiKV**: TiKV is required. Select the initial vCPU and RAM configuration, storage size, and node count. The node count must meet the high availability requirement and must be a multiple of three. After the Resource Pool is created, TiKV can automatically scale out based on workload needs. You can also manually scale out TiKV in advance. Currently, TiDB Cloud does not support manual or automatic TiKV scale-in from the console, because scale-in can be risky. To scale in TiKV, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
    - **TiFlash**: TiFlash is optional. If you do not enable TiFlash when creating the Resource Pool, TiDB Cloud does not deploy TiFlash nodes. You can enable TiFlash later based on your workload needs. If you enable TiFlash, select the vCPU and RAM configuration, storage size, and node count.

    After the Resource Pool is created, you cannot manually change the TiKV machine type from the console. During automatic scale-out, TiDB Cloud might change the TiKV machine type based on workload needs. After TiFlash is provisioned, you cannot disable it from the console. To disable TiFlash, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

    If you set a Pool vCPU Limit, make sure that the total vCPUs of the initial TiKV and TiFlash resources do not exceed 50% of the Pool vCPU Limit. This helps reserve capacity for future instance creation and automatic scale-out.

6. In the **Pool CIDR** area, review or enter the CIDR range for the Resource Pool.

    The Resource Pool CIDR is used as the network address range for resources in the Resource Pool and cannot be modified after the Resource Pool is created.

    The Resource Pool CIDR must meet the following requirements:

    - It must be within one of the supported private network address ranges: `10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`.
    - The prefix length must be between `/16` and `/22`.
    - It must not overlap with the O11Y CIDR or any existing Resource Pool CIDR in the same region.
    - It must not overlap with your application VPC CIDR or any other customer-managed network that needs to connect to this Resource Pool.

    TiDB Cloud validates CIDR overlap with known TiDB Cloud managed network ranges in the target region. TiDB Cloud cannot detect overlap with your application VPCs, on-premises networks, or VPN networks. You must verify these customer-managed network ranges before creating the Resource Pool.

7. In the **High Availability** area, review the high availability mode.

    The high availability mode is inherited from the BYOC deployment configuration of the selected region. You cannot change it when creating a Resource Pool.

8. In the **AWS Resource Tags** area, optionally add tags.

    Tags are applied to all taggable AWS resources within the Resource Pool.

    The following rules apply:

    - Tag keys are required.
    - Tag values are optional.
    - Tag keys and values are case-sensitive.
    - Tag keys must be unique and are checked in a case-sensitive manner.
    - Tag key length must be from 1 to 128 UTF-8 characters.
    - Tag value length must not exceed 256 UTF-8 characters.
    - User-defined tag keys cannot start with `aws:`.
    - System-reserved AWS tags cannot be overwritten or edited.
    - Empty rows are ignored and not submitted.
    - Tags must comply with AWS tagging restrictions.

9. Review the summary on the right side, and then click **Create**.

After you submit the request, TiDB Cloud validates the configuration and starts an asynchronous provisioning operation. The new Resource Pool is displayed on the **Resource Pools** page with the **Creating** status. After provisioning succeeds, the status changes to **Active**.

## What's next

After the Resource Pool becomes **Active**, you can do the following:

- [Create a BYOC instance](/tidb-cloud/byoc/create-tidb-instance-byoc.md) in the Resource Pool.
- [Manage the Resource Pool](/tidb-cloud/byoc/manage-resource-pools-byoc.md), including updating capacity, updating the Pool vCPU Limit, and managing AWS resource tags.
