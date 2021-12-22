---
title: DM 2.0-GA Benchmark Report
summary: Learn about the performance of DM 2.0-GA.
---

# DM 2.0-GA Benchmark Report

This benchmark report describes the test purpose, environment, scenario, and results for DM 2.0-GA.

## Test purpose

The purpose of this test is to evaluate the performance of DM full import and incremental replication and to conclude recommended configurations for DM migration tasks based on the test results.

## Test environment

### Machine information

System information:

| Machine IP  | Operating System           | Kernel version           | File system type |
| :---------: | :---------------------------: | :-------------------: | :--------------: |
| 172.16.5.32 | CentOS Linux release 7.8.2003 | 3.10.0-957.el7.x86_64 | ext4             |
| 172.16.5.33 | CentOS Linux release 7.8.2003 | 3.10.0-957.el7.x86_64 | ext4             |
| 172.16.5.34 | CentOS Linux release 7.8.2003 | 3.10.0-957.el7.x86_64 | ext4             |
| 172.16.5.35 | CentOS Linux release 7.8.2003 | 3.10.0-957.el7.x86_64 | ext4             |
| 172.16.5.36 | CentOS Linux release 7.8.2003 | 3.10.0-957.el7.x86_64 | ext4             |
| 172.16.5.37 | CentOS Linux release 7.8.2003 | 3.10.0-957.el7.x86_64 | ext4             |

Hardware information:

| Type         | Specification                                       |
| :----------: | :-------------------------------------------------: |
| CPU          | Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz, 40 Cores |
| Memory       | 128G, 8 * 16GB DIMM DDR4 2133 MHz                   |
| Disk         | Intel SSD DC P4800X 375G NVMe * 2                   |
| Network card | 10 Gigabit Ethernet                                 |

Others:

* Network rtt between servers: rtt min/avg/max/mdev = 0.074/0.116/0.158/0.042 ms

### Cluster topology

| Machine IP  | Deployed instance                |
| :---------: | :--------------------------------: |
| 172.16.5.32 | PD1, DM-worker1, DM-master         |
| 172.16.5.33 | PD2, MySQL1                        |
| 172.16.5.34 | PD3, TiDB                          |
| 172.16.5.35 | TiKV1(nvme0n1), TiKV2(nvme1n1)     |
| 172.16.5.36 | TiKV3(nvme0n1), TiKV4(nvme1n1)     |
| 172.16.5.37 | TiKV5(nvme0n1), TiKV6(nvme1n1)     |

### Version information

- MySQL version: 5.7.31-log
- TiDB version: v4.0.7
- DM version: v2.0.0
- Sysbench version: 1.0.17

## Test scenario

You can use a simple data migration flow, that is, MySQL1 (172.16.5.33) -> DM-worker(172.16.5.32) -> TiDB (172.16.5.34), to do the test. For detailed test scenario description, see [performance test](/dm/dm-performance-test.md).

### Full import benchmark case

For detailed full import test method, see [Full Import Benchmark Case](/dm/dm-performance-test.md#full-import-benchmark-case).

#### Full import benchmark results

To enable multi-thread concurrent data export via Dumpling, you can configure the `threads` parameter in the `mydumpers` configuration item. This speeds up data export.

| Item       | Data size (GB)  | Threads  | Rows    | Statement-size  | Time (s)  | Dump speed (MB/s)   |
| :----------: | :---------: |:-------: | :-----: | :-------------: | :----------: | :---------------: |
| dump data    | 38.1       | 32       | 320000   | 1000000         | 106.73       | 359.43           |

| Item    | Data size (GB)  | Pool size | Statement per TXN | Max latency of TXN execution (s) | Time (s) | Import speed (MB/s) |
| :-------: | :--------: | :-------: | :-------------------: | :----------------: | :----------: | :-------------: |
| load data | 38.1       | 32        | 4878                  | 20.95              | 1580.54       | 24.11          |

#### Benchmark results with different pool sizes in load unit

In this test, the full amount of data imported using `sysbench` is 3.78 GB. The following is detailed information of the test data:

| load unit pool size| Max latency of TXN execution (s) | Import time (s) | Import Speed (MB/s) | TiDB 99 duration (s) |
| :---------------------: | :---------------: | :----------: | :-------------: | :------------------: |
| 2                       | 0.35              | 438         | 8.63             | 0.32                 |
| 4                       | 0.65              | 305         | 12.30            | 0.55                 |
| 8                       | 1.82              | 231         | 16.36            | 2.26                 |
| 16                      | 3.46              | 228         | 16.57            | 3.04                 |
| 32                      | 5.92              | 208         | 18.17            | 6.56                 |
| 64                      | 8.59              | 221         | 17.10            | 9.62                 |

#### Benchmark results with different row count per statement

In this test, the full amount of imported data is 3.78 GB and the `pool-size` of load unit is set to 32. The statement count is controlled by `statement-size`, `rows`, or `extra-args` parameters in the `mydumpers` configuration item.

| Row count per statement       | mydumpers extra-args | Max latency of TXN execution (s) | Import time (s) | Import speed (MB/s) | TiDB 99 duration (s) |
| :------------------------: | :-----------------------: | :--------------: | :----------: | :-------------: | :------------------: |
|            7506            | -s 1500000 -r 320000      |   8.74           |  218         |     17.3        |        10.49         |
|            5006            | -s 1000000 -r 320000      |   5.92           |  208         |     18.1        |         6.56         |
|            2506            | -s 500000 -r 320000       |   3.07           |  222         |     17.0        |         2.32         |
|            1256            | -s 250000 -r 320000       |   2.01           |  230         |     16.4        |         1.87         |
|            629             | -s 125000 -r 320000       |   0.98           |  241         |     15.6        |         0.94         |
|            315             | -s 62500 -r 320000        |   0.51           |  245         |     15.4        |         0.45         |

### Incremental replication benchmark case

For detailed incremental replication test method, see [Incremental Replication Benchmark Case](/dm/dm-performance-test.md#incremental-replication-benchmark-case).

#### Incremental replication benchmark result

In this test, the `worker-count` of sync unit is set to 32 and `batch` is set to 100.

| Items                       | QPS                | TPS                          | 95% latency                     |
| :------------------------: | :----------------------------------------------------------: | :-------------------------------------------------------------: | :--------------------------: |
| MySQL                      | 38.65k                                                       | 38.65k                                                          | 1.10ms                       |
| DM binlog replication unit | 21.33k (The number of binlog events received per unit of time, not including skipped events)              | -                                                               | 66.75ms (txn execution time)          |
| TiDB                       | 21.90k (Begin/Commit 2.32k Insert 21.35k)                    | 3.52k                                                           | 95%: 5.2ms 99%: 8.3ms          |

#### Benchmark results with different sync unit concurrency

| sync unit worker-count | DM QPS           | Max DM execution latency (ms)   | TiDB QPS | TiDB 99 duration (ms) |
| :---------------------------: | :-------------: | :-----------------------: | :------: | :-------------------: |
| 4                             | 11.83k           | 56                       | 12.1k    | 4                     |
| 8                             | 18.34k           | 58                       | 18.9k    | 5                     |
| 16                            | 20.85k           | 60                       | 21.6k    | 6                     |
| 32                            | 21.33k           | 66                       | 21.9k    | 8                     |
| 64                            | 21.52k           | 68                       | 22.1k    | 10                    |
| 1024                          | 20.45k           | 85                       | 50.5k    | 52                    |

#### Benchmark results with different SQL distribution

| Sysbench type| DM QPS | Max DM execution latency (ms) | TiDB QPS | TiDB 99 duration (ms) |
| :--------------: | :-------------: | :------------------: | :------: | :-------------------: |
| insert_only      | 21.33k          | 66                   | 21.9k    | 8                    |
| write_only       | 10.2k           | 87                  | 11.2k     | 8                    |

## Recommended parameter configuration

### dump unit

We recommend that the statement size be 200 KB~1 MB, and row count in each statement be approximately 1000~5000, which is based on the actual row size in your scenario.

### load unit

We recommend that you set `pool-size` to 16.

### sync unit

We recommend that you set `batch` to 100 and `worker-count` to 16~32.
