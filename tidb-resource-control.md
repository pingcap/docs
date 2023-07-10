---
title: Use Resource Control to Achieve Resource Isolation
summary: Learn how to use the resource control feature to control and schedule application resources.
---

# Use Resource Control to Achieve Resource Isolation

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [TiDB Serverless clusters](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

</CustomContent>

As a cluster administrator, you can use the resource control feature to create resource groups, set quotas for resource groups, and bind users to those groups.

The TiDB resource control feature provides two layers of resource management capabilities: the flow control capability at the TiDB layer and the priority scheduling capability at the TiKV layer. The two capabilities can be enabled separately or simultaneously. See the [Parameters for resource control](#parameters-for-resource-control) for details. This allows the TiDB layer to control the flow of user read and write requests based on the quotas set for the resource groups, and allows the TiKV layer to schedule the requests based on the priority mapped to the read and write quota. By doing this, you can ensure resource isolation for your applications and meet quality of service (QoS) requirements.

- TiDB flow control: TiDB flow control uses the [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket). If there are not enough tokens in a bucket, and the resource group does not specify the `BURSTABLE` option, the requests to the resource group will wait for the token bucket to backfill the tokens and retry. The retry might fail due to timeout.

- TiKV scheduling: You can set the absolute priority [(`PRIORITY`)](/information-schema/information-schema-resource-groups.md#examples) as needed. Different resources are scheduled according to the `PRIORITY` setting. Tasks with high `PRIORITY` are scheduled first. If you do not set the absolute priority, TiKV uses the value of `RU_PER_SEC` of each resource group to determine the priority of the read and write requests for each resource group. Based on the priorities, the storage layer uses the priority queue to schedule and process requests.

## Scenarios for resource control

The introduction of the resource control feature is a milestone for TiDB. It can divide a distributed database cluster into multiple logical units. Even if an individual unit overuses resources, it does not crowd out the resources needed by other units.

With this feature, you can:

- Combine multiple small and medium-sized applications from different systems into a single TiDB cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. When the system workload is low, busy applications can still be allocated the required system resources even if they exceed the set quotas, so as to achieve the maximum utilization of resources.
- Choose to combine all test environments into a single TiDB cluster, or group the batch tasks that consume more resources into a single resource group. It can improve hardware utilization and reduce operating costs while ensuring that critical applications can always get the necessary resources.
- When there are mixed workloads in a system, you can put different workloads into separate resource groups. By using the resource control feature, you can ensure that the response time of transactional applications is not affected by data analysis or batch applications.
- When the cluster encounters an unexpected SQL performance issue, you can use SQL bindings along with resource groups to temporarily limit the resource consumption of a SQL statement.

In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

## Limitations

Currently, the resource control feature has the following limitations:

* This feature only supports flow control and scheduling of read and write requests initiated by foreground clients. It does not support flow control and scheduling of background tasks such as DDL operations and auto analyze.
* Resource control incurs additional scheduling overhead. Therefore, there might be a slight performance degradation when this feature is enabled.

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
            <td>1 storage write batch consumes 1 RU for each replica</td>
        </tr>
        <tr>
            <td>1 storage write request consumes 1 RU</td>
        </tr>
        <tr>
            <td>1 KiB write request payload consumes 1 RU</td>
        </tr>
        <tr>
            <td>SQL CPU</td>
            <td> 3 ms consumes 1 RU</td>
        </tr>
    </tbody>
</table>

> **Note:**
>
> - Each write operation is eventually replicated to all replicas (by default, TiKV has 3 replicas). Each replication operation is considered a different write operation.
> - In addition to queries executed by users, RU can be consumed by background tasks, such as automatic statistics collection.
> - The preceding table lists only the resources involved in RU calculation for TiDB Self-Hosted clusters, excluding the network and storage consumption. For TiDB Serverless RUs, see [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/).

## Parameters for resource control

The resource control feature introduces two new global variables.

* TiDB: you can use the [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) system variable to control whether to enable flow control for resource groups.

<CustomContent platform="tidb">

* TiKV: you can use the [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) parameter to control whether to use request scheduling based on resource groups.

</CustomContent>

<CustomContent platform="tidb-cloud">

* TiKV: For TiDB Self-Hosted, you can use the `resource-control.enabled` parameter to control whether to use request scheduling based on resource group quotas. For TiDB Cloud, the value of the `resource-control.enabled` parameter is `true` by default and does not support dynamic modification.

</CustomContent>

Starting from TiDB v7.0.0, both parameters are enabled by default. The results of the combinations of these two parameters are shown in the following table.

| `resource-control.enabled`  | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-------------------------------------|:-------------------------------------|
| `resource-control.enabled`= true  |  Flow control and scheduling (recommended) | Invalid combination      |
| `resource-control.enabled`= false |  Only flow control (not recommended)                 | The feature is disabled. |

For more information about the resource control mechanism and parameters, see [RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md).

## How to use resource control

This section describes how to use the resource control feature to manage resource groups and control the resource allocation of each resource group.

### Estimate cluster capacity

Before resource planning, you need to know the overall capacity of the cluster. TiDB provides the statement [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md) to estimate the cluster capacity. You can use one of the following methods:

- [Estimate capacity based on actual workload](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
- [Estimate capacity based on hardware deployment](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

<CustomContent platform="tidb">

You can view the [Resource Manager page](/dashboard/dashboard-resource-manager.md) in TiDB Dashboard. For more information, see [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#methods-for-estimating-capacity).

</CustomContent>

<CustomContent platform="tidb-cloud">

For more information, see [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#methods-for-estimating-capacity).

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

#### Bind the current session to a resource group

By binding a session to a resource group, the resource usage of the corresponding session is limited by the specified usage (RU).

The following example binds the current session to the resource group `rg1`.

```sql
SET RESOURCE GROUP rg1;
```

#### Bind the current statement to a resource group

By adding the [`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name) hint to a SQL statement, you can specify the resource group to which the statement is bound. This hint supports `SELECT`, `INSERT`, `UPDATE`, and `DELETE` statements.

The following example binds the current statement to the resource group `rg1`.

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

### Manage queries that consume more resources than expected (Runaway Queries)

> **Warning:**
>
> This feature is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

A runaway query is a query that takes excessive time or resources than expected. Starting from TiDB v7.2.0, the resource control feature introduces the management of runaway queries. You can set criteria for a resource group to identify runaway queries and automatically take actions to prevent them from exhausting resources and affecting other queries.

You can manage runaway queries for a resource group by configuring the `QUERY_LIMIT` field in [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) or [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md).

#### `QUERY_LIMIT` parameters

Supported condition setting:

- `EXEC_ELAPSED`: a query is identified as a runaway query when the query execution time exceeds this limit.

Supported operations (`ACTION`):

- `DRYRUN`: no action is taken. The records are appended for the runaway queries. This is mainly used to observe whether the condition setting is reasonable.
- `COOLDOWN`: the execution priority of the query is lowered to the lowest level. The query continues to execute with the lowest priority and does not occupy resources of other operations.
- `KILL`: the identified query is automatically terminated and reports an error `Query execution was interrupted, identified as runaway query`.

To avoid too many concurrent runaway queries that exhaust system resources before being identified by conditions, the resource control feature introduces a quick identification mechanism. By using the `WATCH` clause, when a query is identified as a runaway query, the current TiDB instance marks the matching queries as runaway queries immediately in the next period of time (defined by `DURATION`), and takes the corresponding actions, instead of waiting for them to be identified by conditions. The `KILL` operation reports an error `Quarantined and interrupted because of being in runaway watch list`.

There are two methods for `WATCH` to match for rapid identification:

- `EXACT` indicates that only SQL statements with exactly the same SQL text are quickly identified.
- `SIMILAR` indicates all SQL statements with the same pattern are matched by Plan Digest, and the literal values are ignored.

The parameters of `QUERY_LIMIT` are as follows:

| Parameter          | Description            | Note                                  |
|---------------|--------------|--------------------------------------|
| `EXEC_ELAPSED`  | When the query execution time exceeds this value, it is identified as a runaway query | EXEC_ELAPSED =`60s` means the query is identified as a runaway query if it takes more than 60 seconds to execute. |
| `ACTION`    | Action taken when a runaway query is identified | The optional values are `DRYRUN`, `COOLDOWN`, and `KILL`. |
| `WATCH`   | Quickly match the identified runaway query. If the same or similar query is encountered again within a certain period of time, the corresponding action is performed immediately. | Optional. For example, `WATCH=SIMILAR DURATION '60s'` and `WATCH=EXACT DURATION '1m'`. |

#### Examples

1. Create a resource group `rg1` with a quota of 500 RUs per second, and define a runaway query as one that exceeds 60 seconds, and lower the priority of the runaway query.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=COOLDOWN);
    ```

2. Change the `rg1` resource group to terminate the runaway queries, and mark the queries with the same pattern as runaway queries immediately in the next 10 minutes.

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=SIMILAR DURATION='10m');
    ```

3. Change the `rg1` resource group to cancel the runaway query check.

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=NULL;
    ```

#### Observability

You can get more information about runaway queries from the following system tables:

+ The `mysql.tidb_runaway_queries` table contains the history records of all runaway queries identified in the past 7 days. Take one of the rows as an example:

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_runaway_queries LIMIT 1\G;
    *************************** 1. row ***************************
    resource_group_name: rg1
                   time: 2023-06-16 17:40:22
             match_type: identify
                 action: kill
           original_sql: select * from sbtest.sbtest1
            plan_digest: 5b7d445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
            tidb_server: 127.0.0.1:4000
    ```

    In the preceding output,`match_type` indicates how the runaway query is identified. The value can be one of the following:

    - `identify` means that it matches the condition of the runaway query.
    - `watch` means that it matches the quick identification rule in the watch list.

+ The `mysql.tidb_runaway_quarantined_watch` table contains the quick identification rule records for runaway queries. Take two of these rows as examples:

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_runaway_quarantined_watch LIMIT 2\G;
    *************************** 1. row ***************************
    resource_group_name: rg1
             start_time: 2023-06-16 17:40:22
               end_time: 2023-06-16 18:10:22
                  watch: similar
             watch_text: 5b7d445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
            tidb_server: 127.0.0.1:4000
    *************************** 2. row ***************************
    resource_group_name: rg1
             start_time: 2023-06-16 17:42:35
               end_time: 2023-06-16 18:12:35
                  watch: exact
             watch_text: select * from sbtest.sbtest1
            tidb_server: 127.0.0.1:4000
    ```

    In the preceding output:

    - `start_time` and `end_time` indicate the time range during which the watch list is valid.
    - `watch` means that the query matches the quick identification rule in the watch list. The value can be one of the following:
        - `similar` indicates that it is matched by Plan Digest. At this time, the `watch_text` column displays the Plan Digest.
        - `exact` indicates that it is matched by SQL text. At this time, the `watch_text` column displays the SQL text.

## Disable resource control

<CustomContent platform="tidb">

1. Execute the following statement to disable the resource control feature.

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. Set the TiKV parameter [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) to `false` to disable scheduling based on the RU of the resource group.

</CustomContent>

<CustomContent platform="tidb-cloud">

1. Execute the following statement to disable the resource control feature.

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. For TiDB Self-Hosted, you can use the `resource-control.enabled` parameter to control whether to use request scheduling based on resource group quotas. For TiDB Cloud, the value of the `resource-control.enabled` parameter is `true` by default and does not support dynamic modification. If you need to disable it for TiDB Dedicated clusters, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

</CustomContent>

## Monitoring metrics and charts

<CustomContent platform="tidb">

TiDB regularly collects runtime information about resource control and provides visual charts of the metrics in Grafana's **TiDB** > **Resource Control** dashboard. The metrics are detailed in the **Resource Control** section of [TiDB Important Monitoring Metrics](/grafana-tidb-dashboard.md).

TiKV also records the request QPS from different resource groups. For more details, see [TiKV Monitoring Metrics Detail](/grafana-tikv-dashboard.md#grpc).

You can view the data of resource groups in the current [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md) table in TiDB Dashboard. For more details, see [Resource Manager page](/dashboard/dashboard-resource-manager.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is only applicable to TiDB Self-Hosted. Currently, TiDB Cloud does not provide resource control metrics.

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
* [RESOURCE GROUP RFC](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md)
