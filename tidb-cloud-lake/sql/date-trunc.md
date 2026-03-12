---
title: DATE_TRUNC
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.745"/>

Truncates a date or timestamp to a specified precision, providing a standardized way to manipulate dates and timestamps. This function is designed to be compatible with various database systems, making it easier for users to migrate and work with different databases.

## Syntax

```sql
DATE_TRUNC(<precision>, <date_or_timestamp>)
```

| Parameter             | Description                                                                                                |
|-----------------------|------------------------------------------------------------------------------------------------------------|
| `<precision>`         | Must be of the following values: `YEAR`, `QUARTER`, `MONTH`, `WEEK`, `DAY`, `HOUR`, `MINUTE` and `SECOND`. |
| `<date_or_timestamp>` | A value of `DATE` or `TIMESTAMP` type.                                                                     |

## Week Start Configuration

When using `WEEK` as the precision parameter, the result depends on the `week_start` setting, which defines the first day of the week:

- `week_start = 1` (default): Monday is considered the first day of the week
- `week_start = 0`: Sunday is considered the first day of the week

You can use the `SETTINGS` clause to change this setting for a specific query:

```sql
-- Set Sunday as the first day of the week
SETTINGS (week_start = 0) SELECT DATE_TRUNC(WEEK, to_date('2024-04-05'));

-- Set Monday as the first day of the week (default)
SETTINGS (week_start = 1) SELECT DATE_TRUNC(WEEK, to_date('2024-04-05'));
```

## Return Type

Same as `<date_or_timestamp>`.

## Examples

```sql
SELECT
    DATE_TRUNC(MONTH, to_date('2022-07-07')),
    DATE_TRUNC(WEEK, to_date('2022-07-07'));

┌────────────────────────────────────────────────────────────────────────────────────┐
│ DATE_TRUNC(MONTH, to_date('2022-07-07')) │ DATE_TRUNC(WEEK, to_date('2022-07-07')) │
├──────────────────────────────────────────┼─────────────────────────────────────────┤
│ 2022-07-01                               │ 2022-07-04                               │
└────────────────────────────────────────────────────────────────────────────────────┘
```

```sql
SELECT
    DATE_TRUNC(HOUR, to_timestamp('2022-07-07 01:01:01.123456')),
    DATE_TRUNC(SECOND, to_timestamp('2022-07-07 01:01:01.123456'));

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ DATE_TRUNC(HOUR, to_timestamp('2022-07-07 01:01:01.123456')) │ DATE_TRUNC(SECOND, to_timestamp('2022-07-07 01:01:01.123456')) │
├─────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────┤
│ 2022-07-07 01:00:00.000000                                  │ 2022-07-07 01:01:01.000000                                     │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## See Also

- [TRUNC](trunc.md): Provides similar functionality with a different syntax for better SQL standard compatibility.
- [TIME_SLICE](time-slice.md): Map a single date/timestamp value to a calendar-aligned interval.
