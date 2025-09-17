---
title: Import Snapshot Files into TiDB Cloud Dedicated
summary: Learn how to import Amazon Aurora or RDS for MySQL snapshot files into TiDB Cloud Dedicated.
---

# Import Snapshot Files into TiDB Cloud Dedicated

You can import snapshot files from Amazon Aurora or RDS for MySQL into TiDB Cloud Dedicated. These snapshots are exported as Parquet files. To ensure a successful import, your data files must follow specific naming conventions. For example, each source data file must have a `.parquet` suffix and be located in a folder named `{db_name}.{table_name}/`. For complete details, see [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md).

The import process for snapshot files is the same as for other Parquet files. For step-by-step instructions, see [Import Apache Parquet Files from Cloud Storage into TiDB Cloud Dedicated](/tidb-cloud/import-parquet-files.md).
