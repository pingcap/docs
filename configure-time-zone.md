---
title: Time Zone Support
summary: Learn how to set the time zone and its format.
aliases: ['/docs/dev/configure-time-zone/','/docs/dev/how-to/configure/time-zone/']
---

# Time Zone Support

The time zone in TiDB is decided by the global [`time_zone`](/system-variables.md#time_zone) system variable and the session `time_zone` system variable. The default value of `time_zone` is `SYSTEM`. The actual time zone corresponding to `SYSTEM` is configured when the TiDB cluster bootstrap is initialized. The detailed logic is as follows:

- Prioritize the use of the `TZ` environment variable.
- If the `TZ` environment variable fails, extract the time zone from the actual soft link address of `/etc/localtime`.
- If both of the above methods fail, use `UTC` as the system time zone.

You can use the following statement to set the global server `time_zone` value at runtime:

```sql
SET GLOBAL time_zone = 'UTC';
```

Examples values are named zones like `UTC`, `Africa/Nairobi`, `Asia/Jakarta` and UTC offsets like `+02:00` and `-05:00`.

Each client has its own time zone setting, given by the session `time_zone` variable. Initially, the session variable takes its value from the global `time_zone` variable, but the client can change its own time zone with this statement:

```sql
SET time_zone = 'US/Pacific';
```

You can use the following statement to view the current values of the global, client-specific and system time zones:

```sql
SELECT @@global.time_zone, @@session.time_zone, @@global.system_time_zone;
```

To set the format of the value of the `time_zone`:

- The value 'SYSTEM' indicates that the time zone should be the same as the system time zone.
- The value can be given as a string indicating an offset from UTC, such as '+10:00' or '-6:00'.
- The value can be given as a named time zone, such as 'Europe/Helsinki', 'US/Eastern', or 'MET'.

The current session time zone setting affects the display and interpretation of time values that are zone-sensitive. This includes the values displayed by functions such as [`NOW()`](/functions-and-operators/date-and-time-functions.md) or `CURTIME()`. The `UTC_TIMESTAMP()` function can be used to get a timestamp based on UTC, which can be useful to avoid time zone specific issues. The `CONVERT_TZ()` function can be used to convert between timezones.

> **Note:**
>
> Only the values of the Timestamp data type is affected by time zone. This is because the Timestamp data type uses the literal value + time zone information. Other data types, such as Datetime/Date/Time, do not have time zone information, thus their values are not affected by the changes of time zone.

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

In this example, no matter how you adjust the value of the time zone, the value of the Datetime data type is not affected. But the displayed value of the Timestamp data type changes if the time zone information changes. In fact, the value that is stored in the storage does not change, it's just displayed differently according to different time zone setting.

> **Note:**
>
> - Time zone is involved during the conversion of the value of Timestamp and Datetime, which is handled based on the current `time_zone` of the session.
> - For data migration, you need to pay special attention to the time zone setting of the primary database and the secondary database.
> - To get correct timestamps it is strongly recommended to setup a reliable clock with NTP or PTP. See [system configuration check: NTP](/check-before-deployment.md#check-and-install-the-ntp-service) for how to check this.
> - When using a timezone that observes daylight saving this might lead to ambigious timestamps and/or nonexistent timestamps, especially if calculations are done with the timestamp.
> - MySQL uses `mysql_tzinfo_to_sql` to convert the timezone database of the OS to tables in the database. This isn't used or needed with TiDB as TiDB relies on timezone data that's part of the Go programming language.

## See also

- [Date and time data-type](/data-type-date-and-time.md)
- [Data and time functions](/functions-and-operators/date-and-time-functions.md)