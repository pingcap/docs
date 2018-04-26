---
title: TiDB TPC-H 50G Performance Test Report V2.0
category: benchmark
draft: true
---

# TiDB TPC-H 50G Performance Test Report

## Test purpose

The test aims at comparing the performance between TiDB v1.0 and v2.0 in OLAP scenario.

> **Note**: Different test environments may lead to different test results.

## Test environment

### Machine hardware information

| Type       |  Name                                                |
|------------|------------------------------------------------------|
| OS         | linux (CentOS 7.3.1611)                              |
| CPU        | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz  |
| RAM        | 128GB                                                |
| DISK       | 1.5T SSD * 2  + Optane SSD * 1                       |

### TPC-H

[tidb-bench/tpch](https://github.com/pingcap/tidb-bench/tree/master/tpch)

### Cluster topology

| Machine IP   | Deployment Instance |
|--------------|---------------------|
| 172.16.31.2  | TiKV \* 2           |
| 172.16.31.3  | TiKV \* 2           |
| 172.16.31.6  | TiKV \* 2           |
| 172.16.31.8  | TiKV \* 2           |
| 172.16.31.10 | TiKV \* 2           |
| 172.16.31.10 | PD \* 1             |
| 172.16.31.4  | TiDB \* 1           |

### Corresponding TiDB version information

TiDB 1.0：

| Component | Version | Commit Hash                                 |
|--------|-------------|--------------------------------------------|
| TiDB   | v1.0.9      | 4c7ee3580cd0a69319b2c0c08abdc59900df7344   |
| TiKV   | v1.0.8      | 2bb923a4cd23dbf68f0d16169fd526dc5c1a9f4a   |
| PD     | v1.0.8      | 137fa734472a76c509fbfd9cb9bc6d0dc804a3b7   |

TiDB 2.0：

| Component | Version      | Commit Hash                            |
|--------|-------------|--------------------------------------------|
| TiDB   | v2.0.0-rc.6 | 82d35f1b7f9047c478f4e1e82aa0002abc8107e7   |
| TiKV   | v2.0.0-rc.6 | 8bd5c54966c6ef42578a27519bce4915c5b0c81f   |
| PD     | v2.0.0-rc.6 | 9b824d288126173a61ce7d51a71fc4cb12360201   |

## Test result

| Query ID	| TiDB 2.0 	         | TiDB 1.0         |
|-----------|--------------------|------------------|
| 1	        | 33.9154210091s	 | 215.305725098s   |
| 2	        | 25.5757238865s	 | Nan              |
| 3	        | 59.6319231987s	 | 196.003419161s   |
| 4	        | 30.2346801758s	 | 249.919836998s   |
| 5	        | 31.6665229797s	 | OOM              |
| 6	        | 13.1118650436s	 | 118.709993839s   |
| 7	        | 31.7108299732s	 | OOM              |
| 8	        | 31.7343668938s	 | 800.546444893s   |
| 9	        | 34.2111070156s	 | 630.639750004s   |
| 10	    | 30.7746679783s	 | 133.547474861s   |
| 11	    | 27.6926951408s	 | 78.0269281864s   |
| 12	    | 27.9628179073s	 | 124.641829014s   |
| 13	    | 27.6760618687s	 | 174.695388079s   |
| 14	    | 19.6767029762s	 | 110.602974892s   |
| 15	    | NaN	             | Nan              |
| 16	    | 24.8907389641s	 | 40.5292630196s   |
| 17	    | 245.796802998s	 | NaN              |
| 18	    | 91.2561578751s	 | OOM              |
| 19	    | 37.6150860786s	 | NaN              |
| 20	    | 44.1677880287s	 | 212.201659918s   |
| 21	    | 31.4664649963s	 | OOM              |
| 22	    | 31.5397689342s	 | 125.471378088s   |

It should be notified that:

- Queries 15 are tagged with Nan because TiDB 1.0 and 2.0 do not support view.
- Queries 2, 17, and 19 in the TiDB 1.0 column are tagged with Nan because TiDB 1.0 does not return a result for long.
- Queries 5, 7, 18, and 21 in the TiDB 1.0 column are tagged with OOM because TiDB 1.0 memory space is occupied too much and then is killed by oom-killer.