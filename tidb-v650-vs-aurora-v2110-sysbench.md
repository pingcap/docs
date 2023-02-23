---
title: TiDB Cloud v6.5.0 LTS vs Aurora 2.11.0 sysbench 1T Test Report
---

# TiDB Cloud v6.5.0 LTS vs Aurora 2.11.0 sysbench 1T Test Report

Test time: 2023-01

## Test Summary

- This is a **latency-sensitive** test. We first conduct 10-minute Sysbench tests to obtain the maximum QPS value with a P95 latency under 100ms for each type of workload by adjusting the concurrency. Then, we conduct a formal two-hour test using the corresponding concurrency.
- Price-Performance
  - Regarding price-performance, TiDB proved to be more cost-effective than Aurora in all three test scenarios based on *3-Year Cost($)/QPS*. For the read-write scenario, Aurora costs **2.3-4.6** times more than TiDB. TiDB can provide better performance when both read and write in the same instance. For the read-only scenario, Aurora costs **1.1-2.3** times more than TiDB, while for the write-only scenario, Aurora costs **1.5-4.1** times more than TiDB. 
- Scalability
  - TiDB has a scalability of over 100%, which is better than Aurora.
- In this test, the IO cost of Aurora accounts for **79%** to **82%** of the total cost, while TiDB's data transfer fees represent 22%-62% of the total expenses.

## Test Configuration
### Configuration of Aurora

| Instance class     | vCPU | ECU | Memory (GiB) | Max. bandwidth (mbps) of local storage | Network performance | Instance Price Per Hour |
|--------------------|------|-----|--------------|----------------------------------------|---------------------|------------------------------|
| db.r5.8xlarge      | 32   | 132 | 256          | 6,800                                  | 10 Gbps             | 4.46                         |
| db.r5.4xlarge | 16   | 71  | 128          | 4,750                                  | Up to 10 Gbps       | 2.32                         |

- Region：us-west-2 
- Version: Aurora (MySQL 5.7) 2.11.0 [[Released on 2022-10-25](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraMySQLReleaseNotes/AuroraMySQL.Updates.2110.html)]
- DB instance Class:
  - Memory optimized classes (includes r classes)
- Availability & durability
  - Multi-AZ deployments: Create an Aurora Reader node in a different AZ 
- Additional configuration
  - DB cluster parameter group/DB parameter group 
    - Create DB cluster parameter group/DB parameter group from  the parameter group named default.aurora-mysql5.7 
    - set max_prepared_stmt_count=1048576 

### Configuration of TiDB

| Cloud Provider | Region | TiDB Node Size (vCPU + RAM) | TiDB Node Quantity | TiKV Node Size (vCPU + RAM) | TiKV Node Quantity | TiKV Node Storage | Dedicated Tier hourly Cost($) |
|----------------|-------------------------|-----------------------------|--------------------|-----------------------------|--------------------|-------------------|-------------------------------|
| GCP            | Oregon (us-west1)       | 16 vCPU, 32 GiB             | 2                  | 16 vCPU, 64 GiB        | 3                  | 1500 GiB          | 9.5007                        |
| GCP            | Oregon (us-west1)       | 16 vCPU, 32 GiB             | 4                  | 16 vCPU, 64 GiB             | 6                  | 1500 GiB          | 19.0014                       |
| AWS            | Oregon (us-west-2) | 16 vCPU, 32 GiB             | 2                  | 16 vCPU, 64 GiB       | 3                  | 1500 GiB          | 9.0836                        |
| AWS            | Oregon (us-west-2)      | 16 vCPU, 32 GiB             | 4                  | 16 vCPU, 64 GiB             | 6                  | 1500 GiB          | 18.1673                       |

- Version:  v6.5.0 [Released on 2022-12-29] 
- System Variables 
  ```
  set global tidb_prepared_plan_cache_size=1000;
  ```

### Configuration of Sysbench
- AWS EC2 instance: m5.2xlarge (CentOS 7)
- GCP Compute Engine VM instance: n2-standard-8 (CentOS 7)
- Version: sysbench 1.1.0-df89d34 (using bundled LuaJIT 2.1.0-beta3)  

## Workloads
Sysbench

| workload name   | workload type | read/write ratio           | #table | table_size  | data size |
|-----------------|---------------|----------------------------|--------|-------------|-----------|
| oltp_read_only  | read-heavy    | Read (100%) and write (0%) | 50     | 100,000,000 | ~ 1 TB    |
| oltp_write_only | write-heavy   | Read (0%) and write (100%) | 50     | 100,000,000 | ~ 1 TB    |
| oltp_read_write | mixed         | Read (75%) and write (25%) | 50     | 100,000,000 | ~ 1 TB    |

## Test Steps
### Test plan for Aurora
1. Deploy an Aurora cluster and a m5.2xlarge EC2 instance for sysbench client on the AWS console
2. Use Sysbench to import 50 tables, each table with 100 million rows of data.
3. Take a snapshot of the cluster for restoration before the tests, ensuring consistency for each test.
4. Execute the `analyze table` statement on each table before each test.
5. Start the Sysbench client to perform the `read_only`, `read_write`, and `write_only` tests. For each workload, the test takes 2 hours.
6. Gathering and analyzing test results.
7. After each type of test, terminate the cluster, and create a new cluster from the snapshot created before.
### Test plan for TiDB
1. Deploy a TiDB cluster on TiDB Cloud console
2. Deploy a m5.2xlarge EC2 (AWS)/ n2-standard-8 Compute Engine VM (GCP) instance and set up VPC Peering with TiDB Cloud
3. Use Sysbench to import 50 tables, each table with 100 million rows of data.
4. Back up the data before the tests for restoration, ensuring consistency for each test.
5. Execute the `analyze table` statement on each table before each test.
6. Start the Sysbench client to perform the `read_only`, `read_write`, and `write_only` tests. Perform stress tests on TiDB Cloud. For each workload, the test takes 2 hours.
7. Gathering and analyzing test results.
8. After each type of test, delete the cluster, and create a new cluster from the backup created before.

#### Install sysbench
```
sudo yum -y install git make automake libtool pkgconfig libaio-devel openssl-devel mysql-devel yum-utils;
cd /tmp/; 
git clone https://github.com/akopytov/sysbench.git;
cd sysbench;
sudo ./autogen.sh;
sudo ./configure;
sudo make -j;
sudo make install
```
#### Prepare test data
Run the following command to prepare the test data:
```
sysbench oltp_common --report-interval=20 --rand-type=uniform --mysql-db=sbtest \
--mysql-host=${host} --mysql-port=${port}  --mysql-user=${user} \
--mysql-password=${password} --threads=50 --tables=50 --table-size=100000000 prepare 
```
#### Gather statistics
Run the following command to gather statistics before each test. To speed up the statistics collection in TiDB, `set tidb_build_stats_concurrency=16; set tidb_index_serial_scan_concurrency=15;` 

```
set tidb_build_stats_concurrency=16; 
set tidb_index_serial_scan_concurrency=15; 
ANALYZE TABLE sbtest.sbtest1; 
ANALYZE TABLE sbtest.sbtest2; 
ANALYZE TABLE sbtest.sbtest3; 
ANALYZE TABLE sbtest.sbtest4; 
...
ANALYZE TABLE sbtest.sbtest47; 
ANALYZE TABLE sbtest.sbtest48; 
ANALYZE TABLE sbtest.sbtest49; 
ANALYZE TABLE sbtest.sbtest50;
```

Perform the test
Run the following command to perform the tests:
```
sysbench ${testname} run --time=7200 --threads=${threads} \
--report-interval=10 --rand-type=uniform --mysql-db=sbtest \
--mysql-host=${host} --mysql-port=${port}  --mysql-user=${user} \
--mysql-password=${password} --tables=50 --table-size=100000000 \
--mysql-ignore-errors=1062,2013,8028,9007 
```

## Test Results
### Price-Performance
- For Aurora, *Instance Cost (writer+reader)/hour (\$)* is the total cost of a Writer instance + a Reader instance. *Other cost/hour ($)* is mainly the storage cost.
- For TiDB, *Instance Cost (writer+reader)/hour ($)* is the total cost of TiDB cost + TiKV cost (including storage cost).
### oltp_read_only

| Instance_type                          | Aurora.r5.4xlarge | 2 TiDB + 3 TiKV (AWS) | 2 TiDB + 3 TiKV (GCP) | Aurora.r5.8xlarge | 4 TiDB + 6 TiKV (AWS) | 4 TiDB + 6 TiKV (GCP) |
|----------------------------------------|-------------------|-----------------------|-----------------------|-------------------|-----------------------|-----------------------|
| Max QPS                                | 42603.36          | 35776.41              | 44299.66              | 66337.71          | 92004.2               | 107443.25             |
| 3-Year Cost($)/QPS                     | 16.32             | 15.52                 | 9.07                  | 18.39             | 13.83                 | 7.94                  |
| 3-Year Cost($)                         | 695,493.51        | 555,128.21            | 401,971.00            | 1,220,180.40      | 1,272,406.64          | 852,822.79            |
| Total Cost/hour ($)                    | 26.46             | 21.12                 | 15.30                 | 46.43             | 48.42                 | 32.45                 |
| Instance Cost (writer+reader)/hour ($) | 4.64              | 9.08                  | 9.50                  | 9.28              | 18.17                 | 19.00                 |
| IO Cost/hour ($)                       | 21.67             | 0.00                  | 0.00                  | 37.00             | 0.00                  | 0.00                  |
| Data Transfer Cost/hour ($)            | 0.00              | 12.04                 | 5.80                  | 0.00              | 30.25                 | 13.45                 |
| Other cost/hour ($)                    | 0.15              | 0.00                  | 0.00                  | 0.15              | 0.00                  | 0.00                  |
| P95 latency                            | 89.16             | 101.13                | 74.46                 | 94.1              | 97.55                 | 90.78                 |
| Threads                                | 200               | 150                   | 150                   | 300               | 350                   | 350                   |
| IO Cost/Total Cost                     | 82%               | 0%                    | 0%                    | 80%               | 0%                    | 0%                    |
| Data Transfer Cost/Total Cost          | 0%                | 57%                   | 38%                   | 0%                | 62%                   | 41%                   |

![Read Only](/media/tidb-cloud/sysbench_tidb_v650_vs_aurora_v2110_oltp_read_only.png)



#### oltp_read_write

| Instance_type                          | Aurora.r5.4xlarge | 2 TiDB + 3 TiKV (AWS) | 2 TiDB + 3 TiKV (GCP) | Aurora.r5.8xlarge | 4 TiDB + 6 TiKV (AWS) | 4 TiDB + 6 TiKV (GCP) |
|----------------------------------------|-------------------|-----------------------|-----------------------|-------------------|-----------------------|-----------------------|
| Max QPS                                | 16616.10          | 31650.91              | 44731.08              | 36500.84          | 76056.7               | 105899.96             |
| 3-Year Cost($)/QPS                     | 42.37             | 16.28                 | 9.17                  | 33.07             | 14.27                 | 8.31                  |
| 3-Year Cost($)                         | 704,041.20        | 515,314.01            | 410,117.80            | 1,207,040.40      | 1,085,493.63          | 880,416.79            |
| Total Cost/hour ($)                    | 26.79             | 19.61                 | 15.61                 | 45.93             | 41.30                 | 33.50                 |
| Instance Cost (writer+reader)/hour ($) | 4.64              | 9.08                  | 9.50                  | 9.28              | 18.17                 | 19.00                 |
| IO Cost/hour ($)                       | 22.00             | 0.00                  | 0.00                  | 36.50             | 0.00                  | 0.00                  |
| Data Transfer Cost/hour ($)            | 0.00              | 10.53                 | 6.11                  | 0.00              | 23.14                 | 14.50                 |
| Other cost/hour ($)                    | 0.15              | 0.00                  | 0.00                  | 0.15              | 0.00                  | 0.00                  |
| P95 latency                            | 84.47             | 127.81                | 89.16                 | 108.68            | 87.56                 | 92.42                 |
| Threads                                | 50                | 150                   | 150                   | 150               | 250                   | 350                   |
| IO Cost/Total Cost                     | 82%               | 0%                    | 0%                    | 79%               | 0%                    | 0%                    |
| Data Transfer Cost/Total Cost          | 0%                | 54%                   | 39%                   | 0%                | 56%                   | 43%                   |

![Read Only](/media/tidb-cloud/sysbench_tidb_v650_vs_aurora_v2110_oltp_read_write.png)



#### oltp_write_only
| Instance_type                          | Aurora.r5.4xlarge | 2 TiDB + 3 TiKV (AWS) | 2 TiDB + 3 TiKV (GCP) | Aurora.r5.8xlarge | 4 TiDB + 6 TiKV (AWS) | 4 TiDB + 6 TiKV (GCP) |
|----------------------------------------|-------------------|-----------------------|-----------------------|-------------------|-----------------------|-----------------------|
| QPS                                    | 10799.79          | 26263.04              | 25996.86              | 71959.07          | 63447.54              | 58223.45              |
| 3-Year Cost($)/QPS                     | 51.81             | 15.18                 | 12.46                 | 18.05             | 12.81                 | 11.02                 |
| 3-Year Cost($)                         | 559,501.20        | 398,762.21            | 323,919.40            | 1,299,020.40      | 813,032.24            | 641,400.19            |
| Total Cost/hour ($)                    | 21.29             | 15.17                 | 12.33                 | 49.43             | 30.94                 | 24.41                 |
| Instance Cost (writer+reader)/hour ($) | 4.64              | 9.08                  | 9.50                  | 9.28              | 18.17                 | 19.00                 |
| IO Cost/hour ($)                       | 16.50             | 0.00                  | 0.00                  | 40.00             | 0.00                  | 0.00                  |
| Data Transfer Cost/hour ($)            | 0.00              | 6.09                  | 2.83                  | 0.00              | 12.77                 | 5.41                  |
| Other cost/hour ($)                    | 0.15              | 0.00                  | 0.00                  | 0.15              | 0.00                  | 0.00                  |
| P95 latency                            | 74.46             | 97.55                 | 99.33                 | 80.03             | 92.42                 | 127.81                |
| Threads                                | 100               | 350                   | 350                   | 900               | 700                   | 700                   |
| IO Cost/Total Cost                     | 78%               | 0%                    | 0%                    | 81%               | 0%                    | 0%                    |
| Data Transfer Cost/Total Cost          | 0%                | 40%                   | 23%                   | 0%                | 41%                   | 22%                   |


![Read Only](/media/tidb-cloud/sysbench_tidb_v650_vs_aurora_v2110_oltp_write_only.png)