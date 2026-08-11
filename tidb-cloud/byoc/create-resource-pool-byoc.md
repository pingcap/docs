---
title: Create a Resource Pool
summary: Learn how to create a resource pool for TiDB Cloud BYOC.
---

# Create a Resource Pool

A resource pool is a management unit for the underlying physical resources, network, and capacity in a TiDB Cloud BYOC deployment. A resource pool can host one or more BYOC instances, and each BYOC instance belongs to a single resource pool.

This document describes how to create a resource pool in the TiDB Cloud console.

## Before you begin

Before you create a resource pool, make sure that the following requirements are met:

- BYOC is enabled for your organization.
- BYOC deployment is complete in the target cloud provider and region.
- You have the `Organization Owner` role. Only Organization Owners can create and manage resource pools.
- You have planned a dedicated CIDR range for the resource pool.
- Your cloud account has sufficient service quota to provision the desired resource pool capacity.

## Create a resource pool

To create a resource pool, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **BYOC Management** > **Resource Pools** in the left navigation pane.

2. On the **Resource Pools** page, click **Create Resource Pool**.

3. In the **Basic Settings** area, configure the following fields:

    - **Resource Pool Name**: enter a name for the resource pool. The name must be valid and unique.
    - **Cloud Provider**: select the cloud provider where the resource pool is created.
    - **Region**: select the region where the resource pool is created.

    You can create a resource pool only in a cloud provider and region where BYOC deployment has been completed. If the target region is not available, complete the BYOC deployment for that region first, and then create the resource pool. After the resource pool is created, you cannot change the cloud provider or region.

4. (Optional) In the **Pool vCPU Limit** area, enable and set a Pool vCPU Limit.

    The Pool vCPU Limit is the maximum total provisioned TiDB vCPU capacity allowed for all database-related resources in the resource pool, including but not limited to TiDB, TiKV, TiFlash, and PD. It does not include vCPUs used by Observability (O11Y) Nodes or Admin Nodes. If you do not set a limit, resource usage is unrestricted and billed based on consumption.

5. In the **Pool Capacity** area, configure the initial TiKV resources and optionally configure TiFlash resources:

    - **TiKV**: TiKV is required. Select the initial vCPU and RAM configuration, storage size, and node count. The node count must meet the high availability requirement and must be a multiple of three. After the resource pool is created, TiKV can automatically scale out based on workload needs. You can also manually scale out TiKV in advance. Currently, TiDB Cloud does not support manual or automatic TiKV scale-in from the console, because scale-in can be risky. To scale in TiKV, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
    - **TiFlash**: TiFlash is optional. If you do not enable TiFlash when creating the resource pool, TiDB Cloud does not deploy TiFlash nodes. You can enable TiFlash later based on your workload needs. If you enable TiFlash, select the vCPU and RAM configuration, storage size, and node count.

    After the Resource Pool is created, you cannot manually change the TiKV machine type from the console. During automatic scale-out, TiDB Cloud might change the TiKV machine type based on workload needs. You can disable TiFlash from the TiDB Cloud console. Disabling TiFlash affects all BYOC instances in the resource pool. TiFlash resources are removed, and analytical workloads that depend on TiFlash might become unavailable or experience performance degradation.

    If you set a Pool vCPU Limit, make sure that the total vCPUs of the initial TiKV and TiFlash resources do not exceed 50% of the Pool vCPU Limit. This helps reserve capacity for future instance creation and automatic scale-out.

6. In the **Pool CIDR** area, review or enter the CIDR range for the resource pool.

    The resource pool CIDR is used as the network address range for resources in the resource pool and cannot be modified after the resource pool is created.

    The resource pool CIDR must meet the following requirements:

    - It must be within one of the supported private network address ranges: `10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`.
    - The prefix length must be between `/16` and `/22`.
    - It must not overlap with the O11Y CIDR or any existing resource pool CIDR in the same region.
    - It must not overlap with your application VPC CIDR or any other customer-managed network that needs to connect to this resource pool.

    TiDB Cloud validates CIDR overlap with known TiDB Cloud managed network ranges in the target region. TiDB Cloud cannot detect overlap with your application VPCs, on-premises networks, or VPN networks. You must verify these customer-managed network ranges before creating the resource pool.

7. In the **High Availability** area, review the high availability mode.

    The high availability mode is inherited from the BYOC deployment configuration of the selected region. You cannot change it when creating a Resource Pool.

8. (Optional) In the **AWS Resource Tags** area, add tags.

    Tags are applied to all taggable AWS resources within the resource pool.

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

After you submit the request, TiDB Cloud validates the configuration and starts an asynchronous provisioning operation. The new resource pool is displayed on the **Resource Pools** page with the **Creating** status. After provisioning succeeds, the status changes to **Active**.

## What's next

After the resource pool becomes **Active**, you can do the following:

- [Create a BYOC instance](/tidb-cloud/byoc/create-tidb-instance-byoc.md) in the resource pool.
- [Manage the resource pool](/tidb-cloud/byoc/manage-resource-pools-byoc.md), including updating capacity, updating the Pool vCPU Limit, and managing AWS resource tags.
