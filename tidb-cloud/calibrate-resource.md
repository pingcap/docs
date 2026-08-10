---
title: Calibrate Resource
summary: Learn how to estimate the RU capacity of your TiDB Cloud Dedicated cluster and allocate resources to resource groups.
---

# Calibrate Resource

[Request Unit (RU)](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) is a resource abstraction unit that represents system resource consumption. Before you allocate resources to [resource groups](/tidb-resource-control-ru-groups.md), it is recommended to estimate the total RU capacity of your cluster first.

For TiDB Cloud Dedicated clusters, you can estimate the RU capacity by using the **Calibrate Resource** feature on the **Monitoring** page of the TiDB Cloud console. This feature is available for all TiDB Cloud Dedicated clusters.

> **Note:**
>
> The estimated capacity is calculated based on hardware specifications or past statistics, and might deviate from the actual capacity of your cluster.

## Estimate the cluster capacity

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the left navigation pane, click **Monitoring**, and then click **Calibrate Resource**.

3. Choose one of the following calibration methods:

    - **Calibrate by Hardware**: estimates the capacity based on the current cluster configuration and the workload model you select. The following workload types are supported, and the default workload type is `TPCC`.

        - `TPCC`: applies to workloads with heavy data write. It is estimated based on a workload model similar to `TPC-C`.
        - `OLTP_WRITE_ONLY`: applies to workloads with heavy data write. It is estimated based on a workload model similar to `sysbench oltp_write_only`.
        - `OLTP_READ_WRITE`: applies to workloads with even data read and write. It is estimated based on a workload model similar to `sysbench oltp_read_write`.
        - `OLTP_READ_ONLY`: applies to workloads with heavy data read. It is estimated based on a workload model similar to `sysbench oltp_read_only`.

    - **Calibrate by Workload**: estimates the capacity based on the actual workload in a selected time window. The time window ranges from 10 minutes to 24 hours.

        If the workload in the selected time window is too low, TiDB cannot generate a capacity estimate. In this case, select another time window with a higher workload, or calibrate resources based on your hardware instead.

4. View the estimation results in the following cards:

    - **Estimated Capacity**: the estimated total RU capacity of the cluster.
    - **Total RU of user resource groups**: the total amount of RU allocated to all user resource groups, excluding the `default` resource group. If this value is more than the estimated capacity, the system triggers an alert.

The page also shows the following metric charts to help you understand the current resource consumption of the cluster:

- **Total RU Consumed**: the total consumption of Request Units counted in real time.
- **RU Consumed by Resource Groups**: the number of Request Units consumed by resource groups in real time.

## Change the resource allocation

To change the resource allocation for a resource group, use the following statement:

```sql
ALTER RESOURCE GROUP <resource group name> RU_PER_SEC=<#ru> [BURSTABLE];
```

For more information about resource groups, see [Use Resource Control to Achieve Resource Group Limitation and Flow Control](/tidb-resource-control-ru-groups.md).

## Limitations

- The `CALIBRATE RESOURCE` statement is not supported on TiDB Cloud Dedicated. To estimate the RU capacity of your cluster, use the **Calibrate Resource** feature in the TiDB Cloud console.
- The **Calibrate Resource** feature is available only for TiDB Cloud Dedicated clusters, not for {{{ .starter }}}, {{{ .essential }}}, or {{{ .premium }}} instances.
