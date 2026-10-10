---
title: CONVERT_TIMEZONE
summary: タイムスタンプをあるタイムゾーンから別のタイムゾーンに変換します。変換先には有効な IANA タイムゾーン名が必要です。
---

# CONVERT_TIMEZONE

`CONVERT_TIMEZONE()` は、タイムスタンプを現在のセッションタイムゾーン（デフォルトは `UTC`）から、第 1 引数で指定したタイムゾーンに変換します。変換先のタイムゾーンは、有効な [IANA timezone name](https://docs.rs/chrono-tz/latest/chrono_tz/enum.Tz.html) である必要があります。

## 構文 {#syntax}

```sql
CONVERT_TIMEZONE(<target_timezone>, <timestamp_expr>)
```

| パラメーター | 説明 |
|----------------------|-----------------------------------------------------------------------------|
| `<target_timezone>`  | `'America/Los_Angeles'` や `'UTC'` などの、大文字と小文字を区別するタイムゾーン名です。 |
| `<timestamp_expr>`   | TIMESTAMP 式（または TIMESTAMP にキャスト可能な値）です。現在のセッションタイムゾーンを使用して解釈されます。 |

## 戻り値の型 {#return-type}

変換先タイムゾーンにおける同じ時点を表す TIMESTAMP 値を返します。

## 動作 {#behavior}

- 変換元のタイムゾーンは常に現在のセッションタイムゾーン（デフォルトは `UTC`）です。変換するデータに合わせて、セッションまたは接続を設定してください。
- 無効なタイムゾーン名を指定するとエラーになります。いずれかの引数が `NULL` の場合、結果は `NULL` になります。
- 夏時間の切り替えによる欠落時間帯では、一部のタイムスタンプが無効になることがあります。`enable_dst_hour_fix = 1`（セッションレベルまたはテナントレベル）を有効にすると、{{{ .lake }}} がそのような値を自動的に調整します。

## 例 {#examples}

### 単一のタイムスタンプを変換する（デフォルトの UTC セッション） {#convert-a-single-timestamp-default-utc-session}

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

### 各ユーザーのタイムゾーンを使って行を変換する {#convert-rows-using-each-user-s-timezone}

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

### DST の欠落時間帯に含まれるタイムスタンプを処理する {#handle-timestamps-inside-dst-gaps}

このセッションでは、タイムゾーンは Asia/Shanghai に設定され、`enable_dst_hour_fix = 1` になっています。`1947-04-15 00:00:00` というタイムスタンプは、時計が進められたためその地域では実在しませんでした。そのため、{{{ .lake }}} は UTC 値を返す前にこれを調整します。

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

## 関連情報 {#see-also}

- [TIMEZONE](/tidb-cloud-lake/sql/timezone.md)
- [TO_TIMESTAMP_TZ](/tidb-cloud-lake/sql/timestamp-tz.md)
- [TO_TIMESTAMP](/tidb-cloud-lake/sql/to-timestamp.md)