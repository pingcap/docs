---
title: TiDB Global Sort
summary: Learn the use cases, limitations, usage, and implementation principles of the TiDB Global Sort.
---

<!-- markdownlint-disable MD029 -->
<!-- markdownlint-disable MD046 -->

# TiDB Global Sort

> **Note:**
>
> - Currently, the Global Sort process consumes a large amount of computing and memory resources of TiDB nodes. In scenarios such as adding indexes online while user business applications are running, it is recommended to add new TiDB nodes to the cluster, configure the [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) variable for these nodes, and connect to these nodes to create tasks. In this way, the distributed framework schedules tasks to these nodes, isolating the workload from other TiDB nodes to reduce the impact of executing backend tasks such as `ADD INDEX` and `IMPORT INTO` on user business applications.
> - When the Global Sort feature is used, it is recommended to use TiDB nodes with at least 16 cores of CPU and 32 GiB of memory to avoid OOM.

> **Note:**
>
> This feature is not available on [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## Overview

The TiDB Global Sort feature enhances the stability and efficiency of data import and DDL (Data Definition Language) operations. It serves as a general operator in the [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md), providing a global sort service on cloud.

Currently, the Global Sort feature supports using Amazon S3 as cloud storage.

## Use cases

The Global Sort feature enhances the stability and efficiency of `IMPORT INTO` and `CREATE INDEX`. By globally sorting the data that are processed by the tasks, it improves the stability, controllability, and scalability of writing data to TiKV. This provides an enhanced user experience for data import and DDL tasks, as well as higher-quality services.

The Global Sort feature executes tasks within the unified DXF, ensuring efficient and parallel sorting of data on a global scale.

## Limitations

Currently, the Global Sort feature is not used as a component of the query execution process responsible for sorting query results.

## Usage

To enable Global Sort, follow these steps:

1. Enable the DXF by setting the value of [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) to `ON`. Starting from v8.1.0, this variable is enabled by default. For newly created clusters of v8.1.0 or later versions, you can skip this step.

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

<CustomContent platform="tidb">

2. Set [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) to a correct cloud storage path. See [an example](/br/backup-and-restore-storages.md).

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

</CustomContent>
<CustomContent platform="tidb-cloud">

2. Set [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) to a correct cloud storage path. See [an example](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages).

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

</CustomContent>

> **Note:**
>
> For [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md), you can also specify the cloud storage path using the [`CLOUD_STORAGE_URI`](/sql-statements/sql-statement-import-into.md#withoptions) option. If both [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) and `CLOUD_STORAGE_URI` are configured with a valid cloud storage path, the configuration of `CLOUD_STORAGE_URI` takes effect for [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md).

## Implementation principles

The algorithm of the Global Sort feature is as follows:

![Algorithm of Global Sort](/media/dist-task/global-sort.jpeg)

The detailed implementation principles are as follows:

### Step 1: Scan and prepare data

1. After TiDB nodes scan a specific range of data (the data source can be either CSV data or table data in TiKV):

    1. TiDB nodes encode them into Key-Value pairs.
    2. TiDB nodes sort Key-Value pairs into several block data segments (the data segments are locally sorted), where each segment is one file and is uploaded into the cloud storage.

2. The TiDB node also records a serial actual Key-Value ranges for each segment (referred to as a statistics file), which is a key preparation for scalable sort implementation. These files are then uploaded into the cloud storage along with the real data.

### Step 2: Sort and distribute data

From step 1, the Global Sort program obtains a list of sorted blocks and their corresponding statistics files, which provide the number of locally sorted blocks. The program also has a real data scope that can be used by PD to split and scatter. The following steps are performed:

1. Sort the records in the statistics file to divide them into nearly equal-sized ranges, which are subtasks that will be executed in parallel.
2. Distribute the subtasks to TiDB nodes for execution.
3. Each TiDB node independently sorts the data of subtasks into ranges and ingests them into TiKV without overlap.
