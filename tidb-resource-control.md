---
title: Use Resource Control to Achieve Resource Isolation
summary: Learn how to use the resource control feature to control and schedule application resources.
---

# Use Resource Control to Achieve Resource Isolation

> **Warning:**
>
> This feature is experimental and its form and usage may change in subsequent versions.

As a cluster administrator, you can use the resource control feature to set read and write quotas for resource groups, and bind users to those groups. This allows the TiDB layer to control the flow of user read and write requests based on the quotas set for the resource group, while the TiKV layer schedules the requests based on the priority of the read and write quota mapping. By doing this, you can ensure resource isolation for your applications and meet quality of service (QoS) requirements.

The TiDB resource control feature provides two layers of resource management capabilities: the flow control capability at the TiDB layer and the priority scheduling capability at the TiKV layer. The two capabilities are orthogonal and can be enabled separately or simultaneously. See the [Parameters for resource control](#parameters-for-resource-control) for details.

- TiDB flow control:  TiDB flow control uses the [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket). If there are not enough tokens in the bucket, and the resource group does not specify the `BURSTABLE` option, the requests to the resource group will wait for the token bucket to backfill the tokens and retry. The retry might fail due to timeout.
- TiKV scheduling: If [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) is enabled, TiKV uses the value of `RU_PER_SEC` of each resource group to map the read and write requests of each resource group to their own priorities. Based on their own priorities, the storage layer uses the priority queue to schedule and process requests.

The introduction of the resource control feature is a milestone for TiDB. It can divide a distributed database cluster into multiple logical units. Even if an individual unit overuses resources, it does not crowd out the resources needed by other units.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

## Scenarios for resource control

With this feature, you can:

- Combine multiple small and medium-sized applications from different systems into a single TiDB cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. When the system workload is low, busy applications can still be allocated the required system resources even if they exceed the set read and write quotas, so as to achieve the maximum utilization of resources.
- Choose to combine all test environments into a single TiDB cluster, or group the batch tasks that consume more resources into a single resource group. It can improve hardware utilization and reduce operating costs while ensuring that critical applications can always get the necessary resources.

In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

## What is Request Unit (RU)

Request Unit (RU) is TiDB's unified abstraction unit for system resources, which currently includes CPU, IOPS and IO bandwidth metrics. The consumption of these three metrics is represented by RU according to a certain ratio.

The following table shows the consumption of TiKV storage layer CPU and IO resources by user requests and the corresponding RU weights.

| Resource        | RU Weight        |
|:----------------|:-----------------|
| CPU             | (1/3) RU/millisecond |
| Read IO         | (1/64) RU/KB       |
| Write IO        | 1 RU/KB          |
| Basic overhead of a read request   | 0.25 RU  |
| Basic overhead of a write request  | 1.5 RU   |

Based on the above table, assuming that the TiKV time consumed by a resource group is `c` milliseconds, `r1` requests that read `r2` KB data, and `w1` write requests that write `w2` KB data, then the formula for the total RUs consumed by the resource group is as follows:

`c`\* 1/3 + (`r1` \* 0.25 + `r2` \* 1/64) + (1.5 \* `w1` + `w2` \* 1 \* `n`)

## Parameters for resource control

The resource control feature introduces two new global variables.

* TiDB: you can use the system variable [`tidb_enable_resource_control`](/system-variables.md#tidb-tidb_enable_resource_control-new-in-v660) to control whether to enable flow control for a resource group.
* TiKV: you can use the parameter [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) to control whether to use request scheduling based on resource group quotas.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> The parameter `resource-control.enabled` is disabled by default. It does not support dynamic modification. You need to contact the [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) to enable it for TiDB Cloud Dedicated Tier clusters.

</CustomContent>

The results of the combinations of these two parameters are shown in the following table.

| `resource-control.enabled`  | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-------------------------------------|:-------------------------------------|
| `resource-control.enabled`= true  |  Flow control and scheduling (recommended) | Invalid combination      |  
| `resource-control.enabled`= false |  Only flow control (not recommended)                 | The feature is disabled. |

## How to use resource control

To create, modify, or delete a resource group, you need to have the `SUPER` or `RESOURCE_GROUP_ADMIN` privilege.

You can create a resource group in the cluster by using [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md), and then bind the users to a specific resource group by using [`CREATE USER`](/sql-statements/ sql-statement-create-user.md) or [`ALTER USER`](/sql-statements/sql-statement-alter-user.md).

For an existing resource group, you can modify the read and write quota of the resource group by using [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md). The quota changes to the resource group take effect immediately.

You can delete a resource group by using [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md).

> **Note:**
>
> - When you bind a user to a resource group by using `CREATE USER` or `ALTER USER`, it will not take effect for the user's existing sessions, but only for the user's new sessions.
> - If a user is not bound to a resource group or is bound to a `default` resource group, the user's requests are not subject to TiDB's flow control restrictions. The `default` resource group is currently not visible to the user and cannot be created or modified.

### Step 1. Enable the resource control feature

Enable the resource control feature.

```sql
SET GLOBAL tidb_enable_resource_control = 'ON';
```

<CustomContent platform="tidb">

In TiKV, set the parameter [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) to `true`.

</CustomContent>

<CustomContent platform="tidb-cloud">

In TiKV, set the parameter [`resource-control.enabled`](https://docs.pingcap.com/tidb/stable/tikv-configuration-file#resource_control) to `true`. The parameter `resource-control.enabled` is disabled by default. You need to contact the [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) to enable it.

</CustomContent>

### Step 2. Create a resource group, and then bind users to it

The following is an example of how to create a resource group and bind users to it.

1. Create a resource group `rg1`. The RU backfill rate is 500 RUs per second and allows applications in this resource group to overrun resources.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2. Create a resource group `rg2`. The RU backfill rate is 500 RUs per second and does not allow applications in this resource group to overrun resources.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3. Bind users `usr1` and `usr2` to resource groups `rg1` and `rg2` respectively.

    ```sql
    ALTER USER usr1 RESOURCE GROUP rg1;
    ```

    ```sql
    ALTER USER usr2 RESOURCE GROUP rg2;
    ```

After you complete the above operations of creating resource groups and binding users, the resource consumption of newly created sessions will be controlled by the specified quota. If the system load is relatively high and there is no spare capacity, the resource consumption rate of `usr2` will be strictly controlled not to exceed the quota. Because `usr1` bound by `rg1` is configured with `BURSTABLE`, the consumption rate of `usr1` is allowed to exceed the quota.

If the resource group corresponds to a request with insufficient quota, the client's request will wait. If the wait time is too long, the request will report an error.

## Monitoring and charts

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is not applicable to TiDB Cloud.

</CustomContent>

TiDB regularly collects runtime information about resource control and provides visual charts of the metrics in Grafana's **TiDB** > **Resource Control** panel. The metrics are detailed in the **Resource Control** section of [TiDB Important Monitoring Metrics](/grafana-tidb-dashboard.md).

## Tool Compatibility

The resource control feature is still in its experimental stage and does not impact the regular usage of data import, export, and other replication tools. BR, TiDB Lightning, and TiCDC do not currently support resource control related DDL processing, and their resource consumption is not limited by resource control.

## Limitations

Currently, the resource control feature has the following limitations:

* This feature only supports restriction and scheduling of read and write requests initiated by frontend clients. It does not support restriction and scheduling of background tasks such as `DDL` and `Auto Analyze`. 
* Resource control incurs additional scheduling overhead. Therefore, there might be a slight performance degradation when this feature is enabled.

## See also

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://docs.google.com/document/d/1sV5EVv8Cdpc6aBCDihc2akpE0iuantPf/)
