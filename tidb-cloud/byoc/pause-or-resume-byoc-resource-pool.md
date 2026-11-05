---
title: Pause or Resume a BYOC Resource Pool
summary: Learn how to pause and resume a TiDB Cloud BYOC resource pool, understand the seven-day automatic resume limit, and review billing and restrictions.
---

# Pause or Resume a BYOC Resource Pool

You can pause a TiDB Cloud BYOC resource pool during idle periods to reduce database compute costs while retaining your data, backups, and network configuration. Pausing a resource pool pauses all instances in the pool together. You cannot pause or resume an individual instance independently.

A resource pool can remain paused for up to 7 days. If you do not resume it earlier, TiDB Cloud automatically starts resuming the entire resource pool when the 7-day limit is reached.

## Before you begin

- Make sure that you have the `Organization Owner` role. For more information, see [Manage Resource Pools](/tidb-cloud/byoc/manage-resource-pools-byoc.md#required-role).
- Make sure that the resource pool is **Active** and that all instances in the pool can be taken offline.
- Complete or stop conflicting operations, such as data import or export, DM, pipeline or changefeed tasks, upgrades, and capacity changes, before pausing the pool.
- Reduce workload activity before requesting a pause. TiDB Cloud checks workload activity and other dependencies before proceeding. If a required check fails or cannot be completed, the pause does not proceed.

## Pause a BYOC resource pool

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **BYOC Management** > **Resource Pools** in the left navigation pane.
2. Locate an **Active** resource pool, click **...** in its row, and select **Pause**.

    Alternatively, click the resource pool name to open the **Resource Pool Details** page, and then click **Pause** in the upper-right corner.

3. In the **Pause Resource Pool?** dialog, review the number of hosted instances affected by the operation.
4. (Optional) Select **Create a Manual Backup before pausing**.

    If selected, TiDB Cloud creates a manual backup for every instance in the resource pool before continuing with the pause. This process might take a long time. Mandatory data protection runs regardless of whether you select this option.

5. Click **Pause Resource Pool**.

    TiDB Cloud completes the required protection checks before removing runtime compute. Wait for the resource pool to reach **Paused**. All instances in the resource pool are paused together.

During preparation, TiDB Cloud performs the required checks and any selected manual backups. If preparation fails, the resource pool returns to **Active**, and runtime compute is not removed.

Once the resource pool enters **Pausing**, SQL connections and operations that require active compute are unavailable. All instances in the pool participate in the pause. The resource pool reaches **Paused** after the required runtime database compute has been removed.

## Behavior while paused

When a resource pool is **Paused**:

- All instances in the pool are paused. You cannot read or write data or run operations that require active database compute.
- Your data and the persistent storage required to resume the pool are retained. The resource pool is not deleted.
- Existing network configuration and connection information are retained for use after the pool resumes.
- Existing backups, logs, and historical metrics remain available according to their retention policies. No new runtime compute metrics are generated.
- Scheduled backups are suspended, and you cannot create new manual backups.
- You cannot create an instance in the paused pool or restore a backup to it. Resume the resource pool first.
- Resource pool configuration and capacity changes are unavailable.

## Resume a BYOC resource pool

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **BYOC Management** > **Resource Pools** in the left navigation pane.
2. Locate a **Paused** resource pool, click **...** in its row, and select **Resume**.

    Alternatively, click the resource pool name to open the **Resource Pool Details** page, and then click **Resume** in the upper-right corner.

3. In the **Resume Resource Pool?** dialog, review the impact on all hosted instances, and click **Resume Resource Pool**.
4. Wait for the resource pool and its hosted instances to return to **Active**.

    The resume operation might take up to 30 minutes. SQL connections remain unavailable while the resource pool is **Resuming**.

The resource pool and its instances enter **Resuming** while TiDB Cloud restores runtime compute and checks readiness. SQL connections remain unavailable until the resume completes. Configuration and scaling operations remain blocked during this process.

After the pool returns to **Active**, all hosted instances return to **Active**. SQL connectivity, scheduled backups, and normal monitoring resume. You can continue using the retained connection information.

## Automatic resume after 7 days

The maximum continuous pause duration is 7 days, starting when the resource pool reaches **Paused**. Time spent in **Pausing** does not count toward this limit.

If you have not resumed the pool before the deadline, TiDB Cloud automatically starts the resume operation. The resource pool enters **Resuming** and becomes available only after the required readiness checks complete.

## Billing

BYOC database vCPU charges follow the actual provisioned database compute capacity:

- During **Pausing**, database compute charges decrease as compute nodes are removed.
- While **Paused**, database vCPU charges are zero because no database compute nodes remain provisioned.
- During **Resuming**, database compute charges increase as compute nodes are provisioned again.

Charges for retained storage, networking, backups, and other infrastructure in your cloud account might continue while the pool is paused. For more information, see [Pricing for TiDB Cloud BYOC](/tidb-cloud/tidb-cloud-billing.md#pricing-for-byoc).

## Troubleshooting

If a resource pool remains in **Pausing** or **Resuming** for an unusually long time, or if SQL connectivity does not recover after the pool returns to **Active**, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
