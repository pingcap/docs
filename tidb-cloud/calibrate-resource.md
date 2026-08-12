---
title: 资源校准
summary: 了解如何估算 TiDB Cloud Dedicated 集群的 RU 容量，并将资源分配给资源组。
---

# 资源校准

[Request Unit (RU)](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) 是一种资源抽象单位，用于表示系统资源消耗。在将资源分配给[资源组](/tidb-resource-control-ru-groups.md)之前，建议先估算集群的总 RU 容量。

对于 TiDB Cloud Dedicated 集群，你可以使用 TiDB Cloud 控制台 **Monitoring** 页面上的 **Calibrate Resource** 功能来估算 RU 容量。该功能适用于所有 TiDB Cloud Dedicated 集群。

> **注意：**
>
> 估算容量基于硬件规格或历史统计数据计算得出，因此可能与集群的实际容量存在偏差。

## 估算集群容量 {#estimate-the-cluster-capacity}

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击目标集群名称，进入其概览页面。

    > **提示：**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 在左侧导航栏中，点击 **Monitoring**，然后点击 **Calibrate Resource**。

3. 选择以下任一种校准方法：

    - **Calibrate by Hardware**：根据当前集群配置以及你选择的工作负载模型来估算容量。支持以下工作负载类型，默认工作负载类型为 `TPCC`。

        - `TPCC`：适用于数据写入较重的工作负载。基于类似 `TPC-C` 的工作负载模型进行估算。
        - `OLTP_WRITE_ONLY`：适用于数据写入较重的工作负载。基于类似 `sysbench oltp_write_only` 的工作负载模型进行估算。
        - `OLTP_READ_WRITE`：适用于数据读写均衡的工作负载。基于类似 `sysbench oltp_read_write` 的工作负载模型进行估算。
        - `OLTP_READ_ONLY`：适用于数据读取较重的工作负载。基于类似 `sysbench oltp_read_only` 的工作负载模型进行估算。

    - **Calibrate by Workload**：根据所选时间窗口内的实际工作负载来估算容量。时间窗口范围为 10 分钟到 24 小时。

        如果所选时间窗口内的工作负载过低，TiDB 将无法生成容量估算结果。在这种情况下，请选择另一个工作负载更高的时间窗口，或者改为基于硬件进行资源校准。

4. 在以下卡片中查看估算结果：

    - **Estimated Capacity**：集群估算的总 RU 容量。
    - **Total RU of user resource groups**：分配给所有用户资源组的 RU 总量，不包括 `default` 资源组。如果该值超过估算容量，系统会触发告警。

该页面还会显示以下指标图表，帮助你了解集群当前的资源消耗情况：

- **Total RU Consumed**：实时统计的 Request Unit 总消耗量。
- **RU Consumed by Resource Groups**：各资源组实时消耗的 Request Unit 数量。

## 更改资源分配 {#change-the-resource-allocation}

如需更改某个资源组的资源分配，请使用以下语句：

```sql
ALTER RESOURCE GROUP <resource group name> RU_PER_SEC=<#ru> [BURSTABLE];
```

有关资源组的更多信息，请参见[使用资源控制实现资源组限制与流控](/tidb-resource-control-ru-groups.md)。

## 限制 {#limitations}

- TiDB Cloud Dedicated 不支持 `CALIBRATE RESOURCE` 语句。要估算集群的 RU 容量，请使用 TiDB Cloud 控制台中的 **Calibrate Resource** 功能。
- **Calibrate Resource** 功能仅适用于 TiDB Cloud Dedicated 集群，不适用于 {{{ .starter }}}、{{{ .essential }}} 或 {{{ .premium }}} 实例。