---
title: 定期使用 TTL (Time to Live) 删除数据
summary: Time to live (TTL) 是一项允许你在行级别管理 TiDB 数据存活时间的功能。在本文档中，你可以了解如何使用 TTL 自动过期并删除旧数据。
---

# 使用 TTL (Time to Live) 定期删除过期数据

Time to live (TTL) 是一项允许你在行级别管理 TiDB 数据存活时间的功能。对于具有 TTL 属性的表，TiDB 会自动检查数据的存活时间，并在行级别删除过期数据。该功能在某些场景下可以有效节省存储空间并提升性能。

以下是一些常见的 TTL 使用场景：

* 定期删除验证码和短链接。
* 定期删除不再需要的历史订单。
* 自动删除计算的中间结果。

TTL 旨在帮助用户定期及时清理不必要的数据，而不会影响线上读写负载。TTL 会同时调度不同的任务到不同的 TiDB 节点，以并行方式在表的单位上删除数据。TTL 不保证所有过期数据会立即被删除，也就是说，即使某些数据已过期，客户端仍可能在过期时间之后一段时间内读取到这些数据，直到后台 TTL 任务将其删除。

## 语法

你可以使用 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 或 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) 语句配置表的 TTL 属性。

### 创建带有 TTL 属性的表

- 创建带有 TTL 属性的表：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

    上述示例创建了表 `t1`，并指定 `created_at` 作为 TTL 时间戳列，表示数据的创建时间。示例还通过 `INTERVAL 3 MONTH` 设置了该行在表中的最长存活时间为 3 个月。超过此时间的数据将会在之后被删除。

- 设置 `TTL_ENABLE` 属性以启用或禁用过期数据清理功能：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
    ```

    如果将 `TTL_ENABLE` 设置为 `OFF`，即使其他 TTL 选项已设置，TiDB 也不会自动清理该表中的过期数据。具有 TTL 属性的表，`TTL_ENABLE` 默认为 `ON`。

- 为了兼容 MySQL，可以使用注释设置 TTL 属性：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
    ```

    在 TiDB 中，使用表的 TTL 属性或通过注释配置 TTL 是等价的。在 MySQL 中，注释会被忽略，创建的是普通表。

### 修改表的 TTL 属性

- 修改表的 TTL 属性：

    ```sql
    ALTER TABLE t1 TTL = `created_at` + INTERVAL 1 MONTH;
    ```

    你可以使用上述语句修改已有 TTL 属性的表，或为没有 TTL 属性的表添加 TTL。

- 修改具有 TTL 属性的表的 `TTL_ENABLE` 值：

    ```sql
    ALTER TABLE t1 TTL_ENABLE = 'OFF';
    ```

- 移除表的所有 TTL 属性：

    ```sql
    ALTER TABLE t1 REMOVE TTL;
    ```

### TTL 与数据类型的默认值

你可以将 TTL 与 [数据类型的默认值](/data-type-default-values.md) 一起使用。以下是两个常见的用法示例：

* 使用 `DEFAULT CURRENT_TIMESTAMP` 指定列的默认值为当前创建时间，并将此列作为 TTL 时间戳列。创建 3 个月前的数据即为过期：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

* 将列的默认值指定为创建时间或最新更新时间，并将此列作为 TTL 时间戳列。未在 3 个月内更新的记录即为过期：

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

### TTL 与生成列

你可以将 TTL 与 [生成列](/generated-columns.md) 结合使用，以配置复杂的过期规则。例如：

```sql
CREATE TABLE message (
    id int PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image bool,
    expire_at TIMESTAMP AS (IF(image,
            created_at + INTERVAL 5 DAY,
            created_at + INTERVAL 30 DAY
    ))
) TTL = `expire_at` + INTERVAL 0 DAY;
```

上述语句将 `expire_at` 列作为 TTL 时间戳列，根据消息类型设置过期时间。如果是图片类型，过期时间为 5 天；否则为 30 天。

你也可以将 TTL 与 [JSON 类型](/data-type-json.md) 结合使用。例如：

```sql
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_info JSON,
    created_at DATE AS (JSON_EXTRACT(order_info, '$.created_at')) VIRTUAL
) TTL = `created_at` + INTERVAL 3 month;
```

## TTL 任务

对于每个具有 TTL 属性的表，TiDB 内部会调度后台任务以清理过期数据。你可以通过设置表的 `TTL_JOB_INTERVAL` 属性来自定义这些任务的执行周期。以下示例将表 `orders` 的后台清理任务设置为每 24 小时运行一次：

```sql
ALTER TABLE orders TTL_JOB_INTERVAL = '24h';
```

`TTL_JOB_INTERVAL` 默认为 `1h`。

在执行 TTL 任务时，TiDB 会将表拆分成最多 64 个任务，Region 是最小单位。这些任务会分布式执行。你可以通过设置系统变量 [`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700) 来限制整个集群中 TTL 任务的并发数。不过，并非所有类型的表的 TTL 任务都能拆分成任务。关于哪些类型的表的 TTL 任务不能拆分成任务的详细信息，请参考 [Limitations](#limitations) 部分。

要禁用 TTL 任务的执行，除了设置 `TTL_ENABLE='OFF'` 表选项外，还可以通过设置全局变量 [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650) 来禁用整个集群中的 TTL 任务：

```sql
SET @@global.tidb_ttl_job_enable = OFF;
```

在某些场景下，你可能希望 TTL 任务只在特定时间窗口内运行。这时可以设置 [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650) 和 [`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650) 全局变量，指定时间窗口。例如：

```sql
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

上述语句允许 TTL 任务仅在 UTC 时间 01:00 到 05:00 之间调度。默认时间窗口为 `00:00 +0000` 到 `23:59 +0000`，允许在任何时间调度。

## 可观察性

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 本节仅适用于 TiDB 自托管版本。目前，TiDB Cloud 不提供 TTL 指标。

</CustomContent>

TiDB 会定期收集 TTL 的运行时信息，并在 Grafana 中提供这些指标的可视化图表。你可以在 Grafana 的 TiDB -> TTL 面板中查看这些指标。

<CustomContent platform="tidb">

有关指标的详细信息，请参见 [TiDB 监控指标](/grafana-tidb-dashboard.md) 中的 TTL 部分。

</CustomContent>

此外，TiDB 提供了三个表，用于获取关于 TTL 任务的更多信息：

+ `mysql.tidb_ttl_table_status` 表包含所有 TTL 表的上一次执行 TTL 任务和正在进行的 TTL 任务的信息

    ```sql
    TABLE mysql.tidb_ttl_table_status LIMIT 1\G
    ```

    ```
    *************************** 1. row ***************************
                          table_id: 85
                   parent_table_id: 85
                  table_statistics: NULL
                       last_job_id: 0b4a6d50-3041-4664-9516-5525ee6d9f90
               last_job_start_time: 2023-02-15 20:43:46
              last_job_finish_time: 2023-02-15 20:44:46
               last_job_ttl_expire: 2023-02-15 19:43:46
                  last_job_summary: {"total_rows":4369519,"success_rows":4369519,"error_rows":0,"total_scan_task":64,"scheduled_scan_task":64,"finished_scan_task":64}
                    current_job_id: NULL
              current_job_owner_id: NULL
            current_job_owner_addr: NULL
         current_job_owner_hb_time: NULL
            current_job_start_time: NULL
            current_job_ttl_expire: NULL
                 current_job_state: NULL
                current_job_status: NULL
    current_job_status_update_time: NULL
    ```

    其中 `table_id` 为分区表的 ID，`parent_table_id` 为表的 ID，和 [`information_schema.tables`](/information-schema/information-schema-tables.md) 中的 ID 一致。如果不是分区表，这两个 ID 相同。

    `{last, current}_job_{start_time, finish_time, ttl_expire}` 分别描述上次或本次 TTL 执行的开始时间、结束时间和过期时间。`last_job_summary` 描述上次 TTL 任务的执行状态，包括总行数、成功行数和失败行数。

+ `mysql.tidb_ttl_task` 表包含正在执行的 TTL 子任务信息。一个 TTL 任务会拆分成多个子任务，该表记录当前正在执行的子任务。

+ `mysql.tidb_ttl_job_history` 表包含已执行 TTL 任务的信息。TTL 任务的历史记录会保存 90 天。

    ```sql
    TABLE mysql.tidb_ttl_job_history LIMIT 1\G
    ```

    ```
    *************************** 1. row ***************************
               job_id: f221620c-ab84-4a28-9d24-b47ca2b5a301
             table_id: 85
      parent_table_id: 85
         table_schema: test_schema
           table_name: TestTable
       partition_name: NULL
          create_time: 2023-02-15 17:43:46
          finish_time: 2023-02-15 17:45:46
           ttl_expire: 2023-02-15 16:43:46
         summary_text: {"total_rows":9588419,"success_rows":9588419,"error_rows":0,"total_scan_task":63,"scheduled_scan_task":63,"finished_scan_task":63}
         expired_rows: 9588419
         deleted_rows: 9588419
    error_delete_rows: 0
               status: finished
    ```

    其中 `table_id` 为分区表的 ID，`parent_table_id` 为表的 ID，和 [`information_schema.tables`](/information-schema/information-schema-tables.md) 中的 ID 一致。`table_schema`、`table_name` 和 `partition_name` 分别对应数据库、表名和分区名。`create_time`、`finish_time` 和 `ttl_expire` 表示 TTL 任务的创建时间、结束时间和过期时间。`expired_rows` 和 `deleted_rows` 表示过期行数和成功删除的行数。

## 与 TiDB 工具的兼容性

TTL 可以与其他 TiDB 迁移、备份和恢复工具配合使用。

| 工具名称 | 支持的最低版本 | 说明 |
| --- | --- | --- |
| Backup & Restore (BR) | v6.6.0 | 使用 BR 还原数据后，表的 `TTL_ENABLE` 属性会被设置为 `OFF`。这会阻止 TiDB 在备份和还原后立即删除过期数据。你需要手动开启 `TTL_ENABLE` 属性以重新启用每个表的 TTL。 |
| TiDB Lightning | v6.6.0 | 使用 TiDB Lightning 导入数据后，导入表的 `TTL_ENABLE` 属性会被设置为 `OFF`。这会阻止 TiDB 在导入后立即删除过期数据。你需要手动开启 `TTL_ENABLE` 属性以重新启用每个表的 TTL。 |
| TiCDC | v7.0.0 | 下游的 `TTL_ENABLE` 属性会被自动设置为 `OFF`。上游的 TTL 删除操作会同步到下游。因此，为避免重复删除，下游表的 `TTL_ENABLE` 属性会被强制设置为 `OFF`。 |

## 与 SQL 的兼容性

| 功能名称 | 说明 |
| :-- | :-- |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md) | `FLASHBACK TABLE` 会将表的 `TTL_ENABLE` 属性设置为 `OFF`。这会阻止 TiDB 在闪回后立即删除过期数据。你需要手动开启 `TTL_ENABLE` 属性以重新启用每个表的 TTL。 |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) | `FLASHBACK DATABASE` 会将表的 `TTL_ENABLE` 属性设置为 `OFF`，但不会修改 `TTL_ENABLE` 属性。这会阻止 TiDB 在闪回后立即删除过期数据。你需要手动开启 `TTL_ENABLE` 属性以重新启用每个表的 TTL。 |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) | `FLASHBACK CLUSTER` 会将系统变量 [`TIDB_TTL_JOB_ENABLE`](/system-variables.md#tidb_ttl_job_enable-new-in-v650) 设置为 `OFF`，但不会更改 `TTL_ENABLE` 属性的值。 |

## 限制

目前，TTL 功能存在以下限制：

* 不能在临时表（包括本地临时表和全局临时表）上设置 TTL 属性。
* 具有 TTL 属性的表不支持被其他表作为外键约束中的主表引用。
* 并不保证所有过期数据会立即被删除。过期数据的删除时间取决于后台清理任务的调度间隔和调度窗口。
* 对于使用 [聚簇索引](/clustered-indexes.md) 的表，TTL 任务只能在以下场景拆分成多个子任务：
    - 主键或复合主键的第一个列为 `INTEGER` 或二进制字符串类型。二进制字符串类型主要包括：
        - `CHAR(N) CHARACTER SET BINARY`
        - `VARCHAR(N) CHARACTER SET BINARY`
        - `BINARY(N)`
        - `VARBINARY(N)`
        - `BIT(N)`
    - 主键或复合主键的第一个列的字符集为 `utf8` 或 `utf8mb4`，排序规则为 `utf8_bin`、`utf8mb4_bin` 或 `utf8mb4_0900_bin`。
    - 对于字符集类型为 `utf8` 或 `utf8mb4` 的表，子任务仅基于可见 ASCII 字符范围拆分。如果许多主键值具有相同的 ASCII 前缀，可能会导致任务拆分不均。
    - 对于不支持将 TTL 任务拆分成多个子任务的表，TTL 任务会在单个 TiDB 节点上顺序执行。如果表中数据量很大，TTL 任务的执行可能变慢。

## 常见问题

<CustomContent platform="tidb">

- 如何判断删除速度是否足够快以保持数据规模相对稳定？

    在 [Grafana `TiDB` 仪表盘](/grafana-tidb-dashboard.md)，`TTL Insert Rows Per Hour` 面板记录了上一小时插入的总行数。对应的 `TTL Delete Rows Per Hour` 记录了上一小时 TTL 任务删除的总行数。如果 `TTL Insert Rows Per Hour` 长期高于 `TTL Delete Rows Per Hour`，意味着插入速率高于删除速率，数据总量会增加。例如：

    ![insert fast example](/media/ttl/insert-fast.png)

    需要注意的是，由于 TTL 不保证过期行会立即被删除，当前插入的行会在未来的 TTL 任务中被删除，即使 TTL 删除速度短时间内低于插入速度，也不一定意味着 TTL 速度过慢。你需要结合实际情况判断。

- 如何判断 TTL 任务的瓶颈在扫描还是删除？

    查看 `TTL Scan Worker Time By Phase` 和 `TTL Delete Worker Time By Phase` 面板。如果扫描工人在 `dispatch` 阶段占用大量时间，而删除工人很少处于 `idle` 阶段，说明扫描工人在等待删除工人完成删除。如果此时集群资源仍然空闲，可以考虑增加 [`tidb_ttl_delete_worker_count`] 来增加删除工人数量。例如：

    ![scan fast example](/media/ttl/scan-fast.png)

    相反，如果扫描工人很少在 `dispatch` 阶段，而删除工人在 `idle` 阶段停留较长时间，说明扫描工人相对繁忙。例如：

    ![delete fast example](/media/ttl/delete-fast.png)

    TTL 任务中的扫描和删除比例与机器配置和数据分布有关，因此每个时刻的监控数据仅代表当前正在执行的 TTL 任务。你可以通过读取表 `mysql.tidb_ttl_job_history` 来判断某一时刻正在运行的 TTL 任务及其对应的表。

- 如何合理配置 `tidb_ttl_scan_worker_count` 和 `tidb_ttl_delete_worker_count`？

    1. 参考“如何判断 TTL 任务的瓶颈在扫描还是删除？”的问题，考虑是否需要增加 `tidb_ttl_scan_worker_count` 或 `tidb_ttl_delete_worker_count` 的值。
    2. 如果 TiKV 节点较多，增加 `tidb_ttl_scan_worker_count` 的值可以使 TTL 任务的工作负载更均衡。

    由于 TTL 工作者过多会带来较大压力，你需要结合 TiDB 的 CPU 水平以及 TiKV 的磁盘和 CPU 使用情况进行评估。根据不同场景和需求（是否需要尽快加快 TTL，或减少 TTL 对其他查询的影响），可以调整 `tidb_ttl_scan_worker_count` 和 `tidb_ttl_delete_worker_count` 的值，以提升 TTL 的扫描和删除速度，或减小 TTL 任务带来的性能影响。

</CustomContent>
<CustomContent platform="tidb-cloud">

- 如何合理配置 `tidb_ttl_scan_worker_count` 和 `tidb_ttl_delete_worker_count`？

   如果 TiKV 节点较多，增加 `tidb_ttl_scan_worker_count` 的值可以使 TTL 任务的工作负载更均衡。

   但过多的 TTL 工作者会带来较大压力，你需要结合 TiDB 的 CPU 水平以及 TiKV 的磁盘和 CPU 使用情况进行评估。根据不同场景和需求（是否需要尽快加快 TTL，或减少 TTL 对其他查询的影响），可以调整 `tidb_ttl_scan_worker_count` 和 `tidb_ttl_delete_worker_count` 的值，以提升 TTL 的扫描和删除速度，或减小 TTL 任务带来的性能影响。

</CustomContent>