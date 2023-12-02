---
title: Date and Time Functions
summary: Learn how to use the data and time functions.
---

# 日付と時刻の関数 {#date-and-time-functions}

TiDB は、 MySQL 5.7で利用可能な[日付と時刻の関数](https://dev.mysql.com/doc/refman/5.7/en/numeric-functions.html)をサポートします。

> **注記：**
>
> -   MySQL は多くの場合、誤ってフォーマットされた日付と時刻の値を受け入れます。たとえば、 `'2020-01-01\n\t01:01:01'`と`'2020-01_01\n\t01:01'`は有効な日付と時刻の値として扱われます。
> -   TiDB は MySQL の動作に一致するよう最善の努力を払っていますが、すべてのインスタンスで一致するとは限りません。日付を正しくフォーマットすることをお勧めします。これは、誤ってフォーマットされた値に対する意図された動作が文書化されておらず、一貫性がないことが多いためです。

**日付/時刻関数:**

| 名前                                                                                                                                             | 説明                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| [`ADDDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_adddate)                                           | 日付値に時間値 (間隔) を追加する                                |
| [`ADDTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_addtime)                                           | 時間を追加する                                           |
| [`CONVERT_TZ()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_convert-tz)                                     | あるタイムゾーンから別のタイムゾーンに変換する                           |
| [`CURDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_curdate)                                           | 現在の日付を返す                                          |
| [`CURRENT_DATE()` 、 `CURRENT_DATE`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_current-date)                | CURDATE() の同義語                                    |
| [`CURRENT_TIME()` 、 `CURRENT_TIME`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_current-time)                | CURTIME() の同義語                                    |
| [`CURRENT_TIMESTAMP()` 、 `CURRENT_TIMESTAMP`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_current-timestamp) | NOW() の同義語                                        |
| [`CURTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_curtime)                                           | 現在時刻を返す                                           |
| [`DATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date)                                                 | 日付または日時式の日付部分を抽出します。                              |
| [`DATE_ADD()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-add)                                         | 日付値に時間値 (間隔) を追加する                                |
| [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-format)                                   | 指定されたとおりに日付をフォーマットします                             |
| [`DATE_SUB()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-sub)                                         | 日付から時間値 (間隔) を減算します。                              |
| [`DATEDIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_datediff)                                         | 2 つの日付を減算する                                       |
| [`DAY()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_day)                                                   | DAYOFMONTH() の同義語                                 |
| [`DAYNAME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayname)                                           | 曜日の名前を返します                                        |
| [`DAYOFMONTH()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayofmonth)                                     | 日付を返します (0 ～ 31)                                  |
| [`DAYOFWEEK()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayofweek)                                       | 引数の曜日インデックスを返します。                                 |
| [`DAYOFYEAR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayofyear)                                       | 年間通算日 (1 ～ 366) を返します。                            |
| [`EXTRACT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_extract)                                           | 日付の一部を抽出する                                        |
| [`FROM_DAYS()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_from-days)                                       | 日数を日付に変換する                                        |
| [`FROM_UNIXTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_from-unixtime)                               | Unix タイムスタンプを日付としてフォーマットする                        |
| [`GET_FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_get-format)                                     | 日付形式の文字列を返します                                     |
| [`HOUR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_hour)                                                 | 時間を抽出する                                           |
| [`LAST_DAY`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_last-day)                                           | 引数の月の最後の日を返します                                    |
| [`LOCALTIME()` 、 `LOCALTIME`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_localtime)                         | NOW() の同義語                                        |
| [`LOCALTIMESTAMP` 、 `LOCALTIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_localtimestamp)          | NOW() の同義語                                        |
| [`MAKEDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_makedate)                                         | 年と日から日付を作成する                                      |
| [`MAKETIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_maketime)                                         | 時、分、秒から時間を作成する                                    |
| [`MICROSECOND()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_microsecond)                                   | 引数からマイクロ秒を返します                                    |
| [`MINUTE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_minute)                                             | 引数から分を返します                                        |
| [`MONTH()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_month)                                               | 経過した日付から月を返します                                    |
| [`MONTHNAME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_monthname)                                       | 月の名前を返します                                         |
| [`NOW()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_now)                                                   | 現在の日付と時刻を返します                                     |
| [`PERIOD_ADD()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_period-add)                                     | 年-月にピリオドを追加する                                     |
| [`PERIOD_DIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_period-diff)                                   | 期間間の月数を返します                                       |
| [`QUARTER()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_quarter)                                           | 日付引数から四半期を返します                                    |
| [`SEC_TO_TIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_sec-to-time)                                   | 秒を「HH:MM:SS」形式に変換します                              |
| [`SECOND()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_second)                                             | 2 番目を返します (0-59)                                  |
| [`STR_TO_DATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_str-to-date)                                   | 文字列を日付に変換する                                       |
| [`SUBDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_subdate)                                           | 3 つの引数を指定して呼び出された場合の DATE_SUB() の同義語              |
| [`SUBTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_subtime)                                           | 減算回数                                              |
| [`SYSDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_sysdate)                                           | 関数が実行された時刻を返します                                   |
| [`TIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_time)                                                 | 渡された式の時刻部分を抽出します。                                 |
| [`TIME_FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_time-format)                                   | 時刻としてフォーマットする                                     |
| [`TIME_TO_SEC()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_time-to-sec)                                   | 引数を秒に変換して返します                                     |
| [`TIMEDIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timediff)                                         | 減算時間                                              |
| [`TIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestamp)                                       | 引数を 1 つ指定すると、この関数は日付または日時の式を返します。 2 つの引数の場合、引数の合計 |
| [`TIMESTAMPADD()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestampadd)                                 | 日時式に間隔を追加する                                       |
| [`TIMESTAMPDIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestampdiff)                               | 日時式から間隔を減算します。                                    |
| [`TO_DAYS()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_to-days)                                           | 日付引数を日数に変換して返します                                  |
| [`TO_SECONDS()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_to-seconds)                                     | 0 年以降の秒数に変換された date または datetime 引数を返します。         |
| [`UNIX_TIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_unix-timestamp)                             | Unix タイムスタンプを返す                                   |
| [`UTC_DATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_utc-date)                                         | 現在の UTC 日付を返します                                   |
| [`UTC_TIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_utc-time)                                         | 現在の UTC 時間を返します                                   |
| [`UTC_TIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_utc-timestamp)                               | 現在の UTC 日付と時刻を返します                                |
| [`WEEK()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_week)                                                 | 週番号を返す                                            |
| [`WEEKDAY()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_weekday)                                           | 平日インデックスを返す                                       |
| [`WEEKOFYEAR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_weekofyear)                                     | 日付の暦週を返します (1 ～ 53)                               |
| [`YEAR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_year)                                                 | 年を返す                                              |
| [`YEARWEEK()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_yearweek)                                         | 年と週を返します                                          |

詳細は[日付と時刻の関数](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html)を参照してください。

## MySQLの互換性 {#mysql-compatibility}

関数`str_to_date()`は TiDB でサポートされていますが、すべての日付と時刻の値を解析することはできません。さらに、次の日付と時刻の書式設定オプションは**実装されていません**。

| フォーマット          | 説明                                               |
| --------------- | ------------------------------------------------ |
| &quot;%a&quot;  | 曜日の短縮名 (日..土)                                    |
| 「%D」            | 英語の接尾語が付いた日付 (0th、1st、2nd、3rd)                   |
| 「%U」            | 週 (00..53)、日曜日が週の最初の日です。 WEEK() モード 0            |
| 「%u」            | 週 (00..53)。月曜日が週の最初の日です。 WEEK() モード 1            |
| 「%V」            | 週 (01..53)、日曜日が週の最初の日です。 WEEK() モード 2; %X とともに使用 |
| 「%v」            | 週 (01..53)。月曜日が週の最初の日です。 WEEK() モード 3; %x とともに使用 |
| 「%W」            | 曜日名（日曜日～土曜日）                                     |
| 「%w」            | 曜日 (0=日曜日..6=土曜日)                                |
| &quot;％バツ&quot; | 日曜日が週の最初の日となる週の年、数値、4 桁。                         |
| &quot;％バツ&quot; | 週の年。月曜日が週の最初の日となる、4 桁の数値。                        |

詳細については[問題 #30082](https://github.com/pingcap/tidb/issues/30082)参照してください。

## 関連するシステム変数 {#related-system-variables}

`default_week_format`変数は`WEEK()`関数に影響します。
