---
title: TO_TIMESTAMP_TZ
summary: 値を TIMESTAMP_TZ に変換し、UTC 時刻とタイムゾーンオフセットの両方を保持します。エラーの代わりに NULL を返したい場合は TRY_TO_TIMESTAMP_TZ を使用します。
---

# TO_TIMESTAMP_TZ

値を [`TIMESTAMP_TZ`](/tidb-cloud-lake/sql/date-time.md#timestamp_tz) に変換し、UTC 時刻とタイムゾーンオフセットの両方を保持します。エラーの代わりに `NULL` を返したい場合は、`TRY_TO_TIMESTAMP_TZ` を使用します。

## 構文 {#syntax}

```sql
TO_TIMESTAMP_TZ(<expr>)
```

`<expr>` には、ISO-8601 形式の文字列（`YYYY-MM-DD`、`YYYY-MM-DDTHH:MM:SS[.fraction][±offset]`）、`TIMESTAMP`、または `DATE` を指定できます。

## 戻り値の型 {#return-type}

`TIMESTAMP_TZ`

## 例 {#examples}

### 明示的なオフセットを含む文字列を解析する {#parse-a-string-with-an-explicit-offset}

```sql
SELECT TO_TIMESTAMP_TZ('2021-12-20 17:01:01.000000 +0000')::STRING AS utc_example;

┌──────────────────────────────────────────┐
│ utc_example                              │
├──────────────────────────────────────────┤
│ 2021-12-20 17:01:01.000000 +0000         │
└──────────────────────────────────────────┘
```

### TIMESTAMP を昇格する {#promote-a-timestamp}

```sql
SELECT TO_TIMESTAMP_TZ(TO_TIMESTAMP('2021-12-20 17:01:01.000000'))::STRING AS from_timestamp;

┌──────────────────────────────────────────┐
│ from_timestamp                           │
├──────────────────────────────────────────┤
│ 2021-12-20 17:01:01.000000 +0000         │
└──────────────────────────────────────────┘
```

### TIMESTAMP に戻す {#convert-back-to-timestamp}

```sql
SELECT TO_TIMESTAMP(TO_TIMESTAMP_TZ('2021-12-20 17:01:01.000000 +0800')) AS back_to_timestamp;

┌────────────────────────┐
│ back_to_timestamp      │
├────────────────────────┤
│ 2021-12-20T09:01:01    │
└────────────────────────┘
```