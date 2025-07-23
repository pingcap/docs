---
title: 使用资源控制实现资源组限制与流量控制
summary: 学习如何使用资源控制功能对应用资源进行控制和调度。
aliases: ['/tidb/v8.5/tidb-resource-control/','/tidb/stable/tidb-resource-control/']
---

# 使用资源控制实现资源组限制与流量控制

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

作为集群管理员，你可以使用资源控制功能创建资源组，设置资源组配额，并绑定用户到这些资源组。

TiDB 的资源控制功能提供了两层资源管理能力：TiDB 层的流量控制能力和 TiKV 层的优先级调度能力。这两种能力可以单独启用或同时启用。详细信息请参见 [Parameters for resource control](#parameters-for-resource-control)。这样，TiDB 层可以根据为资源组设置的配额控制用户读写请求的流量，而 TiKV 层可以根据映射到读写配额的优先级调度请求。通过这种方式，你可以确保应用的资源隔离，并满足服务质量（QoS）要求。

- TiDB 流量控制：TiDB 流量控制采用 [token bucket 算法](https://en.wikipedia.org/wiki/Token_bucket)。如果桶中的令牌不足，且资源组未指定 `BURSTABLE` 选项，请求将等待令牌桶补充令牌后重试。重试可能因超时而失败。

- TiKV 调度：你可以根据需要设置绝对优先级 [`PRIORITY`](/information-schema/information-schema-resource-groups.md#examples)。不同的资源根据 `PRIORITY` 设置进行调度。`PRIORITY` 高的任务优先调度。如果未设置绝对优先级，TiKV 会根据每个资源组的 `RU_PER_SEC` 值来确定读写请求的优先级。存储层会根据优先级使用优先级队列调度和处理请求。

从 v7.4.0 版本开始，资源控制功能支持控制 TiFlash 资源。其原理类似于 TiDB 流量控制和 TiKV 调度：

<CustomContent platform="tidb">

- TiFlash 流量控制：结合 [TiFlash pipeline 执行模型](/tiflash/tiflash-pipeline-model.md)，TiFlash 能更准确地获取不同查询的 CPU 消耗，并将其转换为用于扣减的 [Request Units (RU)](#what-is-request-unit-ru)。流量控制采用 token bucket 算法实现。
- TiFlash 调度：当系统资源不足时，TiFlash 会根据优先级在多个资源组之间调度 pipeline 任务。具体逻辑为：首先评估资源组的 `PRIORITY`，然后考虑 CPU 使用情况和 `RU_PER_SEC`。例如，若 `rg1` 和 `rg2` 的 `PRIORITY` 相同，但 `rg2` 的 `RU_PER_SEC` 是 `rg1` 的两倍，则 `rg2` 的 CPU 使用率也会是 `rg1` 的两倍。

</CustomContent>

<CustomContent platform="tidb-cloud">

- TiFlash 流量控制：结合 [TiFlash pipeline 执行模型](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)，TiFlash 能更准确地获取不同查询的 CPU 消耗，并将其转换为用于扣减的 [Request Units (RU)](#what-is-request-unit-ru)。流量控制采用 token bucket 算法实现。
- TiFlash 调度：当系统资源不足时，TiFlash 会根据优先级在多个资源组之间调度 pipeline 任务。具体逻辑为：首先评估资源组的 `PRIORITY`，然后考虑 CPU 使用情况和 `RU_PER_SEC`。例如，若 `rg1` 和 `rg2` 的 `PRIORITY` 相同，但 `rg2` 的 `RU_PER_SEC` 是 `rg1` 的两倍，则 `rg2` 的 CPU 使用率也会是 `rg1` 的两倍。

</CustomContent>

关于如何管理后台任务和处理资源密集型查询（Runaway Queries），请参阅以下文档：

- [使用资源控制管理后台任务](/tidb-resource-control-background-tasks.md)
- [管理超出预期资源消耗的查询（Runaway Queries）](/tidb-resource-control-runaway-queries.md)

## 资源控制场景

引入资源控制功能是 TiDB 的一个里程碑。它可以将分布式数据库集群划分为多个逻辑单元。即使某个单元资源过度使用，也不会挤占其他单元所需的资源。

有了这个功能，你可以：

- 将来自不同系统的多个中小型应用合并到一个 TiDB 集群中。当某个应用的工作负载变大时，不会影响其他应用的正常运行。当系统负载较低时，即使超出配额，繁忙的应用仍能获得所需的系统资源，从而实现资源的最大利用。
- 选择将所有测试环境合并到一个 TiDB 集群，或将消耗较多资源的批处理任务分组到一个资源组中。这可以提高硬件利用率，降低运营成本，同时确保关键应用始终获得必要的资源。
- 当系统中存在混合负载时，可以将不同的负载放入不同的资源组。通过使用资源控制功能，可以确保事务型应用的响应时间不受数据分析或批处理应用的影响。
- 当集群遇到意外的 SQL 性能问题时，可以结合 SQL 绑定和资源组，临时限制某个 SQL 语句的资源消耗。

此外，合理使用资源控制功能还可以减少集群数量，简化运维难度，降低管理成本。

> **Note:**
>
> - 为评估资源管理的效果，建议在独立的计算和存储节点上部署集群。在通过 `tiup playground` 创建的部署中，调度和其他对集群资源敏感的功能难以正常工作，因为资源在实例间共享。

## 限制

资源控制会带来额外的调度开销。因此，启用该功能时，可能会出现轻微的性能下降（小于 5%）。

## 什么是 Request Unit (RU)

Request Unit (RU) 是 TiDB 中对系统资源的统一抽象单位，目前包括 CPU、IOPS 和 IO 带宽指标。它用于表示对数据库的单个请求所消耗的资源量。请求消耗的 RU 数量取决于多种因素，例如操作类型、查询或修改的数据量。目前，RU 包含以下表格中的资源消耗统计：

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
> - 每次写操作最终会复制到所有副本（默认 TiKV 有 3 个副本）。每次复制操作视为不同的写操作。
> - 上表仅列出 TiDB 自管理集群中 RU 计算涉及的资源，不包括网络和存储消耗。关于 {{{ .starter }}} 的 RU，请参见 [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)。
> - 目前，TiFlash 资源控制仅考虑 SQL CPU，即查询管道任务的 CPU 时间和读请求负载。

## 资源控制参数

资源控制功能引入了以下系统变量或参数：

* TiDB：可以使用 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) 系统变量控制是否启用资源组的流量控制。

<CustomContent platform="tidb">

* TiKV：可以使用 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 参数控制是否基于资源组配额进行请求调度。
* TiFlash：可以使用 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) 系统变量和 [`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) 配置项（在 v7.4.0 引入）控制是否启用 TiFlash 资源控制。

</CustomContent>

<CustomContent platform="tidb-cloud">

* TiKV：对于 TiDB 自管理，可以使用 `resource-control.enabled` 参数控制是否基于资源组配额进行请求调度。对于 TiDB Cloud，`resource-control.enabled` 参数的值默认为 `true`，不支持动态修改。
* TiFlash：对于 TiDB 自管理，可以使用 `tidb_enable_resource_control` 系统变量和 `enable_resource_control` 配置项（在 v7.4.0 引入）控制是否启用 TiFlash 资源控制。

</CustomContent>

从 TiDB v7.0.0 版本开始，`tidb_enable_resource_control` 和 `resource-control.enabled` 默认开启。这两个参数组合的结果如下表所示。

| `resource-control.enabled`  | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-------------------------------------|:-------------------------------------|
| `resource-control.enabled`= true  |  流量控制和调度（推荐） | 无效组合      |
| `resource-control.enabled`= false |  仅流量控制（不推荐）                 | 该功能已禁用 |

<CustomContent platform="tidb">

从 v7.4.0 版本开始，TiFlash 配置项 `enable_resource_control` 默认为开启。它与 `tidb_enable_resource_control` 一起控制 TiFlash 资源控制功能。只有当 `enable_resource_control` 和 `tidb_enable_resource_control` 都启用时，TiFlash 才会执行流量控制和优先级调度。此外，启用 `enable_resource_control` 后，TiFlash 使用 [Pipeline 执行模型](/tiflash/tiflash-pipeline-model.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

从 v7.4.0 版本开始，TiFlash 配置项 `enable_resource_control` 默认为开启。它与 `tidb_enable_resource_control` 一起控制 TiFlash 资源控制功能。只有当 `enable_resource_control` 和 `tidb_enable_resource_control` 都启用时，TiFlash 才会执行流量控制和优先级调度。此外，启用 `enable_resource_control` 后，TiFlash 使用 [Pipeline 执行模型](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)。

</CustomContent>

关于资源控制机制和参数的更多信息，请参见 [RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2022-11-25-global-resource-control.md) 和 [TiFlash Resource Control](https://github.com/pingcap/tiflash/blob/release-8.5/docs/design/2023-09-21-tiflash-resource-control.md)。

## 如何使用资源控制

本节介绍如何使用资源控制功能管理资源组以及控制各资源组的资源分配。

### 估算集群容量

<CustomContent platform="tidb">

在进行资源规划前，你需要了解集群的整体容量。TiDB 提供了 [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md) 语句，用于估算集群容量。你可以采用以下方法之一：

- [基于实际工作负载估算容量](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
- [基于硬件部署估算容量](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

你可以在 TiDB Dashboard 的 [Resource Manager 页面](/dashboard/dashboard-resource-manager.md) 查看。更多信息请参见 [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#methods-for-estimating-capacity)。

</CustomContent>

<CustomContent platform="tidb-cloud">

对于 TiDB 自管理，你可以使用 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/tidb/stable/sql-statement-calibrate-resource) 语句估算集群容量。

对于 TiDB Cloud，该语句不适用。

</CustomContent>

### 管理资源组

要创建、修改或删除资源组，你需要拥有 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 权限。

你可以使用 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 创建集群的资源组。

对于已存在的资源组，可以使用 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 修改其 `RU_PER_SEC`（每秒的 RU 补充速率）选项。对资源组的更改会立即生效。

你也可以使用 [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) 删除资源组。

### 创建资源组

以下是创建资源组的示例。

1. 创建资源组 `rg1`，资源限制为每秒 500 RU，允许应用在该资源组中超出资源限制。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2. 创建资源组 `rg2`，RU 补充速率为每秒 600 RU，不允许应用超出资源限制。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3. 创建资源组 `rg3`，绝对优先级设置为 `HIGH`。目前支持 `LOW|MEDIUM|HIGH`，默认值为 `MEDIUM`。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg3 RU_PER_SEC = 100 PRIORITY = HIGH;
    ```

### 绑定资源组

TiDB 支持以下三个层级的资源组设置。

- 用户层。通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user) 语句，将用户绑定到特定资源组。用户绑定后，用户创建的会话会自动绑定到对应的资源组。
- 会话层。通过 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 设置当前会话的资源组。
- 语句层。通过 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 优化器提示，为当前语句设置资源组。

#### 绑定用户到资源组

以下示例创建用户 `usr1`，并将其绑定到资源组 `rg1`。`rg1` 是在 [创建资源组](#create-a-resource-group) 中示例创建的资源组。

```sql
CREATE USER 'usr1'@'%' IDENTIFIED BY '123' RESOURCE GROUP rg1;
```

以下示例使用 `ALTER USER` 将用户 `usr2` 绑定到资源组 `rg2`。`rg2` 是在 [创建资源组](#create-a-resource-group) 中示例创建的资源组。

```sql
ALTER USER usr2 RESOURCE GROUP rg2;
```

绑定用户后，新创建会话的资源消耗将由指定的配额（Request Unit，RU）控制。如果系统负载较高且没有剩余容量，`usr2` 的资源消耗速率将受到严格限制，不得超过配额。由于 `usr1` 绑定在配置了 `BURSTABLE` 的 `rg1` 上，`usr1` 的消耗速率允许超出配额。

如果请求过多导致资源组资源不足，客户端请求将等待。如果等待时间过长，请求会报错。

> **Note:**
>
> - 使用 `CREATE USER` 或 `ALTER USER` 将用户绑定到资源组后，不会影响用户已有的会话，只对新会话生效。
> - TiDB 在集群初始化时会自动创建一个 `default` 资源组。该资源组的 `RU_PER_SEC` 默认值为 `UNLIMITED`（等于 `INT` 类型的最大值，即 `2147483647`），且处于 `BURSTABLE` 模式。未绑定资源组的语句会自动绑定到此资源组。该资源组不支持删除，但可以修改其 RU 配额。
>
> 要取消用户与资源组的绑定，可以将其重新绑定到 `default` 组，如下所示：

```sql
ALTER USER 'usr3'@'%' RESOURCE GROUP `default`;
```

有关详细信息，请参见 [`ALTER USER ... RESOURCE GROUP`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)。

#### 将当前会话绑定到资源组

你可以使用 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 语句，改变当前会话绑定的资源组。通过绑定会话到资源组，限制该会话的资源使用（RU）。

当系统变量 [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) 设置为 `ON` 时，执行此语句需要拥有 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 或 `RESOURCE_GROUP_USER` 权限。

以下示例将当前会话绑定到资源组 `rg1`。

```sql
SET RESOURCE GROUP rg1;
```

#### 将当前语句绑定到资源组

通过在 SQL 语句中添加 [`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name) 提示，可以指定该语句绑定的资源组。此提示支持 `SELECT`、`INSERT`、`UPDATE` 和 `DELETE` 语句。

当系统变量 [`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) 设置为 `ON` 时，使用此提示需要拥有 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 或 `RESOURCE_GROUP_USER` 权限。

以下示例将当前语句绑定到资源组 `rg1`。

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

## 禁用资源控制

<CustomContent platform="tidb">

1. 执行以下语句禁用资源控制功能。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. 将 TiKV 参数 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 设置为 `false`，以禁用基于资源组 RU 的调度。

3. 将 TiFlash 配置项 [`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) 设置为 `false`，以禁用 TiFlash 资源控制。

</CustomContent>

<CustomContent platform="tidb-cloud">

1. 执行以下语句禁用资源控制功能。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. 对于 TiDB 自管理，可以使用 `resource-control.enabled` 参数控制是否基于资源组配额进行请求调度。对于 TiDB Cloud，`resource-control.enabled` 参数的值默认为 `true`，不支持动态修改。如需在 TiDB Cloud Dedicated 集群中禁用此功能，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

3. 对于 TiDB 自管理，可以使用 `enable_resource_control` 配置项控制是否启用 TiFlash 资源控制。对于 TiDB Cloud，`enable_resource_control` 参数的值默认为 `true`，不支持动态修改。如需在 TiDB Cloud Dedicated 集群中禁用此功能，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

## 查看 RU 消耗

你可以查看 RU 消耗信息。

### 查看 SQL 的 RU 消耗

你可以通过以下方式查看 SQL 语句的 RU 消耗：

- 系统变量 `tidb_last_query_info`
- `EXPLAIN ANALYZE`
- 慢查询及对应的系统表
- `statements_summary`

#### 通过查询系统变量 `tidb_last_query_info` 查看上次 SQL 执行的 RU

TiDB 提供了系统变量 [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)。该变量记录了上次执行的 DML 语句信息，包括该 SQL 执行的 RU。

示例：

1. 执行 `UPDATE` 语句：

    ```sql
    UPDATE sbtest.sbtest1 SET k = k + 1 WHERE id = 1;
    ```

    ```
    Query OK, 1 row affected (0.01 sec)
    Rows matched: 1  Changed: 1  Warnings: 0
    ```

2. 查询系统变量 `tidb_last_query_info` 查看上次执行语句的信息：

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

    结果中，`ru_consumption` 即为该 SQL 执行所消耗的 RU。

#### 通过 `EXPLAIN ANALYZE` 查看 SQL 执行的 RU

你可以使用 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption) 获取 SQL 执行过程中消耗的 RU 数量。注意，RU 数量受缓存（例如 [coprocessor cache](/coprocessor-cache.md)）影响。当多次执行相同 SQL 时，每次的 RU 消耗可能不同。RU 数值不代表每次执行的精确值，但可作为估算参考。

#### 慢查询及对应的系统表

<CustomContent platform="tidb">

启用资源控制后，TiDB 的 [慢查询日志](/identify-slow-queries.md) 和对应的系统表 [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 会包含资源组信息、对应 SQL 的 RU 消耗以及等待可用 RU 的时间。

</CustomContent>

<CustomContent platform="tidb-cloud">

启用资源控制后，系统表 [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 会包含资源组信息、对应 SQL 的 RU 消耗以及等待可用 RU 的时间。

</CustomContent>

#### 通过 `statements_summary` 查看 RU 统计信息

TiDB 的系统表 [`INFORMATION_SCHEMA.statements_summary`](/statement-summary-tables.md#statements_summary) 存储了 SQL 语句的归一化和聚合统计信息。你可以通过该表查看和分析 SQL 执行性能，还包含资源控制的统计信息，包括资源组名、RU 消耗和等待可用 RU 的时间。更多详情请参见 [`statements_summary` 字段说明](/statement-summary-tables.md#statements_summary-fields-description)。

### 查看资源组的 RU 消耗

从 v7.6.0 版本开始，TiDB 提供了系统表 [`mysql.request_unit_by_group`](/mysql-schema/mysql-schema.md#system-tables-related-to-resource-control)，用于存储各资源组的 RU 消耗历史记录。

示例：

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
> `mysql.request_unit_by_group` 的数据由 TiDB 每天结束时自动导入。如果某天某个资源组的 RU 消耗为 0，则不会生成记录。默认情况下，该表存储最近三个月（最多 92 天）的数据。超出此期限的数据会自动清除。

## 监控指标与图表

<CustomContent platform="tidb">

TiDB 定期收集资源控制的运行时信息，并在 Grafana 的 **TiDB** > **Resource Control** 仪表盘中提供指标的可视化图表。指标详见 [TiDB 重要监控指标](/grafana-tidb-dashboard.md) 中的 **Resource Control** 部分。

TiKV 也会记录来自不同资源组的请求 QPS。更多详情请参见 [TiKV 监控指标详情](/grafana-tikv-dashboard.md#grpc)。

你可以在 TiDB Dashboard 的 [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md) 表中查看当前的资源组数据。更多信息请参见 [Resource Manager 页面](/dashboard/dashboard-resource-manager.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 该部分仅适用于 TiDB 自管理。目前，TiDB Cloud 不提供资源控制指标。

TiDB 定期收集资源控制的运行时信息，并在 Grafana 的 **TiDB** > **Resource Control** 仪表盘中提供指标的可视化图表。

TiKV 也会在 Grafana 的 **TiKV** 仪表盘中记录来自不同资源组的请求 QPS。

</CustomContent>

## 工具兼容性

资源控制功能不会影响数据导入、导出及其他复制工具的正常使用。BR、TiDB Lightning 和 TiCDC 目前不支持处理与资源控制相关的 DDL 操作，其资源消耗也不受资源控制限制。

## 常见问题

1. 如果我不想使用资源组，是否必须禁用资源控制？

    不需要。未指定资源组的用户会绑定到资源无限制的 `default` 资源组。当所有用户都属于 `default` 资源组时，资源分配方式与禁用资源控制时相同。

2. 数据库用户可以绑定多个资源组吗？

    不可以。一个数据库用户只能绑定到一个资源组。但在会话运行期间，可以使用 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 设置当前会话使用的资源组，也可以使用优化器提示 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 设置运行语句的资源组。

3. 如果所有资源组的总资源分配（`RU_PER_SEC`）超过系统容量，会发生什么？

    TiDB 在创建资源组时不会验证容量。只要系统有足够的可用资源，TiDB 就能满足每个资源组的资源需求。当系统资源超出限制时，TiDB 会优先满足高优先级资源组的请求。如果同一优先级的请求不能全部满足，TiDB 会根据 `RU_PER_SEC` 按比例分配资源。

## 另请参见

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2022-11-25-global-resource-control.md)
