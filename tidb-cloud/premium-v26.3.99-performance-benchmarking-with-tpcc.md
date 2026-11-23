---
title: TiDB Cloud Premium TPC-C Performance Report v26.3.99
summary: Explore the TPC-C test environment, procedures, and performance results for TiDB Cloud Premium v26.3.99 on AWS Graviton4.
---

# TiDB Cloud Premium TPC-C Performance Report v26.3.99

This document provides the TPC-C performance test steps and results for TiDB Cloud Premium v26.3.99.

## Test overview

These tests demonstrate the TPC-C performance of TiDB Cloud Premium v26.3.99 in online transaction processing (OLTP) scenarios.

## Test environment

### TiDB cluster

The tests were conducted on a TiDB Cloud Premium cluster with the following settings:

- Cluster version: v26.3.99
- Cloud provider and region: AWS (us-west-2)
- Instance platform: AWS Graviton4
- Request Capacity Units (RCUs): 500,000
- Cluster configuration:

    | Node type | Node size | Instance family | Node quantity | Node storage |
    | --- | --- | --- | --- | --- |
    | TiDB | 16 vCPU, 32 GB | m8g | 2 | N/A |
    | TiKV | 16 vCPU, 64 GB | m8g | 3 | 500 GB |
    | PD | 4 vCPU, 8 GB | c8g | 3 | N/A |

For the 400-thread test, the cluster used four TiDB nodes. The 100-thread and 200-thread tests used two TiDB nodes.

### Parameter configuration

For each workload, the system variable [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) was set to `1000`:

```sql
SET GLOBAL tidb_session_plan_cache_size = 1000;
```

### Benchmark executor

The benchmark executor sends SQL queries to the TiDB cluster. The executor used in these tests was a single machine with 12 vCPUs and 24 GB of memory.

## Test steps

The tests used [go-tpc](https://github.com/pingcap/go-tpc) with 1,000 warehouses.

1. In the [TiDB Cloud console](https://tidbcloud.com/), create a TiDB Cloud Premium cluster that meets the [test environment](#test-environment) requirements.
2. Use BR to restore the test data to the `tpcc` database, and wait until the Regions are healthy.
3. Run `ANALYZE TABLE` to collect statistics for the test tables, and warm up the cluster.
4. Run the following command to stress test the cluster. Replace `${HOST}` and `${PASSWORD}` with your actual values. Set `${THREAD}` to `100`, `200`, and `400` in separate tests. Each test at a given concurrency level lasts two hours.

    ```shell
    go-tpc tpcc --host ${HOST} -P 4000 --warehouses 1000 run -D tpcc -T ${THREAD} --time 2h0m0s -p ${PASSWORD} --ignore-error
    ```

5. Extract the tpmC value for `NEW_ORDER` from the results.

    The tpmC metric measures the number of NewOrder transactions processed per minute.

## Test results

For the 400-thread test, the cluster was scaled out to four TiDB nodes because the workload saturated the resources of two TiDB nodes.

| Threads | tpmC |
| --- | --- |
| 100 | 81,495.90 |
| 200 | 132,529.40 |
| 400 (4 TiDB nodes) | 215,619.60 |

![TPC-C performance](/media/tidb-cloud/premium-v26.3.99-tpcc.png)
