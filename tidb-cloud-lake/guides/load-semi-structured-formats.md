---
title: Loading Semi-structured Formats
---

## What is Semi-structured Data?

Semi-structured data contains tags or markers to separate semantic elements while not conforming to rigid database structures. Databend efficiently loads these formats using the `COPY INTO` command, with optional on-the-fly data transformation.

## Supported File Formats

| File Format | Description | Guide |
| ----------- | ----------- | ----- |
| **Parquet** | Efficient columnar storage format | [Loading Parquet](load-semistructured/load-parquet) |
| **CSV** | Comma-separated values | [Loading CSV](load-semistructured/load-csv) |
| **TSV** | Tab-separated values | [Loading TSV](load-semistructured/load-tsv) |
| **NDJSON** | Newline-delimited JSON | [Loading NDJSON](load-semistructured/load-ndjson) |
| **ORC** | Optimized Row Columnar format | [Loading ORC](load-semistructured/load-orc) |
| **Avro** | Row-based format with schema definition | [Loading Avro](load-semistructured/load-avro) |
