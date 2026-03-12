---
title: Querying & Transforming
slug: querying-stage
---

Databend enables direct querying of staged files without loading data into tables first. Query files from any stage type (user, internal, external) or directly from object storage and HTTPS URLs. Ideal for data inspection, validation, and transformation before or after loading.

## Syntax

query only

```sql
SELECT {
    [<alias>.]<column> [, [<alias>.]<column> ...] -- Query columns by name
  | [<alias>.]$<col_position> [, [<alias>.]$<col_position> ...] -- Query columns by position
  | [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] -- Query rows as Variants
}
FROM {@<stage_name>[/<path>] | '<uri>'}  -- stage table function
  [( -- stage table function parameters
    [<connection_parameters>],
    [ PATTERN => '<regex_pattern>'],
    [ FILE_FORMAT => 'CSV | TSV | NDJSON | PARQUET | ORC | Avro | <custom_format_name>'],
    [ FILES => ( '<file_name>' [ , '<file_name>' ... ])],
    [ CASE_SENSITIVE => true | false ]
  )]
  [<alias>]
```

copy with transform

```sql
COPY INTO [<database_name>.]<table_name> [ ( <col_name> [ , <col_name> ... ] ) ]
     FROM (
        SELECT {
            [<alias>.]<column> [, [<alias>.]<column> ...] -- Query columns by name
            | [<alias>.]$<col_position> [, [<alias>.]$<col_position> ...] -- Query columns by position
            | [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] -- Query rows as Variants
            } ]
        FROM {@<stage_name>[/<path>] | '<uri>'} 
    )
[ FILES = ( '<file_name>' [ , '<file_name>' ] [ , ... ] ) ]
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO } [ formatTypeOptions ]
       ) ]
[ copyOptions ]
```
:::info Note

compared the two syntaxes
- Same `Select List` 
- Same ` FROM {@<stage_name>[/<path>] | '<uri>'}`
- diff parameters:
  - query use `table function parameters`, i.e. `(<key> => <value>, ...)` 
  - transform use Options at the end of [Copy into table](/sql/sql-commands/dml/dml-copy-into-table)

:::


## FROM Clause

the FROM Clause use similar syntax of `Table Function`. Like ordinary tables, table `alias` can be used when join with other tables.

table function parameters:

| Parameter               | Description                                             |
|-------------------------|---------------------------------------------------------|
| `FILE_FORMAT`           | File format type (CSV, TSV, NDJSON, PARQUET, ORC, Avro) |
| `PATTERN`               | Regex pattern to filter files                           |
| `FILES`                 | Explicit list of files to query                         |
| `CASE_SENSITIVE`        | Column name case sensitivity (Parquet only)             |
| `connection_parameters` | External storage connection details                     |

## Query File Data

The select list supports three syntaxes; only one may be used, with no mixing.

### Query rows as Variants

- Supported File Formats: NDJSON, AVRO, Parquet, ORC

:::info Note

Currently for Parquet and ORC, `Query rows as Variants` is slower than `Query columns by name`, and the two methods can not be mix used.

:::

syntax: 

```sql
SELECT [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] <FROM Clause>
```

- Example: `SELECT $1:id, $1:name FROM ...`
- Table Schema: ($1: Variant). i.e. Single Column with Variant Object Type, each Variant representing a whole row
- Notes:
  - The type of path expressions like `$1:column` is Variant too, it can be auto cast to native types when used in expressions or load to dest table column, sometimes you may want to cast manually before for type-specific operations (e.g., `CAST($1:id AS INT)`) to make the semantics more explicit.


### Query columns by name
- supported File Formats: NDJSON, AVRO, Parquet, ORC

```sql
SELECT [<alias>.]<column> [, [<alias>.]<column>  ...] <FROM Clause>
```

- Example: `SELECT id, name FROM ...`
- Table Schema: Columns Mapping from Parquet or ORC file schema
- Notes:
  - All files are required to have the same Parquet/ORC schema; otherwise, an error will be returned


### Query columns by Position 
- supported File Formats: CSV, TSV

```sql
SELECT [<alias>.]$<col_position>[, [<alias>.]$<col_position>,  ...] <FROM Clause>
```
- Example: `SELECT $1, $2 FROM ...`
- Table Schema: Columns of type `VARCHAR NULL`
- Notes
  - `<col_position>` starts from 1

## Query Metadata 

You can also include file metadata in your queries, which is useful for tracking data lineage and debugging:

```sql
SELECT METADATA$FILENAME, METADATA$FILE_ROW_NUMBER, $1, <FROM Clause>
(
    FILE_FORMAT => 'ndjson_query_format',
    PATTERN => '.*[.]ndjson'
);
```

The following file-level metadata fields are available for the supported file formats:

| File Metadata              | Type    | Description                                      |
| -------------------------- | ------- |--------------------------------------------------|
| `METADATA$FILENAME`        | VARCHAR | The path of the file from which the row was read |
| `METADATA$FILE_ROW_NUMBER` | INT     | The row number within the file (starting from 0) |


**Use cases:**
- **Data lineage**: Track which source file contributed each record
- **Debugging**: Identify problematic records by file and line number
- **Incremental processing**: Process only specific files or ranges within files

## Tutorials by File Formats
- [Querying Parquet Files](./00-querying-parquet.md) 
- [Querying ORC Files](./05-querying-orc.md)
- [Querying NDJSON Files](./03-querying-ndjson.md)
- [Querying Avro Files](./04-querying-avro.md)
- [Querying CSV Files](./01-querying-csv.md)
- [Querying TSV Files](./02-querying-tsv.md)
