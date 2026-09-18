---
title: 配置慢查询的触发规则
summary: 定义慢查询日志的触发规则。
---

# 配置慢查询的触发规则

<CustomContent platform="tidb">

本文介绍如何使用 [`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) 系统变量来定义[慢查询日志](/identify-slow-queries.md)的触发规则。

[`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) 支持多维度指标组合，适用于慢查询日志的“定向采样”和“问题复现”，使你能够基于特定指标组合筛选目标语句。

对于 TiDB Self-Managed，慢查询日志的触发行为取决于 `tidb_slow_log_rules` 的配置：

- 如果当前会话没有适用的 `tidb_slow_log_rules` 规则（无论是因为未设置该变量，还是因为已配置的规则均不适用于该会话），慢查询日志仍然依赖 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)（单位为毫秒）。
- 如果当前会话存在任意适用的 `tidb_slow_log_rules` 规则，慢查询日志是否输出由规则匹配结果决定，并且会忽略 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)。

</CustomContent>
<CustomContent platform="tidb-cloud">

在 [TiDB Cloud console](https://tidbcloud.com/) 中，你可以在 [**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) 页面的 [**Slow Query**](/tidb-cloud/tune-performance.md#slow-query) 页签查看慢查询。

默认情况下，执行时间超过 300 毫秒的 SQL 查询会被视为慢查询。要配置慢查询的触发规则，你可以修改 [`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) 系统变量。

[`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) 支持多维度指标组合，适用于慢查询的“定向采样”和“问题复现”，使你能够基于特定指标组合筛选目标语句。

</CustomContent>

## 示例 {#examples}

- 标准格式（`SESSION` 作用域）：

    ```sql
    SET SESSION tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

- 无效的 `SESSION` 规则（`SESSION` 作用域不支持 `Conn_ID`）：

    ```sql
    SET SESSION tidb_slow_log_rules = 'Conn_ID: 12, Query_time: 0.5, Is_internal: false';
    ```

<CustomContent platform="tidb">

- 全局规则（适用于所有连接）：

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

- 针对特定连接的全局规则（分别应用于两个连接 `Conn_ID:11` 和 `Conn_ID:12`）：

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Conn_ID: 11, Query_time: 0.5, Is_internal: false; Conn_ID: 12, Query_time: 0.6, Process_time: 0.3, DB: db1';
    ```

</CustomContent>

<CustomContent platform="tidb-cloud" plan="dedicated">

- 全局规则（适用于所有连接）：

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

- 针对特定连接的全局规则（分别应用于两个连接 `Conn_ID:11` 和 `Conn_ID:12`）：

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Conn_ID: 11, Query_time: 0.5, Is_internal: false; Conn_ID: 12, Query_time: 0.6, Process_time: 0.3, DB: db1';
    ```

</CustomContent>

## 统一规则语法和类型约束 {#unified-rule-syntax-and-type-constraints}

- 规则容量与分隔方式：每个支持的作用域最多可包含 10 条规则。规则之间使用 `;` 分隔。
- 条件格式：每个条件使用 `field_name:value` 格式。单条规则中的多个条件使用 `,` 分隔。
- 字段名不区分大小写。字段名中的下划线和其他字符会被保留。

<CustomContent platform="tidb">

TiDB Self-Managed 同时支持 `tidb_slow_log_rules` 的 `SESSION` 和 `GLOBAL` 规则。单个会话在这两个作用域中最多可以有 20 条生效规则。`SESSION` 规则不支持 `Conn_ID`；只有 `GLOBAL` 规则支持该字段。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="dedicated">

TiDB Cloud Dedicated 同时支持 `tidb_slow_log_rules` 的 `SESSION` 和 `GLOBAL` 规则。单个会话在这两个作用域中最多可以有 20 条生效规则。`SESSION` 规则不支持 `Conn_ID`；只有 `GLOBAL` 规则支持该字段。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="essential,premium">

TiDB Cloud Essential 和 TiDB Cloud Premium 仅支持 `tidb_slow_log_rules` 的 `SESSION` 规则。因此，仅在 `GLOBAL` 规则中可用的 `Conn_ID` 不受支持。

</CustomContent>

- 匹配语义：
    - 除 `Conn_ID` 外的数值字段使用 `>=` 进行匹配。`Conn_ID`、字符串字段和布尔字段使用相等匹配（`=`）。
    - `DB` 和 `Resource_group` 的匹配不区分大小写。
    - 不支持显式运算符，例如 `>`、`<` 和 `!=`。

类型约束如下：

- 数值类型（`int64`、`uint64`、`float64`）要求值大于或等于 `0`。负值会导致解析错误。
    - `int64`：最大值为 `2^63-1`。
    - `uint64`：最大值为 `2^64-1`。
    - `float64`：值必须是有限且非负的。最大值约为 `1.79e308`。`NaN` 以及 `Inf`、`-Inf` 等无穷值均无效，并会导致错误。
- `bool`：支持 `true`/`false`、`1`/`0` 和 `t`/`f`（不区分大小写）。
- `string`：当前不支持包含分隔符 `,`（条件分隔符）或 `;`（规则分隔符）的字符串，即使使用引号（单引号或双引号）也不支持。不支持转义。
- 重复字段：如果同一字段在单条规则中被指定多次，则最后一次出现的值生效。

## 支持的字段 {#supported-fields}

下表中的字段遵循[统一规则语法和类型约束](#unified-rule-syntax-and-type-constraints)中描述的一般匹配和类型规则，除非另有说明。

| 字段名 | 类型 | 单位 | 描述 |
| --- | --- | --- | --- |
| `Conn_ID` | `uint` | 次数 | 连接 ID（会话 ID）。该字段使用精确匹配。例如，`Conn_ID:3` 仅匹配会话 ID 为 `3` 的日志。该字段仅在 `GLOBAL` 规则中受支持。 |
| `Session_alias` | `string` | 无 | 当前会话的别名。 |
| `DB` | `string` | 无 | 当前数据库。匹配时不区分大小写。 |
| `Exec_retry_count` | `uint` | 次数 | 该语句的重试次数。该字段通常用于悲观事务，在锁失败时语句会被重试。 |
| `Query_time` | `float` | 秒 | 语句的执行时间。 |
| `Parse_time` | `float` | 秒 | 语句的解析时间。 |
| `Compile_time` | `float` | 秒 | 查询优化的持续时间。 |
| `Rewrite_time` | `float` | 秒 | 重写该语句查询所消耗的时间。 |
| `Optimize_time` | `float` | 秒 | 优化执行计划所消耗的时间。 |
| `Wait_TS` | `float` | 秒 | 语句获取事务时间戳的等待时间。 |
| `Is_internal` | `bool` | 无 | SQL 语句是否为 TiDB 内部语句。`true` 表示该语句在 TiDB 内部执行，`false` 表示该语句由用户执行。 |
| `Digest` | `string` | 无 | SQL 语句的指纹。 |
| `Plan_digest` | `string` | 无 | 执行计划的摘要。 |
| `Num_cop_tasks` | `int` | 次数 | 该语句发送的 Coprocessor 任务数。 |
| `Mem_max` | `int` | bytes | SQL 语句执行期间使用的最大内存空间。 |
| `Disk_max` | `int` | bytes | SQL 语句执行期间使用的最大磁盘空间。 |
| `Write_sql_response_total` | `float` | 秒 | 该语句将结果返回给客户端所消耗的时间。 |
| `Succ` | `bool` | 无 | 语句是否执行成功。 |
| `Resource_group` | `string` | 无 | 该语句绑定的资源组。匹配时不区分大小写。 |
| `KV_total` | `float` | 秒 | 该语句发送到 TiKV 或 TiFlash 的所有 RPC 请求所花费的时间。 |
| `PD_total` | `float` | 秒 | 该语句发送到 PD 的所有 RPC 请求所花费的时间。 |
| `Process_time` | `float` | 秒 | SQL 语句在 TiKV 中的总处理时间。由于数据会并发发送到 TiKV，该值可能超过 `Query_time`。 |
| `Backoff_time` | `float` | 秒 | 语句遇到需要重试的错误时，在重试前的等待时间。常见错误包括锁冲突、Region 切分以及 TiKV 服务器繁忙。 |
| `Total_keys` | `uint` | 次数 | Coprocessor 已扫描的 key 数量。 |
| `Process_keys` | `uint` | 次数 | Coprocessor 已处理的 key 数量。与 `Total_keys` 相比，`Process_keys` 不包含 MVCC 的旧版本。`Process_keys` 与 `Total_keys` 差异较大通常表示存在大量旧版本。 |
| `cop_mvcc_read_amplification` | `float` | 比率 | MVCC 读放大比率，计算方式为 `Total_keys / Process_keys`。 |
| `Prewrite_time` | `float` | 秒 | 两阶段事务提交第一阶段（prewrite）的持续时间。 |
| `Commit_time` | `float` | 秒 | 两阶段事务提交第二阶段（commit）的持续时间。 |
| `Write_keys` | `uint` | 次数 | 事务写入 TiKV 中 Write CF 的 key 数量。 |
| `Write_size` | `uint` | bytes | 事务提交时待写入的 key 或 value 的总大小。 |
| `Prewrite_region` | `uint` | 次数 | 两阶段事务提交第一阶段（prewrite）涉及的 TiKV Region 数量。每个 Region 都会触发一次远程过程调用。 |

## 生效行为与匹配顺序 {#effective-behavior-and-matching-order}

- 设置 `tidb_slow_log_rules` 会覆盖指定作用域中的现有规则，而不是追加新规则。
- 将 `tidb_slow_log_rules` 设置为空字符串会清除指定作用域中的规则。
- 多条规则之间使用 `OR` 组合，而单条规则中的多个字段条件之间使用 `AND` 组合。
- 如果你仍希望使用 SQL 执行时间作为写入慢查询日志的条件，请在规则中使用 `Query_time`，并注意其单位为秒。

<CustomContent platform="tidb">

TiDB Self-Managed 同时支持 `tidb_slow_log_rules` 的 `SESSION` 和 `GLOBAL` 规则。

- 如果当前会话存在任意适用规则，例如 `SESSION` 规则、当前 `Conn_ID` 对应的 `GLOBAL` 规则，或不带 `Conn_ID` 的通用 `GLOBAL` 规则，则慢查询日志是否输出由规则匹配结果决定，并且会忽略 `tidb_slow_log_threshold`。
- 如果当前会话没有适用规则，例如 `SESSION` 和 `GLOBAL` 规则都为空，或者仅配置了与当前 `Conn_ID` 不匹配的 `GLOBAL` 规则，则慢查询日志仍然取决于 `tidb_slow_log_threshold`。`tidb_slow_log_threshold` 的单位为毫秒。
- TiDB 会先匹配 `SESSION` 规则。如果都不匹配，再匹配当前 `Conn_ID` 对应的 `GLOBAL` 规则，最后匹配不带 `Conn_ID` 的通用 `GLOBAL` 规则。
- `SHOW VARIABLES LIKE 'tidb_slow_log_rules'` 和 `SELECT @@SESSION.tidb_slow_log_rules` 返回 `SESSION` 规则文本；如果未设置，则返回空字符串。`SELECT @@GLOBAL.tidb_slow_log_rules` 返回 `GLOBAL` 规则文本。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="dedicated">

TiDB Cloud Dedicated 同时支持 `tidb_slow_log_rules` 的 `SESSION` 和 `GLOBAL` 规则。

- 如果当前会话存在任意适用规则，例如 `SESSION` 规则、当前 `Conn_ID` 对应的 `GLOBAL` 规则，或不带 `Conn_ID` 的通用 `GLOBAL` 规则，则慢查询日志是否输出由规则匹配结果决定。
- 如果当前会话没有适用规则，例如 `SESSION` 和 `GLOBAL` 规则都为空，或者仅配置了与当前 `Conn_ID` 不匹配的 `GLOBAL` 规则，则慢查询日志规则会回退到默认规则：执行时间超过 300 毫秒的 SQL 查询会被视为慢查询。
- TiDB 会先匹配 `SESSION` 规则。如果都不匹配，再匹配当前 `Conn_ID` 对应的 `GLOBAL` 规则，最后匹配不带 `Conn_ID` 的通用 `GLOBAL` 规则。
- `SHOW VARIABLES LIKE 'tidb_slow_log_rules'` 和 `SELECT @@SESSION.tidb_slow_log_rules` 返回 `SESSION` 规则文本；如果未设置，则返回空字符串。`SELECT @@GLOBAL.tidb_slow_log_rules` 返回 `GLOBAL` 规则文本。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="essential,premium">

TiDB Cloud Essential 和 TiDB Cloud Premium 仅支持 `tidb_slow_log_rules` 的 `SESSION` 规则。

- 如果当前会话存在任意 `SESSION` 规则，则慢查询日志是否输出由规则匹配结果决定。
- `SHOW VARIABLES LIKE 'tidb_slow_log_rules'` 和 `SELECT @@SESSION.tidb_slow_log_rules` 返回 `SESSION` 规则文本；如果未设置，则返回空字符串。

</CustomContent>

## 建议 {#recommendations}

- `tidb_slow_log_rules` 旨在替代单一阈值方式。它支持多维度指标条件组合，从而能够更灵活、更细粒度地控制慢查询日志记录。

- 在资源充足的测试环境中（1 个 TiDB 节点，16 个 CPU 核心、48 GiB 内存；3 个 TiKV 节点，每个节点 16 个 CPU 核心、48 GiB 内存），重复的 sysbench 测试表明：当多维度慢查询日志规则在 30 分钟内生成数百万条慢日志记录时，性能影响仍然较小。然而，当日志量达到数千万条时，TPS 会显著下降，延时也会明显增加。因此，如果业务负载较高，或者 CPU 和内存资源已接近上限，请谨慎配置 `tidb_slow_log_rules`，以避免因规则过宽而导致日志泛滥。 <CustomContent platform="tidb">如果你需要限制日志输出速率，请使用 [`tidb_slow_log_max_per_sec`](/system-variables.md#tidb_slow_log_max_per_sec) 对其进行限流，以降低对业务性能的影响。</CustomContent>