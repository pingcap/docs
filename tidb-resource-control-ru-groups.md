---
title: Use Resource Control to Achieve Resource Group Limitation and Flow Control
summary: Learn how to use the resource control feature to control and schedule application resources.
aliases: ['/tidb/v8.5/tidb-resource-control/','/tidb/stable/tidb-resource-control/']
---

# Use Resource Control to Achieve Resource Group Limitation and Flow Control

> **Note:**
>
> This feature is not available on [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

As a cluster administrator, you can use the resource control feature to create resource groups, set quotas for resource groups, and bind users to those groups.

The TiDB resource control feature provides two layers of resource management capabilities: the flow control capability at the TiDB layer and the priority scheduling capability at the TiKV layer. The two capabilities can be enabled separately or simultaneously. See the [Parameters for resource control](#parameters-for-resource-control) for details. This allows the TiDB layer to control the flow of user read and write requests based on the quotas set for the resource groups, and allows the TiKV layer to schedule the requests based on the priority mapped to the read and write quota. By doing this, you can ensure resource isolation for your applications and meet quality of service (QoS) requirements.

- TiDB flow control: TiDB flow control uses the [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket). If there are not enough tokens in a bucket, and the resource group does not specify the `BURSTABLE` option, the requests to the resource group will wait for the token bucket to backfill the tokens and retry. The retry might fail due to timeout.

- TiKV scheduling: You can set the absolute priority [(`PRIORITY`)](/information-schema/information-schema-resource-groups.md#examples) as needed. Different resources are scheduled according to the `PRIORITY` setting. Tasks with high `PRIORITY` are scheduled first. If you do not set the absolute priority, TiKV uses the value of `RU_PER_SEC` of each resource group to determine the priority of the read and write requests for each resource group. Based on the priorities, the storage layer uses the priority queue to schedule and process requests.

Starting from v7.4.0, the resource control feature supports controlling TiFlash resources. Its principle is similar to that of TiDB flow control and TiKV scheduling:

<CustomContent platform="tidb">

- TiFlash flow control: With the [TiFlash pipeline execution model](/tiflash/tiflash-pipeline-model.md), TiFlash can more accurately obtain the CPU consumption of different queries and convert it into [Request Units (RU)](#what-is-request-unit-ru) for deduction. Traffic control is implemented using a token bucket algorithm.
- TiFlash scheduling: When system resources are insufficient, TiFlash schedules pipeline tasks among multiple resource groups based on their priorities. The specific logic is: First, TiFlash assesses the `PRIORITY` of the resource group, then considers the CPU usage and `RU_PER_SEC`. As a result, if `rg1` and `rg2` have the same `PRIORITY` but the `RU_PER_SEC` of `rg2` is twice that of `rg1`, the CPU usage of `rg2` is twice that of `rg1`.

</CustomContent>

<CustomContent platform="tidb-cloud">

- TiFlash flow control: With the [TiFlash pipeline execution model](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model), TiFlash can more accurately obtain the CPU consumption of different queries and convert it into [Request Units (RU)](#what-is-request-unit-ru) for deduction. Traffic control is implemented using a token bucket algorithm.
- TiFlash scheduling: When system resources are insufficient, TiFlash schedules pipeline tasks among multiple resource groups based on their priorities. The specific logic is: First, TiFlash assesses the `PRIORITY` of the resource group, then considers the CPU usage and `RU_PER_SEC`. As a result, if `rg1` and `rg2` have the same `PRIORITY` but the `RU_PER_SEC` of `rg2` is twice that of `rg1`, the CPU usage of `rg2` is twice that of `rg1`.

</CustomContent>

For information on how to manage background tasks and handle resource-intensive queries (Runaway Queries), see the following documents:

- [Use Resource Control to Managing Background Tasks](/tidb-resource-control-background-tasks.md)
- [Manage Queries That Consume More Resources Than Expected (Runaway Queries)](/tidb-resource-control-runaway-queries.md)

## Scenarios for resource control

The introduction of the resource control feature is a milestone for TiDB. It can divide a distributed database cluster into multiple logical units. Even if an individual unit overuses resources, it does not crowd out the resources needed by other units.

With this feature, you can:

- Combine multiple small and medium-sized applications from different systems into a single TiDB cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. When the system workload is low, busy applications can still be allocated the required system resources even if they exceed the set quotas, so as to achieve the maximum utilization of resources.
- Choose to combine all test environments into a single TiDB cluster, or group the batch tasks that consume more resources into a single resource group. It can improve hardware utilization and reduce operating costs while ensuring that critical applications can always get the necessary resources.
- When there are mixed workloads in a system, you can put different workloads into separate resource groups. By using the resource control feature, you can ensure that the response time of transactional applications is not affected by data analysis or batch applications.
- When the cluster encounters an unexpected SQL performance issue, you can use SQL bindings along with resource groups to temporarily limit the resource consumption of a SQL statement.

In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

> **Note:**
>
> - To assess the effectiveness of resource management, it is recommended to deploy the cluster on independent computing and storage nodes. Scheduling and other cluster resource-sensitive features are hardly working properly on the deployment created by `tiup playground`, where the resources are shared across instances. 

## Limitations

Resource control incurs additional scheduling overhead. Therefore, there might be a slight performance degradation (less than 5%) when this feature is enabled.

## What is Request Unit (RU)

Request Unit (RU) is a unified abstraction unit in TiDB for system resources, which currently includes CPU, IOPS, and IO bandwidth metrics. It is used to indicate the amount of resources consumed by a single request to the database. The number of RUs consumed by a request depends on a variety of factors, such as the type of operations, and the amount of data being queried or modified. Currently, the RU contains consumption statistics for the resources in the following table:

<table>
    <thead>
        <tr>
            <th>Resource type</th>
            <th>RU consumption</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3">Read</td>
            <td>2 storage read batches consume 1 RU</td>
        </tr>
        <tr>
            <td>8 storage read requests consume 1 RU</td>
        </tr>
        <tr>
            <td>64 KiB read request payload consumes 1 RU</td>
        </tr>
        <tr>
            <td rowspan="3">Write</td>
            <td>1 storage write batch consumes 1 RU</td>
        </tr>
        <tr>
            <td>1 storage write request consumes 1 RU</td>
        </tr>
        <tr>
            <td>1 KiB write request payload consumes 1 RU</td>
        </tr>
        <tr>
            <td>CPU</td>
            <td> 3 ms consumes 1 RU</td>
        </tr>
    </tbody>
</table>

> **Note:**
>
> - Each write operation is eventually replicated to all replicas (by default, TiKV has 3 replicas). Each replication operation is considered a different write operation.
> - The preceding table lists only the resources involved in RU calculation for TiDB Self-Managed clusters, excluding the network and storage consumption. For {{{ .starter }}} RUs, see [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/).
> - Currently, TiFlash resource control only considers SQL CPU, which is the CPU time consumed by the execution of pipeline tasks for queries, and read request payload.

## Parameters for resource control

The resource control feature introduces the following system variables or parameters:

* TiDB: you can use the [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) system variable to control whether to enable flow control for resource groups.

<CustomContent platform="tidb">

* TiKV: you can use the [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) parameter to control whether to use request scheduling based on resource groups.
* TiFlash: you can use the [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) system variable and the [`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) configuration item (introduced in v7.4.0) to control whether to enable TiFlash resource control.

</CustomContent>

<CustomContent platform="tidb-cloud">

* TiKV: For TiDB Self-Managed, you can use the `resource-control.enabled` parameter to control whether to use request scheduling based on resource group quotas. For TiDB Cloud, the value of the `resource-control.enabled` parameter is `true` by default and does not support dynamic modification.
* TiFlash: For TiDB Self-Managed, you can use the `tidb_enable_resource_control` system variable and the `enable_resource_control` configuration item (introduced in v7.4.0) to control whether to enable TiFlash resource control.

</CustomContent>

Starting from TiDB v7.0.0, `tidb_enable_resource_control` and `resource-control.enabled` are enabled by default. The results of the combinations of these two parameters are shown in the following table.

| `resource-control.enabled`  | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-------------------------------------|:-------------------------------------|
| `resource-control.enabled`= true  |  Flow control and scheduling (recommended) | Invalid combination      |
| `resource-control.enabled`= false |  Only flow control (not recommended)                 | The feature is disabled. |

<CustomContent platform="tidb">

Starting from v7.4.0, the TiFlash configuration item `enable_resource_control` is enabled by default. It works together with `tidb_enable_resource_control` to control the TiFlash resource control feature. TiFlash resource control only performs flow control and priority scheduling when both `enable_resource_control` and `tidb_enable_resource_control` are enabled. Additionally, when `enable_resource_control` is enabled, TiFlash uses the [Pipeline execution model](/tiflash/tiflash-pipeline-model.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Starting from v7.4.0, the TiFlash configuration item `enable_resource_control` is enabled by default. It works together with `tidb_enable_resource_control` to control the TiFlash resource control feature. TiFlash resource control only performs flow control and priority scheduling when both `enable_resource_control` and `tidb_enable_resource_control` are enabled. Additionally, when `enable_resource_control` is enabled, TiFlash uses the [Pipeline execution model](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model).

</CustomContent>

For more information about the resource control mechanism and parameters, see [RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2022-11-25-global-resource-control.md) and [TiFlash Resource Control](https://github.com/pingcap/tiflash/blob/release-8.5/docs/design/2023-09-21-tiflash-resource-control.md).

## How to use resource control

This section describes how to use the resource control feature to manage resource groups and control the resource allocation of each resource group.

### Estimate cluster capacity

<CustomContent platform="tidb">

Before resource planning, you need to know the overall capacity of the cluster. TiDB provides the statement [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md) to estimate the cluster capacity. You can use one of the following methods:

- [Estimate capacity based on actual workload](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
- [Estimate capacity based on hardware deployment](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

You can view the [Resource Manager page](/dashboard/dashboard-resource-manager.md) in TiDB Dashboard. For more information, see [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#methods-for-estimating-capacity).

</CustomContent>

<CustomContent platform="tidb-cloud">

For TiDB Self-Managed, you can use the [`CALIBRATE RESOURCE`](https://docs.pingcap.com/tidb/stable/sql-statement-calibrate-resource) statement to estimate the cluster capacity.

For TiDB Cloud, the [`CALIBRATE RESOURCE`](https://docs.pingcap.com/tidb/stable/sql-statement-calibrate-resource) statement is inapplicable.

</CustomContent>

### Manage resource groups

To create, modify, or delete a resource group, you need to have the `SUPER` or `RESOURCE_GROUP_ADMIN` privilege.

You can create a resource group for a cluster by using [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md).

For an existing resource group, you can modify the `RU_PER_SEC` option (the rate of RU backfilling per second) of the resource group by using [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md). The changes to the resource group take effect immediately.

You can delete a resource group by using [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md).

### Create a resource group

The following is an example of how to create a resource group.

1. Create a resource group `rg1`. The resource limit is 500 RUs per second and allows applications in this resource group to overrun resources.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2. Create a resource group `rg2`. The RU backfill rate is 600 RUs per second and does not allow applications in this resource group to overrun resources.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3. Create a resource group `rg3` with the absolute priority set to `HIGH`. The absolute priority currently supports `LOW|MEDIUM|HIGH`. The default value is `MEDIUM`.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg3 RU_PER_SEC = 100 PRIORITY = HIGH;
    ```

### Bind resource groups

TiDB supports three levels of resource group settings as follows.

- User level. Bind a user to a specific resource group via the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) or [`ALTER USER`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user) statement. After a user is bound to a resource group, sessions created by the user are automatically bound to the corresponding resource group.
- Session level. Set the resource group for the current session via [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md).
- Statement level. Set the resource group for the current statement via [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) Optimizer Hint.

#### Bind users to a resource group

The following example creates a user `usr1` and binds the user to the resource group `rg1`. `rg1` is the resource group created in the example in [Create Resource Group](#create-a-resource-group).

```sql
CREATE USER 'usr1'@'%' IDENTIFIED BY '123' RESOURCE GROUP rg1;
```

The following example uses `ALTER USER` to bind the user `usr2` to the resource group `rg2`. `rg2` is the resource group created in the example in [Create Resource Group](#create-a-resource-group).

```sql
ALTER USER usr2 RESOURCE GROUP rg2;
```

After you bind users, the resource consumption of newly created sessions will be controlled by the specified quota (Request Unit, RU). If the system workload is relatively high and there is no spare capacity, the resource consumption rate of `usr2` will be strictly controlled not to exceed the quota. Because `usr1` is bound by `rg1` with `BURSTABLE` configured, the consumption rate of `usr1` is allowed to exceed the quota.

If there are too many requests that result in insufficient resources for the resource group, the client's requests will wait. If the wait time is too long, the requests will report an error.

> **Note:**
>
> - When you bind a user to a resource group by using `CREATE USER` or `ALTER USER`, it will not take effect for the user's existing sessions, but only for the user's new sessions.
> - TiDB automatically creates a `default` resource group during cluster initialization. For this resource group, the default value of `RU_PER_SEC` is `UNLIMITED` (equivalent to the maximum value of the `INT` type, that is, `2147483647`) and it is in `BURSTABLE` mode. Statements that are not bound to a resource group are automatically bound to this resource group. This resource group does not support deletion, but you can modify the configuration of its RU.

To unbind users from a resource group, you can simply bind them to the `default` group again as follows:

```sql
ALTER USER 'usr3'@'%' RESOURCE GROUP `default`;
```

For more details, see [`ALTER USER ... RESOURCE GROUP`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user).

#### Bind the current session to a resource group

You can use the [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) statement to change the bound resource group of the current session. By binding a session to a resource group, the resource usage of the corresponding session is limited by the specified usage (RU).

When the system variable [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) is set to `ON`, you need to have the `SUPER` or `RESOURCE_GROUP_ADMIN` or `RESOURCE_GROUP_USER` privilege to execute this statement.

The following example binds the current session to the resource group `rg1`.

```sql
SET RESOURCE GROUP rg1;
```

#### Bind the current statement to a resource group

By adding the [`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name) hint to a SQL statement, you can specify the resource group to which the statement is bound. This hint supports `SELECT`, `INSERT`, `UPDATE`, and `DELETE` statements.

When the system variable [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) is set to `ON`, you need to have the `SUPER` or `RESOURCE_GROUP_ADMIN` or `RESOURCE_GROUP_USER` privilege to use this hint.

The following example binds the current statement to the resource group `rg1`.

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

## Disable resource control

<CustomContent platform="tidb">

1. Execute the following statement to disable the resource control feature.

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. Set the TiKV parameter [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) to `false` to disable scheduling based on the RU of the resource group.

3. Set the TiFlash configuration item [`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) to `false` to disable TiFlash resource control.

</CustomContent>

<CustomContent platform="tidb-cloud">

1. Execute the following statement to disable the resource control feature.

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. For TiDB Self-Managed, you can use the `resource-control.enabled` parameter to control whether to use request scheduling based on resource group quotas. For TiDB Cloud, the value of the `resource-control.enabled` parameter is `true` by default and does not support dynamic modification. If you need to disable it for TiDB Cloud Dedicated clusters, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

3. For TiDB Self-Managed, you can use the `enable_resource_control` configuration item to control whether to enable TiFlash resource control. For TiDB Cloud, the value of the `enable_resource_control` parameter is `true` by default and does not support dynamic modification. If you need to disable it for TiDB Cloud Dedicated clusters, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

</CustomContent>

## View RU consumption

You can view information about RU consumption.

### View the RU consumption by SQL

You can view the RU consumption of SQL statements in the following ways:

- The system variable `tidb_last_query_info`
- `EXPLAIN ANALYZE`
- Slow queries and corresponding system table
- `statements_summary`

#### View the RUs consumed by the last SQL execution by querying the system variable `tidb_last_query_info`

TiDB provides the system variable [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014). This system variable records the information of the last DML statement executed, including the RUs consumed by the SQL execution.

Example:

1. Run the `UPDATE` statement:

    ```sql
    UPDATE sbtest.sbtest1 SET k = k + 1 WHERE id = 1;
    ```

    ```
    Query OK, 1 row affected (0.01 sec)
    Rows matched: 1  Changed: 1  Warnings: 0
    ```

2. Query the system variable `tidb_last_query_info` to view the information of the last executed statement:

    ```sql
    SELECT @@tidb_last_query_info;
    ```

    ```
    +------------------------------------------------------------------------------------------------------------------------+
    | @@tidb_last_query_info                                                                                                 |
    +------------------------------------------------------------------------------------------------------------------------+
    | {"txn_scope":"global","start_ts":446809472210829315,"for_update_ts":446809472210829315,"ru_consumption":4.34885578125} |
    +------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.01 sec)
    ```

    In the result, `ru_consumption` is the RUs consumed by the execution of this SQL statement.

#### View RUs consumed during SQL execution by `EXPLAIN ANALYZE`

You can use the [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption) statement to get the amount of RUs consumed during SQL execution. Note that the amount of RUs is affected by the cache (for example, [coprocessor cache](/coprocessor-cache.md)). When the same SQL is executed multiple times, the amount of RUs consumed by each execution might be different. The RU value does not represent the exact value for each execution, but can be used as a reference for estimation.

#### Slow queries and the corresponding system table

<CustomContent platform="tidb">

When you enable resource control, the [slow query log](/identify-slow-queries.md) of TiDB and the corresponding system table [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) contain the resource group, RU consumption of the corresponding SQL, and the time spent waiting for available RUs.

</CustomContent>

<CustomContent platform="tidb-cloud">

When you enable resource control, the system table [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) contains the resource group, RU consumption of the corresponding SQL, and the time spent waiting for available RUs.

</CustomContent>

#### View RU statistics by `statements_summary`

The system table [`INFORMATION_SCHEMA.statements_summary`](/statement-summary-tables.md#statements_summary) in TiDB stores the normalized and aggregated statistics of SQL statements. You can use the system table to view and analyze the execution performance of SQL statements. It also contains statistics about resource control, including the resource group name, RU consumption, and the time spent waiting for available RUs. For more details, see [`statements_summary` fields description](/statement-summary-tables.md#statements_summary-fields-description).

### View the RU consumption of resource groups

Starting from v7.6.0, TiDB provides the system table [`mysql.request_unit_by_group`](/mysql-schema/mysql-schema.md#system-tables-related-to-resource-control) to store the historical records of the RU consumption of each resource group.

Example:

```sql
SELECT * FROM request_unit_by_group LIMIT 5;
```

```
+----------------------------+----------------------------+----------------+----------+
| start_time                 | end_time                   | resource_group | total_ru |
+----------------------------+----------------------------+----------------+----------+
| 2024-01-01 00:00:00.000000 | 2024-01-02 00:00:00.000000 | default        |   334147 |
| 2024-01-01 00:00:00.000000 | 2024-01-02 00:00:00.000000 | rg1            |     4172 |
| 2024-01-01 00:00:00.000000 | 2024-01-02 00:00:00.000000 | rg2            |    34028 |
| 2024-01-02 00:00:00.000000 | 2024-01-03 00:00:00.000000 | default        |   334088 |
| 2024-01-02 00:00:00.000000 | 2024-01-03 00:00:00.000000 | rg1            |     3850 |
+----------------------------+----------------------------+----------------+----------+
5 rows in set (0.01 sec)
```

> **Note:**
>
> The data of `mysql.request_unit_by_group` is automatically imported by a TiDB scheduled task at the end of each day. If the RU consumption of a resource group is 0 on a certain day, no record is generated. By default, this table stores data for the last three months (up to 92 days). Data that exceeds this period is automatically cleared.

## Monitoring metrics and charts

<CustomContent platform="tidb">

TiDB regularly collects runtime information about resource control and provides visual charts of the metrics in Grafana's **TiDB** > **Resource Control** dashboard. The metrics are detailed in the **Resource Control** section of [TiDB Important Monitoring Metrics](/grafana-tidb-dashboard.md).

TiKV also records the request QPS from different resource groups. For more details, see [TiKV Monitoring Metrics Detail](/grafana-tikv-dashboard.md#grpc).

You can view the data of resource groups in the current [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md) table in TiDB Dashboard. For more details, see [Resource Manager page](/dashboard/dashboard-resource-manager.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is only applicable to TiDB Self-Managed. Currently, TiDB Cloud does not provide resource control metrics.

TiDB regularly collects runtime information about resource control and provides visual charts of the metrics in Grafana's **TiDB** > **Resource Control** dashboard.

TiKV also records the request QPS from different resource groups in Grafana's **TiKV** dashboard.

</CustomContent>

## Tool compatibility

The resource control feature does not impact the regular usage of data import, export, and other replication tools. BR, TiDB Lightning, and TiCDC do not currently support processing DDL operations related to resource control, and their resource consumption is not limited by resource control.

## FAQ

1. Do I have to disable resource control if I don't want to use resource groups?

    No. Users who do not specify any resource groups will be bound to the `default` resource group that has unlimited resources. When all users belong to the `default` resource group, the resource allocation method is the same as when the resource control is disabled.

2. Can a database user be bound to several resource groups?

    No. A database user can only be bound to one resource group. However, during the session runtime, you can use [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) to set the resource group used by the current session. You can also use the optimizer hint [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) to set the resource group for the running statement.

3. What happens when the total resource allocation (`RU_PER_SEC`) of all resource groups exceeds the system capacity?

    TiDB does not verify the capacity when you create a resource group. As long as the system has enough available resources, TiDB can meet the resource requirements of each resource group. When the system resources exceed the limit, TiDB prioritizes satisfying requests from resource groups with higher priority. If requests with the same priority cannot all be met, TiDB allocates resources proportionally according to the resource allocation (`RU_PER_SEC`).

## See also

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2022-11-25-global-resource-control.md)
