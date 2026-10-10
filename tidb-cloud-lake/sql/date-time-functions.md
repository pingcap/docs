---
title: 日付・時刻関数
summary: このページでは、{{{ .lake }}} の日付・時刻関数について、参照しやすいように機能別に整理して包括的に紹介します。
---

# 日付・時刻関数

このページでは、{{{ .lake }}} の日付・時刻関数について、参照しやすいように機能別に整理して包括的に紹介します。

## 現在の日付・時刻関数 {#current-date-time-functions}

| Function                                  | Description                  | Example                                              |
|-------------------------------------------|------------------------------|------------------------------------------------------|
| [NOW](/tidb-cloud-lake/sql/now.md)                             | 現在の日付と時刻を返します   | `NOW()` → `2024-06-04 17:42:31.123456`               |
| [CURRENT_TIMESTAMP](/tidb-cloud-lake/sql/current-timestamp.md) | 現在の日付と時刻を返します   | `CURRENT_TIMESTAMP()` → `2024-06-04 17:42:31.123456` |
| [TODAY](/tidb-cloud-lake/sql/today.md)                         | 現在の日付を返します         | `TODAY()` → `2024-06-04`                             |
| [TOMORROW](/tidb-cloud-lake/sql/tomorrow.md)                   | 翌日の日付を返します         | `TOMORROW()` → `2024-06-05`                          |
| [YESTERDAY](/tidb-cloud-lake/sql/yesterday.md)                 | 前日の日付を返します         | `YESTERDAY()` → `2024-06-03`                         |

## 日付・時刻の抽出関数 {#date-time-extraction-functions}

| 関数                                      | 説明                          | 例                                  |
|-----------------------------------------------|--------------------------------------|------------------------------------------|
| [YEAR](/tidb-cloud-lake/sql/year.md)                               | 日付から年を抽出します               | `YEAR('2024-06-04')` → `2024`            |
| [MONTH](/tidb-cloud-lake/sql/month.md)                             | 日付から月を抽出します               | `MONTH('2024-06-04')` → `6`              |
| [DAY](/tidb-cloud-lake/sql/day.md)                                 | 日付から日を抽出します               | `DAY('2024-06-04')` → `4`                |
| [QUARTER](/tidb-cloud-lake/sql/quarter.md)                         | 日付から四半期を抽出します           | `QUARTER('2024-06-04')` → `2`            |
| [WEEK](/tidb-cloud-lake/sql/week.md) / [WEEKOFYEAR](/tidb-cloud-lake/sql/weekofyear.md) | 日付から週番号を抽出します           | `WEEK('2024-06-04')` → `23`              |
| [EXTRACT](/tidb-cloud-lake/sql/extract.md)                         | 日付から一部を抽出します             | `EXTRACT(MONTH FROM '2024-06-04')` → `6` |
| [DATE_PART](/tidb-cloud-lake/sql/date-part.md)                     | 日付から一部を抽出します             | `DATE_PART('month', '2024-06-04')` → `6` |
| [YEARWEEK](/tidb-cloud-lake/sql/yearweek.md)                       | 年と週番号を返します                 | `YEARWEEK('2024-06-04')` → `202423`      |
| [MILLENNIUM](/tidb-cloud-lake/sql/millennium.md)                   | 日付からミレニアムを返します         | `MILLENNIUM('2024-06-04')` → `3`         |

## 日付・時刻の変換関数 {#date-time-conversion-functions}

| 関数                                  | 説明                                 | 例                                                       |
|-------------------------------------------|---------------------------------------------|---------------------------------------------------------------|
| [DATE](/tidb-cloud-lake/sql/date.md)                           | 値を DATE 型に変換します                    | `DATE('2024-06-04')` → `2024-06-04`                           |
| [TO_DATE](/tidb-cloud-lake/sql/to-date.md)                     | 文字列を DATE 型に変換します                | `TO_DATE('2024-06-04')` → `2024-06-04`                        |
| [TO_DATETIME](/tidb-cloud-lake/sql/datetime.md)             | 文字列を DATETIME 型に変換します            | `TO_DATETIME('2024-06-04 12:30:45')` → `2024-06-04 12:30:45`  |
| [TO_TIMESTAMP](/tidb-cloud-lake/sql/to-timestamp.md)           | 文字列を TIMESTAMP 型に変換します           | `TO_TIMESTAMP('2024-06-04 12:30:45')` → `2024-06-04 12:30:45` |
| [TO_UNIX_TIMESTAMP](/tidb-cloud-lake/sql/unix-timestamp.md) | 日付を Unix timestamp に変換します          | `TO_UNIX_TIMESTAMP('2024-06-04')` → `1717516800`              |
| [TO_YYYYMM](/tidb-cloud-lake/sql/yyyymm.md)                 | 日付を YYYYMM 形式にフォーマットします      | `TO_YYYYMM('2024-06-04')` → `202406`                          |
| [TO_YYYYMMDD](/tidb-cloud-lake/sql/yyyymmdd.md)             | 日付を YYYYMMDD 形式にフォーマットします    | `TO_YYYYMMDD('2024-06-04')` → `20240604`                      |
| [TO_YYYYMMDDHH](/tidb-cloud-lake/sql/yyyymmddhh.md)         | 日付を YYYYMMDDHH 形式にフォーマットします  | `TO_YYYYMMDDHH('2024-06-04 12:30:45')` → `2024060412`         |
| [TO_YYYYMMDDHHMMSS](/tidb-cloud-lake/sql/yyyymmddhhmmss.md) | 日付を YYYYMMDDHHMMSS 形式にフォーマットします | `TO_YYYYMMDDHHMMSS('2024-06-04 12:30:45')` → `20240604123045` |
| [DATE_FORMAT](/tidb-cloud-lake/sql/date-format.md)             | フォーマット文字列に従って日付を整形します  | `DATE_FORMAT('2024-06-04', '%Y-%m-%d')` → `'2024-06-04'`      |
| [CONVERT_TIMEZONE](/tidb-cloud-lake/sql/convert-timezone.md)   | timestamp を対象のタイムゾーンに変換します  | `CONVERT_TIMEZONE('America/Los_Angeles', '2024-11-01 11:36:10')` → `2024-10-31 20:36:10` |

## 日付・時刻の算術関数 {#date-time-arithmetic-functions}

| 関数                                       | 説明                                                                                           | 例                                                                                     |
|------------------------------------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| [DATE_ADD](/tidb-cloud-lake/sql/date-add.md)                  | 日付に時間間隔を加算します                                                                   | `DATE_ADD(DAY, 7, '2024-06-04')` → `2024-06-11`                                      |
| [DATE_SUB](/tidb-cloud-lake/sql/date-sub.md)                  | 日付から時間間隔を減算します                                                                 | `DATE_SUB(MONTH, 1, '2024-06-04')` → `2024-05-04`                                    |
| [ADD INTERVAL](/tidb-cloud-lake/sql/add-interval.md)           | 日付に interval を加算します                                                                 | `'2024-06-04' + INTERVAL 1 DAY` → `2024-06-05`                                       |
| [SUBTRACT INTERVAL](/tidb-cloud-lake/sql/subtract-interval.md) | 日付から interval を減算します                                                               | `'2024-06-04' - INTERVAL 1 MONTH` → `2024-05-04`                                     |
| [DATE_DIFF](/tidb-cloud-lake/sql/date-diff.md)                | 2 つの日付の差を返します                                                                     | `DATE_DIFF(DAY, '2024-06-01', '2024-06-04')` → `3`                                   |
| [TIMESTAMP_DIFF](/tidb-cloud-lake/sql/timestamp-diff.md)      | 2 つの timestamp の差を返します                                                              | `TIMESTAMP_DIFF(HOUR, '2024-06-04 10:00:00', '2024-06-04 15:00:00')` → `5`           |
| [MONTHS_BETWEEN](/tidb-cloud-lake/sql/months-between.md)      | 2 つの日付の間の月数を返します                                                               | `MONTHS_BETWEEN('2024-06-04', '2024-01-04')` → `5`                                   |
| [DATE_BETWEEN](/tidb-cloud-lake/sql/date-between.md)          | ある日付が他の 2 つの日付の間にあるかを確認します                                            | `DATE_BETWEEN('2024-06-04', '2024-06-01', '2024-06-10')` → `true`                    |
| [AGE](/tidb-cloud-lake/sql/age.md)                            | timestamp 同士、または timestamp と現在の日付/時刻との差を計算します                         | `AGE('2000-01-01'::TIMESTAMP, '1990-05-15'::TIMESTAMP)` → `9 years 7 months 17 days` |
| [ADD_MONTHS](/tidb-cloud-lake/sql/add-months.md)              | 月末日を維持しながら、日付に月を加算します。                                                 | `ADD_MONTHS('2025-04-30',1)` → `2025-05-31`                                          |

## 日付・時刻の切り捨て関数 {#date-time-truncation-functions}

| 関数                                      | 説明                                                      | 例                                                             |
|-----------------------------------------------|------------------------------------------------------------------|---------------------------------------------------------------------|
| [DATE_TRUNC](/tidb-cloud-lake/sql/date-trunc.md)                   | timestamp を指定した精度に切り捨てます                           | `DATE_TRUNC('month', '2024-06-04')` → `2024-06-01`                  |
| [TIME_SLICE](/tidb-cloud-lake/sql/time-slice.md)                   | 単一の日付/timestamp 値をカレンダーに整列した interval にマッピングします | `TIME_SLICE('2024-06-04', 4, 'MONTH', 'START')` → `2024-05-01`      |
| [TO_START_OF_DAY](/tidb-cloud-lake/sql/to-start-of-day.md)         | その日の開始時刻を返します                                       | `TO_START_OF_DAY('2024-06-04 12:30:45')` → `2024-06-04 00:00:00`    |
| [TO_START_OF_HOUR](/tidb-cloud-lake/sql/to-start-of-hour.md)       | その時間の開始時刻を返します                                     | `TO_START_OF_HOUR('2024-06-04 12:30:45')` → `2024-06-04 12:00:00`   |
| [TO_START_OF_MINUTE](/tidb-cloud-lake/sql/to-start-of-minute.md)   | その分の開始時刻を返します                                       | `TO_START_OF_MINUTE('2024-06-04 12:30:45')` → `2024-06-04 12:30:00` |
| [TO_START_OF_MONTH](/tidb-cloud-lake/sql/to-start-of-month.md)     | その月の開始日を返します                                         | `TO_START_OF_MONTH('2024-06-04')` → `2024-06-01`                    |
| [TO_START_OF_QUARTER](/tidb-cloud-lake/sql/to-start-of-quarter.md) | その四半期の開始日を返します                                     | `TO_START_OF_QUARTER('2024-06-04')` → `2024-04-01`                  |
| [TO_START_OF_YEAR](/tidb-cloud-lake/sql/to-start-of-year.md)       | その年の開始日を返します                                         | `TO_START_OF_YEAR('2024-06-04')` → `2024-01-01`                     |
| [TO_START_OF_WEEK](/tidb-cloud-lake/sql/to-start-of-week.md)       | その週の開始日を返します                                         | `TO_START_OF_WEEK('2024-06-04')` → `2024-06-03`                     |

## 日付・時刻のナビゲーション関数 {#date-time-navigation-functions}

| 関数                              | 説明                                                 | 例                                                    |
|---------------------------------|----------------------------------------------------|-------------------------------------------------------|
| [LAST_DAY](/tidb-cloud-lake/sql/last-day.md)         | その月の最終日を返します                           | `LAST_DAY('2024-06-04')` → `2024-06-30`               |
| [NEXT_DAY](/tidb-cloud-lake/sql/next-day.md)         | 指定した曜日の次の日付を返します                   | `NEXT_DAY('2024-06-04', 'SUNDAY')` → `2024-06-09`     |
| [PREVIOUS_DAY](/tidb-cloud-lake/sql/previous-day.md) | 指定した曜日の前の日付を返します                   | `PREVIOUS_DAY('2024-06-04', 'MONDAY')` → `2024-06-03` |

## その他の日付・時刻関数 {#other-date-time-functions}

| 関数                  | 説明                  | 例                                                                  |
|---------------------------|------------------------------|--------------------------------------------------------------------------|
| [TIMEZONE](/tidb-cloud-lake/sql/timezone.md)   | 現在のタイムゾーンを返します | `TIMEZONE()` → `'UTC'`                                                   |
| [TIME_SLOT](/tidb-cloud-lake/sql/time-slot.md) | 時間スロットを返します       | `TIME_SLOT('2024-06-04 12:30:45', 15, 'MINUTE')` → `2024-06-04 12:30:00` |