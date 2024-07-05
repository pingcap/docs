---
title: TiDB Data Type
summary: Learn about default values for data types in TiDB.
aliases: ['/docs/dev/data-type-default-values/','/docs/dev/reference/sql/data-types/default-values/']
---

# Default Values

The `DEFAULT` value clause in a data type specification indicates a default value for a column.

You can set default values for all data types. Typically, default values must be constants and cannot be functions or expressions, but there are some exceptions:

- For time types, you can use `NOW`, `CURRENT_TIMESTAMP`, `LOCALTIME`, and `LOCALTIMESTAMP` functions as default values for `TIMESTAMP` and `DATETIME` columns.
- For integer types, you can use the `NEXT VALUE FOR` function to set the next value of a sequence as the default value for a column, and use the [`RAND()`](/functions-and-operators/numeric-functions-and-operators.md) function to generate a random floating-point value as the default value for a column.
- For string types, you can use the [`UUID()`](/functions-and-operators/miscellaneous-functions.md) function to generate a [universally unique identifier (UUID)](/best-practices/uuid.md) as the default value for a column.
- For binary types, you can use the [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md) function to convert a UUID to the binary format and set the converted value as the default value for a column.
- Starting from v8.0.0, TiDB additionally supports [specifying the default values](#specify-expressions-as-default-values) for [`BLOB`](/data-type-string.md#blob-type), [`TEXT`](/data-type-string.md#text-type), and [`JSON`](/data-type-json.md#json-type) data types, but you can only use expressions to set the [default values](#default-values) for them.

If a column definition includes no explicit `DEFAULT` value, TiDB determines the default value as follows:

- If the column can take `NULL` as a value, the column is defined with an explicit `DEFAULT NULL` clause.
- If the column cannot take `NULL` as the value, TiDB defines the column with no explicit `DEFAULT` clause.

For data entry into a `NOT NULL` column that has no explicit `DEFAULT` clause, if an `INSERT` or `REPLACE` statement includes no value for the column, TiDB handles the column according to the SQL mode in effect at the time:

- If strict SQL mode is enabled, an error occurs for transactional tables, and the statement is rolled back. For nontransactional tables, an error occurs.
- If strict mode is not enabled, TiDB sets the column to the implicit default value for the column data type.

Implicit defaults are defined as follows:

- For numeric types, the default is 0. If declared with the `AUTO_INCREMENT` attribute, the default is the next value in the sequence.
- For date and time types other than `TIMESTAMP`, the default is the appropriate "zero" value for the type. For `TIMESTAMP`, the default value is the current date and time.
- For string types other than `ENUM`, the default value is the empty string. For `ENUM`, the default is the first enumeration value.

## Specify expressions as default values

Starting from 8.0.13, MySQL supports specifying expressions as default values in the `DEFAULT` clause. For more information, see [Explicit default handling as of MySQL 8.0.13](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html#data-type-defaults-explicit).

Starting from v8.0.0, TiDB additionally supports specifying the following expressions as default values in the `DEFAULT` clause.

* `UPPER(SUBSTRING_INDEX(USER(), '@', 1))`
* `REPLACE(UPPER(UUID()), '-', '')`
* `DATE_FORMAT` expressions in the following formats:
    * `DATE_FORMAT(NOW(), '%Y-%m')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H.%i.%s')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s')`
* `STR_TO_DATE('1980-01-01', '%Y-%m-%d')`

Starting from v8.0.0, TiDB additionally supports assigning default values to `BLOB`, `TEXT`, and `JSON` data types. However, you can only use expressions to set the default values for these data types. The following is an example of `BLOB`:

```sql
CREATE TABLE t2 (b BLOB DEFAULT (RAND()));
```
