---
title: Interval
summary: INTERVAL は、自然言語テキスト (`'1 year 2 months'`、`'3 days ago'`) またはマイクロ秒数を表す整数として記述できる期間を表します。{{{ .lake }}} は、千年単位からマイクロ秒単位までの単位をサポートし、interval、日付、timestamp に対する算術演算を可能にします。
---

# Interval

## 概要 {#overview}

`INTERVAL` は、自然言語テキスト (`'1 year 2 months'`、`'3 days ago'`) またはマイクロ秒数を表す整数として記述できる期間を表します。{{{ .lake }}} は、千年単位からマイクロ秒単位までの単位をサポートし、interval、日付、timestamp に対する算術演算を可能にします。

> **Note:**
>
> 数値の interval を解析する際、小数部分は切り捨てられます。`'1.6 seconds'` は 1 秒の interval になります。

## 例 {#examples}

### リテラルと数値 {#literals-and-numeric-values}

```sql
CREATE OR REPLACE TABLE intervals (duration INTERVAL);

INSERT INTO intervals VALUES
  ('1 year 2 months'),       -- positive natural language
  ('1 year 2 months ago'),   -- negative because of "ago"
  ('1000000'),               -- 1 second in microseconds
  ('-1000000');              -- -1 second

SELECT TO_STRING(duration) AS duration_text FROM intervals;
```

結果:

```
┌──────────────────────┐
│ duration_text        │
├──────────────────────┤
│ 1 year 2 months      │
│ -1 year -2 months    │
│ 0:00:01              │
│ -0:00:01             │
└──────────────────────┘
```

```sql
SELECT
  TO_STRING(TO_INTERVAL('1 seconds'))   AS whole,
  TO_STRING(TO_INTERVAL('1.6 seconds')) AS fractional;
```

結果:

```
┌────────┬────────────┐
│ whole  │ fractional │
├────────┼────────────┤
│ 0:00:01 │ 0:00:01   │
└────────┴────────────┘
```

### interval の算術演算 {#interval-arithmetic}

```sql
SELECT
  TO_STRING(TO_DAYS(3) + TO_DAYS(1)) AS add_interval,
  TO_STRING(TO_DAYS(3) - TO_DAYS(1)) AS subtract_interval;
```

結果:

```
┌──────────────┬──────────────────┐
│ add_interval │ subtract_interval │
├──────────────┼──────────────────┤
│ 4 days       │ 2 days           │
└──────────────┴──────────────────┘
```

### DATE と TIMESTAMP への適用 {#apply-to-date-and-timestamp}

```sql
SELECT
  DATE '2024-12-20' + TO_DAYS(2) AS add_days,
  DATE '2024-12-20' - TO_DAYS(2) AS subtract_days,
  TIMESTAMP '2024-12-20 10:00:00' + TO_HOURS(36) AS add_hours,
  TIMESTAMP '2024-12-20 10:00:00' - TO_HOURS(36) AS subtract_hours;
```

結果:

```
┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ add_days           │ subtract_days      │ add_hours          │ subtract_hours     │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ 2024-12-22T00:00:00 │ 2024-12-18T00:00:00 │ 2024-12-21T22:00:00 │ 2024-12-18T22:00:00 │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┘
```

interval は数値と同じように加算または減算できるため、ウィンドウをスライドさせたり、マイクロ秒単位まで正確に制御しながらオフセットを計算したりすることが簡単にできます。