---
title: Date and Time Types
summary: 了解支持的日期和时间类型。
---

# Date and Time Types

TiDB 支持所有 MySQL 日期和时间数据类型，用于存储时间值：[`DATE`](#date-type)、[`TIME`](#time-type)、[`DATETIME`](#datetime-type)、[`TIMESTAMP`](#timestamp-type) 和 [`YEAR`](#year-type)。更多信息请参见 [Date and Time Data Types in MySQL](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-types.html)。

每种类型都有其有效值范围，并使用零值表示无效值。此外，`TIMESTAMP` 和 `DATETIME` 类型在修改时可以自动生成新的时间值。

在处理日期和时间值类型时，请注意：

+ 虽然 TiDB 会尝试解释不同的格式，但日期部分必须采用 year-month-day（例如，'1998-09-04'）的格式，而不能使用 month-day-year 或 day-month-year。
+ 如果日期的 year 部分用 2 位数字指定，TiDB 会根据 [特定规则](#two-digit-year-portion-contained-in-the-date) 进行转换。
+ 如果在上下文中需要数字值，TiDB 会自动将日期或时间值转换为数字类型。例如：

    ```sql
    mysql> SELECT NOW(), NOW()+0, NOW(3)+0;
    +---------------------+----------------+--------------------+
    | NOW()               | NOW()+0        | NOW(3)+0           |
    +---------------------+----------------+--------------------+
    | 2012-08-15 09:28:00 | 20120815092800 | 20120815092800.889 |
    +---------------------+----------------+--------------------+
    ```

+ TiDB 可能会自动将无效值或超出支持范围的值转换为该类型的零值。这一行为取决于设置的 SQL Mode。例如：

    ```sql
    mysql> show create table t1;
    +-------+---------------------------------------------------------------------------------------------------------+
    | Table | Create Table                                                                                            |
    +-------+---------------------------------------------------------------------------------------------------------+
    | t1    | CREATE TABLE `t1` (
      `a` time DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
    +-------+---------------------------------------------------------------------------------------------------------+
    1 行，耗时 0.00 秒

    mysql> select @@sql_mode;
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    | @@sql_mode                                                                                                                                |
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    1 行，耗时 0.00 秒

    mysql> insert into t1 values ('2090-11-32:22:33:44');
    ERROR 1292 (22007): Truncated incorrect time value: '2090-11-32:22:33:44'
    mysql> set @@sql_mode='';                                                                                                                                                                                                                     查询成功，影响行数 0（0.01 秒）

    mysql> insert into t1 values ('2090-11-32:22:33:44');
    查询成功，影响行数 1，警告 1（0.01 秒）

    mysql> select * from t1;
    +----------+
    | a        |
    +----------+
    | 00:00:00 |
    +----------+
    1 行，耗时 0.01 秒
    ```

+ 设置不同的 SQL Mode 可以改变 TiDB 的行为。
+ 如果没有启用 `NO_ZERO_DATE`，TiDB 允许 `DATE` 和 `DATETIME` 列中的月份或天数为零值，例如 `'2009-00-00'` 或 `'2009-01-00'`。如果在函数中计算此类日期类型，例如 `DATE_SUB()` 或 `DATE_ADD()`，结果可能不正确。
+ 默认情况下，TiDB 启用 `NO_ZERO_DATE` SQL Mode。此模式阻止存储零值，如 `'0000-00-00'`。

不同类型的零值显示在下表中：

| Date Type | "Zero" Value |
| :------   |  :----       |
| DATE      | '0000-00-00' |
| TIME      | '00:00:00'   |
| DATETIME  | '0000-00-00 00:00:00' |
| TIMESTAMP | '0000-00-00 00:00:00' |
| YEAR      | 0000         |

如果 SQL Mode 允许，`DATE`、`DATETIME` 和 `TIMESTAMP` 的无效值会自动转换为对应类型的零值（'0000-00-00' 或 '0000-00-00 00:00:00'）。

## 支持的类型

### `DATE` 类型

`DATE` 只包含日期部分，不包含时间部分，显示格式为 `YYYY-MM-DD`。支持的范围是 `'0000-01-01'` 到 `'9999-12-31'`：

```sql
DATE
```

### `TIME` 类型

`TIME` 类型的格式为 `HH:MM:SS[.fraction]`，有效值范围为 `'-838:59:59.000000'` 到 `'838:59:59.000000'`。`TIME` 不仅用来表示一天中的时间，也用来表示两个事件之间的时间间隔。可以指定一个范围从 0 到 6 的 `fsp`（小数秒精度）值，若省略，默认精度为 0：

```sql
TIME[(fsp)]
```

> **Note:**
>
> 注意 `TIME` 的简写形式。例如，'11:12' 表示 '11:12:00'，而不是 '00:11:12'。但 '1112' 表示 '00:11:12'。这些差异由是否存在 `:` 字符引起。

### `DATETIME` 类型

`DATETIME` 包含日期部分和时间部分。有效值范围为 `'0000-01-01 00:00:00.000000'` 到 `'9999-12-31 23:59:59.999999'`。

TiDB 以 `YYYY-MM-DD HH:MM:SS[.fraction]` 格式显示 `DATETIME` 值，但允许用字符串或数字为 `DATETIME` 列赋值。可以指定一个范围从 0 到 6 的 `fsp`，若省略，默认精度为 0：

```sql
DATETIME[(fsp)]
```

### `TIMESTAMP` 类型

`TIMESTAMP` 包含日期部分和时间部分。有效值范围为 `'1970-01-01 00:00:01.000000'` 到 `'2038-01-19 03:14:07.999999'`（UTC 时间）。可以指定一个范围从 0 到 6 的 `fsp`，若省略，默认精度为 0。

在 `TIMESTAMP` 中，不允许月份或天数为零值，唯一例外是零值 `'0000-00-00 00:00:00'`。

```sql
TIMESTAMP[(fsp)]
```

#### Timezone Handling

当存储 `TIMESTAMP` 时，TiDB 会将 `TIMESTAMP` 值从当前时区转换为 UTC 时间。当检索 `TIMESTAMP` 时，TiDB 会将存储的 `TIMESTAMP` 值从 UTC 转换为当前时区（注意：`DATETIME` 不以此方式处理）。每个连接的默认时区为服务器的本地时区，可以通过环境变量 `time_zone` 修改。

> **Warning:**
>
> 和 MySQL 一样，`TIMESTAMP` 数据类型存在 [Year 2038 Problem](https://en.wikipedia.org/wiki/Year_2038_problem)。如果存储的值可能超出 2038 年，请考虑使用 `DATETIME` 类型。

### `YEAR` 类型

`YEAR` 类型的格式为 `'YYYY'`。支持的值范围为 1901 到 2155，或零值 0000：

```sql
YEAR[(4)]
```

`YEAR` 遵循以下格式规则：

+ 四位数字，范围为 1901 到 2155
+ 四位字符串，范围为 `'1901'` 到 `'2155'`
+ 一位或两位数字，范围为 1 到 99。对应地，1-69 转换为 2001-2069，70-99 转换为 1970-1999
+ 一位或两位字符串，范围为 `'0'` 到 `'99'`
+ 数值 0 被视为 0000，而字符串 `'0'` 或 `'00'` 被视为 2000

无效的 `YEAR` 值会自动转换为 0000（如果用户未使用 `NO_ZERO_DATE` SQL Mode）。

## `TIMESTAMP` 和 `DATETIME` 的自动初始化与更新

带有 `TIMESTAMP` 或 `DATETIME` 值类型的列可以在插入或更新时自动初始化为当前时间。

对于表中的任何 `TIMESTAMP` 或 `DATETIME` 类型列，可以设置默认值或自动更新为当前时间。

这些属性可以在定义列时通过设置 `DEFAULT CURRENT_TIMESTAMP` 和 `ON UPDATE CURRENT_TIMESTAMP` 来实现。`DEFAULT` 也可以设置为特定值，例如 `DEFAULT 0` 或 `DEFAULT '2000-01-01 00:00:00'`。

```sql
CREATE TABLE t1 (
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

除非明确指定为 `NOT NULL`，否则 `DATETIME` 的默认值为 `NULL`。对于后者，如果未设置默认值，默认值为 0。

```sql
CREATE TABLE t1 (
    dt1 DATETIME ON UPDATE CURRENT_TIMESTAMP,         -- 默认 NULL
    dt2 DATETIME NOT NULL ON UPDATE CURRENT_TIMESTAMP -- 默认 0
);
```

## 时间值的小数部分

`DATETIME` 和 `TIMESTAMP` 值可以包含最多 6 位的微秒级小数部分。在任何 `DATETIME` 或 `TIMESTAMP` 类型的列中，都会存储小数部分，而不是舍弃。带有小数部分的值格式为 `'YYYY-MM-DD HH:MM:SS[.fraction]'`，其中 `fraction` 范围为 000000 到 999999。必须用小数点将小数部分与其他部分分隔。

+ 使用 `type_name(fsp)` 定义支持小数精度的列，其中 `type_name` 可以是 `TIME`、`DATETIME` 或 `TIMESTAMP`。例如：

    ```sql
    CREATE TABLE t1 (t TIME(3), dt DATETIME(6));
    ```

  `fsp` 必须在 0 到 6 之间。

  `0` 表示没有小数部分。如果省略，默认值为 0。

+ 在插入包含小数部分的 `TIME`、`DATETIME` 或 `TIMESTAMP` 时，如果小数位数过少或过多，可能需要四舍五入。例如：

    ```sql
    mysql> CREATE TABLE fractest( c1 TIME(2), c2 DATETIME(2), c3 TIMESTAMP(2) );
    Query OK, 0 rows affected (0.33 sec)

    mysql> INSERT INTO fractest VALUES
         > ('17:51:04.777', '2014-09-08 17:51:04.777',   '2014-09-08 17:51:04.777');
    Query OK, 1 row affected (0.03 sec)

    mysql> SELECT * FROM fractest;
    +-------------|------------------------|------------------------+
    | c1          | c2                     | c3                     |
    +-------------|------------------------|------------------------+
    | 17:51:04.78 | 2014-09-08 17:51:04.78 | 2014-09-08 17:51:04.78 |
    +-------------|------------------------|------------------------+
    1 行，耗时 0.00 秒
    ```

## 日期和时间类型之间的转换

有时需要在日期和时间类型之间进行转换，但某些转换可能导致信息丢失。例如，`DATE`、`DATETIME` 和 `TIMESTAMP` 值各自有其范围。`TIMESTAMP` 不应早于 1970 年 UTC 时间，也不应晚于 UTC 时间 `'2038-01-19 03:14:07'`。根据此规则，`1968-01-01` 是 `DATE` 或 `DATETIME` 的有效日期值，但转换为 `TIMESTAMP` 时会变成 0。

`DATE` 的转换规则：

+ 转换为 `DATETIME` 或 `TIMESTAMP` 时，会添加时间部分 `'00:00:00'`，因为 `DATE` 不包含时间信息
+ 转换为 `TIME` 时，结果为 `'00:00:00'`

`DATETIME` 或 `TIMESTAMP` 的转换规则：

+ 转换为 `DATE` 时，会丢弃时间和小数部分。例如，`'1999-12-31 23:59:59.499'` 转换为 `'1999-12-31'`
+ 转换为 `TIME` 时，会丢弃日期部分，因为 `TIME` 不包含日期信息

当将 `TIME` 转换为其他时间和日期格式时，日期部分会自动指定为 `CURRENT_DATE()`。最终转换的结果是由 `TIME` 和 `CURRENT_DATE()` 组成的日期。也就是说，如果 `TIME` 的值超出 `'00:00:00'` 到 `'23:59:59'` 的范围，转换后日期部分不代表当天。

将 `TIME` 转换为 `DATE` 时，过程类似，时间部分会被丢弃。

可以使用 `CAST()` 函数显式将值转换为 `DATE` 类型。例如：

```sql
date_col = CAST(datetime_col AS DATE)
```

将 `TIME` 和 `DATETIME` 转换为数字格式。例如：

```sql
mysql> SELECT CURTIME(), CURTIME()+0, CURTIME(3)+0;
+-----------|-------------|--------------+
| CURTIME() | CURTIME()+0 | CURTIME(3)+0 |
+-----------|-------------|--------------+
| 09:28:00  |       92800 |    92800.887 |
+-----------|-------------|--------------+
mysql> SELECT NOW(), NOW()+0, NOW(3)+0;
+---------------------|----------------|--------------------+
| NOW()               | NOW()+0        | NOW(3)+0           |
+---------------------|----------------|--------------------+
| 2012-08-15 09:28:00 | 20120815092800 | 20120815092800.889 |
+---------------------|----------------|--------------------+
```

### 两位数字的年份部分在日期中的含义

日期中包含的两位数字年份部分不明确，存在歧义。

对于 `DATETIME`、`DATE` 和 `TIMESTAMP` 类型，TiDB 遵循以下规则以消除歧义：

- 01 到 69 之间的值转换为 2001 到 2069 之间的值
- 70 到 99 之间的值转换为 1970 到 1999 之间的值

这些规则也适用于 `YEAR` 类型，但有一例外：

当插入数字 `00` 到 `YEAR(4)` 时，结果为 0000，而不是 2000。

如果希望结果为 2000，应明确指定值为 2000。

两位数字的年份部分在某些函数（如 `MIN()` 和 `MAX()`）中可能无法正确计算。对于这些函数，使用四位数字的格式更合适。