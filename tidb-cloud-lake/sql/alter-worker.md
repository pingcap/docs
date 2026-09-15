---
title: ALTER WORKER
summary: 使用 ALTER WORKER 修改 worker 的标签、选项或状态。
---

# ALTER WORKER

> **注意：**
>
> 于 v1.3.0 中引入。

用于修改 worker 的标签、选项或状态。

> **注意：**
>
> 此命令要求启用 cloud control。

## 语法 {#syntax}

```sql
ALTER WORKER <worker_name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER WORKER <worker_name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER WORKER <worker_name> SET <option_name> = <option_value> [ , <option_name> = <option_value> ... ]

ALTER WORKER <worker_name> UNSET <option_name> [ , <option_name> ... ]

ALTER WORKER <worker_name> SUSPEND

ALTER WORKER <worker_name> RESUME
```

## 参数 {#parameters}

| 形式 | 说明 |
|------|-------------|
| `SET TAG` | 添加或修改 worker 标签。标签值必须是字符串字面量。 |
| `UNSET TAG` | 删除一个或多个 worker 标签。 |
| `SET` | 添加或修改 worker 选项。选项名称会被规范化为小写。 |
| `UNSET` | 删除一个或多个 worker 选项。 |
| `SUSPEND` | 挂起 worker。 |
| `RESUME` | 恢复 worker。 |

## 示例 {#examples}

为 worker 设置标签：

```sql
ALTER WORKER read_env
SET TAG purpose = 'sandbox', owner = 'ci';
```

修改 worker 选项：

```sql
ALTER WORKER read_env
SET size = 'medium', auto_suspend = '600';
```

删除一个标签和一个选项：

```sql
ALTER WORKER read_env UNSET TAG owner;
ALTER WORKER read_env UNSET auto_suspend;
```

更改 worker 状态：

```sql
ALTER WORKER read_env SUSPEND;
ALTER WORKER read_env RESUME;
```

## 相关主题 {#related-topics}

- [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) - 创建 worker
- [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) - 列出 worker 及其元信息
- [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) - 删除 worker