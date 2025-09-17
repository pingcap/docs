---
title: Import Snapshot Files into {{{ .starter }}} or Essential
summary: Learn how to import Amazon Aurora or RDS for MySQL snapshot files into {{{ .starter }}} or Essential.
---

# Import Snapshot Files into {{{ .starter }}} or Essential

You can import snapshot files from Amazon Aurora or RDS for MySQL into {{{ .starter }}} or Essential. These snapshots are exported as Parquet files. To ensure a successful import, your data files must follow specific naming conventions. For example, all source data files must have a `.parquet` suffix and be located in a folder named `{db_name}.{table_name}/`. For complete details, see [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md).

The import process for snapshot files is the same as for other Parquet files. For step-by-step instructions, see [Import Apache Parquet Files from Cloud Storage into {{{ .starter }}} or Essential](/tidb-cloud/import-parquet-files-serverless.md).
