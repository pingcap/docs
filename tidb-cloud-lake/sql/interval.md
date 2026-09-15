---
title: Interval
summary: INTERVAL 表示一个持续时间，可以写成自然语言文本（`'1 year 2 months'`、`'3 days ago'`），也可以写成以微秒为单位的整数。{{{ .lake }}} 支持从千年到微秒的时间单位，并允许对 interval、日期和时间戳进行算术运算。
---

# Interval

## 概述 {#overview}

`INTERVAL` 表示一个持续时间，可以写成自然语言文本（`'1 year 2 months'`、`'3 days ago'`），也可以写成以微秒为单位的整数。{{{ .lake }}} 支持从千年到微秒的时间单位，并允许对 interval、日期和时间戳进行算术运算。

> **注意：**
>
> 解析数值型 interval 时，小数部分会被丢弃。`'1.6 seconds'` 会变成一个 1 秒的 interval。

## 示例 {#examples}

### 字面量和数值 {#literals-and-numeric-values}

```sql
CREATE OR REPLACE TABLE intervals (duration INTERVAL);

INSERT INTO intervals VALUES
  ('1 year 2 months'),       -- positive natural language
  ('1 year 2 months ago'),   -- negative because of "ago"
  ('1000000'),               -- 1 second in microseconds
  ('-1000000');              -- -1 second

SELECT TO_STRING(duration) AS duration_text FROM intervals;
```

结果：

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

结果：

```
┌────────┬────────────┐
│ whole  │ fractional │
├────────┼────────────┤
│ 0:00:01 │ 0:00:01   │
└────────┴────────────┘
```

### Interval 算术运算 {#interval-arithmetic}

```sql
SELECT
  TO_STRING(TO_DAYS(3) + TO_DAYS(1)) AS add_interval,
  TO_STRING(TO_DAYS(3) - TO_DAYS(1)) AS subtract_interval;
```

结果：

```
┌──────────────┬──────────────────┐
│ add_interval │ subtract_interval │
├──────────────┼──────────────────┤
│ 4 days       │ 2 days           │
└──────────────┴──────────────────┘
```

### 应用于 DATE 和 TIMESTAMP {#apply-to-date-and-timestamp}

```sql
SELECT
  DATE '2024-12-20' + TO_DAYS(2) AS add_days,
  DATE '2024-12-20' - TO_DAYS(2) AS subtract_days,
  TIMESTAMP '2024-12-20 10:00:00' + TO_HOURS(36) AS add_hours,
  TIMESTAMP '2024-12-20 10:00:00' - TO_HOURS(36) AS subtract_hours;
```

结果：

```
┌────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ add_days           │ subtract_days      │ add_hours          │ subtract_hours     │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ 2024-12-22T00:00:00 │ 2024-12-18T00:00:00 │ 2024-12-21T22:00:00 │ 2024-12-18T22:00:00 │
└────────────────────┴────────────────────┴────────────────────┴────────────────────┘
```

interval 的加减方式与数字类似，因此可以方便地滑动时间窗口，或以精确到微秒的控制来计算偏移。