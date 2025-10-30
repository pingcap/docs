---
title: Statement Summary Tables
summary: 了解 TiDB 中的语句概要表。
---

# 语句概要表

为更好地处理 SQL 性能问题，MySQL 在 `performance_schema` 中提供了 [statement summary tables](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-summary-tables.html)（语句概要表），用于通过统计信息监控 SQL。在这些表中，`events_statements_summary_by_digest` 表凭借其丰富的字段（如延迟、执行次数、扫描行数、全表扫描等）在定位 SQL 问题时非常有用。

因此，从 v4.0.0-rc.1 版本开始，TiDB 在 `information_schema`（**不是** `performance_schema`）中提供了与 `events_statements_summary_by_digest` 功能类似的系统表。

- [`statements_summary`](#statements_summary)
- [`statements_summary_history`](#statements_summary_history)
- [`cluster_statements_summary`](#statements_summary_evicted)
- [`cluster_statements_summary_history`](#statements_summary_evicted)
- [`statements_summary_evicted`](#statements_summary_evicted)

> **注意：**
>
> 上述表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

本文档详细介绍了这些表，并说明如何使用它们来排查 SQL 性能问题。

## `statements_summary`

`statements_summary` 是 `information_schema` 下的系统表。`statements_summary` 按资源组、SQL 摘要（digest）和执行计划摘要（plan digest）对 SQL 语句进行分组，并为每类 SQL 提供统计信息。

这里的 “SQL 摘要” 与慢日志中的含义一致，是通过标准化 SQL 语句计算得到的唯一标识。标准化过程会忽略常量、空白字符，并且不区分大小写。因此，语法一致的语句会有相同的摘要。例如：

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

标准化后，它们都属于如下类别：

```sql
select * from employee where id in (...) and salary between ? and ?;
```

这里的 “plan digest” 指的是通过标准化执行计划计算得到的唯一标识。标准化过程会忽略常量。相同的 SQL 语句可能会因为执行计划不同而被分到不同的类别。属于同一类别的 SQL 语句具有相同的执行计划。

`statements_summary` 存储 SQL 监控指标的聚合结果。一般来说，每个监控指标都包含最大值和平均值。例如，执行延迟指标对应两个字段：`AVG_LATENCY`（平均延迟）和 `MAX_LATENCY`（最大延迟）。

为保证监控指标的实时性，`statements_summary` 表中的数据会定期清理，仅保留和展示最近的聚合结果。定期清理的周期由系统变量 `tidb_stmt_summary_refresh_interval` 控制。如果你在清理后立即查询，可能会看到数据量很少。

以下是查询 `statements_summary` 的示例输出：

```
   SUMMARY_BEGIN_TIME: 2020-01-02 11:00:00
     SUMMARY_END_TIME: 2020-01-02 11:30:00
            STMT_TYPE: Select
          SCHEMA_NAME: test
               DIGEST: 0611cc2fe792f8c146cc97d39b31d9562014cf15f8d41f23a4938ca341f54182
          DIGEST_TEXT: select * from employee where id = ?
          TABLE_NAMES: test.employee
          INDEX_NAMES: NULL
          SAMPLE_USER: root
           EXEC_COUNT: 3
          SUM_LATENCY: 1035161
          MAX_LATENCY: 399594
          MIN_LATENCY: 301353
          AVG_LATENCY: 345053
    AVG_PARSE_LATENCY: 57000
    MAX_PARSE_LATENCY: 57000
  AVG_COMPILE_LATENCY: 175458
  MAX_COMPILE_LATENCY: 175458
  ...........
              AVG_MEM: 103
              MAX_MEM: 103
              AVG_DISK: 65535
              MAX_DISK: 65535
    AVG_AFFECTED_ROWS: 0
           FIRST_SEEN: 2020-01-02 11:12:54
            LAST_SEEN: 2020-01-02 11:25:24
    QUERY_SAMPLE_TEXT: select * from employee where id=3100
     PREV_SAMPLE_TEXT:
          PLAN_DIGEST: f415b8d52640b535b9b12a9c148a8630d2c6d59e419aad29397842e32e8e5de3
                 PLAN:  Point_Get_1     root    1       table:employee, handle:3100
```

> **注意：**
>
> - 在 TiDB 中，语句概要表中各字段的时间单位为纳秒（ns），而在 MySQL 中为皮秒（ps）。
> - 从 v7.5.1 和 v7.6.0 开始，对于启用了 [资源管控](/tidb-resource-control-ru-groups.md) 的集群，`statements_summary` 会按资源组进行聚合，例如同一语句在不同资源组下执行会被收集为不同的记录。

## `statements_summary_history`

`statements_summary_history` 的表结构与 `statements_summary` 完全一致。`statements_summary_history` 保存一段时间范围内的历史数据。通过查看历史数据，你可以排查异常并对比不同时段的监控指标。

`SUMMARY_BEGIN_TIME` 和 `SUMMARY_END_TIME` 字段分别表示历史时间段的起始和结束时间。

## `statements_summary_evicted`

[`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40) 系统变量限制了 `statements_summary` 和 `statements_summary_history` 两张表在内存中总共能存储的 SQL 摘要数量。当超过该限制时，TiDB 会从 `statements_summary` 和 `statements_summary_history` 表中淘汰最久未使用的 SQL 摘要。

<CustomContent platform="tidb">

> **注意：**
>
> 当启用 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary) 后，`statements_summary_history` 表中的数据会持久化到磁盘。此时，`tidb_stmt_summary_max_stmt_count` 只限制 `statements_summary` 表在内存中能存储的 SQL 摘要数量，超出时仅从 `statements_summary` 表中淘汰最久未使用的 SQL 摘要。

</CustomContent>

`statements_summary_evicted` 表记录了淘汰发生的时间段以及该时间段内被淘汰的 SQL 摘要数量。该表有助于你评估 `tidb_stmt_summary_max_stmt_count` 是否配置合理。如果该表有记录，说明某一时刻 SQL 摘要数量超过了 `tidb_stmt_summary_max_stmt_count`。

<CustomContent platform="tidb">

在 [TiDB Dashboard 的 SQL 语句页面](/dashboard/dashboard-statement-list.md#others) 中，被淘汰语句的信息会显示在 `Others` 行。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [诊断页面的 SQL 语句标签页](/tidb-cloud/tune-performance.md#statement-analysis) 中，被淘汰语句的信息会显示在 `Others` 行。

</CustomContent>

## 语句概要的 `cluster` 表

`statements_summary`、`statements_summary_history` 和 `statements_summary_evicted` 只展示单个 TiDB 实例的语句概要。要查询整个集群的数据，需要查询 `cluster_statements_summary`、`cluster_statements_summary_history` 或 `cluster_statements_summary_evicted` 表。

`cluster_statements_summary` 展示每个 TiDB 实例的 `statements_summary` 数据。`cluster_statements_summary_history` 展示每个 TiDB 实例的 `statements_summary_history` 数据。`cluster_statements_summary_evicted` 展示每个 TiDB 实例的 `statements_summary_evicted` 数据。这些表通过 `INSTANCE` 字段表示 TiDB 实例的地址，其他字段与 `statements_summary`、`statements_summary_history`、`statements_summary_evicted` 相同。

## 参数配置

以下系统变量用于控制语句概要功能：

- `tidb_enable_stmt_summary`：是否开启语句概要功能。`1` 表示开启，`0` 表示关闭。默认开启。关闭后系统表中的统计信息会被清空；下次开启时重新统计。测试表明开启该功能对性能影响很小。
- `tidb_stmt_summary_refresh_interval`：`statements_summary` 表的刷新周期，单位为秒（s）。默认值为 `1800`。
- `tidb_stmt_summary_history_size`：`statements_summary_history` 表中每类 SQL 语句存储的历史周期数，也是 `statements_summary_evicted` 表的最大记录数。默认值为 `24`。
- `tidb_stmt_summary_max_stmt_count`：限制 `statements_summary` 和 `statements_summary_history` 两张表在内存中总共能存储的 SQL 摘要数量。默认值为 `3000`。

    超过该限制后，TiDB 会从 `statements_summary` 和 `statements_summary_history` 表中淘汰最久未使用的 SQL 摘要，被淘汰的摘要会计入 [`statements_summary_evicted`](#statements_summary_evicted) 表。

    > **注意：**
    >
    > - 当某个 SQL 摘要被淘汰时，其所有时间段相关的概要数据会从 `statements_summary` 和 `statements_summary_history` 表中移除。因此，即使某个时间段内 SQL 摘要数量未超限，`statements_summary_history` 表中的 SQL 摘要数量也可能小于实际数量。如果出现这种情况且影响性能，建议适当增大 `tidb_stmt_summary_max_stmt_count` 的值。
    > - 对于 TiDB 自建集群，当启用 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary) 后，`statements_summary_history` 表中的数据会持久化到磁盘。此时，`tidb_stmt_summary_max_stmt_count` 只限制 `statements_summary` 表在内存中能存储的 SQL 摘要数量，超出时仅从 `statements_summary` 表中淘汰最久未使用的 SQL 摘要。

- `tidb_stmt_summary_max_sql_length`：指定 `DIGEST_TEXT` 和 `QUERY_SAMPLE_TEXT` 的最大显示长度。默认值为 `4096`。
- `tidb_stmt_summary_internal_query`：是否统计 TiDB 内部 SQL 语句。`1` 表示统计，`0` 表示不统计。默认值为 `0`。

语句概要配置示例如下：

```sql
set global tidb_stmt_summary_max_stmt_count = 3000;
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

上述配置生效后，`statements_summary` 表每 30 分钟清空一次，`statements_summary_history` 表最多存储 3000 种 SQL 类型，每种类型保留最近 24 个周期的数据。`statements_summary_evicted` 表记录最近 24 个周期内被淘汰的 SQL 语句，且每 30 分钟更新一次。

> **注意：**
>
> - 如果某类 SQL 每分钟出现一次，则 `statements_summary_history` 可保存最近 12 小时的数据。如果某类 SQL 只在每天 00:00 到 00:30 出现，则 `statements_summary_history` 可保存最近 24 天的数据（每个周期为 1 天）。
> - `tidb_stmt_summary_history_size`、`tidb_stmt_summary_max_stmt_count` 和 `tidb_stmt_summary_max_sql_length` 配置项会影响内存使用量。建议根据实际需求、SQL 大小、SQL 数量和机器配置合理调整，不建议设置过大。可通过 `tidb_stmt_summary_history_size` \* `tidb_stmt_summary_max_stmt_count` \* `tidb_stmt_summary_max_sql_length` \* `3` 计算内存占用。

### 设置合适的语句概要表大小

系统运行一段时间（视负载而定）后，你可以检查 `statement_summary` 表，判断是否发生了 SQL 淘汰。例如：

```sql
select @@global.tidb_stmt_summary_max_stmt_count;
select count(*) from information_schema.statements_summary;
```

```sql
+-------------------------------------------+
| @@global.tidb_stmt_summary_max_stmt_count |
+-------------------------------------------+
| 3000                                      |
+-------------------------------------------+
1 row in set (0.001 sec)

+----------+
| count(*) |
+----------+
|     3001 |
+----------+
1 row in set (0.001 sec)
```

可以看到 `statements_summary` 表已满。接着查询 `statements_summary_evicted` 表中的淘汰数据：

```sql
select * from information_schema.statements_summary_evicted;
```

```sql
+---------------------+---------------------+---------------+
| BEGIN_TIME          | END_TIME            | EVICTED_COUNT |
+---------------------+---------------------+---------------+
| 2020-01-02 16:30:00 | 2020-01-02 17:00:00 |            59 |
+---------------------+---------------------+---------------+
| 2020-01-02 16:00:00 | 2020-01-02 16:30:00 |            45 |
+---------------------+---------------------+---------------+
2 row in set (0.001 sec)
```

从上述结果可见，最多有 59 类 SQL 被淘汰。此时建议将 `statement_summary` 表的大小至少增加 59 条记录，即增大到至少 3059 条。

## 限制

默认情况下，语句概要表保存在内存中。当 TiDB 实例重启时，所有数据都会丢失。

<CustomContent platform="tidb">

为解决该问题，TiDB v6.6.0 实验性引入了 [语句概要持久化](#persist-statements-summary) 功能，默认关闭。开启后，历史数据不再保存在内存中，而是直接写入磁盘。这样即使 TiDB 实例重启，历史数据依然可用。

</CustomContent>

## 语句概要持久化

<CustomContent platform="tidb-cloud">

本节仅适用于 TiDB 自建集群。对于 TiDB Cloud，`tidb_stmt_summary_enable_persistent` 参数的默认值为 `false`，且不支持动态修改。

</CustomContent>

> **警告：**
>
> 语句概要持久化为实验性功能。不建议在生产环境中使用。该功能可能随时变更或移除，恕不另行通知。如发现 bug，可在 GitHub 提 [issue](https://github.com/pingcap/tidb/issues)。

<CustomContent platform="tidb">

如 [限制](#limitation) 一节所述，语句概要表默认保存在内存中，TiDB 实例重启后所有概要数据会丢失。从 v6.6.0 起，TiDB 实验性地提供了配置项 [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)，允许用户开启或关闭语句概要持久化。

</CustomContent>

<CustomContent platform="tidb-cloud">

如 [限制](#limitation) 一节所述，语句概要表默认保存在内存中，TiDB 实例重启后所有概要数据会丢失。从 v6.6.0 起，TiDB 实验性地提供了配置项 `tidb_stmt_summary_enable_persistent`，允许用户开启或关闭语句概要持久化。

</CustomContent>

要开启语句概要持久化，可以在 TiDB 配置文件中添加如下配置项：

```toml
[instance]
tidb_stmt_summary_enable_persistent = true
# 以下为默认值，可根据需要修改
# tidb_stmt_summary_filename = "tidb-statements.log"
# tidb_stmt_summary_file_max_days = 3
# tidb_stmt_summary_file_max_size = 64 # MiB
# tidb_stmt_summary_file_max_backups = 0
```

开启语句概要持久化后，内存中只保留当前实时数据，不再保留历史数据。实时数据刷新为历史数据后，会按照 [参数配置](#parameter-configuration) 中 `tidb_stmt_summary_refresh_interval` 的周期写入磁盘。查询 `statements_summary_history` 或 `cluster_statements_summary_history` 表时，会返回内存和磁盘上的数据合并结果。

<CustomContent platform="tidb">

> **注意：**
>
> - 开启语句概要持久化后，[参数配置](#parameter-configuration) 中的 `tidb_stmt_summary_history_size` 配置项不再生效，因为内存中不再保留历史数据。此时，持久化历史数据的保留周期和大小由以下三个配置项控制：[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)、[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660)、[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)。
> - `tidb_stmt_summary_refresh_interval` 的值越小，数据写入磁盘越及时，但也会导致更多冗余数据写入磁盘。

</CustomContent>

## 故障排查示例

本节通过两个示例说明如何利用语句概要功能排查 SQL 性能问题。

### SQL 延迟高是否由服务端引起？

本例中，客户端在对 `employee` 表进行点查时表现缓慢。你可以对 SQL 文本进行模糊查询：

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary
    WHERE digest_text LIKE 'select * from employee%';
```

`1ms` 和 `0.3ms` 的 `avg_latency` 属于正常范围，因此可以判断不是服务端原因。你可以继续排查客户端或网络问题。

```sql
+-------------+------------+------------------------------------------+
| avg_latency | exec_count | query_sample_text                        |
+-------------+------------+------------------------------------------+
|     1042040 |          2 | select * from employee where name='eric' |
|      345053 |          3 | select * from employee where id=3100     |
+-------------+------------+------------------------------------------+
2 rows in set (0.00 sec)
```

### 哪些类别的 SQL 语句总耗时最长？

如果 10:00 到 10:30 期间 QPS 明显下降，你可以从历史表中找出总耗时最长的三类 SQL 语句：

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary_history
    WHERE summary_begin_time='2020-01-02 10:00:00'
    ORDER BY sum_latency DESC LIMIT 3;
```

结果显示以下三类 SQL 语句总耗时最长，应优先优化。

```sql
+-------------+-------------+------------+-----------------------------------------------------------------------+
| sum_latency | avg_latency | exec_count | query_sample_text                                                     |
+-------------+-------------+------------+-----------------------------------------------------------------------+
|     7855660 |     1122237 |          7 | select avg(salary) from employee where company_id=2013                |
|     7241960 |     1448392 |          5 | select * from employee join company on employee.company_id=company.id |
|     2084081 |     1042040 |          2 | select * from employee where name='eric'                              |
+-------------+-------------+------------+-----------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

## 字段说明

### `statements_summary` 字段说明

以下为 `statements_summary` 表中各字段的说明。

基础字段：

- `STMT_TYPE`：SQL 语句类型。
- `SCHEMA_NAME`：本类 SQL 语句执行时的当前 schema。
- `DIGEST`：本类 SQL 语句的摘要。
- `DIGEST_TEXT`：标准化后的 SQL 语句。
- `QUERY_SAMPLE_TEXT`：本类 SQL 语句的原始 SQL，仅取一条。
- `TABLE_NAMES`：SQL 涉及的所有表，多个表用逗号分隔。
- `INDEX_NAMES`：SQL 涉及的所有索引，多个索引用逗号分隔。
- `SAMPLE_USER`：执行本类 SQL 语句的用户，仅取一个。
- `PLAN_DIGEST`：执行计划的摘要。
- `PLAN`：原始执行计划，若有多条，仅取一条的计划。
- `BINARY_PLAN`：二进制编码的原始执行计划，若有多条，仅取一条的计划。可通过 [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan) 解析具体执行计划。
- `PLAN_CACHE_HITS`：本类 SQL 命中执行计划缓存的总次数。
- `PLAN_IN_CACHE`：上一次执行本类 SQL 是否命中执行计划缓存。
- `PLAN_CACHE_UNQUALIFIED`：本类 SQL 未命中执行计划缓存的次数。
- `PLAN_CACHE_UNQUALIFIED_LAST_REASON`：本类 SQL 上一次未命中执行计划缓存的原因。

与执行时间相关的字段：

- `SUMMARY_BEGIN_TIME`：当前统计周期的起始时间。
- `SUMMARY_END_TIME`：当前统计周期的结束时间。
- `FIRST_SEEN`：本类 SQL 首次出现的时间。
- `LAST_SEEN`：本类 SQL 最后一次出现的时间。

<CustomContent platform="tidb">

与 TiDB 实例相关的字段：

- `EXEC_COUNT`：本类 SQL 的总执行次数。
- `SUM_ERRORS`：执行过程中发生的错误总数。
- `SUM_WARNINGS`：执行过程中发生的警告总数。
- `SUM_LATENCY`：本类 SQL 的总执行延迟。
- `MAX_LATENCY`：本类 SQL 的最大执行延迟。
- `MIN_LATENCY`：本类 SQL 的最小执行延迟。
- `AVG_LATENCY`：本类 SQL 的平均执行延迟。
- `AVG_PARSE_LATENCY`：解析器平均延迟。
- `MAX_PARSE_LATENCY`：解析器最大延迟。
- `AVG_COMPILE_LATENCY`：编译器平均延迟。
- `MAX_COMPILE_LATENCY`：编译器最大延迟。
- `AVG_MEM`：平均内存（字节）使用量。
- `MAX_MEM`：最大内存（字节）使用量。
- `AVG_DISK`：平均磁盘空间（字节）使用量。
- `MAX_DISK`：最大磁盘空间（字节）使用量。
- `AVG_TIDB_CPU_TIME`：本类 SQL 在 TiDB 实例上消耗的平均 CPU 时间。仅在开启 [Top SQL](/dashboard/top-sql.md) 功能时有意义，否则值为 `0`。

</CustomContent>

<CustomContent platform="tidb-cloud">

与 TiDB 实例相关的字段：

- `EXEC_COUNT`：本类 SQL 的总执行次数。
- `SUM_ERRORS`：执行过程中发生的错误总数。
- `SUM_WARNINGS`：执行过程中发生的警告总数。
- `SUM_LATENCY`：本类 SQL 的总执行延迟。
- `MAX_LATENCY`：本类 SQL 的最大执行延迟。
- `MIN_LATENCY`：本类 SQL 的最小执行延迟。
- `AVG_LATENCY`：本类 SQL 的平均执行延迟。
- `AVG_PARSE_LATENCY`：解析器平均延迟。
- `MAX_PARSE_LATENCY`：解析器最大延迟。
- `AVG_COMPILE_LATENCY`：编译器平均延迟。
- `MAX_COMPILE_LATENCY`：编译器最大延迟。
- `AVG_MEM`：平均内存（字节）使用量。
- `MAX_MEM`：最大内存（字节）使用量。
- `AVG_DISK`：平均磁盘空间（字节）使用量。
- `MAX_DISK`：最大磁盘空间（字节）使用量。
- `AVG_TIDB_CPU_TIME`：本类 SQL 在 TiDB 实例上消耗的平均 CPU 时间。仅在开启 Top SQL 功能时有意义，否则值为 `0`。

</CustomContent>

与 TiKV Coprocessor 任务相关的字段：

- `SUM_COP_TASK_NUM`：发送的 Coprocessor 请求总数。
- `MAX_COP_PROCESS_TIME`：Coprocessor 任务的最大执行时间。
- `MAX_COP_PROCESS_ADDRESS`：执行时间最长的 Coprocessor 任务所在地址。
- `MAX_COP_WAIT_TIME`：Coprocessor 任务的最大等待时间。
- `MAX_COP_WAIT_ADDRESS`：等待时间最长的 Coprocessor 任务所在地址。
- `AVG_PROCESS_TIME`：SQL 在 TiKV 的平均处理时间。
- `MAX_PROCESS_TIME`：SQL 在 TiKV 的最大处理时间。
- `AVG_WAIT_TIME`：SQL 在 TiKV 的平均等待时间。
- `MAX_WAIT_TIME`：SQL 在 TiKV 的最大等待时间。
- `AVG_BACKOFF_TIME`：SQL 遇到需重试错误时的平均等待时间。
- `MAX_BACKOFF_TIME`：SQL 遇到需重试错误时的最大等待时间。
- `AVG_TOTAL_KEYS`：Coprocessor 扫描的平均 key 数。
- `MAX_TOTAL_KEYS`：Coprocessor 扫描的最大 key 数。
- `AVG_PROCESSED_KEYS`：Coprocessor 实际处理的平均 key 数。与 `avg_total_keys` 相比，不包含 MVCC 的旧版本。如果两者差异较大，说明存在大量旧版本。
- `MAX_PROCESSED_KEYS`：Coprocessor 实际处理的最大 key 数。
- `AVG_TIKV_CPU_TIME`：本类 SQL 在 TiKV 实例上消耗的平均 CPU 时间。

与事务相关的字段：

- `AVG_PREWRITE_TIME`：预写阶段的平均耗时。
- `MAX_PREWRITE_TIME`：预写阶段的最大耗时。
- `AVG_COMMIT_TIME`：提交阶段的平均耗时。
- `MAX_COMMIT_TIME`：提交阶段的最大耗时。
- `AVG_GET_COMMIT_TS_TIME`：获取 `commit_ts` 的平均耗时。
- `MAX_GET_COMMIT_TS_TIME`：获取 `commit_ts` 的最大耗时。
- `AVG_COMMIT_BACKOFF_TIME`：提交阶段遇到需重试错误时的平均等待时间。
- `MAX_COMMIT_BACKOFF_TIME`：提交阶段遇到需重试错误时的最大等待时间。
- `AVG_RESOLVE_LOCK_TIME`：事务间锁冲突的平均解决时间。
- `MAX_RESOLVE_LOCK_TIME`：事务间锁冲突的最大解决时间。
- `AVG_LOCAL_LATCH_WAIT_TIME`：本地事务的平均等待时间。
- `MAX_LOCAL_LATCH_WAIT_TIME`：本地事务的最大等待时间。
- `AVG_WRITE_KEYS`：平均写入 key 数。
- `MAX_WRITE_KEYS`：最大写入 key 数。
- `AVG_WRITE_SIZE`：平均写入数据量（字节）。
- `MAX_WRITE_SIZE`：最大写入数据量（字节）。
- `AVG_PREWRITE_REGIONS`：预写阶段涉及的 Region 平均数。
- `MAX_PREWRITE_REGIONS`：预写阶段涉及的最大 Region 数。
- `AVG_TXN_RETRY`：事务平均重试次数。
- `MAX_TXN_RETRY`：事务最大重试次数。
- `SUM_BACKOFF_TIMES`：本类 SQL 遇到需重试错误时的总重试次数。
- `BACKOFF_TYPES`：所有需重试错误类型及各自重试次数，格式为 `type:number`，多个类型用逗号分隔，如 `txnLock:2,pdRPC:1`。
- `AVG_AFFECTED_ROWS`：平均影响行数。
- `PREV_SAMPLE_TEXT`：当前 SQL 为 `COMMIT` 时，`PREV_SAMPLE_TEXT` 为上一个 SQL 语句。此时按摘要和 `prev_sample_text` 分组，即不同 `prev_sample_text` 的 `COMMIT` 语句分到不同行。非 `COMMIT` 语句时该字段为空字符串。

与资源管控相关的字段：

- `AVG_REQUEST_UNIT_WRITE`：SQL 平均消耗的写 RU 数量。
- `MAX_REQUEST_UNIT_WRITE`：SQL 最大消耗的写 RU 数量。
- `AVG_REQUEST_UNIT_READ`：SQL 平均消耗的读 RU 数量。
- `MAX_REQUEST_UNIT_READ`：SQL 最大消耗的读 RU 数量。
- `AVG_QUEUED_RC_TIME`：SQL 等待可用 RU 的平均时间。
- `MAX_QUEUED_RC_TIME`：SQL 等待可用 RU 的最大时间。
- `RESOURCE_GROUP`：SQL 绑定的资源组。

### `statements_summary_evicted` 字段说明

- `BEGIN_TIME`：记录起始时间。
- `END_TIME`：记录结束时间。
- `EVICTED_COUNT`：该周期内被淘汰的 SQL 类别数量。