---
title: TiDB Cloud Lake 优化器如何工作
summary: "{{{ .lake }}} 的查询优化器会协调一系列转换，将 SQL 文本变为可执行计划。优化器会构建查询的抽象表示，并结合实时统计信息，应用基于规则的重写，探索不同的连接方案，最终选择成本最低的物理运算符。"
---

# TiDB Cloud Lake 优化器如何工作

{{{ .lake }}} 的查询优化器会协调一系列转换，将 SQL 文本变为可执行计划。优化器会构建查询的抽象表示，并结合实时统计信息，应用基于规则的重写，探索不同的连接方案，最终选择成本最低的物理运算符。

同一套优化器流水线支撑分析报表、JSON 搜索、向量检索和地理空间搜索——**{{{ .lake }}} 维护着一个能够理解其存储的所有数据类型的统一优化器。**

## 是什么让 {{{ .lake }}} 的优化器高效运转 {#what-makes-lake-s-optimizer-tick}

- 统计信息会自动保持最新：写入数据时，{{{ .lake }}} 会立即维护行数、值范围和 NDV，因此优化器无需任何手动维护，就能使用最新信息进行选择率估算、连接顺序决策和成本计算。
- 先处理形态，再计算成本：在进行全局搜索之前，这条流水线会先做去相关、谓词/限制下推以及聚合拆分，从而缩小搜索空间，并将更多工作下推到存储层。
- DP + Cascades 协同工作：DPhpy 用于寻找较优的连接顺序；基于 memo 的 Cascades 阶段则在同一个 SExpr memo 上选择成本最低的物理运算符。
- 从设计上就感知分布式：规划阶段会决定采用本地执行还是分布式执行，并将广播重写为基于键的 shuffle，以避免热点。

## 示例查询 {#example-query}

我们将使用下面这条分析查询，并展示每个 stage 如何对其进行转换。

```sql
WITH recent_orders AS (
  SELECT *
  FROM orders
  WHERE order_date >= DATE_TRUNC('month', today()) - INTERVAL '3' MONTH
    AND fulfillment_status <> 'CANCELLED'
)
SELECT c.region,
       COUNT(*) AS order_count,
       COUNT(o.id) AS row_count,
       COUNT(DISTINCT o.product_id) AS product_count,
       MIN(o.total_amount) AS min_amount,
       AVG(o.total_amount) AS avg_amount
FROM recent_orders o
JOIN customers c ON o.customer_id = c.id
LEFT JOIN products p ON o.product_id = p.id
WHERE c.status = 'ACTIVE'
  AND o.total_amount > 0
  AND p.is_active = TRUE
  AND EXISTS (
        SELECT 1
        FROM support_tickets t
        WHERE t.customer_id = c.id
          AND t.created_at > DATE_TRUNC('month', today()) - INTERVAL '1' MONTH
      )
GROUP BY c.region
HAVING COUNT(*) > 100
ORDER BY order_count DESC
LIMIT 10;
```

## 阶段 1：准备与统计信息 {#phase-1-prep-stats}

阶段 1 会让查询更易于推理，并为成本计算准备所需的数据。对于我们的示例，优化器会执行以下具体步骤：

### 1. 展平子查询 {#1-flatten-the-subquery}

将 `EXISTS (...)` 检查转换为常规连接，这样流水线的其余部分就能看到一棵统一的连接树。

```
# Before (correlated)
customers ─┐
           ├─ JOIN ─ orders
support ───┘        │
                    └─ EXISTS (references customers)

# After (semi-join)
customers ─┐
support ───┴─ SEMI JOIN ─ orders
```

等价 SQL（语义保持不变）：

```sql
FROM (
  SELECT *
  FROM orders
  WHERE order_date >= DATE_TRUNC('month', today()) - INTERVAL '3' MONTH
    AND fulfillment_status <> 'CANCELLED'
) o
JOIN customers c ON o.customer_id = c.id
LEFT JOIN products p ON o.product_id = p.id
JOIN (
  SELECT DISTINCT customer_id
  FROM support_tickets
  WHERE created_at > DATE_TRUNC('month', today()) - INTERVAL '1' MONTH
) t ON t.customer_id = c.id
```

### 2. 检查元信息捷径 {#2-check-metadata-shortcuts}

如果像 `MIN(o.total_amount)` 这样的聚合没有任何过滤条件，优化器会直接从表统计信息中获取结果，而不是扫描数据：

```
-- Conceptual replacement when no filters apply
SELECT MIN(total_amount)
FROM orders

# becomes

SELECT table_stats.min_total_amount
```

在我们的查询中存在过滤条件，因此仍然保留真实计算。

### 3. 附加统计信息 {#3-attach-statistics}

在规划期间，{{{ .lake }}} 会为被扫描的表收集行数、值范围和去重计数。SQL 本身不会发生变化，但后续的选择率估算和成本估算将保持准确，而无需任何 `ANALYZE` 作业。

### 4. 规范化聚合 {#4-normalize-aggregates}

附加统计信息后，优化器会重写可共享计数器的聚合。`COUNT(o.id)` 会变为 `COUNT(*)`，这样引擎就能为这两种用法维护同一个计数器。只有 SELECT 列表会发生变化：

```sql
SELECT c.region,
       COUNT(*)            AS order_count,
       COUNT(*)            AS row_count,      -- was COUNT(o.id)
       COUNT(DISTINCT o.product_id) AS product_count,
       MIN(o.total_amount) AS min_amount,
       AVG(o.total_amount) AS avg_amount
...
```

## 阶段 2：细化逻辑计划 {#phase-2-refine-the-logic}

阶段 2 会执行有针对性的重写，只保留真正需要的工作：

### 1. 下推过滤条件/限制 {#1-push-filters-limits-down}

```
# Before
Filter (o.total_amount > 0)
└─ Scan (recent_orders)

# After
Scan (recent_orders, pushdown_predicates=[total_amount > 0])
```

带有限制的排序也会进一步收紧：

```
# Before
Limit (10)
└─ Sort (order_count DESC)
   └─ Join (...)

# After
Sort (order_count DESC)
└─ Limit (10)
   └─ Join (...)
```

### 2. 删除冗余 {#2-drop-redundancies}

```
# Before
Filter (1 = 1 AND c.status = 'ACTIVE')
└─ ...

# After
Filter (c.status = 'ACTIVE')
└─ ...
```

### 3. 拆分聚合 {#3-split-aggregates}

```
# Before
Aggregate (COUNT/AVG)
└─ Scan (recent_orders)

# After
Aggregate (final)
└─ Aggregate (partial)
   └─ Scan (recent_orders)
```

部分聚合会尽量靠近数据执行，然后再由一个最终步骤合并结果。

### 4. 将过滤条件下推到 CTE 中 {#4-push-filters-into-the-cte}

只引用 CTE 列的谓词会被下推到 `recent_orders` 的定义内部，从而在连接之前先缩小数据规模：

```sql
WITH recent_orders AS (
  SELECT *
  FROM orders
  WHERE order_date >= DATE_TRUNC('month', today()) - INTERVAL '3' MONTH
    AND fulfillment_status <> 'CANCELLED'
    AND total_amount > 0              -- pushed from outer query
)
```

## 阶段 3：成本与物理计划 {#phase-3-cost-physical-plan}

在拥有整洁的逻辑计划和最新统计信息后，优化器会做出三个决策：

### 1. 选择连接顺序 {#1-choose-the-join-order}

由统计信息引导的动态规划程序（`DPhpyOptimizer`）会评估连接排列组合。它倾向于在较小且经过过滤的表（`customers`、`products`、`support_tickets`）上构建哈希表，而让大型事实表（`recent_orders`）对其进行探测：

```
    customers      products
           \      /
            HASH JOIN (build)
                 |
        recent_orders  (probe)
                 |
        SEMI JOIN support_tickets
```

### 2. 收紧连接语义 {#2-tighten-join-semantics}

基于规则的处理阶段会调整上面发现的连接。

#### a. 将安全的 LEFT 连接转换为 INNER 连接 {#a-turn-safe-left-joins-into-inner-joins}

我们的查询以 `LEFT JOIN products p` 开始，但谓词 `p.is_active = TRUE` 保证只保留与 product 匹配的行。优化器会将连接类型改写为：

```
# Before
recent_orders ──⊗── products   (LEFT)
            filter: p.is_active = TRUE

# After
recent_orders ──⋈── products   (INNER)
```

#### b. 删除重复谓词 {#b-drop-duplicate-predicates}

如果某个连接条件重复出现（例如 `o.customer_id = c.id` 被列出两次），`DeduplicateJoinConditionOptimizer` 只保留一份，这样执行器只需计算一次。

#### c. 按需交换连接两侧 {#c-optionally-swap-join-sides}

如果仍然启用了连接重排序，`CommuteJoin` 可以交换连接输入，从而让优化器与期望的 build/probe 方向保持一致（例如，确保较小的表构建哈希表，或匹配某种分布策略）：

```
# Before                     # After (smaller table builds)
customers ──⋈── recent_orders   recent_orders ──⋈── customers
```

### 3. 选择物理计划和分布方式 {#3-pick-the-physical-plan-and-distribution}

`CascadesOptimizer` 使用 {{{ .lake }}} 的成本模型，在哈希、归并或嵌套循环实现之间进行选择。该流水线还会决定计划是否应保持本地执行；如果有可用的计算集群 (Warehouse) 集群，且连接规模较大，则会将广播交换重写为哈希 shuffle，以便更均匀地分摊工作负载。最后的清理步骤会删除冗余的投影和未使用的 CTE。

## 可观测性 {#observability}

- `EXPLAIN` 显示最终优化后的计划。
- `EXPLAIN PIPELINE` 展示执行拓扑结构。
- `SET enable_optimizer_trace = 1` 会在查询日志中记录优化器的每一步。