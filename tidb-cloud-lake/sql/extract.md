---
title: EXTRACT
summary: 日付、タイムスタンプ、または interval の指定された部分を取得します。
---

# EXTRACT

日付、タイムスタンプ、または interval の指定された部分を取得します。

関連情報: [DATE_PART](/tidb-cloud-lake/sql/date-part.md)

## 構文 {#syntax}

```sql
-- Extract from a date or timestamp
EXTRACT(
  YEAR | QUARTER | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND |
  DOW | DOY | EPOCH | ISODOW | YEARWEEK | MILLENNIUM
  FROM <date_or_timestamp>
)

-- Extract from an interval
EXTRACT( YEAR | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND | MICROSECOND ｜ EPOCH FROM <interval> )
```

| キーワード | 説明 |
|--------------|-------------------------------------------------------------------------|
| `DOW`        | 曜日。日曜日 (0) から土曜日 (6) まで。 |
| `DOY`        | 年内通算日。1 から 366 まで。 |
| `EPOCH`      | 1970-01-01 00:00:00 からの秒数。 |
| `ISODOW`     | ISO 曜日。月曜日 (1) から日曜日 (7) まで。 |
| `YEARWEEK`   | ISO 8601 に従った年と週番号の組み合わせ（例: 202415）。 |
| `MILLENNIUM` | 日付が属する千年紀（1 は 1–1000 年、2 は 1001–2000 年、以降同様）。 |

## 戻り値の型 {#return-type}

戻り値の型は、抽出するフィールドによって異なります。

- Integer を返す: 離散的な日付または時刻のコンポーネント（例: YEAR、MONTH、DAY、DOY、HOUR、MINUTE、SECOND）を抽出する場合、この関数は Integer を返します。

    ```sql
    SELECT EXTRACT(DAY FROM now());  -- Returns Integer
    SELECT EXTRACT(DOY FROM now());  -- Returns Integer
    ```

- Float を返す: EPOCH（1970-01-01 00:00:00 UTC からの秒数）を抽出する場合、この関数は小数秒を含む可能性があるため、Float を返します。

    ```sql
    SELECT EXTRACT(EPOCH FROM now());  -- Returns Float
    ```

## 例 {#examples}

次の例では、現在のタイムスタンプからさまざまなフィールドを抽出します。

```sql
SELECT
  NOW(),
  EXTRACT(DAY FROM NOW()),
  EXTRACT(DOY FROM NOW()),
  EXTRACT(EPOCH FROM NOW()),
  EXTRACT(ISODOW FROM NOW()),
  EXTRACT(YEARWEEK FROM NOW()),
  EXTRACT(MILLENNIUM FROM NOW());

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│            now()           │ EXTRACT(DAY FROM now()) │ EXTRACT(DOY FROM now()) │ EXTRACT(EPOCH FROM now()) │ EXTRACT(ISODOW FROM now()) │ EXTRACT(YEARWEEK FROM now()) │ EXTRACT(MILLENNIUM FROM now()) │
├────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────────────┼────────────────────────────┼──────────────────────────────┼────────────────────────────────┤
│ 2025-04-16 18:04:22.773888 │                      16 │                     106 │         1744826662.773888 │                          3 │                       202516 │                              3 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

次の例では、interval から日数を抽出します。

```sql
SELECT EXTRACT(DAY FROM '1 day 2 hours 3 minutes 4 seconds'::INTERVAL);

┌─────────────────────────────────────────────────────────────────┐
│ EXTRACT(DAY FROM '1 day 2 hours 3 minutes 4 seconds'::INTERVAL) │
├─────────────────────────────────────────────────────────────────┤
│                                                               1 │
└─────────────────────────────────────────────────────────────────┘
```