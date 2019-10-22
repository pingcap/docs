---
title: TiSpark Benchmark Results
summary: Learn the TiSpark benchmark results
category: reference
---

# Benchmark test of data write

This document offers the benchmark results of data write between TiSpark and TiDB.

The following tests are performed on four machines whose configuration is as follows:

```
Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz * 2 = 40Vu
12 * 16G = 188G
```

`FIO` test result:

```
WRITE: bw=705MiB/s (740MB/s), 705MiB/s-705MiB/s (740MB/s-740MB/s), io=20.0GiB (21.5GB), run=29034-29034msec
```

The table schema:

```
CREATE TABLE ORDERS  (O_ORDERKEY       INTEGER NOT NULL,
                      O_CUSTKEY        INTEGER NOT NULL,
                      O_ORDERSTATUS    CHAR(1) NOT NULL,
                      O_TOTALPRICE     DECIMAL(15,2) NOT NULL,
                      O_ORDERDATE      DATE NOT NULL,
                      O_ORDERPRIORITY  CHAR(15) NOT NULL,
                      O_CLERK          CHAR(15) NOT NULL,
                      O_SHIPPRIORITY   INTEGER NOT NULL,
                      O_COMMENT        VARCHAR(79) NOT NULL);

```

## Benchmark of TiSpark write

The result of TiSpark write test is as follows:

| Count(*)    | Data Size | Parallel Number | Prepare(s) | Pre-write(s) | Commit(s) | Total(s) |
| :----------- | :--------- | :--------------- | :---------- | :------------ | :---------- | :--------- |
| 1,500,000   | 165M      | 2               | 17         | 68           | 62         | 148       |
| 15,000,000  | 1.7G      | 24              | 49         | 157          | 119        | 326       |
| 150,000,000 | 17G       | 120             | 630        | 1236         | 1098       | 2964      |

## Benchmark of Spark with JDBC

The benchmark result of the Spark with JDBC:

| Count(*)    | Data Size | Parallel Number | Spark JDBC Write(s) | Comments                            |
| :----------- | :--------- | :--------------- | :-------------------- | :----------------------------------- |
| 1,500,000   | 165M      | 24              | 22                   |                                     |
| 15,000,000  | 1.7G      | 24              | 411                  | Using 120 parallel causes `KV Busy`. |
| 150,000,000 | 17G       | 24              | 2936                 | Using 120 parallel causes `KV Busy`. |
