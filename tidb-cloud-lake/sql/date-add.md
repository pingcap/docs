---
title: DATE_ADD
summary: 向 DATE 或 TIMESTAMP 值添加指定的时间间隔。
---

# DATE_ADD

向 DATE 或 TIMESTAMP 值添加指定的时间间隔。

## 语法 {#syntax}

```sql
DATE_ADD(<unit>, <interval>,  <date_or_time_expr>)
```

| 参数                  | 描述                                                                                               |
|-----------------------|----------------------------------------------------------------------------------------------------|
| `<unit>`              | 指定时间单位：`YEAR`、`QUARTER`、`MONTH`、`WEEK`、`DAY`、`HOUR`、`MINUTE` 和 `SECOND`。 |
| `<interval>`          | 要添加的间隔，例如，当单位为 `DAY` 时，2 表示 2 天。                                      |
| `<date_or_time_expr>` | `DATE` 或 `TIMESTAMP` 类型的值。                                                             |

## 返回类型 {#return-type}

DATE 或 TIMESTAMP（取决于 `<date_or_time_expr>` 的类型）。

## 示例 {#examples}

以下示例向当前日期添加不同的时间间隔（年、季度、月、周和天）：

```sql
SELECT
    TODAY(),
    DATE_ADD(YEAR, 1, TODAY()),
    DATE_ADD(QUARTER, 1, TODAY()),
    DATE_ADD(MONTH, 1, TODAY()),
    DATE_ADD(WEEK, 1, TODAY()),
    DATE_ADD(DAY, 1, TODAY());

-[ RECORD 1 ]-----------------------------------
                      today(): 2024-10-10
   DATE_ADD(YEAR, 1, today()): 2025-10-10
DATE_ADD(QUARTER, 1, today()): 2025-01-10
  DATE_ADD(MONTH, 1, today()): 2024-11-10
   DATE_ADD(WEEK, 1, today()): 2024-10-17
    DATE_ADD(DAY, 1, today()): 2024-10-11
```

以下示例向当前时间戳添加不同的时间间隔（小时、分钟和秒）：

```sql
SELECT
    NOW(),
    DATE_ADD(HOUR, 1, NOW()),
    DATE_ADD(MINUTE, 1, NOW()),
    DATE_ADD(SECOND, 1, NOW());

-[ RECORD 1 ]-----------------------------------
                     now(): 2024-10-10 01:35:33.601312
  DATE_ADD(HOUR, 1, now()): 2024-10-10 02:35:33.601312
DATE_ADD(MINUTE, 1, now()): 2024-10-10 01:36:33.601312
DATE_ADD(SECOND, 1, now()): 2024-10-10 01:35:34.601312
```

- 当单位为 MONTH 时，如果日期是该月的最后一天，或者结果月份的天数少于原日期中的“日”部分，
- 则结果为结果月份的最后一天。否则，结果中的“日”部分与原日期相同。

当向某个日期加一个月后会得到无效日期时（例如，1 月 31 日 → 2 月 31 日），将返回结果月份中最后一个有效日期：

```sql
SELECT DATE_ADD(month, 1, '2023-01-31'::DATE) ;
╭────────────────────────────────────────╮
│ DATE_ADD(MONTH, 1, '2023-01-31'::DATE) │
│                  Date                  │
├────────────────────────────────────────┤
│ 2023-02-28                             │
╰────────────────────────────────────────╯

```

当向某个日期加一个月后，结果月份有足够的天数时，将执行简单的月份运算：

```sql
SELECT DATE_ADD(month, 1, '2023-02-28'::DATE);
╭────────────────────────────────────────╮
│ DATE_ADD(MONTH, 1, '2023-02-28'::DATE) │
│                  Date                  │
├────────────────────────────────────────┤
│ 2023-03-28                             │
╰────────────────────────────────────────╯

```

## 另请参阅 {#see-also}

- [ADD_MONTH](/tidb-cloud-lake/sql/add-months.md): 用于添加月份的函数
- [DATE_SUB](/tidb-cloud-lake/sql/date-sub.md): 用于减去时间间隔的函数