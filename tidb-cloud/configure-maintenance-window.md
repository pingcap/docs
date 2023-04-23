---
title: Configure maintenance window
summary: Learn how to configure maintenance window for your cluster.
---

# Configure Maintenance Window

A maintenance window is a designated timeframe during which scheduled maintenance activities, such as operating system updates, security patches, and infrastructure upgrades, are executed to ensure the reliability, security, and performance of the TiDB Cloud service.

With the maintenance window feature, you can easily schedule and manage maintenance tasks, minimizing the impact on cluster availability.

> **Note:**
>
> - The maintenance window feature is only available for [Dedicated Tier clusters](/tidb-cloud/select-cluster-tier.md#dedicated-tier) under the specified project (as multiple clusters are hosted in one EKS).
> - When the schedule maintenance time comes, if a manual or daily backup is currently in progress, the maintenance might be delayed until the backup is successfully completed.

During the maintenance window, you might experience temporary connection disruptions or QPS fluctuations, but the clusters remain accessible.

- The existing data import, backup, restore, migration, and replication tasks can still run normally.
- Maintenance tasks are executed on each eligible TiDB cluster one by one so the overall impact on the cluster performance is minimal.

## Allowed and disallowed operations during a maintenance window

- The following operations are allowed during a maintenance window:

    - DDL operations
    - Create clusters
    - Delete clusters
    - Create backup tasks
    - Restore clusters
    - Access the cluster **Overview**, **Events**, **Backup** pages

- The following operations are disallowed during a maintenance window (the corresponding features will be displayed in gray in the TiDB Cloud console):

    - Modify, pause, or resume clusters
    - Change security settings
    - Create private links or configure VPC peering
    - Create import tasks, migration jobs, or changefeeds
    - Access the cluster **SQL Diagnosis**,**Monitoring**, and **Alerts** pages

## Be notified by maintenance windows

It is important to be aware of the maintenance window schedule and plan your operations accordingly to avoid potential disruptions.

For each maintenance window, all project members will receive three emails as notifications from TiDB Cloud at the following time points:

- 72 hours before the maintenance window starts.
- The time when the maintenance tasks are started.
- The time when the maintenance tasks are completed.

## View and configure maintenance windows

Scheduling regular maintenance ensures that essential updates are performed and safeguards the TiDB Cloud service from security threats, performance issues, and unreliability. Therefore, the maintenance window is enabled by default and cannot be disabled.

The default maintenance window starts at 03:00 AM every Wednesday (based on the project time zone of your cluster). You can modify the start time of the maintenance window, or defer maintenance items until the deadline as follows:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [Clusters](https://tidbcloud.com/console/clusters) page of your project.

    > **Note:**
    >
    > If you have multiple projects, you can view the project list and switch to another project from the ☰ hover menu in the upper-left corner.

2. In the left navigation bar, click <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Admin**.

3. On the **Admin** page, click **Maintenance** in the left navigation pane.

     If a maintenance window is planned, the corresponding maintenance items are displayed on the **Maintenance** page 2 to 4 weeks before the deadline. For each maintenance item, you can view its descriptions, status, scheduled start time, and deadline, which is the latest time for execution.

4. (Optional) Click <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="mantine-1o1jehl"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> to customize the start time.

5. If any scheduled maintenance items are displayed, the maintenance tasks will start at the designated time.

6. To defer the start time of a maintenance item, click **Defer** and set a new time.

    If deferring maintenance items beyond the deadline is required, you need to contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md#tidb-cloud-support) to get help.

## FAQs

- What is the frequency of triggering maintenance?

    It is infrequently, usually once every few months. And the maintenance items will be displayed 2 to 4 weeks before the deadline, allowing you to make necessary preparations.

- Are the clusters still be available during the maintenance window?

    TiDB clusters remain available during the maintenance window, and you can continue to perform SQL operations. You might experience brief connection disruptions or QPS fluctuations, which will be resolved after the maintenance is completed. Overall, the impact on the cluster is minimal.

- How can I enable and disable the maintenance window?

    The maintenance window is enabled by default and cannot be disabled. You can modify the start time of the maintenance window or defer maintenance items as described in [View and configure maintenance windows](#view-and-configure-maintenance-windows).

- How long does a maintenance window last?

    For each project, the maintenance is executed on each eligible TiDB cluster one by one. The duration of maintenance varies depending on the number of clusters, cluster data size, and the maintenance items to be performed.

- Will maintenance be performed on clusters in any state?

    No. If clusters are in states such as **IMPORTING**, **MODIFYING**, **BACKUP**, **RESTORING**, or **RESUMING**, maintenance tasks will be triggered after these operations are completed. For clusters in the **CREATING** state, maintenance operations are not required.

    Note that for clusters with large data volumes, the backup process might take a long time, such as 12 hours. If the scheduled maintenance time comes and a backup task is in progress, the maintenance will be triggered after the backup is completed. Therefore, it is recommended to carefully set the start time for backups and the maintenance window to minimize the impact on the clusters