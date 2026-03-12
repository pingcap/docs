---
title: TRY_TO_TIMESTAMP
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.528"/>

A variant of [TO_TIMESTAMP](to-timestamp.md) in Databend that, while performing the same conversion of an input expression to a timestamp, incorporates error-handling support by returning NULL if the conversion fails instead of raising an error.

See also: [TO_TIMESTAMP](to-timestamp.md)

## Syntax

```sql
-- Convert a string or integer to a timestamp
TRY_TO_TIMESTAMP(<expr>)

-- Convert a string to a timestamp using the given pattern
TRY_TO_TIMESTAMP(<expr>, <pattern>)
```

If given two arguments, the function converts the first string to a timestamp based on the pattern specified in the second string. To specify the pattern, use specifiers. The specifiers allow you to define the desired format for date and time values. For a comprehensive list of supported specifiers, see [Formatting Date and Time](../../00-sql-reference/10-data-types/datetime.md#formatting-date-and-time).

## Aliases

- [TRY_TO_DATETIME](try-to-datetime.md)

## Examples

```sql
SELECT TRY_TO_TIMESTAMP('2022-01-02 02:00:11'), TRY_TO_DATETIME('2022-01-02 02:00:11');

┌──────────────────────────────────────────────────────────────────────────────────┐
│ try_to_timestamp('2022-01-02 02:00:11') │ try_to_datetime('2022-01-02 02:00:11') │
├─────────────────────────────────────────┼────────────────────────────────────────┤
│ 2022-01-02 02:00:11                     │ 2022-01-02 02:00:11                    │
└──────────────────────────────────────────────────────────────────────────────────┘

SELECT TRY_TO_TIMESTAMP('2024-06-12 10:21:39', '%Y-%m-%d %H:%M:%S'), TRY_TO_DATETIME('2024-06-12 10:21:39', '%Y-%m-%d %H:%M:%S');

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ try_to_timestamp('2024-06-12 10:21:39', '%y-%m-%d %h:%m:%s') │ try_to_datetime('2024-06-12 10:21:39', '%y-%m-%d %h:%m:%s') │
├──────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 2024-06-12 10:21:39                                          │ 2024-06-12 10:21:39                                         │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT TRY_TO_TIMESTAMP('databend'), TRY_TO_DATETIME('databend');

┌────────────────────────────────────────────────────────────┐
│ try_to_timestamp('databend') │ try_to_datetime('databend') │
├──────────────────────────────┼─────────────────────────────┤
│ NULL                         │ NULL                        │
└────────────────────────────────────────────────────────────┘

SELECT TRY_TO_TIMESTAMP('2024-06-12 10:21:39', '%y-%m-%d %H:%M:%S'), TRY_TO_DATETIME('2024-06-12 10:21:39', '%y-%m-%d %H:%M:%S');

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ try_to_timestamp('2024-06-12 10:21:39', '%y-%m-%d %h:%m:%s') │ try_to_datetime('2024-06-12 10:21:39', '%y-%m-%d %h:%m:%s') │
├──────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ NULL                                                         │ NULL                                                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```