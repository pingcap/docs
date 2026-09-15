---
title: SHOW WORKERS
summary: 使用 SHOW WORKERS 列出 worker 及其元信息。
---

# SHOW WORKERS

> **注意：**
>
> 于 v1.3.0 中引入。

列出当前租户中的 worker。

> **注意：**
>
> 此命令要求启用 cloud control。

## 语法 {#syntax}

```sql
SHOW WORKERS
```

## 输出 {#output}

`SHOW WORKERS` 返回以下列：

| 列名 | 描述 |
|--------|-------------|
| `name` | Worker 名称 |
| `tags` | JSON 格式的 Worker 标签 |
| `options` | JSON 格式的 Worker 选项 |
| `created_at` | Worker 创建时间戳 |
| `updated_at` | Worker 修改时间戳 |

## 示例 {#examples}

```sql
SHOW WORKERS;
```

示例输出：

```text
read_env,{},"{""auto_resume"":""true"",""auto_suspend"":""300"",""max_cluster_count"":""3"",""min_cluster_count"":""1"",""size"":""small""}",2026-04-23T11:40:27.942797+00:00,2026-04-23T11:40:27.942797+00:00
```

## 相关主题 {#related-topics}

- [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) - 创建 worker
- [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) - 修改 worker 的标签、选项或状态
- [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) - 删除 worker