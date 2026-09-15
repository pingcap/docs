---
title: TO_TIMESTAMP
summary: 将表达式转换为带时间的日期。
---

# TO_TIMESTAMP

将表达式转换为带时间的日期。

另请参阅：[TO_DATE](/tidb-cloud-lake/sql/to-date.md)

## 语法 {#syntax}

此函数支持多种重载形式，涵盖以下使用场景：

```sql
-- Convert a string or integer to a timestamp
TO_TIMESTAMP(<expr>)
```

如果给定的是 [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) 日期格式的字符串，函数会从该字符串中提取日期；如果给定的是整数，函数会根据 `x` 的绝对值，将该整数解释为 Unix epoch（1970 年 1 月 1 日午夜）之前（负数）或之后（正数）的秒数、毫秒数或微秒数：

| 范围                                        | 单位                 |
|---------------------------------------------|----------------------|
| \|x\| < 31,536,000,000                      | 秒                   |
| 31,536,000,000 ≤ \|x\| < 31,536,000,000,000 | 毫秒                 |
| \|x\| ≥ 31,536,000,000,000                  | 微秒                 |

```sql
-- Convert a string to a timestamp using the given pattern
TO_TIMESTAMP(<expr>, <pattern>)
```

该函数根据第二个字符串中指定的模式，将第一个字符串转换为时间戳。要指定模式，请使用格式说明符。格式说明符可用于定义日期和时间值的目标格式。有关支持的格式说明符完整列表，请参阅[日期和时间格式化](/tidb-cloud-lake/sql/date-time.md#formatting-date-and-time)。

```sql
-- Convert an integer to a timestamp based on the specified scale
TO_TIMESTAMP(<int>, <scale>)
```

该函数将整数值转换为时间戳，并将该整数解释为自 Unix epoch（1970 年 1 月 1 日午夜）以来的秒数（或基于指定 scale 的小数秒）。scale 定义了小数秒的精度，支持从 0 到 6 的取值。例如：

- `scale = 0`：将整数解释为秒。
- `scale = 1`：将整数解释为十分之一秒。
- `scale = 6`：将整数解释为微秒。

## 返回类型 {#return-type}

返回格式为 `YYYY-MM-DD hh:mm:ss.ffffff` 的时间戳：

- 返回的时间戳始终反映你的 {{{ .lake }}} 时区。
    - 当给定字符串中包含时区信息时，函数会将时间戳转换为 {{{ .lake }}} 中配置的时区对应的时间。换句话说，它会调整时间戳，使其反映 {{{ .lake }}} 中设置的时区。

    ```sql
    -- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
    SET timezone = 'America/Toronto';

    SELECT TO_TIMESTAMP('2022-01-02T01:12:00-07:00'), TO_TIMESTAMP('2022/01/02T01:12:00-07:00', '%Y/%m/%dT%H:%M:%S%::z');

    ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ to_timestamp('2022-01-02t01:12:00-07:00') │ to_timestamp('2022/01/02t01:12:00-07:00', '%y/%m/%dt%h:%m:%s%::z') │
    ├───────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
    │ 2022-01-02 03:12:00                       │ 2022-01-02 03:12:00                                                │
    └────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

    - 如果给定字符串中不包含时区信息，则会假定该时间戳属于当前会话中配置的时区。

    ```sql
    -- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
    SET timezone = 'America/Toronto';

    SELECT TO_TIMESTAMP('2022-01-02T01:12:00'), TO_TIMESTAMP('2022/01/02T01:12:00', '%Y/%m/%dT%H:%M:%S');

    ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ to_timestamp('2022-01-02t01:12:00') │ to_timestamp('2022/01/02t01:12:00', '%y/%m/%dt%h:%m:%s') │
    ├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
    │ 2022-01-02 01:12:00                 │ 2022-01-02 01:12:00                                      │
    └────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

- 如果给定字符串符合该格式但不包含时间部分，则会自动补全为该模式。补充值为 0。
- 如果转换失败，将返回错误。为避免此类错误，你可以使用 [TRY_TO_TIMESTAMP](/tidb-cloud-lake/sql/try-to-timestamp.md) 函数。

    ```sql
    root@localhost:8000/default> SELECT TO_TIMESTAMP('20220102');
    error: APIError: ResponseError with 1006: cannot parse to type `TIMESTAMP` while evaluating function `to_timestamp('20220102')`

    root@localhost:8000/default> SELECT TRY_TO_TIMESTAMP('20220102');

    SELECT
    try_to_timestamp('20220102')

    ┌──────────────────────────────┐
    │ try_to_timestamp('20220102') │
    ├──────────────────────────────┤
    │ NULL                         │
    └──────────────────────────────┘
    ```

## 别名 {#aliases}

- [TO_DATETIME](/tidb-cloud-lake/sql/datetime.md)
- [STR_TO_TIMESTAMP](/tidb-cloud-lake/sql/str-to-timestamp.md)

## 示例 {#examples}

### 示例 1：将字符串转换为时间戳 {#example-1-converting-string-to-timestamp}

```sql
SELECT TO_TIMESTAMP('2022-01-02 02:00:11');

┌─────────────────────────────────────┐
│ to_timestamp('2022-01-02 02:00:11') │
├─────────────────────────────────────┤
│ 2022-01-02 02:00:11                 │
└─────────────────────────────────────┘

SELECT TO_TIMESTAMP('2022-01-02T01');

┌───────────────────────────────┐
│ to_timestamp('2022-01-02t01') │
├───────────────────────────────┤
│ 2022-01-02 01:00:00           │
└───────────────────────────────┘

-- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
SET timezone = 'America/Toronto';
-- Convert provided string to current timezone ('America/Toronto')
SELECT TO_TIMESTAMP('2022-01-02T01:12:00-07:00');

┌───────────────────────────────────────────┐
│ to_timestamp('2022-01-02t01:12:00-07:00') │
├───────────────────────────────────────────┤
│ 2022-01-02 03:12:00                       │
└───────────────────────────────────────────┘
```

### 示例 2：将整数转换为时间戳 {#example-2-converting-integer-to-timestamp}

```sql
SELECT TO_TIMESTAMP(1), TO_TIMESTAMP(-1);

┌───────────────────────────────────────────┐
│   to_timestamp(1)   │  to_timestamp(- 1)  │
├─────────────────────┼─────────────────────┤
│ 1969-12-31 19:00:01 │ 1969-12-31 18:59:59 │
└───────────────────────────────────────────┘
```

你也可以将整数字符串转换为时间戳：

```sql
SELECT TO_TIMESTAMP(TO_INT64('994518299'));

┌─────────────────────────────────────┐
│ to_timestamp(to_int64('994518299')) │
├─────────────────────────────────────┤
│ 2001-07-07 15:04:59                 │
└─────────────────────────────────────┘
```

- 你也可以使用 `SELECT TO_TIMESTAMP('994518299', '%s')` 进行转换，但不推荐这样做。对于此类转换，{{{ .lake }}} 建议使用上面的示例方法以获得更好的性能。

- Timestamp 的取值范围是 1000-01-01 00:00:00.000000 到 9999-12-31 23:59:59.999999。如果你运行以下语句，{{{ .lake }}} 会返回错误：

```bash
root@localhost:8000/default> SELECT TO_TIMESTAMP(9999999999999999999);
error: APIError: ResponseError with 1006: number overflowed while evaluating function `to_int64(9999999999999999999)`
```

### 示例 3：按模式转换字符串 {#example-3-converting-string-with-pattern}

```sql
-- Set timezone to 'America/Toronto' (UTC-5:00, Eastern Standard Time)
SET timezone = 'America/Toronto';

-- Convert provided string to current timezone ('America/Toronto')
SELECT TO_TIMESTAMP('2022/01/02T01:12:00-07:00', '%Y/%m/%dT%H:%M:%S%::z');

┌────────────────────────────────────────────────────────────────────┐
│ to_timestamp('2022/01/02t01:12:00-07:00', '%y/%m/%dt%h:%m:%s%::z') │
├────────────────────────────────────────────────────────────────────┤
│ 2022-01-02 03:12:00                                                │
└────────────────────────────────────────────────────────────────────┘

-- If no timezone is specified, the session's time zone applies.
SELECT TO_TIMESTAMP('2022/01/02T01:12:00', '%Y/%m/%dT%H:%M:%S');

┌──────────────────────────────────────────────────────────┐
│ to_timestamp('2022/01/02t01:12:00', '%y/%m/%dt%h:%m:%s') │
├──────────────────────────────────────────────────────────┤
│ 2022-01-02 01:12:00                                      │
└──────────────────────────────────────────────────────────┘
```

### 示例 4：转换带扩展的整数 {#example-4-converting-integer-with-scale}

```sql
-- 将一个整数按秒精度解释（scale = 0）
SELECT TO_TIMESTAMP(1638473645, 0), TO_TIMESTAMP(-1638473645, 0);

┌─────────────────────────────────────────────────────────────┐
│ to_timestamp(1638473645, 0) │ to_timestamp(- 1638473645, 0) │
├─────────────────────────────┼───────────────────────────────┤
│ 2021-12-02 19:34:05         │ 1918-01-30 04:25:55           │
└─────────────────────────────────────────────────────────────┘

-- 将一个整数按毫秒精度解释（scale = 3）
SELECT TO_TIMESTAMP(1638473645123, 3);

┌────────────────────────────────┐
│ to_timestamp(1638473645123, 3) │
├────────────────────────────────┤
│ 2021-12-02 19:34:05.123        │
└────────────────────────────────┘
```