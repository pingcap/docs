---
title: TiDB Data Type
summary: Learn about default values for data types in TiDB.
aliases: ['/docs/dev/data-type-default-values/','/docs/dev/reference/sql/data-types/default-values/']
---

# Default Values

The `DEFAULT` value clause in a data type specification indicates a default value for a column. The default value must be a constant and cannot be a function or an expression. But for the time type, you can specify the `NOW`, `CURRENT_TIMESTAMP`, `LOCALTIME`, and `LOCALTIMESTAMP` functions as the default for `TIMESTAMP` and `DATETIME` columns.

Starting from v8.0.0, TiDB supports [specifying expressions as default values](#specify-expressions-as-default-values) for [`BLOB`](/data-type-string.md#blob-type), [`TEXT`](/data-type-string.md#text-type), and [`JSON`](/data-type-json.md#json-type) data types.

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

> **Warning:**
>
> Currently, this feature is experimental. It is not recommended that you use it in production environments. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

Starting from 8.0.13, MySQL supports specifying expressions as default values in the `DEFAULT` clause. For more information, see [Explicit default handling as of MySQL 8.0.13](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html#data-type-defaults-explicit). 

TiDB has implemented this feature and supports specifying some expressions as default values in the `DEFAULT` clause. Starting from v8.0.0, TiDB supports assigning default values to `BLOB`, `TEXT`, and `JSON` data types. However, these default values can only be set as expressions. The following is an example of `BLOB`:

```sql
CREATE TABLE t2 (b BLOB DEFAULT (RAND()));
```

TiDB currently supports the following expressions:

* [`RAND()`](/functions-and-operators/numeric-functions-and-operators.md)
* [`UUID()`](/functions-and-operators/miscellaneous-functions.md)
* [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md)

Starting from TiDB v8.0.0, the `DEFAULT` clause supports using the following expressions to set default values.

* `UPPER(SUBSTRING_INDEX(USER(), '@', 1))`

* `REPLACE(UPPER(UUID()), '-', '')`

* The `DATE_FORMAT` supports the following formats:

    * `DATE_FORMAT(NOW(), '%Y-%m')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H.%i.%s')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s')`

* `STR_TO_DATE('1980-01-01', '%Y-%m-%d')`

> **Note:**
>
> Currently, the `ADD COLUMN` statement does not support using expressions as default values.
