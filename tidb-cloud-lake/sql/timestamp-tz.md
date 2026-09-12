---
title: TO_TIMESTAMP_TZ
summary: 将一个值转换为 TIMESTAMP_TZ，同时保留 UTC 时刻和时区偏移。如果你希望在出错时返回 NULL 而不是报错，请使用 TRY_TO_TIMESTAMP_TZ。
---

# TO_TIMESTAMP_TZ

将一个值转换为 [`TIMESTAMP_TZ`](/tidb-cloud-lake/sql/date-time.md#timestamp_tz)，同时保留 UTC 时刻和时区偏移。如果你希望在出错时返回 `NULL` 而不是报错，请使用 `TRY_TO_TIMESTAMP_TZ`。

## 语法 {#syntax}

```sql
TO_TIMESTAMP_TZ(<expr>)
```

`<expr>` 可以是 ISO-8601 风格的字符串（`YYYY-MM-DD`、`YYYY-MM-DDTHH:MM:SS[.fraction][±offset]`）、`TIMESTAMP` 或 `DATE`。

## 返回类型 {#return-type}

`TIMESTAMP_TZ`

## 示例 {#examples}

### 解析带有显式偏移的字符串 {#parse-a-string-with-an-explicit-offset}

```sql
SELECT TO_TIMESTAMP_TZ('2021-12-20 17:01:01.000000 +0000')::STRING AS utc_example;

┌──────────────────────────────────────────┐
│ utc_example                              │
├──────────────────────────────────────────┤
│ 2021-12-20 17:01:01.000000 +0000         │
└──────────────────────────────────────────┘
```

### 提升为 TIMESTAMP {#promote-a-timestamp}

```sql
SELECT TO_TIMESTAMP_TZ(TO_TIMESTAMP('2021-12-20 17:01:01.000000'))::STRING AS from_timestamp;

┌──────────────────────────────────────────┐
│ from_timestamp                           │
├──────────────────────────────────────────┤
│ 2021-12-20 17:01:01.000000 +0000         │
└──────────────────────────────────────────┘
```

### 转换回 TIMESTAMP {#convert-back-to-timestamp}

```sql
SELECT TO_TIMESTAMP(TO_TIMESTAMP_TZ('2021-12-20 17:01:01.000000 +0800')) AS back_to_timestamp;

┌────────────────────────┐
│ back_to_timestamp      │
├────────────────────────┤
│ 2021-12-20T09:01:01    │
└────────────────────────┘
```