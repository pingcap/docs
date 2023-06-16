---
title: 50 TB Data Import Practices
summary: Based on the experience of importing large single tables in the past, this article summarizes a best practice, hoping to help the import of large data volumes and large single tables
---

# Preface
TiDB Lightning ([Physical Import Mode](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)) is a comprehensive and efficient data import tool used for importing data into empty tables and initializing empty clusters, and uses files as the data source. TiDB Lightning provides two running modes: Single Instance and [Parallel Import](https://docs.pingcap.com/tidb/stable/tidb-lightning-distributed-import). You can import source files of different sizes.
- If the data scale of the source files is within 10 TB, it is recommended to use a single instance of TiDB Lightning for the import.
- If the data scale of the source files exceeds 10 TB, it is recommended to use multiple instances of TiDB Lightning for [Parallel Import](https://docs.pingcap.com/tidb/stable/tidb-lightning-distributed-import).
  - If the source file data scale is exceptionally large ( larger than 50 TB), in addition to parallel importing, you need to make certain preparations and optimizations based on the characteristics of the source data, table definitions, and parameter configurations to achieve better and faster completion of large-scale data import.
  
This article introduces some key factors and steps that affect TiDB Lightning data import. We have successfully imported large single table data over 50 TB into both the internal environment and customer site, and have accumulated these best practices based on these real application scenarios. These best practices can help you import large datasets successfully.

The following sections in this article apply to both importing multiple tables and importing large single tables:
- Key factors
- Prepare source files
- Estimate storage space
- Change configuration parameters
- Resolve the "checksum mismatch" issue
- Enable checkpoint

Due to the special nature of importing large single tables, best practices are described separately in the following section:
- Best practices for importing a large single table
# Key factors
When you import data, there are some key factors that can affect import performance and might even cause import to fail. Some common critical factors are as follows:
- Source files:
  - Whether the data within a single file is sorted by the primary key. Sorted data can achieve optimal import performance.
  - Whether there is overlap in the content of source files across TiDB Lightning instances. The smaller the overlap, the better the import performance.
- Table definitions:
  - The number and size of secondary indexes per table can affect import speed. More indexes result in slower imports and more space consumption after import.
  - Index data size = Number of indexes * Index size * Number of rows.
- Compression ratio:

  Data imported into a TiDB cluster is stored in a compressed format. The compression ratio can not be calculated in advance. It can only be determined after the data is actually imported into the TiKV cluster. You can first import a portion of the data (for example, 10%) to obtain the corresponding compression ratio of the cluster, and then use it to estimate the compression ratio of the entire data import.
- Configuration parameters:
  - `region-concurrency`: The concurrency of TiDB Lightning main logical processing. 
  - `send-kv-pairs`: The number of Key-Value pairs sent by TiDB Lightning to TiKV in a single request.
  - `disk-quota`:The disk quota used by TiDB Lightning local temp files when using Physical Import Mode
  - `GOMEMLIMIT`: TiDB Lightning is implemented in the Go language. Configure GOMEMLIMIT properly.
- Data validation:

  After data and index import is completed, an [`admin checksum`](https://docs.pingcap.com/tidb/dev/sql-statement-admin-checksum-table) is performed on each table, comparing it with the local checksum value of TiDB Lightning. When there are many tables or individual tables have a large number of rows, the checksum phase can take a long time.
- Execution plan:

  After the checksum is successfully completed, an [analyze table](https://docs.pingcap.com/tidb/dev/sql-statement-analyze-table) operation is performed on each table to generate the optimal execution plan. The [analyze table](https://docs.pingcap.com/tidb/dev/sql-statement-analyze-table) operation can be time-consuming when dealing with a large number of tables or individual tables with a significant amount of data.
- Relevant issues:
 
  During the actual process of importing 50 TB of data, certain issues might occur that are only exposed when dealing with a massive number of source files and large-scale clusters. When choosing a product version, it is recommended to check whether the corresponding issues have been fixed. 
  The following issues have been resolved in versions v6.5.3, v7.1, and later versions:
    - [Issue-14745](https://github.com/tikv/tikv/issues/14745): After the import is completed, a large number of temporary files are left in the TiKV import directory.
    - [Issue-6426](https://github.com/tikv/pd/issues/6426): The PD [range scheduling](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode-usage#scope-of-pausing-scheduling-during-import) interface might fail to scatter regions, resulting in timeout issues. Before v6.2.0, global scheduling is disabled by default, which can avoid triggering this problem.
    - [Issue-43079](https://github.com/pingcap/tidb/pull/43079): TiDB Lightning fails to refresh the Region Peers information during retry for NotLeader errors.
    - [Issue-43291](https://github.com/pingcap/tidb/issues/43291): TiDB Lightning does not retry in cases where temporary files are not found (the "No such file or directory" error).
# Prepare source files
- When generating files, within a single file, it is preferable to sort them by the primary key. If the table definition does not have a primary key, you can add an auto-increment primary key. In this case, the order of the file content does not matter.
- When multiple TiDB Lightning instances are partitioning the source files, it is advisable to minimize primary key overlap. If the generated files are globally ordered, they can be distributed into different TiDB Lightning instances based on ranges to achieve optimal import performance.
- Control each file to be less than 96 MB in size during file generation.
- If a file is exceptionally large and exceeds 256 MB, enable [strict-format](https://docs.pingcap.com/tidb/stable/migrate-from-csv-files-to-tidb#step-4-tune-the-import-performance-optional).
  
# Estimate storage space
Currently, there are two effective methods for space estimation:
- Assuming the total data size is A, the total index size is B, the replication factor is 3, and the compression ratio is α (typically around 2.5), the overall occupied space can be calculated as: (A+B)*3/α. This method is primarily used for estimating without performing any data import, to plan the cluster topology.
- Import only 10% of the data and multiply the actual occupied space by 10 to estimate the final space usage for that batch of data. This method is more accurate, especially when importing a large amount of data.

Note that it is recommended to reserve 20% of storage space, as background tasks such as compaction and snapshot replication also consume a portion of the storage space.
# Change configuration parameters
- `region-concurrency`: The concurrency of TiDB Lightning main logical processing. During parallel importing, it is recommended to set it to 75% of the CPU cores to prevent resource overload and potential OOM issues.
- `send-kv-pairs`: The number of Key-Value pairs sent by TiDB Lightning to TiKV in a single request. It is recommended to adjust this value based on the formula send-kv-pairs * row-size < 1 MB (In version 7.2, this parameter is replaced by `send-kv-size`, and no additional setting is required).
- `GOMEMLIMIT`: TiDB Lightning is implemented in the Go language. Setting GOMEMLIMIT to 80% of the instance memory to reduce the probability of OOM caused by the Go GC mechanism.
- `disk-quota`: It is advisable to ensure that the sorting directory space of TiDB Lightning is larger than the size of the data source. Otherwise, disk-quota can be set to 80% of the sorting directory space of TiDB Lightning. In this case, TiDB Lightning will sort and write data in batches based on the disk-quota, but the import performance will be lower than complete sorting.

  For more information about TiDB Lightning parameters, see [TiDB Lightning configuration parameters](https://docs.pingcap.com/tidb/stable/tidb-lightning-configuration).
# Resolve the "checksum mismatch" error
Conflicts might occur during data validation. The error message is "checksum mismatch". To resolve this issue, take the following approaches:

1. In the source data, check for conflicts primary key or unique key and resolve the conflicts before reimporting. In most cases, this is the most common cause.
2. Check if the table primary key or unique key definition is reasonable. If not, modify the table definition and reimport.
3. Enable [conflict detection](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode-usage#conflict-detection). This feature assumes that there is a small number (less than 10%) of unexpected conflicting data in the source data and requires TiDB Lightning to detect and resolve the conflicts.
# Enable checkpoint
For importing a large volume of data, it is essential to refer to the [Lightning Checkpoints](https://docs.pingcap.com/tidb/stable/tidb-lightning-checkpoints) documentation and enable checkpoints. It is recommended to prioritize using MySQL as the driver to avoid losing the checkpoint information if TiDB Lightning is running in a container environment where the container exits and deletes the checkpoint information.

If you encounter insufficient space in downstream TiKV during import, you can manually kill all TiDB Lightning instances (without using the -9 option). After scaling up the capacity, you can resume the import based on the checkpoint information.
# Best practices for importing a large single table
Importing multiple tables can increase the time required for checksum and analyze operations, sometimes exceeding the time required for data import itself. However, in general, it is not necessary to adjust the configuration. If there are one or more large tables among the multiple tables, it is recommended to separate the source files of these large tables and import them separately.

This section focuses on the best practices for importing large single tables. There is no strict definition for a large single table, but it is generally considered to meet one of the following conditions:
- The table size exceeds 10 TB.
- The number of rows exceeds 1 billion and the number of columns exceeds 50 in a wide table.
## Prepare source files
Follow the steps outlined in the source file preparation process mentioned above. For a large single table, if global ordering is not achievable but ordering within each file based on the primary key is possible, and the file is a standard CSV file, it is recommended to generate a large single file with each around 20 GB. Then, enable strict-format. This approach reduces overlap between TiDB Lightning instances and allows TiDB Lightning to split the file before the import, resulting in optimal import speed.
## Plan cluster topology
Prepare TiDB Lightning based on 5 TB to 10 TB of source data per instance. Deploy one TiDB Lightning instance on each node. The specifications of the nodes can be based on the [Environment of TiDB Lightning instance](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode#environment-requirements).
## Change configuration parameters
- Set `region-concurrency` to 75% of the number of cores of the TiDB Lightning instance.
- Set `send-kv-pairs` to 3200.
- Adjust `GOMEMLIMIT` to 80% of the memory on the node where the instance is located.

If during the import process, PD Scatter Region latency exceeds 30 minutes, consider the following optimizations:
- Check if the TiKV cluster encounters any IO bottlenecks.
- Increase TiKV `raftstore.apply-pool-size` from the default value of 2 to 4 or 8.
- Reduce TiDB Lightning `region-split-concurrency` to half the number of CPU cores, with a minimum value of 1.
## Disable execution plan
In the case of a large single table (for example, with over 1 billion rows and more than 50 columns), it is recommended to turn off the analyze operation (`analyze="off"`) during the import process and manually execute the [ANALYZE TABLE](https://docs.pingcap.com/zh/tidb/stable/sql-statement-analyze-table#analyze) statement after the import is completed.
