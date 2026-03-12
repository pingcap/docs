---
title: Date & Time Functions
---

This page provides a comprehensive overview of Date & Time functions in Databend, organized by functionality for easy reference.

## Current Date & Time Functions

| Function                                  | Description                       | Example                                              |
|-------------------------------------------|-----------------------------------|------------------------------------------------------|
| [NOW](now.md)                             | Returns the current date and time | `NOW()` → `2024-06-04 17:42:31.123456`               |
| [CURRENT_TIMESTAMP](current-timestamp.md) | Returns the current date and time | `CURRENT_TIMESTAMP()` → `2024-06-04 17:42:31.123456` |
| [TODAY](today.md)                         | Returns the current date          | `TODAY()` → `2024-06-04`                             |
| [TOMORROW](tomorrow.md)                   | Returns tomorrow's date           | `TOMORROW()` → `2024-06-05`                          |
| [YESTERDAY](yesterday.md)                 | Returns yesterday's date          | `YESTERDAY()` → `2024-06-03`                         |

## Date & Time Extraction Functions

| Function                                      | Description                          | Example                                  |
|-----------------------------------------------|--------------------------------------|------------------------------------------|
| [YEAR](year.md)                               | Extracts the year from a date        | `YEAR('2024-06-04')` → `2024`            |
| [MONTH](month.md)                             | Extracts the month from a date       | `MONTH('2024-06-04')` → `6`              |
| [DAY](day.md)                                 | Extracts the day from a date         | `DAY('2024-06-04')` → `4`                |
| [QUARTER](quarter.md)                         | Extracts the quarter from a date     | `QUARTER('2024-06-04')` → `2`            |
| [WEEK](week.md) / [WEEKOFYEAR](weekofyear.md) | Extracts the week number from a date | `WEEK('2024-06-04')` → `23`              |
| [EXTRACT](extract.md)                         | Extracts a part from a date          | `EXTRACT(MONTH FROM '2024-06-04')` → `6` |
| [DATE_PART](date-part.md)                     | Extracts a part from a date          | `DATE_PART('month', '2024-06-04')` → `6` |
| [YEARWEEK](yearweek.md)                       | Returns year and week number         | `YEARWEEK('2024-06-04')` → `202423`      |
| [MILLENNIUM](millennium.md)                   | Returns the millennium from a date   | `MILLENNIUM('2024-06-04')` → `3`         |

## Date & Time Conversion Functions

| Function                                  | Description                                 | Example                                                       |
|-------------------------------------------|---------------------------------------------|---------------------------------------------------------------|
| [DATE](date.md)                           | Converts a value to DATE type               | `DATE('2024-06-04')` → `2024-06-04`                           |
| [TO_DATE](to-date.md)                     | Converts a string to DATE type              | `TO_DATE('2024-06-04')` → `2024-06-04`                        |
| [TO_DATETIME](to-datetime.md)             | Converts a string to DATETIME type          | `TO_DATETIME('2024-06-04 12:30:45')` → `2024-06-04 12:30:45`  |
| [TO_TIMESTAMP](to-timestamp.md)           | Converts a string to TIMESTAMP type         | `TO_TIMESTAMP('2024-06-04 12:30:45')` → `2024-06-04 12:30:45` |
| [TO_UNIX_TIMESTAMP](to-unix-timestamp.md) | Converts a date to Unix timestamp           | `TO_UNIX_TIMESTAMP('2024-06-04')` → `1717516800`              |
| [TO_YYYYMM](to-yyyymm.md)                 | Formats date as YYYYMM                      | `TO_YYYYMM('2024-06-04')` → `202406`                          |
| [TO_YYYYMMDD](to-yyyymmdd.md)             | Formats date as YYYYMMDD                    | `TO_YYYYMMDD('2024-06-04')` → `20240604`                      |
| [TO_YYYYMMDDHH](to-yyyymmddhh.md)         | Formats date as YYYYMMDDHH                  | `TO_YYYYMMDDHH('2024-06-04 12:30:45')` → `2024060412`         |
| [TO_YYYYMMDDHHMMSS](to-yyyymmddhhmmss.md) | Formats date as YYYYMMDDHHMMSS              | `TO_YYYYMMDDHHMMSS('2024-06-04 12:30:45')` → `20240604123045` |
| [DATE_FORMAT](date-format.md)             | Formats a date according to a format string | `DATE_FORMAT('2024-06-04', '%Y-%m-%d')` → `'2024-06-04'`      |
| [CONVERT_TIMEZONE](convert-timezone.md)   | Converts a timestamp to the target timezone | `CONVERT_TIMEZONE('America/Los_Angeles', '2024-11-01 11:36:10')` → `2024-10-31 20:36:10` |

## Date & Time Arithmetic Functions

| Function                                 | Description                                                                                  | Example                                                                              |
|------------------------------------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| [DATE_ADD](date-add.md)                  | Adds a time interval to a date                                                               | `DATE_ADD(DAY, 7, '2024-06-04')` → `2024-06-11`                                      |
| [DATE_SUB](date-sub.md)                  | Subtracts a time interval from a date                                                        | `DATE_SUB(MONTH, 1, '2024-06-04')` → `2024-05-04`                                    |
| [ADD INTERVAL](addinterval.md)           | Adds an interval to a date                                                                   | `'2024-06-04' + INTERVAL 1 DAY` → `2024-06-05`                                       |
| [SUBTRACT INTERVAL](subtractinterval.md) | Subtracts an interval from a date                                                            | `'2024-06-04' - INTERVAL 1 MONTH` → `2024-05-04`                                     |
| [DATE_DIFF](date-diff.md)                | Returns the difference between two dates                                                     | `DATE_DIFF(DAY, '2024-06-01', '2024-06-04')` → `3`                                   |
| [TIMESTAMP_DIFF](timestamp-diff.md)      | Returns the difference between two timestamps                                                | `TIMESTAMP_DIFF(HOUR, '2024-06-04 10:00:00', '2024-06-04 15:00:00')` → `5`           |
| [MONTHS_BETWEEN](months-between.md)      | Returns the number of months between two dates                                               | `MONTHS_BETWEEN('2024-06-04', '2024-01-04')` → `5`                                   |
| [DATE_BETWEEN](date-between.md)          | Checks if a date is between two other dates                                                  | `DATE_BETWEEN('2024-06-04', '2024-06-01', '2024-06-10')` → `true`                    |
| [AGE](age.md)                            | Calculate the difference between timestamps or between a timestamp and the current date/time | `AGE('2000-01-01'::TIMESTAMP, '1990-05-15'::TIMESTAMP)` → `9 years 7 months 17 days` |
| [ADD_MONTHS](add-months.md)              | Adds months to a date while preserving end-of-month days.                                    | `ADD_MONTHS('2025-04-30',1)` → `2025-05-31`                                          |

## Date & Time Truncation Functions

| Function                                      | Description                                                      | Example                                                             |
|-----------------------------------------------|------------------------------------------------------------------|---------------------------------------------------------------------|
| [DATE_TRUNC](date-trunc.md)                   | Truncates a timestamp to a specified precision                   | `DATE_TRUNC('month', '2024-06-04')` → `2024-06-01`                  |
| [TIME_SLICE](time-slice.md)                   | Map a single date/timestamp value to a calendar-aligned interval | `TIME_SLICE('2024-06-04', 4, 'MONTH', 'START')` → `2024-05-01`      |
| [TO_START_OF_DAY](to-start-of-day.md)         | Returns the start of the day                                     | `TO_START_OF_DAY('2024-06-04 12:30:45')` → `2024-06-04 00:00:00`    |
| [TO_START_OF_HOUR](to-start-of-hour.md)       | Returns the start of the hour                                    | `TO_START_OF_HOUR('2024-06-04 12:30:45')` → `2024-06-04 12:00:00`   |
| [TO_START_OF_MINUTE](to-start-of-minute.md)   | Returns the start of the minute                                  | `TO_START_OF_MINUTE('2024-06-04 12:30:45')` → `2024-06-04 12:30:00` |
| [TO_START_OF_MONTH](to-start-of-month.md)     | Returns the start of the month                                   | `TO_START_OF_MONTH('2024-06-04')` → `2024-06-01`                    |
| [TO_START_OF_QUARTER](to-start-of-quarter.md) | Returns the start of the quarter                                 | `TO_START_OF_QUARTER('2024-06-04')` → `2024-04-01`                  |
| [TO_START_OF_YEAR](to-start-of-year.md)       | Returns the start of the year                                    | `TO_START_OF_YEAR('2024-06-04')` → `2024-01-01`                     |
| [TO_START_OF_WEEK](to-start-of-week.md)       | Returns the start of the week                                    | `TO_START_OF_WEEK('2024-06-04')` → `2024-06-03`                     |

## Date & Time Navigation Functions

| Function                        | Description                                            | Example                                               |
|---------------------------------|--------------------------------------------------------|-------------------------------------------------------|
| [LAST_DAY](last-day.md)         | Returns the last day of the month                      | `LAST_DAY('2024-06-04')` → `2024-06-30`               |
| [NEXT_DAY](next-day.md)         | Returns the date of the next specified day of week     | `NEXT_DAY('2024-06-04', 'SUNDAY')` → `2024-06-09`     |
| [PREVIOUS_DAY](previous-day.md) | Returns the date of the previous specified day of week | `PREVIOUS_DAY('2024-06-04', 'MONDAY')` → `2024-06-03` |

## Other Date & Time Functions

| Function                  | Description                  | Example                                                                  |
|---------------------------|------------------------------|--------------------------------------------------------------------------|
| [TIMEZONE](timezone.md)   | Returns the current timezone | `TIMEZONE()` → `'UTC'`                                                   |
| [TIME_SLOT](time-slot.md) | Returns time slots           | `TIME_SLOT('2024-06-04 12:30:45', 15, 'MINUTE')` → `2024-06-04 12:30:00` |
