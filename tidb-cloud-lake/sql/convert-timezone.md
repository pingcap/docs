---
title: CONVERT_TIMEZONE
summary: 将时间戳从一个时区转换到另一个时区，并且要求目标时区名称是有效的 IANA 时区名称。
---

# CONVERT_TIMEZONE

`CONVERT_TIMEZONE()` 将时间戳从当前会话时区（默认 `UTC`）转换为第一个参数中提供的时区。目标时区必须是有效的 [IANA timezone name](https://docs.rs/chrono-tz/latest/chrono_tz/enum.Tz.html)。

## 语法 {#syntax}

```sql
CONVERT_TIMEZONE(<target_timezone>, <timestamp_expr>)
```

| 参数                 | 描述                                                                        |
|----------------------|-----------------------------------------------------------------------------|
| `<target_timezone>`  | 大小写敏感的时区名称，例如 `'America/Los_Angeles'` 或 `'UTC'`。             |
| `<timestamp_expr>`   | TIMESTAMP 表达式（或可转换为 TIMESTAMP 的值）。使用当前会话时区进行解释。   |

## 返回类型 {#return-type}

返回一个 TIMESTAMP 值，表示目标时区中的同一时刻。

## 行为 {#behavior}

- 源时区始终等于当前会话时区（默认 `UTC`）。请将会话或连接配置为与你要转换的数据相匹配。
- 无效的时区名称会引发错误。如果任一参数为 `NULL`，结果为 `NULL`。
- 夏令时缺口可能会导致某些时间戳无效。开启 `enable_dst_hour_fix = 1`（会话或租户级别）后，{{{ .lake }}} 会自动调整此类值。

## 示例 {#examples}

### 转换单个时间戳（默认 UTC 会话） {#convert-a-single-timestamp-default-utc-session}

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

### 使用每个用户的时区转换行数据 {#convert-rows-using-each-user-s-timezone}

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

### 处理 DST 缺口中的时间戳 {#handle-timestamps-inside-dst-gaps}

在此会话中，时区配置为 Asia/Shanghai，且 `enable_dst_hour_fix = 1`。时间戳 `1947-04-15 00:00:00` 在该时区中实际上从未存在，因为时钟曾向前跳变，因此 {{{ .lake }}} 会在返回 UTC 值之前先对其进行调整。

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

## 另请参阅 {#see-also}

- [TIMEZONE](/tidb-cloud-lake/sql/timezone.md)
- [TO_TIMESTAMP_TZ](/tidb-cloud-lake/sql/timestamp-tz.md)
- [TO_TIMESTAMP](/tidb-cloud-lake/sql/to-timestamp.md)