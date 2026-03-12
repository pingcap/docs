---
title: Unload Data from Databend
slug: /unload-data
---

Databend's `COPY INTO` command exports data to various file formats and storage locations with flexible formatting options.

## Supported File Formats


| Format | Example Syntax | Primary Use Case |
|--------|---------------|------------------|
| [**Unload Parquet File**](/guides/unload-data/unload-parquet) | `FILE_FORMAT = (TYPE = PARQUET)` | Analytics workloads, efficient storage |
| [**Unload CSV File**](/guides/unload-data/unload-csv) | `FILE_FORMAT = (TYPE = CSV)` | Data exchange, universal compatibility |
| [**Unload TSV File**](/guides/unload-data/unload-tsv) | `FILE_FORMAT = (TYPE = TSV)` | Tabular data with comma values |
| [**Unload NDJSON File**](/guides/unload-data/unload-ndjson) | `FILE_FORMAT = (TYPE = NDJSON)` | Semi-structured data, flexible schemas |

## Storage Destinations


| Destination | Example | When to Use |
|-------------|---------|-------------|
| **Named Stage** | `COPY INTO my_stage FROM my_table` | For repeated exports to the same location |
| **S3-Compatible Storage** | `COPY INTO 's3://bucket/path/' FROM my_table` | Cloud object storage with Amazon S3 |

