---
title: Manage Resource Pools
summary: Learn how to view and manage Resource Pools for TiDB Cloud BYOC.
---

# Manage Resource Pools

A Resource Pool represents the underlying physical resources, network, and capacity used by TiDB Cloud BYOC instances. You can use Resource Pool management to view resource usage, manage capacity, update AWS resource tags, and delete unused Resource Pools.

Resource Pools are organization-level BYOC resources. They are not associated with projects.

## Required role

Only users with the `Organization Owner` role can manage Resource Pools.

Other roles might have read-only access to Resource Pools, but they cannot create, edit, delete, or modify Resource Pools.

## View Resource Pools

To view Resource Pools, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **BYOC Management** > **Resource Pools** in the left navigation pane.

2. On the **Resource Pools** page, view the Resource Pool list.

    The list displays information such as the Resource Pool name, status, cloud provider, region, instance count, and creation time.

3. To filter Resource Pools, use the search box and filters at the top of the page.

4. To refresh the list, click the refresh icon.

## Resource Pool statuses

The following statuses are displayed for Resource Pools:

- **Creating**: the Resource Pool is being provisioned. You can view basic information, but you cannot create instances or make configuration changes.
- **Active**: the Resource Pool is available. Normal management operations are available.
- **Modifying**: the Resource Pool is being modified. You can view the overview, metrics, instances, tags, and other details, but you cannot update capacity or update the Pool vCPU Limit.

## View Resource Pool details

To view Resource Pool details, click the name of a Resource Pool on the **Resource Pools** page.

The Resource Pool details page includes the following information:

- **Pool vCPU Usage**: shows the current provisioned TiDB vCPU and additional vCPU provision.
- **Instances in This Pool**: lists the BYOC instances that run in this Resource Pool.
- **Metrics**: shows vCPU usage and physical storage usage trends.
- **Pool Capacity**: shows TiKV and TiFlash capacity information.
- **AWS Resource Tags**: shows AWS tags applied to supported resources in this Resource Pool.

## View metrics

The **Metrics** area on the Resource Pool details page provides the following charts:

- **vCPU Usage Trend**: shows the provisioned TiDB vCPU usage trend for the Resource Pool. The chart also displays the current vCPU value.
- **Physical Storage Usage Trend**: shows the actual physical storage usage trend for the Resource Pool. The chart also displays the current storage value.

You can select a time range to view historical metrics. By default, metrics for the past 30 days are displayed.

To refresh the metric data, click **Refresh**.

If metric data is not available yet, the chart displays **No Data Available Yet**.

## Update the Pool vCPU Limit

The Pool vCPU Limit is an optional customer-defined limit for the maximum provisioned TiDB vCPU capacity allowed for a Resource Pool. Additional vCPU provision, such as Admin Nodes and Observability Nodes, is not counted toward this limit.

To update the Pool vCPU Limit, take the following steps:

1. Go to the Resource Pool details page.
2. In the **Pool vCPU Usage** area, click **Update vCPU Limit**.
3. In the displayed dialog, turn on or turn off **Setup Limit**.
4. If you turn on **Setup Limit**, enter a new Pool vCPU Limit.
5. If you turn off **Setup Limit**, no customer-defined vCPU limit applies to the Resource Pool, and billing remains based on actual usage.
6. Confirm the update.

When you set a new Pool vCPU Limit, the value must be greater than or equal to `100` vCPU and the current provisioned TiDB vCPU. Otherwise, the update is rejected.

If the Resource Pool is in the **Modifying** status, **Update vCPU Limit** is disabled.

## Update capacity

You can update the TiKV and TiFlash capacity of a Resource Pool.

To update capacity, take the following steps:

1. Go to the Resource Pool details page.
2. In the **Pool Capacity** area, click **Update Capacity**.
3. In the **Update _resource-pool-name_ Capacity** dialog, update TiKV or TiFlash capacity.
4. If a Pool vCPU Limit is configured, review the capacity evaluation.
5. Click **Save**.

If a Pool vCPU Limit is configured, the dialog displays the following capacity evaluation information:

- **Current vCPU Usage**: the current provisioned TiDB vCPU usage of the Resource Pool.
- **Scaling vCPU Preview**: the estimated provisioned TiDB vCPU usage after the capacity update.
- **Max vCPU Limit**: the current Pool vCPU Limit.
- **Scale Evaluation**: whether the capacity update is allowed under the current Pool vCPU Limit.

If no Pool vCPU Limit is configured, the capacity evaluation information is not displayed.

The following rules apply:

- Only scale-out operations are supported in the TiDB Cloud console. If you have additional node or size requirements, or if you need to scale in, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
- TiKV node count must be adjusted in increments of three.
- TiKV storage can only be increased.
- TiKV machine type cannot be changed after the Resource Pool is created.
- TiFlash is optional. If TiFlash is not enabled, no TiFlash nodes are provisioned.
- You can enable TiFlash later based on workload requirements.
- After TiFlash is provisioned, you cannot disable it from the TiDB Cloud console. To disable TiFlash, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
- TiFlash machine type can be changed online.
- TiFlash storage can only be increased.
- TiFlash node count can only be increased.
- If a Pool vCPU Limit is configured, the **Scaling vCPU Preview** must not exceed the **Max vCPU Limit**.

If the Resource Pool is in the **Modifying** status, **Update Capacity** is disabled.

## Manage AWS resource tags

AWS resource tags are applied to supported AWS resources in the Resource Pool.

To manage AWS resource tags, take the following steps:

1. Go to the Resource Pool details page.
2. In the **AWS Resource Tags** area, click **Edit Tags**.
3. Add, edit, or delete tags.
4. Save the changes.

The following rules apply:

- Tags are applied to all taggable AWS resources within the Resource Pool.
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

## Rename a Resource Pool

To rename a Resource Pool, take the following steps:

1. Go to the Resource Pool details page or the **Resource Pools** page.
2. Click **...**.
3. Click **Rename**.
4. Enter a new name and confirm the change.

Renaming a Resource Pool changes only its display name. It does not modify underlying cloud resource IDs.

## Delete a Resource Pool

You can delete a Resource Pool only when it contains no BYOC instances.

To delete a Resource Pool, take the following steps:

1. Go to the **Resource Pools** page.
2. Locate the Resource Pool that you want to delete.
3. Click **...** > **Delete**.
4. Enter the Resource Pool name to confirm the deletion.

Deleting a Resource Pool does not delete historical instance backups. Backup retention and Recycle Bin behavior follow the existing BYOC backup and restore rules.

## Operation restrictions

When a Resource Pool has an ongoing modification operation, TiDB Cloud refreshes Resource Pool data in real time or near real time. During this period:

- You can view the Resource Pool overview, metrics, instances, tags, and other details.
- You can create an instance if the backend validation succeeds.
- You can delete an instance if the instance is in a deletable state.
- You cannot update the Pool vCPU Limit.
- You cannot update capacity.

The backend performs final validation when you submit an operation. If the Resource Pool state changes during the operation, the request might be rejected.
