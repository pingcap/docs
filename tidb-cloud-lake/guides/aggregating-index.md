---
title: 聚合索引
summary: 聚合索引通过预计算并存储聚合结果，显著加速分析型查询，避免在常见分析操作中扫描整张表。
---

# 聚合索引

聚合索引通过预计算并存储聚合结果，显著加速分析型查询，避免在常见分析操作中扫描整张表。

## 它解决了什么问题？ {#what-problem-does-it-solve}

大规模数据集上的分析型查询会面临显著的性能挑战：

| 问题 | 影响 | 聚合索引解决方案 |
|---------|--------|---------------------------|
| **全表扫描** | SUM、COUNT、MIN、MAX 查询需要扫描数百万行 | 直接读取预计算结果 |
| **重复计算** | 相同的聚合被反复计算 | 结果只存储一次，多次复用 |
| **仪表盘查询缓慢** | 分析仪表盘加载需要数分钟 | 常见指标可实现亚秒级响应 |
| **计算成本高** | 大量聚合负载会消耗资源 | 对缓存结果仅需极少计算 |
| **用户体验差** | 用户需要等待报表和分析结果 | 为商业智能提供即时结果 |

**示例**：销售分析查询 `SELECT SUM(revenue), COUNT(*) FROM sales WHERE region = 'US'` 需要处理 1 亿行数据。没有聚合索引时，它需要扫描所有美国销售记录；有了聚合索引后，它可以立即返回预计算结果。

## 工作原理 {#how-it-works}

1. **创建索引** → 定义需要预计算的聚合查询
2. **结果存储** → {{{ .lake }}} 将聚合结果存储在优化后的数据块中
3. **查询匹配** → 传入的查询会自动使用预计算结果
4. **自动修改** → 当底层数据发生变化时，结果会刷新

## 快速开始 {#quick-setup}

```sql
-- Create table with sample data
CREATE TABLE sales(region VARCHAR, product VARCHAR, revenue DECIMAL, quantity INT);

-- Create aggregating index for common analytics
CREATE AGGREGATING INDEX sales_summary AS
SELECT region, SUM(revenue), COUNT(*), AVG(quantity)
FROM sales
GROUP BY region;

-- Refresh the index (manual mode)
REFRESH AGGREGATING INDEX sales_summary;

-- Verify the index is used
EXPLAIN SELECT region, SUM(revenue) FROM sales GROUP BY region;
```

## 支持的操作 {#supported-operations}

| ✅ 支持 | ❌ 不支持 |
|-------------|-----------------|
| SUM、COUNT、MIN、MAX、AVG | 窗口函数 |
| GROUP BY 子句 | GROUPING SETS |
| WHERE 过滤条件 | ORDER BY、LIMIT |
| 简单聚合 | 复杂子查询 |

## 刷新策略 {#refresh-strategies}

| 策略 | 适用场景 | 配置 |
|----------|-------------|---------------|
| **自动（SYNC）** | 实时分析、小规模数据集 | `CREATE AGGREGATING INDEX ... SYNC` |
| **手动** | 大规模数据集、批处理 | `CREATE AGGREGATING INDEX ...`（默认） |
| **后台（Cloud）** | 生产负载 | 在 {{{ .lake }}} 中自动执行 |

### 自动刷新与手动刷新 {#automatic-vs-manual-refresh}

```sql
-- Automatic refresh (updates with every data change)
CREATE AGGREGATING INDEX auto_summary AS
SELECT region, SUM(revenue) FROM sales GROUP BY region SYNC;

-- Manual refresh (update on demand)
CREATE AGGREGATING INDEX manual_summary AS
SELECT region, SUM(revenue) FROM sales GROUP BY region;

REFRESH AGGREGATING INDEX manual_summary;
```

## 性能示例 {#performance-example}

以下示例展示了显著的性能提升：

```sql
-- Prepare data
CREATE TABLE agg(a int, b int, c int);
INSERT INTO agg VALUES (1,1,4), (1,2,1), (1,2,4), (2,2,5);

-- Create an aggregating index
CREATE AGGREGATING INDEX my_agg_index AS SELECT MIN(a), MAX(c) FROM agg;

-- Refresh the aggregating index
REFRESH AGGREGATING INDEX my_agg_index;

-- Verify if the aggregating index works
EXPLAIN SELECT MIN(a), MAX(c) FROM agg;

-- Key indicators in the execution plan:
-- ├── aggregating index: [SELECT MIN(a), MAX(c) FROM default.agg]
-- ├── rewritten query: [selection: [index_col_0 (#0), index_col_1 (#1)]]
-- This shows the query uses precomputed results instead of scanning raw data
```

## 最佳实践 {#best-practices}

| 实践 | 收益 |
|----------|---------|
| **为常见查询建立索引** | 聚焦于频繁执行的分析查询 |
| **使用手动刷新** | 更好地控制修改时机 |
| **监控索引使用情况** | 使用 EXPLAIN 验证索引是否被利用 |
| **清理未使用的索引** | 删除未被使用的索引 |
| **匹配查询模式** | 索引过滤条件应与实际查询一致 |

## 管理命令 {#management-commands}

| 命令 | 用途 |
|---------|---------|
| `CREATE AGGREGATING INDEX` | 创建新的聚合索引 |
| `REFRESH AGGREGATING INDEX` | 使用最新数据修改索引 |
| `DROP AGGREGATING INDEX` | 删除索引（使用 VACUUM TABLE 清理存储） |
| `SHOW AGGREGATING INDEXES` | 列出所有索引 |

## 重要说明 {#important-notes}

**适合使用聚合索引的场景：**

- 频繁的分析型查询（仪表盘、报表）
- 具有重复聚合的大规模数据集
- 稳定的查询模式
- 对性能要求高的应用

**不适合使用的场景：**

- 数据频繁变化
- 一次性的分析型查询
- 小表上的简单查询

## 配置 {#configuration}

```sql
-- Enable/disable aggregating index feature
SET enable_aggregating_index_scan = 1;  -- Enable (default)
SET enable_aggregating_index_scan = 0;  -- Disable
```

---

*聚合索引最适用于大规模数据集上的重复性分析负载。建议从最常用的仪表盘和报表查询开始。*