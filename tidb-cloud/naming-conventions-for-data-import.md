---
title: Naming Conventions for Data Import
summary: Learn about the naming conventions of CSV, Parquet, Aurora Snapshot, and SQL files.
---

# Naming Conventions for Data Import

The Data Import feature in TiDB Cloud supports the following file formats: CSV, Parquet, Aurora Snapshot, and SQL. To make sure that data can be imported successfully, note the following:

- Prepare the SQL file for creating the target database (optional) and the SQL file for creating the target table that conform to the naming conventions. If the SQL file for creating the target table is not provided, you need to create the corresponding table manually in the target database in advance.
- Prepare a data file that conforms to the naming conventions for importing data. If the data file name cannot meet the requirements, it is recommended to use the file pattern to perform the import task. Otherwise, the import task can not scan the data files you need to import.

## Naming conventions for data files and schema files

This section describes the naming conventions for data files and schema files.

### CSV

When you import CSV files, name the schema files and data files as follows:

- DB schema file (optional): `${db_name}-schema-create.sql`
- Table schema file: `${db_name}.${table_name}-schema.sql`
- Data file: `${db_name}.${table_name}[.XXXXXX].csv` ([.XXXXXX] is optional)

For example, `import_db.test_table.csv`, `import_db.test_table.01.csv`

### Parquet

When you import Parquet files, name the schema files and data files as follows:

- DB schema file (optional): `${db_name}-schema-create.sql`
- Table schema file: `${db_name}.${table_name}-schema.sql`
- Data file: `${db_name}.${table_name}[.XXXXXX][.{snappy|gz|lzo}].parquet` (`[.XXXXXXX]` and `[.{snappy|gz|lzo}]` are optional )

For example, `import_db.test_table.parquet`, `import_db.test_table.01.parquet`, 
 `import_db.test_table.gz.parquet`, `import_db.test_table.01.gz.parquet`

### Aurora Snapshot

When you import Aurora Snapshot files, name the schema files and data files as follows:

- DB schema file (optional): `${db_name}-schema-create.sql`
- Table schema file: `${db_name}.${table_name}-schema.sql`
- Data file: All files with the `.parquet` suffix in the `${db_name}.${table_name}/` folder.

### SQL

When you import SQL files, name the schema files and data files as follows:

- DB schema file (optional): `${db_name}-schema-create.sql`
- Table schema file: `${db_name}.${table_name}-schema.sql`
- Data file: `${db_name}.${table_name}[.XXXXXXX].sql` ([.XXXXXXX] is optional)

For example, `import_db.test_table.sql`, `import_db.test_table.01.sql`

If the SQL file is exported through TiDB Dumpling with the default configuration, it conforms to the naming convention by default.

## File pattern

If the source file of CSV or Parquet does not conform to the naming convention, you can use File pattern to establish the mapping relationship between the source file and the target table, so as to realize the data import. This feature does not support Aurora Snapshot and SQL File.

- For CSV files, see **File Pattern** in [Step 4. Import CSV files to TiDB Cloud](/tidbcloud/import-csv-files.md#step-4-import-csv-files-to-tidb-cloud)
- For Parquet files, see **File Pattern** in [Step 4. Import Parquet files to TiDB Cloud](/tidbcloud/import-parquet-files.md#step-4-import-parquet-files-to-tidb-cloud)
