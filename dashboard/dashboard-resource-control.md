---
title: TiDB Dashboard Resource Control Page
summary: Introduces how to use TiDB Dashboard's Resource Control page to view information about resource control, so you can estimate cluster capacity and better allocate resources.
---

# TiDB Dashboard Resource Control Page

To implement resource isolation using the [Resource Control](/tidb-resource-control.md) feature, cluster administrators can define Resource Groups and limit read and write quotas through Resource Groups. Before resource planning, you need to know the overall capacity of the cluster. This page can help you view information about resource control so that you can estimate the cluster capacity and better allocate resources.

## Access Page

You can use one of the following two methods to access the cluster resource control page:

* After logging into TiDB Dashboard, click **Resource Manager** in the left navigation bar.

* Visit <http://127.0.0.1:2379/dashboard/#/resource_manager> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## Resource Control Details

The Resource Control Details page is shown in the following image:

![TiDB Dashboard: Resource Manager](/media/dashboard/dashboard-resource-manager-info.png)

The resource manager details page contains the following three sections:

- Configuration: Data from TiDB's `RESOURCE_GROUPS` table with information about all resource groups. For more information, see [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md).

- Estimated Capacity: Before resource planning, you need to know the overall capacity of the cluster. You can use one of the following methods:

    - [Estimate capacity based on actual workload](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
    - [Estimate capacity based on hardware deployment](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

- Metrics: By observing the metrics on the panel, you can understand the current resource consumption status of the cluster as a whole.

## Capacity estimation

Before doing resource planning, you need to know the overall capacity of the cluster. Two estimation methods are currently provided to estimate the capacity of the current cluster's [`Request Unit (RU)`](/tidb-resource-control.md#what-is-request-unit-ru#what-is-request-unit-ru):

- [Estimate capacity based on hardware deployment](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)
    
    Here accepts the following different workload types:
    
    - `tpcc`: applies to workloads with heavy data write. It is estimated based on a workload model similar to `TPC-C`.
    - `oltp_write_only`: applies to workloads with heavy data write. It is estimated based on a workload model similar to `sysbench oltp_write_only`.
    - `oltp_read_write`: applies to workloads with even data read and write. It is estimated based on a workload model similar to `sysbench oltp_read_write`.
    - `oltp_read_only`: applies to workloads with heavy data read. It is estimated based on a workload model similar to `sysbench oltp_read_only`.

    ![Estimated capacity based on hardware deployment](/media/dashboard/dashboard-resource-manager-calibrate-by-hardware.png)

    Total RU of user resource groups indicates the total number of RUs currently available except for `default` users. The system will alert when this value is less than the capacity estimate. TiDB automatically creates a `default` resource group during cluster initialization. For this resource group, the default value of `RU_PER_SEC` is `UNLIMITED`. When all users belong to the `default` resource group, resources are allocated in the same way as when resource control is turned off.

- [Estimate capacity based on actual workload](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)

    ![Calibrate by Workload](/media/dashboard/dashboard-resource-manager-calibrate-by-workload.png)

    You can select a time range of 10 minutes to 24 hours for the estimation. The time zone is the same as the time zone of the front-end user.

    - When the time window range does not fall between 10 minutes and 24 hours, an error occurs, an error will be reported `ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s`.

    - When the workload within the time window is too low, an error will be reported `ERROR 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead`.

  You can select the appropriate time range by using **CPU Usage** in [Monitoring Metrics](#monitoring-metrics).

## Monitoring Metrics

By observing the metrics on the panel, you can understand the current resource consumption status of the cluster as a whole. The monitoring metrics and their meanings are as follows:

- Total RU Consumed: The total consumption of Request Units counted in real time
- RU Consumed by Resource Groups: The number of Request Units consumed by resource groups in real time.
- TiDB
    - CPU Quota: The maximum CPU usage of TiDB
    - CPU Usage: CPU usage of all TiDB instances
- TiKV
    - CPU Quota: The maximum CPU usage of TiKV
    - CPU Usage: CPU usage of all TiKV instances
    - IO MBps: I/O throughput of all TiKV instances