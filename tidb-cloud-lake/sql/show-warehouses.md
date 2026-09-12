---
title: SHOW WAREHOUSES
summary: 列出当前租户可见的所有计算集群。
---

# SHOW WAREHOUSES

列出当前租户可见的所有计算集群。

## 语法 {#syntax}

```sql
SHOW WAREHOUSES [ LIKE '<pattern>' ] [ <pattern_without_like> ]
```

| 参数 | 描述 |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| `LIKE '<pattern>'`       | 可选。使用 SQL `LIKE` 语义过滤计算集群名称（`%` 匹配任意字符序列，`_` 匹配任意单个字符）。 |
| `<pattern_without_like>` | 可选。当省略 `LIKE` 但后面跟随一个字面量时，该字面量会被视为 `LIKE '<literal>'`。 |

## 输出列 {#output-columns}

| 列 | 描述 |
| ------------------- | ----------------------------------------- |
| `name`              | 计算集群名称 |
| `state`             | 当前状态（例如 Running、Suspended） |
| `size`              | 计算集群大小 |
| `auto_suspend`      | 自动挂起超时时间（秒） |
| `auto_resume`       | 是否启用自动恢复 |
| `min_cluster_count` | 自动扩缩容的最小集群数 |
| `max_cluster_count` | 自动扩缩容的最大集群数 |
| `role`              | 计算集群角色 |
| `comment`           | 用户定义的注释 |
| `tags`              | JSON 格式字符串表示的计算集群标签 |
| `created_by`        | 创建者 |
| `created_on`        | 创建时间戳 |

## 示例 {#examples}

列出所有计算集群：

```sql
SHOW WAREHOUSES;
```

列出匹配某个模式的计算集群：

```sql
SHOW WAREHOUSES LIKE '%prod%';
```

在不使用 `LIKE` 的情况下使用字面量：

```sql
SHOW WAREHOUSES 'nightly-etl';
```