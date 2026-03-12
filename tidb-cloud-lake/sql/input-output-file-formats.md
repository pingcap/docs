---
title: Input & Output File Formats
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.713"/>

Databend accepts a variety of file formats both as a source and as a target for data loading or unloading. This page explains the supported file formats and their available options.

## Syntax

To specify a file format in a statement, use the following syntax:

```sql
-- Specify a standard file format
... FILE_FORMAT = ( TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO } [ formatTypeOptions ] )

-- Specify a custom file format
... FILE_FORMAT = ( FORMAT_NAME = '<your-custom-format>' )
```

Databend determines the file format used by a COPY or Select statement in the following order of priority:
1. First, it checks if a FILE_FORMAT is explicitly specified within the statement.
2. If no FILE_FORMAT is specified in the operation, it uses the file format initially defined for the stage at the time of stage creation.
3. If no file format was defined for the stage during its creation, Databend defaults to using the PARQUET format.

:::note
- Databend currently supports ORC and AVRO as a source ONLY. Unloading data into an ORC or AVRO file is not supported yet.
- For managing custom file formats in Databend, see [File Format](../10-sql-commands/00-ddl/13-file-format/index.md).
:::

### formatTypeOptions

`formatTypeOptions` includes one or more options to describe other format details about the file. The options vary depending on the file format. See the sections below to find out the available options for each supported file format.

```sql
formatTypeOptions ::=
  RECORD_DELIMITER = '<character>'
  FIELD_DELIMITER = '<character>'
  SKIP_HEADER = <integer>
  QUOTE = '<character>'
  ESCAPE = '<character>'
  NAN_DISPLAY = '<string>'
  ROW_TAG = '<string>'
  COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | XZ | NONE
```

## CSV Options

Databend CSV is compliant with [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180) and is subject to the following conditions:

- A string must be quoted if it contains the character of a [QUOTE](#quote), [ESCAPE](#escape), [RECORD_DELIMITER](#record_delimiter), or [FIELD_DELIMITER](#field_delimiter).
- No character will be escaped in a quoted string except [QUOTE](#quote).
- No space should be left between a [FIELD_DELIMITER](#field_delimiter) and a [QUOTE](#quote).

### RECORD_DELIMITER

Delimiter character(s) to separates records in a file.

**Available Values**:

- `\r\n`
- A one-byte, non-alphanumeric character, such as `#` and `|`.
- A character with the escape char: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\xHH`

**Default**: `\n`

### FIELD_DELIMITER

Delimiter character to separates fields in a record.

**Available Values**:

- A one-byte, non-alphanumeric character, such as `#` and `|`.
- A character with the escape char: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\xHH`

**Default**: `,` (comma)

### QUOTE (Load Only)

Character used to quote values.

For data loading, the quote is not necessary unless a string contains the character of a [QUOTE](#quote-load-only), [ESCAPE](#escape), [RECORD_DELIMITER](#record_delimiter), or [FIELD_DELIMITER](#field_delimiter).

**Available Values**: `'\''`, `'"'`, or ``'`'``(backtick)

**Default**: `'"'`

### ESCAPE

Character used to escape the quote character within quoted values, in addition to [QUOTE](#quote-load-only) itself. 

In some variants of CSV, quotes are escaped using a special escape character like `\`, instead of escaping quotes by doubling quoting.

**Available Values**: `'\\'` or `''` (emtpy, means only use double quoting)

**Default**: `''`

### SKIP_HEADER (Load Only)

Number of lines to be skipped from the beginning of the file.

**Default**: `0`

### OUTPUT_HEADER (Unload Only)

Include a header row with column names.

**Default**: `false`

### NAN_DISPLAY

String that represent a "NaN" (Not-a-Number).

**Available Values**: Must be literal `'nan'` or `'null'` (case-insensitive)

**Default**: `'NaN'`

### NULL_DISPLAY

String that represent a NULL value.

When loading data, unquoted matches always become NULL, quoted matches convert to NULL only when `ALLOW_QUOTED_NULLS=true`.

**Default**: `'\N'`

### ALLOW_QUOTED_NULLS (Load Only)

Allow the conversion of quoted strings to NULL values. 

Quoted strings that match `NULL_DISPLAY` become NULL only when this flag is true. Unquoted matches become NULL regardless of this option.

**Default**: `false`

### ERROR_ON_COLUMN_COUNT_MISMATCH (Load Only)

Return error if the number of columns in the data file doesn't match the number of columns in the destination table.

**Default**: `true`

### EMPTY_FIELD_AS (Load Only)

The value that unquoted empty fields(i.e `,,`) is converted to.

| Available Values | Convert to                                                          |
|------------------|----------------------------------------------------------------------------------|
| `NULL`           | `NULL`. Error if column is not nullable.                                         |
| `STRING`         | For String columns:`''`. <br/> For other columns: `NULL`. Error if not nullable. |
| `FIELD_DEFAULT`  | The column's default value.                                                      |

**Default**: `NULL`

### QUOTED_EMPTY_FIELD_AS (Load Only)

The value that quoted empty fields(i.e `,"",`) is converted to.

**Available Values**: same as [EMPTY_FIELD_AS](#empty_field_as-load-only)

**Default**: `STRING`

### BINARY_FORMAT

Encoding format for `Binary` column.

**Available Values**: `HEX` or `BASE64`

**Default**: `HEX`

### GEOMETRY_FORMAT

Encoding format for `Geometry` column.

**Available Values**: `EWKT`, `WKB`, `WKB`, `EWKB`, `GEOJSON`

**Default**: `EWKT`

### COMPRESSION

The compression algorithm.

| Available Values | Description                                                     |
|------------------|-----------------------------------------------------------------|
| `NONE`           | Indicates that the files are not compressed.                    |
| `AUTO`           | Auto detect compression via file extensions                     |
| `GZIP`           |                                                                 |
| `BZ2`            |                                                                 |
| `BROTLI`         | Must be specified if loading/unloading Brotli-compressed files. |
| `ZSTD`           | Zstandard v0.8 (and higher) is supported.                       |
| `DEFLATE`        | Deflate-compressed files (with zlib header, RFC1950).           |
| `RAW_DEFLATE`    | Deflate-compressed files (without any header, RFC1951).         |
| `XZ`             |                                                                 |

**Default**: `NONE`

## TSV Options

Databend TSV is subject to the following conditions:

- [RECORD_DELIMITER](#record_delimiter-1), [FIELD_DELIMITER](#field_delimiter-1) are escaped by `\` to resolve [delimter collision](https://en.wikipedia.org/wiki/Delimiter#Delimiter_collision)
- In addition to delimters, these characters in are also escaped: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\\`, `\'`.
- [QUOTE](#quote-load-only) is NOT part of the format.
- NULL is represent as `\N`.

:::note
1. In Databend, the main difference between TSV and CSV is NOT using a tab instead of a comma as a field delemiter (which can be changed by options), but using escaping instead of quoting for 
[delimter collision](https://en.wikipedia.org/wiki/Delimiter#Delimiter_collision)
2. We recommend CSV over TSV as a storage format since it has a formal standard.
3. TSV can be used to load files generated by
   1. [Clickhouse TSV](https://clickhouse.com/docs/integrations/data-formats/csv-tsv#tsv-tab-separated-files)
   2. [MySQL TabSeperated](https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html) MySQL `mysqldump --tab`. If `--fields-enclosed-by` or `--fields-optinally-enclosed-by`, use CSV instead.
   3. [Postgresql TEXT](https://www.postgresql.org/docs/current/sql-copy.html).
   4. [Snowflake CSV](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#type-csv) with default options. If `ESCAPE_UNENCLOSED_FIELD` is specified, use CSV instead.
   5. Hive Textfile.
:::

### RECORD_DELIMITER

Delimiter character(s) to separates records in a file.

**Available Values**:

- `\r\n`
- An arbitrary character, such as `#` and `|`.
- A character with the escape char: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\xHH`

**Default**: `\n`

### FIELD_DELIMITER

Delimiter character to separates fields in a record.

**Available Values**:

- A non-alphanumeric character, such as `#` and `|`.
- A character with the escape char: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\xHH`

**Default**: `\t` (TAB)

### COMPRESSION

Same as [the COMPRESSION option for CSV](#compression).

## NDJSON Options

### NULL_FIELD_AS (Load Only)

The value that `null` is converted to.

| Available Values        | Convert to                                               |
|-------------------------|----------------------------------------------------------|
| `NULL` (Default)        | NULL for nullable fields. Error for non-nullable fields. |
| `FIELD_DEFAULT`         | The default value of the field.                          |

### MISSING_FIELD_AS (Load Only)

The value that missing field is converted to.

| Available Values | Convert to                                               |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| Error.                                                   |
| `NULL`           | NULL for nullable fields. Error for non-nullable fields. |
| `FIELD_DEFAULT`  | The default value of the field.                          |

### COMPRESSION

Same as [the COMPRESSION option for CSV](#compression).

## PARQUET Options

### MISSING_FIELD_AS (Load Only)

The value that missing field is converted to.

| Available Values | Convert to                                               |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| Error.                                                   |
| `FIELD_DEFAULT`  | The default value of the field.                          |

### COMPRESSION (Unload Only)

Compression algorithm for internal blocks of parquet file.

| Available Values | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `ZSTD` (default) | Zstandard v0.8 (and higher) is supported.                                   |
| `SNAPPY`         | Snappy is a popular and fast compression algorithm often used with Parquet. |


## ORC Options


### MISSING_FIELD_AS (Load Only)

The value that missing field is converted to.

| Available Values | Convert to                                               |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| Error.                                                   |
| `FIELD_DEFAULT`  | The default value of the field.                          |


## AVRO Options

### MISSING_FIELD_AS (Load Only)

The value that missing field is converted to.

| Available Values | Convert to                                               |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| Error.                                                   |
| `FIELD_DEFAULT`  | The default value of the field.                          |
