---
title: BR Batch Create Table
summary: Learn how to use BR batch create table feature. When restoring data, BR can use batch create table feature to speed up the restoration.
---

# BR Batch Create Table

When restoring data using Backup & Restore (BR), BR creates the databases and tables in the target TiDB first, then starts restoring data. In the versions earlier than TiDB v6.0.0, BR uses the [serial execution](#implementation-principles) scheme to create tables in the restoration process. However, when restoring data with a large number (nearly 50000) of tables, this scheme takes much time to create tables.

To speed up the table creation process, and thereby reduce the time for restoring data, the BR batch create table feature is introduced in TiDB v6.0.0. This feature is enabled by default.

> **Note:**
>
> - To use the BR batch create table feature, both TiDB and BR should be in 6.0.0 or later versions. If either TiDB or BR is in the version lower than 6.0.0, BR uses the serial execution scheme.
> - Suppose that you use a cluster management tool (for example, TiUP), and your TiDB and BR are in 6.0.0 or later versions. In this case, BR enables batch create table feature by default without additional configuration.

## User scenario

When you need to restore data with a considerable number of tables, for example, 50000 tables, you can use BR batch create table feature to speed up the restoration process.

For the detailed effect, see [Test batch create table feature](#test-batch-create-table).

## Use batch create table

BR enables batch create table feature and configures `--ddl-batch-size=128` by default in 6.0.0 or later versions. Therefore, you do not need to configure this parameter additionally. `--ddl-batch-size=128` means that BR creates tables in multiple batches, and each batch has 128 tables.

To disable this feature, you can set `--ddl-batch-size` to `0` by the following command:

{{< copyable "shell-regular" >}}

```shell
br restore full -s local:///br_data/ --pd 172.16.5.198:2379 --log-file restore.log --ddl-batch-size=0
```

After disabling the feature, BR uses the [serial execution scheme](#implementation-principles) instead.

## Implementation principles

- Serial execution scheme before v6.0.0:

    In the versions earlier than 6.0.0, BR uses the serial execution scheme. When restoring data, BR creates the databases and tables in the target TiDB first, then starts restoring data. To create tables, after calling TiDB API, BR uses the SQL statement `Create Table`. TiDB DDL owner creates tables sequentially. Once the DDL owner creates a table, the schema version changes correspondingly, and each version change synchronizes to other BRs and other TiDB DDL workers. Hence, when restoring a large number of tables, the serial execution scheme takes too much time.

- Batch create table scheme since v6.0.0:

    The batch create table feature uses the concurrent batch table creation scheme. From v6.0.0, by default, BR creates tables in multiple batches, and each batch has 128 tables. Using this scheme, when BR creates one batch of tables, TiDB schema version only changes once. This scheme significantly increases the speed of table creation.

## Test batch create table

This section describes the information of testing batch create table feature. The test environment is as follows:

- Cluster configurations:

    - 15 TiKV instances. Each TiKV instance has 16 CPU cores, 80 GB memory, and 16 threads to process RPC requests ([`import.num-threads`](/tikv-configuration-file.md#num-threads) = 16).
    - 3 TiDB instances. Each TiDB instance has 16 CPU cores, 32 GB memory.
    - 3 PD instances. Each PD instance has 16 CPU cores, 32 GB memory.

- Data to be restored: 16.16 TB

The test result is as follows:

```
‘[2022/03/12 22:37:49.060 +08:00] [INFO] [collector.go:67] ["Full restore success summary"] [total-ranges=751760] [ranges-succeed=751760] [ranges-failed=0] [split-region=1h33m18.078448449s] [restore-ranges=542693] [total-take=1h41m35.471476438s] [restore-data-size(after-compressed)=8.337TB] [Size=8336694965072] [BackupTS=431773933856882690] [total-kv=148015861383] [total-kv-size=16.16TB] [average-speed=2.661GB/s]’
```

In the result, you can find that the average speed of restoring one TiKV instance is as high as 181.65 MB/s （`average-speed(GB/s)`/`tikv_count` = `181.65(MB/s)`）.