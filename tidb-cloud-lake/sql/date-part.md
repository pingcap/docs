---
title: DATE_PART
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.723"/>

Retrieves the designated portion of a date or timestamp.

See also: [EXTRACT](extract.md)

## Syntax

```sql
DATE_PART(
  YEAR | QUARTER | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND |
  DOW | DOY | EPOCH | ISODOW | YEARWEEK | MILLENNIUM,
  <date_or_timestamp_expr>
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

## Return Type

Integer.

## Examples

This example demonstrates how to use DATE_PART to extract various components—such as year, month, ISO week day, year-week combination, and millennium—from the current timestamp:

```sql
SELECT
  DATE_PART(YEAR, NOW())        AS year_part,
  DATE_PART(QUARTER, NOW())     AS quarter_part,
  DATE_PART(MONTH, NOW())       AS month_part,
  DATE_PART(WEEK, NOW())        AS week_part,
  DATE_PART(DAY, NOW())         AS day_part,
  DATE_PART(HOUR, NOW())        AS hour_part,
  DATE_PART(MINUTE, NOW())      AS minute_part,
  DATE_PART(SECOND, NOW())      AS second_part,
  DATE_PART(DOW, NOW())         AS dow_part,
  DATE_PART(DOY, NOW())         AS doy_part,
  DATE_PART(EPOCH, NOW())       AS epoch_part,
  DATE_PART(ISODOW, NOW())      AS isodow_part,
  DATE_PART(YEARWEEK, NOW())    AS yearweek_part,
  DATE_PART(MILLENNIUM, NOW())  AS millennium_part;
```

```sql
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ year_part │ quarter_part │ month_part │ week_part │ day_part │ hour_part │ minute_part │ second_part │ dow_part │ doy_part │     epoch_part    │ isodow_part │ yearweek_part │ millennium_part │
├───────────┼──────────────┼────────────┼───────────┼──────────┼───────────┼─────────────┼─────────────┼──────────┼──────────┼───────────────────┼─────────────┼───────────────┼─────────────────┤
│      2025 │            2 │          4 │        16 │       16 │        18 │          10 │          10 │        3 │      106 │ 1744827010.257671 │           3 │        202516 │               3 │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```