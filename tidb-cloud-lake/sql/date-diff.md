---
title: DATE_DIFF
summary: 指定した時間単位に基づいて、2 つの日付またはタイムスタンプの差を計算します。`<end_date>` が `<start_date>` より後の場合は結果は正になり、前の場合は負になります。
---

# DATE_DIFF

指定した時間単位に基づいて、2 つの日付またはタイムスタンプの差を計算します。`<end_date>` が `<start_date>` より後の場合は結果は正になり、前の場合は負になります。

関連情報: [DATE_BETWEEN](/tidb-cloud-lake/sql/date-between.md)

## 構文 {#syntax}

```sql
DATE_DIFF(
  YEAR | QUARTER | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND |
  DOW | DOY | EPOCH | ISODOW | YEARWEEK | MILLENNIUM,
  <start_date_or_timestamp>,
  <end_date_or_timestamp>
)
```

| キーワード | 説明 |
|--------------|-------------------------------------------------------------------------|
| `DOW`        | 曜日。日曜日 (0) から土曜日 (6) まで。                       |
| `DOY`        | 年間通算日。1 から 366 まで。                                         |
| `EPOCH`      | 1970-01-01 00:00:00 からの秒数。                        |
| `ISODOW`     | ISO 曜日。月曜日 (1) から日曜日 (7) まで。                     |
| `YEARWEEK`   | ISO 8601 に従った年と週番号の組み合わせ（例: 202415）。   |
| `MILLENNIUM` | 日付が属する千年紀（1 は 1–1000 年、2 は 1001–2000 年、など）。 |

## DATE_DIFF と DATE_BETWEEN の違い {#date-diff-vs-date-between}

`DATE_DIFF` 関数は、2 つの日付の間でユーザーが指定した単位（たとえば日、月、年）の境界をいくつまたぐかを数えます。一方、`DATE_BETWEEN` は、その間に厳密に含まれる完全な単位の数を数えます。例:

```sql
SELECT
    DATE_DIFF(month, '2025-07-31', '2025-10-01'),    -- returns 3
    DATE_BETWEEN(month, '2025-07-31', '2025-10-01'); -- returns 2
```

この例では、`DATE_DIFF` は 3 つの月境界（July → August → September → October）をまたぐため `3` を返します。一方、`DATE_BETWEEN` は日付の間に完全な 2 か月分、つまり August と September が含まれるため `2` を返します。

## 例 {#examples}

この例では、固定のタイムスタンプ (`2020-01-01 00:00:00`) と現在のタイムスタンプ (`NOW()`) の差を、年、ISO 曜日、年週、千年紀などのさまざまな単位で計算します。

```sql
SELECT
  DATE_DIFF(YEAR,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_year,
  DATE_DIFF(QUARTER,     TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_quarter,
  DATE_DIFF(MONTH,       TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_month,
  DATE_DIFF(WEEK,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_week,
  DATE_DIFF(DAY,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_day,
  DATE_DIFF(HOUR,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_hour,
  DATE_DIFF(MINUTE,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_minute,
  DATE_DIFF(SECOND,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_second,
  DATE_DIFF(DOW,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_dow,
  DATE_DIFF(DOY,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_doy,
  DATE_DIFF(EPOCH,       TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_epoch,
  DATE_DIFF(ISODOW,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_isodow,
  DATE_DIFF(YEARWEEK,    TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_yearweek,
  DATE_DIFF(MILLENNIUM,  TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_millennium;
```

```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ diff_year │ diff_quarter │ diff_month │ diff_week │ diff_day │ diff_hour │ diff_minute │ diff_second │ diff_dow │ diff_doy │ diff_epoch │ diff_isodow │ diff_yearweek │ diff_millennium │
├───────────┼──────────────┼────────────┼───────────┼──────────┼───────────┼─────────────┼─────────────┼──────────┼──────────┼────────────┼─────────────┼───────────────┼─────────────────┤
│         5 │           21 │         63 │       276 │     1932 │     46386 │     2783184 │   166991069 │     1932 │     1932 │  166991069 │        1932 │           515 │               0 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```