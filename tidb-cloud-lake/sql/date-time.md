---
title: Date & Time
description: Databend's Date and Time data type supports standardization and compatibility with various SQL standards, making it easier for users migrating from other database systems.
sidebar_position: 6
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.834"/>

## Overview

| Name         | Aliases                   | Storage Size | Resolution  | Min Value                  | Max Value                      | Format                                                                         |
|--------------|---------------------------|--------------|-------------|----------------------------|--------------------------------|--------------------------------------------------------------------------------|
| DATE         |                           | 4 bytes      | Day         | 0001-01-01                 | 9999-12-31                     | `YYYY-MM-DD`                                                                   |
| TIMESTAMP    | DATETIME                  | 8 bytes      | Microsecond | 0001-01-01 00:00:00.000000 | 9999-12-31 23:59:59.999999 UTC | `YYYY-MM-DD hh:mm:ss[.fraction]`, uses session timezone for display            |
| TIMESTAMP_TZ | TIMESTAMP WITH TIME ZONE  | 8 bytes      | Microsecond | 0001-01-01 00:00:00.000000 | 9999-12-31 23:59:59.999999 UTC | `YYYY-MM-DD hh:mm:ss[.fraction]±hh:mm`, stores UTC value plus offset           |

`DATE` keeps only calendar values, `TIMESTAMP` stores UTC internally but renders through the current session timezone, and `TIMESTAMP_TZ` preserves the original offset for auditing or replication scenarios.

## Examples

### DATE

```sql
CREATE TABLE events (event_date DATE);
INSERT INTO events VALUES ('2024-01-15'), ('2024-12-31');
SELECT * FROM events;
```

Result:
```
┌────────────┐
│ event_date │
├────────────┤
│ 2024-01-15 │
│ 2024-12-31 │
└────────────┘
```

### TIMESTAMP

```sql
CREATE TABLE meetings (
  meeting_id INT,
  meeting_time TIMESTAMP
);

INSERT INTO meetings VALUES (1, '2024-01-15 14:00:00+08:00');

SETTINGS (timezone = 'UTC')
SELECT meeting_id, meeting_time FROM meetings;

SETTINGS (timezone = 'America/New_York')
SELECT meeting_id, meeting_time FROM meetings;
```

Result (timezone = 'UTC'):
```
┌────────────┬──────────────────────┐
│ meeting_id │ meeting_time         │
├────────────┼──────────────────────┤
│          1 │ 2024-01-15T06:00:00 │
└────────────┴──────────────────────┘
```

Result (timezone = 'America/New_York'):
```
┌────────────┬──────────────────────┐
│ meeting_id │ meeting_time         │
├────────────┼──────────────────────┤
│          1 │ 2024-01-15T01:00:00 │
└────────────┴──────────────────────┘
```

### TIMESTAMP_TZ

```sql
CREATE TABLE system_logs (
  log_id INT,
  log_time TIMESTAMP_TZ
);

INSERT INTO system_logs VALUES
  (1, '2024-01-15 14:00:00+08:00'),
  (2, '2024-01-15 06:00:00+00:00'),
  (3, '2024-01-15 01:00:00-05:00');

SETTINGS (timezone = 'UTC')
SELECT log_id, TO_STRING(log_time) AS log_time FROM system_logs;

SETTINGS (timezone = 'Asia/Shanghai')
SELECT log_id, TO_STRING(log_time) AS log_time FROM system_logs;
```

Result (timezone = 'UTC'):
```
┌────────┬────────────────────────────────────────────┐
│ log_id │ log_time                                   │
├────────┼────────────────────────────────────────────┤
│      1 │ 2024-01-15 14:00:00.000000 +0800           │
│      2 │ 2024-01-15 06:00:00.000000 +0000           │
│      3 │ 2024-01-15 01:00:00.000000 -0500           │
└────────┴────────────────────────────────────────────┘
```

Result (timezone = 'Asia/Shanghai'):
```
┌────────┬────────────────────────────────────────────┐
│ log_id │ log_time                                   │
├────────┼────────────────────────────────────────────┤
│      1 │ 2024-01-15 14:00:00.000000 +0800           │
│      2 │ 2024-01-15 06:00:00.000000 +0000           │
│      3 │ 2024-01-15 01:00:00.000000 -0500           │
└────────┴────────────────────────────────────────────┘
```

The offset is part of the stored value, so the display never changes.

## Choosing the Right Type

- Use `DATE` for calendar values without time of day.
- Use `TIMESTAMP` when different sessions should display the same moment in their local timezone.
- Use `TIMESTAMP_TZ` when you must keep the input offset for compliance or debugging.

## Daylight Saving Time Adjustments

Enable `enable_dst_hour_fix` to make Databend automatically roll missing hours forward when daylight saving time skips part of the day.

```sql
SET enable_dst_hour_fix = 1;

SETTINGS (timezone = 'America/Toronto')
SELECT to_datetime('2024-03-10 02:01:00');
```

Result:
```
┌────────────────────────────────────┐
│ to_datetime('2024-03-10 02:01:00') │
├────────────────────────────────────┤
│ 2024-03-10T03:01:00                │
└────────────────────────────────────┘
```

Use `SET enable_dst_hour_fix = 0` to return to the default behavior if you would rather raise errors for missing hours.

## Handling Invalid Values

Dates outside the supported range automatically clamp to their minimum values.

```sql
SELECT
  ADD_DAYS(TO_DATE('9999-12-31'), 1)         AS overflow_date,
  SUBTRACT_MINUTES(TO_DATE('1000-01-01'), 1) AS underflow_timestamp;
```

Result:
```
┌───────────────┬──────────────────────────┐
│ overflow_date │ underflow_timestamp      │
├───────────────┼──────────────────────────┤
│ 0001-01-01    │ 0999-12-31T18:41:28      │
└───────────────┴──────────────────────────┘
```
The values wrap to the minimum representable date or timestamp instead of raising an error.
## Formatting Date and Time

Functions such as [TO_DATE](../../20-sql-functions/05-datetime-functions/to-date.md) and [TO_TIMESTAMP](../../20-sql-functions/05-datetime-functions/to-timestamp.md) accept explicit format strings. Control how they parse or render values by adjusting `date_format_style` and `week_start`.

### Date Format Styles

Use `date_format_style` to switch between two format vocabularies:

- **MySQL** (default) uses specifiers like `%Y`, `%m`, `%d`.
- **Oracle** uses specifiers like `YYYY`, `MM`, `DD` to match ANSI-style masks.

```sql
-- Oracle-style mask
SETTINGS (date_format_style = 'Oracle')
SELECT to_string('2024-04-05'::DATE, 'YYYY-MM-DD');
```

Result (Oracle):
```
┌──────────────────────────────────────┐
│ to_string('2024-04-05'::DATE, 'YYYY-MM-DD') │
├──────────────────────────────────────┤
│ 2024-04-05                           │
└──────────────────────────────────────┘
```

```sql
-- Back to MySQL-style mask
SETTINGS (date_format_style = 'MySQL')
SELECT to_string('2024-04-05'::DATE, '%Y-%m-%d');
```

Result (MySQL):
```
┌──────────────────────────────────────┐
│ to_string('2024-04-05'::DATE, '%Y-%m-%d') │
├──────────────────────────────────────┤
│ 2024-04-05                           │
└──────────────────────────────────────┘
```

### Week Start Configuration

`week_start` defines which day begins the week for functions such as `DATE_TRUNC` or `TRUNC` when using `WEEK` precision.

```sql
SETTINGS (week_start = 0) SELECT DATE_TRUNC(WEEK, to_date('2024-04-05')); -- Sunday
SETTINGS (week_start = 1) SELECT DATE_TRUNC(WEEK, to_date('2024-04-05')); -- Monday
```

Result (week_start = 0):
```
┌────────────────────────────────┐
│ DATE_TRUNC(WEEK, TO_DATE('2024-04-05')) │
├────────────────────────────────┤
│ 2024-03-31                     │
└────────────────────────────────┘
```

Result (week_start = 1):
```
┌────────────────────────────────┐
│ DATE_TRUNC(WEEK, TO_DATE('2024-04-05')) │
├────────────────────────────────┤
│ 2024-04-01                     │
└────────────────────────────────┘
```

### MySQL Format Specifiers

To handle date and time formatting, Databend makes use of the chrono::format::strftime module, which is a standard module provided by the chrono library in Rust. This module enables precise control over the formatting of dates and times. The following content is excerpted from [https://docs.rs/chrono/latest/chrono/format/strftime/index.html](https://docs.rs/chrono/latest/chrono/format/strftime/index.html):

| Spec. | Example                          | Description                                                                                                                                                                                                                                                                                                                     |
| ----- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|       |                                  | DATE SPECIFIERS:                                                                                                                                                                                                                                                                                                                |
| %Y    | 2001                             | The full proleptic Gregorian year, zero-padded to 4 digits. chrono supports years from -262144 to 262143. Note: years before 1 BCE or after 9999 CE, require an initial sign (+/-).                                                                                                                                             |
| %C    | 20                               | The proleptic Gregorian year divided by 100, zero-padded to 2 digits.                                                                                                                                                                                                                                                           |
| %y    | 01                               | The proleptic Gregorian year modulo 100, zero-padded to 2 digits.                                                                                                                                                                                                                                                               |
| %m    | 07                               | Month number (01–12), zero-padded to 2 digits.                                                                                                                                                                                                                                                                                  |
| %b    | Jul                              | Abbreviated month name. Always 3 letters.                                                                                                                                                                                                                                                                                       |
| %B    | July                             | Full month name. Also accepts corresponding abbreviation in parsing.                                                                                                                                                                                                                                                            |
| %h    | Jul                              | Same as %b.                                                                                                                                                                                                                                                                                                                     |
| %d    | 08                               | Day number (01–31), zero-padded to 2 digits.                                                                                                                                                                                                                                                                                    |
| %e    | 8                                | Same as %d but space-padded. Same as %\_d.                                                                                                                                                                                                                                                                                      |
| %a    | Sun                              | Abbreviated weekday name. Always 3 letters.                                                                                                                                                                                                                                                                                     |
| %A    | Sunday                           | Full weekday name. Also accepts corresponding abbreviation in parsing.                                                                                                                                                                                                                                                          |
| %w    | 0                                | Sunday = 0, Monday = 1, …, Saturday = 6.                                                                                                                                                                                                                                                                                        |
| %u    | 7                                | Monday = 1, Tuesday = 2, …, Sunday = 7. (ISO 8601)                                                                                                                                                                                                                                                                              |
| %U    | 28                               | Week number starting with Sunday (00–53), zero-padded to 2 digits.                                                                                                                                                                                                                                                              |
| %W    | 27                               | Same as %U, but week 1 starts with the first Monday in that year instead.                                                                                                                                                                                                                                                       |
| %G    | 2001                             | Same as %Y but uses the year number in ISO 8601 week date.                                                                                                                                                                                                                                                                      |
| %g    | 01                               | Same as %y but uses the year number in ISO 8601 week date.                                                                                                                                                                                                                                                                      |
| %V    | 27                               | Same as %U but uses the week number in ISO 8601 week date (01–53).                                                                                                                                                                                                                                                              |
| %j    | 189                              | Day of the year (001–366), zero-padded to 3 digits.                                                                                                                                                                                                                                                                             |
| %D    | 07/08/01                         | Month-day-year format. Same as %m/%d/%y.                                                                                                                                                                                                                                                                                        |
| %x    | 07/08/01                         | Locale’s date representation (e.g., 12/31/99).                                                                                                                                                                                                                                                                                  |
| %F    | 2001-07-08                       | Year-month-day format (ISO 8601). Same as %Y-%m-%d.                                                                                                                                                                                                                                                                             |
| %v    | 8-Jul-2001                       | Day-month-year format. Same as %e-%b-%Y.                                                                                                                                                                                                                                                                                        |
|       |                                  | TIME SPECIFIERS:                                                                                                                                                                                                                                                                                                                |
| %H    | 00                               | Hour number (00–23), zero-padded to 2 digits.                                                                                                                                                                                                                                                                                   |
| %k    | 0                                | Same as %H but space-padded. Same as %\_H.                                                                                                                                                                                                                                                                                      |
| %I    | 12                               | Hour number in 12-hour clocks (01–12), zero-padded to 2 digits.                                                                                                                                                                                                                                                                 |
| %l    | 12                               | Same as %I but space-padded. Same as %\_I.                                                                                                                                                                                                                                                                                      |
| %P    | am                               | am or pm in 12-hour clocks.                                                                                                                                                                                                                                                                                                     |
| %p    | AM                               | AM or PM in 12-hour clocks.                                                                                                                                                                                                                                                                                                     |
| %M    | 34                               | Minute number (00–59), zero-padded to 2 digits.                                                                                                                                                                                                                                                                                 |
| %S    | 60                               | Second number (00–60), zero-padded to 2 digits.                                                                                                                                                                                                                                                                                 |
| %f    | 026490000                        | The fractional seconds (in nanoseconds) since last whole second. Databend recommends converting the Integer string into an Integer first, other than using this specifier. See [Converting Integer to Timestamp](/sql/sql-functions/datetime-functions/to-timestamp#example-2-converting-integer-to-timestamp) for an example. |
| %.f   | .026490                          | Similar to .%f but left-aligned. These all consume the leading dot.                                                                                                                                                                                                                                                             |
| %.3f  | .026                             | Similar to .%f but left-aligned but fixed to a length of 3.                                                                                                                                                                                                                                                                     |
| %.6f  | .026490                          | Similar to .%f but left-aligned but fixed to a length of 6.                                                                                                                                                                                                                                                                     |
| %.9f  | .026490000                       | Similar to .%f but left-aligned but fixed to a length of 9.                                                                                                                                                                                                                                                                     |
| %3f   | 026                              | Similar to %.3f but without the leading dot.                                                                                                                                                                                                                                                                                    |
| %6f   | 026490                           | Similar to %.6f but without the leading dot.                                                                                                                                                                                                                                                                                    |
| %9f   | 026490000                        | Similar to %.9f but without the leading dot.                                                                                                                                                                                                                                                                                    |
| %R    | 00:34                            | Hour-minute format. Same as %H:%M.                                                                                                                                                                                                                                                                                              |
| %T    | 00:34:60                         | Hour-minute-second format. Same as %H:%M:%S.                                                                                                                                                                                                                                                                                    |
| %X    | 00:34:60                         | Locale’s time representation (e.g., 23:13:48).                                                                                                                                                                                                                                                                                  |
| %r    | 12:34:60 AM                      | Hour-minute-second format in 12-hour clocks. Same as %I:%M:%S %p.                                                                                                                                                                                                                                                               |
|       |                                  | TIME ZONE SPECIFIERS:                                                                                                                                                                                                                                                                                                           |
| %Z    | ACST                             | Local time zone name. Skips all non-whitespace characters during parsing.                                                                                                                                                                                                                                                       |
| %z    | +0930                            | Offset from the local time to UTC (with UTC being +0000).                                                                                                                                                                                                                                                                       |
| %:z   | +09:30                           | Same as %z but with a colon.                                                                                                                                                                                                                                                                                                    |
| %::z  | +09:30:00                        | Offset from the local time to UTC with seconds.                                                                                                                                                                                                                                                                                 |
| %:::z | +09                              | Offset from the local time to UTC without minutes.                                                                                                                                                                                                                                                                              |
| %#z   | +09                              | Parsing only: Same as %z but allows minutes to be missing or present.                                                                                                                                                                                                                                                           |
|       |                                  | DATE & TIME SPECIFIERS:                                                                                                                                                                                                                                                                                                         |
| %c    | Sun Jul 8 00:34:60 2001          | Locale’s date and time (e.g., Thu Mar 3 23:05:25 2005).                                                                                                                                                                                                                                                                         |
| %+    | 2001-07-08T00:34:60.026490+09:30 | ISO 8601 / RFC 3339 date & time format.                                                                                                                                                                                                                                                                                         |
| %s    | 994518299                        | UNIX timestamp, the number of seconds since 1970-01-01 00:00 UTC. Databend recommends converting the Integer string into an Integer first, other than using this specifier. See [Converting Integer to Timestamp](/sql/sql-functions/datetime-functions/to-timestamp#example-2-converting-integer-to-timestamp) for an example. |
|       |                                  | SPECIAL SPECIFIERS:                                                                                                                                                                                                                                                                                                             |
| %t    |                                  | Literal tab (\t).                                                                                                                                                                                                                                                                                                               |
| %n    |                                  | Literal newline (\n).                                                                                                                                                                                                                                                                                                           |
| %%    |                                  | Literal percent sign.                                                                                                                                                                                                                                                                                                           |

It is possible to override the default padding behavior of numeric specifiers %?. This is not allowed for other specifiers and will result in the BAD_FORMAT error.

| Modifier | Description                                                                   |
| -------- | ----------------------------------------------------------------------------- |
| %-?      | Suppresses any padding including spaces and zeroes. (e.g. %j = 012, %-j = 12) |
| %\_?     | Uses spaces as a padding. (e.g. %j = 012, %\_j = 12)                          |
| %0?      | Uses zeroes as a padding. (e.g. %e = 9, %0e = 09)                             |

- %C, %y: This is floor division, so 100 BCE (year number -99) will print -1 and 99 respectively.

- %U: Week 1 starts with the first Sunday in that year. It is possible to have week 0 for days before the first Sunday.

- %G, %g, %V: Week 1 is the first week with at least 4 days in that year. Week 0 does not exist, so this should be used with %G or %g.

- %S: It accounts for leap seconds, so 60 is possible.

- %f, %.f, %.3f, %.6f, %.9f, %3f, %6f, %9f:
  The default %f is right-aligned and always zero-padded to 9 digits for the compatibility with glibc and others, so it always counts the number of nanoseconds since the last whole second. E.g. 7ms after the last second will print 007000000, and parsing 7000000 will yield the same.

  The variant %.f is left-aligned and print 0, 3, 6 or 9 fractional digits according to the precision. E.g. 70ms after the last second under %.f will print .070 (note: not .07), and parsing .07, .070000 etc. will yield the same. Note that they can print or read nothing if the fractional part is zero or the next character is not ..

  The variant %.3f, %.6f and %.9f are left-aligned and print 3, 6 or 9 fractional digits according to the number preceding f. E.g. 70ms after the last second under %.3f will print .070 (note: not .07), and parsing .07, .070000 etc. will yield the same. Note that they can read nothing if the fractional part is zero or the next character is not . however will print with the specified length.

  The variant %3f, %6f and %9f are left-aligned and print 3, 6 or 9 fractional digits according to the number preceding f, but without the leading dot. E.g. 70ms after the last second under %3f will print 070 (note: not 07), and parsing 07, 070000 etc. will yield the same. Note that they can read nothing if the fractional part is zero.

- %Z: Offset will not be populated from the parsed data, nor will it be validated. Timezone is completely ignored. Similar to the glibc strptime treatment of this format code.

  It is not possible to reliably convert from an abbreviation to an offset, for example CDT can mean either Central Daylight Time (North America) or China Daylight Time.

- %+: Same as %Y-%m-%dT%H:%M:%S%.f%:z, i.e. 0, 3, 6 or 9 fractional digits for seconds and colons in the time zone offset.

  This format also supports having a Z or UTC in place of %:z. They are equivalent to +00:00.

  Note that all T, Z, and UTC are parsed case-insensitively.

  The typical strftime implementations have different (and locale-dependent) formats for this specifier. While Chrono's format for %+ is far more stable, it is best to avoid this specifier if you want to control the exact output.

- %s: This is not padded and can be negative. For the purpose of Chrono, it only accounts for non-leap seconds so it slightly differs from ISO C strftime behavior.

### Oracle Format Specifiers

When `date_format_style` is set to 'Oracle', the following format specifiers are supported:

| Oracle Format | Description                                  | Example Output (for '2024-04-05 14:30:45.123456') |
|---------------|----------------------------------------------|---------------------------------------------------|
| YYYY          | 4-digit year                                 | 2024                                              |
| YY            | 2-digit year                                 | 24                                                |
| MMMM          | Full month name                              | April                                             |
| MON           | Abbreviated month name                       | Apr                                               |
| MM            | Month number (01-12)                         | 04                                                |
| DD            | Day of month (01-31)                         | 05                                                |
| DY            | Abbreviated day name                         | Fri                                               |
| HH24          | Hour of day (00-23)                          | 14                                                |
| HH12          | Hour of day (01-12)                          | 02                                                |
| AM/PM         | Meridian indicator                           | PM                                                |
| MI            | Minute (00-59)                               | 30                                                |
| SS            | Second (00-59)                               | 45                                                |
| FF            | Fractional seconds                           | 123456                                            |
| UUUU          | ISO week-numbering year                      | 2024                                              |
| TZH:TZM       | Time zone hour and minute with colon         | +08:00                                            |
| TZH           | Time zone hour                               | +08                                               |

Examples comparing MySQL and Oracle format styles with the same data:

```sql
-- MySQL format style (default)
SELECT to_string('2022-12-25'::DATE, '%m/%d/%Y');

┌────────────────────────────────┐
│ to_string('2022-12-25', '%m/%d/%Y') │
├────────────────────────────────┤
│ 12/25/2022                     │
└────────────────────────────────┘

-- Oracle format style (same data as MySQL example above)
SETTINGS (date_format_style = 'Oracle')
SELECT to_string('2022-12-25'::DATE, 'MM/DD/YYYY');

┌────────────────────────────────┐
│ to_string('2022-12-25', 'MM/DD/YYYY') │
├────────────────────────────────┤
│ 12/25/2022                     │
└────────────────────────────────┘
```
