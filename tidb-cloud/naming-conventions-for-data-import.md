---
title: Naming Conventions for Data Import
summary: Learn about the naming conventions for CSV, Parquet, Aurora Snapshot, and SQL files during data import.
---

# Naming Conventions for Data Import

The Data Import feature in TiDB Cloud supports the following file formats: CSV, Parquet, Aurora Snapshot, and SQL. To make sure that data can be imported successfully, you need to prepare the following:

- Prepare the SQL file for creating the target database (optional) and the SQL file for creating the target table that conform to the naming conventions. If the SQL file for creating the target table is not provided, you need to create the corresponding table manually in the target database in advance.
- Prepare a data file that conforms to the naming conventions for importing data. If the data file name cannot meet the requirements, it is recommended to use the file pattern to perform the import task. Otherwise, the import task can not scan the data files you need to import.

## Naming conventions for schema files

This section describes the naming conventions for database and table schema files. The naming conventions for schema files are the same for all the following types of source files: CSV, Parquet, Aurora Snapshot, and SQL.

The naming conventions for schema files are as follows:

- Database schema file(optional): `${db_name}-schema-create.sql`
- Table schema file: `${db_name}.${table_name}-schema.sql`

For example:

- mytestdb-schema-create.sql
- mytestdb.testtable-schema.sql

## Naming conventions for data files

This section describes the naming conventions for data files. Depending on the type of source files, the naming conventions for data files are different.

### CSV

When you import CSV files, name the data files as follows:

- `${db_name}.${table_name}[.XXXXXX].csv` ([.XXXXXX] is optional)

For example:

- `import_db.test_table.csv`
- `import_db.test_table.01.csv`

### Parquet

When you import Parquet files, name the data files as follows:

- `${db_name}.${table_name}[.XXXXXX][.{snappy|gz|lzo}].parquet` (`[.XXXXXXX]` and `[.{snappy|gz|lzo}]` are optional)

For example:

- `import_db.test_table.parquet`
- `import_db.test_table.01.parquet`
- `import_db.test_table.gz.parquet`
- `import_db.test_table.01.gz.parquet`

### Aurora Snapshot

When you import Aurora Snapshot files, name the data files as follows:

- All files with the `.parquet` suffix in the `${db_name}.${table_name}/` folder.

A data file name can contain any prefix consisting of "a-z, 0-9, - , _ , ." and suffix ".parquet". For example:

- `dbname.tablename.01.parquet`

### SQL

When you import SQL files, name the data files as follows:

- `${db_name}.${table_name}[.XXXXXXX].sql` ([.XXXXXXX] is optional)

For example:

- `import_db.test_table.sql`
- `import_db.test_table.01.sql`

If the SQL file is exported through TiDB Dumpling with the default configuration, it conforms to the naming convention by default.

## File pattern

If the source file of CSV or Parquet does not conform to the naming convention, you can use File pattern to establish the name mapping relationship between the source data file and the target table, so as to perform the data import task. This feature does not support Aurora Snapshot and SQL File.

- For CSV files, see **File Pattern** in [Step 4. Import CSV files to TiDB Cloud](/tidbcloud/import-csv-files.md#step-4-import-csv-files-to-tidb-cloud)
- For Parquet files, see **File Pattern** in [Step 4. Import Parquet files to TiDB Cloud](/tidbcloud/import-parquet-files.md#step-4-import-parquet-files-to-tidb-cloud)
