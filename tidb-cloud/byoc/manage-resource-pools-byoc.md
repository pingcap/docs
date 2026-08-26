---
title: Manage Resource Pools
summary: Learn how to view and manage resource pools for TiDB Cloud BYOC.
---

# Manage Resource Pools

A resource pool represents the underlying physical resources, network, and capacity used by TiDB Cloud BYOC instances. You can use resource pool management to view resource usage, manage capacity, update AWS resource tags, and delete unused resource pools.

Resource pools are organization-level BYOC resources and are not associated with projects.

## Required role

Only users with the `Organization Owner` role can manage resource pools.

Other roles might have read-only access to resource pools, but they cannot create, edit, delete, or modify resource pools.

## View resource pools

To view resource pools, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **BYOC Management** > **Resource Pools** in the left navigation pane.

2. On the **Resource Pools** page, view the resource pool list.

    The list displays information such as the resource pool name, status, cloud provider, region, instance count, and creation time.

3. To filter resource pools, use the search box and filters at the top of the page.

4. To refresh the list, click the refresh icon.

## Resource pool statuses

The following statuses are displayed for resource pools:

- **Creating**: the resource pool is being provisioned. You can view basic information, but you cannot create instances or make configuration changes.
- **Active**: the resource pool is available. Normal management operations are available.
- **Modifying**: the resource pool is being modified. You can view the overview, metrics, instances, tags, and other details, but you cannot create instances or change the capacity or Pool vCPU Limit.

## View resource pool details

To view resource pool details, click the name of a resource pool on the **Resource Pools** page.

The resource pool details page includes the following information:

- **High Availability**: shows whether the resource pool uses zonal or regional high availability. This value is read-only. You cannot change the high availability mode or availability zone placement after the resource pool is created.
- **Pool vCPU Usage**: shows the current provisioned TiDB vCPU and additional vCPU provision.
- **Instances in This Pool**: lists the BYOC instances that run in this resource pool.
- **Metrics**: shows vCPU usage and physical storage usage trends.
- **Pool Capacity**: shows TiKV and TiFlash capacity information.
- **AWS Resource Tags**: shows AWS tags applied to supported resources in this resource pool.

## View metrics

The **Metrics** area on the resource pool details page provides the following charts:

- **vCPU Usage Trend**: shows the provisioned TiDB vCPU usage trend for the resource pool. The chart also displays the current vCPU value.
- **Physical Storage Usage Trend**: shows the actual physical storage usage trend for the resource pool. The chart also displays the current storage value.

You can select a time range to view historical metrics. By default, metrics for the past 30 days are displayed.

To refresh the metric data, click **Refresh**.

If metric data is not available yet, the chart displays **No Data Available Yet**.

## Update the Pool vCPU Limit

The Pool vCPU Limit is an optional customer-defined limit for the maximum provisioned TiDB vCPU capacity allowed for a resource pool. Additional vCPU provision, such as admin nodes and observability nodes, is not counted toward this limit.

To update the Pool vCPU Limit, take the following steps:

1. Go to the Resource Pool details page.
2. In the **Pool vCPU Usage** area, click **Update vCPU Limit**.
3. In the displayed dialog, turn on or turn off **Setup Limit**.

    - If you turn on **Setup Limit**, enter a new Pool vCPU Limit.
    - If you turn off **Setup Limit**, no customer-defined vCPU limit applies to the resource pool, and billing remains based on actual usage.

4. Confirm the update.

When you set a new Pool vCPU Limit, the value must be greater than or equal to `100` vCPU and the current provisioned TiDB vCPU. Otherwise, the update is rejected.

> **Note:**
>
> Even when the current provisioned vCPU is below the Pool vCPU Limit, creating or restoring an instance might cause the total provisioned vCPU to exceed the limit. This might restrict resource scaling and degrade the performance of all instances in the resource pool. Before creating or restoring an instance, make sure that the resource pool has sufficient vCPU capacity.

If the current provisioned vCPU of a resource pool is greater than or equal to its Pool vCPU Limit, you cannot create or restore an instance in that resource pool. To create or restore an instance, increase or turn off the Pool vCPU Limit, or select another resource pool.

If the resource pool is in the **Modifying** status, **Update vCPU Limit** is disabled.

## Update capacity

You can update the TiKV and TiFlash capacity of a resource pool.

To update capacity, take the following steps:

1. Go to the Resource Pool details page.
2. In the **Pool Capacity** area, click **Update Capacity**.
3. In the **Update _resource-pool-name_ Capacity** dialog, update TiKV or TiFlash capacity.
4. If a Pool vCPU Limit is configured, review the capacity evaluation.
5. Click **Save**.

If a Pool vCPU Limit is configured, the dialog displays the following capacity evaluation information:

- **Current vCPU Usage**: the current provisioned TiDB vCPU usage of the resource pool.
- **Scaling vCPU Preview**: the estimated provisioned TiDB vCPU usage after the capacity update.
- **Max vCPU Limit**: the current Pool vCPU Limit.
- **Scale Evaluation**: whether the capacity update is allowed under the current Pool vCPU Limit.

If no Pool vCPU Limit is configured, the capacity evaluation information is not displayed.

The following rules apply:

- Only scale-out operations are supported in the TiDB Cloud console. If you have additional node or size requirements, or if you need to scale in, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
- TiKV node count must be adjusted in increments of three.
- TiKV storage can only be increased.
- TiKV machine type cannot be changed after the resource pool is created.
- TiFlash is optional. If TiFlash is not enabled, no TiFlash nodes are provisioned.
- You can enable TiFlash later based on workload requirements.
- You can disable TiFlash from the TiDB Cloud console. Disabling TiFlash affects all BYOC instances in the resource pool. TiFlash resources are removed, and analytical workloads that depend on TiFlash might become unavailable or experience performance degradation.
- TiFlash machine type can be changed online.
- TiFlash storage can only be increased.
- TiFlash node count can only be increased.
- If a Pool vCPU Limit is configured, the **Scaling vCPU Preview** must not exceed the **Max vCPU Limit**.

If the resource pool is in the **Modifying** status, **Update Capacity** is disabled.

## Manage AWS resource tags

AWS resource tags are applied to supported AWS resources in the resource pool.

To manage AWS resource tags, take the following steps:

1. Go to the Resource Pool details page.
2. In the **AWS Resource Tags** area, click **Edit Tags**.
3. Add, edit, or delete tags.
4. Save the changes.

The following rules apply:

- Tags are applied to all taggable AWS resources within the resource pool.
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

## Rename a resource pool

To rename a resource pool, take the following steps:

1. Go to the Resource Pool details page or the **Resource Pools** page.
2. Click **...**.
3. Click **Rename**.
4. Enter a new name and confirm the change.

Renaming a resource pool changes only its display name. It does not modify underlying cloud resource IDs.

## Delete a resource pool

You can delete a resource pool only when it contains no BYOC instances.

To delete a resource pool, take the following steps:

1. Go to the **Resource Pools** page.
2. Locate the resource pool that you want to delete.
3. Click **...** > **Delete**.
4. Enter the resource pool name to confirm the deletion.

Deleting a resource pool does not delete historical instance backups. Backup retention and Recycle Bin behavior follow the existing BYOC backup and restore rules.

## Operation restrictions

When a resource pool has an ongoing modification operation, TiDB Cloud refreshes resource pool data in real time or near real time. During this period:

- You can view the resource pool overview, metrics, instances, tags, and other details.
- You cannot create an instance. You can create instances only when the resource pool is in the **Active** status.
- You can delete an instance if the instance is in a deletable state.
- You cannot update the Pool vCPU Limit.
- You cannot update capacity.

The backend performs final validation when you submit an operation. If the resource pool state changes during the operation, the request might be rejected.
