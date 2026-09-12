---
title: 日期与时间函数
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的日期与时间函数，便于快速查阅。
---

# 日期与时间函数

本页按功能分类，全面概述了 {{{ .lake }}} 中的日期与时间函数，便于快速查阅。

## 当前日期与时间函数 {#current-date-time-functions}

| Function                                  | 描述                   | 示例                                                 |
|-------------------------------------------|------------------------|------------------------------------------------------|
| [NOW](/tidb-cloud-lake/sql/now.md)                             | 返回当前日期和时间     | `NOW()` → `2024-06-04 17:42:31.123456`               |
| [CURRENT_TIMESTAMP](/tidb-cloud-lake/sql/current-timestamp.md) | 返回当前日期和时间     | `CURRENT_TIMESTAMP()` → `2024-06-04 17:42:31.123456` |
| [TODAY](/tidb-cloud-lake/sql/today.md)                         | 返回当前日期           | `TODAY()` → `2024-06-04`                             |
| [TOMORROW](/tidb-cloud-lake/sql/tomorrow.md)                   | 返回明天的日期         | `TOMORROW()` → `2024-06-05`                          |
| [YESTERDAY](/tidb-cloud-lake/sql/yesterday.md)                 | 返回昨天的日期         | `YESTERDAY()` → `2024-06-03`                         |

## 日期与时间提取函数 {#date-time-extraction-functions}

| Function                                      | 描述                         | 示例                                     |
|-----------------------------------------------|------------------------------|------------------------------------------|
| [YEAR](/tidb-cloud-lake/sql/year.md)                               | 从日期中提取年份             | `YEAR('2024-06-04')` → `2024`            |
| [MONTH](/tidb-cloud-lake/sql/month.md)                             | 从日期中提取月份             | `MONTH('2024-06-04')` → `6`              |
| [DAY](/tidb-cloud-lake/sql/day.md)                                 | 从日期中提取日               | `DAY('2024-06-04')` → `4`                |
| [QUARTER](/tidb-cloud-lake/sql/quarter.md)                         | 从日期中提取季度             | `QUARTER('2024-06-04')` → `2`            |
| [WEEK](/tidb-cloud-lake/sql/week.md) / [WEEKOFYEAR](/tidb-cloud-lake/sql/weekofyear.md) | 从日期中提取周序号           | `WEEK('2024-06-04')` → `23`              |
| [EXTRACT](/tidb-cloud-lake/sql/extract.md)                         | 从日期中提取指定部分         | `EXTRACT(MONTH FROM '2024-06-04')` → `6` |
| [DATE_PART](/tidb-cloud-lake/sql/date-part.md)                     | 从日期中提取指定部分         | `DATE_PART('month', '2024-06-04')` → `6` |
| [YEARWEEK](/tidb-cloud-lake/sql/yearweek.md)                       | 返回年份和周序号             | `YEARWEEK('2024-06-04')` → `202423`      |
| [MILLENNIUM](/tidb-cloud-lake/sql/millennium.md)                   | 返回日期所属的千年           | `MILLENNIUM('2024-06-04')` → `3`         |

## 日期与时间转换函数 {#date-time-conversion-functions}

| Function                                  | 描述                                        | 示例                                                          |
|-------------------------------------------|---------------------------------------------|---------------------------------------------------------------|
| [DATE](/tidb-cloud-lake/sql/date.md)                           | 将值转换为 DATE 类型                        | `DATE('2024-06-04')` → `2024-06-04`                           |
| [TO_DATE](/tidb-cloud-lake/sql/to-date.md)                     | 将字符串转换为 DATE 类型                    | `TO_DATE('2024-06-04')` → `2024-06-04`                        |
| [TO_DATETIME](/tidb-cloud-lake/sql/datetime.md)             | 将字符串转换为 DATETIME 类型                | `TO_DATETIME('2024-06-04 12:30:45')` → `2024-06-04 12:30:45`  |
| [TO_TIMESTAMP](/tidb-cloud-lake/sql/to-timestamp.md)           | 将字符串转换为 TIMESTAMP 类型               | `TO_TIMESTAMP('2024-06-04 12:30:45')` → `2024-06-04 12:30:45` |
| [TO_UNIX_TIMESTAMP](/tidb-cloud-lake/sql/unix-timestamp.md) | 将日期转换为 Unix 时间戳                    | `TO_UNIX_TIMESTAMP('2024-06-04')` → `1717516800`              |
| [TO_YYYYMM](/tidb-cloud-lake/sql/yyyymm.md)                 | 将日期格式化为 YYYYMM                       | `TO_YYYYMM('2024-06-04')` → `202406`                          |
| [TO_YYYYMMDD](/tidb-cloud-lake/sql/yyyymmdd.md)             | 将日期格式化为 YYYYMMDD                     | `TO_YYYYMMDD('2024-06-04')` → `20240604`                      |
| [TO_YYYYMMDDHH](/tidb-cloud-lake/sql/yyyymmddhh.md)         | 将日期格式化为 YYYYMMDDHH                   | `TO_YYYYMMDDHH('2024-06-04 12:30:45')` → `2024060412`         |
| [TO_YYYYMMDDHHMMSS](/tidb-cloud-lake/sql/yyyymmddhhmmss.md) | 将日期格式化为 YYYYMMDDHHMMSS               | `TO_YYYYMMDDHHMMSS('2024-06-04 12:30:45')` → `20240604123045` |
| [DATE_FORMAT](/tidb-cloud-lake/sql/date-format.md)             | 按格式字符串格式化日期                      | `DATE_FORMAT('2024-06-04', '%Y-%m-%d')` → `'2024-06-04'`      |
| [CONVERT_TIMEZONE](/tidb-cloud-lake/sql/convert-timezone.md)   | 将时间戳转换为目标时区                      | `CONVERT_TIMEZONE('America/Los_Angeles', '2024-11-01 11:36:10')` → `2024-10-31 20:36:10` |

## 日期与时间算术函数 {#date-time-arithmetic-functions}

| Function                                 | 描述                                                                 | 示例                                                                                 |
|------------------------------------------|----------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| [DATE_ADD](/tidb-cloud-lake/sql/date-add.md)                  | 为日期增加一个时间间隔                                               | `DATE_ADD(DAY, 7, '2024-06-04')` → `2024-06-11`                                      |
| [DATE_SUB](/tidb-cloud-lake/sql/date-sub.md)                  | 从日期中减去一个时间间隔                                             | `DATE_SUB(MONTH, 1, '2024-06-04')` → `2024-05-04`                                    |
| [ADD INTERVAL](/tidb-cloud-lake/sql/add-interval.md)           | 为日期增加一个间隔                                                   | `'2024-06-04' + INTERVAL 1 DAY` → `2024-06-05`                                       |
| [SUBTRACT INTERVAL](/tidb-cloud-lake/sql/subtract-interval.md) | 从日期中减去一个间隔                                                 | `'2024-06-04' - INTERVAL 1 MONTH` → `2024-05-04`                                     |
| [DATE_DIFF](/tidb-cloud-lake/sql/date-diff.md)                | 返回两个日期之间的差值                                               | `DATE_DIFF(DAY, '2024-06-01', '2024-06-04')` → `3`                                   |
| [TIMESTAMP_DIFF](/tidb-cloud-lake/sql/timestamp-diff.md)      | 返回两个时间戳之间的差值                                             | `TIMESTAMP_DIFF(HOUR, '2024-06-04 10:00:00', '2024-06-04 15:00:00')` → `5`           |
| [MONTHS_BETWEEN](/tidb-cloud-lake/sql/months-between.md)      | 返回两个日期之间相差的月数                                           | `MONTHS_BETWEEN('2024-06-04', '2024-01-04')` → `5`                                   |
| [DATE_BETWEEN](/tidb-cloud-lake/sql/date-between.md)          | 检查某个日期是否位于另外两个日期之间                                 | `DATE_BETWEEN('2024-06-04', '2024-06-01', '2024-06-10')` → `true`                    |
| [AGE](/tidb-cloud-lake/sql/age.md)                            | 计算两个时间戳之间，或某个时间戳与当前日期/时间之间的差值           | `AGE('2000-01-01'::TIMESTAMP, '1990-05-15'::TIMESTAMP)` → `9 years 7 months 17 days` |
| [ADD_MONTHS](/tidb-cloud-lake/sql/add-months.md)              | 在保留月末日期的情况下为日期增加月数。                               | `ADD_MONTHS('2025-04-30',1)` → `2025-05-31`                                          |

## 日期与时间截断函数 {#date-time-truncation-functions}

| Function                                      | 描述                                                     | 示例                                                                |
|-----------------------------------------------|----------------------------------------------------------|---------------------------------------------------------------------|
| [DATE_TRUNC](/tidb-cloud-lake/sql/date-trunc.md)                   | 将时间戳截断到指定精度                                   | `DATE_TRUNC('month', '2024-06-04')` → `2024-06-01`                  |
| [TIME_SLICE](/tidb-cloud-lake/sql/time-slice.md)                   | 将单个日期/时间戳值映射到按日历对齐的时间区间             | `TIME_SLICE('2024-06-04', 4, 'MONTH', 'START')` → `2024-05-01`      |
| [TO_START_OF_DAY](/tidb-cloud-lake/sql/to-start-of-day.md)         | 返回当天的开始时间                                       | `TO_START_OF_DAY('2024-06-04 12:30:45')` → `2024-06-04 00:00:00`    |
| [TO_START_OF_HOUR](/tidb-cloud-lake/sql/to-start-of-hour.md)       | 返回当前小时的开始时间                                   | `TO_START_OF_HOUR('2024-06-04 12:30:45')` → `2024-06-04 12:00:00`   |
| [TO_START_OF_MINUTE](/tidb-cloud-lake/sql/to-start-of-minute.md)   | 返回当前分钟的开始时间                                   | `TO_START_OF_MINUTE('2024-06-04 12:30:45')` → `2024-06-04 12:30:00` |
| [TO_START_OF_MONTH](/tidb-cloud-lake/sql/to-start-of-month.md)     | 返回当月的开始日期                                       | `TO_START_OF_MONTH('2024-06-04')` → `2024-06-01`                    |
| [TO_START_OF_QUARTER](/tidb-cloud-lake/sql/to-start-of-quarter.md) | 返回当季度的开始日期                                     | `TO_START_OF_QUARTER('2024-06-04')` → `2024-04-01`                  |
| [TO_START_OF_YEAR](/tidb-cloud-lake/sql/to-start-of-year.md)       | 返回当年的开始日期                                       | `TO_START_OF_YEAR('2024-06-04')` → `2024-01-01`                     |
| [TO_START_OF_WEEK](/tidb-cloud-lake/sql/to-start-of-week.md)       | 返回当周的开始日期                                       | `TO_START_OF_WEEK('2024-06-04')` → `2024-06-03`                     |

## 日期与时间导航函数 {#date-time-navigation-functions}

| Function                        | 描述                                       | 示例                                                  |
|---------------------------------|--------------------------------------------|-------------------------------------------------------|
| [LAST_DAY](/tidb-cloud-lake/sql/last-day.md)         | 返回当月的最后一天                         | `LAST_DAY('2024-06-04')` → `2024-06-30`               |
| [NEXT_DAY](/tidb-cloud-lake/sql/next-day.md)         | 返回下一个指定星期几的日期                 | `NEXT_DAY('2024-06-04', 'SUNDAY')` → `2024-06-09`     |
| [PREVIOUS_DAY](/tidb-cloud-lake/sql/previous-day.md) | 返回上一个指定星期几的日期                 | `PREVIOUS_DAY('2024-06-04', 'MONDAY')` → `2024-06-03` |

## 其他日期与时间函数 {#other-date-time-functions}

| Function                  | 描述                 | 示例                                                                     |
|---------------------------|----------------------|--------------------------------------------------------------------------|
| [TIMEZONE](/tidb-cloud-lake/sql/timezone.md)   | 返回当前时区         | `TIMEZONE()` → `'UTC'`                                                   |
| [TIME_SLOT](/tidb-cloud-lake/sql/time-slot.md) | 返回时间槽           | `TIME_SLOT('2024-06-04 12:30:45', 15, 'MINUTE')` → `2024-06-04 12:30:00` |