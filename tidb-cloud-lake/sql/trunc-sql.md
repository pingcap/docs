---
title: TRUNC
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced: v1.2.745"/>

Truncates a date or timestamp to a specified precision. This function follows a widely adopted date truncation syntax, making it easier for users migrating from other database systems.

## Syntax

```sql
TRUNC(<date_or_timestamp>, <datetime_interval_type>)
```

| Parameter                  | Description                                                                                                |
|----------------------------|------------------------------------------------------------------------------------------------------------|
| `<date_or_timestamp>`      | A value of `DATE` or `TIMESTAMP` type.                                                                     |
| `<datetime_interval_type>` | Must be one of the following values: `YEAR`, `QUARTER`, `MONTH`, `WEEK`, `DAY`, `HOUR`, `MINUTE`, `SECOND`. |

## Week Start Configuration

When using `WEEK` as the datetime interval type, the result depends on the `week_start` setting, which defines the first day of the week:

- `week_start = 1` (default): Monday is considered the first day of the week
- `week_start = 0`: Sunday is considered the first day of the week

You can use the `SETTINGS` clause to change this setting for a specific query:

```sql
-- Set Sunday as the first day of the week
SETTINGS (week_start = 0) SELECT TRUNC(to_date('2024-04-05'), 'WEEK');

-- Set Monday as the first day of the week (default)
SETTINGS (week_start = 1) SELECT TRUNC(to_date('2024-04-05'), 'WEEK');
```

## Return Type

Same as `<date_or_timestamp>`.

## Examples

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

The following example demonstrates how the `week_start` setting affects the result of `TRUNC` with `WEEK` precision:

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

Using `TRUNC` with timestamp values:

```sql
SELECT TRUNC(to_timestamp('2022-07-07 15:30:45.123456'), 'DAY');

┌───────────────────────────────────────────────────────┐
│ TRUNC(to_timestamp('2022-07-07 15:30:45.123456'), 'DAY') │
├───────────────────────────────────────────────────────┤
│ 2022-07-07 00:00:00.000000                            │
└───────────────────────────────────────────────────────┘
