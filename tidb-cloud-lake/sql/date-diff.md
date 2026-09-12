---
title: DATE_DIFF
summary: 根据指定的时间单位，计算两个日期或时间戳之间的差值。如果 `<end_date>` 晚于 `<start_date>`，结果为正；如果早于 `<start_date>`，结果为负。
---

# DATE_DIFF

根据指定的时间单位，计算两个日期或时间戳之间的差值。如果 `<end_date>` 晚于 `<start_date>`，结果为正；如果早于 `<start_date>`，结果为负。

另请参阅：[DATE_BETWEEN](/tidb-cloud-lake/sql/date-between.md)

## 语法 {#syntax}

```sql
DATE_DIFF(
  YEAR | QUARTER | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND |
  DOW | DOY | EPOCH | ISODOW | YEARWEEK | MILLENNIUM,
  <start_date_or_timestamp>,
  <end_date_or_timestamp>
)
```

| 关键字 | 描述 |
|--------------|-------------------------------------------------------------------------|
| `DOW`        | 一周中的第几天。星期日 (0) 到星期六 (6)。 |
| `DOY`        | 一年中的第几天。1 到 366。 |
| `EPOCH`      | 自 1970-01-01 00:00:00 以来的秒数。 |
| `ISODOW`     | ISO 一周中的第几天。星期一 (1) 到星期日 (7)。 |
| `YEARWEEK`   | 年份与周数组合后的值，遵循 ISO 8601（例如，202415）。 |
| `MILLENNIUM` | 日期所属的千年（1 表示 1–1000 年，2 表示 1001–2000 年，依此类推）。 |

## DATE_DIFF 与 DATE_BETWEEN 的区别 {#date-diff-vs-date-between}

`DATE_DIFF` 函数用于统计两个日期之间跨越了多少个用户指定单位的边界（例如天、月或年），而 `DATE_BETWEEN` 用于统计两个日期之间严格包含了多少个完整单位。例如：

```sql
SELECT
    DATE_DIFF(month, '2025-07-31', '2025-10-01'),    -- returns 3
    DATE_BETWEEN(month, '2025-07-31', '2025-10-01'); -- returns 2
```

在这个示例中，`DATE_DIFF` 返回 `3`，因为该时间范围跨越了 3 个月边界（July → August → September → October）；而 `DATE_BETWEEN` 返回 `2`，因为这两个日期之间有 2 个完整的月份：August 和 September。

## 示例 {#examples}

以下示例计算固定时间戳（`2020-01-01 00:00:00`）与当前时间戳（`NOW()`）之间在多个单位下的差值，例如年、ISO 星期几、年周以及千年：

```sql
SELECT
  DATE_DIFF(YEAR,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_year,
  DATE_DIFF(QUARTER,     TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_quarter,
  DATE_DIFF(MONTH,       TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_month,
  DATE_DIFF(WEEK,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_week,
  DATE_DIFF(DAY,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_day,
  DATE_DIFF(HOUR,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_hour,
  DATE_DIFF(MINUTE,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_minute,
  DATE_DIFF(SECOND,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_second,
  DATE_DIFF(DOW,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_dow,
  DATE_DIFF(DOY,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_doy,
  DATE_DIFF(EPOCH,       TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_epoch,
  DATE_DIFF(ISODOW,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_isodow,
  DATE_DIFF(YEARWEEK,    TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_yearweek,
  DATE_DIFF(MILLENNIUM,  TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_millennium;
```

```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ diff_year │ diff_quarter │ diff_month │ diff_week │ diff_day │ diff_hour │ diff_minute │ diff_second │ diff_dow │ diff_doy │ diff_epoch │ diff_isodow │ diff_yearweek │ diff_millennium │
├───────────┼──────────────┼────────────┼───────────┼──────────┼───────────┼─────────────┼─────────────┼──────────┼──────────┼────────────┼─────────────┼───────────────┼─────────────────┤
│         5 │           21 │         63 │       276 │     1932 │     46386 │     2783184 │   166991069 │     1932 │     1932 │  166991069 │        1932 │           515 │               0 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```