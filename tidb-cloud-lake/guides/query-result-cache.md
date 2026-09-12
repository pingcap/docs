---
title: 查询结果缓存
summary: "{{{ .lake }}} 在启用后会缓存并持久化每个已执行查询的结果。这可以显著缩短获得查询结果所需的时间。"
---

# 查询结果缓存

{{{ .lake }}} 在启用后会缓存并持久化每个已执行查询的结果。这可以显著缩短获得查询结果所需的时间。

## 缓存使用条件 {#cache-usage-conditions}

只有在**所有**条件都满足时，查询结果才会从缓存中复用：

| 条件 | 要求 |
|-----------|-------------|
| **启用缓存** | 当前会话中 `enable_query_result_cache = 1` |
| **相同查询** | 查询文本必须完全一致（大小写敏感） |
| **执行时间** | 原始查询运行时 ≥ `query_result_cache_min_execute_secs` |
| **结果大小** | 缓存结果 ≤ `query_result_cache_max_bytes` |
| **TTL 有效** | 缓存存活时间 < `query_result_cache_ttl_secs` |
| **数据一致性** | 自缓存以来表数据未发生变化（除非 `query_result_cache_allow_inconsistent = 1`） |
| **会话作用域** | 缓存仅限当前会话 |

> **注意：**
>
> 默认情况下（`query_result_cache_allow_inconsistent = 0`），当底层表数据发生变化时，缓存结果会被自动失效。这可以确保数据一致性，但在频繁修改的表上可能会降低缓存效果。

## 快速开始 {#quick-start}

在你的会话中启用查询结果缓存：

```sql
-- Enable query result cache
SET enable_query_result_cache = 1;

-- Optional: Cache all queries (including fast ones)
SET query_result_cache_min_execute_secs = 0;
```

## 配置项 {#configuration-settings}

| 设置 | 默认值 | 描述 |
|---------|---------|-------------|
| `enable_query_result_cache` | 0 | 启用/禁用查询结果缓存 |
| `query_result_cache_allow_inconsistent` | 0 | 即使底层数据已变化，也允许使用缓存结果 |
| `query_result_cache_max_bytes` | 1048576 | 单个缓存结果的最大大小（字节） |
| `query_result_cache_min_execute_secs` | 1 | 开始缓存前所需的最小执行时间 |
| `query_result_cache_ttl_secs` | 300 | 缓存过期时间（5 分钟） |

## 性能示例 {#performance-example}

本示例演示如何缓存一个 TPC-H Q1 查询：

### 1. 启用缓存 {#1-enable-caching}

```sql
SET enable_query_result_cache = 1;
SET query_result_cache_min_execute_secs = 0;
```

### 2. 第一次执行（无缓存） {#2-first-execution-no-cache}

```sql
SELECT
    l_returnflag,
    l_linestatus,
    sum(l_quantity) as sum_qty,
    sum(l_extendedprice) as sum_base_price,
    sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
    sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
    avg(l_quantity) as avg_qty,
    avg(l_extendedprice) as avg_price,
    avg(l_discount) as avg_disc,
    count(*) as count_order
FROM lineitem
WHERE l_shipdate <= add_days(to_date('1998-12-01'), -90)
GROUP BY l_returnflag, l_linestatus
ORDER BY l_returnflag, l_linestatus;
```

**结果**：4 行，耗时 **21.492 秒**（处理了 6 亿行）

### 3. 验证缓存条目 {#3-verify-cache-entry}

```sql
SELECT sql, query_id, result_size, num_rows FROM system.query_cache;
```

### 4. 第二次执行（来自缓存） {#4-second-execution-from-cache}

再次运行相同的查询。

**结果**：4 行，耗时 **0.164 秒**（处理了 0 行）

## 缓存管理 {#cache-management}

### 监控缓存使用情况 {#monitor-cache-usage}

```sql
SELECT * FROM system.query_cache;
```

### 访问缓存结果 {#access-cached-results}

```sql
SELECT * FROM RESULT_SCAN(LAST_QUERY_ID());
```

### 缓存生命周期 {#cache-lifecycle}

在以下情况下，缓存结果会被自动移除：

- **TTL 过期**（默认：5 分钟）
- **结果大小超过限制**（默认：1MB）
- **会话结束**（缓存的作用域为会话）
- **底层数据发生变化**（为保证一致性会自动失效）
- **表结构发生变化**（schema 修改会使缓存失效）

> **注意：**
>
> 查询结果缓存的作用域为会话。每个会话都会维护自己的缓存，并在会话结束时自动清理。