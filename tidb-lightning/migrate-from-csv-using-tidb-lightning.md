---
title: TiDB Lightning CSV Support and Restrictions
summary: Learn how to import CSV files via TiDB Lightning.
aliases: ['/docs/dev/tidb-lightning/migrate-from-csv-using-tidb-lightning/','/docs/dev/reference/tools/tidb-lightning/csv/']
---

# TiDB Lightning CSV Support and Restrictions

This document describes how to migrate data from CSV files to TiDB using TiDB Lightning. For information about how to generate CSV files from MySQL, see [Export to CSV files using Dumpling](/dumpling-overview.md#export-to-csv-files).

TiDB Lightning supports reading CSV (comma-separated values) data source, as well as other delimited format such as TSV (tab-separated values).

## File name

A CSV file representing a whole table must be named as `db_name.table_name.csv`. This will be restored as a table `table_name` inside the database `db_name`.

If a table spans multiple CSV files, they should be named like `db_name.table_name.003.csv`. The number part do not need to be continuous, but must be increasing and zero-padded.

The file extension must be `*.csv`, even if the content is not separated by commas.

## Schema

CSV files are schema-less. To import them into TiDB, a table schema must be provided. This could be done either by:

* Providing a file named `db_name.table_name-schema.sql` containing the `CREATE TABLE` DDL statement, and also a file named `db_name-schema-create.sql` containing the `CREATE DATABASE` DDL statement.
* Manually creating the table schema in TiDB.

## Configuration

The CSV format can be configured in `tidb-lightning.toml` under the `[mydumper.csv]` section. Most settings have a corresponding option in the MySQL [`LOAD DATA`] statement.

```toml
[mydumper.csv]
# Separator between fields. Must be ASCII characters. It is not recommended to use the default ','. It is recommended to use '\|+\|' or other uncommon character combinations.
separator = ','
# Quoting delimiter. Empty value means no quoting.
delimiter = '"'
# Line terminator. Empty value means both "\n" (LF) and "\r\n" (CRLF) are line terminators.
terminator = ''
# Whether the CSV files contain a header.
# If `header` is true, the first line will be skipped.
header = true
# Whether the CSV contains any NULL value.
# If `not-null` is true, all columns from CSV cannot be NULL.
not-null = false
# When `not-null` is false (that is, CSV can contain NULL),
# fields equal to this value will be treated as NULL.
null = '\N'
# Whether to interpret backslash escapes inside fields.
backslash-escape = true
# If a line ends with a separator, remove it.
trim-last-separator = false
```

In all string fields such as `separator`, `delimiter` and `terminator`, if the input involves special characters, you can use backslash escape sequence to represent them in a *double-quoted* string (`"…"`). For example, `separator = "\u001f"` means using the ASCII character 0x1F as separator.

Additionally, you can use *single-quoted* strings (`'…'`) to suppress backslash escaping. For example, `terminator = '\n'` means using the two-character string: a backslash followed by the letter "n", as the terminator.

See the [TOML v1.0.0 specification] for details.

[`LOAD DATA`]: https://dev.mysql.com/doc/refman/8.0/en/load-data.html

[TOML v1.0.0 specification]: https://toml.io/en/v1.0.0#string

### `separator`

- Defines the field separator.
- Can be multiple characters, but must not be empty.
- Common values:

    * `','` for CSV (comma-separated values)
    * `"\t"` for TSV (tab-separated values)
    * `"\u0001"` to use the ASCII character 0x01 as separator

- Corresponds to the `FIELDS TERMINATED BY` option in the LOAD DATA statement.

### `delimiter`

- Defines the delimiter used for quoting.
- If `delimiter` is empty, all fields are unquoted.
- Common values:

    * `'"'` quote fields with double-quote, same as [RFC 4180]
    * `''` disable quoting

- Corresponds to the `FIELDS ENCLOSED BY` option in the `LOAD DATA` statement.

[RFC 4180]: https://tools.ietf.org/html/rfc4180

### `terminator`

- Defines the line terminator.
- If `terminator` is empty, both `"\r"` (U+000D Carriage Return) and `"\n"` (U+000A Line Feed) are used as terminator.
- Corresponds to the `LINES TERMINATED BY` option in the `LOAD DATA` statement.

### `header`

- Whether *all* CSV files contain a header row.
- If `header` is true, the first row will be used as the *column names*. If `header` is false, the first row is not special and treated as an ordinary data row.

### `not-null` and `null`

- The `not-null` setting controls whether all fields are non-nullable.
- If `not-null` is false, the string specified by `null` will be transformed to the SQL NULL instead of a concrete value.
- Quoting will not affect whether a field is null.

    For example, with the CSV file:

    ```csv
    A,B,C
    \N,"\N",
    ```

    In the default settings (`not-null = false; null = '\N'`), the columns `A` and `B` are both converted to NULL after importing to TiDB. The column `C` is simply the empty string `''` but not NULL.

### `backslash-escape`

- Whether to interpret backslash escapes inside fields.
- If `backslash-escape` is true, the following sequences are recognized and transformed:

    | Sequence | Converted to             |
    |----------|--------------------------|
    | `\0`     | Null character (U+0000)  |
    | `\b`     | Backspace (U+0008)       |
    | `\n`     | Line feed (U+000A)       |
    | `\r`     | Carriage return (U+000D) |
    | `\t`     | Tab (U+0009)             |
    | `\Z`     | Windows EOF (U+001A)     |

    In all other cases (for example, `\"`) the backslash is simply stripped, leaving the next character (`"`) in the field. The character left has no special roles (for example, delimiters) and is just an ordinary character.

- Quoting will not affect whether backslash escapes are interpreted.

- Corresponds to the `FIELDS ESCAPED BY '\'` option in the `LOAD DATA` statement.

### `trim-last-separator`

- Treats the field `separator` as a terminator, and removes all trailing separators.

    For example, with the CSV file:

    ```csv
    A,,B,,
    ```

- When `trim-last-separator = false`, this is interpreted as a row of 5 fields `('A', '', 'B', '', '')`.
- When `trim-last-separator = true`, this is interpreted as a row of 3 fields `('A', '', 'B')`.

- This option is deprecated, because the behavior with multiple trailing separators is not intuitive. Use the `terminator` option instead. If your old configuration was

    ```toml
    separator = ','
    trim-last-separator = true
    ```

    we recommend changing this to

    ```toml
    separator = ','
    terminator = ",\n"
    ```

### Non-configurable options

TiDB Lightning does not support every option supported by the `LOAD DATA` statement. Some examples:

* There cannot be line prefixes (`LINES STARTING BY`).
* The header cannot be simply skipped (`IGNORE n LINES`). It must be valid column names if present.

## Strict format

Lightning works the best when the input files have uniform size around 256 MB. When the input is a single huge CSV file, Lightning can only use one thread to process it, which slows down import speed a lot.

This can be fixed by splitting the CSV into multiple files first. For the generic CSV format, there is no way to quickly identify when a row starts and ends without reading the whole file. Therefore, Lightning by default does *not* automatically split a CSV file. However, if you are certain that the CSV input adheres to certain restrictions, you can enable the `strict-format` setting to allow Lightning to split the file into multiple 256 MB-sized chunks for parallel processing.

```toml
[mydumper]
strict-format = true
```

Currently, a strict CSV file means every field occupies only a single line. In other words, one of the following must be true:

* Delimiter is empty, or
* Every field does not contain the terminator itself. In the default configuration, this means every field does not contain CR (`\r`) or LF (`\n`).

If a CSV file is not strict, but `strict-format` was wrongly set to `true`, a field spanning multiple lines may be cut in half into two chunks, causing parse failure, or even worse, quietly importing corrupted data.

## Common configurations

### CSV

The default setting is already tuned for CSV following RFC 4180.

```toml
[mydumper.csv]
separator = ',' # It is not recommended to use the default ','. It is recommended to use '\|+\|' or other uncommon character combinations.
delimiter = '"'
header = true
not-null = false
null = '\N'
backslash-escape = true
```

Example content:

```
ID,Region,Count
1,"East",32
2,"South",\N
3,"West",10
4,"North",39
```

### TSV

```toml
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
```

Example content:

```
ID    Region    Count
1     East      32
2     South     NULL
3     West      10
4     North     39
```

### TPC-H DBGEN

```toml
[mydumper.csv]
separator = '|'
delimiter = ''
terminator = "|\n"
header = false
not-null = true
backslash-escape = false
```

Example content:

```
1|East|32|
2|South|0|
3|West|10|
4|North|39|
```
