---
title: CONVERT_TIMEZONE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.680"/>

`CONVERT_TIMEZONE()` converts a timestamp from the current session timezone (default `UTC`) to the timezone supplied in the first argument. The destination timezone must be a valid [IANA timezone name](https://docs.rs/chrono-tz/latest/chrono_tz/enum.Tz.html).

## Syntax

```sql
CONVERT_TIMEZONE(<target_timezone>, <timestamp_expr>)
```

| Parameter            | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `<target_timezone>`  | Case-sensitive timezone name such as `'America/Los_Angeles'` or `'UTC'`.    |
| `<timestamp_expr>`   | TIMESTAMP expression (or a value castable to TIMESTAMP). Interpreted using the current session timezone. |

## Return Type

Returns a TIMESTAMP value that represents the same instant in the target timezone.

## Behavior

- The source timezone always equals the current session timezone (default `UTC`). Configure the session or connection to match the data you are converting.
- Invalid timezone names raise an error. If either argument is `NULL`, the result is `NULL`.
- Daylight-saving gaps can make some timestamps invalid. Turn on `enable_dst_hour_fix = 1` (session or tenant level) so Databend adjusts such values automatically.

## Examples

### Convert a single timestamp (default UTC session)

```sql
SELECT CONVERT_TIMEZONE('America/Los_Angeles', '2024-11-01 11:36:10');
```

```
┌──────────────────────────────────────────────────────┐
│ convert_timezone('America/Los_Angeles', '2024-11-01… │
├──────────────────────────────────────────────────────┤
│ 2024-11-01 04:36:10.000000                           │
└──────────────────────────────────────────────────────┘
```

### Convert rows using each user's timezone

```sql
SELECT
    user_tz,
    event_time,
    CONVERT_TIMEZONE(user_tz, event_time) AS local_time
FROM (
    VALUES
        ('America/Los_Angeles', '2024-10-31 22:21:15'::TIMESTAMP),
        ('Asia/Shanghai',       '2024-10-31 22:21:15'::TIMESTAMP),
        (NULL,                  '2024-10-31 22:21:15'::TIMESTAMP)
) AS v(user_tz, event_time)
ORDER BY user_tz NULLS LAST;
```

```
┌──────────────────────┬──────────────────────────────┬──────────────────────────────┐
│ user_tz              │ event_time                   │ local_time                   │
├──────────────────────┼──────────────────────────────┼──────────────────────────────┤
│ America/Los_Angeles  │ 2024-10-31 22:21:15.000000   │ 2024-10-31 15:21:15.000000   │
│ Asia/Shanghai        │ 2024-10-31 22:21:15.000000   │ 2024-11-01 06:21:15.000000   │
│ NULL                 │ 2024-10-31 22:21:15.000000   │ NULL                         │
└──────────────────────┴──────────────────────────────┴──────────────────────────────┘
```

### Handle timestamps inside DST gaps

In this session the timezone is configured as Asia/Shanghai and `enable_dst_hour_fix = 1`. The timestamp `1947-04-15 00:00:00` never existed there because clocks jumped forward, so Databend adjusts it before returning the UTC value.

```sql
SELECT CONVERT_TIMEZONE('UTC', '1947-04-15 00:00:00');
```

```
┌──────────────────────────────────────────────┐
│ convert_timezone('UTC', '1947-04-15 00:00:00')│
├──────────────────────────────────────────────┤
│ 1947-04-14 15:00:00.000000                   │
└──────────────────────────────────────────────┘
```

## See Also

- [TIMEZONE](timezone.md)
- [TO_TIMESTAMP_TZ](to-timestamp-tz.md)
- [TO_TIMESTAMP](to-timestamp.md)
