---
title: EXTRACT
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.723"/>

Retrieves the designated portion of a date, timestamp, or interval.

See also: [DATE_PART](date-part.md)

## Syntax

```sql
-- Extract from a date or timestamp
EXTRACT(
  YEAR | QUARTER | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND |
  DOW | DOY | EPOCH | ISODOW | YEARWEEK | MILLENNIUM
  FROM <date_or_timestamp>
)

-- Extract from an interval
EXTRACT( YEAR | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND | MICROSECOND ｜ EPOCH FROM <interval> )
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

The return type depends on the field being extracted:

- Returns Integer: When extracting discrete date or time components (e.g., YEAR, MONTH, DAY, DOY, HOUR, MINUTE, SECOND), the function returns an Integer.

    ```sql
    SELECT EXTRACT(DAY FROM now());  -- Returns Integer
    SELECT EXTRACT(DOY FROM now());  -- Returns Integer
    ```

- Returns Float: When extracting EPOCH (the number of seconds since 1970-01-01 00:00:00 UTC), the function returns a Float, as it may include fractional seconds.

    ```sql
    SELECT EXTRACT(EPOCH FROM now());  -- Returns Float
    ```

## Examples

This example extracts various fields from the current timestamp:

```sql
SELECT 
  NOW(), 
  EXTRACT(DAY FROM NOW()), 
  EXTRACT(DOY FROM NOW()), 
  EXTRACT(EPOCH FROM NOW()), 
  EXTRACT(ISODOW FROM NOW()), 
  EXTRACT(YEARWEEK FROM NOW()), 
  EXTRACT(MILLENNIUM FROM NOW());

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│            now()           │ EXTRACT(DAY FROM now()) │ EXTRACT(DOY FROM now()) │ EXTRACT(EPOCH FROM now()) │ EXTRACT(ISODOW FROM now()) │ EXTRACT(YEARWEEK FROM now()) │ EXTRACT(MILLENNIUM FROM now()) │
├────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────────────┼────────────────────────────┼──────────────────────────────┼────────────────────────────────┤
│ 2025-04-16 18:04:22.773888 │                      16 │                     106 │         1744826662.773888 │                          3 │                       202516 │                              3 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example extracts the number of days from an interval:

```sql
SELECT EXTRACT(DAY FROM '1 day 2 hours 3 minutes 4 seconds'::INTERVAL);

┌─────────────────────────────────────────────────────────────────┐
│ EXTRACT(DAY FROM '1 day 2 hours 3 minutes 4 seconds'::INTERVAL) │
├─────────────────────────────────────────────────────────────────┤
│                                                               1 │
└─────────────────────────────────────────────────────────────────┘
```