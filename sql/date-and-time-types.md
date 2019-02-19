---
title: date and time types
category: user guide
---

# Date and time types


The values used to represent date and time types are DATE, TIME, DATETIME, TIMESTAMP, and YEAR. Each of these types has its own range of valid values, and uses a zero value to indicate that it is an invalid value. The TIMESTAMP has an behavior of automatic update, which will be introduced later.

When dealing with date and time value types, please be noted: 

+ Although TiDB tries to parse different formats, the date part must be in the format of year-month-day (for example, '98-09-04'), rather than month-day-year or day-month-year.
+ Ambiguity occurs when the year contained in the date value is in 2 digits. Then TiDB converts the value based on the following rules:
  - Value between 70 and 99 is converted to a value between 1970 and 1999
  - Value between 00 and 69 is converted to a value between 2000 and 2069
+ If a numberic value is needed in the context, TiDB automatically converts the date or time value into a numeric type.
+ If TiDB encounters a date or time value that is beyond the representation range, or is invalid, it automatically converts the value to a zero value of that type.
+ Setting different SQL modes can change TiDB behaviors.
+ TiDB allows month or day in the columns of DATE and DATETIME to be zero value, for example, '2009-00-00' or '2009-01-00'. If this date type is to be calculated in a function, for example, in `DATE_SUB()` or `DATE_ADD()`, the result can be incorrect. 
+ TiDB allows zero value '0000-00-00' to be stored. Sometimes '0000-00-00' is more convenient for users than NULL value. 

Different types of zero value are shown in the following table:

| Date Type | "Zero" Value |
| :------   |  :----       |
| DATE      | '0000-00-00' |
| TIME      | '00:00:00'   |
| DATETIME  | '0000-00-00 00:00:00' |
| TIMESTAMP | '0000-00-00 00:00:00' |
| YEAR      | 0000         |

## DATE, DATETIME and TIMESTAMP types

DATE, DATETIME, TIMESTAMP are 3 relevant types. This part describes the common points and differences among these 3 types. 

DATE only contains date part and no time part. TiDB accepts and shows the values of DATE type in 'YYYY-MM-DD' format. The acceptable values range from '1000-01-01' to '9999-12-31'.

DATETIME contains both date part and time part, and the format is 'YYYY-MM-DD HH:MM:SS'. The acceptable values range from '1000-01-01 00:00:00' to '9999-12-31 23:59:59'.

TIMESTAMP contains both date part and time part. Its values range from '1970-01-01 00:00:01' to '2038-01-19 03:14:07' in UTC time.

DATETIME and TIMESTAMP values can contain a fractional part of up to 6 digits which is accurate to milliseconds. In any column of DATETIME or TIMESTAMP types, a fractional part will be stored instead of being discarded. With a fractional part, the value is in the format of 'YYYY-MM-DD HH:MM:SS[.fraction]', and the fraction ranges from 000000 to 999999. A decimal point must be used to seperate the fraction from the rest.

When TIMESTAMP is to be stored, TiDB converts the TIMESTAMP value from the current time zone to UTC time zone. When TIMESTAMP  is to be indexed, TiDB converts the stored TIMESTAMP value from UTC time zone to the current time zone (noted: DATETIME will not be handled in this way). The default time zone for each connection is the server's local time zone, which can be modified by the environment variable `time_zone` .

Invalid DATE, DATETIME, TIMESTAMP values will be automatically converted to the corresponding type of zero value ( '0000-00-00' or '0000-00-00 00:00:00' ). 

**Note**: In TIMESTAMP, zero is not allowed to appear in the month or day part. The only exception is zero value itself '0000-00-00 00:00:00'.

Ambiguity occurs when the year contained in the date value is in 2 digits. Then TiDB converts the value based on the following rules:

- Value between 00 and 69 is converted to a value between 2000 and 2069
- Value between 70 and 99 is converted to a value between 1970 and 1999



## TIME type

For TIME type, the format is 'HH:MM:SS' and the value ranges from '-838:59:59' to '838:59:59'. The value of time part is larger, because TIME is used not only to indicate the time within a day but also to indicate the time interval between 2 events.

TIME can contain a fractional part. With a fractional part, TIME ranges from '-838:59:59.000000' to '838:59:59.000000'.

Please pay attention to the abbreviated form of TIME. For example, '11:12' means '11:12:00' instead of '00:11:12'. However, '1112' means '00:11:12'. These differences are caused by the presence or absence of the colon:, because the 2 situations will be handed differently. 



## YEAR type

For YEAR type, the format is YYYY. The value ranges from 1901 to 2155, or is a zero value 0000. 

YEAR  follows these format rules:

+ Four-digit numeral ranges from 1901 to 2155
+ Four-digit string ranges from '1901' to '2155'
+ One-digit or two-digit numeral ranges from 1 to 99. Accordingly, 1-69 is converted to 2001-2069 and 70-99 is converted to 1970-1999
+ One-digit or two-digit string ranges from '0' to '99'
+ Value 0 is taken as 0000 wheras the string '0' or '00' is taken as 2000

Invalid YEAR value is automatically converted to 0000. 

## Automatic initialization and update of TIMESTAMP and DATETIME

Columns with TIMESTAMP or DATETIME value type can be automatically initialized or updated to the current time.

For any column with TIMESTAMP or DATETIME value type in the table, you can set the default or auto-update value as current timestamp. 

These properties can be set by setting `DEFAULT CURRENT_TIMESTAMP` and `ON UPDATE CURRENT_TIMESTAMP` when the column is being defined. DEFAULT can also be set as a specific value, such as `DEFAULT 0` or `DEFAULT '2000-01-01 00:00:00'` .

```
CREATE TABLE t1 (
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

The default value for DATETIME is `NULL` unless it is specified as `NOT NULL`. For the latter situation, if no default value is set, the default value will be 0.

```
CREATE TABLE t1 (
  dt1 DATETIME ON UPDATE CURRENT_TIMESTAMP,         -- default NULL
  dt2 DATETIME NOT NULL ON UPDATE CURRENT_TIMESTAMP -- default 0
);
```



## Decimal part of time value

Decimal part is allowed in TIME, DATETIME, TIMESTAMP value types. The decimal can be accurate to milliseconds.

+ Use `type_name(fsp)` to define a column that supports fractional precision, where `type_name` can be TIME, DATETIME or TIMESTAMP. For example,

  ```
  CREATE TABLE t1 (t TIME(3), dt DATETIME(6));
  ```

  fsp must range from 0 to 6. 

  0 means there is no fractional part. If fsp is omitted, the default is 0.

+ When inserting TIME, DATETIME or TIMESTAMP which contain a fractional part, if the number of digit of the fraction is too few, or too many, rounding may be needed in the situation. For example,

  ```
  mysql> CREATE TABLE fractest( c1 TIME(2), c2 DATETIME(2), c3 TIMESTAMP(2) );
  Query OK, 0 rows affected (0.33 sec)
  
  mysql> INSERT INTO fractest VALUES
       > ('17:51:04.777', '2014-09-08 17:51:04.777', '2014-09-08 17:51:04.777');
  Query OK, 1 row affected (0.03 sec)
  
  mysql> SELECT * FROM fractest;
  +-------------|------------------------|------------------------+
  | c1          | c2                     | c3                     |
  +-------------|------------------------|------------------------+
  | 17:51:04.78 | 2014-09-08 17:51:04.78 | 2014-09-08 17:51:04.78 |
  +-------------|------------------------|------------------------+
  1 row in set (0.00 sec)
  ```

## Conversions between date and time types

Sometimes we need to make conversions between date and time types. But some conversions may lead to information loss. For example, DATE, DATETIME and TIMESTAMP values all have their own respective ranges. TIMESTAMP should be no earlier than the year 1970 in UTC time or no later than UTC time '2038-01-19 03:14:07'. Based on this rule, '1968-01-01' is a valid date value of DATE or DATETIME, but becomes 0 when it is converted to TIMESTAMP.

The conversions of DATE:

+ When DATE is converted to DATETIME or TIMESTAMP, a time part '00:00:00' will be added, because DATE does not contain any time information
+ When DATE is converted to TIME, the result is '00:00:00'

Conversions of DATETIME or TIMESTAMP:

+ When DATETIME or TIMESTAMP is converted to DATE, the time and fractional part will be discarded. For example, '1999-12-31 23:59:59.499' is converted to '1999-12-31'
+ When DATETIME or TIMESTAMP is converted to TIME, the time part will be discarded, because TIME does not contain any time information

When we convert TIME to other time and date formats, the date part is automatically specified as  `CURRENT_DATE()`. The final converted result is a date that consists of TIME and `CURRENT_DATE()`. This is to say that if the value of TIME is beyond the range from '00:00:00' to '23:59:59', the converted date part does not indicate the current day.

When TIME is converted to DATE, the process is similar, and the time part will be discarded.

Using the `CAST()` function can explicitly convert a value to a DATE type. For example,

```
date_col = CAST(datetime_col AS DATE)
```

converting TIME and DATETIME to numeric format:

```
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



## Two-digit year contained in the date

The two-digit year contained in date does not explicitly indicate the actual year and is ambiguous. 

For DATETIME, DATE and TIMESTAMP types, TiDB follows these rules to eliminate ambiguity: 

- Value between 00 and 69 is converted to a value between 2000 and 2069
- Value between 70 and 99 is converted to a value between 1970 and1999

These rules also apply to the YEAR type, with one exception:

When numeral 00 is inserted to YEAR(4), the result will be 0000 rather than 2000. 

If you want the result to be 2000, you should specify value to be 2000, '0' or '00'.

The two-digit year may not be properly calculated in some functions such  `MIN()` and  `MAX()` . For these functions, the four-digit format suites better.










