---
title: Loading Semi-structured Formats
summary: Semi-structured data contains tags or markers to separate semantic elements while not conforming to rigid database structures. Databend efficiently loads these formats using the COPY INTO command, with optional on-the-fly data transformation.
---
## What is Semi-structured Data?

Semi-structured data contains tags or markers to separate semantic elements while not conforming to rigid database structures. Databend efficiently loads these formats using the `COPY INTO` command, with optional on-the-fly data transformation.

## Supported File Formats

| File Format | Description | Guide |
| ----------- | ----------- | ----- |
| **Parquet** | Efficient columnar storage format | [Loading Parquet](/tidb-cloud-lake/guides/load-parquet.md) |
| **CSV** | Comma-separated values | [Loading CSV](/tidb-cloud-lake/guides/load-csv.md) |
| **TSV** | Tab-separated values | [Loading TSV](/tidb-cloud-lake/guides/load-tsv.md) |
| **NDJSON** | Newline-delimited JSON | [Loading NDJSON](/tidb-cloud-lake/guides/load-ndjson.md) |
| **ORC** | Optimized Row Columnar format | [Loading ORC](/tidb-cloud-lake/guides/load-orc.md) |
| **Avro** | Row-based format with schema definition | [Loading Avro](/tidb-cloud-lake/guides/load-avro.md) |
