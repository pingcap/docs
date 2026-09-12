---
title: 查询语法
summary: 本页提供 {{{ .lake }}} 中查询语法的参考信息。每个组件都可以单独使用，也可以组合使用以构建强大的查询。
---

# 查询语法

本页提供 {{{ .lake }}} 中查询语法的参考信息。每个组件都可以单独使用，也可以组合使用以构建强大的查询。

## 核心查询组件 {#core-query-components}

| 组件 | 描述 |
|-----------|-------------|
| **[SELECT](/tidb-cloud-lake/sql/select.md)** | 从表中检索数据——所有查询的基础 |
| **[FROM / JOIN](/tidb-cloud-lake/sql/join.md)** | 指定数据源并组合多个表 |
| **[WHERE](/tidb-cloud-lake/sql/select.md#where-clause)** | 根据条件过滤行 |
| **[GROUP BY](/tidb-cloud-lake/sql/group-by.md)** | 对行进行分组并执行聚合（SUM、COUNT、AVG 等） |
| **[HAVING](/tidb-cloud-lake/sql/group-by.md)** | 过滤分组后的结果 |
| **[ORDER BY](/tidb-cloud-lake/sql/select.md#order-by-clause)** | 对查询结果进行排序 |
| **[LIMIT / TOP](/tidb-cloud-lake/sql/top.md)** | 限制返回的行数 |

## 高级功能 {#advanced-features}

| 组件 | 描述 |
|-----------|-------------|
| **[WITH (CTE)](/tidb-cloud-lake/sql/clause.md)** | 为复杂逻辑定义可复用的查询块 |
| **[PIVOT](/tidb-cloud-lake/sql/pivot.md)** | 将行转换为列（宽格式） |
| **[UNPIVOT](/tidb-cloud-lake/sql/unpivot.md)** | 将列转换为行（长格式） |
| **[QUALIFY](/tidb-cloud-lake/sql/qualify.md)** | 在窗口函数计算后过滤行 |
| **[VALUES](/tidb-cloud-lake/sql/values.md)** | 创建内联临时数据集 |

## 时间旅行与流处理 {#time-travel-streaming}

| 组件 | 描述 |
|-----------|-------------|
| **[AT](/tidb-cloud-lake/sql/at.md)** | 查询特定时间点的数据 |
| **[CHANGES](/tidb-cloud-lake/sql/changes.md)** | 跟踪插入、修改和删除 |
| **[WITH CONSUME](/tidb-cloud-lake/sql/with-consume.md)** | 通过偏移管理处理流式数据 |
| **[WITH STREAM HINTS](/tidb-cloud-lake/sql/stream-hints.md)** | 优化流处理行为 |

## 查询执行 {#query-execution}

| 组件 | 描述 |
|-----------|-------------|
| **[SETTINGS 子句](/tidb-cloud-lake/sql/settings-clause.md)** | 配置查询优化和执行参数 |

## 查询结构 {#query-structure}

一个典型的 {{{ .lake }}} 查询遵循以下结构：

```sql
[WITH cte_expressions]
SELECT [TOP n] columns
FROM table
[JOIN other_tables]
[WHERE conditions]
[GROUP BY columns]
[HAVING group_conditions]
[QUALIFY window_conditions]
[ORDER BY columns]
[LIMIT n]
```