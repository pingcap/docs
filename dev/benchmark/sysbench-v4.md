---
title: TiDB Sysbench Performance Test Report -- v3.0 vs. v2.1
category: benchmark
---

# TiDB Sysbench Performance Test Report -- v3.0 vs. v2.1

## Test purpose

This test aims to compare the performance of TiDB 3.0 and TiDB 2.1 in the OLTP scenario.

## Test version, time, and place

TiDB version: v3.0.0-rc.2 vs. v2.1.8

Time: June, 2019

Place: Beijing

## Test environment

This test runs on AWS EC2 and uses the CentOS-7.6.1810-Nitro (ami-028946f4cffc8b916) image. The components and types of instances are as follows:

| Component  |  Instance type  |
| :--- | :-------- |
|  PD   | r5d.xlarge |
| TiKV  | c5d.xlarge |
| TiDB  | c5d.xlarge |

Sysbench version: 1.0.17

## Test plan

Use Sysbench to import **16 tables, with 10,000,000 pieces of data in each table**. Start three sysbench to add pressure to three TiDB instances. The number of concurrent requests increases incrementally. A single concurrent test lasts 5 minutes.

Prepare data using the following command:

```sh
sysbench oltp_common \
    --threads=16 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    prepare --tables=16 --table-size=10000000
```

Then test TiDB using the following command:

```sh
sysbench $testname \
    --threads=$threads \
    --time=300 \
    --report-interval=15 \
    --rand-type=uniform \
    --rand-seed=$RANDOM \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    run --tables=16 --table-size=10000000
```

### TiDB version information

### v3.0.0-rc.2

| Component  |                 GitHash                |
| :--- | :-------------------------------------- |
| TiDB  | `e5dcc9b354dfa3b6b3a34cbd5949b2bec56b5bea` |
| TiKV  | `59a0f2b1dd45baea9bfdb4aab69b50fdbded08af` |
|  PD   | `c44ddf4abaaf54bcc99955b787bfe26b35fcfe8e` |

### v2.1.8

| Component  |                 GitHash                  |
| :--- | :-------------------------------------- |
| TiDB  | `9a2d2da372947a50a02f9b9238a49f2db7ab9971` |
| TiKV  | `f58ed66cee9a10d605e56c878b1bf91c7b711a54` |
|  PD   | `1961ce08dcdead4198fa23a7ed079b135768c206` |

### TiDB parameter configuration

Configure the global variable in both TiDB v2.1 and v3.0:

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
```

In addition, the following configuration is made in v3.0:

```toml
[prepared-plan-cache]
enabled = true
[tikv-client]
max-batch-wait-time = 1000000
```

### TiKV parameter configuration

Configure the global variable in both TiDB v2.1 and v3.0:

```toml
[readpool.storage]
normal-concurrency = 12
[server]
grpc-concurrency = 8
```

In addition, the following configuration is made in v3.0:

```toml
[raftstore]
apply-pool-size = 4
store-pool-size = 4
```

### Cluster topology

|                 Machine IP                  |  Deployment instance  |
| :-------------------------------------- | :--------- |
|               172.31.25.16               | 3\*Sysbench |
| 172.31.10.75, 172.31.3.211, 172.31.11.12 |     PD      |
| 172.31.8.167, 172.31.6.107, 172.31.14.99 |    TiKV     |
|  172.31.1.94, 172.31.15.193, 172.31.2.6  |    TiDB     |

## Test result

### `Point Select` test

**v2.1:**

| Threads |    QPS    | 95% latency(ms) |
| :------- | :-------- | :-------------- |
| 150     | 137171.43 |            1.25 |
| 300     | 221861.81 |            2.00 |
| 600     | 266727.44 |            4.25 |
| 900     | 282689.31 |            6.32 |
| 1200    | 290614.52 |            8.43 |
| 1500    | 296218.09 |           10.27 |

**v3.0:**

| Threads |    QPS    | 95% latency(ms) |
| :------- | :-------- | :-------------- |
| 150     | 158908.53 |            1.04 |
| 300     | 279335.92 |            1.30 |
| 600     | 422278.72 |            2.11 |
| 900     | 484304.54 |            3.07 |
| 1200    | 502705.22 |            4.10 |
| 1500    | 509098.83 |            5.18 |

![point select](/media/sysbench_v4_point_select.png)

### `Update Non-Index` test

**v2.1:**

| Threads |   QPS    | 95% latency (ms) |
| :------- | :------- | :-------------- |
| 150     | 20755.37 |            8.90 |
| 300     | 27598.11 |           14.21 |
| 600     | 32072.08 |           33.12 |
| 900     | 32503.02 |           56.84 |
| 1200    | 32361.03 |           90.78 |
| 1500    | 32393.35 |          116.80 |

**v3.0:**

| Threads |   QPS    | 95% latency (ms) |
| :------- | -------: | --------------: |
| 150     | 24710.00 |            8.43 |
| 300     | 30347.88 |           13.95 |
| 600     | 38685.87 |           23.52 |
| 900     | 45567.08 |           30.81 |
| 1200    | 49982.75 |           39.65 |
| 1500    | 55717.09 |           51.02 |

![update non-index](/media/sysbench_v4_update_non_index.png)

### `Update Index` test

**v2.1:**

| Threads |   QPS    | 95% latency(ms) |
| ------- | -------: | --------------: |
| 150     | 13167.36 |           14.73 |
| 300     | 14670.16 |           31.94 |
| 600     | 15508.57 |           75.82 |
| 900     | 16290.25 |          116.80 |
| 1200    | 16060.43 |          164.45 |
| 1500    | 16219.86 |          204.11 |

**v3.0:**

| Threads |   QPS    | 95% latency(ms) |
| ------- | -------: | --------------: |
| 150     | 15202.94 |           13.46 |
| 300     | 18874.35 |           23.52 |
| 600     | 23882.45 |           40.37 |
| 900     | 25602.60 |           63.32 |
| 1200    | 25340.77 |          104.84 |
| 1500    | 26294.65 |          155.80 |

![update index](/media/sysbench_v4_update_index.png)

### `Read Write` test

**v2.1:**

| Threads |   TPS   |   QPS    | 95% latency(ms) |
| ------- | ------: | -------: | --------------: |
| 150     | 3182.82 | 63656.28 |           57.87 |
| 300     | 3828.92 | 76578.28 |          101.13 |
| 600     | 4304.55 | 86091.07 |          183.21 |
| 900     | 4527.28 | 90545.70 |          272.27 |
| 1200    | 4726.97 | 94539.33 |          350.33 |
| 1500    | 4869.35 | 97386.99 |          427.07 |

**v3.0:**

| Threads |   TPS   |    QPS    | 95% latency(ms) |
| ------- | ------: | --------: | --------------: |
| 150     | 3703.97 |  74079.43 |           50.11 |
| 300     | 4890.35 |  97806.84 |           77.19 |
| 600     | 5644.47 | 112889.45 |          142.39 |
| 900     | 6095.21 | 121904.23 |          204.11 |
| 1200    | 6168.28 | 123365.48 |          267.41 |
| 1500    | 6429.45 | 128589.10 |          314.45 |

![read write](/media/sysbench_v4_read_write.png)
