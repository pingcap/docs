---
title: Interval Functions
summary: このセクションでは、{{{ .lake }}} の interval 関数に関するリファレンス情報を提供します。interval 関数を使用すると、日付および時刻の計算で使用するさまざまな時間単位の interval 値を作成できます。
---

# Interval Functions

このセクションでは、{{{ .lake }}} の interval 関数に関するリファレンス情報を提供します。interval 関数を使用すると、日付および時刻の計算で使用するさまざまな時間単位の interval 値を作成できます。

## 時間単位変換関数 {#time-unit-conversion-functions}

### 日単位の interval {#day-based-intervals}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [TO_DAYS](/tidb-cloud-lake/sql/days.md) | 数値を日単位の interval に変換します | `TO_DAYS(2)` → `2 days` |
| [TO_WEEKS](/tidb-cloud-lake/sql/weeks.md) | 数値を週単位の interval に変換します | `TO_WEEKS(3)` → `21 days` |
| [TO_MONTHS](/tidb-cloud-lake/sql/months.md) | 数値を月単位の interval に変換します | `TO_MONTHS(2)` → `2 months` |
| [TO_YEARS](/tidb-cloud-lake/sql/years.md) | 数値を年単位の interval に変換します | `TO_YEARS(1)` → `1 year` |

### 時間単位の interval {#hour-based-intervals}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [TO_HOURS](/tidb-cloud-lake/sql/hours.md) | 数値を時間単位の interval に変換します | `TO_HOURS(5)` → `5:00:00` |
| [TO_MINUTES](/tidb-cloud-lake/sql/minutes.md) | 数値を分単位の interval に変換します | `TO_MINUTES(90)` → `1:30:00` |
| [TO_SECONDS](/tidb-cloud-lake/sql/seconds.md) | 数値を秒単位の interval に変換します | `TO_SECONDS(3600)` → `1:00:00` |
| [EPOCH](/tidb-cloud-lake/sql/epoch.md) | TO_SECONDS のエイリアスです | `EPOCH(60)` → `00:01:00` |

### より小さい時間単位 {#smaller-time-units}

| Function | 説明 | 例 |
|----------|-------------|--------|
| [TO_MILLISECONDS](/tidb-cloud-lake/sql/milliseconds.md) | 数値をミリ秒単位の interval に変換します | `TO_MILLISECONDS(2000)` → `00:00:02` |
| [TO_MICROSECONDS](/tidb-cloud-lake/sql/microseconds.md) | 数値をマイクロ秒単位の interval に変換します | `TO_MICROSECONDS(2000000)` → `00:00:02` |

### より大きい時間単位 {#larger-time-units}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [TO_DECADES](/tidb-cloud-lake/sql/decades.md) | 数値を十年単位の interval に変換します | `TO_DECADES(2)` → `20 years` |
| [TO_CENTRIES](/tidb-cloud-lake/sql/to-centuries.md) | 数値を世紀単位の interval に変換します | `TO_CENTRIES(1)` → `100 years` |
| [TO_MILLENNIA](/tidb-cloud-lake/sql/millennia.md) | 数値を千年単位の interval に変換します | `TO_MILLENNIA(1)` → `1000 years` |