---
title: Configure Maintenance Window
summary: Learn how to configure maintenance window for your cluster.
---

# Configure Maintenance Window

A maintenance window is a designated timeframe during which planned maintenance activities, such as operating system updates, security patches, and infrastructure upgrades, are performed automatically to ensure the reliability, security, and performance of the TiDB Cloud service.

During a maintenance window, the maintenance is executed on TiDB clusters one by one so the overall impact is minimal. Although there might be temporary connection disruptions or QPS fluctuations, the clusters remain available, and the existing data import, backup, restore, migration, and replication tasks can still run normally.

By configuring the maintenance window, you can easily schedule and manage maintenance activities to minimize the maintenance impact. For example, you can set the start time of the maintenance window to avoid peak hours of your application workloads.

> **Note:**
>
> The maintenance window feature is only available for [TiDB Dedicated clusters](/tidb-cloud/select-cluster-tier.md#dedicated-tier).

## Allowed and disallowed operations during a maintenance window

During a maintenance window, some operations are allowed, while some are not.

- Allowed operations:

    - SQL operations
    - Create clusters
    - Delete clusters
    - Create backup tasks
    - Restore clusters
    - Access cluster pages

- Disallowed operations:

    - Modify, pause, or resume clusters
    - Change security settings in the TiDB Cloud console
    - Create private links or configure VPC peering
    - Create import tasks, migration jobs, or changefeeds
    - Scale specifications of migration jobs or changefeeds

## Get notifications for maintenance activities

To avoid potential disruptions, it is important to be aware of the maintenance schedules and plan your operations accordingly.

For every maintenance window, TiDB Cloud sends three email notifications to all project members at the following time points:

- 72 hours before a maintenance window starts
- The time when a maintenance window is started
- The time when a maintenance window is completed

## View and configure maintenance windows

Regular maintenance ensures that essential updates are performed to safeguard TiDB Cloud from security threats, performance issues, and unreliability. Therefore, the maintenance window is enabled by default and cannot be disabled.

If a maintenance window is planned, the default start time of the window is 03:00 Wednesday (based on the time zone of your TiDB Cloud organization) of the target week.

You can modify the start time to your preferred time or defer maintenance activities until the deadline as follows:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [Clusters](https://tidbcloud.com/console/clusters) page of your project.

    > **Note:**
    >
    > If you have multiple projects, you can view the project list and switch to another project from the ☰ hover menu in the upper-left corner.

2. In the left navigation bar, click <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path d="M12 14.5H7.5C6.10444 14.5 5.40665 14.5 4.83886 14.6722C3.56045 15.06 2.56004 16.0605 2.17224 17.3389C2 17.9067 2 18.6044 2 20M14.5 6.5C14.5 8.98528 12.4853 11 10 11C7.51472 11 5.5 8.98528 5.5 6.5C5.5 4.01472 7.51472 2 10 2C12.4853 2 14.5 4.01472 14.5 6.5ZM22 16.516C22 18.7478 19.6576 20.3711 18.8054 20.8878C18.7085 20.9465 18.6601 20.9759 18.5917 20.9911C18.5387 21.003 18.4613 21.003 18.4083 20.9911C18.3399 20.9759 18.2915 20.9465 18.1946 20.8878C17.3424 20.3711 15 18.7478 15 16.516V14.3415C15 13.978 15 13.7962 15.0572 13.6399C15.1077 13.5019 15.1899 13.3788 15.2965 13.2811C15.4172 13.1706 15.5809 13.1068 15.9084 12.9791L18.2542 12C18.3452 11.9646 18.4374 11.8 18.4374 11.8H18.5626C18.5626 11.8 18.6548 11.9646 18.7458 12L21.0916 12.9791C21.4191 13.1068 21.5828 13.1706 21.7035 13.2811C21.8101 13.3788 21.8923 13.5019 21.9428 13.6399C22 13.7962 22 13.978 22 14.3415V16.516Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Admin**.

3. On the **Admin** page, click **Maintenance** in the left navigation pane.

     - If any maintenance activities are displayed, check the descriptions, scheduled start time, and deadline. The maintenance activities will start at the designated time.

     - If there is no maintenance data, it means no maintenance activity is scheduled recently.

4. (Optional) Click <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="mantine-1o1jehl"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> to modify the start time of the maintenance window. Note that the maintenance will be performed at the specified start time only if there is a maintenance window planned for that week.

5. To defer the start time of a scheduled maintenance activity, click **Defer** in the **Action** column and change it to the next feasible maintenance window before the deadline.

    If you need to defer the maintenance activity beyond the deadline, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md#tidb-cloud-support) for assistance.

## FAQs

- What are maintenance activities?

    Maintenance activities typically include operating system updates, security patches, and infrastructure upgrades.

- Can I disable a maintenance window?

    No. The maintenance window is enabled by default and cannot be disabled. You can modify the start time of the maintenance window or defer a maintenance activity to 2 to 4 weeks until the deadline. For more information, see [View and configure maintenance windows](#view-and-configure-maintenance-windows).

- How long does a maintenance window last?

    It depends. For each project, maintenance is executed on eligible TiDB clusters one by one. The duration of maintenance varies depending on the number of clusters, cluster data size, and the maintenance activities to be performed.

- Will maintenance activities be performed on clusters in any status?

    No. TiDB Cloud checks the cluster status before performing a maintenance activity on a cluster.

    - If the cluster is in the **Creating** or **Paused** status, maintenance activities are not required.
    - If the cluster is running a daily or manual backup, the maintenance will be delayed and triggered until the current backup is successfully completed. Note that for clusters with large data volumes, the backup process might take a long time, such as 12 hours. To minimize the impact on the clusters, it is recommended to carefully set the start time for backups and the maintenance window.
    - If the cluster is in any other status, the maintenance activities will start as scheduled.
