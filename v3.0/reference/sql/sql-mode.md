---
title: SQL Mode
summary: Learn SQL mode.
category: reference
---

# SQL Mode

TiDB servers are operated in different SQL modes, and different clients might use different modes. SQL mode defines which SQL syntaxes are supported by TiDB and which type of data validation check is to perform.

+ Before TiDB is started, you can modify the `--sql-mode="modes"` configuration item to set SQL mode.

+ After TiDB is started, you can modify `SET [ SESSION | GLOBAL ] sql_mode='modes'` to set SQL mode.

You must have `SUPER` privilege when setting SQL mode at the `GLOBAL` level. Only the newly established connections after your setting are affected, and the old connections are not affected. Changes to SQL mode at the `SESSION` level only affect the current client.

`Modes` are a series of different modes separated by commas (','). You can use the `SELECT @@sql_mode` statement to check the current SQL mode. The default value of SQL mode: `ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, NO_ENGINE_SUBSTITUTION`.

## Important `sql_mode` value

* `ANSI`: This mode complies with standard SQL and data is verified in this mode. If data does not comply with the defined type or length, data types are adjusted or truncated and a `warning` is returned.
* `STRICT_TRANS_TABLES`: In this strict mode, data is strictly checked. When any data goes wrong, it is inserted into a table and an error is returned.
* `TRADITIONAL`: In this mode, TiDB behaves like a "traditional" SQL database system. An error instead of a warning is returned when any incorrect value is inserted into a column. Then the `INSERT` or `UPDATE` statement is immediately abandoned if an error is found.

## SQL mode table

| Name | Description |
| --- | --- |
| `PIPES_AS_CONCAT` | Treat "\|\|" as a string concatenation operator (`+`) (the same as `CONCAT()`), not as an `OR` (supported) |
| `ANSI_QUOTES` | Treat `"` as an identifier. If `ANSI_QUOTES` is enabled, only single quotes are treated as string literals, and double quotes are interpreted as identifiers, so double quotes cannot be used to quote strings. (supported)|
| `IGNORE_SPACE` | If this mode is enabled, the system ignores space. For example: "user" and "user " are the same. (supported)|
| `ONLY_FULL_GROUP_BY` | If the column that appears in `GROUP BY` is absent in `SELECT`, `HAVING`, or `ORDER BY`, the SQL statement is illegal, because it is abnormal for a column to be absent in `GROUP BY` but displayed by query. (supported) |
| `NO_UNSIGNED_SUBTRACTION` | In subtraction, if an operand has no symbol, do not mark the result as `UNSIGNED`. (supported)|
| `NO_DIR_IN_CREATE` | Ignore all `INDEX DIRECTORY` and `DATA DIRECTORY` directives when a table is created. This option is only useful for replication servers (syntax support only) |
| `NO_KEY_OPTIONS` | When you use the `SHOW CREATE TABLE` statement, MySQL-specific syntaxes are not exported, such as `ENGINE`. You must consider this option when migrating across DB types using mysqldump. (syntax support only)|
| `NO_FIELD_OPTIONS` | When you use the `SHOW CREATE TABLE` statement, MySQL-specific syntaxes are not exported, such as `ENGINE`. You must consider this option when migrating across DB types using mysqldump. (syntax support only) |
| `NO_TABLE_OPTIONS` | When you use the `SHOW CREATE TABLE` statement, MySQL-specific syntaxes are not exported, such as `ENGINE`. You must consider this option when migrating across DB types using mysqldump. (syntax support only)|
| `NO_AUTO_VALUE_ON_ZERO` | If this mode is enabled, when the value passed in the `AUTO_INCREMENT` column is `0` or a specific value, the system directly writes this value to this column. When `NULL` is passed, the system automatically generates the next serial number. (supported)|
| `NO_BACKSLASH_ESCAPES` | If this mode is enabled, the `\` backslash symbol only stands for itself. (support)|
| `STRICT_TRANS_TABLES` | To enable the strict mode for the transaction storage engine and roll back the entire statement after an illegal value is inserted. (supported) |
| `STRICT_ALL_TABLES` | For transactional tables, to roll back the entire transaction statement after an illegal value is inserted. (support) |
| `NO_ZERO_IN_DATE` | In strict mode, dates with a month or day part of `0` are not accepted. If you use the `IGNORE` option, TiDB inserts '0000-00-00' for a similar date. In non-strict mode, this date is accepted but a warning is returned. (supported)
| `NO_ZERO_DATE` | In strict mode, do not use '0000-00-00' as a legal date. You can still insert a zero date with the `IGNORE` option. In non-strict mode, this date is accepted but a warning is returned. (supported)|
| `ALLOW_INVALID_DATES` | In this mode, the system does not check the validity of all dates but only that of the month value between `1` and `12` and the date value between `1` and `31` for the `DATE` and `DATATIME` columns only. All `TIMESTAMP` columns need this validity check. (supported) |
| `ERROR_FOR_DIVISION_BY_ZERO` | If this mode is enabled, the system returns an error when the dividend is `0` in the `INSERT` or `UPDATE` process. <br> If this mode is not enabled, the system returns a warning and `NULL` is used instead. (supported) |
| `NO_AUTO_CREATE_USER` | To prevent `GRANT` from automatically creating new users, except for the specified password (supported)|
| `HIGH_NOT_PRECEDENCE` | The priority of the `NOT` operator is an expression. For example: `NOT a BETWEEN b AND c` is interpreted as `NOT (a BETWEEN b AND c)`. In some older versions of MySQL, this expression is interpreted as `(NOT a) BETWEEN b AND c`. (supported) |
| `NO_ENGINE_SUBSTITUTION` | To prevent the automatic replacement of storage engines if the required storage engine is disabled or not compiled. (syntax support only)|
| `PAD_CHAR_TO_FULL_LENGTH` | If this mode is enabled, the system does not truncate the trailing spaces for `CHAR` types. (supported) |
| `REAL_AS_FLOAT` | Treat `REAL` as the synonym of `FLOAT`, not the synonym of `DOUBLE` (supported)|
| `POSTGRESQL` | Equivalent to `PIPES_AS_CONCAT`, `ANSI_QUOTES`, `IGNORE_SPACE`, `NO_KEY_OPTIONS`, `NO_TABLE_OPTIONS`, `NO_FIELD_OPTIONS` (supported)|
| `MSSQL` | Equivalent to `PIPES_AS_CONCAT`, `ANSI_QUOTES`, `IGNORE_SPACE`, `NO_KEY_OPTIONS`, `NO_TABLE_OPTIONS`, `NO_FIELD_OPTIONS` (supported)|
| `DB2` | Equivalent to `PIPES_AS_CONCAT`, `ANSI_QUOTES`, `IGNORE_SPACE`, `NO_KEY_OPTIONS`, `NO_TABLE_OPTIONS`, `NO_FIELD_OPTIONS` (supported)|
| `MAXDB` | Equivalent to `PIPES_AS_CONCAT`, `ANSI_QUOTES`, `IGNORE_SPACE`, `NO_KEY_OPTIONS`, `NO_TABLE_OPTIONS`, `NO_FIELD_OPTIONS`, `NO_AUTO_CREATE_USER` (supported)|
| `MySQL323` | Equivalent to `NO_FIELD_OPTIONS`, `HIGH_NOT_PRECEDENCE` (supported)|
| `MYSQL40` | Equivalent to `NO_FIELD_OPTIONS`, `HIGH_NOT_PRECEDENCE` (supported)|
| `ANSI` | Equivalent to `REAL_AS_FLOAT`, `PIPES_AS_CONCAT`, `ANSI_QUOTES`, `IGNORE_SPACE` (supported)|
| `TRADITIONAL` | Equivalent to `STRICT_TRANS_TABLES`, `STRICT_ALL_TABLES`, `NO_ZERO_IN_DATE`, `NO_ZERO_DATE`, `ERROR_FOR_DIVISION_BY_ZERO`, `NO_AUTO_CREATE_USER` (supported) |
| `ORACLE` | Equivalent to `PIPES_AS_CONCAT`, `ANSI_QUOTES`, `IGNORE_SPACE`, `NO_KEY_OPTIONS`, `NO_TABLE_OPTIONS`, `NO_FIELD_OPTIONS`, `NO_AUTO_CREATE_USER` (supported)|
