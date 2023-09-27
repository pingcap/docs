---
title: TiDB Global Sort
summary: Learn the use cases, limitations, usage, and implementation principles of the TiDB Global Sort.
---

# TiDB Global Sort

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> Currently, this feature is only applicable to TiDB Dedicated clusters. You cannot use it on TiDB Serverless clusters.

</CustomContent>

## Overview

The TiDB Global Sort feature enhances the stability and efficiency of data import and DDL (Data Definition Language) operations. It serves as a general operator in the [distributed execution framework](/tidb-distributed-execution-framework.md). Through the distributed execution framework, it provides a global sort service on cloud.

Additionally, it can be easily extended to support multiple shared storage interfaces such as S3 and POSIX, enabling seamless integration with different storage systems. This flexibility enables efficient and adaptable data sorting for various use cases.

## Use cases

The Global Sort feature is designed to enhance the efficiency of `IMPORT INTO` and `CREATE INDEX`. By integrating Global Sort into backend tasks, you can improve stability, control, and scalability. As a result, TiDB offers an enhanced user experience and higher-quality service.

The Global Sort feature provides services for executing tasks within the unified distributed parallel execution framework and ensuring efficient and parallel sorting of data on a global scale.

## Limitations

Currently, the Global Sort feature is not used as a component of the query execution process responsible for sorting query results.

## Usage

1. Before enabling Global Sort, you need to enable the distributed execution framework. To do so, set the value of [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) to `ON`:

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

2. Set [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) to a correct cloud storage path. See [an example](/br/backup-and-restore-storages.md).

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

## Implementation principles

The algorithm of the Global Sort feature is as follows:

![Algorithm of Global Sort](/media/dist-task/global-sort.jpeg)

The detailed implementation principles is as follows:

### Step 1: Scan and prepare data

1. After TiDB nodes scan a specific range of data:

    1. TiDB nodes encode them into Key-Value pairs.
    2. TiDB nodes sort Key-Value pairs into several block data segments, where each segment is one file and is uploaded into the cloud storage.

2. The TiDB node also records a serial actual Key-Value ranges for each segment (referred to as a statistics file), which is a key preparation for scalable sort implementation. These files are then uploaded into the cloud storage along with the real data.

### Step 2: Sort and distribute data

From step 1, the Global Sort program obtains a list of sorted blocks and their corresponding statistics files, which provide the number of locally sorted blocks. The program also has a real data scope that can be used by PD to split and scatter. The following steps are performed:

1. Sort the records in the statistics file to divide them into nearly equal-sized ranges, which are subtasks that will be executed in parallel.
2. Distribute the subtasks to TiDB nodes for execution.
3. Each TiDB node independently sorts the data of subtasks into ranges and ingests them into TiKV without overlap.
