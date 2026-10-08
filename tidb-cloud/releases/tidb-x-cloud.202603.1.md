---
title: TiDB-X-CLOUD.202603.1 Release Notes
summary: 了解 TiDB-X-CLOUD.202603.1 内核的功能特性。
---

# TiDB-X-CLOUD.202603.1 Release Notes

**发布日期**：2026 年 7 月 16 日

**适用的 TiDB Cloud 计划**：{{{ .essential }}} 和 {{{ .premium }}}

**TiDB X 内核版本**：`TiDB-X-CLOUD.202603.1`

从 2026 年 7 月 16 日起，新创建的 {{{ .essential }}} 和 {{{ .premium }}} 实例默认使用的内核版本为 `TiDB-X-CLOUD.202603.1`。

在 `TiDB-X-CLOUD.202603.1` 中：

- `202603` 表示该内核版本的基线代码分支创建于 2026 年 3 月，这与发布日期不同。
- `1` 表示这是基于 `TiDB-X-CLOUD.202603` 基线分支构建的第一个补丁版本。

## 功能特性 {#features}

### 性能 {#performance}

* 针对某些有损 DDL 操作（例如 `BIGINT → INT` 和 `CHAR(120) → VARCHAR(60)`）引入了显著的性能提升：在不发生数据截断的情况下，这些操作的执行时间可从数小时缩短到数分钟、数秒，甚至数毫秒，性能提升可达数十倍到数十万倍 [#63366](https://github.com/pingcap/tidb/issues/63366) @[wjhuang2016](https://github.com/wjhuang2016) @[tangenta](https://github.com/tangenta) @[fzzf678](https://github.com/fzzf678) <!-- pr: https://github.com/pingcap/tidb/pull/64834, https://github.com/pingcap/tidb/pull/64337, https://github.com/pingcap/tidb/pull/64188, https://github.com/pingcap/tidb/pull/64111, https://github.com/pingcap/tidb/pull/63465, https://github.com/pingcap/tidb/pull/63970, https://github.com/pingcap/tidb/pull/63965 -->

    优化策略如下：

    - 在严格 SQL 模式下，TiDB 会在类型转换期间预检查潜在的数据截断风险。
    - 如果未检测到数据截断风险，TiDB 仅修改元信息，并尽可能避免重建索引。
    - 如果必须重建索引，TiDB 会使用更高效的 ingest 过程，从而显著提升索引重建性能。

  下表展示了在一个包含 114 GiB 数据、6 亿行记录的表上进行基准测试时的性能提升示例。测试集群由 3 个 TiDB 节点、6 个 TiKV 节点和 1 个 PD 节点组成。所有节点均配置为 16 个 CPU 核心和 32 GiB 内存。

    | 场景 | 操作类型 | 优化前 | 优化后 | 性能提升 |
    |----------|----------------|---------------------|--------------------|--------------------------|
    | 非索引列 | `BIGINT → INT` | 2 小时 34 分钟 | 1 分 5 秒 | 快 142 倍 |
    | 索引列 | `BIGINT → INT` | 6 小时 25 分钟 | 0.05 秒 | 快 460,000 倍 |
    | 索引列 | `CHAR(120) → VARCHAR(60)` | 7 小时 16 分钟 | 12 分 56 秒 | 快 34 倍 |

    请注意，以上测试结果基于 DDL 执行期间未发生数据截断这一前提条件。该优化不适用于有符号整数型与无符号整数型之间的转换、字符集之间的转换，或带有 TiFlash 副本的表。

    更多信息，参见[文档](https://docs.pingcap.com/tidbcloud/sql-statement-modify-column/?plan=premium)。

### 可观测性 {#observability}

* 支持为慢查询定义多维度、细粒度的触发规则 [#62959](https://github.com/pingcap/tidb/issues/62959) [#64010](https://github.com/pingcap/tidb/issues/64010) @[zimulala](https://github.com/zimulala) <!-- pr: https://github.com/pingcap/tidb/pull/66132, https://github.com/pingcap/tidb/pull/66064, https://github.com/pingcap/tidb/pull/65086 -->

    在 TiDB Cloud 中，默认将执行时间超过 300 毫秒的 SQL 查询视为慢查询。你可以在 [TiDB Cloud console](https://tidbcloud.com/) 的 [**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) 页面中的 [**Slow Query**](/tidb-cloud/tune-performance.md#slow-query) 页签查看慢查询。

    TiDB Cloud 现在提供了对慢查询日志更灵活的控制方式。你可以使用 [`tidb_slow_log_rules`](https://docs.pingcap.com/tidbcloud/system-variables/?plan=premium#tidb_slow_log_rules) 系统变量，在会话和 SQL 级别基于 `Query_time`、`Digest`、`Mem_max` 和 `KV_total` 等条件定义多维度的慢查询日志输出规则。你还可以使用 `WRITE_SLOW_LOG` hint 强制为特定 SQL 语句记录慢查询日志。这使得对慢查询日志的控制更加灵活且更细粒度。

    更多信息，参见[文档](https://docs.pingcap.com/tidbcloud/config-slow-query-trigger-rules/?plan=premium)。

### SQL {#sql}

* 支持在 `FOR UPDATE OF` 子句中使用表别名 [#63035](https://github.com/pingcap/tidb/issues/63035) @[cryo-zd](https://github.com/cryo-zd) <!-- pr: https://github.com/pingcap/tidb/pull/65532 -->

    在此版本之前，当 `SELECT ... FOR UPDATE OF <table>` 语句在加锁子句中引用表别名时，TiDB 可能无法正确解析该别名，即使别名有效，也会返回 `table not exists` 错误。

    TiDB 现已支持在 `FOR UPDATE OF` 子句中使用表别名。TiDB 现在可以从 `FROM` 子句中正确解析加锁目标，包括使用别名的表，从而确保行锁按预期生效。这提升了与 MySQL 的兼容性，并使在使用表别名的查询中，`SELECT ... FOR UPDATE OF` 语句更加稳定可靠。

    更多信息，参见[文档](https://docs.pingcap.com/tidbcloud/sql-statement-select/?plan=premium)。

* 支持部分索引，以减少索引存储和 DML 维护开销 [#62664](https://github.com/pingcap/tidb/issues/62664) [#62761](https://github.com/pingcap/tidb/issues/62761) [#62758](https://github.com/pingcap/tidb/issues/62758) [#63447](https://github.com/pingcap/tidb/issues/63447) [#64344](https://github.com/pingcap/tidb/issues/64344) @[YangKeao](https://github.com/YangKeao) @[winoros](https://github.com/winoros) @[wjhuang2016](https://github.com/wjhuang2016) <!-- pr: https://github.com/pingcap/tidb/pull/64434, https://github.com/pingcap/tidb/pull/62762, https://github.com/pingcap/tidb/pull/62759, https://github.com/pingcap/tidb/pull/65051 -->

    现在，TiDB 支持部分索引，即仅为满足索引 `WHERE` 子句中定义谓词的行建立索引。你可以通过 `CREATE INDEX ... WHERE ...`、`ALTER TABLE ... ADD INDEX ... WHERE ...`，或在 `CREATE TABLE` 中定义索引来创建部分索引。

    当你经常基于特定条件查询某个子集的行，或者需要仅在特定条件下生效的唯一约束时，部分索引会非常有用。由于谓词之外的行不会写入索引，部分索引有助于减少索引存储，并可降低 `INSERT`、`UPDATE` 和 `DELETE` 操作期间的索引维护开销。

    为了有效使用部分索引，请定义与常见查询中过滤条件相匹配的谓词。只有当查询谓词与部分索引谓词匹配或可推出该谓词时，TiDB 才会选择部分索引。当前，部分索引谓词支持基础比较运算符（`=`, `!=`, `<`, `<=`, `>`, `>=`）、`IS NULL`、`IS NOT NULL` 以及带常量值的 `IN` 谓词。

    更多信息，参见[文档](https://docs.pingcap.com/tidbcloud/sql-statement-create-index/?plan=premium#partial-indexes)。

## 兼容性变更 {#compatibility-changes}

### MySQL 兼容性 {#mysql-compatibility}

* Dumpling 通过适配更新后的 MySQL binary log 命名方式，支持从 MySQL 8.4 导出数据。[#53082](https://github.com/pingcap/tidb/issues/53082) @[dveeden](https://github.com/dveeden) <!-- pr: https://github.com/pingcap/tidb/pull/66704 -->

## 改进项 {#improvements}

- 增强 Parquet 文件的解析机制，以提升 Parquet 格式数据的导入性能 [#62906](https://github.com/pingcap/tidb/issues/62906) @[joechenrh](https://github.com/joechenrh) <!-- pr: https://github.com/pingcap/tidb/pull/66564, https://github.com/pingcap/tidb/pull/63979 -->
- 将 `tidb_analyze_column_options` 的默认值改为 `ALL`，以默认收集所有列的统计信息 [#64992](https://github.com/pingcap/tidb/issues/64992) @[0xPoe](https://github.com/0xPoe) <!-- pr: https://github.com/pingcap/tidb/pull/65020, https://github.com/pingcap/tidb/pull/64994 -->
- 优化 `IndexHashJoin` 算子的执行逻辑，在特定 JOIN 场景中使用增量处理，避免一次性加载大量数据，从而显著降低内存使用并提升性能 [#63303](https://github.com/pingcap/tidb/issues/63303) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan) <!-- pr: https://github.com/pingcap/tidb/pull/63723 -->
- 新增全局系统变量 `tidb_enable_batch_query_region`，用于控制 TiDB 是否对 PD 使用批量 Region 查询，以提升获取 Region 信息的效率；该变量默认关闭 [#58439](https://github.com/pingcap/tidb/issues/58439) [#8690](https://github.com/tikv/pd/issues/8690) @[JmPotato](https://github.com/JmPotato) <!-- pr: https://github.com/tikv/pd/pull/10139, https://github.com/tikv/pd/pull/10105 -->
- 对具有大量索引的表上的查询，优化器会在代价估算前裁剪无关索引，从而提升优化器性能，减少查询规划时间，并避免不必要的全范围越界估算 [#63856](https://github.com/pingcap/tidb/issues/63856) @[terry1purcell](https://github.com/terry1purcell) @[qw4990](https://github.com/qw4990) <!-- pr: https://github.com/pingcap/tidb/pull/66304, https://github.com/pingcap/tidb/pull/65854, https://github.com/pingcap/tidb/pull/64999, https://github.com/pingcap/tidb/pull/64794, https://github.com/pingcap/tidb/pull/64675, https://github.com/pingcap/tidb/pull/64484, https://github.com/pingcap/tidb/pull/64115, https://github.com/pingcap/tidb/pull/64053, https://github.com/pingcap/tidb/pull/64086, https://github.com/pingcap/tidb/pull/64054 -->
- 支持对匹配前缀索引的 `ORDER BY ... LIMIT/OFFSET` 查询进行部分有序索引优化。当 `tidb_opt_partial_ordered_index_for_topn` 设置为 `COST` 时，TiDB 可以利用索引的部分有序性来减少全表扫描，并提升 `TOPN` 查询性能 [#63280](https://github.com/pingcap/tidb/issues/63280) [#65813](https://github.com/pingcap/tidb/issues/65813) [#66338](https://github.com/pingcap/tidb/issues/66338) @[elsa0520](https://github.com/elsa0520) @[xzhangxian1008](https://github.com/xzhangxian1008) @[winoros](https://github.com/winoros) <!-- pr: https://github.com/pingcap/tidb/pull/65314, https://github.com/pingcap/tidb/pull/66268, https://github.com/pingcap/tidb/pull/66181, https://github.com/pingcap/tidb/pull/65799, https://github.com/pingcap/tidb/pull/65533 -->
- 缓解在高分区表且使用本地索引时，`IndexLookUp` 查询产生的 Coprocessor 请求突发问题，以提升查询稳定性并减少性能抖动 [#67545](https://github.com/pingcap/tidb/issues/67545) @[gengliqi](https://github.com/gengliqi) <!-- pr: https://github.com/pingcap/tidb/pull/69334 -->
- 通过减少执行期间不必要的表达式缓冲区分配，优化 `INSERT ... ON DUPLICATE KEY UPDATE` 语句的 CPU 和内存使用 [#65003](https://github.com/pingcap/tidb/issues/65003) @[windtalker](https://github.com/windtalker) <!-- pr: https://github.com/pingcap/tidb/pull/65244 -->
- 优化时间戳推进和 Leader 选举的逻辑 [#9981](https://github.com/tikv/pd/issues/9981) @[bufferflies](https://github.com/bufferflies) <!-- pr: https://github.com/tikv/pd/pull/9986 -->