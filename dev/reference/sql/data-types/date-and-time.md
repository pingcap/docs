---
title: TiDB Data Type
summary: Learn about the data types supported in TiDB.
category: reference
---

# Date and time types

### Overview

TiDB supports all the MySQL floating-point types, including DATE, DATETIME, TIMESTAMP, TIME, and YEAR. For more information, [Date and Time Types in MySQL](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-types.html).

#### Type definition

Syntax:

```sql
DATE
> A date. The supported range is '1000-01-01' to '9999-12-31'. TiDB displays DATE values in 'YYYY-MM-DD' format.

DATETIME[(fsp)]
> A date and time combination. The supported range is '1000-01-01 00:00:00.000000' to '9999-12-31 23:59:59.999999'. TiDB displays DATETIME values in 'YYYY-MM-DD HH:MM:SS[.fraction]' format, but permits assignment of values to DATETIME columns using either strings or numbers.
An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0.

TIMESTAMP[(fsp)]
> A timestamp. The range is '1970-01-01 00:00:01.000000' to '2038-01-19 03:14:07.999999'.
An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0.
An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0.

TIME[(fsp)]
> A time. The range is '-838:59:59.000000' to '838:59:59.000000'. TiDB displays TIME values in 'HH:MM:SS[.fraction]' format.
An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0.

YEAR[(4)]
> A year in four-digit format. Values display as 1901 to 2155, and 0000.

```
