---
title: EXTRACT
summary: 提取日期、时间戳或间隔中指定的部分。
---

# EXTRACT

提取日期、时间戳或间隔中指定的部分。

另请参阅：[DATE_PART](/tidb-cloud-lake/sql/date-part.md)

## 语法 {#syntax}

```sql
-- Extract from a date or timestamp
EXTRACT(
  YEAR | QUARTER | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND |
  DOW | DOY | EPOCH | ISODOW | YEARWEEK | MILLENNIUM
  FROM <date_or_timestamp>
)

-- Extract from an interval
EXTRACT( YEAR | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND | MICROSECOND ｜ EPOCH FROM <interval> )
```

| 关键字 | 描述 |
|--------------|-------------------------------------------------------------------------|
| `DOW`        | 一周中的第几天。星期日 (0) 到星期六 (6)。 |
| `DOY`        | 一年中的第几天。1 到 366。 |
| `EPOCH`      | 自 1970-01-01 00:00:00 以来的秒数。 |
| `ISODOW`     | ISO 一周中的第几天。星期一 (1) 到星期日 (7)。 |
| `YEARWEEK`   | 按照 ISO 8601 组合的年份和周数（例如，202415）。 |
| `MILLENNIUM` | 日期所属的千年（年份 1–1000 为 1，1001–2000 为 2，依此类推）。 |

## 返回类型 {#return-type}

返回类型取决于被提取的字段：

- 返回整数型：提取离散的日期或时间组成部分时（例如 YEAR、MONTH、DAY、DOY、HOUR、MINUTE、SECOND），该函数返回一个整数型值。

    ```sql
    SELECT EXTRACT(DAY FROM now());  -- Returns Integer
    SELECT EXTRACT(DOY FROM now());  -- Returns Integer
    ```

- 返回 float：提取 EPOCH（自 1970-01-01 00:00:00 UTC 以来的秒数）时，该函数返回一个 float，因为结果可能包含小数秒。

    ```sql
    SELECT EXTRACT(EPOCH FROM now());  -- Returns Float
    ```

## 示例 {#examples}

以下示例从当前时间戳中提取多个字段：

```sql
SELECT
  NOW(),
  EXTRACT(DAY FROM NOW()),
  EXTRACT(DOY FROM NOW()),
  EXTRACT(EPOCH FROM NOW()),
  EXTRACT(ISODOW FROM NOW()),
  EXTRACT(YEARWEEK FROM NOW()),
  EXTRACT(MILLENNIUM FROM NOW());

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│            now()           │ EXTRACT(DAY FROM now()) │ EXTRACT(DOY FROM now()) │ EXTRACT(EPOCH FROM now()) │ EXTRACT(ISODOW FROM now()) │ EXTRACT(YEARWEEK FROM now()) │ EXTRACT(MILLENNIUM FROM now()) │
├────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────────────┼────────────────────────────┼──────────────────────────────┼────────────────────────────────┤
│ 2025-04-16 18:04:22.773888 │                      16 │                     106 │         1744826662.773888 │                          3 │                       202516 │                              3 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

以下示例从一个 interval 中提取天数：

```sql
SELECT EXTRACT(DAY FROM '1 day 2 hours 3 minutes 4 seconds'::INTERVAL);

┌─────────────────────────────────────────────────────────────────┐
│ EXTRACT(DAY FROM '1 day 2 hours 3 minutes 4 seconds'::INTERVAL) │
├─────────────────────────────────────────────────────────────────┤
│                                                               1 │
└─────────────────────────────────────────────────────────────────┘
```