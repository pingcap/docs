---
title: Date and Time Functions
summary: データと時刻関数の使用方法を学びます。
---

# 日付と時刻関数 {#date-and-time-functions}

TiDB は、MySQL 8.0 で利用可能な[日付と時刻関数](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html)のすべてをサポートします。

> **注記：**
>
> -   MySQL は、多くの場合、形式が正しくない日付と時刻の値を受け入れます。たとえば、 `'2020-01-01\n\t01:01:01'`と`'2020-01_01\n\t01:01'`有効な日付と時刻の値として扱われます。
> -   TiDB は MySQL の動作に一致するように最善を尽くしますが、すべてのインスタンスで一致するとは限りません。日付を正しくフォーマットすることをお勧めします。これは、誤ってフォーマットされた値に対する意図された動作が文書化されておらず、一貫性がないことが多いためです。

**日付/時刻関数:**

| 名前                                                                                                                                             | 説明                                                 |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| [`ADDDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_adddate)                                           | 日付値に時間値（間隔）を追加する                                   |
| [`ADDTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_addtime)                                           | 時間を追加                                              |
| [`CONVERT_TZ()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_convert-tz)                                     | あるタイムゾーンから別のタイムゾーンに変換する                            |
| [`CURDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_curdate)                                           | 現在の日付を返す                                           |
| [`CURRENT_DATE()` 、 `CURRENT_DATE`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_current-date)                | CURDATE() の同義語                                     |
| [`CURRENT_TIME()` 、 `CURRENT_TIME`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_current-time)                | CURTIME() の同義語                                     |
| [`CURRENT_TIMESTAMP()` 、 `CURRENT_TIMESTAMP`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_current-timestamp) | NOW() の同義語                                         |
| [`CURTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_curtime)                                           | 現在の時刻を返す                                           |
| [`DATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date)                                                 | 日付または日付時刻式の日付部分を抽出します                              |
| [`DATE_ADD()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-add)                                         | 日付値に時間値（間隔）を追加する                                   |
| [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-format)                                   | 指定された日付の形式                                         |
| [`DATE_SUB()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-sub)                                         | 日付から時間値（間隔）を減算する                                   |
| [`DATEDIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_datediff)                                         | 2つの日付を減算する                                         |
| [`DAY()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_day)                                                   | DAYOFMONTH() の同義語                                  |
| [`DAYNAME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayname)                                           | 曜日の名前を返す                                           |
| [`DAYOFMONTH()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayofmonth)                                     | 月の日付を返す (0-31)                                     |
| [`DAYOFWEEK()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayofweek)                                       | 引数の曜日インデックスを返す                                     |
| [`DAYOFYEAR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayofyear)                                       | 年の何日目かを返します（1～366）                                 |
| [`EXTRACT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_extract)                                           | 日付の一部を抽出する                                         |
| [`FROM_DAYS()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_from-days)                                       | 日数を日付に変換する                                         |
| [`FROM_UNIXTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_from-unixtime)                               | Unixタイムスタンプを日付としてフォーマットする                          |
| [`GET_FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_get-format)                                     | 日付形式の文字列を返す                                        |
| [`HOUR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_hour)                                                 | 時間を抽出                                              |
| [`LAST_DAY`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_last-day)                                           | 引数の月の最終日を返す                                        |
| [`LOCALTIME()` 、 `LOCALTIME`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_localtime)                         | NOW() の同義語                                         |
| [`LOCALTIMESTAMP` 、 `LOCALTIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_localtimestamp)          | NOW() の同義語                                         |
| [`MAKEDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_makedate)                                         | 年と日から日付を作成する                                       |
| [`MAKETIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_maketime)                                         | 時間、分、秒から時間を作成する                                    |
| [`MICROSECOND()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_microsecond)                                   | 引数からマイクロ秒を返す                                       |
| [`MINUTE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_minute)                                             | 引数から分を返す                                           |
| [`MONTH()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_month)                                               | 経過した日付から月を返す                                       |
| [`MONTHNAME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_monthname)                                       | 月の名前を返す                                            |
| [`NOW()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_now)                                                   | 現在の日付と時刻を返す                                        |
| [`PERIOD_ADD()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_period-add)                                     | 年月間にピリオドを追加する                                      |
| [`PERIOD_DIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_period-diff)                                   | 期間間の月数を返す                                          |
| [`QUARTER()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_quarter)                                           | 日付引数から四半期を返す                                       |
| [`SEC_TO_TIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_sec-to-time)                                   | 秒を「HH:MM:SS」形式に変換します                               |
| [`SECOND()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_second)                                             | 秒を返す (0-59)                                        |
| [`STR_TO_DATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_str-to-date)                                   | 文字列を日付に変換する                                        |
| [`SUBDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_subdate)                                           | 3つの引数で呼び出された場合のDATE_SUB()の同義語                      |
| [`SUBTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_subtime)                                           | 回数を引く                                              |
| [`SYSDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_sysdate)                                           | 関数が実行される時刻を返す                                      |
| [`TIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_time)                                                 | 渡された式の時間部分を抽出します                                   |
| [`TIME_FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_time-format)                                   | 時間としてフォーマット                                        |
| [`TIME_TO_SEC()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_time-to-sec)                                   | 引数を秒数に変換して返します                                     |
| [`TIMEDIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timediff)                                         | 時間を減算する                                            |
| [`TIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestamp)                                       | 引数が1つの場合、この関数は日付または日付時刻式を返します。引数が2つの場合、引数の合計を返します。 |
| [`TIMESTAMPADD()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestampadd)                                 | 日付時刻式に間隔を追加する                                      |
| [`TIMESTAMPDIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestampdiff)                               | 日付時刻式から間隔を減算する                                     |
| [`TO_DAYS()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_to-days)                                           | 日付引数を日数に変換して返します                                   |
| [`TO_SECONDS()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_to-seconds)                                     | 日付または日付時刻引数を0年からの秒数に変換して返します。                      |
| [`UNIX_TIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_unix-timestamp)                             | Unixタイムスタンプを返す                                     |
| [`UTC_DATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_utc-date)                                         | 現在のUTC日付を返す                                        |
| [`UTC_TIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_utc-time)                                         | 現在のUTC時間を返す                                        |
| [`UTC_TIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_utc-timestamp)                               | 現在のUTCの日付と時刻を返します                                  |
| [`WEEK()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_week)                                                 | 週番号を返す                                             |
| [`WEEKDAY()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_weekday)                                           | 曜日インデックスを返す                                        |
| [`WEEKOFYEAR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_weekofyear)                                     | 日付の暦週を返します (1-53)                                  |
| [`YEAR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_year)                                                 | 年を返す                                               |
| [`YEARWEEK()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_yearweek)                                         | 年と週を返す                                             |

詳細は[日付と時刻関数](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html)参照。

## MySQL 互換性 {#mysql-compatibility}

関数`STR_TO_DATE()`は TiDB でサポートされていますが、すべての日付と時刻の値を解析することはできません。また、次の日付と時刻の書式設定オプションは**実装されていません**。

| フォーマット          | 説明                                               |
| --------------- | ------------------------------------------------ |
| 「%a」            | 曜日の略称（日曜～土曜）                                     |
| 「%D」            | 英語の接尾辞付きの月日（0日、1日、2日、3日）                         |
| 「%U」            | 週（00..53）、日曜日が週の最初の日。WEEK() モード 0                |
| 「%u」            | 週 (00..53)、月曜日が週の最初の日。WEEK() モード 1               |
| 「%V」            | 週 (01..53)、日曜日が週の最初の日。WEEK() モード 2。%X とともに使用される。 |
| 「%v」            | 週 (01..53)、月曜日が週の最初の日。WEEK() モード 3。%x とともに使用     |
| 「%W」            | 曜日名（日曜日..土曜日）                                    |
| &quot;%w&quot;  | 曜日 (0=日曜日..6=土曜日)                                |
| &quot;％バツ&quot; | 日曜日を週の最初の日とする週の年、数字、4 桁。                         |
| &quot;％バツ&quot; | 週の年。月曜日が週の最初の日となります。数字 4 桁。                      |

詳細は[問題 #30082](https://github.com/pingcap/tidb/issues/30082)参照してください。

## 関連するシステム変数 {#related-system-variables}

[`default_week_format`](/system-variables.md#default_week_format)変数は`WEEK()`関数に影響します。
