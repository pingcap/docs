---
title: IMPORT INTO
summary: An overview of the usage of IMPORT INTO in TiDB.
---

# IMPORT INTO

The `IMPORT INTO` statement lets you import data to TiDB via the [Physical Import Mode](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode) of TiDB Lightning. You can use `IMPORT INTO` in the following two ways:

- `IMPORT INTO ... FROM FILE`: imports data files in formats such as `CSV`, `SQL`, and `PARQUET` into an empty table in TiDB.
- `IMPORT INTO ... FROM SELECT`: imports the query result of a `SELECT` statement into an empty table in TiDB. You can also use it to import historical data queried with [`AS OF TIMESTAMP`](/as-of-timestamp.md).

<CustomContent platform="tidb">

> **Note:**
>
> Compared with [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md), `IMPORT INTO` can be directly executed on TiDB nodes, supports automated distributed task scheduling and [TiDB Global Sort](/tidb-global-sort.md), and offers significant improvements in deployment, resource utilization, task configuration convenience, ease of invocation and integration, high availability, and scalability. It is recommended that you consider using `IMPORT INTO` instead of TiDB Lightning in appropriate scenarios.

</CustomContent>

## Restrictions

- `IMPORT INTO` only supports importing data into existing empty tables in the database.
- `IMPORT INTO` does not support importing data into an empty partition if other partitions of the same table already contain data. The target table must be completely empty for import operations.
- `IMPORT INTO` does not support importing data into a [temporary table](/temporary-tables.md) or a [cached table](/cached-tables.md).
- `IMPORT INTO` does not support transactions or rollback. Executing `IMPORT INTO` within an explicit transaction (`BEGIN`/`END`) will return an error.
- `IMPORT INTO` does not support working simultaneously with features such as [Backup & Restore](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview), [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md), [acceleration of adding indexes](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630), data import using TiDB Lightning, data replication using TiCDC, or [Point-in-Time Recovery (PITR)](https://docs.pingcap.com/tidb/stable/br-log-architecture). For more compatibility information, see [Compatibility of TiDB Lightning and `IMPORT INTO` with TiCDC and Log Backup](https://docs.pingcap.com/tidb/stable/tidb-lightning-compatibility-and-scenarios).
- During the data import process, do not perform DDL or DML operations on the target table, and do not execute [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) for the target database. These operations can lead to import failures or data inconsistencies. In addition, it is **NOT** recommended to perform read operations during the import process, as the data being read might be inconsistent. Perform read and write operations only after the import is completed.
- The import process consumes system resources significantly. For TiDB Self-Managed, to get better performance, it is recommended to use TiDB nodes with at least 32 cores and 64 GiB of memory. TiDB writes sorted data to the TiDB [temporary directory](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) during import, so it is recommended to configure high-performance storage media for TiDB Self-Managed, such as flash memory. For more information, see [Physical Import Mode limitations](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode#requirements-and-restrictions).
- For TiDB Self-Managed, the TiDB [temporary directory](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) is expected to have at least 90 GiB of available space. It is recommended to allocate storage space that is equal to or greater than the volume of data to be imported.
- One import job supports importing data into one target table only.
- `IMPORT INTO` is not supported during TiDB cluster upgrades.
- Ensure that the data to be imported does not contain any records with primary key or non-null unique index conflicts. Otherwise, the conflicts can result in import task failures.
- Known issue: the `IMPORT INTO` task might fail if the PD address in the TiDB node configuration file is inconsistent with the current PD topology of the cluster. This inconsistency can arise in situations such as that PD was scaled in previously, but the TiDB configuration file was not updated accordingly or the TiDB node was not restarted after the configuration file update.

### `IMPORT INTO ... FROM FILE` restrictions

- For TiDB Self-Managed, each `IMPORT INTO` task supports importing data within 10 TiB. If you enable the [Global Sort](/tidb-global-sort.md) feature, each `IMPORT INTO` task supports importing data within 40 TiB.
- For [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated), if your data to be imported exceeds 500 GiB, it is recommended to use TiDB nodes with at least 16 cores and enable the [Global Sort](/tidb-global-sort.md) feature, then each `IMPORT INTO` task supports importing data within 40 TiB. If your data to be imported is within 500 GiB or if the cores of your TiDB nodes are less than 16, it is not recommended to enable the [Global Sort](/tidb-global-sort.md) feature.
- The execution of `IMPORT INTO ... FROM FILE` blocks the current connection until the import is completed. To execute the statement asynchronously, you can add the `DETACHED` option.
- Up to 16 `IMPORT INTO` tasks can run simultaneously on each cluster (see [TiDB Distributed eXecution Framework (DXF) usage limitations](/tidb-distributed-execution-framework.md#limitation)). When a cluster lacks sufficient resources or reaches the maximum number of tasks, newly submitted import tasks are queued for execution.
- When the [Global Sort](/tidb-global-sort.md) feature is used for data import, the value of the `THREAD` option must be at least `8`.
- When the [Global Sort](/tidb-global-sort.md) feature is used for data import, the data size of a single row after encoding must not exceed 32 MiB.
- All `IMPORT INTO` tasks that are created when [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md) is not enabled run directly on the nodes where the tasks are submitted, and these tasks will not be scheduled for execution on other TiDB nodes even after DXF is enabled later. After DXF is enabled, only newly created `IMPORT INTO` tasks that import data from S3 or GCS are automatically scheduled or failed over to other TiDB nodes for execution.

### `IMPORT INTO ... FROM SELECT` restrictions

- `IMPORT INTO ... FROM SELECT` can only be executed on the TiDB node that the current user is connected to, and it blocks the current connection until the import is complete.
- `IMPORT INTO ... FROM SELECT` only supports two [import options](#withoptions): `THREAD` and `DISABLE_PRECHECK`.
- `IMPORT INTO ... FROM SELECT` does not support the task management statements such as `SHOW IMPORT JOB(s)` and `CANCEL IMPORT JOB <job-id>`.
- The [temporary directory](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) of TiDB requires sufficient space to store the entire query result of the `SELECT` statement (configuring the `DISK_QUOTA` option is not supported currently).
- Importing historical data using [`tidb_snapshot`](/read-historical-data.md) is not supported.
- Because the syntax of the `SELECT` clause is complex, the `WITH` parameter in `IMPORT INTO` might conflict with it and cause parsing errors, such as `GROUP BY ... [WITH ROLLUP]`. It is recommended to create a view for complex `SELECT` statements and then use `IMPORT INTO ... FROM SELECT * FROM view_name` for importing. Alternatively, you can clarify the scope of the `SELECT` clause with parentheses, such as `IMPORT INTO ... FROM (SELECT ...) WITH ...`.

## Prerequisites for import

Before using `IMPORT INTO` to import data, make sure the following requirements are met:

- The target table to be imported is already created in TiDB and it is empty.
- The target cluster has sufficient space to store the data to be imported.
- For TiDB Self-Managed, the [temporary directory](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) of the TiDB node connected to the current session has at least 90 GiB of available space. If [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) is enabled and the data for import is from S3 or GCS, also make sure that the temporary directory of each TiDB node in the cluster has sufficient disk space.

## Required privileges

Executing `IMPORT INTO` requires the `SELECT`, `UPDATE`, `INSERT`, `DELETE`, and `ALTER` privileges on the target table. To import files in TiDB local storage, the `FILE` privilege is also required.

## Synopsis

```ebnf+diagram
ImportIntoStmt ::=
    'IMPORT' 'INTO' TableName ColumnNameOrUserVarList? SetClause? FROM fileLocation Format? WithOptions?
    |
    'IMPORT' 'INTO' TableName ColumnNameList? FROM SelectStatement WithOptions?

ColumnNameOrUserVarList ::=
    '(' ColumnNameOrUserVar (',' ColumnNameOrUserVar)* ')'

ColumnNameList ::=
    '(' ColumnName (',' ColumnName)* ')'

SetClause ::=
    'SET' SetItem (',' SetItem)*

SetItem ::=
    ColumnName '=' Expr

Format ::=
    'CSV' | 'SQL' | 'PARQUET'

WithOptions ::=
    'WITH' OptionItem (',' OptionItem)*

OptionItem ::=
    optionName '=' optionVal | optionName
```

## Parameter description

### ColumnNameOrUserVarList

It specifies how each field in the data file corresponds to the columns in the target table. You can also use it to map fields to variables to skip certain fields for the import, or use it in `SetClause`.

- If this parameter is not specified, the number of fields in each row of the data file must match the number of columns in the target table, and the fields will be imported to the corresponding columns in order.
- If this parameter is specified, the number of specified columns or variables must match the number of fields in each row of the data file.

### SetClause

It specifies how the values of target columns are calculated. In the right side of the `SET` expression, you can reference the variables specified in `ColumnNameOrUserVarList`.

In the left side of the `SET` expression, you can only reference a column name that is not included in `ColumnNameOrUserVarList`. If the target column name already exists in `ColumnNameOrUserVarList`, the `SET` expression is invalid.

### fileLocation

It specifies the storage location of the data file, which can be an Amazon S3 or GCS URI path, or a TiDB local file path.

- Amazon S3 or GCS URI path: for URI configuration details, see [URI Formats of External Storage Services](/external-storage-uri.md).

- TiDB local file path: it must be an absolute path, and the file extension must be `.csv`, `.sql`, or `.parquet`. Make sure that the files corresponding to this path are stored on the TiDB node connected by the current user, and the user has the `FILE` privilege.

> **Note:**
>
> If [SEM](/system-variables.md#tidb_enable_enhanced_security) is enabled in the target cluster, the `fileLocation` cannot be specified as a local file path.

In the `fileLocation` parameter, you can specify a single file, or use the `*` and `[]` wildcards to match multiple files for import. Note that the wildcard can only be used in the file name, because it does not match directories or recursively match files in subdirectories. Taking files stored on Amazon S3 as examples, you can configure the parameter as follows:

- Import a single file: `s3://<bucket-name>/path/to/data/foo.csv`
- Import all files in a specified path: `s3://<bucket-name>/path/to/data/*`
- Import all files with the `.csv` suffix in a specified path: `s3://<bucket-name>/path/to/data/*.csv`
- Import all files with the `foo` prefix in a specified path: `s3://<bucket-name>/path/to/data/foo*`
- Import all files with the `foo` prefix and the `.csv` suffix in a specified path: `s3://<bucket-name>/path/to/data/foo*.csv`
- Import `1.csv` and `2.csv` in a specified path: `s3://<bucket-name>/path/to/data/[12].csv`

### Format

The `IMPORT INTO` statement supports three data file formats: `CSV`, `SQL`, and `PARQUET`. If not specified, the default format is `CSV`.

### WithOptions

You can use `WithOptions` to specify import options and control the data import process. For example, to execute the import of data files asynchronously in the backend, you can enable the `DETACHED` mode for the import by adding the `WITH DETACHED` option to the `IMPORT INTO` statement.

The supported options are described as follows:

| Option name | Supported data sources and formats | Description |
|:---|:---|:---|
| `CHARACTER_SET='<string>'` | CSV | Specifies the character set of the data file. The default character set is `utf8mb4`. The supported character sets include `binary`, `utf8`, `utf8mb4`, `gb18030`, `gbk`, `latin1`, and `ascii`. |
| `FIELDS_TERMINATED_BY='<string>'` | CSV | Specifies the field separator. The default separator is `,`. |
| `FIELDS_ENCLOSED_BY='<char>'` | CSV | Specifies the field delimiter. The default delimiter is `"`. |
| `FIELDS_ESCAPED_BY='<char>'` | CSV | Specifies the escape character for fields. The default escape character is `\`. |
| `FIELDS_DEFINED_NULL_BY='<string>'` | CSV | Specifies the value that represents `NULL` in the fields. The default value is `\N`. |
| `LINES_TERMINATED_BY='<string>'` | CSV | Specifies the line terminator. By default, `IMPORT INTO` automatically identifies `\n`, `\r`, or `\r\n` as line terminators. If the line terminator is one of these three, you do not need to explicitly specify this option. |
| `SKIP_ROWS=<number>` | CSV | Specifies the number of rows to skip. The default value is `0`. You can use this option to skip the header in a CSV file. If you use a wildcard to specify the source files for import, this option applies to all source files that are matched by the wildcard in `fileLocation`. |
| `SPLIT_FILE` | CSV | Splits a single CSV file into multiple smaller chunks of around 256 MiB for parallel processing to improve import efficiency. This parameter only works for **non-compressed** CSV files and has the same usage restrictions as that of TiDB Lightning [`strict-format`](https://docs.pingcap.com/tidb/stable/tidb-lightning-data-source#strict-format). Note that you need to explicitly specify `LINES_TERMINATED_BY` for this option. |
| `DISK_QUOTA='<string>'` | All file formats | Specifies the disk space threshold that can be used during data sorting. The default value is 80% of the disk space in the TiDB [temporary directory](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630). If the total disk size cannot be obtained, the default value is 50 GiB. When specifying `DISK_QUOTA` explicitly, make sure that the value does not exceed 80% of the disk space in the TiDB temporary directory. |
| `DISABLE_TIKV_IMPORT_MODE` | All file formats | Specifies whether to disable switching TiKV to import mode during the import process. By default, switching TiKV to import mode is not disabled. If there are ongoing read-write operations in the cluster, you can enable this option to avoid impact from the import process. |
| `THREAD=<number>` | All file formats and query results of `SELECT` | Specifies the concurrency for import. For `IMPORT INTO ... FROM FILE`, the default value of `THREAD` is 50% of the number of CPU cores on the TiDB node, the minimum value is `1`, and the maximum value is the number of CPU cores. For `IMPORT INTO ... FROM SELECT`, the default value of `THREAD` is `2`, the minimum value is `1`, and the maximum value is two times the number of CPU cores on the TiDB node. To import data into a new cluster without any data, it is recommended to increase this concurrency appropriately to improve import performance. If the target cluster is already used in a production environment, it is recommended to adjust this concurrency according to your application requirements. |
| `MAX_WRITE_SPEED='<string>'` | All file formats | Controls the write speed to a TiKV node. By default, there is no speed limit. For example, you can specify this option as `1MiB` to limit the write speed to 1 MiB/s. |
| `CHECKSUM_TABLE='<string>'` | All file formats | Configures whether to perform a checksum check on the target table after the import to validate the import integrity. The supported values include `"required"` (default), `"optional"`, and `"off"`. `"required"` means performing a checksum check after the import. If the checksum check fails, TiDB will return an error and the import will exit. `"optional"` means performing a checksum check after the import. If an error occurs, TiDB will return a warning and ignore the error. `"off"` means not performing a checksum check after the import. |
| `DETACHED` | All file formats | Controls whether to execute `IMPORT INTO` asynchronously. When this option is enabled, executing `IMPORT INTO` immediately returns the information of the import job (such as the `Job_ID`), and the job is executed asynchronously in the backend. |
| `CLOUD_STORAGE_URI` | All file formats | Specifies the target address where encoded KV data for [Global Sort](/tidb-global-sort.md) is stored. When `CLOUD_STORAGE_URI` is not specified, `IMPORT INTO` determines whether to use Global Sort based on the value of the system variable [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740). If this system variable specifies a target storage address, `IMPORT INTO` uses this address for Global Sort. When `CLOUD_STORAGE_URI` is specified with a non-empty value, `IMPORT INTO` uses that value as the target storage address. When `CLOUD_STORAGE_URI` is specified with an empty value, local sorting is enforced. Currently, the target storage address only supports S3. For details about the URI configuration, see [Amazon S3 URI format](/external-storage-uri.md#amazon-s3-uri-format). When this feature is used, all TiDB nodes must have read and write access for the target S3 bucket, including at least these permissions: `s3:ListBucket`, `s3:GetObject`, `s3:DeleteObject`, `s3:PutObject`, `s3: AbortMultipartUpload`. |
| `DISABLE_PRECHECK` | All file formats and query results of `SELECT` | Setting this option disables pre-checks of non-critical items, such as checking whether there are CDC or PITR tasks.  |

## `IMPORT INTO ... FROM FILE` usage

For TiDB Self-Managed, `IMPORT INTO ... FROM FILE` supports importing data from files stored in Amazon S3, GCS, and the TiDB local storage. For [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated), `IMPORT INTO ... FROM FILE` supports importing data from files stored in Amazon S3 and GCS. For [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless), `IMPORT INTO ... FROM FILE` supports importing data from files stored in Amazon S3 and Alibaba Cloud OSS.

- For data files stored in Amazon S3 or GCS, `IMPORT INTO ... FROM FILE` supports running in the [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md).

    - When the DXF is enabled ([tidb_enable_dist_task](/system-variables.md#tidb_enable_dist_task-new-in-v710) is `ON`), `IMPORT INTO` splits a data import job into multiple sub-jobs and distributes these sub-jobs to different TiDB nodes for execution to improve the import efficiency.
    - When the DXF is disabled, `IMPORT INTO ... FROM FILE` only supports running on the TiDB node where the current user is connected.

- For data files stored locally in TiDB, `IMPORT INTO ... FROM FILE` only supports running on the TiDB node where the current user is connected. Therefore, the data files need to be placed on the TiDB node where the current user is connected. If you access TiDB through a proxy or load balancer, you cannot import data files stored locally in TiDB.

### Compressed files

`IMPORT INTO ... FROM FILE` supports importing compressed `CSV` and `SQL` files. It can automatically determine whether a file is compressed and the compression format based on the file extension:

| Extension | Compression format |
|:---|:---|
| `.gz`, `.gzip` | gzip compression format |
| `.zstd`, `.zst` | ZStd compression format |
| `.snappy` | snappy compression format |

> **Note:**
>
> - The Snappy compressed file must be in the [official Snappy format](https://github.com/google/snappy). Other variants of Snappy compression are not supported.
> - Because TiDB Lightning cannot concurrently decompress a single large compressed file, the size of the compressed file affects the import speed. It is recommended that a source file is no greater than 256 MiB after decompression.

### Global Sort

> **Note:**
>
> Global Sort is not available on [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

`IMPORT INTO ... FROM FILE` splits the data import job of a source data file into multiple sub-jobs, each sub-job independently encoding and sorting data before importing. If the encoded KV ranges of these sub-jobs have significant overlap (to learn how TiDB encodes data to KV, see [TiDB computing](/tidb-computing.md)), TiKV needs to keep compaction during import, leading to a decrease in import performance and stability.

In the following scenarios, there can be significant overlap in KV ranges:

- If rows in the data file assigned to each sub-job have overlapping primary key ranges, the data KV generated by the encoding of each sub-job will also overlap.
    - `IMPORT INTO` splits sub-jobs based on the traversal order of data files, usually sorted by file name in lexicographic order.
- If the target table has many indexes, or the index column values are scattered in the data file, the index KV generated by the encoding of each sub-job will also overlap.

When the [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md) is enabled, you can enable [Global Sort](/tidb-global-sort.md) by specifying the `CLOUD_STORAGE_URI` option in the `IMPORT INTO` statement or by specifying the target storage address for encoded KV data using the system variable [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740). Currently, Global Sort supports using Amazon S3 as the storage address. When Global Sort is enabled, `IMPORT INTO` writes encoded KV data to the cloud storage, performs Global Sort in the cloud storage, and then parallelly imports the globally sorted index and table data into TiKV. This prevents problems caused by KV overlap and enhances import stability and performance.

Global Sort consumes a significant amount of memory resources. Before the data import, it is recommended to configure the [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640) and [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) variables, which avoids golang GC being frequently triggered and thus affecting the import efficiency.

```sql
SET GLOBAL tidb_server_memory_limit_gc_trigger=1;
SET GLOBAL tidb_server_memory_limit='75%';
```

> **Note:**
>
> - If the KV range overlap in a source data file is low, enabling Global Sort might decrease import performance. This is because when Global Sort is enabled, TiDB needs to wait for the completion of local sorting in all sub-jobs before proceeding with the Global Sort operations and subsequent import.
> - After an import job using Global Sort completes, the files stored in the cloud storage for Global Sort are cleaned up asynchronously in a background thread.

### Output

When `IMPORT INTO ... FROM FILE` completes the import or when the `DETACHED` mode is enabled, TiDB returns the current job information in the output, as shown in the following examples. For the description of each field, see [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md).

When `IMPORT INTO ... FROM FILE` completes the import, the example output is as follows:

```sql
IMPORT INTO t FROM '/path/to/small.csv';
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|  60002 | /path/to/small.csv | `test`.`t`   |      363 |       | finished | 16B              |             2 |                | 2023-06-08 16:01:22.095698 | 2023-06-08 16:01:22.394418 | 2023-06-08 16:01:26.531821 | root@%     |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
```

When the `DETACHED` mode is enabled, executing the `IMPORT INTO ... FROM FILE` statement will immediately return the job information in the output. From the output, you can see that the status of the job is `pending`, which means waiting for execution.

```sql
IMPORT INTO t FROM '/path/to/small.csv' WITH DETACHED;
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
```

### View and manage import jobs

For an import job with the `DETACHED` mode enabled, you can use [`SHOW IMPORT`](/sql-statements/sql-statement-show-import-job.md) to view its current job progress.

After an import job is started, you can cancel it using [`CANCEL IMPORT JOB <job-id>`](/sql-statements/sql-statement-cancel-import-job.md).

### Examples

#### Import a CSV file with headers

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### Import a file asynchronously in the `DETACHED` mode

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH DETACHED;
```

#### Skip importing a specific field in your data file

Assume that your data file is in the CSV format and its content is as follows:

```
id,name,age
1,Tom,23
2,Jack,44
```

And assume that the target table schema for the import is `CREATE TABLE t(id int primary key, name varchar(100))`. To skip importing the `age` field in the data file to the table `t`, you can execute the following SQL statement:

```sql
IMPORT INTO t(id, name, @1) FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### Import multiple data files using wildcards

Assume that there are three files named `file-01.csv`, `file-02.csv`, and `file-03.csv` in the `/path/to/` directory. To import these three files into a target table `t` using `IMPORT INTO`, you can execute the following SQL statement:

```sql
IMPORT INTO t FROM '/path/to/file-*.csv';
```

If you only need to import `file-01.csv` and `file-03.csv` into the target table, execute the following SQL statement:

```sql
IMPORT INTO t FROM '/path/to/file-0[13].csv';
```

#### Import data files from Amazon S3 or GCS

- Import data files from Amazon S3:

    ```sql
    IMPORT INTO t FROM 's3://bucket-name/test.csv?access-key=XXX&secret-access-key=XXX';
    ```

- Import data files from GCS:

    ```sql
    IMPORT INTO t FROM 'gs://import/test.csv?credentials-file=${credentials-file-path}';
    ```

For details about the URI path configuration for Amazon S3 or GCS, see [URI Formats of External Storage Services](/external-storage-uri.md).

#### Calculate column values using SetClause

Assume that your data file is in the CSV format and its content is as follows:

```
id,name,val
1,phone,230
2,book,440
```

And assume that the target table schema for the import is `CREATE TABLE t(id int primary key, name varchar(100), val int)`. If you want to multiply the `val` column values by 100 during the import, you can execute the following SQL statement:

```sql
IMPORT INTO t(id, name, @1) SET val=@1*100 FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### Import a data file in the SQL format

```sql
IMPORT INTO t FROM '/path/to/file.sql' FORMAT 'sql';
```

#### Limit the write speed to TiKV

To limit the write speed to a TiKV node to 10 MiB/s, execute the following SQL statement:

```sql
IMPORT INTO t FROM 's3://bucket/path/to/file.parquet?access-key=XXX&secret-access-key=XXX' FORMAT 'parquet' WITH MAX_WRITE_SPEED='10MiB';
```

## `IMPORT INTO ... FROM SELECT` usage

`IMPORT INTO ... FROM SELECT` lets you import the query result of a `SELECT` statement to an empty table in TiDB. You can also use it to import historical data queried with [`AS OF TIMESTAMP`](/as-of-timestamp.md).

### Import the query result of `SELECT`

To import the `UNION` result to the target table `t`, with the import concurrency specified as `8` and precheck of non-critical items configured as disabled, execute the following SQL statement:

```sql
IMPORT INTO t FROM SELECT * FROM src UNION SELECT * FROM src2 WITH THREAD = 8, DISABLE_PRECHECK;
```

### Import historical data at a specified time point

To import historical data at a specified time point to the target table `t`, execute the following SQL statement:

```sql
IMPORT INTO t FROM SELECT * FROM src AS OF TIMESTAMP '2024-02-27 11:38:00';
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
* [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)
* [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md)
