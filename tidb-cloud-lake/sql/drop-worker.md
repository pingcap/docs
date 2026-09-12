---
title: DROP WORKER
summary: 使用 DROP WORKER 移除 worker。
---

# DROP WORKER

> **注意：**
>
> 于 v1.3.0 中引入。

移除一个 worker。

> **注意：**
>
> 此命令要求启用 cloud control。

## 语法 {#syntax}

```sql
DROP WORKER [ IF EXISTS ] <worker_name>
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `IF EXISTS` | 可选。如果 worker 不存在，则抑制报错。 |
| `<worker_name>` | worker 名称。 |

## 示例 {#examples}

```sql
DROP WORKER read_env;
```

```sql
DROP WORKER IF EXISTS read_env;
```

## 相关主题 {#related-topics}

- [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) - 创建 worker
- [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) - 修改 worker 的标签、选项或状态
- [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) - 列出 workers 及其元信息