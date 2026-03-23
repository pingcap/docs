---
title: Loading from Files
summary: TiDB Cloud Lake offers simple, powerful commands to load data files into tables. Most operations require just a single command.
---

# Loading from Files

{{{ .lake }}} offers simple, powerful commands to load data files into tables. Most operations require just a single command. Your data must be in a [supported format](/tidb-cloud-lake/sql/input-output-file-formats.md).

![Data Loading and Unloading Overview](/media/tidb-cloud-lake/load-unload.jpeg)

## Supported File Formats

| Format | Type | Description |
|--------|------|-------------|
| [**CSV**](/tidb-cloud-lake/guides/load-csv.md), [**TSV**](/tidb-cloud-lake/guides/load-tsv.md) | Delimited | Text files with customizable delimiters |
| [**NDJSON**](/tidb-cloud-lake/guides/load-ndjson.md) | Semi-structured | JSON objects, one per line |
| [**Parquet**](/tidb-cloud-lake/guides/load-parquet.md) | Semi-structured | Efficient columnar storage format |
| [**ORC**](/tidb-cloud-lake/guides/load-orc.md) | Semi-structured | High-performance columnar format |
| [**Avro**](/tidb-cloud-lake/guides/load-avro.md) | Semi-structured | Compact binary format with schema |

## Loading by File Location

Select the location of your files to find the recommended loading method:

| Data Source | Recommended Tool | Description | Documentation |
|-------------|-----------------|-------------|---------------|
| **Staged Data Files** | **COPY INTO** | Fast, efficient loading from internal/external stages or user stage | [Loading from Stage](/tidb-cloud-lake/guides/load-from-stage.md) |
| **Cloud Storage** | **COPY INTO** | Load from Amazon S3, Google Cloud Storage, Microsoft Azure | [Loading from Bucket](/tidb-cloud-lake/guides/load-from-bucket.md) |
| **Local Files** | [**BendSQL**](https://github.com/databendlabs/BendSQL) | Databend's native CLI tool for local file loading | [Loading from Local File](/tidb-cloud-lake/guides/load-from-local-file.md) |
| **Remote Files** | **COPY INTO** | Load data from remote HTTP/HTTPS locations | [Loading from Remote File](/tidb-cloud-lake/guides/load-from-remote-file.md) |
