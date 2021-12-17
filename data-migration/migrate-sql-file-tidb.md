---
title: Migrate Data from SQL Files to TiDB
summary: Learn how to migrate data from SQL Files to TiDB.
---

# Migrate Data from SQL Files to TiDB

This document describes how to migrate data from MySQL SQL files to TiDB using TiDB Lightning. For how to generate MySQL SQL files, refer to [Export to SQL Files](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-to-sql-files).

## Prerequisites

- [Install TiDB Lightning using TiUP](/migration-tools.md)
- [Get the target database privileges required for TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database)

## Step 1. Prepare SQL files

Put all the SQL files in the same directory, like `/data/my_datasource/`. TiDB Lighting recursively searches for all `.sql` files in this directory and its subdirectories.

## Step 2. Define the target table schema

Because CSV files do not contain schema information, before importing data into TiDB, you need to create the target table schema. You can create the target table schema by either of the following two methods:

* **Method 1**: create the target table schema using TiDB Lightning.

    1. Write SQL files that contain the required DDL statements.

        - The format of file name is `${db_name}-schema-create.sql`, and this file should have `CREATE DATABASE` statements.
        - The format of file name is `${db_name}.${table_name}-schema.sql`, and this file should have `CREATE TABLE` statements.

    2. During the migration, add the following configuration in `tidb-lightning.toml`:

        ```toml
        [mydumper]
        no-schema = false # To create the target table schema using Lightning, set the value to false
        ```

* **Method 2**: create the target table schema manually.

    During the migration, add the following configuration in `tidb-lightning.toml`:

    ```toml
    [mydumper]
    no-schema = true # If you have already created the target table schema, set the value to true, which means skipping the schema creation.
    ```

## Step 3: Create the configuration file

Create a `tidb-lightning.toml` file with the following content:

{{< copyable "" >}}

```toml
[lightning]
# Log
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# "local"：Default. The local backend is used to import large volumes of data (1 TiB or above). During the import, the target TiDB cluster cannot provide any service.
# "tidb"：The "tidb" backend can also be used to import small volumes of data (below 1 TiB). During the import, the target TiDB cluster can provide service normally. For the information about backend mode, refer to [TiDB Lightning Backends](https://docs.pingcap.com/tidb/stable/tidb-lightning-backends)
backend = "local"
# Set the temporary storage directory for the sorted Key value files. The directory must be empty, and the storage space must be enough to hold the largest single table from the data source. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage and exclusive I/O for the directory.
sorted-kv-dir = "${sorted-kv-dir}"

[mydumper]
# Directory of the data source, supports local path (like `/data/my_datasource/`) or S3 path (like `s3://bucket-name/data-path`).
data-source-dir = "${my_datasource}"

# Do not create a table schema. If you have manually created the target table schema in #Step 2, set it to true; otherwise, it is false.
no-schema = true

# The information of target cluster.
host = "${ip}"
port = 4000
user = "${user_name}"
password = "${password}"
# The table schema is obtained from the TiDB "status port".
status-port = ${port}       # For example, 10080
# Address of the PD cluster
pd-addr = "${ip}:${port}"   # For example: 172.16.31.3:2379. When backend = "local", you must specify status-port and pd-addr. Otherwise, the import will be abnormal.
```

For more information on the configuration file, refer to [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

## Step 4: Import the data

To start the import, run `tidb-lightning`. If you launch the program in the command line, the program might exit because of the `SIGHUP` signal. In this case, it is recommended to run the program with a `nohup` or `screen` tool. For example:

{{< copyable "shell-regular" >}}

```shell
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

If the import fails, refer to [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md) for troubleshooting.