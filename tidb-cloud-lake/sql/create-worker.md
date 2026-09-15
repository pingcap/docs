---
title: CREATE WORKER
summary: 使用可选的键值选项列表创建一个 worker。
---

# CREATE WORKER

> **注意：**
>
> 于 v1.3.0 中引入。

创建一个 worker。

> **注意：**
>
> 此命令要求启用 cloud control。

## 语法 {#syntax}

```sql
CREATE WORKER [ IF NOT EXISTS ] <worker_name>
    [ WITH <option_name> = <option_value> [ , <option_name> = <option_value> ... ] ]
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `IF NOT EXISTS` | 可选。如果 worker 已存在，则成功返回且不做任何更改。 |
| `<worker_name>` | worker 名称。 |
| `<option_name>` | worker 选项键。 |
| `<option_value>` | worker 选项值。 |

## 选项 {#options}

{{{ .lake }}} 接受单个 `WITH` 子句，后跟一个以逗号分隔的选项列表。常见的 worker 选项包括：

| 选项 | 示例值 | 描述 |
|--------|---------------|-------------|
| `size` | `'small'` | 控制 worker 的计算规模。 |
| `auto_suspend` | `'300'` | 自动挂起前的空闲超时时间。 |
| `auto_resume` | `'true'` | 控制 worker 是否自动恢复。 |
| `max_cluster_count` | `'3'` | 自动扩缩容集群数量的上限。 |
| `min_cluster_count` | `'1'` | 自动扩缩容集群数量的下限。 |

- `WITH` 最多只能出现一次。
- 选项之间使用逗号分隔。
- 在发送请求之前，选项名称会被规范化为小写。
- `option_value` 可以写为字符串字面量、裸标识符、无符号整数或布尔值。
- `CREATE WORKER` 不支持 `TAG` 子句。

## 示例 {#examples}

创建一个不带选项的 worker：

```sql
CREATE WORKER read_env;
```

使用 `IF NOT EXISTS` 创建一个 worker：

```sql
CREATE WORKER IF NOT EXISTS read_env;
```

使用自定义选项创建一个 worker：

```sql
CREATE WORKER IF NOT EXISTS read_env
WITH size = 'small',
     auto_suspend = '300',
     auto_resume = 'true',
     max_cluster_count = '3',
     min_cluster_count = '1';
```

## 相关主题 {#related-topics}

- [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) - 修改 worker 的标签、选项或状态
- [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) - 列出 workers 及其元信息
- [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) - 删除一个 worker