---
title: TO_TIMESTAMP
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.664"/>

Converts an expression to a date with time.

See also: [TO_DATE](to-date)

## Syntax

This function supports multiple overloads, covering the following use cases:

```sql
-- Convert a string or integer to a timestamp
TO_TIMESTAMP(<expr>)
```

If given an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date format string, the function extracts a date from the string; If given is an integer, the function interprets the integer as the number of seconds, milliseconds, or microseconds before (for a negative number) or after (for a positive number) the Unix epoch (midnight on January 1, 1970), depending on the absolute value of `x`:

| Range                                       | Unit                 |
|---------------------------------------------|----------------------|
| \|x\| < 31,536,000,000                      | Seconds              |
| 31,536,000,000 ≤ \|x\| < 31,536,000,000,000 | Milliseconds         |
| \|x\| ≥ 31,536,000,000,000                  | Microseconds         |

```sql
-- Convert a string to a timestamp using the given pattern
TO_TIMESTAMP(<expr>, <pattern>)
```

The function converts the first string to a timestamp based on the pattern specified in the second string. To specify the pattern, use specifiers. The specifiers allow you to define the desired format for date and time values. For a comprehensive list of supported specifiers, see [Formatting Date and Time](../../00-sql-reference/10-data-types/datetime.md#formatting-date-and-time).


```sql
-- Convert an integer to a timestamp based on the specified scale
TO_TIMESTAMP(<int>, <scale>)
```

The function converts an integer value to a timestamp, interpreting the integer as the number of seconds (or fractional seconds, based on the specified scale) since the Unix epoch (midnight on January 1, 1970). The scale defines the precision of the fractional seconds and supports values from 0 to 6. For example:

- `scale = 0`: Interprets the integer as seconds.
- `scale = 1`: Interprets the integer as tenths of a second.
- `scale = 6`: Interprets the integer as microseconds.

## Return Type

Returns a timestamp in the format `YYYY-MM-DD hh:mm:ss.ffffff`: 

- The returned timestamp always reflects your Databend timezone.
    - When timezone information is present in the given string, it converts the timestamp to the time corresponding to the timezone configured in Databend. In other words, it adjusts the timestamp to reflect the timezone set in Databend.

    ```sql
    -- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
    SET timezone = 'America/Toronto';

    SELECT TO_TIMESTAMP('2022-01-02T01:12:00-07:00'), TO_TIMESTAMP('2022/01/02T01:12:00-07:00', '%Y/%m/%dT%H:%M:%S%::z');

    ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ to_timestamp('2022-01-02t01:12:00-07:00') │ to_timestamp('2022/01/02t01:12:00-07:00', '%y/%m/%dt%h:%m:%s%::z') │
    ├───────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
    │ 2022-01-02 03:12:00                       │ 2022-01-02 03:12:00                                                │
    └────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

    - In the absence of timezone information in the given string, it assumes the timestamp as belonging to the timezone configured in the current session.

    ```sql
    -- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
    SET timezone = 'America/Toronto';
    
    SELECT TO_TIMESTAMP('2022-01-02T01:12:00'), TO_TIMESTAMP('2022/01/02T01:12:00', '%Y/%m/%dT%H:%M:%S');

    ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ to_timestamp('2022-01-02t01:12:00') │ to_timestamp('2022/01/02t01:12:00', '%y/%m/%dt%h:%m:%s') │
    ├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
    │ 2022-01-02 01:12:00                 │ 2022-01-02 01:12:00                                      │
    └────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

- If the given string matches this format but does not have the time part, it is automatically extended to this pattern. The padding value is 0.
- If the conversion fails, an error will be returned. To avoid such errors, you can use the [TRY_TO_TIMESTAMP](try-to-timestamp.md) function.

    ```sql
    root@localhost:8000/default> SELECT TO_TIMESTAMP('20220102');
    error: APIError: ResponseError with 1006: cannot parse to type `TIMESTAMP` while evaluating function `to_timestamp('20220102')`

    root@localhost:8000/default> SELECT TRY_TO_TIMESTAMP('20220102');

    SELECT
    try_to_timestamp('20220102')

    ┌──────────────────────────────┐
    │ try_to_timestamp('20220102') │
    ├──────────────────────────────┤
    │ NULL                         │
    └──────────────────────────────┘
    ```

## Aliases

- [TO_DATETIME](to-datetime.md)
- [STR_TO_TIMESTAMP](str-to-timestamp.md)

## Examples

### Example-1: Converting String to Timestamp

```sql
SELECT TO_TIMESTAMP('2022-01-02 02:00:11');

┌─────────────────────────────────────┐
│ to_timestamp('2022-01-02 02:00:11') │
├─────────────────────────────────────┤
│ 2022-01-02 02:00:11                 │
└─────────────────────────────────────┘

SELECT TO_TIMESTAMP('2022-01-02T01');

┌───────────────────────────────┐
│ to_timestamp('2022-01-02t01') │
├───────────────────────────────┤
│ 2022-01-02 01:00:00           │
└───────────────────────────────┘

-- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
SET timezone = 'America/Toronto';
-- Convert provided string to current timezone ('America/Toronto')
SELECT TO_TIMESTAMP('2022-01-02T01:12:00-07:00');

┌───────────────────────────────────────────┐
│ to_timestamp('2022-01-02t01:12:00-07:00') │
├───────────────────────────────────────────┤
│ 2022-01-02 03:12:00                       │
└───────────────────────────────────────────┘
```

### Example-2: Converting Integer to Timestamp

```sql
SELECT TO_TIMESTAMP(1), TO_TIMESTAMP(-1);

┌───────────────────────────────────────────┐
│   to_timestamp(1)   │  to_timestamp(- 1)  │
├─────────────────────┼─────────────────────┤
│ 1969-12-31 19:00:01 │ 1969-12-31 18:59:59 │
└───────────────────────────────────────────┘
```

You can also convert an Integer string into a timestamp:

```sql
SELECT TO_TIMESTAMP(TO_INT64('994518299'));

┌─────────────────────────────────────┐
│ to_timestamp(to_int64('994518299')) │
├─────────────────────────────────────┤
│ 2001-07-07 15:04:59                 │
└─────────────────────────────────────┘
```

:::note
- You can use `SELECT TO_TIMESTAMP('994518299', '%s')` for the conversion as well, but it is not recommended. For such conversions, Databend recommends using the method in the example above for better performance.

- A Timestamp value ranges from 1000-01-01 00:00:00.000000 to 9999-12-31 23:59:59.999999. Databend would return an error if you run the following statement:

```bash
root@localhost:8000/default> SELECT TO_TIMESTAMP(9999999999999999999);
error: APIError: ResponseError with 1006: number overflowed while evaluating function `to_int64(9999999999999999999)`
```
:::

### Example-3: Converting String with Pattern

```sql
-- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
SET timezone = 'America/Toronto';

-- Convert provided string to current timezone ('America/Toronto')
SELECT TO_TIMESTAMP('2022/01/02T01:12:00-07:00', '%Y/%m/%dT%H:%M:%S%::z');

┌────────────────────────────────────────────────────────────────────┐
│ to_timestamp('2022/01/02t01:12:00-07:00', '%y/%m/%dt%h:%m:%s%::z') │
├────────────────────────────────────────────────────────────────────┤
│ 2022-01-02 03:12:00                                                │
└────────────────────────────────────────────────────────────────────┘

-- If no timezone is specified, the session's time zone applies.
SELECT TO_TIMESTAMP('2022/01/02T01:12:00', '%Y/%m/%dT%H:%M:%S');

┌──────────────────────────────────────────────────────────┐
│ to_timestamp('2022/01/02t01:12:00', '%y/%m/%dt%h:%m:%s') │
├──────────────────────────────────────────────────────────┤
│ 2022-01-02 01:12:00                                      │
└──────────────────────────────────────────────────────────┘
```

### Example-4: Converting Integer with Scale

```sql
-- Interpret an integer with seconds precision (scale = 0)
SELECT TO_TIMESTAMP(1638473645, 0), TO_TIMESTAMP(-1638473645, 0);

┌─────────────────────────────────────────────────────────────┐
│ to_timestamp(1638473645, 0) │ to_timestamp(- 1638473645, 0) │
├─────────────────────────────┼───────────────────────────────┤
│ 2021-12-02 19:34:05         │ 1918-01-30 04:25:55           │
└─────────────────────────────────────────────────────────────┘

-- Interpret an integer with milliseconds precision (scale = 3)
SELECT TO_TIMESTAMP(1638473645123, 3);

┌────────────────────────────────┐
│ to_timestamp(1638473645123, 3) │
├────────────────────────────────┤
│ 2021-12-02 19:34:05.123        │
└────────────────────────────────┘
```