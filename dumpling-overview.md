---
title: Dumpling Overview
summary: Use the Dumpling tool to export data from TiDB.
aliases: ['/docs/dev/mydumper-overview/','/docs/dev/reference/tools/mydumper/','/tidb/dev/mydumper-overview/']
---

# Dumpling Overview

This document introduces the data export tool - [Dumpling](https://github.com/pingcap/dumpling). Dumpling exports data stored in TiDB/MySQL as SQL or CSV data files and can be used to make a logical full backup or export.

For backups of SST files (key-value pairs) or backups of incremental data that are not sensitive to latency, refer to [BR](/br/backup-and-restore-tool.md). For real-time backups of incremental data, refer to [TiCDC](/ticdc/ticdc-overview.md).

> **Note:**
>
> PingCAP previously maintained a fork of the [mydumper project](https://github.com/maxbube/mydumper) with enhancements specific to TiDB. This fork has since been replaced by [Dumpling](/dumpling-overview.md), which has been rewritten in Go, and supports more optimizations that are specific to TiDB. It is strongly recommended that you use Dumpling instead of mydumper.
>
> For the overview of Mydumper, refer to [v4.0 Mydumper documentation](https://docs.pingcap.com/tidb/v4.0/backup-and-restore-using-mydumper-lightning).

## Improvements of Dumpling compared with Mydumper

1. Support exporting data in multiple formats, including SQL and CSV
2. Support the [table-filter](https://github.com/pingcap/tidb-tools/blob/master/pkg/table-filter/README.md) feature, which makes it easier to filter data
3. Support exporting data to Amazon S3 cloud storage.
4. More optimizations are made for TiDB:
    - Support configuring the memory limit of a single TiDB SQL statement
    - Support automatic adjustment of TiDB GC time for TiDB v4.0.0 and above
    - Use TiDB's hidden column `_tidb_rowid` to optimize the performance of concurrent data export from a single table
    - For TiDB, you can set the value of [`tidb_snapshot`](/read-historical-data.md#how-tidb-reads-data-from-history-versions) to specify the time point of the data backup. This ensures the consistency of the backup, instead of using `FLUSH TABLES WITH READ LOCK` to ensure the consistency.

## Dumpling introduction

Dumpling is written in Go. The Github project is [pingcap/dumpling](https://github.com/pingcap/dumpling).

For detailed usage of Dumpling, use the `--help` option or refer to [Option list of Dumpling](#option-list-of-dumpling).

When using Dumpling, you need to execute the export command on a running cluster. This document assumes that there is a TiDB instance on the `127.0.0.1:4000` host and that this TiDB instance has a root user without a password.

You can get Dumpling using [TiUP](/tiup/tiup-overview.md) by running `tiup install dumpling`. Afterwards, you can use `tiup dumpling ...` to run Dumpling.

Dumpling is also included in the tidb-toolkit installation package and can be [download here](/download-ecosystem-tools.md#dumpling).

## Export data from TiDB/MySQL

### Required privileges

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT
- PROCESS

### Export to SQL files

Dumpling exports data to SQL files by default. You can also export data to SQL files by adding the `--filetype sql` flag:

{{< copyable "shell-regular" >}}

```shell
dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  --filetype sql \
  -t 8 \
  -o /tmp/test \
  -r 200000 \
  -F 256MiB
```

In the command above:

+ The `-h`, `-p`, and `-u` option respectively mean the address, the port, and the user. If a password is required for authentication, you can use `-p $YOUR_SECRET_PASSWORD` to pass the password to Dumpling.
+ The `-o` option specifies the export directory of the storage, which supports a local file path or a [URL of an external storage](/br/backup-and-restore-storages.md).
+ The `-t` option specifies the number of threads for the export. Increasing the number of threads improves the concurrency of Dumpling and the export speed, and also increases the database's memory consumption. Therefore, it is not recommended to set the number too large. Usually, it's less than 64.
+ The `-r` option specifies the maximum number of rows in a single file. With this option specified, Dumpling enables the in-table concurrency to speed up the export and reduce the memory usage. When the upstream database is TiDB v3.0 or later versions, a value of this parameter greater than 0 indicates that the TiDB region information is used for splitting and the value specified here will no longer take effect.
+ The `-F` option is used to specify the maximum size of a single file (the unit here is `MiB`; inputs like `5GiB` or `8KB` are also acceptable). It is recommended to keep its value to 256 MiB or less if you plan to use TiDB Lightning to load this file into a TiDB instance.

> **Note:**
>
> If the size of a single exported table exceeds 10 GB, it is **strongly recommended to use** the `-r` and `-F` options.

### Export to CSV files

You can export data to CSV files by adding the `--filetype csv` argument.

When you export data to CSV files, you can use `--sql <SQL>` to filter the records with the SQL statements. For example, you can export all records that match `id < 100` in `test.sbtest1` using the following command:

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --filetype csv \
  --sql 'select * from `test`.`sbtest1` where id < 100' \
  -F 100MiB \
  --output-filename-template 'test.sbtest1.{{.Index}}'
```

In the command above:

- The `--sql` option can be used only for exporting to CSV files. The command above executes the `SELECT * FROM <table-name> WHERE id <100` statement on all tables to be exported. If a table does not have the specified field, the export fails.
- When you use the `--sql` option, Dumpling cannot obtain the exported table and schema information. You can specify the file name format of the CSV files using the `--output-filename-template` option, which facilitates the subsequent use of [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import the data file. For example, `--output-filename-template='test.sbtest1.{{.Index}}'` specifies that the exported CSV files are named as `test.sbtest1.000000000` or `test.sbtest1.000000001`.
- You can use options like `--csv-separator` and `--csv-delimiter` to configure the CSV file format. For details, refer to the [Dumpling option list](#option-list-of-dumpling).

> **Note:**
>
> *Strings* and *keywords* are not distinguished by Dumpling. If the imported data is the Boolean type, the value of `true` is converted to `1` and the value of `false` is converted to `0`.

### Format of exported files

- `metadata`: The start time of the exported files and the position of the master binary log.

    {{< copyable "shell-regular" >}}

    ```shell
    cat metadata
    ```

    ```shell
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

- `{schema}-schema-create.sql`: The SQL file used to create the schema

    {{< copyable "shell-regular" >}}

    ```shell
    cat test-schema-create.sql
    ```

    ```shell
    CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
    ```

- `{schema}.{table}-schema.sql`: The SQL file used to create the table

    {{< copyable "shell-regular" >}}

    ```shell
    cat test.t1-schema.sql
    ```

    ```shell
    CREATE TABLE `t1` (
      `id` int(11) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
    ```

- `{schema}.{table}.{0001}.{sql|csv`}: The date source file

    {{< copyable "shell-regular" >}}

    ```shell
    cat test.t1.0.sql
    ```

    ```shell
    /*!40101 SET NAMES binary*/;
    INSERT INTO `t1` VALUES
    (1);
    ```

- `*-schema-view.sql`、`*-schema-trigger.sql`、`*-schema-post.sql`: Other exported files

### Export data to Amazon S3 cloud storage

Since v4.0.8, Dumpling supports exporting data to cloud storages. If you need to back up data to Amazon's S3 backend storage, you need to specify the S3 storage path in the `-o` parameter.

You need to create an S3 bucket in the specified region (see the [Amazon documentation - How do I create an S3 Bucket](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)). If you also need to create a folder in the bucket, see the [Amazon documentation - Creating a folder](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html).

Pass `SecretKey` and `AccessKey` of the account with the permission to access the S3 backend storage to the Dumpling node as environment variables.

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

Dumpling also supports reading credential files from `~/.aws/credentials`. For more Dumpling configuration, see the configuration of [External storages](/br/backup-and-restore-storages.md).

When you back up data using Dumpling, explicitly specify the `--s3.region` parameter, which means the region of the S3 storage (for example, `ap-northeast-1`):

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -r 200000 \
  -o "s3://${Bucket}/${Folder}" \
  --s3.region "${region}"
```

### Filter the exported data

#### Use the `--where` option to filter data

By default, Dumpling exports all databases except system databases (including `mysql`, `sys`, `INFORMATION_SCHEMA`, `PERFORMANCE_SCHEMA`, `METRICS_SCHEMA`, and `INSPECTION_SCHEMA`). You can use `--where <SQL where expression>` to select the records to be exported.

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  --where "id < 100"
```

The above command exports the data that matches `id < 100` from each table. Note that you cannot use the `--where` parameter together with `--sql`.

#### Use the `--filter` option to filter data

Dumpling can filter specific databases or tables by specifying the table filter with the `--filter` option. The syntax of table filters is similar to that of `.gitignore`. For details, see [Table Filter](/table-filter.md).

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -h 127.0.0.1 \
  -o /tmp/test \
  -r 200000 \
  --filter "employees.*" \
  --filter "*.WorkOrder"
```

The above command exports all the tables in the `employees` database and the `WorkOrder` tables in all databases.

#### Use the `-B` or `-T` option to filter data

Dumpling can also export specific databases with the `-B` option or specific tables with the `-T` option.

> **Note:**
>
> - The `--filter` option and the `-T` option cannot be used at the same time.
> - The `-T` option can only accept a complete form of inputs like `database-name.table-name`, and inputs with only the table name are not accepted. Example: Dumpling cannot recognize `-T WorkOrder`.

Examples:

- `-B employees` exports the `employees` database.
- `-T employees.WorkOrder` exports the `employees.WorkOrder` table.

### Improve export efficiency through concurrency

The exported file is stored in the `./export-<current local time>` directory by default. Commonly used options are as follows:

- The `-t` option specifies the number of threads for the export. Increasing the number of threads improves the concurrency of Dumpling and the export speed, and also increases the database's memory consumption. Therefore, it is not recommended to set the number too large.
- The `-r` option specifies the maximum number of records (or the number of rows in the database) for a single file. When it is enabled, Dumpling enables concurrency in the table to improve the speed of exporting large tables. When the upstream database is TiDB v3.0 or later versions, a value of this parameter greater than 0 indicates that the TiDB region information is used for splitting and the value specified here will no longer take effect.
- The `--compress gzip` option can be used to compress the dump. This can help to speed up dumping of data if storage is the bottleneck or if storage capacity is a concern. The drawback of this is an increase in CPU usage. Each file is compressed individually.

With the above options specified, Dumpling can have a quicker speed of data export.

### Adjust Dumpling's data consistency options

> **Note:**
>
> In most scenarios, you do not need to adjust the default data consistency options of Dumpling (the default value is `auto`).

Dumpling uses the `--consistency <consistency level>` option to control the way in which data is exported for "consistency assurance". When using snapshot for consistency, you can use the `--snapshot` option to specify the timestamp to be backed up. You can also use the following levels of consistency:

- `flush`: Use [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock) to temporarily interrupt the DML and DDL operations of the replica database, to ensure the global consistency of the backup connection, and to record the binlog position (POS) information. The lock is released after all backup connections start transactions. It is recommended to perform full backups during off-peak hours or on the MySQL replica database.
- `snapshot`: Get a consistent snapshot of the specified timestamp and export it.
- `lock`: Add read locks on all tables to be exported.
- `none`: No guarantee for consistency.
- `auto`: Use `flush` for MySQL and `snapshot` for TiDB.

After everything is done, you can see the exported file in `/tmp/test`:

{{< copyable "shell-regular" >}}

```shell
ls -lh /tmp/test | awk '{print $5 "\t" $9}'
```

```
140B  metadata
66B   test-schema-create.sql
300B  test.sbtest1-schema.sql
190K  test.sbtest1.0.sql
300B  test.sbtest2-schema.sql
190K  test.sbtest2.0.sql
300B  test.sbtest3-schema.sql
190K  test.sbtest3.0.sql
```

### Export historical data snapshot of TiDB

Dumpling can export the data of a certain [tidb_snapshot](/read-historical-data.md#how-tidb-reads-data-from-history-versions) with the `--snapshot` option specified.

The `--snapshot` option can be set to a TSO (the `Position` field output by the `SHOW MASTER STATUS` command) or a valid time of the `datetime` data type (in the form of `YYYY-MM-DD hh:mm:ss`), for example:

{{< copyable "shell-regular" >}}

```shell
./dumpling --snapshot 417773951312461825
./dumpling --snapshot "2020-07-02 17:12:45"
```

The TiDB historical data snapshots when the TSO is `417773951312461825` and the time is `2020-07-02 17:12:45` are exported.

### Control the memory usage of exporting large tables

When Dumpling is exporting a large single table from TiDB, Out of Memory (OOM) might occur because the exported data size is too large, which causes connection abort and export failure. You can use the following parameters to reduce the memory usage of TiDB:

+ Setting `-r` to split the data to be exported into chunks. This reduces the memory overhead of TiDB's data scan and enables concurrent table data dump to improve export efficiency. When the upstream database is TiDB v3.0 or later versions, a value of this parameter greater than 0 indicates that the TiDB region information is used for splitting and the value specified here will no longer take effect.
+ Reduce the value of `--tidb-mem-quota-query` to `8589934592` (8 GB) or lower. `--tidb-mem-quota-query` controls the memory usage of a single query statement in TiDB.
+ Adjust the `--params "tidb_distsql_scan_concurrency=5"` parameter. [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) is a session variable which controls the concurrency of the scan operations in TiDB.

### TiDB GC settings when exporting a large volume of data

When exporting data from TiDB, if the TiDB version is later than or equal to v4.0.0 and Dumpling can access the PD address of the TiDB cluster, Dumpling automatically extends the GC time without affecting the original cluster.

In other scenarios, if the data size is very large, to avoid export failure due to GC during the export process, you can extend the GC time in advance:

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_gc_life_time = '720h';
```

After your operation is completed, set the GC time back (the default value is `10m`):

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

Finally, all the exported data can be imported back to TiDB using [TiDB Lightning](/tidb-lightning/tidb-lightning-backends.md).

## Option list of Dumpling

| Options                      | Usage                                                                                                                                                                                                                                                                                                                              | Default value                              |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `-V` or `--version`          | Output the Dumpling version and exit directly                                                                                                                                                                                                                                                                                      |
| `-B` or `--database`         | Export specified databases                                                                                                                                                                                                                                                                                                         |
| `-T` or `--tables-list`      | Export specified tables                                                                                                                                                                                                                                                                                                            |
| `-f` or `--filter`           | Export tables that match the filter pattern. For the filter syntax, see [table-filter](/table-filter.md).                                                                                                                                                                                                                          |    `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]` (export all databases or tables excluding system schemas) |
| `--case-sensitive`           | whether table-filter is case-sensitive                                                                                                                                                                                                                                                                                             | false (case-insensitive)                   |
| `-h` or `--host`             | The IP address of the connected database host                                                                                                                                                                                                                                                                                      | "127.0.0.1"                                |
| `-t` or `--threads`          | The number of concurrent backup threads                                                                                                                                                                                                                                                                                            | 4                                          |
| `-r` or `--rows`             | Split the table into rows with a specified number of rows (generally applicable for concurrent operations of splitting a large table into multiple files. When the upstream database is TiDB v3.0 or later versions, a value of this parameter greater than 0 indicates that the TiDB region information is used for splitting and the value specified here will no longer take effect.                                                                                                                                                                                 |
| `-L` or `--logfile`          | Log output address. If it is empty, the log will be output to the console                                                                                                                                                                                                                                                          | ""                                         |
| `--loglevel`                 | Log level {debug,info,warn,error,dpanic,panic,fatal}                                                                                                                                                                                                                                                                               | "info"                                     |
| `--logfmt`                   | Log output format {text,json}                                                                                                                                                                                                                                                                                                      | "text"                                     |
| `-d` or `--no-data`          | Do not export data (suitable for scenarios where only the schema is exported)                                                                                                                                                                                                                                                      |
| `--no-header`                | Export CSV files of the tables without generating header                                                                                                                                                                                                                                                                           |
| `-W` or `--no-views`         | Do not export the views                                                                                                                                                                                                                                                                                                            | true                                       |
| `-m` or `--no-schemas`       | Do not export the schema with only the data exported                                                                                                                                                                                                                                                                               |
| `-s` or `--statement-size`   | Control the size of the `INSERT` statements; the unit is bytes                                                                                                                                                                                                                                                                     |
| `-F` or `--filesize`         | The file size of the divided tables. The unit must be specified such as `128B`, `64KiB`, `32MiB`, and `1.5GiB`.                                                                                                                                                                                                                    |
| `--filetype`                 | Exported file type (csv/sql)                                                                                                                                                                                                                                                                                                       | "sql"                                      |
| `-o` or `--output`           | The path of exported local files or [the URL of the external storage](/br/backup-and-restore-storages.md)                                                                                                                                                                                                                                                                                                    | "./export-${time}"                         |
| `-S` or `--sql`              | Export data according to the specified SQL statement. This command does not support concurrent export.                                                                                                                                                                                                                             |
| `--consistency`              | flush: use FTWRL before the dump <br/> snapshot: dump the TiDB data of a specific snapshot of a TSO <br/> lock: execute `lock tables read` on all tables to be dumped <br/> none: dump without adding locks, which cannot guarantee consistency <br/> auto: use --consistency flush for MySQL; use --consistency snapshot for TiDB | "auto"                                     |
| `--snapshot`                 | Snapshot TSO; valid only when `consistency=snapshot`                                                                                                                                                                                                                                                                               |
| `--where`                    | Specify the scope of the table backup through the `where` condition                                                                                                                                                                                                                                                                |
| `-p` or `--password`         | The password of the connected database host                                                                                                                                                                                                                                                                                        |
| `-P` or `--port`             | The port of the connected database host                                                                                                                                                                                                                                                                                            | 4000                                       |
| `-u` or `--user`             | The username of the connected database host                                                                                                                                                                                                                                                                                        | "root"                                     |
| `--dump-empty-database`      | Export the `CREATE DATABASE` statements of the empty databases                                                                                                                                                                                                                                                                     | true                                       |
| `--ca`                       | The address of the certificate authority file for TLS connection                                                                                                                                                                                                                                                                   |
| `--cert`                     | The address of the client certificate file for TLS connection                                                                                                                                                                                                                                                                      |
| `--key`                      | The address of the client private key file for TLS connection                                                                                                                                                                                                                                                                      |
| `--csv-delimiter`            | Delimiter of character type variables in CSV files                                                                                                                                                                                                                                                                                 | '"'                                        |
| `--csv-separator`            | Separator of each value in CSV files. It is not recommended to use the default ‘,’. It is recommended to use ‘\|+\|’ or other uncommon character combinations| ','                                                                                                                                                                                                                                                                                               | ','                                        |
| `--csv-null-value`           | Representation of null values in CSV files                                                                                                                                                                                                                                                                                         | "\\N"                                      |
| `--escape-backslash`         | Use backslash (`\`) to escape special characters in the export file                                                                                                                                                                                                                                                                | true                                       |
| `--output-filename-template` | The filename templates represented in the format of [golang template](https://golang.org/pkg/text/template/#hdr-Arguments) <br/> Support the `{{.DB}}`, `{{.Table}}`, and `{{.Index}}` arguments <br/> The three arguments represent the database name, table name, and chunk ID of the data file                                  | '{{.DB}}.{{.Table}}.{{.Index}}'            |
| `--status-addr`              | Dumpling's service address, including the address for Prometheus to pull metrics and pprof debugging                                                                                                                                                                                                                               | ":8281"                                    |
| `--tidb-mem-quota-query`     | The memory limit of exporting SQL statements by a single line of Dumpling command, and the unit is byte. For v4.0.10 or later versions, if you do not set this parameter, TiDB uses the value of the `mem-quota-query` configuration item as the memory limit value by default. For versions earlier than v4.0.10, the parameter value defaults to 32 GB.  | 34359738368 |
| `--params`                   | Specifies the session variable for the connection of the database to be exported. The required format is `"character_set_client=latin1,character_set_connection=latin1"`                                                                                                                                                           |
