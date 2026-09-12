---
title: DATE_SUB
summary: 从提供的日期或带时间的日期（timestamp/datetime）中减去时间间隔或日期间隔。
---

# DATE_SUB

从提供的日期或带时间的日期（timestamp/datetime）中减去时间间隔或日期间隔。

## 语法 {#syntax}

```sql
DATE_SUB(<unit>, <value>,  <date_or_time_expr>)
```

## 参数 {#arguments}

| 参数                  | 描述                                                                 |
|-----------------------|----------------------------------------------------------------------|
| `<unit>`              | 必须是以下值之一：`YEAR`、`QUARTER`、`MONTH`、`DAY`、`HOUR`、`MINUTE` 和 `SECOND` |
| `<value>`             | 表示要增加的时间单位数量。例如，如果要增加 2 天，则该值为 2。         |
| `<date_or_time_expr>` | `DATE` 或 `TIMESTAMP` 类型的值                                       |

## 返回类型 {#return-type}

该函数返回与 `<date_or_time_expr>` 参数相同类型的值。

## 示例 {#examples}

```sql
SELECT date_sub(YEAR, 1, to_date('2018-01-02'));

┌──────────────────────────────────────────┐
│ date_sub(year, 1, to_date('2018-01-02')) │
├──────────────────────────────────────────┤
│ 2017-01-02                               │
└──────────────────────────────────────────┘
```