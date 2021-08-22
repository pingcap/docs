---
title: Explore HTAP
summary: Learn how to explore and use the features of TiDB HTAP.
---

# Explore HTAP

This guide describes how to explore and use the features of TiDB Hybrid Transactional and Analytical Processing (HTAP).

> **Note:**
>
> If you are new to TiDB HTAP and want to start using it quickly, see [Quick start with HTAP](/quick-start-with-htap.md).

## Use cases

TiDB HTAP can meet the needs that have increment massive data, reduce the risk cost of operation, and be used for on-premises big data technology stacks without difficulty, thereby presenting the value of data assets in real time.

The following are the use cases of HTAP:

- Hybrid load

    When using TiDB for real-time Online Analytical Processing (OLAP) that is in hybrid load scenarios, you only need to provide an entry point. Then TiDB automatically selects different processing engines based on the specific business.

- Real-time stream processing

    When using TiDB in real-time stream processing scenarios, TiDB ensures that the continuously flowed data is queried in real time. At the same time, TiDB also can handle highly concurrent workloads and Business Intelligence (BI) queries.

- Data center

    When using TiDB as a data center, TiDB can meet specific business needs by seamlessly connecting the data for the application and the data warehouse.

For more information about use cases of TiDB HTAP, see [blogs about HTAP on the PingCAP website](https://pingcap.com/blog-cn/#HTAP).

## Architecture

In TiDB, a row-based storage engine [TiKV](/tikv-overview.md) for Online Transactional Processing (OLTP) and a columnar storage engine [TiFlash](/tiflash/tiflash-overview.md) for Online Analytical Processing (OLAP) co-exist, replicate data automatically, and keep strong consistency. 

For more information about the architecture, see [architecture of TiDB HTAP](/tiflash/tiflash-overview.md#architecture).

## Prerequisites for environment

Before exploring the features of TiDB HTAP, you need to configure TiDB and the corresponding storage engine according to the data volume. If the data volume is huge (for example, 100 T), it is recommended to use TiFlash Massively Parallel Processing (MPP) as the primary solution and TiSpark as the supplementary solution.

- TiFlash

    - If you have deployed a TiDB cluster but not TiFlash nodes, add the TiFlash nodes in the on-premises TiDB cluster. For detailed information, see [Scale out a TiFlash cluster](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster).
    - If you have not deployed a TiDB cluster, see [Deploy a TiDB Cluster using TiUP](/production-deployment-using-tiup.md). At the same time, you also need to deploy the minimal cluster topology along with [TiFlash](/tiflash-deployment-topology.md).
    - When deciding how to choose the number of TiFlash nodes, consider the following scenarios:

        - If you mainly need OLTP that runs small-scale analytical processing, deploy one or several TiFlash nodes. They can dramatically increase the speed of analytic queries.
        - If the OLTP throughput does not cause significant pressure to I/O usage rate of the TiFlash nodes, each TiFlash node uses more resources for computation, and thus the TiFlash cluster can have near-linear scalability. The number of TiFlash nodes should be tuned based on expected performance and response time.
        - If the OLTP throughput is relatively high (for example, the rate of write throughput or update throughput is higher than 10 million lines/hours), the hot write regions and hot read regions can be formed. This is because the I/O usage in TiKV and TiFlash becomes the bottleneck due to limited write capacity of network and physical disk in this case.

- TiSpark

    - If your data needs to be analyzed with Spark, deploy TiSpark (Spark 3.x is not currently supported). For specific process, see [TiSpark User Guide](/tispark-overview.md).

<!--    - Real-time stream processing
  - If you want to build an efficient and easy-to-use real-time data warehouse with TiDB and Flink, you are welcome to participate in Apache Flink x TiDB meetups.-->

## Prerequisites for data

After TiFlash is deployed, data replication does not automatically begin. You need to manually specify the tables to be replicated to TiFlash.

- If there is no data in the TiDB Cluster, migrate the data to TiDB first. For detailed information, see [data migration](/migration-overview.md).
- If the TiDB cluster already has the replicated data from upstream, after TiFlash is deployed, data replication does not automatically begin. You need to manually specify the tables to be replicated to TiFlash. For detailed information, see [Use TiFlash](/tiflash/use-tiflash.md).

## Data processing

With TiDB, you can simply enter SQL statements for queries or write requirements. For the tables to be replicated to TiFlash, TiDB chooses the best execution freely by the front-end optimizer.

> **Note:**
> 
> MPP mode of TiFlash is enabled by default. When an SQL statement is executed, TiDB automatically determines whether to run in MPP mode through the optimizer.
>
> - To disable MPP mode of TiFlash, set the value of [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50) system variable to `OFF`.
> - To forcibly enable MPP mode of TiFlash for query execution, set the value of [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50) and [tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-new-in-v51) to `ON`.
> - To see whether to use MPP mode when TiDB execute queries, see [Explain Statements in the MPP Mode](/explain-mpp.md#explain-statements-in-the-mpp-mode). If the output of `EXPLAIN` statement includes `ExchangeSender` and `ExchangeReceiver` operator, MPP mode is activated.

## Performance monitoring

When using TiDB, you can monitor the running status and check TiDB performance by the following methods:

- [TiDB Dashboard](/dashboard/dashboard-intro.md): you can see the overall running status of the TiDB cluster, analyse distribution and trends of read and write traffic, and learn the detailed execution information of slow queries.
- [Monitoring system (Prometheus & Grafana)](/grafana-overview-dashboard.md): you can see the monitoring parameters of TiDB cluster-related componants including PD, TiDB, TiKV, TiFlash,TiCDC, and Node_exporter.

To see the alert rules of TiDB cluster and TiFlash cluster, see [TiDB cluster alert rules](/alert-rules.md) and [TiFlash alert rules](/tiflash/tiflash-alert-rules.md).

## Troubleshooting

If you have issues while using TiDB, refer to the following documents:

- [Analyze slow queries](/analyze-slow-queries.md)
- [Identify expensive queries](/identify-expensive-queries.md)
- [Troubleshoot hotspot issues](/troubleshoot-hot-spot-issues.md)
- [TiDB cluster troubleshooting guide](/troubleshoot-tidb-cluster.md)
- [Troubleshoot a TiFlash Cluster](/tiflash/troubleshoot-tiflash.md)

You are also welcome to create [Github Issues](https://github.com/pingcap/tiflash/issues) or submit your questions on [AskTUG](https://asktug.com/).

## What's next

- To see TiFlash version, critical logs and system tables of TiFlash, see [Maintain a TiFlash cluster](/tiflash/maintain-tiflash.md).
- To remove a specific TiFlash node, see [Scale out a TiFlash cluster](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster).