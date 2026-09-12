---
title: TIMEZONE
summary: 返回当前连接的时区。
---

# TIMEZONE

返回当前连接的时区。

{{{ .lake }}} 默认使用 UTC（协调世界时）作为时区，并允许你将时区更改为你当前的地理位置。有关可赋给 `timezone` 设置的可用值，请参阅 <https://docs.rs/chrono-tz/latest/chrono_tz/enum.Tz.html>。详情请参见下面的示例。

## 语法 {#syntax}

```
SELECT TIMEZONE();
```

## 示例 {#examples}

```sql
-- Return the current timezone
SELECT TIMEZONE();

┌────────────┐
│ timezone() │
├────────────┤
│ UTC        │
└────────────┘

-- Set the timezone to China Standard Time
SET timezone='Asia/Shanghai';

SELECT TIMEZONE();

┌───────────────┐
│   timezone()  │
├───────────────┤
│ Asia/Shanghai │
└───────────────┘
```