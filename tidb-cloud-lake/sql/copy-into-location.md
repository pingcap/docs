---
title: "COPY INTO <location>"
sidebar_label: "COPY INTO <location>"
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.881"/>

COPY INTO allows you to unload data from a table or query into one or more files in one of the following locations:

- User / Internal / External stages: See [What is Stage?](/guides/load-data/stage/what-is-stage) to learn about stages in Databend.
- Buckets or containers created in a storage service.

See also: [`COPY INTO <table>`](dml-copy-into-table.md)

## Syntax

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
[ PARTITION BY ( <expr> ) ]
[ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET } [ formatTypeOptions ]
       ) ]
[ copyOptions ]
[ VALIDATION_MODE = RETURN_ROWS ]
[ DETAILED_OUTPUT = true | false ]
```

### internalStage

```sql
internalStage ::= @<internal_stage_name>[/<path>]
```

### externalStage

```sql
externalStage ::= @<external_stage_name>[/<path>]
```

### externalLocation

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs groupId="externallocation">

<TabItem value="Amazon S3-like Storage Services" label="Amazon S3-like Storage Services">

```sql
externalLocation ::=
  's3://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

For the connection parameters available for accessing Amazon S3-like storage services, see [Connection Parameters](/00-sql-reference/51-connect-parameters.md).
</TabItem>

<TabItem value="Azure Blob Storage" label="Azure Blob Storage">

```sql
externalLocation ::=
  'azblob://<container>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

For the connection parameters available for accessing Azure Blob Storage, see [Connection Parameters](/00-sql-reference/51-connect-parameters.md).
</TabItem>

<TabItem value="Google Cloud Storage" label="Google Cloud Storage">

```sql
externalLocation ::=
  'gcs://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

For the connection parameters available for accessing Google Cloud Storage, see [Connection Parameters](/00-sql-reference/51-connect-parameters.md).
</TabItem>

<TabItem value="Alibaba Cloud OSS" label="Alibaba Cloud OSS">

```sql
externalLocation ::=
  'oss://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

For the connection parameters available for accessing Alibaba Cloud OSS, see [Connection Parameters](/00-sql-reference/51-connect-parameters.md).
</TabItem>

<TabItem value="Tencent Cloud Object Storage" label="Tencent Cloud Object Storage">

```sql
externalLocation ::=
  'cos://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

For the connection parameters available for accessing Tencent Cloud Object Storage, see [Connection Parameters](/00-sql-reference/51-connect-parameters.md).
</TabItem>

</Tabs>

### FILE_FORMAT

See [Input & Output File Formats](../../00-sql-reference/50-file-format-options.md) for details.

### PARTITION BY

Specifies an expression used to partition the unloaded data into separate folders. The expression must evaluate to a `STRING` type. Each distinct value produced by the expression creates a subfolder in the destination path, and the corresponding rows are written into files under that subfolder.

- If the expression evaluates to `NULL`, the rows are placed in a special `_NULL_` folder.
- The expression can reference any columns from the source table or query.
- Path traversal (`..`) is not allowed in partition values.

The following options are incompatible with `PARTITION BY` and will cause an error if set:

| Option              | Restriction                                      |
| ------------------- | ------------------------------------------------ |
| SINGLE              | Cannot be `TRUE` when using `PARTITION BY`.      |
| OVERWRITE           | Cannot be `TRUE` when using `PARTITION BY`.      |
| INCLUDE_QUERY_ID    | Cannot be `FALSE` when using `PARTITION BY`.     |

### copyOptions

```sql
copyOptions ::=
  [ SINGLE = true | false ]
  [ MAX_FILE_SIZE = <num> ]
  [ OVERWRITE = true | false ]
  [ INCLUDE_QUERY_ID = true | false ]
  [ USE_RAW_PATH = true | false ]
```

| Parameter        | Default                | Description                                                                                                                                                                    |
| ---------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SINGLE           | false                  | When `true`, the command unloads data into one single file.                                                                                                                    |
| MAX_FILE_SIZE    | 67108864 bytes (64 MB) | The maximum size (in bytes) of each file to be created. Effective when `SINGLE` is false.                                                                                      |
| OVERWRITE        | false                  | When `true`, existing files with the same name at the target path will be overwritten. Note: `OVERWRITE = true` requires `USE_RAW_PATH = true` and `INCLUDE_QUERY_ID = false`. |
| INCLUDE_QUERY_ID | true                   | When `true`, a unique UUID will be included in the exported file names.                                                                                                        |
| USE_RAW_PATH     | false                  | When `true`, the exact user-provided path (including the full file name) will be used for exporting the data. If set to `false`, the user must provide a directory path.       |

### DETAILED_OUTPUT

Determines whether a detailed result of the data unloading should be returned, with the default value set to `false`. For more information, see [Output](#output).

## Output

COPY INTO provides a summary of the data unloading results with these columns:

| Column        | Description                                                                                   |
| ------------- | --------------------------------------------------------------------------------------------- |
| rows_unloaded | The number of rows successfully unloaded to the destination.                                  |
| input_bytes   | The total size, in bytes, of the data read from the source table during the unload operation. |
| output_bytes  | The total size, in bytes, of the data written to the destination.                             |

When `DETAILED_OUTPUT` is set to `true`, COPY INTO provides results with the following columns. This assists in locating the unloaded files, especially when using `MAX_FILE_SIZE` to separate the unloaded data into multiple files.

| Column    | Description                                        |
| --------- | -------------------------------------------------- |
| file_name | The name of the unloaded file.                     |
| file_size | The size of the unloaded file in bytes.            |
| row_count | The number of rows contained in the unloaded file. |

## Examples

In this section, the provided examples make use of the following table and data:

```sql
-- Create sample table
CREATE TABLE canadian_city_population (
     city_name VARCHAR(50),
     population INT
);

-- Insert sample data
INSERT INTO canadian_city_population (city_name, population)
VALUES
('Toronto', 2731571),
('Montreal', 1704694),
('Vancouver', 631486),
('Calgary', 1237656),
('Ottawa', 934243),
('Edmonton', 972223),
('Quebec City', 542298),
('Winnipeg', 705244),
('Hamilton', 536917),
('Halifax', 403390);
```

### Example 1: Unloading to Internal Stage

This example unloads data to an internal stage:

```sql
-- Create an internal stage
CREATE STAGE my_internal_stage;

-- Unload data from the table to the stage using the PARQUET file format
COPY INTO @my_internal_stage
    FROM canadian_city_population
    FILE_FORMAT = (TYPE = PARQUET);

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         211 │          572 │
└────────────────────────────────────────────┘

LIST @my_internal_stage;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               name                              │  size  │        md5       │         last_modified         │      creator     │
├─────────────────────────────────────────────────────────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ data_abe520a3-ee88-488c-9221-b07c562c9a30_0000_00000000.parquet │    572 │ NULL             │ 2024-01-18 16:20:48.979 +0000 │ NULL             │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Example 2: Unloading to Compressed File

This example unloads data into a compressed file:

```sql
-- Create an internal stage
CREATE STAGE my_internal_stage;

-- Unload data from the table to the stage using the CSV file format with gzip compression
COPY INTO @my_internal_stage
    FROM canadian_city_population
    FILE_FORMAT = (TYPE = CSV COMPRESSION = gzip);

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         182 │          168 │
└────────────────────────────────────────────┘

LIST @my_internal_stage;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │  size  │        md5       │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ data_7970afa5-32e3-4e7d-b793-e42a2a82a8e6_0000_00000000.csv.gz │    168 │ NULL             │ 2024-01-18 16:27:01.663 +0000 │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- COPY INTO also works with custom file formats. See below:
-- Create a custom file format named my_csv_gzip with CSV format and gzip compression
CREATE FILE FORMAT my_csv_gzip TYPE = CSV COMPRESSION = gzip;

-- Unload data from the table to the stage using the custom file format my_csv_gzip
COPY INTO @my_internal_stage
    FROM canadian_city_population
    FILE_FORMAT = (FORMAT_NAME = 'my_csv_gzip');

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         182 │          168 │
└────────────────────────────────────────────┘

LIST @my_internal_stage;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │  size  │        md5       │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ data_d006ba1c-0609-46d7-a67b-75c7078d86ff_0000_00000000.csv.gz │    168 │ NULL             │ 2024-01-18 16:29:29.721 +0000 │ NULL             │
│ data_7970afa5-32e3-4e7d-b793-e42a2a82a8e6_0000_00000000.csv.gz │    168 │ NULL             │ 2024-01-18 16:27:01.663 +0000 │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Example 3: Unloading to Bucket

This example unloads data into a bucket on MinIO:

```sql
-- Unload data from the table to a bucket named 'databend' on MinIO using the PARQUET file format
COPY INTO 's3://databend'
    CONNECTION = (
    ENDPOINT_URL = 'http://localhost:9000/',
    ACCESS_KEY_ID = 'ROOTUSER',
    SECRET_ACCESS_KEY = 'CHANGEME123',
    region = 'us-west-2'
    )
    FROM canadian_city_population
    FILE_FORMAT = (TYPE = PARQUET);

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         211 │          572 │
└────────────────────────────────────────────┘
```

![Alt text](/img/sql/copy-into-bucket.png)

### Example 4: Unloading with PARTITION BY

This example unloads data into partitioned folders based on a derived expression:

```sql
-- Create a sample table
CREATE TABLE sales_data (
    sale_date DATE,
    region VARCHAR,
    amount INT
);

INSERT INTO sales_data VALUES
    ('2025-01-15', 'east', 100),
    ('2025-01-20', 'west', 200),
    ('2025-02-10', 'east', 150),
    (NULL, 'west', 50);

-- Create an internal stage
CREATE STAGE partitioned_stage;

-- Unload data partitioned by year-month derived from sale_date
-- When sale_date is NULL, to_varchar() returns NULL, so the entire
-- concatenation evaluates to NULL and the row lands in the _NULL_ folder.
COPY INTO @partitioned_stage
    FROM sales_data
    PARTITION BY ('month=' || to_varchar(sale_date, 'YYYY-MM'))
    FILE_FORMAT = (TYPE = PARQUET);

-- Verify the partitioned folder layout
SELECT name FROM list_stage(location => '@partitioned_stage') ORDER BY name;

┌──────────────────────────────────────────────────────────────────┐
│                              name                                │
├──────────────────────────────────────────────────────────────────┤
│ _NULL_/data_<query_id>_0000_00000000.parquet                     │
│ month=2025-01/data_<query_id>_0000_00000000.parquet              │
│ month=2025-02/data_<query_id>_0000_00000000.parquet              │
└──────────────────────────────────────────────────────────────────┘
```

When the partition expression evaluates to `NULL`, the data is placed in a `_NULL_` folder. Each unique partition value creates its own subfolder containing the corresponding data files.
