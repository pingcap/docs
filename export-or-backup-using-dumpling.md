---
title: Export or Backup Data Using Dumpling
summary: Use the Dumpling tool to export or backup data in TiDB.
category: how-to
---

# Export or Backup Data Using Dumpling

This document introduces how to use the [Dumpling](https://github.com/pingcap/dumpling) tool to export or backup data in TiDB. Dumpling exports data stored in TiDB as SQL or CSV data files and can be used to complete logical full backup or export.

For backups of SST files (KV pairs) or backups of incremental data that are not sensitive to latency, refer to [BR](/br/backup-and-restore-tool.md). For real-time backups of incremental data, refer to [TiCDC](/ticdc/ticdc-overview.md).

When using Dumpling, you need to execute the export command on a running cluster. This document assumes that there is a TiDB instance on the `127.0.0.1:4000` host and that this TiDB instance has a root user without a password.

## Export data from TiDB

Export data using the following command:

{{< copyable "shell-regular" >}}

```shell
dumpling \
  -u root \
  -P 4000 \
  -H 127.0.0.1 \
  --filetype sql \
  --threads 32 \
  -o /tmp/test \
  -F $(( 1024 * 1024 * 256 ))
```

In the above command, `-H`, `-P` and `-u` mean address, port and user, respectively. If password authentication is required, you can pass it to Dumpling with `-p $YOUR_SECRET_PASSWORD`.

Dumpling exports all tables (except for system tables) in the entire database by default. You can use `--where <SQL where expression>` to select the records to be exported. If the exported data is in CSV format (CSV files can be exported using `--filetype csv`), you can also use `--sql <SQL>` to export records selected by the specified SQL statement. 

For example, you can export all records that match `id < 100` in `test.sbtest1` using the following command:

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -H 127.0.0.1 \
  -o /tmp/test \
  --filetype csv \
  --sql "select * from `test`.`sbtest1` where id < 100"
```

Note that the `--sql` option can be used only for exporting CSV files for now. However, you can use `--where` to filter the rows to be exported, and use the following command to export all rows with `id < 100`:

> **Note:**
>
> You need to execute the `select * from <table-name> where id < 100` statement on all tables to be exported. If any table does not have the specified field, then the export fails.

{{< copyable "shell-regular" >}}

```shell
./dumpling \
  -u root \
  -P 4000 \
  -H 127.0.0.1 \
  -o /tmp/test \
  --where "id < 100"
```

> **Note:**
> 
> Currently, Dumpling does not support exporting only certain tables specified by users (i.e. `-T` flag, see [this issue](https://github.com/pingcap/dumpling/issues/76)). If you do need this feature, you can use [MyDumper](/backup-and-restore-using-mydumper-lightning.md) instead.

默认情况下，导出的文件会存储到 `./export-<current local time>` 目录下。常用参数如下：
The exported file is stored in the `. /export-<current local time>` directory by default. Commonly used parameters are as follows:

- `-o` 用于选择存储导出文件的目录。
- `-F` 选项用于指定单个文件的最大大小（和 MyDumper 不同，这里的单位是字节）。
- `-r` 选项用于指定单个文件的最大记录数（或者说，数据库中的行数）。

- `-o` is used to select the directory where the exported file will be stored.
- `-F` is used to specify the maximum size of a single file (different from MyDumper, the unit here is byte).
- `-r` is used to specify the maximum number of records (or, rather, the number of rows in the database) for a single file.

利用以上参数可以让 Dumpling 的并行度更高。
You can use the above parameters to provide Dumpling with a higher degree of parallelism.

还有一个尚未在上面展示出来的标志是 `--consistency <consistency level>`，这个标志控制导出数据“一致性保证”的方式。对于 TiDB 来说，默认情况下，会通过获取某个时间戳的快照来保证一致性（即 `--consistency snapshot`）。在使用 snapshot 来保证一致性的时候，可以使用 `--snapshot` 参数指定要备份的时间戳。还可以使用以下的一致性级别：
Another flag that has not yet been shown above is the `--consistency <consistency level>`, which controls the way in which data is exported for "consistency assurance". For TiDB, consistency is ensured by getting a snapshot of a certain timestamp by default (i.e. `--consistency snapshot`). When using snapshot for consistency, you can use the `--snapshot` parameter to specify the timestamp to back up. You can also use the following levels of consistency:


- `flush`：使用 [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock) 来保证一致性。
- `snapshot`：获取指定时间戳的一致性快照并导出。
- `lock`：为待导出的所有表上读锁。
- `none`：不做任何一致性保证。
- `auto`：对 MySQL 使用 `flush`，对 TiDB 使用 `snapshot`。

- `FLUSH`: use [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock) to ensure consistency.
- `snapshot`: Get a consistent snapshot of the specified timestamp and export it.
- `lock`: Add locks to read all tables to be exported.
- `none`: No guarantee of consistency.
- `auto`: use `flush` for MySQL and `snapshot` for TiDB.

一切完成之后，你应该可以在 `/tmp/test` 看到导出的文件了：
After everything is done, you can see the exported file in `/tmp/test`:

```shell
$ ls -lh /tmp/test | awk '{print $5 "\t" $9}'

140B  metadata
66B   test-schema-create.sql
300B  test.sbtest1-schema.sql
190K  test.sbtest1.0.sql
300B  test.sbtest2-schema.sql
190K  test.sbtest2.0.sql
300B  test.sbtest3-schema.sql
190K  test.sbtest3.0.sql
```

另外，假如数据量非常大，可以提前调长 GC 时间，以避免因为导出过程中发生 GC 导致导出失败：
In addition, if the data volume is very large, you can extend the GC time in advance to avoid export failure due to GC occurring during the export process.

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
```

在操作结束之后，再将 GC 时间调回原样（默认是 `10m`）：
After the operation is completed, you can set the GC time back to the same (default is `10m`):

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
```

最后，所有的这些导出数据都可以用 [Lightning](/tidb-lightning/tidb-lightning-tidb-backend.md) 导入回 TiDB。
Finally, you can import all this exported data back to TiDB using [Lightning](/tidb-lightning/tidb-lightning-tidb-backend.md).
