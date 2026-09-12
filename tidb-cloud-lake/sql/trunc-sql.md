---
title: TRUNC
summary: 将日期或时间戳截断到指定精度。该函数遵循广泛采用的日期截断语法，使从其他数据库系统迁移的用户更容易上手。
---

# TRUNC

> **注意：**
>
> 于 v1.2.745 中引入。

将日期或时间戳截断到指定精度。该函数遵循广泛采用的日期截断语法，使从其他数据库系统迁移的用户更容易上手。

## 语法 {#syntax}

```sql
TRUNC(<date_or_timestamp>, <datetime_interval_type>)
```

| 参数                       | 描述                                                                                                       |
|----------------------------|------------------------------------------------------------------------------------------------------------|
| `<date_or_timestamp>`      | `DATE` 或 `TIMESTAMP` 类型的值。                                                                           |
| `<datetime_interval_type>` | 必须是以下值之一：`YEAR`、`QUARTER`、`MONTH`、`WEEK`、`DAY`、`HOUR`、`MINUTE`、`SECOND`。                 |

## Week Start 配置 {#week-start-configuration}

当使用 `WEEK` 作为日期时间间隔类型时，结果取决于 `week_start` 设置，该设置定义了一周的第一天：

- `week_start = 1`（默认）：将星期一视为一周的第一天
- `week_start = 0`：将星期日视为一周的第一天

你可以使用 `SETTINGS` 子句为特定查询更改此设置：

```sql
-- Set Sunday as the first day of the week
SETTINGS (week_start = 0) SELECT TRUNC(to_date('2024-04-05'), 'WEEK');

-- Set Monday as the first day of the week (default)
SETTINGS (week_start = 1) SELECT TRUNC(to_date('2024-04-05'), 'WEEK');
```

## 返回类型 {#return-type}

与 `<date_or_timestamp>` 相同。

## 示例 {#examples}

```sql
-- Truncate to different precisions
SELECT
    TRUNC(to_date('2022-07-07'), 'MONTH'),
    TRUNC(to_date('2022-07-07'), 'WEEK'),
    TRUNC(to_date('2022-07-07'), 'YEAR');

┌────────────────────────────────────────────────────────────────────────────────────┐
│ TRUNC(to_date('2022-07-07'), 'MONTH') │ TRUNC(to_date('2022-07-07'), 'WEEK') │ TRUNC(to_date('2022-07-07'), 'YEAR') │
├──────────────────────────────────────┼─────────────────────────────────────┼─────────────────────────────────────┤
│ 2022-07-01                           │ 2022-07-04                          │ 2022-01-01                          │
└────────────────────────────────────────────────────────────────────────────────────┘
```

以下示例演示了 `week_start` 设置如何影响使用 `WEEK` 精度时 `TRUNC` 的结果：

```sql
-- Default: week_start = 1 (Monday as first day of week)
SELECT TRUNC(to_date('2024-04-03'), 'WEEK');  -- Wednesday

┌─────────────────────────────────────┐
│ TRUNC(to_date('2024-04-03'), 'WEEK') │
├─────────────────────────────────────┤
│ 2024-04-01                          │ -- Monday
└─────────────────────────────────────┘

-- Setting week_start = 0 (Sunday as first day of week)
SETTINGS (week_start = 0) SELECT TRUNC(to_date('2024-04-03'), 'WEEK');  -- Wednesday

┌─────────────────────────────────────┐
│ TRUNC(to_date('2024-04-03'), 'WEEK') │
├─────────────────────────────────────┤
│ 2024-03-31                          │ -- Sunday
└─────────────────────────────────────┘
```

将 `TRUNC` 与时间戳值一起使用：

```sql
SELECT TRUNC(to_timestamp('2022-07-07 15:30:45.123456'), 'DAY');

┌───────────────────────────────────────────────────────┐
│ TRUNC(to_timestamp('2022-07-07 15:30:45.123456'), 'DAY') │
├───────────────────────────────────────────────────────┤
│ 2022-07-07 00:00:00.000000                            │
└───────────────────────────────────────────────────────┘
```