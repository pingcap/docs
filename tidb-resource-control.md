---
title: Use Resource Control to Achieve Resource Isolation
summary: Learn how to use resource management to control and schedule application resource consumption.
---

# Use Resource Control to Achieve Resource Isolation

> **Warning:**
>
> This feature is experimental and its form and usage may change in subsequent versions.

Using the resource control feature, as a cluster administrator, you can define resource groups and limit the read and write quotas by resource groups. After you bind users to a resource group, the TiDB layer will perform flow control on the user's read and write requests according to the read and write quotas set by the bound resource group. Meanwile, the TiKV layer will schedule the requests according to the priority of the read and write quota mapping. Through flow control and scheduling, you can achieve resource isolation of your applications and meet the quality of service (QoS) requirements.

The introduction of the resource control feature is a milestone for TiDB. It can divide a distributed database cluster into multiple logical units. Even if an individual unit overuses resources, it does not crowd out the resources needed by other units. 

This feature applies to the following scenarios:

- You can combine multiple small and medium-sized applications from different systems into one TiDB cluster. If the load of an individual application grows larger, it does not affect the normal operation of other businesses. When the system load is low, busy applications can still be allocated the required system resources even if they exceed the set read and write quotas, so as to achieve the maximum utilization of resources.
- You can choose to combine all test environments into a single cluster, or group the batch tasks that consume more resources into a single resource group. It can improve hardware utilization and reduce operating costs while ensuring that critical applications receive the necessary resources.

In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

## Parameters for resource control

The resource control feature introduces two new global variables.

* TiDB: you can use the system variable [`tidb_enable_resource_control`](/system-variables.md#tidb-tidb_enable_resource_control) to control whether to enable flow control for a resource group. 
* TiKV: you can use the parameter [`resource_control.enabled`](/tikv-configuration-file.md#resource_control) to control whether to use request scheduling based on resource group quotas. Note that this parameter does not support dynamic modification. You need to restart the TiKV instance to for the modification to take effect.

The results of the combination of these two parameters are shown in the following table.

| `resource_control.enabled`  | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-------------------------------------|:-------------------------------------|
| `resource_control.enabled`= true  |  Flow control and scheduling (recommended) | Invalid combination      |  
| `resource_control.enabled`= false |  Only flow control                         | The feature is disabled. |

## How to use resource control

