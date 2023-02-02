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

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature does not support [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

## Parameters for resource control

The resource control feature introduces two new global variables.

* TiDB: you can use the system variable [`tidb_enable_resource_control`](/system-variables.md#tidb-tidb_enable_resource_control) to control whether to enable flow control for a resource group. 
* TiKV: you can use the parameter [`resource_control.enabled`](/tikv-configuration-file.md#resource_control) to control whether to use request scheduling based on resource group quotas. 

<CustomContent platform="tidb-cloud">

> **Note:**
>
> The parameter `resource_control.enabled` is disabled by default. It does not support dynamic modification. You need to contact the [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) to enable it. You need to restart the TiKV instance for the modification to take effect.

</CustomContent>

The results of the combination of these two parameters are shown in the following table.

| `resource_control.enabled`  | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-------------------------------------|:-------------------------------------|
| `resource_control.enabled`= true  |  Flow control and scheduling (recommended) | Invalid combination      |  
| `resource_control.enabled`= false |  Only flow control                         | The feature is disabled. |

## How to use resource control

For an existing resource group, you can modify the read and write quota of the resource group by using [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md). The quota changes to the resource group take effect immediately.

You can delete a resource group by using [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md). The user bound by the deleted resource group will use the `default` resource group for resource isolation.

> **Note:**
> 
> - When you bind a user resource group with `CREATE USER` or `ALTER USER`, it will not take effect for the user's existing sessions, but only for the user's new sessions.
> - The `default` resource group does not have quota restrictions for bound user applications. It is recommended to create the `default` resource group by using [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md), or modify the quota for the `default` resource group by using [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) to control the quota for the `default` resource group.

### Prerequisites

To create, modify, or delete a resource group, you need to have the `SUPER` or `RESOURCE_GROUP_ADMIN` privilege.

You can create a resource group in the cluster with [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md), and then bind the users to a specific resource group by using [`CREATE USER`](/sql-statements/ sql-statement-create-user.md) or [`ALTER USER`](/sql-statements/sql-statement-alter-user.md).

### Step 1. Enable the resource control feature

Enable flow control for the resource group.

```sql
SET GLOBAL tidb_enable_resource_control = 'ON';
```

In TiKV, set the parameter `resource_control.enabled` to `true`. The parameter `resource_control.enabled` is disabled by default. You need to contact the [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) to enable it.

### Step 2. Create a resource group, and bind users to it

Resource group quotas are expressed as [RU (Resource Unit)](/tidb-RU.md), which is TiDB's unified abstraction of CPU, IO, and other system resources.

The following is an example of how to create a resource group and bind users to it.

1. Create a resource group `rg1` with a quota of 500 RU per second for read requests and 300 RU per second for write requests, and allow applications in this resource group to use excessive resources when system resources are available.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1
    RRU_PER_SEC = 500
    WRU_PER_SEC = 300
    BURSTABLE
    ;
    ```

2. Create a resource group `rg2` with a quota of 600 RU per second for read requests and 400 RU per second for write requests, and do not allow applications in this resource group to use excessive resources even when system resources are available.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2
    RRU_PER_SEC = 600
    WRU_PER_SEC = 400
    ;
    ```

3. Bind users `usr1` and `usr2` to resource groups `rg1` and `rg2` respectively.

    ```sql
    ALTER USER usr1 RESOURCE GROUP rg1;
    ```

    ```sql
    ALTER USER usr2 RESOURCE GROUP rg2;
    ```

After you complete the preceeding operations, the resource consumption by newly created sessions is controlled by the specified quota. Read requests are limited by the quota of the read RU, and write requests are limited by the quota of the write RU. If the system load is relatively high and there is no spare capacity, the resource consumption rate of both users will be strictly controlled not to exceed the quota. Meanwhile, the consumption ratio of RU metrics for both users' read and write requests is basically proportional to the specified quota. When system resources are abundant, the resource consumption rate of `usr1` is allowed to exceed the quota because it has set `BURSTABLE`.

## Monitoring and charts

TiDB regularly collects runtime information about resource control and provides visual charts of the metrics in Grafana's **TiDB** > **Resource Control** panel. The metrics are detailed in the **Resource Control** section of [TiDB Important Monitoring Metrics](/grafana-tidb-dashboard.md).

## Tool Compatibility

The resource control feature is not compatible with data export/import and replication tools including BR, TiDB Lightning, and TiCDC.

## Limitations

Currently, the resource control feature has the following limitations:

* This feature only supports restriction and scheduling of read and write requests initiated by frontend clients. It does not support restriction and scheduling of background tasks such as `DDL` and `Auto Analyze`. 
* Resource control will incur additional scheduling overhead. Therefore, there might be a slight performance degradation when this feature is enabled.

## See also

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://docs.google.com/document/d/1sV5EVv8Cdpc6aBCDihc2akpE0iuantPf/)
* [RU](/tidb-RU.md)
