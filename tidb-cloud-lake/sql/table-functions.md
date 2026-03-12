---
title: Table Functions
---

This page provides reference information for the table functions in Databend. Table functions return a set of rows (similar to a table) and can be used in the FROM clause of a query.

## Data Schema & File Inspection

| Function | Description | Example |
|----------|-------------|--------|
| [INFER_SCHEMA](./01-infer-schema.md) | Detects file metadata schema and retrieves column definitions | `SELECT * FROM INFER_SCHEMA(LOCATION => '@mystage/data/')` |
| [INSPECT_PARQUET](./02-inspect-parquet.md) | Inspects the structure of Parquet files | `SELECT * FROM INSPECT_PARQUET(LOCATION => '@mystage/data.parquet')` |

## Stage & Query Management

| Function | Description | Example |
|----------|-------------|--------|
| [LIST_STAGE](./03-list-stage.md) | Lists files in a stage | `SELECT * FROM LIST_STAGE(LOCATION => '@mystage/data/')` |
| [READ_FILE](./read-file.md) | Reads file content from a stage as binary | `SELECT read_file('@mystage/file.csv')` |
| [RESULT_SCAN](./result-scan.md) | Retrieves the result set of a previous query | `SELECT * FROM RESULT_SCAN(LAST_QUERY_ID())` |

## Data Generation

| Function | Description | Example |
|----------|-------------|--------|
| [GENERATE_SERIES](./05-generate-series.md) | Generates a sequence of values | `SELECT * FROM GENERATE_SERIES(1, 10, 2)` |

## Data Transformation & Expansion

| Function | Description | Example |
|----------|-------------|--------|
| [FLATTEN](./flatten.md) | Transforms nested JSON or array data into tabular format | `SELECT * FROM FLATTEN(INPUT => parse_json('[1,2,3]'))` |

## System Information & Management

| Function | Description | Example |
|----------|-------------|--------|
| [SHOW_GRANTS](./show-grants.md) | Shows granted privileges | `SELECT * FROM SHOW_GRANTS()` |
| [SHOW_VARIABLES](./show-variables.md) | Shows system variables | `SELECT * FROM SHOW_VARIABLES()` |
| [STREAM_STATUS](./stream-status.md) | Shows stream status information | `SELECT * FROM STREAM_STATUS('mystream')` |
| [TASK_HISTROY](./task_histroy.md) | Shows task execution history | `SELECT * FROM TASK_HISTROY('mytask')` |
| [POLICY_REFERENCES](./policy-references.md) | Returns associations between security policies and tables/views | `SELECT * FROM POLICY_REFERENCES(POLICY_NAME => 'mypolicy')` |

## Storage Engine Functions

| Function | Description | Example |
|----------|-------------|--------|
| [FUSE_VACUUM_TEMPORARY_TABLE](./fuse-vacuum-temporary-table.md) | Cleans up temporary tables | `SELECT * FROM FUSE_VACUUM_TEMPORARY_TABLE()` |
| [FUSE_AMEND](./fuse-amend.md) | Manages data amendments | `SELECT * FROM FUSE_AMEND()` |

## Iceberg Integration

| Function | Description | Example |
|----------|-------------|--------|
| [ICEBERG_MANIFEST](./iceberg-manifest.md) | Shows Iceberg table manifest information | `SELECT * FROM ICEBERG_MANIFEST('mytable')` |
| [ICEBERG_SNAPSHOT](./iceberg-snapshot.md) | Shows Iceberg table snapshot information | `SELECT * FROM ICEBERG_SNAPSHOT('mytable')` |

## Anonymization

| Function | Description | Example |
|----------|-------------|---------|
| [OBFUSCATE](../19-data-anonymization-functions/obfuscate.md) | dataset anonymization | `SELECT * FROM OBFUSCATE(users)` |
