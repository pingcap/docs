---
title: QUERY_HISTORY
summary: 获取查询执行日志，用于分析和监控。
---

# QUERY_HISTORY

获取查询执行日志，用于分析和监控。

## 语法 {#syntax}

```sql
QUERY_HISTORY
    [ BY WAREHOUSE <warehouse_name> ]
    [ FROM '<timestamp>' ]
    [ TO '<timestamp>' ]
    [ LIMIT <unsigned_integer> ]
```

| 参数 | 描述 |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `BY WAREHOUSE` | 可选。将日志过滤到特定的计算集群 (Warehouse)。空名称会报错。 |
| `FROM`         | 可选。查询范围的开始时间戳。格式：`YYYY-MM-DD HH:MM:SS`（UTC 或显式时区）。默认值为 `TO` 之前 1 小时。 |
| `TO`           | 可选。查询范围的结束时间戳。格式：`YYYY-MM-DD HH:MM:SS`（UTC 或显式时区）。默认值为当前时间。 |
| `LIMIT`        | 可选。返回的最大记录数。默认值为 `10`。必须为正整数。 |

## 输出列 {#output-columns}

结果包含以下列，例如：

| 列名 | 描述 |
| ------------ | ------------------------------------- |
| `query_id`   | 查询的唯一标识符 |
| `query_text` | 已执行的 SQL 语句 |
| `scan_bytes` | 扫描的数据量 |
| ...          | 其他查询指标和元信息 |

## 示例 {#examples}

获取特定计算集群的最近查询历史：

```sql
QUERY_HISTORY
    BY WAREHOUSE 'etl-wh'
    FROM '2023-08-20 00:00:00'
    TO '2023-08-20 06:00:00'
    LIMIT 200;
```

获取所有计算集群中的最近 10 条查询：

```sql
QUERY_HISTORY;
```

获取带有自定义限制的查询历史：

```sql
QUERY_HISTORY LIMIT 50;
```