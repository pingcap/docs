---
title: TiDB Lightning Data Source
summary: Learn all the data sources supported by TiDB Lightning.
aliases: ['/docs/dev/tidb-lightning/migrate-from-csv-using-tidb-lightning/','/docs/dev/reference/tools/tidb-lightning/csv/','/tidb/dev/migrate-from-csv-using-tidb-lightning/']
---

# TiDB Lightning Data Source

TiDB Lightning supports importing data from multiple data sources to TiDB clusters. To specify the data source for TiDB Lightning, use the following configuration:

```toml
[mydumper]
# Local source data directory or the URL of the external storage such as S3.
data-source-dir = "/data/my_database"
```

When TiDB Lightning is running, it looks for all files that match the pattern of `data-source-dir`.

| File | Type | Pattern |
| --------- | -------- | ------- |
| Schema file | Contains the `CREATE TABLE` DDL statement | `${db_name}.${table_name}-schema.sql` |
| Schema file | Contains the `CREATE DATABASE` DDL statement| `${db_name}-schema-create.sql` |
| Data file | If the data file contains data for a whole table, the file is imported into a table named `${db_name}.${table_name}` | <code>\${db_name}.\${table_name}.\${csv\|sql\|parquet}</code> |
| Data file | If the data for a table is split in multiple data files, each data file must have a number in its filename as suffix | <code>\${db_name}.\${table_name}.001.\${csv\|sql\|parquet}</code> |

TiDB Lightning processes data in parallel as much as possible. Because