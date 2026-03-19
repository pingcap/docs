---
title: Unload Data from TiDB Cloud Lake
summary: Databend's COPY INTO command exports data to various file formats and storage locations with flexible formatting options.
---

# Unload Data from TiDB Cloud Lake

Databend's `COPY INTO` command exports data to various file formats and storage locations with flexible formatting options.

## Supported File Formats

| Format | Example Syntax | Primary Use Case |
|--------|---------------|------------------|
| [**Unload Parquet File**](/tidb-cloud-lake/guides/unload-parquet-file.md) | `FILE_FORMAT = (TYPE = PARQUET)` | Analytics workloads, efficient storage |
| [**Unload CSV File**](/tidb-cloud-lake/guides/unload-csv-file.md) | `FILE_FORMAT = (TYPE = CSV)` | Data exchange, universal compatibility |
| [**Unload TSV File**](/tidb-cloud-lake/guides/unload-tsv-file.md) | `FILE_FORMAT = (TYPE = TSV)` | Tabular data with comma values |
| [**Unload NDJSON File**](/tidb-cloud-lake/guides/unload-ndjson-file.md) | `FILE_FORMAT = (TYPE = NDJSON)` | Semi-structured data, flexible schemas |

## Storage Destinations

| Destination | Example | When to Use |
|-------------|---------|-------------|
| **Named Stage** | `COPY INTO my_stage FROM my_table` | For repeated exports to the same location |
| **S3-Compatible Storage** | `COPY INTO 's3://bucket/path/' FROM my_table` | Cloud object storage with Amazon S3 |
