---
title: 分层存储可观测性
summary: 了解如何在 TiDB Cloud Premium 或 BYOC 中监控分层存储，包括转换进度、IA 读取指标和缓存性能面板。
---

# 分层存储可观测性

本文介绍如何监控低频访问（Infrequent Access，IA）存储，包括存储类别转换进度、SQL 级别的 IA 读取指标，以及集群级别的 IA 缓存性能。

> **注意：**
>
> 分层存储目前在 {{{ .premium }}} 和 {{{ .byoc }}} 中处于**私有预览**阶段，且默认禁用。如需使用，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 为你的实例启用。本文描述的行为反映的是当前预览版的实现，可能会在正式发布（GA）前发生变化。

## 监控存储类别转换 {#monitor-storage-class-transitions}

本节介绍如何跟踪存储类别转换的进度，以及如何查看历史转换记录。

无论你使用哪种方式修改存储类别，转换进度的跟踪方式都相同：

- `STORAGE_CLASS` 语法糖，例如 `ALTER TABLE t1 STORAGE_CLASS='IA'`
- `ENGINE_ATTRIBUTE` 形式，例如 `ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"IA"}'`
- 使用 `ENGINE_ATTRIBUTE` 进行的分区级修改

分区表仅支持 `ENGINE_ATTRIBUTE`，因此分区转换会与表级转换一起显示在相同的视图中。直接创建为 IA 存储类别的表或分区没有数据需要迁移，因此不会出现在这些视图中。

`ALTER TABLE` 语句本身会在几秒内修改 schema 元信息。随后，Region 级别的数据迁移会在 TiKV 中异步运行，并且与 DDL 生命周期解耦，因此 `ADMIN SHOW DDL JOBS` 不会报告其进度。请使用 `SHOW STORAGE_CLASS TRANSITIONS` 跟踪正在进行中的转换，并查询 `mysql.tidb_storage_class_transition_history` 查看历史和当前转换。当转换开始时，会向历史表插入一条记录，`state = 'RUNNING'`；当转换进入最终状态时，该记录会被原地更新。

### 查看进行中的转换 {#view-in-progress-transitions}

```sql
SHOW STORAGE_CLASS TRANSITIONS;
SHOW STORAGE_CLASS TRANSITIONS LIKE 'table_name';
SHOW STORAGE_CLASS TRANSITIONS WHERE DIRECTION = 'TO_STANDARD';
```

`SHOW STORAGE_CLASS TRANSITIONS` 等价于 `SELECT * FROM INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS`。

`INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` 表列出了当前正在进行中的转换。它没有状态列，因为其中每一行都表示一个进行中的转换。该表包含以下列：

| 列 | 类型 | 描述 |
|-|-|-|
| `TABLE_SCHEMA` | VARCHAR(64) | 数据库名称 |
| `TABLE_NAME` | VARCHAR(64) | 表名称 |
| `TABLE_ID` | BIGINT(21) | 表的内部 ID |
| `PARTITION_NAME` | VARCHAR(64) | 分区名称。对于表级转换，该值为 `NULL` |
| `PARTITION_ID` | BIGINT(21) | 分区的内部 ID。对于表级转换，该值为 `NULL` |
| `DIRECTION` | VARCHAR(16) | 转换方向：`TO_IA` 或 `TO_STANDARD` |
| `TOTAL_REPLICAS` | BIGINT(21) UNSIGNED | 参与转换的副本总数。在首次成功观测之前，该值为 `NULL` |
| `COMPLETED_REPLICAS` | BIGINT(21) UNSIGNED | 已就绪的副本数。在首次成功观测之前，该值为 `NULL` |
| `PROGRESS` | DOUBLE | `COMPLETED_REPLICAS` 与 `TOTAL_REPLICAS` 的比值，范围为 `0` 到 `1`。乘以 100 可得到百分比。只有当某次观测报告了有效的进度比值后，该值才不是 `NULL`；这可能晚于首次填充 `TOTAL_REPLICAS` 和 `COMPLETED_REPLICAS` 的观测 |
| `START_TIME` | DATETIME(6) | 转换开始时间，使用会话时区 |
| `DURATION` | BIGINT(21) UNSIGNED | 从转换开始到当前的已耗时秒数 |
| `LAST_UPDATE_TIME` | DATETIME(6) | 最近一次成功观测到进度的时间 |

> **注意：**
>
> - 只有当你对该表拥有 `ALL` 权限时，对应行才可见。对于你无权访问的表，其对应行会被跳过，不会报错，也不会给出警告。
> - 进度每 10 秒采集一次，因此这些值不是实时的。

要检查某个特定转换的进度和已耗时长：

```sql
SELECT TABLE_NAME, DIRECTION, COMPLETED_REPLICAS, TOTAL_REPLICAS,
       ROUND(PROGRESS * 100, 1) AS PROGRESS_PCT,
       DURATION, LAST_UPDATE_TIME
FROM INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS
WHERE TABLE_SCHEMA = 'db_name' AND TABLE_NAME = 'table_name';
```

一个转换会经历一个进行中状态，并最终进入两个终态之一。每种状态也都会记录在 `mysql.tidb_storage_class_transition_history` 中：

| 状态 | 记录位置 | 描述 |
|-|-|-|
| `RUNNING` | `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` 和 `mysql.tidb_storage_class_transition_history` 的 `state` 列 | Region 级转换正在进行中。`INFORMATION_SCHEMA` 表只列出这类转换，因此没有状态列。当转换处于 `RUNNING` 时，其历史记录中的 `finish_time`、`duration`、`total_replicas` 和 `completed_replicas` 都为 `NULL`。可使用 `PROGRESS`、`COMPLETED_REPLICAS` 和 `TOTAL_REPLICAS` 跟踪进度，使用 `DURATION` 跟踪已耗时长 |
| `COMPLETED` | `mysql.tidb_storage_class_transition_history` 的 `state` 列 | 所有副本均已就绪。该转换会从 `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` 中移除，其历史记录会更新为 `COMPLETED` |
| `SUPERSEDED` | `mysql.tidb_storage_class_transition_history` 的 `state` 列 | 在转换完成前发起了反向转换，因此该转换被作废。其历史记录会更新为 `SUPERSEDED` |

### 判断转换是否卡住 {#determine-whether-a-conversion-is-stuck}

结合观察 `LAST_UPDATE_TIME`、`COMPLETED_REPLICAS` 和 `DURATION`：

- `COMPLETED_REPLICAS` 持续增加，且 `LAST_UPDATE_TIME` 不断推进：说明转换正在正常进行，只是数据量较大。
- `DURATION` 持续增长，但 `COMPLETED_REPLICAS` 长时间没有增加：说明转换可能因系统异常而卡住，例如 TiKV 滚动重启、资源暂时不足，或对象存储短时不可用。
- `TOTAL_REPLICAS`、`COMPLETED_REPLICAS`、`PROGRESS` 和 `LAST_UPDATE_TIME` 始终为 `NULL`：说明尚未成功完成任何一次观测。这些列会一起被填充和清空，因此 `LAST_UPDATE_TIME` 无法判断是否仍在尝试观测。此时应检查 `DURATION`：只要转换仍在被跟踪，它就会持续增加。如果这些列一直为 `NULL`，但 `DURATION` 持续增长，说明轮询仍在运行，只是尚未返回有效观测结果。

你无法自行处理卡住的转换。请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 获取帮助。问题解决后，`COMPLETED_REPLICAS` 会继续增加，直到转换达到 `COMPLETED`，你无需执行额外操作。

### 反转仍在进行中的转换 {#reverse-a-conversion-that-is-still-in-progress}

如果某个表或分区的前一次转换仍在进行中，而你又发起了反向转换，则前一次转换会被作废：

- 在 `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` 中，该表或分区对应的行会被新的转换替换。`DIRECTION` 显示新的方向，`START_TIME` 为新转换的开始时间，进度也会从头重新计算。该表或分区最终只保留一行记录。
- 在 `mysql.tidb_storage_class_transition_history` 中，被作废转换的历史记录会更新为 `state = 'SUPERSEDED'`。其 `finish_time` 为新转换的开始时间，`total_replicas` 和 `completed_replicas` 为其被作废前最后一次观测到的值。如果此前尚无任何观测，这两列都为 `NULL`。

要了解被作废转换在作废前推进到了什么程度，可查询历史表中 `state = 'SUPERSEDED'` 的记录。

### 查询转换历史 {#query-transition-history}

每次转换开始时，都会在 `mysql.tidb_storage_class_transition_history` 表中记录一条记录，并在转换推进过程中持续更新。该表包含以下列：

| 列 | 类型 | 描述 |
|-|-|-|
| `table_schema` | VARCHAR(64) | 数据库名称 |
| `table_name` | VARCHAR(64) | 表名称 |
| `table_id` | BIGINT | 表的内部 ID。它与 `start_ts` 和 `direction` 一起构成该表的主键 |
| `partition_name` | VARCHAR(64) | 分区名称。对于表级转换，该值为 `NULL` |
| `partition_id` | BIGINT | 分区的内部 ID。对于表级转换，该值为 `NULL` |
| `direction` | VARCHAR(16) | 转换方向：`TO_IA` 或 `TO_STANDARD` |
| `state` | VARCHAR(16) | 转换状态：`RUNNING`、`COMPLETED` 或 `SUPERSEDED` |
| `total_replicas` | BIGINT UNSIGNED | 参与转换的副本总数。对于 `SUPERSEDED` 记录，这是转换被作废前最后一次观测到的值；如果没有任何观测，则为 `NULL`。当转换处于 `RUNNING` 时，该值为 `NULL` |
| `completed_replicas` | BIGINT UNSIGNED | 已就绪的副本数。对于 `COMPLETED` 记录，该值等于 `total_replicas`。对于 `SUPERSEDED` 记录，这是转换被作废前最后一次观测到的值；如果没有任何观测，则为 `NULL`。当转换处于 `RUNNING` 时，该值为 `NULL` |
| `schema_version` | BIGINT | 该转换所属的 TiDB schema 版本 |
| `start_ts` | BIGINT UNSIGNED | 转换开始时的 TSO。它与 `table_id` 和 `direction` 一起标识该转换 |
| `start_time` | DATETIME(6) | 转换开始时间 |
| `finish_time` | DATETIME(6) | 转换进入最终状态的时间。对于 `COMPLETED` 记录，这是所有副本都已就绪的时间。对于 `SUPERSEDED` 记录，这是新转换的开始时间。在转换进入最终状态之前，该值为 `NULL` |
| `duration` | BIGINT UNSIGNED | 总耗时（秒）。对于 `SUPERSEDED` 记录，该值仅覆盖从开始到被作废的时间，而不是一次完整转换的总时长。当转换仍处于 `RUNNING` 时，该值为 `NULL` |

你可以使用该表估算在自己集群上类似转换所需的时间，这比参考测试环境中的任何数据都更可靠：

```sql
-- Average duration of completed conversions, grouped by direction.
-- Filter on state = 'COMPLETED': the duration of a SUPERSEDED record
-- does not represent a full conversion.
SELECT direction,
       COUNT(*) AS total_conversions,
       ROUND(AVG(duration), 0) AS avg_duration_sec,
       MIN(duration) AS min_duration_sec,
       MAX(duration) AS max_duration_sec
FROM mysql.tidb_storage_class_transition_history
WHERE state = 'COMPLETED'
GROUP BY direction;

-- The most recent finished conversion of a specific table
SELECT table_name, direction, state, duration AS total_duration_sec,
       total_replicas, completed_replicas, start_time, finish_time
FROM mysql.tidb_storage_class_transition_history
WHERE table_schema = 'db_name' AND table_name = 'table_name'
    AND state <> 'RUNNING'
ORDER BY finish_time DESC
LIMIT 1;

-- Conversions that were voided by a reverse conversion
SELECT table_schema, table_name, partition_name, direction,
       completed_replicas, total_replicas, start_time, finish_time, duration
FROM mysql.tidb_storage_class_transition_history
WHERE state = 'SUPERSEDED'
ORDER BY finish_time DESC;
```

#### 历史记录保留策略 {#retention-of-history-records}

`mysql.tidb_storage_class_transition_history` 中保留的最大记录数由系统变量 [`tidb_storage_class_transition_history_size`](#tidb_storage_class_transition_history_size) 控制。当记录数超过该限制时，会优先删除最旧的记录，排序依据为 `finish_time`。保留策略最多每分钟执行一次，因此行数可能会暂时超过该限制。

```sql
-- View the current retention limit
SELECT @@tidb_storage_class_transition_history_size;

-- Retain up to 500 records
SET GLOBAL tidb_storage_class_transition_history_size = 500;
```

#### tidb_storage_class_transition_history_size {#tidb-storage-class-transition-history-size}

- 作用域：GLOBAL
- 持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：Integer
- 默认值：`1000`
- 范围：`[100, 100000]`
- 该变量用于设置 `mysql.tidb_storage_class_transition_history` 表中保留的存储类别转换记录的最大数量。值越大，历史记录保留时间越长，同时也会占用 `mysql` 数据库中更多空间。

## 在 SQL 级别监控 IA 读取 {#monitor-ia-reads-at-the-sql-level}

本节介绍 `EXPLAIN ANALYZE`、语句摘要表、慢查询日志以及 TiDB Cloud 控制台中可用的 IA 指标。

### EXPLAIN ANALYZE {#explain-analyze}

当查询涉及远程数据加载时，`scan_detail` 会包含以下字段：

```sql
EXPLAIN ANALYZE SELECT * FROM t_ia WHERE id BETWEEN 1 AND 50000;
-- The output includes:
-- ia_remote_read_segment_size: 2320453     -- Total bytes loaded remotely
-- ia_remote_read_segment_count: 3           -- Number of remote loading events
-- ia_remote_read_segment_wait_time: 0.008   -- Remote wait time (seconds)
```

> **注意：**
>
> IA 信号是按请求维度反映读路径证据的，并不是表级别的稳定标记——同一条查询第一次执行时可能显示 IA 信息，但在缓存命中后再次执行时可能就不再显示。
>
> 此外，`ia_remote_read_segment_wait_time` 是所有远程请求耗时的聚合值。由于 TiKV 底层采用并行读取机制，该值可能会超过 SQL 的实际执行时间。

### 语句摘要 {#statement-summary}

`STATEMENTS_SUMMARY`、`STATEMENTS_SUMMARY_HISTORY` 及其对应的 `CLUSTER_` 表包含以下 IA 列：

| 列 | 描述 |
|-|-|
| `IA_EXEC_COUNT` | 至少触发过一次 IA 远程读取的执行次数。将其与 `EXEC_COUNT` 对比，可以得到访问 IA 数据的执行占比。例如，`IA_EXEC_COUNT = 2` 且 `EXEC_COUNT = 1000` 表示只有 0.2% 的执行访问了 IA 数据 |
| `AVG_IA_REMOTE_READ_SEGMENT_COUNT` | 每次执行平均读取的远程 segment 数量 |
| `MAX_IA_REMOTE_READ_SEGMENT_COUNT` | 单次执行中读取的最大远程 segment 数量 |
| `AVG_IA_REMOTE_READ_SEGMENT_SIZE` | 每次执行的平均远程读取数据量 |
| `MAX_IA_REMOTE_READ_SEGMENT_SIZE` | 单次执行中的最大远程读取数据量 |
| `AVG_IA_REMOTE_READ_SEGMENT_WAIT_TIME` | 每次执行的平均远程等待时间 |
| `MAX_IA_REMOTE_READ_SEGMENT_WAIT_TIME` | 单次执行中的最大远程等待时间 |

`AVG_` 和 `MAX_` 列用于回答每次执行远程读取了多少数据，而 `IA_EXEC_COUNT` 用于回答到底有多少次执行发生了远程读取。应结合这两个维度一起分析：如果某条语句的 `AVG_IA_REMOTE_READ_SEGMENT_SIZE` 很小，但 `IA_EXEC_COUNT / EXEC_COUNT` 比例很高，说明它频繁地以小数据量访问冷数据。

对于不涉及 IA 表的查询，这些列的值为 `0` 或 `NULL`。

要找出冷读执行占比最高的语句，请使用以下查询：

```sql
SELECT DIGEST_TEXT, EXEC_COUNT, IA_EXEC_COUNT,
       ROUND(IA_EXEC_COUNT / EXEC_COUNT * 100, 2) AS ia_exec_pct,
       AVG_IA_REMOTE_READ_SEGMENT_SIZE
FROM INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY_HISTORY
WHERE IA_EXEC_COUNT > 0
ORDER BY ia_exec_pct DESC
LIMIT 10;
```

### 慢查询 {#slow-queries}

`INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 包含以下 IA 列：

- `IA_remote_read_segment_count`
- `IA_remote_read_segment_size`
- `IA_remote_read_segment_wait_time`

在 `ADMIN SHOW SLOW` 的输出中也可以看到相同字段：

```sql
ADMIN SHOW SLOW RECENT 10;
ADMIN SHOW SLOW TOP INTERNAL 10;
ADMIN SHOW SLOW TOP ALL 10;
```

这些字段的语义和单位与 `SLOW_QUERY` 表中的相同。对于不涉及 IA 表的查询，这些值为 `NULL` 或 `0`。在 TiDB Cloud 控制台的慢查询详情中，也可以看到对应字段。

### 控制台中的 SQL 语句列表 {#sql-statement-list-in-the-console}

`IA_EXEC_COUNT` 列也会显示在 SQL 语句诊断列表中：

- **Cloud Console**：**Monitoring** > **Diagnosis** > **SQL Statement**
- **Clinic**：**Diagnosis** > **SQL Statements**

该列名为 **Exec Count of IA**，位于 **Executions Count** 之后，便于直接比较这两个值。它和其他列一样支持升序和降序排序。对于不涉及 IA 表的语句，该值为 `0`。

## 在集群级别监控 IA 缓存性能 {#monitor-ia-cache-performance-at-the-cluster-level}

本节介绍 TiDB Cloud 控制台中用于观察 IA 缓存行为的集群级面板。

### IA Cache Performance 面板 {#ia-cache-performance-panels}

路径：**Monitoring** > **Metrics** > **Instance Overview** > **IA Cache Performance**。

| 面板 | 描述 |
|-|-|
| **IA Cache Hit Rate (%)** | 集群整体的 IA 缓存命中率。当该值低于 85% 时，会显示黄色指示器 |
| **IA Cache Miss Rate (ops/s)** | IA 缓存未命中的频率。该值通常保持较低。若突然升高，表示出现了大量冷读，或缓存正承受压力 |
| **IA Remote Read Segment** | 从对象存储读取 segment 的频率（Count）和数据量（Size）。可用于评估对象存储请求量和带宽消耗 |
| **IA Remote Read Segment Wait Time** | 单次远程读取的等待时间，以 P99 和 Avg 展示。若持续升高，表示对象存储延时恶化或受到带宽限制 |

你可以使用时间选择器调整时间窗口，以观察更长时间的趋势。如果集群中没有 IA 表，这些面板会显示 **No IA data**，而不是 `0%` 或错误信息。

要监控单条语句的冷数据读取量，请使用 **Monitoring** > **Diagnosis** > **Slow Query** > **Coprocessor** 中的 `IA Remote Read Segment Size` 面板。

### 解读这些面板 {#interpret-the-panels}

缓存命中率取决于实际访问模式。访问集中时，命中率可能超过 95%；访问分散时，则可能低于 95%。

- **命中率突然下降**：检查 **IA Cache Miss Rate** 是否同时上升。如果同时上升，说明冷读确实增加，而不是采集问题。然后使用语句摘要表中的 `IA_EXEC_COUNT` 来识别哪些语句触发了冷读。
- **命中率持续偏低**：说明缓存正承受冷数据压力。可以考虑提高 IA cache 级别，或减少设置为 IA 的数据量。参见[配置和管理分层存储](/tidb-cloud/tiered-storage-guide.md)。
- **评估某张表是否适合 IA**：将某个分区设置为 IA 后，至少观察一个完整业务日的 **IA Cache Hit Rate**。如果命中率稳定，说明该访问模式适合 IA；如果波动很大或平均值较低，说明数据访问过于分散，不适合 IA。

## 诊断工作流 {#diagnostic-workflows}

### 在变更前估算转换窗口 {#estimate-the-conversion-window-before-a-change}

1. 运行 `SHOW STORAGE_CLASS TRANSITIONS`，检查是否已有其他转换正在进行。该表仅列出进行中的转换。
2. 查询 `mysql.tidb_storage_class_transition_history`，查看集群中过去类似转换的 `duration`，并按 `state = 'COMPLETED'` 进行过滤。
3. 在转换过程中，结合 `DURATION` 和 `PROGRESS` 估算剩余时间。

### 排查缓存命中率突然下降 {#investigate-a-sudden-drop-in-cache-hit-rate}

1. 确认 **IA Cache Hit Rate** 的下降，并检查 **IA Cache Miss Rate** 是否同时上升。
2. 在语句摘要表中识别 `IA_EXEC_COUNT / EXEC_COUNT` 比例较高的语句。
3. 如果许多语句的该比例同时上升，则很可能是一批分析型查询正在扫描 IA 表，并将热点数据从缓存中逐出。
4. 决定是提高 IA cache 级别，还是将受影响的数据迁回 Standard 存储。

### 决定是否将表保留在 IA 中 {#decide-whether-to-keep-a-table-in-ia}

1. 对访问该表的语句汇总 `IA_EXEC_COUNT / EXEC_COUNT`。
2. 如果大多数语句始终保持较高的冷读比例，则说明 IA 的缓存命中率过低。可以考虑将该表切回 Standard。
3. 如果冷读比例较低，但少数语句每次读取的数据量很大，则应优化这些语句，而不是将整张表切回。

## 另请参阅 {#see-also}

- [分层存储概览](/tidb-cloud/tiered-storage-overview.md)
- [配置和管理分层存储](/tidb-cloud/tiered-storage-guide.md)
- [分层存储限制](/tidb-cloud/tiered-storage-limitations.md)
- [分层存储常见问题](/tidb-cloud/tiered-storage-faq.md)