---
title: DATE_BETWEEN
summary: 计算两个日期或时间戳之间的时间间隔，并以指定单位的整数型差值返回。正值表示第一个时间早于第二个时间，负值则表示相反。
---

# DATE_BETWEEN

计算两个日期或时间戳之间的时间间隔，并以指定单位的整数型差值返回。正值表示第一个时间早于第二个时间，负值则表示相反。

另请参阅：[DATE_DIFF](/tidb-cloud-lake/sql/date-diff.md)

## 语法 {#syntax}

```sql
DATE_BETWEEN(
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
| `YEARWEEK`   | 年份与周数组合，遵循 ISO 8601（例如，202415）。 |
| `MILLENNIUM` | 日期所属的千年（1 表示 1–1000 年，2 表示 1001–2000 年，依此类推）。 |

## DATE_DIFF 与 DATE_BETWEEN 的区别 {#date-diff-vs-date-between}

`DATE_DIFF` 函数用于计算两个日期之间跨越了多少个用户指定单位的边界（例如天、月或年），而 `DATE_BETWEEN` 用于计算它们之间严格包含了多少个完整单位。例如：

```sql
SELECT
    DATE_DIFF(month, '2025-07-31', '2025-10-01'),    -- returns 3
    DATE_BETWEEN(month, '2025-07-31', '2025-10-01'); -- returns 2
```

在这个示例中，`DATE_DIFF` 返回 `3`，因为该时间范围跨越了 3 个月边界（July → August → September → October）；而 `DATE_BETWEEN` 返回 `2`，因为这两个日期之间有 2 个完整的月份：August 和 September。

## 示例 {#examples}

以下示例计算固定时间戳（`2020-01-01 00:00:00`）与当前时间戳（`NOW()`）之间在多种单位下的差值，例如年、ISO 工作日、年周和千年：

```sql
SELECT
  DATE_BETWEEN(YEAR,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_year,
  DATE_BETWEEN(QUARTER,     TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_quarter,
  DATE_BETWEEN(MONTH,       TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_month,
  DATE_BETWEEN(WEEK,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_week,
  DATE_BETWEEN(DAY,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_day,
  DATE_BETWEEN(HOUR,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_hour,
  DATE_BETWEEN(MINUTE,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_minute,
  DATE_BETWEEN(SECOND,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_second,
  DATE_BETWEEN(DOW,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_dow,
  DATE_BETWEEN(DOY,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_doy,
  DATE_BETWEEN(EPOCH,       TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_epoch,
  DATE_BETWEEN(ISODOW,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_isodow,
  DATE_BETWEEN(YEARWEEK,    TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_yearweek,
  DATE_BETWEEN(MILLENNIUM,  TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_millennium;
```

```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ diff_year │ diff_quarter │ diff_month │ diff_week │ diff_day │ diff_hour │ diff_minute │ diff_second │ diff_dow │ diff_doy │ diff_epoch │ diff_isodow │ diff_yearweek │ diff_millennium │
├───────────┼──────────────┼────────────┼───────────┼──────────┼───────────┼─────────────┼─────────────┼──────────┼──────────┼────────────┼─────────────┼───────────────┼─────────────────┤
│         5 │           21 │         63 │       276 │     1933 │     46414 │     2784887 │   167093234 │     1933 │     1933 │  167093234 │        1933 │           276 │               0 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```