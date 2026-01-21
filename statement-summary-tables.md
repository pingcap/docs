---
title: Statement Summary Tables
summary: 了解 TiDB 中的 Statement Summary Table。
---

# Statement Summary Tables

为更好地处理 SQL 性能问题，MySQL 在 `performance_schema` 中提供了 [statement summary tables](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-summary-tables.html)，用于通过统计信息监控 SQL。在这些表中，`events_statements_summary_by_digest` 通过其丰富的字段（如延时、执行次数、扫描行数、全表扫描等）在定位 SQL 问题时非常有用。

因此，从 v4.0.0-rc.1 开始，TiDB 在 `information_schema`（**不是** `performance_schema`）中提供了与 `events_statements_summary_by_digest` 功能类似的系统表。

- [`statements_summary`](#statements_summary)
- [`statements_summary_history`](#statements_summary_history)
- [`cluster_statements_summary`](#statements_summary_evicted)
- [`cluster_statements_summary_history`](#statements_summary_evicted)
- [`statements_summary_evicted`](#statements_summary_evicted)

> **注意：**
>
> 上述表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

本文档详细介绍了这些表，并介绍如何使用它们来排查 SQL 性能问题。

## `statements_summary`

`statements_summary` 是 `information_schema` 中的系统表。`statements_summary` 按资源组、SQL digest 和 plan digest 对 SQL 语句进行分组，并为每类 SQL 提供统计信息。

这里的 “SQL digest” 与慢日志中使用的一致，是通过标准化 SQL 语句计算出的唯一标识。标准化过程会忽略常数、空白字符，并且不区分大小写。因此，语法一致的语句具有相同的 digest。例如：

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

标准化后，它们都属于如下类别：

```sql
select * from employee where id in (...) and salary between ? and ?;
```

这里的 “plan digest” 指的是通过标准化执行计划计算出的唯一标识。标准化过程会忽略常数。相同的 SQL 语句可能会因为执行计划不同而被分到不同的类别。属于同一类别的 SQL 语句具有相同的执行计划。

`statements_summary` 存储 SQL 监控指标的聚合结果。一般来说，每个监控指标都包含最大值和平均值。例如，执行延时指标对应两个字段：`AVG_LATENCY`（平均延时）和 `MAX_LATENCY`（最大延时）。

为保证监控指标的实时性，`statements_summary` 表中的数据会定期清理，仅保留和展示最近的聚合结果。定期清理数据的周期由 `tidb_stmt_summary_refresh_interval` 系统变量控制。如果你在清理后立即查询，显示的数据可能会很少。

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
> - 在 TiDB 中，statement summary 表中字段的时间单位为纳秒（ns），而在 MySQL 中为皮秒（ps）。
> - 从 v7.5.1 和 v7.6.0 开始，对于启用了 [资源管控](/tidb-resource-control-ru-groups.md) 的集群，`statements_summary` 会按资源组聚合，例如，相同语句在不同资源组中执行会被收集为不同的记录。

## `statements_summary_history`

`statements_summary_history` 的表结构与 `statements_summary` 完全一致。`statements_summary_history` 保存一段时间范围内的历史数据。通过查看历史数据，你可以排查异常并对比不同时段的监控指标。

`SUMMARY_BEGIN_TIME` 和 `SUMMARY_END_TIME` 字段分别表示历史时间范围的起始和结束时间。

## `statements_summary_evicted`

[`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40) 系统变量限制了 `statements_summary` 和 `statements_summary_history` 表在内存中总共能存储的 SQL digest 数量。当超过该限制时，TiDB 会从 `statements_summary` 和 `statements_summary_history` 表中淘汰最近最少使用的 SQL digest。

<CustomContent platform="tidb">

> **注意：**
>
> 当启用 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary) 后，`statements_summary_history` 表中的数据会持久化到磁盘。此时，`tidb_stmt_summary_max_stmt_count` 只限制 `statements_summary` 表在内存中能存储的 SQL digest 数量，超出后 TiDB 只会从 `statements_summary` 表中淘汰最近最少使用的 SQL digest。

</CustomContent>

`statements_summary_evicted` 表记录了发生淘汰的时间段以及该时间段内被淘汰的 SQL digest 数量。该表有助于你评估 `tidb_stmt_summary_max_stmt_count` 是否为你的负载配置得当。如果该表有记录，说明某一时刻 SQL digest 数量超过了 `tidb_stmt_summary_max_stmt_count`。

<CustomContent platform="tidb">

在 [TiDB Dashboard 的 SQL 语句页面](/dashboard/dashboard-statement-list.md#others) 中，被淘汰语句的信息会显示在 `Others` 行。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [诊断页面的 SQL 语句标签页](/tidb-cloud/tune-performance.md#statement-analysis) 中，被淘汰语句的信息会显示在 `Others` 行。

</CustomContent>

## statement summary 的 `cluster` 表

`statements_summary`、`statements_summary_history` 和 `statements_summary_evicted` 只展示单个 TiDB 服务器的 statement summary。要查询整个集群的数据，需要查询 `cluster_statements_summary`、`cluster_statements_summary_history` 或 `cluster_statements_summary_evicted` 表。

`cluster_statements_summary` 展示每个 TiDB 服务器的 `statements_summary` 数据。`cluster_statements_summary_history` 展示每个 TiDB 服务器的 `statements_summary_history` 数据。`cluster_statements_summary_evicted` 展示每个 TiDB 服务器的 `statements_summary_evicted` 数据。这些表通过 `INSTANCE` 字段表示 TiDB 服务器的地址，其他字段与 `statements_summary`、`statements_summary_history` 和 `statements_summary_evicted` 相同。

## 参数配置

以下系统变量用于控制 statement summary：

- `tidb_enable_stmt_summary`：决定是否启用 statement summary 功能。`1` 表示启用，`0` 表示禁用。默认启用。禁用后系统表中的统计信息会被清空；下次启用时会重新统计。测试表明启用该功能对性能影响很小。
- `tidb_stmt_summary_refresh_interval`：`statements_summary` 表的刷新周期，单位为秒（s）。默认值为 `1800`。
- `tidb_stmt_summary_history_size`：`statements_summary_history` 表中每类 SQL 语句存储的周期数，也是 `statements_summary_evicted` 表的最大记录数。默认值为 `24`。
- `tidb_stmt_summary_max_stmt_count`：限制 `statements_summary` 和 `statements_summary_history` 表在内存中总共能存储的 SQL digest 数量。默认值为 `3000`。

    超过该限制后，TiDB 会从 `statements_summary` 和 `statements_summary_history` 表中淘汰最近最少使用的 SQL digest。被淘汰的 digest 会被计入 [`statements_summary_evicted`](#statements_summary_evicted) 表。

    > **注意：**
    >
    > - 当某个 SQL digest 被淘汰时，其所有时间段相关的汇总数据会从 `statements_summary` 和 `statements_summary_history` 表中移除。因此，即使某个时间段内 SQL digest 数量未超限，`statements_summary_history` 表中的 SQL digest 数量也可能小于实际数量。如果出现这种情况并影响性能，建议适当增大 `tidb_stmt_summary_max_stmt_count` 的值。
    > - 对于 TiDB 自建集群，当启用 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary) 后，`statements_summary_history` 表中的数据会持久化到磁盘。此时，`tidb_stmt_summary_max_stmt_count` 只限制 `statements_summary` 表在内存中能存储的 SQL digest 数量，超出后 TiDB 只会从 `statements_summary` 表中淘汰最近最少使用的 SQL digest。

- `tidb_stmt_summary_max_sql_length`：指定 `DIGEST_TEXT` 和 `QUERY_SAMPLE_TEXT` 的最大显示长度。默认值为 `4096`。
- `tidb_stmt_summary_internal_query`：决定是否统计 TiDB SQL 语句。`1` 表示统计，`0` 表示不统计。默认值为 `0`。

statement summary 配置示例如下：

```sql
set global tidb_stmt_summary_max_stmt_count = 3000;
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

上述配置生效后，`statements_summary` 表每 30 分钟清空一次，`statements_summary_history` 表最多存储 3000 种 SQL 类型。每种类型，`statements_summary_history` 表保存最近 24 个周期的数据。`statements_summary_evicted` 表记录最近 24 个周期内 statement summary 被淘汰的情况，并每 30 分钟更新一次。

> **注意：**
>
> - 如果某种 SQL 类型每分钟出现一次，`statements_summary_history` 会保存最近 12 小时的数据。如果某种 SQL 类型每天只在 00:00 到 00:30 出现一次，`statements_summary_history` 会保存最近 24 个周期的数据，每个周期为 1 天。因此，该 SQL 类型会保存最近 24 天的数据。
> - `tidb_stmt_summary_history_size`、`tidb_stmt_summary_max_stmt_count` 和 `tidb_stmt_summary_max_sql_length` 配置项会影响内存使用量。建议根据实际需求、SQL 大小、SQL 数量和机器配置合理调整，不建议设置过大。可通过 `tidb_stmt_summary_history_size` \* `tidb_stmt_summary_max_stmt_count` \* `tidb_stmt_summary_max_sql_length` \* `3` 计算内存占用。

### 设置合适的 statement summary 大小

系统运行一段时间后（具体时间取决于系统负载），你可以通过查询 `statement_summary` 表判断是否发生了 SQL 淘汰。例如：

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

可以看到 `statements_summary` 表已满。然后查询 `statements_summary_evicted` 表中的淘汰数据：

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

从上述结果可以看到，最多有 59 种 SQL 类型被淘汰。此时建议将 `statement_summary` 表的大小至少增加 59 条记录，即增大到至少 3059 条。

## 限制

默认情况下，statements summary 表保存在内存中。当 TiDB 服务器重启时，所有数据都会丢失。

<CustomContent platform="tidb">

为解决该问题，TiDB v6.6.0 实验性地引入了 [statements summary 持久化](#persist-statements-summary) 特性，默认关闭。启用后，历史数据不再保存在内存中，而是直接写入磁盘。这样即使 TiDB 服务器重启，历史数据依然可用。

</CustomContent>

## 持久化 statements summary

<CustomContent platform="tidb-cloud">

本节仅适用于 TiDB 自建集群。对于 TiDB Cloud，`tidb_stmt_summary_enable_persistent` 参数的默认值为 `false`，且不支持动态修改。

</CustomContent>

> **警告：**
>
> statements summary 持久化是实验特性。不建议在生产环境中使用。该特性可能随时变更或移除，恕不另行通知。如发现 bug，可在 GitHub 提交 [issue](https://github.com/pingcap/tidb/issues)。

<CustomContent platform="tidb">

如 [限制](#limitation) 一节所述，statements summary 表默认保存在内存中。一旦 TiDB 服务器重启，所有 statements summary 都会丢失。从 v6.6.0 开始，TiDB 实验性地提供了 [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660) 配置项，允许用户开启或关闭 statements summary 持久化。

</CustomContent>

<CustomContent platform="tidb-cloud">

如 [限制](#limitation) 一节所述，statements summary 表默认保存在内存中。一旦 TiDB 服务器重启，所有 statements summary 都会丢失。从 v6.6.0 开始，TiDB 实验性地提供了 `tidb_stmt_summary_enable_persistent` 配置项，允许用户开启或关闭 statements summary 持久化。

</CustomContent>

要启用 statements summary 持久化，可以在 TiDB 配置文件中添加如下配置项：

```toml
[instance]
tidb_stmt_summary_enable_persistent = true
# 以下为默认值，可根据需要修改。
# tidb_stmt_summary_filename = "tidb-statements.log"
# tidb_stmt_summary_file_max_days = 3
# tidb_stmt_summary_file_max_size = 64 # MiB
# tidb_stmt_summary_file_max_backups = 0
```

启用 statements summary 持久化后，内存中只保留当前实时数据，不再保留历史数据。实时数据刷新为历史数据后，会按照 [参数配置](#parameter-configuration) 一节中 `tidb_stmt_summary_refresh_interval` 的周期写入磁盘。查询 `statements_summary_history` 或 `cluster_statements_summary_history` 表时，会返回内存和磁盘上的数据合并结果。

<CustomContent platform="tidb">

> **注意：**
>
> - 启用 statements summary 持久化后，[参数配置](#parameter-configuration) 一节中的 `tidb_stmt_summary_history_size` 配置项将不再生效，因为内存不再保留历史数据。此时，历史数据的保留周期和大小由以下三个配置项控制：[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)、[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) 和 [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)。
> - `tidb_stmt_summary_refresh_interval` 的值越小，数据写入磁盘越及时，但也会导致更多冗余数据写入磁盘。

</CustomContent>

## 排查示例

本节通过两个示例说明如何使用 statement summary 功能排查 SQL 性能问题。

### SQL 延时高是否由服务端引起？

本例中，客户端在对 `employee` 表进行点查时表现缓慢。你可以对 SQL 文本进行模糊查询：

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary
    WHERE digest_text LIKE 'select * from employee%';
```

`1ms` 和 `0.3ms` 属于 `avg_latency` 的正常范围，因此可以判断不是服务端原因。你可以继续排查客户端或网络。

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
- `SCHEMA_NAME`：该类别 SQL 语句执行时的当前 schema。
- `DIGEST`：该类别 SQL 语句的 digest。
- `DIGEST_TEXT`：标准化后的 SQL 语句。
- `QUERY_SAMPLE_TEXT`：该类别 SQL 语句的原始 SQL，仅取一条。
- `TABLE_NAMES`：SQL 语句涉及的所有表，多个表用逗号分隔。
- `INDEX_NAMES`：SQL 语句使用的所有索引，多个索引用逗号分隔。
- `SAMPLE_USER`：执行该类别 SQL 语句的用户，仅取一个。
- `PLAN_DIGEST`：执行计划的 digest。
- `PLAN`：原始执行计划，若有多条语句，仅取一条的计划。
- `BINARY_PLAN`：二进制编码的原始执行计划，若有多条语句，仅取一条的计划。可通过 [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan) 解析具体执行计划。
- `PLAN_CACHE_HITS`：该类别 SQL 语句命中 plan cache 的总次数。
- `PLAN_IN_CACHE`：上一次执行该类别 SQL 语句是否命中 plan cache。
- `PLAN_CACHE_UNQUALIFIED`：该类别 SQL 语句未命中 plan cache 的次数。
- `PLAN_CACHE_UNQUALIFIED_LAST_REASON`：该类别 SQL 语句上一次未命中 plan cache 的原因。

与执行时间相关的字段：

- `SUMMARY_BEGIN_TIME`：当前汇总周期的起始时间。
- `SUMMARY_END_TIME`：当前汇总周期的结束时间。
- `FIRST_SEEN`：首次出现该类别 SQL 语句的时间。
- `LAST_SEEN`：最后一次出现该类别 SQL 语句的时间。

<CustomContent platform="tidb">

与 TiDB 服务器相关的字段：

- `EXEC_COUNT`：该类别 SQL 语句的总执行次数。
- `SUM_ERRORS`：执行过程中发生的错误总数。
- `SUM_WARNINGS`：执行过程中发生的警告总数。
- `SUM_LATENCY`：该类别 SQL 语句的总执行延时。
- `MAX_LATENCY`：该类别 SQL 语句的最大执行延时。
- `MIN_LATENCY`：该类别 SQL 语句的最小执行延时。
- `AVG_LATENCY`：该类别 SQL 语句的平均执行延时。
- `AVG_PARSE_LATENCY`：解析器的平均延时。
- `MAX_PARSE_LATENCY`：解析器的最大延时。
- `AVG_COMPILE_LATENCY`：编译器的平均延时。
- `MAX_COMPILE_LATENCY`：编译器的最大延时。
- `AVG_MEM`：平均使用内存（字节）。
- `MAX_MEM`：最大使用内存（字节）。
- `AVG_DISK`：平均使用磁盘空间（字节）。
- `MAX_DISK`：最大使用磁盘空间（字节）。
- `AVG_TIDB_CPU_TIME`：该类别 SQL 语句消耗的 TiDB 服务器平均 CPU 时间。仅在启用 [Top SQL](/dashboard/top-sql.md) 功能时有意义，否则值始终为 `0`。

</CustomContent>

<CustomContent platform="tidb-cloud">

与 TiDB 服务器相关的字段：

- `EXEC_COUNT`：该类别 SQL 语句的总执行次数。
- `SUM_ERRORS`：执行过程中发生的错误总数。
- `SUM_WARNINGS`：执行过程中发生的警告总数。
- `SUM_LATENCY`：该类别 SQL 语句的总执行延时。
- `MAX_LATENCY`：该类别 SQL 语句的最大执行延时。
- `MIN_LATENCY`：该类别 SQL 语句的最小执行延时。
- `AVG_LATENCY`：该类别 SQL 语句的平均执行延时。
- `AVG_PARSE_LATENCY`：解析器的平均延时。
- `MAX_PARSE_LATENCY`：解析器的最大延时。
- `AVG_COMPILE_LATENCY`：编译器的平均延时。
- `MAX_COMPILE_LATENCY`：编译器的最大延时。
- `AVG_MEM`：平均使用内存（字节）。
- `MAX_MEM`：最大使用内存（字节）。
- `AVG_DISK`：平均使用磁盘空间（字节）。
- `MAX_DISK`：最大使用磁盘空间（字节）。
- `AVG_TIDB_CPU_TIME`：该类别 SQL 语句消耗的 TiDB 服务器平均 CPU 时间。仅在启用 Top SQL 功能时有意义，否则值始终为 `0`。

</CustomContent>

与 TiKV Coprocessor 任务相关的字段：

- `SUM_COP_TASK_NUM`：发送的 Coprocessor 请求总数。
- `MAX_COP_PROCESS_TIME`：Coprocessor 任务的最大执行时间。
- `MAX_COP_PROCESS_ADDRESS`：执行时间最长的 Coprocessor 任务的地址。
- `MAX_COP_WAIT_TIME`：Coprocessor 任务的最大等待时间。
- `MAX_COP_WAIT_ADDRESS`：等待时间最长的 Coprocessor 任务的地址。
- `AVG_PROCESS_TIME`：SQL 语句在 TiKV 的平均处理时间。
- `MAX_PROCESS_TIME`：SQL 语句在 TiKV 的最大处理时间。
- `AVG_WAIT_TIME`：SQL 语句在 TiKV 的平均等待时间。
- `MAX_WAIT_TIME`：SQL 语句在 TiKV 的最大等待时间。
- `AVG_BACKOFF_TIME`：SQL 语句遇到需重试错误时，重试前的平均等待时间。
- `MAX_BACKOFF_TIME`：SQL 语句遇到需重试错误时，重试前的最大等待时间。
- `AVG_TOTAL_KEYS`：Coprocessor 扫描的平均 key 数量。
- `MAX_TOTAL_KEYS`：Coprocessor 扫描的最大 key 数量。
- `AVG_PROCESSED_KEYS`：Coprocessor 处理的平均 key 数量。与 `avg_total_keys` 相比，`avg_processed_keys` 不包含 MVCC 的旧版本。如果两者差异较大，说明存在大量旧版本。
- `MAX_PROCESSED_KEYS`：Coprocessor 处理的最大 key 数量。
- `AVG_TIKV_CPU_TIME`：该类别 SQL 语句消耗的 TiKV 服务器平均 CPU 时间。

与事务相关的字段：

- `AVG_PREWRITE_TIME`：prewrite 阶段的平均耗时。
- `MAX_PREWRITE_TIME`：prewrite 阶段的最长耗时。
- `AVG_COMMIT_TIME`：commit 阶段的平均耗时。
- `MAX_COMMIT_TIME`：commit 阶段的最长耗时。
- `AVG_GET_COMMIT_TS_TIME`：获取 `commit_ts` 的平均耗时。
- `MAX_GET_COMMIT_TS_TIME`：获取 `commit_ts` 的最长耗时。
- `AVG_COMMIT_BACKOFF_TIME`：commit 阶段遇到需重试错误时，重试前的平均等待时间。
- `MAX_COMMIT_BACKOFF_TIME`：commit 阶段遇到需重试错误时，重试前的最大等待时间。
- `AVG_RESOLVE_LOCK_TIME`：事务间锁冲突的平均解决时间。
- `MAX_RESOLVE_LOCK_TIME`：事务间锁冲突的最长解决时间。
- `AVG_LOCAL_LATCH_WAIT_TIME`：本地事务的平均等待时间。
- `MAX_LOCAL_LATCH_WAIT_TIME`：本地事务的最大等待时间。
- `AVG_WRITE_KEYS`：平均写入 key 数量。
- `MAX_WRITE_KEYS`：最大写入 key 数量。
- `AVG_WRITE_SIZE`：平均写入数据量（字节）。
- `MAX_WRITE_SIZE`：最大写入数据量（字节）。
- `AVG_PREWRITE_REGIONS`：prewrite 阶段涉及的 Region 平均数量。
- `MAX_PREWRITE_REGIONS`：prewrite 阶段涉及的最大 Region 数量。
- `AVG_TXN_RETRY`：事务平均重试次数。
- `MAX_TXN_RETRY`：事务最大重试次数。
- `SUM_BACKOFF_TIMES`：该类别 SQL 语句遇到需重试错误时的总重试次数。
- `BACKOFF_TYPES`：所有需重试的错误类型及各自的重试次数。字段格式为 `type:number`，多个类型用逗号分隔，如 `txnLock:2,pdRPC:1`。
- `AVG_AFFECTED_ROWS`：平均受影响行数。
- `PREV_SAMPLE_TEXT`：当前 SQL 语句为 `COMMIT` 时，`PREV_SAMPLE_TEXT` 为上一个语句。此时，SQL 语句按 digest 和 `prev_sample_text` 分组，即不同 `prev_sample_text` 的 `COMMIT` 语句分到不同行。当前 SQL 语句不是 `COMMIT` 时，`PREV_SAMPLE_TEXT` 为空字符串。

与资源管控相关的字段：

- `AVG_REQUEST_UNIT_WRITE`：SQL 语句平均消耗的写 RU 数量。
- `MAX_REQUEST_UNIT_WRITE`：SQL 语句最大消耗的写 RU 数量。
- `AVG_REQUEST_UNIT_READ`：SQL 语句平均消耗的读 RU 数量。
- `MAX_REQUEST_UNIT_READ`：SQL 语句最大消耗的读 RU 数量。
- `AVG_QUEUED_RC_TIME`：SQL 语句执行时等待可用 RU 的平均时间。
- `MAX_QUEUED_RC_TIME`：SQL 语句执行时等待可用 RU 的最大时间。
- `RESOURCE_GROUP`：SQL 语句绑定的资源组。

与存储引擎相关的字段：

- `STORAGE_KV`：v8.5.5 引入，表示上一次执行该类别 SQL 语句是否从 TiKV 读取数据。
- `STORAGE_MPP`：v8.5.5 引入，表示上一次执行该类别 SQL 语句是否从 TiFlash 读取数据。

### `statements_summary_evicted` 字段说明

- `BEGIN_TIME`：记录起始时间。
- `END_TIME`：记录结束时间。
- `EVICTED_COUNT`：该记录周期内被淘汰的 SQL 类型数量。