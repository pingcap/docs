---
title: DATE_DIFF
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.723"/>

Calculates the difference between two dates or timestamps based on a specified time unit. The result is positive if the `<end_date>` is after the `<start_date>`, and negative if it's before.

See also: [DATE_BETWEEN](date-between.md)

## Syntax

```sql
DATE_DIFF(
  YEAR | QUARTER | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND |
  DOW | DOY | EPOCH | ISODOW | YEARWEEK | MILLENNIUM,
  <start_date_or_timestamp>,
  <end_date_or_timestamp>
)
```

| Keyword      | Description                                                             |
|--------------|-------------------------------------------------------------------------|
| `DOW`        | Day of the Week. Sunday (0) through Saturday (6).                       |
| `DOY`        | Day of the Year. 1 through 366.                                         |
| `EPOCH`      | The number of seconds since 1970-01-01 00:00:00.                        |
| `ISODOW`     | ISO Day of the Week. Monday (1) through Sunday (7).                     |
| `YEARWEEK`   | The year and week number combined, following ISO 8601 (e.g., 202415).   |
| `MILLENNIUM` | The millennium of the date (1 for years 1–1000, 2 for 1001–2000, etc.). |

## DATE_DIFF vs. DATE_BETWEEN

The `DATE_DIFF` function counts how many boundaries of a user-specified unit (such as day, month, or year) are crossed between two dates, while `DATE_BETWEEN` counts how many complete units fall strictly between them. For example:

```sql
SELECT
    DATE_DIFF(month, '2025-07-31', '2025-10-01'),    -- returns 3
    DATE_BETWEEN(month, '2025-07-31', '2025-10-01'); -- returns 2
```

In this example, `DATE_DIFF` returns `3` because the range crosses three month boundaries (July → August → September → October), while `DATE_BETWEEN` returns `2` because there are two full months between the dates: August and September.

## Examples

This example calculates the difference between a fixed timestamp (`2020-01-01 00:00:00`) and the current timestamp (`NOW()`), across various units such as year, ISO weekday, year-week, and millennium:

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