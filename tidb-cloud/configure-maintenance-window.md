---
title: Configure maintenance window
summary: Learn how to configure maintenance window for your cluster.
---

# Configure Maintenance Window

A maintenance window is a designated timeframe during which scheduled maintenance activities, such as operating system updates, security patches, and infrastructure upgrades, are executed to ensure the reliability, security, and performance of the TiDB Cloud service.

With maintenance window, you can easily schedule and manage maintenance tasks, minimizing the impact on cluster availability.

> **Note:**
>
> - Maintenance Window is only available for [Dedicated Tier clusters](/tidb-cloud/select-cluster-tier.md#dedicated-tier) under the specified project (as multiple clusters are hosted in one EKS).

 During the maintenance window:

- You might experience temporary connection disruptions or QPS fluctuations, but the clusters remain accessible.
- You can still perform SQL operations, cluster creation, preview, and deletion. All other operations, such as scaling, version upgrade, data import, data migration, and changefeed changes are not allowed and can only be performed after the maintenance items are completed. For a full list of allowed and disallowed operations, see xxx.
- Maintenance will be executed on each eligible TiDB cluster one by one to minimize the impact granularity.

## Be notified by maintenance windows

It is important to be aware of the maintenance window schedule and plan your operations accordingly to avoid potential disruptions.

For each maintenance window, all project members will receive a total of 3 emails as notifications at the following time points:

- 72 hours before the maintenance window starts (if any).
- The start time of the maintenance window (if any).
- The end time of the maintenance items are completed(if any).

## View and configure maintenance windows

Scheduling regular maintenance ensures that necessary updates are performed and safeguards the TiDB Cloud service from security threats, performance issues, and unreliability.

The maintenance window is enabled by default and cannot be disabled. you can modify the start time of the maintenance window or defer maintenance items until the deadline. If deferring maintenance items beyond the deadline is required, users need to submit a support ticket.

1. Once users access the Admin page and click on "Maintenance". On the Maintenance page, you can view a list of all maintenance items, such as their descriptions, status,scheduled start time, and deadline, which is the latest time for execution.
2. View the Maintenance window for the respective project, which includes a default Start time set for Every Wednesday at 3:00 AM ,based on the time zone of the TiDB Cluster's project.
3. (Optional) Customize the weekly start time to a desired timing. If there are maintenance items scheduled within that time window, the maintenance tasks will start at the designated time. --Users can also choose to defer a maintenance item to the next window, but not beyond the deadline.

## Allowed and disallowed operations during maintenance window

During the maintenance window, note the following:

- The existing data import, backup, restore, migration, and replication tasks can still run normally. If a manual or daily backup is currently in progress, the maintenance may be delayed until the backup is successfully completed. However, the daily backup or restore processes can still continue during the maintenance window.

- the following operations are allowed:

    - DDL operations
    - Create Cluster
    - Delete Cluster
    - Create Backup Task
    - Restore
    - Click cluster menus for overview, events, backup.

- The following operations are disallowed (the corresponding function will be in gray in the TiDB Cloud console).

    - Modify, pause, or resume a cluster
    - Change security settings
    - Create Private links or configure VPC peering
    - Create import tasks, migration jobs, or changefeed
    - Access **SQL Diagnosis**,**Monitoring**, and **Alerts**

## FAQs

- What is the frequency of triggering maintenance?

  It is infrequently, usually once every few months. And the maintenance items will be displayed 2 to 4 weeks before the deadline, allowing you to make necessary preparations.

- Will the clusters still be available during the maintenance window?

    TiDB clusters will remain available during the maintenance window, and you can continue to perform SQL operations. Users may experience brief connection disruptions or QPS fluctuations, which will be resolved after the maintenance is completed. Overall, the impact on the cluster is minimal.

- How to enable and disable the maintenance window?
The maintenance window is enabled by default and cannot be disabled. Users can modify the start time of the maintenance window or defer maintenance items until the deadline. If deferring maintenance items beyond the deadline is required, users need to submit a support ticket.

- How long will the maintenance window last?
The maintenance window will be executed on each eligible TiDB Cluster one by one. The duration of maintenance will vary depending on the number of clusters, cluster data size, and the maintenance items that need to be performed.

- Will maintenance be performed on clusters in any state?

Clusters in states such as importing, modifying, backup & restoring, or resuming will undergo maintenance operations after these operations are completed. Please note that for some clusters with large data volumes, the backup process may take a long time, such as 12 hours. Since the maintenance will be triggered after the backup is completed（if any), it is recommended to carefully set the start time for backups and the maintenance window in order to minimize the impact on the clusters.Clusters in the creating state do not require maintenance operations.







