---
title: IMPORT INTO vs. TiDB Lightning
summary: Learn about the differences between `IMPORT INTO` and TiDB Lightning.
---

# IMPORT INTO vs. TiDB Lightning

Many users have provided feedback that the deployment, configuration, and maintenance of [TiDB Lightning](/tidb-lightning/tidb-lightning-configuration.md) are quite complex, especially in scenarios involving [parallel importing](/tidb-lightning/tidb-lightning-distributed-import.md) of large volumes of data.

As a result, TiDB has gradually integrated some functionalities of TiDB Lightning into the [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) SQL statement. You can directly import data by executing `IMPORT INTO`, thereby improving the efficiency of data import. In addition, `IMPORT INTO` supports some functionalities that TiDB Lightning does not, such as automatic distributed task scheduling and [TiDB Global Sort](/tidb-global-sort.md).

`IMPORT INTO` is introduced in v7.2.0 and becomes generally available (GA) in v7.5.0. Once the `IMPORT INTO` capability can fully replace TiDB Lightning, TiDB Lightning will be deprecated. At that time, a notification will be provided in advance on the official website.

## Comparison between `IMPORT INTO` and TiDB Lightning

The following sections describe the differences between `IMPORT INTO` and TiDB Lightning in multiple dimensions.

### Deployment cost

#### `IMPORT INTO`

`IMPORT INTO` does not require separate deployment. You can run it directly on TiDB nodes, which eliminates additional deployment work.

#### TiDB Lightning

By contrast, TiDB Lightning requires [separate server deployment](/tidb-lightning/deploy-tidb-lightning.md).

### Resource utilization

#### `IMPORT INTO`

You can share TiDB nodes with other businesses or use them at different times to fully use the resources. For stable business operations with optimal import performance, you can specify [specific TiDB nodes](/system-variables.md#tidb_service_scope-new-in-v740) to be dedicated solely to `IMPORT INTO` for data import.

When using TiDB Global Sort, there is no need to mount large local disks. TiDB Global Sort can be done using S3. Once completed, you can delete the data to save storage costs.

#### TiDB Lightning

Separate servers are required to deploy and run TiDB Lightning. When there are no import tasks being executed, these machine resources remain idle. This idle time is even longer in scenarios where import tasks are executed periodically.

If the volume of imported data is large, it is necessary to prepare large local disks to sort the data to be imported.

### Task configuration and integration

#### `IMPORT INTO`

You can directly write SQL statements to submit import tasks, which is easy to call and integrate.

#### TiDB Lightning

By contrast, TiDB Lightning requires you to write [task configuration files](/tidb-lightning/tidb-lightning-configuration.md), which are complex and not easily called by third parties.

### Task scheduling

#### `IMPORT INTO`

`IMPORT INTO` is naturally distributed. For example, when you import 40 TiB of source data files into one target table, after submitting the SQL statement, TiDB will automatically split it into multiple sub-tasks and schedule them to execute distributed import tasks on different TiDB nodes.

#### TiDB Lightning

Configuration for TiDB Lightning is complex, inefficient, and prone to errors.

For example, if you start 10 parallel TiDB Lightning imports, you need to write 10 TiDB Lightning configuration files, and configure each configuration file with the range of source files to be read by each TiDB Lightning instance. TiDB Lightning instance 1 reads the first 100 files, instance 2 reads the next 100 files, and so on.

In addition, you need to configure the shared metadata table and other configuration information for these 10 TiDB Lightning instances.

### Global Sort vs. local sort

#### `IMPORT INTO`

Based on global sort, tens of TiB of source data can be transmitted to multiple TiDB nodes, where the encoded data KV pairs and index KV pairs are transferred to S3 for global sorting before being written to TiKV.

Because it is globally sorted, data imported from various TiDB nodes into TiKV does not overlap, allowing it to be ingested directly into the RocksDB's L6 layer. This eliminates the need for TiKV to perform compaction operations, resulting in significant improvement in both write performance and stability of TiKV.

After the import is completed, the data used for global sorting on S3 will be automatically deleted, saving storage costs.

#### TiDB Lightning

TiDB Lightning only supports local sort. For example, for tens of TiB of source data, if TiDB Lightning does not have large local disks configured, or if multiple TiDB Lightning instances are used for parallel import, each TiDB Lightning instance will only use local disks to sort the data responsible for the import. Due to the inability to perform global sorting, there will be overlap between the data imported into TiKV by multiple TiDB Lightning instances, especially in scenarios where index data is more prevalent, triggering TiKV to perform compaction operations. Bcause compaction is a very resource-intensive operation, it will lead to a decrease in TiKV's write performance and stability.

In addition, after data import is complete, you still need to retain the local disks of TiDB Lightning for the next import. The cost is relatively higher compared to S3.

### Performance

Currently, there are no performance test comparison results under equivalent test environments between `IMPORT INTO` and TiDB Lightning.

The `IMPORT INTO` performance test results with Global Sort are as follows:

Data Sets:

- 40 TiB of data (2.26 billion rows, single row size 19 KiB)
- 10 TiB of data (565 million rows, single row size 19 KiB)

AWS:

- Importing 40 TiB of data, 10 TiDB (16C32G) 20 TiKV nodes (16C27G), the average single TiDB node import speed is approximately 222 GiB/h.
- Importing 10 TiB of data, 5 TiDB (16C32G) 10 TiKV (16C27G), the average single TiDB node import speed is approximately 307 GiB/h.

### High availability

#### `IMPORT INTO`

After a TiDB node failure, tasks on that node are automatically transferred to the remaining TiDB nodes to continue running.

#### TiDB Lightning

After a TiDB Lightning instance node failure, you need to perform manual recovery of tasks on a new node based on previously recorded checkpoints, allowing for resumption of task execution.

### Scalability

#### `IMPORT INTO`

Due to the use of Global Sort, data imported into TiKV does not overlap, resulting in better scalability compared to TiDB Lightning.

#### TiDB Lightning

Due to only supporting local sort, data imported into TiKV might overlap when adding TiDB Lightning instances, resulting in more compaction operations for TiKV, limiting scalability relative to `IMPORT INTO`.

## Functionalities not supported by `IMPORT INTO`

Currently, `IMPORT INTO` still lacks some functionalities that cannot replace TiDB Lightning, such as:

- Logical import

    Before importing data with `IMPORT INTO`, the target table must be empty. If you need to import data into a table that already contains data, it is recommended to use methods like `LOAD DATA` or direct insertion. TiDB v8.0 supports batch DML for executing large transactions.

- Conflict data handling

    `IMPORT INTO` currently does not support conflict data handling. You need to define the table structure properly to ensure that the data to be imported does not conflict with primary keys (PK) or unique keys (UK). Otherwise, it might cause task failures.

- Importing data into multiple target tables

    Currently, only one target table is allowed for the `IMPORT INTO` SQL statement. If you want to import data into multiple target tables, you need to submit multiple `IMPORT INTO` SQL statements.

In future versions, these functionalities will be supported by `IMPORT INTO`, along with additional enhancements to its capabilities, such as allowing modification of concurrency during task execution and adjusting throughput for writing to TiKV. This will make it more convenient for you to manage tasks.

## Summary

Compared with TiDB Lightning, `IMPORT INTO` has greatly improved  in terms of deployment, resource utilization, task configuration convenience, ease of invocation and integration, automated distributed task scheduling and management, enhanced import stability based on Global Sort, high availability, and scalability. It is recommended that you consider using `IMPORT INTO` instead of TiDB Lightning in appropriate scenarios.
