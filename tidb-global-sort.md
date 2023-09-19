---
title: TiDB Global Sort
summary: Learn the use cases, limitations, usage, and implementation principles of the TiDB Global Sort.
---

# TiDB Global Sort

> **Warning:**
>
> This feature is an experimental feature. It is not recommended to use it in production environments.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> Currently, this feature is only applicable to TiDB Dedicated clusters. You cannot use it on TiDB Serverless clusters.

</CustomContent>

## Feature Overview

TiDB's Global Sort feature enhances the stability and efficiency of Import data and DDL (Data Definition Language) operations. It serves as a general operator in the [distributed parallel execution framework](/tidb-distributed-execution-framework.md) and through distributed parallel executuion framework, it can also provide a global sort service on cloud.

Additionally, it can easy to be extended to support multiple shared storage interfaces such as S3 and POSIX, enabling seamless integration with different storage systems. This flexibility enables efficient and adaptable data sorting for various use cases.

## Goals and non-goals

#### Goals

Implementing this global sort feature facilitates the efficient import into and create index. By incorporating this functionality into backend tasks, we can achieve improved stability, control, and scalability. Ultimately, this enhancement results in a better user experience and higher service quality provided by TiDB. So, in conclusion, the global sort feature will be implemented as an operator within the unified distributed parallel execution framework. This operator will provide services for executing tasks within the framework, ensuring efficient and parallel sorting of data on a global scale.

### Non-goals 

Currently, the Global Sort feature is not used as a component of the query execution process responsible for sorting query results.

## Usage

1. To enable the distributed framework, set the value of [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) to `ON`:

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

2. Set [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) to the correct cloud storage path. See [Example](/br/backup-and-restore-storages.md)
   ```sql
   SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
   ```

## Implementation principles

The algorithm of the TiDB backend task distributed execution framework is as follows:

![Algorithm of Global Sort](/media/dist-task/global-sort.jpeg)

The details of the algorithm is as follows:
### Step 1: scan and prepare data

  1. After TiDB nodes scan a specific range of data
    1. They encode them into Key-Value pairs.
    2. They Sort them into several block data segments, where each segment will be one file and is uploaded into S3
  2. The TiDB node also records a serial actual Key-Value ranges for each segment (referred to as a statistics file), which is a key preparation for scalable sort implementation. These files are then uploaded into S3 along with the real data.

  ### Step 2: Sorting and distributing data

  1. From Step 1, we obtain a list of sorted blocks and their correlated statistics files, which gives us the number of locally sorted blocks. We also have a real data scope that could be used by PD to split and scatter.
    1. The records in the statistics file are sorted to cut an almost even range to be subtasks of Step 2's sort and ingest regions.
	  2. The subtasks are distributed to TiDB nodes for execution.
	  3. All TiDB nodes will independently sort the data of subtasks into ranges and ingest them into TiKV without overlap.