---
title: IMPORT INTO vs. TiDB Lightning
summary: Learn about the differences between `IMPORT INTO` and TiDB Lightning.
---

# IMPORT INTO vs. TiDB Lightning

Many users have provided feedback that the deployment, configuration, and maintenance of [TiDB Lightning](/tidb-lightning/tidb-lightning-configuration.md) are complex, especially in scenarios involving [parallel importing](/tidb-lightning/tidb-lightning-distributed-import.md) of large datasets.

Based on the feedback, TiDB has gradually integrated some functionalities of TiDB Lightning into the [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) SQL statement. You can directly import data by executing `IMPORT INTO`, thereby improving the efficiency of data import. In addition, `IMPORT INTO` supports some functionalities that TiDB Lightning does not, such as automatic distributed task scheduling and [TiDB Global Sort](/tidb-global-sort.md).

`IMPORT INTO` is introduced in v7.2.0 and becomes generally available (GA) in v7.5.0. It will continue to be improved and optimized in future versions. Once the `IMPORT INTO` capability can fully replace TiDB Lightning, TiDB Lightning will be deprecated. At that time, relevant notification will be provided in advance in TiDB Release Notes and documentation.

## Comparison between `IMPORT INTO` and TiDB Lightning

The following sections describe the differences between `IMPORT INTO` and TiDB Lightning in multiple dimensions.

### Deployment cost

#### `IMPORT INTO`

`IMPORT INTO` does not require separate deployment. You can run it directly on TiDB nodes, which eliminates additional deployment work.

#### TiDB Lightning

By contrast, TiDB Lightning requires [separate server deployment](/tidb-lightning/deploy-tidb-lightning.md).

### Resource utilization

#### `IMPORT INTO`

The `IMPORT INTO` task and other business workloads can share TiDB resources or utilize them at different times to fully leverage the TiDB resources. To ensure stable operation of business workloads while maintaining the performance and stability of the `IMPORT INTO` task, you can specify [specific TiDB nodes](/system-variables.md#tidb_service_scope-new-in-v740) dedicated to `IMPORT INTO` for data import.

When you use [TiDB Global Sort](/tidb-global-sort.md), there is no need to mount large local disks. TiDB Global Sort can use Amazon S3 as the storage. Once the import task is completed, the temporary data stored on Amazon S3 for global sorting will be automatically deleted to save storage costs.

#### TiDB Lightning

You need separate servers to deploy and run TiDB Lightning. When no import tasks are executed, these resources remain idle. The total idle time is even longer in scenarios where import tasks are executed periodically, resulting in a waste of resources.

If the dataset to be imported is large, you also need to prepare large local disks to sort the data to be imported.

### Task configuration and integration

#### `IMPORT INTO`

You can directly write SQL statements to submit import tasks, which are easy to call and integrate.

#### TiDB Lightning

By contrast, TiDB Lightning requires you to write [task configuration files](/tidb-lightning/tidb-lightning-configuration.md). These configuration files are complex and not easily called by third parties.

### Task scheduling

#### `IMPORT INTO`

`IMPORT INTO` supports distributed execution. For example, when you import 40 TiB of source data files into one target table, after submitting the SQL statement, TiDB will automatically split the import task into multiple sub-tasks and schedule different TiDB nodes to execute these sub-tasks.

#### TiDB Lightning

By contrast, the configuration for TiDB Lightning is complex, inefficient, and prone to errors.

Assume that you start 10 TiDB Lightning instances to import data in parallel, then you need to create 10 TiDB Lightning configuration files. In each file, you need to configure the range of source files to be read by the corresponding TiDB Lightning instance. For example, TiDB Lightning instance 1 reads the first 100 files, instance 2 reads the next 100 files, and so on.

In addition, you need to configure the shared metadata table and other configuration information for these 10 TiDB Lightning instances, which is complex.

### Global Sort vs. local sort

#### `IMPORT INTO`

With TiDB Global Sort, `IMPORT INTO` can transmit tens of TiB of source data to multiple TiDB nodes, encode the data KV pairs and index KV pairs, and then transfer these pairs to Amazon S3 for global sorting before writing them into TiKV.

Because these KV pairs are globally sorted, data imported from various TiDB nodes into TiKV does not overlap, allowing it to be written directly into the RocksDB. This eliminates the need for TiKV to perform compaction operations, resulting in significant improvement in both write performance and stability of TiKV.

After the import is completed, the data used for global sorting on Amazon S3 will be automatically deleted, saving storage costs.

#### TiDB Lightning

TiDB Lightning only supports local sort. For example, for tens of TiB of source data, if TiDB Lightning does not have large local disks configured, or if multiple TiDB Lightning instances are used for parallel import, each TiDB Lightning instance can only use local disks to sort the data to be imported. Due to the inability to perform global sort, there will be an overlap between the data imported into TiKV by multiple TiDB Lightning instances, especially in scenarios where index data is more prevalent, triggering TiKV to perform compaction operations. Compaction operations are resource-intensive, which will lead to a decrease in TiKV's write performance and stability.

If you want to continue importing data later, you will need to keep the TiDB Lightning server and the disks on the server for the next import. The cost of using preallocated disks is relatively high, compared with `IMPORT INTO` using Amazon S3 on a pay-as-you-go basis.

### Performance

Currently, there are no performance test comparison results under equivalent test environments between `IMPORT INTO` and TiDB Lightning.

When Amazon S3 is used as the storage for global sorting, the performance test results for `IMPORT INTO` are as follows:

| Source dataset                    | Node configuration                                           | Average import speed per TiDB node |
|------------------------------------|--------------------------------------------------------------|------------------------------------|
| 40 TiB data (2.26 billion rows, 19 KiB per row) | 10 TiDB (16C32G) nodes and 20 TiKV (16C27G) nodes | 222 GiB/h |
| 10 TiB data (565 million rows, 19 KiB per row) | 5 TiDB (16C32G) nodes and 10 TiKV (16C27G) nodes | 307 GiB/h |

### High availability

#### `IMPORT INTO`

After a TiDB node fails, tasks on that node are automatically transferred to the remaining TiDB nodes to continue running.

#### TiDB Lightning

After a TiDB Lightning instance node fails, you need to perform manual recovery of tasks on a new node based on previously recorded checkpoints.

### Scalability

#### `IMPORT INTO`

Due to the use of Global Sort, data imported into TiKV does not overlap, resulting in better scalability compared with TiDB Lightning.

#### TiDB Lightning

Due to only supporting local sort, data imported into TiKV might overlap when new TiDB Lightning instances are added, resulting in more compaction operations for TiKV and limiting scalability relative to `IMPORT INTO`.

## Functionalities not supported by `IMPORT INTO`

Currently, `IMPORT INTO` still lacks some functionalities and cannot fully replace TiDB Lightning in some scenarios, such as:

- Logical import

    Before importing data with `IMPORT INTO`, the target table must be empty. If you need to import data into a table that already contains data, it is recommended to use methods such as [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) or direct insertion. Starting from v8.0, TiDB supports [bulk DML](/system-variables.md#tidb_dml_type-new-in-v800) for executing large transactions.

- Conflict data handling

    `IMPORT INTO` currently does not support conflict data handling. Before the data import, you need to define the table schema properly to ensure that the data to be imported does not conflict with primary keys (PK) or unique keys (UK). Otherwise, it might cause task failures.

- Importing data into multiple target tables

    Currently, only one target table is allowed for one `IMPORT INTO` SQL statement. If you want to import data into multiple target tables, you need to submit multiple `IMPORT INTO` SQL statements.

In future versions, these functionalities will be supported by `IMPORT INTO`, along with additional enhancements to its capabilities, such as allowing modification of concurrency during task execution and adjusting throughput for writing to TiKV. This will make it more convenient for you to manage tasks.

## Summary

Compared with TiDB Lightning, `IMPORT INTO`can be directly executed on TiDB nodes, supports automated distributed task scheduling and [TiDB Global Sort](/tidb-global-sort.md), and offers significant improvements in deployment, resource utilization, task configuration convenience, ease of invocation and integration, high availability, and scalability. It is recommended that you consider using `IMPORT INTO` instead of TiDB Lightning in appropriate scenarios.
