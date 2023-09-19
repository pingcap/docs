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

The global sort feature we introduce enhances the stability and efficiency of the Import and DDL (Data Definition Language) functionality. It serves as a general operator within our distributed parallel execution framework and can also be deployed as a cloud service. Moreover, it supports various shared storage interfaces (e.g., S3, POSIX usage ), facilitating seamless integration with different storage systems. This versatility enables efficient and flexible data sorting operations across diverse use cases.

# Goals and non-goals
## Goals
Implementing this global sort feature facilitates the efficient import into and create index. By incorporating this functionality into backend tasks, we can achieve improved stability, control, and scalability. Ultimately, this enhancement results in a better user experience and higher service quality provided by TiDB. So, in conclusion, the global sort feature will be implemented as an operator within the unified distributed parallel execution framework. This operator will provide services for executing tasks within the framework, ensuring efficient and parallel sorting of data on a global scale.

## Non-goals 
Currently, It will not be utilized as a component of the query execution process responsible for sorting the query results.

## Usage

1. To enable the distributed framework, set the value of [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) to `ON`:

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```
2. Also, need to set [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) to correct cloud storage path.[Example](/br/backup-and-restore-storages.md)
   ```sql
   SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
   ```

## Implementation principles

The Algorithm of the TiDB backend task distributed execution framework is as follows:

![Algorithm of Global Sort](/media/dist-task/global-sort.jpeg)

### Algorithm
Step 1: scan and prepare data
  1. After  TiDB node scans a specific volume of data
    1.  Encodes them into Key-Value pairs.
    2. Sort them into several block data segments, each segment will be one file and be uploaded into S3
  2. Also record a serial Actual Key-Value Distribution for each segment(called statistics file), which is key preparation for scalable sort implementation.  Then upload them into S3 with the real data.
Step 2: From the first step, we got a list of sorted blocks and it correlated statistics file, whick gives us the number of locally sorted blocks. Also, we have a real data scope that could be used by PD to split and scatter. 
  1. Sort statistics file records to cut an almost even range to be subtasks of step2 sort and ingest regions.
  2. Distribute subtasks to TiDB nodes for execution.
  3. All TiDB nodes will independently sort subtask's data into ranges and ingest them into TiKV without overlap.