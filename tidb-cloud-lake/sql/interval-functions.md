---
title: 区间函数
summary: 本节提供 {{{ .lake }}} 中区间函数的参考信息。区间函数允许你创建各种时间单位的区间值，用于日期和时间计算。
---

# 区间函数

本节提供 {{{ .lake }}} 中区间函数的参考信息。区间函数允许你创建各种时间单位的区间值，用于日期和时间计算。

## 时间单位转换函数 {#time-unit-conversion-functions}

### 基于天的区间 {#day-based-intervals}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [TO_DAYS](/tidb-cloud-lake/sql/days.md) | 将数字转换为天数区间 | `TO_DAYS(2)` → `2 days` |
| [TO_WEEKS](/tidb-cloud-lake/sql/weeks.md) | 将数字转换为周数区间 | `TO_WEEKS(3)` → `21 days` |
| [TO_MONTHS](/tidb-cloud-lake/sql/months.md) | 将数字转换为月数区间 | `TO_MONTHS(2)` → `2 months` |
| [TO_YEARS](/tidb-cloud-lake/sql/years.md) | 将数字转换为年数区间 | `TO_YEARS(1)` → `1 year` |

### 基于小时的区间 {#hour-based-intervals}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [TO_HOURS](/tidb-cloud-lake/sql/hours.md) | 将数字转换为小时区间 | `TO_HOURS(5)` → `5:00:00` |
| [TO_MINUTES](/tidb-cloud-lake/sql/minutes.md) | 将数字转换为分钟区间 | `TO_MINUTES(90)` → `1:30:00` |
| [TO_SECONDS](/tidb-cloud-lake/sql/seconds.md) | 将数字转换为秒数区间 | `TO_SECONDS(3600)` → `1:00:00` |
| [EPOCH](/tidb-cloud-lake/sql/epoch.md) | TO_SECONDS 的别名 | `EPOCH(60)` → `00:01:00` |

### 更小的时间单位 {#smaller-time-units}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [TO_MILLISECONDS](/tidb-cloud-lake/sql/milliseconds.md) | 将数字转换为毫秒区间 | `TO_MILLISECONDS(2000)` → `00:00:02` |
| [TO_MICROSECONDS](/tidb-cloud-lake/sql/microseconds.md) | 将数字转换为微秒区间 | `TO_MICROSECONDS(2000000)` → `00:00:02` |

### 更大的时间单位 {#larger-time-units}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [TO_DECADES](/tidb-cloud-lake/sql/decades.md) | 将数字转换为十年区间 | `TO_DECADES(2)` → `20 years` |
| [TO_CENTRIES](/tidb-cloud-lake/sql/to-centuries.md) | 将数字转换为世纪区间 | `TO_CENTRIES(1)` → `100 years` |
| [TO_MILLENNIA](/tidb-cloud-lake/sql/millennia.md) | 将数字转换为千年区间 | `TO_MILLENNIA(1)` → `1000 years` |