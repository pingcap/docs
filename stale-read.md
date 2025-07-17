---
title: Stale Read 的使用场景
summary: 了解 Stale Read 及其使用场景。
---

# Stale Read 的使用场景

本文档描述了 Stale Read 的使用场景。Stale Read 是 TiDB 应用的一种机制，用于读取存储在 TiDB 中的历史版本数据。通过该机制，你可以读取某一特定时间点或在指定时间范围内的对应历史数据，从而节省存储节点之间数据复制带来的延迟。

在使用 Stale Read 时，TiDB 会随机选择一个副本进行数据读取，这意味着所有副本都可以用于数据读取。如果你的应用不能容忍读取非实时数据，则不要使用 Stale Read；否则，从副本读取的数据可能不是写入 TiDB 的最新数据。

## 场景示例

<CustomContent platform="tidb">

+ 场景一：如果一个事务仅涉及读取操作，并且在一定程度上容忍数据的陈旧性，可以使用 Stale Read 获取历史数据。使用 Stale Read 时，TiDB 会将查询请求发送到任何副本，可能会牺牲部分实时性能，从而提高查询的吞吐量。特别是在查询小表的场景中，如果使用强一致性读取，可能会导致领导节点集中在某个存储节点上，造成查询压力集中，从而成为整个查询的瓶颈。而 Stale Read 可以提升整体查询吞吐量，显著改善查询性能。

+ 场景二：在某些地理分布式部署的场景中，如果使用强一致性跟随者读取，为确保从跟随者读取的数据与领导者存储的数据一致，TiDB 会向不同的数据中心请求 `Readindex` 进行验证，这会增加整个查询过程的访问延迟。使用 Stale Read 时，TiDB 会访问当前数据中心的副本以读取对应数据，可能会牺牲部分实时性能，从而避免跨中心连接带来的网络延迟，降低整个查询的访问延迟。更多信息请参见 [Three-Data-Center Deployment 的本地读取最佳实践](/best-practices/three-dc-local-read.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果一个事务仅涉及读取操作，并且在一定程度上容忍数据的陈旧性，可以使用 Stale Read 获取历史数据。使用 Stale Read 时，TiDB 会将查询请求发送到任何副本，可能会牺牲部分实时性能，从而提高查询的吞吐量。特别是在查询小表的场景中，如果使用强一致性读取，可能会导致领导节点集中在某个存储节点上，造成查询压力集中，从而成为整个查询的瓶颈。而 Stale Read 可以提升整体查询吞吐量，显著改善查询性能。

</CustomContent>

## 使用方式

TiDB 提供在语句级、会话级和全局级别执行 Stale Read 的方法，具体如下：

- 语句级
    - 指定精确时间点（**推荐**）：如果你需要 TiDB 从某一特定时间点读取全局一致的数据，且不违反隔离级别，可以在查询语句中指定该时间点的对应时间戳。详细用法请参见 [`AS OF TIMESTAMP` clause](/as-of-timestamp.md#syntax)。
    - 指定时间范围：如果你需要 TiDB 在不违反隔离级别的前提下，读取时间范围内尽可能新的数据，可以在查询语句中指定时间范围。在指定的时间范围内，TiDB 会选择一个合适的时间戳读取对应的数据。“合适”意味着在该时间戳之前没有开始但尚未提交的事务，即 TiDB 可以在访问的副本上执行读取操作，且读取操作不会被阻塞。详细用法请参考 [`AS OF TIMESTAMP` Clause](/as-of-timestamp.md#syntax) 和 [`TIDB_BOUNDED_STALENESS` function](/as-of-timestamp.md#syntax) 的介绍。
- 会话级
    - 指定时间范围：在一个会话中，如果你希望在后续查询中，TiDB 在不违反隔离级别的前提下，读取时间范围内尽可能新的数据，可以通过设置 `tidb_read_staleness` 系统变量来指定时间范围。详细用法请参见 [`tidb_read_staleness`](/tidb-read-staleness.md)。

此外，TiDB 还提供通过设置 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640) 和 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640) 系统变量，在会话或全局级别指定精确时间点的方式。详细用法请参见 [使用 `tidb_external_ts` 执行 Stale Read](/tidb-external-ts.md)。

### 降低 Stale Read 延迟

Stale Read 功能会周期性地推进 TiDB 集群的 Resolved TS 时间戳，确保 TiDB 读取符合事务一致性的数据。如果 Stale Read 使用的时间戳（例如，`AS OF TIMESTAMP '2016-10-08 16:45:26'`）大于 Resolved TS，Stale Read 会触发 TiDB 先推进 Resolved TS 并等待推进完成后再读取数据，从而导致延迟增加。

为了降低 Stale Read 的延迟，你可以修改以下 TiKV 配置项，使 TiDB 更频繁地推进 Resolved TS 时间戳：

```toml
[resolved-ts]
advance-ts-interval = "20s" # 默认值为 "20s"。你可以将其设置为更小的值，例如 "1s"，以更频繁地推进 Resolved TS。
```

> **Note:**
>
> 减小上述 TiKV 配置项会导致 TiKV CPU 使用率和节点间流量增加。

<CustomContent platform="tidb">

关于 Resolved TS 的内部原理和诊断技术的更多信息，请参见 [理解 TiKV 中的 Stale Read 和 safe-ts](/troubleshoot-stale-read.md)。

</CustomContent>

## 限制

当对某个表的 Stale Read 查询被下推到 TiFlash 时，如果该表在查询指定的读取时间戳之后执行了更新的 DDL 操作，查询将返回错误。这是因为 TiFlash 只支持读取具有最新 schema 的数据。

以以下表为例：

```sql
create table t1(id int);
alter table t1 set tiflash replica 1;
```

在一分钟后执行以下 DDL 操作：

```sql
alter table t1 add column c1 int not null;
```

然后，使用 Stale Read 查询一分钟前的数据：

```sql
set @@session.tidb_enforce_mpp=1;
select * from t1 as of timestamp NOW() - INTERVAL 1 minute;
```

TiFlash 会返回如下错误：

```
ERROR 1105 (HY000): other error for mpp stream: From MPP<query:<query_ts:1673950975508472943, local_query_id:18, server_id:111947, start_ts:438816196526080000>,task_id:1>: Code: 0, e.displayText() = DB::TiFlashException: Table 323 schema version 104 newer than query schema version 100, e.what() = DB::TiFlashException,
```

为了避免此错误，你可以将 Stale Read 指定的读取时间戳更改为 DDL 操作之后的时间。