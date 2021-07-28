---
title: Migrate from Amazon Aurora MySQL Using TiDB Lightning
summary: Learn how to migrate full data from Amazon Aurora MySQL to TiDB using TiDB Lightning.
---

# Migrate from Aurora snapshot to TiDB

This document introduces how to migrate full data from Amazon Aurora MySQL to TiDB using TiDB Lightning.

TiDB Lightning is a tool used for fast full import of large amounts of data into a TiDB cluster.

Currently, TiDB Lightning can mainly be used in the following two scenarios:

- Importing large amounts of new data quickly
- Restore all backup data

Currently, TiDB Lightning supports:

- The data source of the Dumpling, CSV or Amazon Aurora Parquet exported formats.
- Reading data from a local disk or from the Amazon S3 storage. For details, see [External Storages](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages).

## Before starting the migration, complete the following tasks

Because the snapshot data exported from Aurora to S3 does not contain the SQL statement file used to create database tables, you need to manually export and import the table creation statements corresponding to the database tables into TiDB. You can use Dumpling and TiDB Lightning to create all table schemas:

- [Export snapshots of Aurora to S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html)
- [Export table schema using dumpling]()
- [Deploy Lighting using TiUP]()
- [Deploy Dumping using TiUP]()

***

## Step 1: Use Dumpling to export table schema files

    ```
    tiup dumpling --host 127.0.0.1 --port 4000 --user root --password password --no-data --output ./schema --filter "mydb.*"
    ```

    > **Note:**
    >
    > - Set the parameters of the data source address and the path of output files according to your actual situation.
    > - If you need to export all database tables, you do not need to set the `--filter` parameter. If you only need to export some of the database tables, configure `--filter` according to [table-filter](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md).

## Step 2: Configure the data source of TiDB Lightning

Based on different deployment methods, edit the `tidb-lighting.toml` configuration file as follows:

1. Configure `data-source-dir` under `[mydumper]` as the S3 Bucket path of exported data.

    ```
    [mydumper]
    # Data source directory
    data-source-dir = "s3://bucket-name/data-path"
    ```

2. Configure the target TiDB cluster as follows:

    ```
    [tidb]
    # The target cluster information. Fill in one address of tidb-server.
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # The PD address of the cluster.
    pd-addr = "127.0.0.1:2379"
    ```

3. Configure the backend mode:

    ```
    [tikv-importer]
    # Uses Local-backend.
    backend = "local"
    # The storage path of local temporary files. Ensure that the corresponding directory does not exist or is empty and that the disk capacity is large enough for storage.
    sorted-kv-dir = "/path/to/local-temp-dir"
    ```

4. Configure the file routing.

    ```
    [mydumper]
    no-schema = true

    [[mydumper.files]]
    # Uses single quoted strings to avoid escaping.
    pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
    schema = '$1'
    table = '$2'
    type = '$3'
    ```

> **Note:**
>
> - The above example uses the Local-backend for best performance. You can also choose TiDB-backend or Importer-backend according to your need. For detailed introduction of the three backend modes, see [TiDB Lightning Backends](/tidb-lightning/tidb-lightning-backends.md).
> - Because the path for exporting snapshot data from Aurora is different from the default file naming format supported by TiDB Lightning, you need to set additional file routing configuration.
> - If TLS is enabled in the target TiDB cluster, you also need to configure TLS.

For other configurations, see [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

## Step 3: Create table schema

Use TiDB Lightning to create table schemas:

    ```
    tiup tidb-lightning -config tidb-lightning.toml -d ./schema -no-schema=false
    ```

    In this example, TiDB Lightning is only used to create table schemas, so you need to execute the above command quickly. At a regular speed, ten table creation statements can be executed in one second.

> **Note:**
>
> If the number of database tables to create is relatively small, you can manually create the corresponding databases and tables in TiDB directly, or use other tools such as mysqldump to export the schema and then import it into TiDB.

## Step 4: Run TiDB Lightning to import data

Run TiDB Lightning to start the import operation. 

```bash
# !/bin/bash
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

When the import operation is started, view the progress by the following two ways:

- `grep` the keyword `progress` in logs, which is updated every 5 minutes by default.
- [Monitor TiDB Lightning](/tidb-lightning/monitor-tidb-lightning.md)

***

## Helpful Topics

- [Incrementally synchronize data From Aurora MySQL to TiDB]()



- [Lighting Administration Guide](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)
