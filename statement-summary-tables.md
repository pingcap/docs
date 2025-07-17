---
title: Statement Summary Tables
summary: 了解 TiDB 中的 Statement Summary Table。
---

# Statement Summary Tables

为了更好地处理 SQL 性能问题，MySQL 在 `performance_schema` 中提供了 [statement summary tables](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-summary-tables.html)，用于监控带有统计信息的 SQL。在这些表中，`events_statements_summary_by_digest` 非常有用，它具有丰富的字段，如延迟、执行时间、扫描行数和全表扫描等，有助于定位 SQL 问题。

因此，从 v4.0.0-rc.1 版本开始，TiDB 在 `information_schema` 中提供了与 `events_statements_summary_by_digest` 类似的系统表（**不是** `performance_schema`），具有相似的功能。

- [`statements_summary`](#statements_summary)
- [`statements_summary_history`](#statements_summary_history)
- [`cluster_statements_summary`](#statements_summary_evicted)
- [`cluster_statements_summary_history`](#statements_summary_evicted)
- [`statements_summary_evicted`](#statements_summary_evicted)

> **Note:**
>
> 以上表在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

本文档详细介绍这些表，并说明如何利用它们排查 SQL 性能问题。

## `statements_summary`

`statements_summary` 是 `information_schema` 中的系统表。它将 SQL 语句按资源组、SQL digest 和计划 digest 进行分组，并提供每个类别的统计信息。

这里的“SQL digest”与慢日志中使用的相同，是通过规范化 SQL 语句计算得出的唯一标识符。规范化过程会忽略常量、空白字符，并且不区分大小写。因此，语法一致的语句具有相同的 digest。例如：

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

规范化后，它们都属于以下类别：

```sql
select * from employee where id in (...) and salary between ? and ?;
```

这里的“plan digest” 指通过规范化执行计划计算得出的唯一标识符。规范化过程会忽略常量。相同的 SQL 语句可能会被分到不同的类别，因为它们可能有不同的执行计划。属于同一类别的 SQL 语句具有相同的执行计划。

`statements_summary` 存储 SQL 监控指标的聚合结果。一般来说，每个监控指标都包括最大值和平均值。例如，执行延迟指标对应两个字段：`AVG_LATENCY`（平均延迟）和 `MAX_LATENCY`（最大延迟）。

为了确保监控指标的实时性，`statements_summary` 表中的数据会定期清理，只保留和显示最近的聚合结果。数据清理由系统变量 `tidb_stmt_summary_refresh_interval` 控制。如果你在清理后立即查询，显示的数据可能非常少。

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

> **Note:**
>
> - 在 TiDB 中，statement summary 表中字段的时间单位为纳秒（ns），而在 MySQL 中为皮秒（ps）。
> - 从 v7.5.1 和 v7.6.0 开始，对于启用 [resource control](/tidb-resource-control-ru-groups.md) 的集群，`statements_summary` 会按资源组进行聚合，例如，在不同资源组中执行的相同语句会作为不同的记录收集。

## `statements_summary_history`

`statements_summary_history` 的表结构与 `statements_summary` 相同。它保存某个时间范围内的历史数据。通过查看历史数据，可以排查异常情况，并对比不同时间范围的监控指标。

字段 `SUMMARY_BEGIN_TIME` 和 `SUMMARY_END_TIME` 表示历史时间范围的起始时间和结束时间。

## `statements_summary_evicted`

[`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40) 系统变量限制了 `statements_summary` 和 `statements_summary_history` 表在内存中存储的 SQL digest 数量。一旦超出此限制，TiDB 会从 `statements_summary` 和 `statements_summary_history` 表中逐出最少使用的 SQL digest。

<CustomContent platform="tidb">

> **Note:**
>
> 当 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary) 被启用时，`statements_summary_history` 表中的数据会持久化到磁盘。在这种情况下，`tidb_stmt_summary_max_stmt_count` 仅限制 `statements_summary` 表在内存中的存储数量，TiDB 只会从 `statements_summary` 表中逐出最少使用的 SQL digest。

</CustomContent>

`statements_summary_evicted` 表记录了逐出发生的时间段以及在此期间被逐出的 SQL digest 数量。此表有助于你评估 `tidb_stmt_summary_max_stmt_count` 是否合理配置。如果该表中有记录，说明在某个时间点 SQL digest 数量超出了限制。

<CustomContent platform="tidb">

在 [TiDB Dashboard 的 SQL 语句页面](/dashboard/dashboard-statement-list.md#others)，逐出语句的信息会显示在 `Others` 行。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [诊断页面的 SQL 语句标签](/tidb-cloud/tune-performance.md#statement-analysis)，逐出语句的信息会显示在 `Others` 行。

</CustomContent>

## 语句摘要的 `cluster` 表

`statements_summary`、`statements_summary_history` 和 `statements_summary_evicted` 表只显示单个 TiDB 服务器的语句摘要。若要查询整个集群的数据，需要查询 `cluster_statements_summary`、`cluster_statements_summary_history` 或 `cluster_statements_summary_evicted` 表。

`cluster_statements_summary` 展示每个 TiDB 服务器的 `statements_summary` 数据。`cluster_statements_summary_history` 展示每个 TiDB 服务器的 `statements_summary_history` 数据。`cluster_statements_summary_evicted` 展示每个 TiDB 服务器的 `statements_summary_evicted` 数据。这些表使用 `INSTANCE` 字段表示 TiDB 服务器的地址，其他字段与 `statements_summary`、`statements_summary_history` 和 `statements_summary_evicted` 相同。

## 参数配置

以下系统变量用于控制语句摘要：

- `tidb_enable_stmt_summary`：决定是否启用语句摘要功能。`1` 表示启用，`0` 表示禁用。默认启用。禁用后，系统表中的统计会被清空；再次启用时会重新计算。测试表明启用此功能对性能影响很小。
- `tidb_stmt_summary_refresh_interval`：`statements_summary` 表的刷新间隔，单位为秒（s），默认值为 `1800`。
- `tidb_stmt_summary_history_size`：存储在 `statements_summary_history` 表中的每个 SQL 类别的最大记录数，也是 `statements_summary_evicted` 表的最大记录数，默认值为 `24`。
- `tidb_stmt_summary_max_stmt_count`：限制 `statements_summary` 和 `statements_summary_history` 表在内存中存储的 SQL digest 数量。默认值为 `3000`。

    超出此限制后，TiDB 会从两个表中逐出最少使用的 SQL digest。这些逐出记录会计入 [`statements_summary_evicted`](#statements_summary_evicted)。

    > **Note:**
    >
    > - 当 SQL digest 被逐出时，其所有时间范围的相关摘要数据会从 `statements_summary` 和 `statements_summary_history` 表中移除。因此，即使某个时间范围内的 SQL digest 数量未超出限制，`statements_summary_history` 表中的实际 SQL digest 数量也可能少于实际值。如果此情况影响性能，建议增加 `tidb_stmt_summary_max_stmt_count` 的值。
    > - 对于 TiDB 自托管版本，当 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary) 被启用时，`statements_summary_history` 表中的数据会持久化到磁盘。在这种情况下，`tidb_stmt_summary_max_stmt_count` 仅限制 `statements_summary` 表在内存中的存储数量，TiDB 只会从 `statements_summary` 表中逐出最少使用的 SQL digest。

- `tidb_stmt_summary_max_sql_length`：指定 `DIGEST_TEXT` 和 `QUERY_SAMPLE_TEXT` 的最大显示长度，默认值为 `4096`。
- `tidb_stmt_summary_internal_query`：决定是否统计 TiDB SQL 语句。`1` 表示统计，`0` 表示不统计，默认值为 `0`。

示例配置如下：

```sql
set global tidb_stmt_summary_max_stmt_count = 3000;
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

配置生效后，`statements_summary` 表每 30 分钟清理一次，`statements_summary_history` 表最多存储 3000 种 SQL 语句。每种类型的 SQL，`statements_summary_history` 会存储最近 24 个时间段的数据。`statements_summary_evicted` 记录最近 24 个被逐出的时间段。`statements_summary_evicted` 每 30 分钟更新一次。

> **Note:**
>
> - 如果某个 SQL 类型每分钟出现一次，`statements_summary_history` 会存储最近 12 小时的数据；如果每天 00:00 到 00:30 之间出现一次，`statements_summary_history` 会存储最近 24 个周期（每天一个周期），每个周期为 1 天。因此，`statements_summary_history` 会存储该 SQL 类型最近 24 天的数据。
> - `tidb_stmt_summary_history_size`、`tidb_stmt_summary_max_stmt_count` 和 `tidb_stmt_summary_max_sql_length` 配置项会影响内存使用。建议根据实际需求、SQL 大小、SQL 数量和机器配置调整，避免设置过大。可以通过 `tidb_stmt_summary_history_size` \* `tidb_stmt_summary_max_stmt_count` \* `tidb_stmt_summary_max_sql_length` \* `3` 估算内存用量。

### 设置合理的语句摘要大小

系统运行一段时间后（根据系统负载而定），可以检查 `statement_summary` 表，确认是否发生了 SQL 逐出。例如：

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

可以看到，`statements_summary` 表已满。接着检查 `statements_summary_evicted` 表中的逐出数据：

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

从结果可以看出，最多有 59 个 SQL 类别被逐出。建议将 `statements_summary` 表的大小至少增加到 3059 条记录，以容纳这些逐出类别。

## 限制

默认情况下，语句摘要表存储在内存中。重启 TiDB 服务器后，所有数据会丢失。

<CustomContent platform="tidb">

为解决此问题，TiDB 在 v6.6.0 版本中试验性引入了 [statement summary persistence](#persist-statements-summary) 功能，默认关闭。启用后，历史数据不再存储在内存中，而是直接写入磁盘。这样，即使重启 TiDB 服务器，历史数据依然可用。

</CustomContent>

## 持久化语句摘要

<CustomContent platform="tidb-cloud">

此部分仅适用于 TiDB 自托管版本。对于 TiDB Cloud，`tidb_stmt_summary_enable_persistent` 参数的默认值为 `false`，且不支持动态修改。

</CustomContent>

> **Warning:**
>
> Statements summary persistence 是一个实验性功能，不建议在生产环境中使用。此功能可能会在未提前通知的情况下被更改或移除。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb)。

<CustomContent platform="tidb">

如 [限制](#limitation) 部分所述，语句摘要表默认存储在内存中。重启 TiDB 后，所有语句摘要会丢失。从 v6.6.0 开始，TiDB 试验性提供了配置项 [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)，允许用户启用或禁用语句摘要持久化。

</CustomContent>

<CustomContent platform="tidb-cloud">

如 [限制](#limitation) 部分所述，语句摘要表默认存储在内存中。重启 TiDB 后，所有语句摘要会丢失。从 v6.6.0 开始，TiDB 试验性提供了配置项 `tidb_stmt_summary_enable_persistent`，允许用户启用或禁用语句摘要持久化。

</CustomContent>

要启用语句摘要持久化，可以在 TiDB 配置文件中添加如下配置项：

```toml
[instance]
tidb_stmt_summary_enable_persistent = true
# 以下条目使用默认值，可根据需要修改。
# tidb_stmt_summary_filename = "tidb-statements.log"
# tidb_stmt_summary_file_max_days = 3
# tidb_stmt_summary_file_max_size = 64 # MiB
# tidb_stmt_summary_file_max_backups = 0
```

启用后，内存中只保存当前的实时数据，不存储历史数据。当实时数据刷新为历史数据时，会在 `tidb_stmt_summary_refresh_interval`（详见参数配置部分）间隔内将历史数据写入磁盘。查询 `statements_summary_history` 或 `cluster_statements_summary_history` 表时，会返回内存和磁盘中合并的结果。

<CustomContent platform="tidb">

> **Note:**
>
> - 启用语句摘要持久化后，`tidb_stmt_summary_history_size` 配置将不再生效，因为内存不存储历史数据。取而代之的，是以下三个配置，用于控制持久化的历史数据的保留时间和大小：[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660)、[`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) 和 [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)。
> - `tidb_stmt_summary_refresh_interval` 越小，数据写入磁盘越及时，但也意味着写入的冗余数据更多。

</CustomContent>

## 排查示例

本节提供两个示例，演示如何利用语句摘要功能排查 SQL 性能问题。

### 高 SQL 延迟可能由服务器端引起吗？

在此示例中，客户端表现出对 `employee` 表的点查询较慢。你可以对 SQL 文本进行模糊搜索：

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary
    WHERE digest_text LIKE 'select * from employee%';
```

`1ms` 和 `0.3ms` 被认为在 `avg_latency` 的正常范围内。因此，可以判断服务器端不是原因。可以从客户端或网络方面排查。

```sql
+-------------+------------+------------------------------------------+
| avg_latency | exec_count | query_sample_text                        |
+-------------+------------+------------------------------------------+
|     1042040 |          2 | select * from employee where name='eric' |
|      345053 |          3 | select * from employee where id=3100     |
+-------------+------------+------------------------------------------+
2 rows in set (0.00 sec)
```

### 哪些类别的 SQL 语句耗时最长？

如果在 10:00 到 10:30 之间 QPS 明显下降，可以从历史表中找出耗时最长的三个 SQL 类别：

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary_history
    WHERE summary_begin_time='2020-01-02 10:00:00'
    ORDER BY sum_latency DESC LIMIT 3;
```

结果显示，以下三个类别的 SQL 语句总耗时最长，优先级较高，需重点优化：

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

以下为 `statements_summary` 表中字段的说明。

基础字段：

- `STMT_TYPE`: SQL 语句类型。
- `SCHEMA_NAME`: 当前执行该类别 SQL 语句的 schema。
- `DIGEST`: 该类别 SQL 语句的 digest。
- `DIGEST_TEXT`: 规范化的 SQL 语句。
- `QUERY_SAMPLE_TEXT`: 该类别 SQL 语句的原始 SQL，只取一个。
- `TABLE_NAMES`: SQL 语句涉及的所有表，多个用逗号分隔。
- `INDEX_NAMES`: SQL 语句使用的所有索引，多个用逗号分隔。
- `SAMPLE_USER`: 执行该类别 SQL 语句的用户，只取一个。
- `PLAN_DIGEST`: 执行计划的 digest。
- `PLAN`: 原始执行计划，若有多个语句，只取其中一个的计划。
- `BINARY_PLAN`: 编码为二进制的原始执行计划，若有多个语句，只取其中一个的计划。执行 [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan) 解析具体执行计划。
- `PLAN_CACHE_HITS`: 该类别 SQL 语句命中计划缓存的总次数。
- `PLAN_IN_CACHE`: 表示上次执行该类别 SQL 语句是否命中计划缓存。
- `PLAN_CACHE_UNQUALIFIED`: 未命中计划缓存的次数。
- `PLAN_CACHE_UNQUALIFIED_LAST_REASON`: 上次未命中计划缓存的原因。

与执行时间相关字段：

- `SUMMARY_BEGIN_TIME`: 当前统计周期的起始时间。
- `SUMMARY_END_TIME`: 当前统计周期的结束时间。
- `FIRST_SEEN`: 该类别 SQL 第一次出现的时间。
- `LAST_SEEN`: 该类别 SQL 最后一次出现的时间。

<CustomContent platform="tidb">

与 TiDB 服务器相关的字段：

- `EXEC_COUNT`: 该类别 SQL 的总执行次数。
- `SUM_ERRORS`: 执行过程中发生的错误总数。
- `SUM_WARNINGS`: 执行过程中发生的警告总数。
- `SUM_LATENCY`: 该类别 SQL 的总执行延迟。
- `MAX_LATENCY`: 该类别 SQL 的最大执行延迟。
- `MIN_LATENCY`: 该类别 SQL 的最小执行延迟。
- `AVG_LATENCY`: 该类别 SQL 的平均执行延迟。
- `AVG_PARSE_LATENCY`: 解析器的平均延迟。
- `MAX_PARSE_LATENCY`: 解析器的最大延迟。
- `AVG_COMPILE_LATENCY`: 编译器的平均延迟。
- `MAX_COMPILE_LATENCY`: 编译器的最大延迟。
- `AVG_MEM`: 平均使用的内存（字节）。
- `MAX_MEM`: 最大使用的内存（字节）。
- `AVG_DISK`: 平均使用的磁盘空间（字节）。
- `MAX_DISK`: 最大使用的磁盘空间（字节）。
- `AVG_TIDB_CPU_TIME`: 该类别 SQL 消耗的 TiDB 服务器 CPU 时间的平均值。仅在启用 [Top SQL](/dashboard/top-sql.md) 功能时有意义，否则始终为 `0`。

</CustomContent>

<CustomContent platform="tidb-cloud">

与 TiDB 服务器相关的字段：

- `EXEC_COUNT`: 该类别 SQL 的总执行次数。
- `SUM_ERRORS`: 执行过程中发生的错误总数。
- `SUM_WARNINGS`: 执行过程中发生的警告总数。
- `SUM_LATENCY`: 该类别 SQL 的总执行延迟。
- `MAX_LATENCY`: 该类别 SQL 的最大执行延迟。
- `MIN_LATENCY`: 该类别 SQL 的最小执行延迟。
- `AVG_LATENCY`: 该类别 SQL 的平均执行延迟。
- `AVG_PARSE_LATENCY`: 解析器的平均延迟。
- `MAX_PARSE_LATENCY`: 解析器的最大延迟。
- `AVG_COMPILE_LATENCY`: 编译器的平均延迟。
- `MAX_COMPILE_LATENCY`: 编译器的最大延迟。
- `AVG_MEM`: 平均使用的内存（字节）。
- `MAX_MEM`: 最大使用的内存（字节）。
- `AVG_DISK`: 平均使用的磁盘空间（字节）。
- `MAX_DISK`: 最大使用的磁盘空间（字节）。
- `AVG_TIDB_CPU_TIME`: 该类别 SQL 消耗的 TiDB 服务器 CPU 时间的平均值。仅在启用 Top SQL 功能时有意义，否则为 `0`。

</CustomContent>

与 TiKV Coprocessor 任务相关字段：

- `SUM_COP_TASK_NUM`: 发送的 Coprocessor 请求总数。
- `MAX_COP_PROCESS_TIME`: Coprocessor 任务的最大执行时间。
- `MAX_COP_PROCESS_ADDRESS`: 执行时间最长的 Coprocessor 任务地址。
- `MAX_COP_WAIT_TIME`: Coprocessor 任务的最大等待时间。
- `MAX_COP_WAIT_ADDRESS`: 等待时间最长的 Coprocessor 任务地址。
- `AVG_PROCESS_TIME`: TiKV 中 SQL 语句的平均处理时间。
- `MAX_PROCESS_TIME`: TiKV 中 SQL 语句的最大处理时间。
- `AVG_WAIT_TIME`: TiKV 中 SQL 语句的平均等待时间。
- `MAX_WAIT_TIME`: TiKV 中 SQL 语句的最大等待时间。
- `AVG_BACKOFF_TIME`: SQL 语句遇到需要重试的错误时，重试前的平均等待时间。
- `MAX_BACKOFF_TIME`: SQL 语句遇到需要重试的错误时，重试前的最大等待时间。
- `AVG_TOTAL_KEYS`: Coprocessor 扫描的平均键数。
- `MAX_TOTAL_KEYS`: Coprocessor 扫描的最大键数。
- `AVG_PROCESSED_KEYS`: Coprocessor 处理的平均键数。与 `avg_total_keys` 比较，`avg_processed_keys` 不包括 MVCC 的旧版本。两者差异大说明存在大量旧版本。
- `MAX_PROCESSED_KEYS`: Coprocessor 处理的最大键数。
- `AVG_TIKV_CPU_TIME`: TiKV 服务器 CPU 时间的平均值。

事务相关字段：

- `AVG_PREWRITE_TIME`: 预写阶段的平均时间。
- `MAX_PREWRITE_TIME`: 预写阶段的最长时间。
- `AVG_COMMIT_TIME`: 提交阶段的平均时间。
- `MAX_COMMIT_TIME`: 提交阶段的最长时间。
- `AVG_GET_COMMIT_TS_TIME`: 获取 `commit_ts` 的平均时间。
- `MAX_GET_COMMIT_TS_TIME`: 获取 `commit_ts` 的最长时间。
- `AVG_COMMIT_BACKOFF_TIME`: 提交阶段遇到错误需要重试时，重试前的平均等待时间。
- `MAX_COMMIT_BACKOFF_TIME`: 提交阶段遇到错误需要重试时，重试前的最大等待时间。
- `AVG_RESOLVE_LOCK_TIME`: 解决事务间锁冲突的平均时间。
- `MAX_RESOLVE_LOCK_TIME`: 解决锁冲突的最长时间。
- `AVG_LOCAL_LATCH_WAIT_TIME`: 本地事务的平均等待时间。
- `MAX_LOCAL_LATCH_WAIT_TIME`: 本地事务的最大等待时间。
- `AVG_WRITE_KEYS`: 写入的平均键数。
- `MAX_WRITE_KEYS`: 写入的最大键数。
- `AVG_WRITE_SIZE`: 写入数据的平均大小（字节）。
- `MAX_WRITE_SIZE`: 写入数据的最大大小（字节）。
- `AVG_PREWRITE_REGIONS`: 预写阶段涉及的 Regions 数量平均值。
- `MAX_PREWRITE_REGIONS`: 预写阶段涉及的最大 Regions 数量。
- `AVG_TXN_RETRY`: 事务重试的平均次数。
- `MAX_TXN_RETRY`: 事务重试的最大次数。
- `SUM_BACKOFF_TIMES`: 遇到需要重试的错误时的重试总次数。
- `BACKOFF_TYPES`: 需要重试的所有错误类型及每种类型的重试次数，格式为 `type:number`，多个用逗号分隔，如 `txnLock:2,pdRPC:1`。
- `AVG_AFFECTED_ROWS`: 影响的平均行数。
- `PREV_SAMPLE_TEXT`: 当前 SQL 为 `COMMIT` 时，`PREV_SAMPLE_TEXT` 为上一个 `COMMIT` 前的语句。此时，SQL 按 digest 和 `prev_sample_text` 分组。不同 `prev_sample_text` 的 `COMMIT` 语句会分到不同的行。当当前 SQL 不是 `COMMIT` 时，`PREV_SAMPLE_TEXT` 为空字符串。

资源控制相关字段：

- `AVG_REQUEST_UNIT_WRITE`: SQL 语句消耗的写 RU 平均值。
- `MAX_REQUEST_UNIT_WRITE`: SQL 语句消耗的最大写 RU。
- `AVG_REQUEST_UNIT_READ`: SQL 语句消耗的读 RU 平均值。
- `MAX_REQUEST_UNIT_READ`: SQL 语句消耗的最大读 RU。
- `AVG_QUEUED_RC_TIME`: 执行 SQL 时等待可用 RU 的平均等待时间。
- `MAX_QUEUED_RC_TIME`: 执行 SQL 时等待可用 RU 的最大等待时间。
- `RESOURCE_GROUP`: 绑定到 SQL 语句的资源组。

### `statements_summary_evicted` 字段说明

- `BEGIN_TIME`: 记录开始时间。
- `END_TIME`: 记录结束时间。
- `EVICTED_COUNT`: 在该时间段内被逐出的 SQL 类别数。
