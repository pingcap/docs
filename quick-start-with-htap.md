---
title: Quick start with HTAP
summary: Learn how to quickly get started with the TiDB HTAP.
---

# Quick Start Guide for TiDB HTAP

This guide walks you through the quickest way to get started with TiDB's one-stop Hybrid Transactional and Analytical Processing (HTAP).

> **Note:**
>
> The steps provided in this guide is ONLY for quick start, NOT for production. To explore more features of HTAP, see [explore HTAP](/explore-htap.md).

## Basic concepts

Before using TiDB HTAP, you need to have basic knowledge about [TiKV](/tikv-overview.md), a row-based storage engine for TiDB Online Transactional Processing (OLTP), and [TiFlash](/tiflash/tiflash-overview.md), a columnar storage engine for TiDB Online Analytical Processing (OLAP).

- Storage engines of HTAP: The row-based storage engine and the columnar storage engine co-exist for HTAP. Both storage engines can replicate data automatically and keep strong consistency. The row-based storage engine optimizes OLTP performance, and the columnar storage engine optimizes OLAP performance.
- Data consistency of HTAP: As a distributed and transactional key-value database, TiKV provides transactional APIs with ACID compliance. With the implementation of the [Raft onsensus algorithm](https://raft.github.io/raft.pdf), TiKV guarantees data consistency between multiple replicas and high availability. TiFlash replicates data from TiKV in real time, which ensures that data is strongly consistent between TiKV.
- Data isolation of HTAP: TiKV and TiFlash can be deployed on different machines as needed to solve the problem of HTAP resource isolation.
- MPP computing engine: [MPP](/tiflash/use-tiflash.md#control-whether-to-select-the-mpp-mode) is a distributed computing framework provided by the TiFlash engine since TiDB 5.0, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. If the MPP mode is enabled, the run time of the analytic queries can be significantly reduced.

## Steps

This document take a popular [TPC-H](http://www.tpc.org/tpch/) dataset as an example to guide you to experience the convenience and high performance of TiDB HTAP by trying to query.

### Step 1: Prerequisites for deployment

Before using TiDB HTAP, follow the steps in the [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md) to deploy a local test environment.

In [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md):

- You are recommended to run `tiup playground` to start a TiDB cluster of the latest version. When you run the following command, 1 TiDB instance, 1 TiKV instance, 1 PD instance, and 1 TiFlash instance are deloyed automatically:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup playground
    ```

- If you want to specify the TiDB version and the number of the instances of each component, run the command that specifies the number of the instances of TiFlash as following:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup playground v5.1.0 --db 2 --pd 3 --kv 3 --tiflash 1 --monitor
    ```

> **Note:**
>
> `tiup playground` command is ONLY for quick start, NOT for production.

### Step 2: Prerequisites for data

By following these steps, you can create the [TPC-H](http://www.tpc.org/tpch/) dataset for using TiDB HTAP. If you are interested in TPC-H, see [General Implementation Guidelines](http://tpc.org/tpc_documents_current_versions/pdf/tpc-h_v3.0.0.pdf).

> **Note:**
>
> If you want to use your existing data for analytic queries, you can [migrate your data to TiDB](/migration-overview.md). If you want to design and create your own data, you can create it by executing SQL statements or using related tools.

1. Install the tool that creates data by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup install bench
    ```

2. Create the data by by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

    If the output of this command shows `Finished`, it indicates that the data is created.

3. Execute the following SQL statement to see the created data:

    {{< copyable "sql" >}}

    ```sql
    SELECT CONCAT(table_schema,'.',table_name) AS 'Table Name', table_rows AS 'Number of Rows', CONCAT(ROUND(data_length/(1024*1024*1024),4),'G') AS 'Data Size', CONCAT(ROUND(index_length/(1024*1024*1024),4),'G') AS 'Index Size', CONCAT(ROUND((data_length+index_length)/(1024*1024*1024),4),'G') AS'Total'FROM information_schema.TABLES WHERE table_schema LIKE 'test';
    ```

    As you can see from the output, eight tables are created in total, and the largest table has 6 million rows of data (the actual amount of the created data is in line with the value of the SQL query, because the data is randomly created by the tool).

    ```sql
    +---------------+----------------+-----------+------------+---------+
    | Table Name    | Number of Rows | Data Size | Index Size | Total   |
    +---------------+----------------+-----------+------------+---------+
    | test.nation   |             25 | 0.0000G   | 0.0000G    | 0.0000G |
    | test.region   |              5 | 0.0000G   | 0.0000G    | 0.0000G |
    | test.part     |         200000 | 0.0245G   | 0.0000G    | 0.0245G |
    | test.supplier |          10000 | 0.0014G   | 0.0000G    | 0.0014G |
    | test.partsupp |         800000 | 0.1174G   | 0.0119G    | 0.1293G |
    | test.customer |         150000 | 0.0242G   | 0.0000G    | 0.0242G |
    | test.orders   |        1514336 | 0.1673G   | 0.0000G    | 0.1673G |
    | test.lineitem |        6001215 | 0.7756G   | 0.0894G    | 0.8651G |
    +---------------+----------------+-----------+------------+---------+
    8 rows in set (0.06 sec)
     ```

    This is a database of a commercial ordering system. In which, the `test.nation` table indicates the information about countries, the `test.region` table indicates the information about regions, the `test.part` table indicates the information about parts, the `test.supplier` table indicates the information about suppliers, the `test.partsupp` table indicates the information about parts from suppliers, the `test.customer` table indicates the information about customers, the `test.customer` table indicates the information about orders, and the `test.lineitem` table indicates the information about online items.

### Step 3: Query with the row-based storage engine

You can see the performance of TiDB when using only the row-based storage engine (for most databases) by executing the following SQL statements:

{{< copyable "sql" >}}

```sql
SELECT
    l_orderkey,
    SUM(
        l_extendedprice * (1 - l_discount)
    ) AS revenue,
    o_orderdate,
    o_shippriority
FROM
    customer,
    orders,
    lineitem
WHERE
    c_mktsegment = 'BUILDING'
AND c_custkey = o_custkey
AND l_orderkey = o_orderkey
AND o_orderdate < DATE '1996-01-01'
AND l_shipdate > DATE '1996-02-01'
GROUP BY
    l_orderkey,
    o_orderdate,
    o_shippriority
ORDER BY
    revenue DESC,
    o_orderdate
limit 10;
```

This is a shipping priority query that gives priority and potential revenue to the highest-revenue order that has not been shipped by a specified date. The potential income is defined as the sum of `l_extendedprice * (1-l_discount)`. The orders are listed in descending order of revenue. In this example, this query lists the unshipped orders with potential query revenue in the top 10.

### Step 4: Replication with the columnar storage engine

After TiFlash is deployed, data replication does not automatically begin. You need to send a DDL statement to TiDB through a MySQL client to create a TiFlash replica for a specific table:

{{< copyable "sql" >}}

```sql
ALTER TABLE test.customer SET TIFLASH REPLICA 1;
ALTER TABLE test.orders SET TIFLASH REPLICA 1;
ALTER TABLE test.lineitem SET TIFLASH REPLICA 1;
```

You can check the status of the TiFlash replicas of a specific table using the following statement:

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'customer';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'orders';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'lineitem';
```

In the result of above statement:

- `AVAILABLE` indicates whether the TiFlash replicas of this table is available or not. `1` means available and `0` means unavailable. Once the replicas become available, this status does not change. If you use DDL statements to modify the number of replicas, the replication status will be recalculated.
- `PROGRESS` means the progress of the replication. The value is between 0.0 and 1.0. 1 means at least one replica is replicated.

### Step 5: analyze data faster using HTAP

If you execute the SQL statements in [Step 3](#step-3-query-with-the-row-based-storage-engine), you can see the performance of TiDB HTAP.

For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use TiFlash replicas based on the cost estimation. You can use the `desc` or `explain analyze` statement to check whether or not a TiFlash replica is selected. For example:

{{< copyable "sql" >}}

```sql
explain analyze SELECT
    l_orderkey,
    SUM(
        l_extendedprice * (1 - l_discount)
    ) AS revenue,
    o_orderdate,
    o_shippriority
FROM
    customer,
    orders,
    lineitem
WHERE
    c_mktsegment = 'BUILDING'
AND c_custkey = o_custkey
AND l_orderkey = o_orderkey
AND o_orderdate < DATE '1996-01-01'
AND l_shipdate > DATE '1996-02-01'
GROUP BY
    l_orderkey,
    o_orderdate,
    o_shippriority
ORDER BY
    revenue DESC,
    o_orderdate
limit 10;
```

If the result of the `EXPLAIN` statement shows `ExchangeSender` and `ExchangeReceiver` operators, it indicates that the MPP mode has taken effect.

In addition, you can specify that each part of the entire query is computed using only the TiFlash. For detailed inforamtion, see [Use TiDB to read TiFlash replicas](/tiflash/use-tiflash.md#use-TiDB-to-read-TiFlash-replicas).

You can compare query results and query performance of these two methods.

## What's next

- [Architecture of TiDB HTAP](stable/tiflash-overview.md#architecture)
- [Explore HTAP](/explore-htap.md)
- [Use TiFlash](/stable/use-tiflash.md#use-tiflash)