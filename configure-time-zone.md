---
title: Time Zone Support
summary: The time zone setting in TiDB is controlled by the `time_zone` system variable, which can be set at the session or global level. The displayed values of the `TIMESTAMP` data type are affected by the time zone setting, while the `DATETIME`, `DATE`, and `TIME` data types are not affected. For data migration, you need to pay special attention to whether the time zone settings of the primary database and the secondary database are consistent.
aliases: ['/docs/dev/configure-time-zone/','/docs/dev/how-to/configure/time-zone/']
---

# Time Zone Support

The time zone in TiDB is decided by the [`time_zone`](/system-variables.md#time_zone) system variable. You can set it at the session or global level. The default value of `time_zone` is `SYSTEM`. The actual time zone corresponding to `SYSTEM` is configured when the TiDB cluster bootstrap is initialized. The detailed logic is as follows:

1. TiDB prioritizes the use of the `TZ` environment variable.
2. If the `TZ` environment variable fails, TiDB reads the time zone from the soft link at `/etc/localtime`.
3. If both of the preceding methods fail, TiDB uses `UTC` as the system time zone.

## View time zone settings

To view the current values of the global, client-specific, and system time zones, execute the following statement:

```sql
SELECT @@global.time_zone, @@session.time_zone, @@global.system_time_zone;
```

## Set the time zone

In TiDB, the value of the `time_zone` system variable can be set in one of the following formats:

- `SYSTEM` (default value), which indicates that the time zone should be the same as the system time zone.
- A UTC offset, such as `'+10:00'` or `'-6:00'`.
- A named time zone, such as `'Europe/Helsinki'`, `'US/Eastern'`, or `'MET'`.

Depending on your needs, you can set the time zone in TiDB at the global or session level as follows:

- Set the time zone in TiDB at the global level:

    ```sql
    SET GLOBAL time_zone = ${time-zone-value};
    ```

    For example, set the global time zone to UTC:

    ```sql
    SET GLOBAL time_zone = 'UTC';
    ```

- Set the time zone in TiDB at the session level:

    ```sql
    SET time_zone = ${time-zone-value};
    ```

    For example, set the time zone of the current session to US/Pacific:

    ```sql
    SET time_zone = 'US/Pacific';
    ```

## Functions and data types affected by time zone settings

The current session time zone setting affects the display and interpretation of time values that are zone-sensitive, such as the values returned by [`NOW()`](/functions-and-operators/date-and-time-functions.md) and `CURTIME()` functions. To convert between time zones, use the `CONVERT_TZ()` function. To get a timestamp based on UTC, use the `UTC_TIMESTAMP()` function, which helps avoid time zone-related issues.

In TiDB, the displayed values of the `TIMESTAMP` data type are affected by time zone settings. This is because the `TIMESTAMP` data type uses the literal value and time zone information. Other data types, such as `DATETIME`, `DATE`, and `TIME`, do not have time zone information, thus their values are not affected by the changes of time zone.

For example:

```sql
create table t (ts timestamp, dt datetime);
```

```
Query OK, 0 rows affected (0.02 sec)
```

```sql
set @@time_zone = 'UTC';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
insert into t values ('2017-09-30 11:11:11', '2017-09-30 11:11:11');
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
set @@time_zone = '+8:00';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
select * from t;
```

```
+---------------------|---------------------+
| ts                  | dt                  |
+---------------------|---------------------+
| 2017-09-30 19:11:11 | 2017-09-30 11:11:11 |
+---------------------|---------------------+
1 row in set (0.00 sec)
```

In this example, no matter how you adjust the time zone value, the value of the `DATETIME` data type is not affected. However, the displayed value of the `TIMESTAMP` data type reflects changes in the time zone. In fact, the `TIMESTAMP` value stored in the database remains unchanged, but it is displayed differently according to different time zone settings.

## Important considerations for time zone settings

- Time zone is involved during the conversion of the values of `TIMESTAMP` and `DATETIME`, which is handled based on the `time_zone` of the current session.
- For data migration, you need to pay special attention to whether the time zone settings of the primary database and the secondary database are consistent.
- To get accurate timestamps, it is strongly recommended that you configure a reliable clock using Network Time Protocol (NTP) or Precision Time Protocol (PTP) services. For information about how to check NTP services, see [Check and install the NTP service](/check-before-deployment.md#check-and-install-the-ntp-service).
- Be aware that using time zones that observe daylight saving time can result in ambiguous or nonexistent timestamps, especially when performing calculations with those timestamps.
- MySQL uses [`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.4/en/mysql-tzinfo-to-sql.html) to convert the time zone database of the operating system into tables in the `mysql` database. In contrast, TiDB directly reads the time zone data files from the time zone database of the operating system, which leverages the built-in time zone handling capabilities of the Go programming language.

## See also

- [Date and time data-type](/data-type-date-and-time.md)
- [Data and time functions](/functions-and-operators/date-and-time-functions.md)
