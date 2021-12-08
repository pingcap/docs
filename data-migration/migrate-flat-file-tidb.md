---
title: Migrate Data from CSV Files to TiDB
summary: Learn how to migrate data from CSV files to TiDB.
---

# Migrate Data from CSV Files to TiDB

TiDB Lightning supports importing data from CSV files and other delimiter formats, such as tab-separated values (TSV). Other flat file formats are also supported.

This document describes how to migrate data from CSV files to TiDB.

## Prerequisites

- [Install TiDB Lightning using TiUP](/migration-tools.md).
- [Get the target database privileges required for TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database).

## Step 1. Prepare the CSV files

Put all the CSV files in the same directory. If you need TiDB Lightning to recognize all CSV files, the file name should satisfy the following requirements:

- If a CSV file contains the data for an entire table, name the file `${db_name}.${table_name}.csv`.
- If the data of one table is separated into multiple CSV files, append a numeric suffix to these CSV files. For example, `${db_name}.${table_name}.003.csv`. The numeric suffixes may not be consecutive, but must be in ascending order. You might need to add extra zeros before the number to ensure all the suffixes are in the same length.

## Step 2. Create the target table schema

Because CSV files do not contain schema information, before importing data into TiDB, you need to create the target table schema. You can create the target table schema by either of the two methods:

* **Method 1**: create the target table schema using TiDB Lightning.

    1. Write SQL files that contain the required DDL statements.

        - Put `CREATE DATABASE` statements in the `${db_name}-schema-create.sql` files.
        - Put `CREATE TABLE` statements in the `${db_name}.${table_name}-schema.sql` files.

    2. During the migration, add the following configuration in `tidb-lightning.toml`:

        ```toml
        [mydumper]
        no-schema = false # To create database and table using Lightning, set the value to false
        ```

* **Method 2**: create the target table schema manually.

    During the migration, add the following configuration in `tidb-lightning.toml`:

    ```toml
    [mydumper]
    no-schema = true # If you have already created the target table schema, set the value to true, which means skipping the schema creation.
    ```

## Step 3. Create the configuration file

Create a `tidb-lightning.toml` file with the following content:

{{< copyable "shell-regular" >}}

```toml
[lightning]
# log.
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# "local": Default. The local backend is used to import large volumes of data (1 TB or above). During the import, the target TiDB cluster cannot provide any service.
# "tidb": The "tidb" backend is used to import small volumes of data (below 1 TB). During the import, the target TiDB cluster can provide service normally.
backend = "local"
# Set the temporary storage directory for the sorted KV files. The directory must be empty, and the storage space must be enough to hold the largest single table from the data source.
sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

[mydumper]
# Directory of the data source.
data-source-dir = "/data/my_datasource/"

# Configure whether to create the target database and table.
# If you need TiDB Lightning to create the target database and table, set the value to false.
# If you have already created the target database and table, set the value to true.
no-schema = true

# Define CSV format.
[mydumper.csv]
# Field separator of the CSV file. Must be ASCII character. Simple delimiters like "," is not recommended. It is recommended to use an uncommon character combination like "|+|".
separator = ','
# Delimiter. Can be ASCII character or empty.
delimiter = '"'
# Whether the CSV file has a table header.
# If set to true, the first line of the CSV file is treated as the header and skipped.
header = true
# Whether the CSV file contains NULL.
# If this item is set to true, any column of the CSV file cannot be parsed as NULL.
not-null = false
# If `not-null` is set to false (CSV contains NULL),
# The following value is parsed as NULL.
null = '\N'
# Whether to parse the backslash as an escape character.
backslash-escape = true
# Whether to trim the line that ends with a separator.
trim-last-separator = false

# The target cluster.
host = "${ip}"
port = ${port}
user = "${user_name}"
password = "${password}"
# The table schema is obtained from the TiDB status port.
status-port = ${port} # e.g.: 10080
# Address of the PD cluster
pd-addr = "${ip}:${port}" # e.g.: 172.16.31.3:2379. When backend = "local", you must specify status-port and pd-addr. Otherwise, the import will be abnormal.
```

## Step 4. Speed up the import (optional)

When you import data from CSV files with a uniform size of about 256 MiB, TiDB Lightning works in the best performance. However, if you import data from a single large CSV file, TiDB Lightning can only use one thread to process the import by default, which might slow down the import speed.

To speed up the import, you can split a large CSV file into smaller ones. For CSV files in common formats, it is hard to quickly locate the beginning and ending positions of each line; therefore, by default, TiDB Lightning does not automatically split CSV files. But if your CSV files to be imported meet certain format requirements, you can enable the `strict-format` mode. In this mode, TiDB Lightning automatically splits CSV files into multiple files, each in about 256 MiB, and processes them in parallel.

> **Note:**
>
> If the CSV file is not in strict format but the `strict-format` mode is set to `true` by mistake, a field that spans multiple lines will be split into two fields. This causes the parsing to fail, and TiDB Lightning might import the corrupted data without reporting an error.

In a strict format CSV file, each field only takes up one line. It must meets the following requirements:

- The delimiter is empty.
- Each field does not contain CR (\r) or LF (\n).

If your CSV file meets the above requirements, you can speed up the import by enabling the `strict-format` mode as follows:

```toml
[mydumper]
strict-format = true
```

## Step 5. Import the data

To start the import, run `tidb-lightning`. If you launch the program in command line, the program might exit because of `SIGHUP` signal. In this case, it is recommended to run the program with a `nohup` or `screen` tool. For example:

{{< copyable "shell-regular" >}}

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

After TiDB Lightning completes the import, it exits automatically. If the import is successful, the last line of `tidb-lightning.log` prints `tidb lightning exit`.

If the import fails, refer to [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md) for troubleshooting.

## Other file formats

If your data source is in other formats, you must end the file name with `.csv` and make corresponding changes in the `[mydumper.csv]` section of the `tidb-lightning.toml` configuration file. Here are some examples for common formats:

**TSV**

```toml
# Format example
# ID    Region    Count
# 1     East      32
# 2     South     NULL
# 3     West      10
# 4     North     39

# Format configuration
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
trim-last-separator = false
```

**TPC-H DBGEN**

```toml
# Format example
# 1|East|32|
# 2|South|0|
# 3|West|10|
# 4|North|39|

# Format configuration
[mydumper.csv]
separator = '|'
delimiter = ''
header = false
not-null = true
backslash-escape = false
trim-last-separator = true
```

## What's next

- [`mydumper.csv` field definitions](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)
