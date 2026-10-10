---
title: DATE_PART
summary: 日付またはタイムスタンプの指定した部分を取得します。
---

# DATE_PART

日付またはタイムスタンプの指定した部分を取得します。

関連情報: [EXTRACT](/tidb-cloud-lake/sql/extract.md)

## 構文 {#syntax}

```sql
DATE_PART(
  YEAR | QUARTER | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND |
  DOW | DOY | EPOCH | ISODOW | YEARWEEK | MILLENNIUM,
  <date_or_timestamp_expr>
)
```

| キーワード | 説明 |
|--------------|-------------------------------------------------------------------------|
| `DOW`        | 曜日。日曜日 (0) から土曜日 (6) まで。 |
| `DOY`        | 年間通算日。1 から 366 まで。 |
| `EPOCH`      | 1970-01-01 00:00:00 からの経過秒数。 |
| `ISODOW`     | ISO 曜日。月曜日 (1) から日曜日 (7) まで。 |
| `YEARWEEK`   | ISO 8601 に従った年と週番号の組み合わせ（例: 202415）。 |
| `MILLENNIUM` | 日付が属する千年紀（1 は 1–1000 年、2 は 1001–2000 年、以降同様）。 |

## 戻り値の型 {#return-type}

整数。

## 例 {#examples}

この例では、DATE_PART を使用して、現在のタイムスタンプから年、月、ISO 曜日、年週の組み合わせ、千年紀などのさまざまなコンポーネントを抽出する方法を示します。

```sql
SELECT
  DATE_PART(YEAR, NOW())        AS year_part,
  DATE_PART(QUARTER, NOW())     AS quarter_part,
  DATE_PART(MONTH, NOW())       AS month_part,
  DATE_PART(WEEK, NOW())        AS week_part,
  DATE_PART(DAY, NOW())         AS day_part,
  DATE_PART(HOUR, NOW())        AS hour_part,
  DATE_PART(MINUTE, NOW())      AS minute_part,
  DATE_PART(SECOND, NOW())      AS second_part,
  DATE_PART(DOW, NOW())         AS dow_part,
  DATE_PART(DOY, NOW())         AS doy_part,
  DATE_PART(EPOCH, NOW())       AS epoch_part,
  DATE_PART(ISODOW, NOW())      AS isodow_part,
  DATE_PART(YEARWEEK, NOW())    AS yearweek_part,
  DATE_PART(MILLENNIUM, NOW())  AS millennium_part;
```

```sql
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ year_part │ quarter_part │ month_part │ week_part │ day_part │ hour_part │ minute_part │ second_part │ dow_part │ doy_part │     epoch_part    │ isodow_part │ yearweek_part │ millennium_part │
├───────────┼──────────────┼────────────┼───────────┼──────────┼───────────┼─────────────┼─────────────┼──────────┼──────────┼───────────────────┼─────────────┼───────────────┼─────────────────┤
│      2025 │            2 │          4 │        16 │       16 │        18 │          10 │          10 │        3 │      106 │ 1744827010.257671 │           3 │        202516 │               3 │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```