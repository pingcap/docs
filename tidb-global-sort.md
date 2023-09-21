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

## Feature overview

TiDB's Global Sort feature enhances the stability and efficiency of data import and DDL (Data Definition Language) operations. It serves as a general operator in the [distributed parallel execution framework](/tidb-distributed-execution-framework.md). Through the distributed parallel execution framework, it provides a global sort service on cloud.

Additionally, it can be easily extended to support multiple shared storage interfaces such as S3 and POSIX, enabling seamless integration with different storage systems. This flexibility enables efficient and adaptable data sorting for various use cases.

## Use cases

The Global Sort feature is designed to enhance the efficiency of `IMPORT INTO` and `CREATE INDEX`. By integrating Global Sort into backend tasks, we can improve stability, control, and scalability. As a result, TiDB will offer an enhanced user experience and higher-quality service.

The Global Sort feature provides services for executing tasks within the unified distributed parallel execution framework and ensuring efficient and parallel sorting of data on a global scale.

## Limitations

Currently, the Global Sort feature is not used as a component of the query execution process responsible for sorting query results.

## Use Global Sort

1. Before enabling Global Sort, you need to enable the distributed execution framework. To do so, set the value of [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) to `ON`:

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

2. Set [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) to the correct cloud storage path. See [an example](/br/backup-and-restore-storages.md).

   ```sql
   SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
   ```

## Implementation principles

The algorithm of the TiDB backend task distributed execution framework is as follows:

![Algorithm of Global Sort](/media/dist-task/global-sort.jpeg)

The detailed implementation principles is as follows:

### Step 1: Scan and prepare data

1. After TiDB nodes scan a specific range of data:

    1. TiDB nodes encode them into Key-Value pairs.
    2. TiDB nodes sort Key-Value pairs into several block data segments, where each segment is one file and is uploaded into S3.

2. The TiDB node also records a serial actual Key-Value ranges for each segment (referred to as a statistics file), which is a key preparation for scalable sort implementation. These files are then uploaded into S3 along with the real data.

### Step 2: Sort and distribute data

From Step 1, we have obtained a list of sorted blocks and their correlated statistics files, which gives us the number of locally sorted blocks. We also have a real data scope that can be used by PD to split and scatter. The following steps are performed:

1. The records in the statistics file are sorted to cut an almost even range to be subtasks of Step 2's sort and ingest regions.
2. The subtasks are distributed to TiDB nodes for execution.
3. All TiDB nodes will independently sort the data of subtasks into ranges and ingest them into TiKV without overlap.
