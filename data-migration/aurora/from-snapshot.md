---
title: Migrate from Aurora snapshot to TiDB
summary: Learn how to migrate full data from Amazon Aurora MySQL to TiDB using TiDB Lightning.
---

# Migrate from Aurora snapshot to TiDB

This document describes how to migrate full data from Amazon Aurora MySQL to TiDB using TiDB Lightning. Both Dumpling and TiDB Lighting are used for this migration.

## Prerequisites

- [Deploy Lightning using TiUP](/quick-install-tools.md)
- [Deploy Dumping using TiUP](/quick-install-tools.md)

***

## Step 1. Export snapshot data of Aurora to Amazon S3

To export a snapshot to Amazon S3, refer to Amazon's official document [Exporting DB snapshot data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html).

## Step 2. Export table schema files using Dumpling 

Because the snapshot data exported to Amazon S3 does not contain the SQL statement file for creating database tables, you need to manually export and import the table creation statements into TiDB. You can use Dumpling and TiDB Lightning to create all table schemas:

{{< copyable "shell-regular" >}}

```shell
tiup dumpling --host ${host} --port 3306 --user root --password password --no-data --output ./schema --filter "mydb.*"
```

The parameters used in this step is as follows. For more parameters of Dumpling, refer to [Dumpling overview](/dumpling-overview.md).

| Parameter | Description |
| :--------| :------------|
| `-h` or `--host`             | The IP address of the connected database |
| `-p` or `--password`         | The password of the connected database |
| `-u` or `--user`             | The username of the connected database |
| `-P` or `--port`             | The port of the connected database |
| `-d` or `--no-data`          | Do not export data (suitable for scenarios where only the schema is exported) |
| `-o` or `--output`           | The path of exported local files or [the URL of the external storage](/br/backup-and-restore-storages.md) |
| `-f` or `--filter`           | Export tables that match the filter pattern. For the filter syntax, refer to [table-filter](/table-filter.md) |

## Step 3. Create the TiDB Lightning configuration file 

Create the `tidb-lighting.toml` configuration file as follows:

{{< copyable "shell-regular" >}}

```shell
vim tidb-lighting.toml
```

{{< copyable "" >}}

```toml
[tidb]

# The target cluster information. Fill in one address of tidb-server.
host = "${host}" # the target database address, for example: 172.16.128.1
port = ${port}   # the target database port, for example: 4000
user = "${user_name}"  # the target database username, for example: root
password = "${password}"  # the target database password
pd-addr = "${pd_address}"  # The default PD address of the cluster, for example: 127.0.0.1:2379

[tikv-importer]

# The "Local" backend mode is used by default for the best performance, which is suitable for large data volumes larger than 1 TiB. But in this mode, the downstream TiDB cannot provide services during the import process.
# The data volume less than 1 TiB can also adopt the "tidb" backend mode, and downstream TiDB can provide services normally. For more information about the backend mode, refer to [TiDB Lightning](/tidb-lightning/tidb-lightning-backends.md).
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

If you want to configure TLS in the target TiDB cluster, or know about more configurations, refer to the [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

## Step 4. Create table schemas in TiDB

Create table schemas using TiDB Lightning:

{{< copyable "shell-regular" >}}

```shell
tiup tidb-lightning -config tidb-lightning.toml -d ./schema -no-schema=false
```

In this example, TiDB Lightning is only used to create table schemas, so the above command runs very fast. In average, It only takes one second to execute ten table creation statements.

| Parameter | Description |
| :--------| :------------|
| `-config`                     | Reads global configuration from file. If not specified, the default value is used. |
| `-d`                          | Directory or [external storage URL](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages) of the data dump to read from |
| `-no-schema`                  | Ignore schema files, and get schema directly from TiDB |

For more parameters, refer to [TiDB Lightning Configuration](https://docs.pingcap.com/tidb/stable/tidb-lightning-configuration).

> **Note:**
>
> If the number of database tables to create is relatively small, you can directly and manually create the corresponding databases and tables in TiDB. Or you can use other tools such as mysqldump to export the schemas and then import them into TiDB.

## Step 5. Import data into TiDB using TiDB Lightning

Execute the following commands to start to import using TiDB Lightning:

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

## Helpful topics

- [Incrementally synchronize data From Aurora MySQL to TiDB](/data-migration/aurora/increment-aurora.md)
- [Lightning Administration Guide](/tidb-lightning/tidb-lightning-overview.md)
