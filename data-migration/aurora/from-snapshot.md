---
title: Migrate from Amazon Aurora MySQL Using TiDB Lightning
summary: Learn how to migrate full data from Amazon Aurora MySQL to TiDB using TiDB Lightning.
---

# Migrate from Aurora snapshot to TiDB

This document introduces how to migrate full data from Amazon Aurora MySQL to TiDB using TiDB Lightning. Both Dumpling and TiDB Lighting are used in this document.

Prerequisites

- [Deploy TiDB Lighting using TiUP](/data-migration/quick_install_tools.md)
- [Deploy Dumping using TiUP](/data-migration/quick_install_tools.md)

***

## Step 1. Export snapshots of Aurora to S3

Amazon's official documentation details how to generate a Snapshot to S3: [https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html)

## Step 2. Use Dumpling to export table schema files

Because the snapshot data exported from Aurora to S3 does not contain the SQL statement file used to create database tables, you need to manually export and import the table creation statements corresponding to the database tables into TiDB. You can use Dumpling and TiDB Lightning to create all table schemas:

{{< copyable "shell-regular" >}}

```shell
tiup dumpling --host ${host} --port 3306 --user root --password password --no-data --output ./schema --filter "mydb.*"
```

|Parameter|Description|
|-|-|
| `-h` or `--host`             |The IP address of the connected database|
| `-p` or `--password`         |The password of the connected database|
| `-u` or `--user`             |The username of the connected database|
| `-P` or `--port`             |The port of the connected database|
| `-d` or `--no-data`          |Do not export data (suitable for scenarios where only the schema is exported)  |
| `-o` or `--output`           |The path of exported local files or [the URL of the external storage](/br/backup-and-restore-storages.md)|
| `-f` or `--filter`           |Export tables that match the filter pattern. For the filter syntax, see [table-filter](/table-filter.md)|

> **Note:**
>
> For more parameters of Dumpling, see [Dumpling overview](/dumpling-overview.md).

## Step 3. Prepare the TiDB Lightning configuration file 

Based on different deployment methods, create the `tidb-lighting.toml` configuration file as follows:

{{< copyable "shell-regular" >}}

```shell
vim tidb-lighting.toml
```

{{< copyable "" >}}

```ini
[tidb]
# The target cluster information. Fill in one address of tidb-server.
host = "${host}"
port = ${port}
user = "${user_name}"
password = "${password}" 
# The default PD address of the cluster.
pd-addr = "127.0.0.1:2379"

[tikv-importer]
# Uses Local-backend for best performance. You can also choose TiDB-backend or Importer-backend according to your need. For detailed introduction of the three backend modes, see [TiDB Lightning Backends](/tidb-lightning/tidb-lightning-backends.md).
backend = "local"
# The storage path of local temporary files. Ensure that the corresponding directory does not exist or is empty and that the disk capacity is large enough for storage.
sorted-kv-dir = "${path}"

[mydumper]
# Data source directory
data-source-dir = "${s3_path}"  # eg: s3://bucket-name/data-path

# We will create the schema in [step 4](#create-table-schema), so here we set no-schema to true
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
> - If TLS is enabled in the target TiDB cluster, you also need to configure TLS.
> - For more configurations, see [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

## Step 4. Create table schemas in TiDB

Use TiDB Lightning to create table schemas:

{{< copyable "shell-regular" >}}

```shell
tiup tidb-lightning -config tidb-lightning.toml -d ./schema -no-schema=false
```

In this example, TiDB Lightning is only used to create table schemas, so the above command runs very fast. In average, ten table creation statements can be executed in one second.

> **Note:**
>
> If the number of database tables to create is relatively small, you can manually create the corresponding databases and tables in TiDB directly, or use other tools such as mysqldump to export the schema and then import it into TiDB.

## Step 5. Import data to TiDB

Run TiDB Lightning to start the import operation. 

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

When the import operation is started, view the progress by the following two ways:

- `grep` the keyword `progress` in logs, which is updated every 5 minutes by default.
- [Monitor TiDB Lightning](/tidb-lightning/monitor-tidb-lightning.md)

***

## Helpful Topics

- [Incrementally synchronize data From Aurora MySQL to TiDB](/data-migration/aurora/increment-aurora.md)
- [Lighting Administration Guide](/tidb-lightning/tidb-lightning-overview.md)
