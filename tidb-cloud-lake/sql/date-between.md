---
title: DATE_BETWEEN
summary: 2 つの日付またはタイムスタンプの間の時間間隔を計算し、指定した単位での差を整数で返します。1 つ目の時刻が 2 つ目より前の場合は正の値、逆の場合は負の値を返します。
---

# DATE_BETWEEN

2 つの日付またはタイムスタンプの間の時間間隔を計算し、指定した単位での差を整数で返します。1 つ目の時刻が 2 つ目より前の場合は正の値、逆の場合は負の値を返します。

関連情報: [DATE_DIFF](/tidb-cloud-lake/sql/date-diff.md)

## 構文 {#syntax}

```sql
DATE_BETWEEN(
  YEAR | QUARTER | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND |
  DOW | DOY | EPOCH | ISODOW | YEARWEEK | MILLENNIUM,
  <start_date_or_timestamp>,
  <end_date_or_timestamp>
)
```

| キーワード | 説明 |
|--------------|-------------------------------------------------------------------------|
| `DOW`        | 曜日。日曜日 (0) から土曜日 (6) まで。 |
| `DOY`        | 年内通算日。1 から 366 まで。 |
| `EPOCH`      | 1970-01-01 00:00:00 からの経過秒数。 |
| `ISODOW`     | ISO 曜日。月曜日 (1) から日曜日 (7) まで。 |
| `YEARWEEK`   | ISO 8601 に従った年と週番号の組み合わせ（例: 202415）。 |
| `MILLENNIUM` | 日付が属する千年紀（1 は 1–1000 年、2 は 1001–2000 年、以降同様）。 |

## DATE_DIFF と DATE_BETWEEN の違い {#date-diff-vs-date-between}

`DATE_DIFF` 関数は、2 つの日付の間でユーザー指定の単位（day、month、year など）の境界をいくつまたぐかを数えます。一方、`DATE_BETWEEN` は、その間に厳密に含まれる完全な単位の数を数えます。例:

```sql
SELECT
    DATE_DIFF(month, '2025-07-31', '2025-10-01'),    -- returns 3
    DATE_BETWEEN(month, '2025-07-31', '2025-10-01'); -- returns 2
```

この例では、`DATE_DIFF` は 3 つの月境界（July → August → September → October）をまたぐため `3` を返します。一方、`DATE_BETWEEN` は日付の間に完全な 2 か月分、つまり August と September が含まれるため `2` を返します。

## 例 {#examples}

この例では、固定のタイムスタンプ (`2020-01-01 00:00:00`) と現在のタイムスタンプ (`NOW()`) の差を、year、ISO weekday、year-week、millennium などのさまざまな単位で計算します。

```sql
SELECT
  DATE_BETWEEN(YEAR,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_year,
  DATE_BETWEEN(QUARTER,     TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_quarter,
  DATE_BETWEEN(MONTH,       TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_month,
  DATE_BETWEEN(WEEK,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_week,
  DATE_BETWEEN(DAY,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_day,
  DATE_BETWEEN(HOUR,        TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_hour,
  DATE_BETWEEN(MINUTE,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_minute,
  DATE_BETWEEN(SECOND,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_second,
  DATE_BETWEEN(DOW,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_dow,
  DATE_BETWEEN(DOY,         TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_doy,
  DATE_BETWEEN(EPOCH,       TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_epoch,
  DATE_BETWEEN(ISODOW,      TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_isodow,
  DATE_BETWEEN(YEARWEEK,    TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_yearweek,
  DATE_BETWEEN(MILLENNIUM,  TIMESTAMP '2020-01-01 00:00:00', NOW())        AS diff_millennium;
```

```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ diff_year │ diff_quarter │ diff_month │ diff_week │ diff_day │ diff_hour │ diff_minute │ diff_second │ diff_dow │ diff_doy │ diff_epoch │ diff_isodow │ diff_yearweek │ diff_millennium │
├───────────┼──────────────┼────────────┼───────────┼──────────┼───────────┼─────────────┼─────────────┼──────────┼──────────┼────────────┼─────────────┼───────────────┼─────────────────┤
│         5 │           21 │         63 │       276 │     1933 │     46414 │     2784887 │   167093234 │     1933 │     1933 │  167093234 │        1933 │           276 │               0 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```