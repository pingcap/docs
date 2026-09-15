---
title: ALTER WORKLOAD GROUP
summary: 使用指定的配额设置修改 workload group。
---

# ALTER WORKLOAD GROUP

使用指定的配额设置修改 workload group。

## 语法 {#syntax}

```sql
ALTER WORKLOAD GROUP <group_name>
[SET cpu_quota = '<percentage>', query_timeout = '<duration>']
```

## 参数 {#parameters}

| 参数                   | 类型     | 必填 | 默认值       | 描述 |
|------------------------|----------|----------|--------------|-----------------------------------------------------------------------------|
| `cpu_quota`            | string   | 否       | （无限制）   | 以百分比字符串表示的 CPU 资源配额（例如 `"20%"`） |
| `query_timeout`        | duration | 否       | （无限制）   | 查询超时时长（单位：`s`/`sec`=秒，`m`/`min`=分钟，`h`/`hour`=小时，`d`/`day`=天，`ms`=毫秒，无单位=秒） |
| `memory_quota`         | string or integer   | 否       | （无限制）   | 工作负载组的最大内存使用限制（百分比或绝对值） |
| `max_concurrency`      | integer  | 否       | （无限制）   | 工作负载组的最大并发数 |
| `query_queued_timeout` | duration | 否       | （无限制）   | 当工作负载组超过最大并发数时，排队等待的最长时间（单位：`s`/`sec`=秒，`m`/`min`=分钟，`h`/`hour`=小时，`d`/`day`=天，`ms`=毫秒，无单位=秒） |

## 示例 {#examples}

```sql
ALTER WORKLOAD GROUP analytics SET cpu_quota = '20%', query_timeout = '10m';
```