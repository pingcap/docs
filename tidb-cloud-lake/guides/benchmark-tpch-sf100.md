---
title: "TPC-H Benchmark: {{{ .lake }}} vs. Snowflake"
summary: 本指南基于 TPC-H SF100 数据集，对 {{{ .lake }}} 与 Snowflake 的性能和成本进行了对比。内容包括数据加载与查询执行的基准测试，以及复现结果的操作说明。
---

# TPC-H Benchmark: {{{ .lake }}} vs. Snowflake

## 快速概览 {#quick-overview}

### TPC-H {#tpc-h}

TPC-H 基准测试是评估决策支持系统的标准，重点关注复杂查询和数据维护。本分析使用 TPC-H SF100（SF1 = 600 万行）数据集对 {{{ .lake }}} 与 Snowflake 进行对比。该数据集包含 100GB 数据，以及分布在 22 个查询中的约 6 亿行数据。

> **Note:**
>
> TPC Benchmark™ 和 TPC-H™ 是 Transaction Processing Performance Council（[TPC](http://www.tpc.org)）的商标。我们的基准测试虽然受 TPC-H 启发，但不能与官方 TPC-H 结果直接比较。

### Snowflake 和 {{{ .lake }}} {#snowflake-and-lake}

- **[Snowflake](https://www.snowflake.com)**：Snowflake 以其先进特性而闻名，例如存储与计算分离、按需可扩展计算、数据共享以及克隆能力。

- **[{{{ .lake }}}](https://www.tidbcloud.com)**：{{{ .lake }}} 提供与 Snowflake 类似的功能。作为云原生数据仓库，它同样实现了存储与计算分离，并可按需提供可扩展计算能力。

    它将自己定位为 Snowflake 的一种现代化且更具成本效益的替代方案，尤其适用于大规模分析场景。

## 性能和成本对比 {#performance-and-cost-comparison}

- **数据加载成本**：与 Snowflake 相比，{{{ .lake }}} 在数据加载方面实现了 **48% 的成本降低**。
- **查询执行成本**：在查询执行方面，{{{ .lake }}} 比 Snowflake 大约 **便宜 35%**（冷运行；热运行约为 27%）。

> **Note:**
>
> 本基准测试对 Snowflake 和 {{{ .lake }}} 均使用默认设置，未进行任何特殊调优。本次对比基于 Snowflake Gen1 standard warehouses（`GENERATION = '1'`）。同时请记住，**不要只听我们的一面之词——我们鼓励你亲自运行并验证这些结果。**

### 数据加载基准测试 {#data-loading-benchmark}

![TPC-H SF100 data loading benchmark](/media/tidb-cloud-lake/tpch-sf100-data-loading-benchmark.png)

| 表            | Snowflake (总计 695s，成本 $0.77) | {{{ .lake }}} (总计 446s，成本 $0.40) | 行数        |
| ---------------- | --------------------------- | -------------------------------- | ----------- |
| customer         | 18.137                      | 13.436                           | 15,000,000  |
| lineitem         | 477.740                     | 305.812                          | 600,037,902 |
| nation           | 1.347                       | 0.708                            | 25          |
| orders           | 103.088                     | 64.323                           | 150,000,000 |
| part             | 19.908                      | 12.192                           | 20,000,000  |
| partsupp         | 67.410                      | 45.346                           | 80,000,000  |
| region           | 0.743                       | 0.725                            | 5           |
| supplier         | 3.000                       | 3.687                            | 10,000,000  |
| **总时间**   | **695s**                    | **446s**                         |             |
| **总成本**   | **$0.77**                   | **$0.40**                        |             |
| **存储大小** | **20.8GB**                  | **24.5GB**                       |             |

### 查询基准测试：冷运行 {#query-benchmark-cold-run}

![TPC-H SF100 Cold Run Benchmark](/media/tidb-cloud-lake/tpch-sf100-cold-run-benchmark.png)

| 查询          | Snowflake（总计 207s，成本 $0.23） | {{{ .lake }}}（总计 166s，成本 $0.15） |
| -------------- | --------------------------------- | -------------------------------------- |
| TPC-H 1        | 11.703                            | 8.036                                  |
| TPC-H 2        | 4.524                             | 3.786                                  |
| TPC-H 3        | 8.908                             | 6.040                                  |
| TPC-H 4        | 8.108                             | 4.462                                  |
| TPC-H 5        | 9.202                             | 7.014                                  |
| TPC-H 6        | 1.237                             | 3.234                                  |
| TPC-H 7        | 9.082                             | 7.345                                  |
| TPC-H 8        | 10.886                            | 8.976                                  |
| TPC-H 9        | 18.152                            | 13.340                                 |
| TPC-H 10       | 13.525                            | 12.891                                 |
| TPC-H 11       | 2.582                             | 2.183                                  |
| TPC-H 12       | 10.099                            | 8.839                                  |
| TPC-H 13       | 13.458                            | 7.206                                  |
| TPC-H 14       | 8.001                             | 4.612                                  |
| TPC-H 15       | 8.737                             | 4.621                                  |
| TPC-H 16       | 4.864                             | 1.645                                  |
| TPC-H 17       | 5.363                             | 14.315                                 |
| TPC-H 18       | 19.971                            | 12.058                                 |
| TPC-H 19       | 9.893                             | 12.579                                 |
| TPC-H 20       | 8.538                             | 8.836                                  |
| TPC-H 21       | 16.439                            | 12.270                                 |
| TPC-H 22       | 3.744                             | 1.926                                  |
| **总时间** | **207s**                          | **166s**                               |
| **总成本** | **$0.23**                         | **$0.15**                              |

### 查询基准测试：热运行 {#query-benchmark-hot-run}

![TPC-H SF100 Hot Run Benchmark](/media/tidb-cloud-lake/tpch-sf100-hot-run-benchmark.png)

| 查询          | Snowflake（总计 138s，成本 $0.15） | {{{ .lake }}}（总计 124s，成本 $0.11） |
| -------------- | ---------------------------------- | --------------------------------------- |
| TPC-H 1        | 8.934                              | 7.568                                   |
| TPC-H 2        | 3.018                              | 3.125                                   |
| TPC-H 3        | 6.089                              | 5.234                                   |
| TPC-H 4        | 4.914                              | 3.392                                   |
| TPC-H 5        | 5.800                              | 4.857                                   |
| TPC-H 6        | 0.891                              | 2.142                                   |
| TPC-H 7        | 5.381                              | 4.389                                   |
| TPC-H 8        | 5.724                              | 5.887                                   |
| TPC-H 9        | 10.283                             | 9.621                                   |
| TPC-H 10       | 10.368                             | 8.524                                   |
| TPC-H 11       | 1.165                              | 1.364                                   |
| TPC-H 12       | 7.052                              | 5.352                                   |
| TPC-H 13       | 12.829                             | 6.180                                   |
| TPC-H 14       | 3.288                              | 2.725                                   |
| TPC-H 15       | 3.475                              | 2.748                                   |
| TPC-H 16       | 4.094                              | 1.124                                   |
| TPC-H 17       | 4.203                              | 13.757                                  |
| TPC-H 18       | 18.583                             | 11.630                                  |
| TPC-H 19       | 3.888                              | 7.881                                   |
| TPC-H 20       | 6.379                              | 5.797                                   |
| TPC-H 21       | 10.287                             | 9.806                                   |
| TPC-H 22       | 1.573                              | 1.122                                   |
| **总时间** | **138s**                           | **124s**                                |
| **总成本** | **$0.15**                          | **$0.11**                               |

## 复现基准测试 {#reproduce-the-benchmark}

你可以按照以下步骤复现该基准测试。

### 基准测试环境 {#benchmark-environment}

该基准测试在相似条件下对 Snowflake 和 {{{ .lake }}} 进行了测试：

| 参数      | Snowflake                                                | {{{ .lake }}}                            |
| -------------- | -------------------------------------------------------- | ----------------------------------------- |
| 计算集群 (Warehouse) 大小 | Small                                                    | Small                                     |
| 价格          | [$4/hour](https://www.snowflake.com/en/pricing-options/) | [$3.2/hour](https://www.pingcap.com/pricing) |
| AWS Region     | us-east-2                                                | us-east-2                                 |
| 存储        | AWS S3                                                   | AWS S3                                    |

- TPC-H SF100 数据集来源于 [Amazon Redshift](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/CloudDataWarehouseBenchmark/Cloud-DWB-Derived-from-TPCH)，在未进行任何特定调优的情况下被加载到 {{{ .lake }}} 和 Snowflake 中。

### 基准测试方法 {#benchmark-methodology}

该基准测试中的查询执行包含冷运行和热运行两种方式：

1. **Cold Run**：在执行查询之前，先暂停并恢复数据仓库。
2. **Hot Run**：数据仓库不暂停，使用本地磁盘缓存。

### 前提条件 {#prerequisites}

- 拥有一个 [Snowflake account](https://signup.snowflake.com)
- 创建一个 [{{{ .lake }}} account](https://tidbcloud.com)

### 数据加载 {#data-loading}

1. **Snowflake Data Load**：

    - 登录你的 [Snowflake account](https://app.snowflake.com/)。
    - 创建与 TPC-H schema 对应的表。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql)。
    - 使用 `COPY INTO` 命令从 AWS S3 加载数据。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql)。

2. **{{{ .lake }}} Data Load**：

    - 登录你的 [{{{ .lake }}} account](https://tidbcloud.com)。
    - 按照 TPC-H schema 创建所需的表。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql)。
    - 使用与 Snowflake 类似的方法从 AWS S3 加载数据。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql)。

### TPC-H 查询 {#tpc-h-queries}

1. **Snowflake Queries**：

    - 登录你的 [Snowflake account](https://app.snowflake.com/)。
    - 运行 TPC-H 查询。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/queries.sql)。

2. **{{{ .lake }}} Queries**：

    - 登录你的 [{{{ .lake }}} account](https://tidbcloud.com)。
    - 运行 TPC-H 查询。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/queries.sql)。