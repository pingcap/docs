---
title: "TPC-H Benchmark: {{{ .lake }}} vs. Snowflake"
summary: This guide presents a performance and cost comparison between {{{ .lake }}} and Snowflake using the TPC-H SF100 dataset. It includes data loading and query execution benchmarks, along with instructions to reproduce the results.
---

# TPC-H Benchmark: {{{ .lake }}} vs. Snowflake

## Quick Overview

### TPC-H

The TPC-H benchmark is a standard for evaluating decision support systems, focusing on complex queries and data maintenance. This analysis compares {{{ .lake }}} with Snowflake using the TPC-H SF100 (SF1 = 6 million rows) dataset, encompassing 100GB of data and approximately 600 million rows across 22 queries.

> **Note:**
>
> The TPC Benchmark™ and TPC-H™ are trademarks of the Transaction Processing Performance Council ([TPC](http://www.tpc.org)). Our benchmark, while inspired by TPC-H, is not directly comparable to official TPC-H results.

### Snowflake and {{{ .lake }}}

- **[Snowflake](https://www.snowflake.com)**: Snowflake is renowned for its advanced features such as separating storage and compute, scalable computing on demand, data sharing, and cloning capabilities.

- **[{{{ .lake }}}](https://www.tidbcloud.com)**: {{{ .lake }}} offers [similar functionalities](https://github.com/databendlabs/databend/issues/13059) to Snowflake, being a cloud-native data warehouse that also separates storage from computing and provides scalable computing as needed.

    It builds on the open-source [{{{ .lake }}} project](https://github.com/tidbcloud/lakesql) and positions itself as a modern, cost-effective alternative to Snowflake, especially for large-scale analytics.

## Performance and Cost Comparison

- **Data Loading Costs**: {{{ .lake }}} achieves a **48% cost reduction** in data loading compared to Snowflake.
- **Query Execution Costs**: {{{ .lake }}} is approximately **60% less expensive** for query execution than Snowflake.

> **Note:**
>
> This benchmark uses default settings for both Snowflake and {{{ .lake }}} without any special tuning. This comparison is based on Snowflake Gen1 standard warehouses (`GENERATION = '1'`). And remember, **don't just take our word for it — you're encouraged to run and verify these results yourself.**

### Data Loading Benchmark

![TPC-H SF100 data loading benchmark](/media/tidb-cloud-lake/tpch-sf100-data-loading-benchmark.png)

| Table            | Snowflake (695s, Cost $0.77) | {{{ .lake }}} (446s, Cost $0.40) | Rows        |
| ---------------- | --------------------------- | -------------------------------- | ----------- |
| customer         | 18.137                      | 13.436                           | 15,000,000  |
| lineitem         | 477.740                     | 305.812                          | 600,037,902 |
| nation           | 1.347                       | 0.708                            | 25          |
| orders           | 103.088                     | 64.323                           | 150,000,000 |
| part             | 19.908                      | 12.192                           | 20,000,000  |
| partsupp         | 67.410                      | 45.346                           | 80,000,000  |
| region           | 0.743                       | 0.725                            | 5           |
| supplier         | 3.000                       | 3.687                            | 10,000,000  |
| **Total Time**   | **695s**                    | **446s**                         |             |
| **Total Cost**   | **$0.77**                   | **$0.40**                        |             |
| **Storage Size** | **20.8GB**                  | **24.5GB**                       |             |

### Query Benchmark: Cold Run

![TPC-H SF100 Cold Run Benchmark](/media/tidb-cloud-lake/tpch-sf100-cold-run-benchmark.png)

| Query          | Snowflake (Total 207s, Cost $0.23) | {{{ .lake }}} (Total 166s, Cost $0.15) |
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
| **Total Time** | **207s**                          | **166s**                               |
| **Total Cost** | **$0.23**                         | **$0.15**                              |

### Query Benchmark: Hot Run

![TPC-H SF100 Hot Run Benchmark](/media/tidb-cloud-lake/tpch-sf100-hot-run-benchmark.png)

| Query          | Snowflake (Total 138s, Cost $0.15) | {{{ .lake }}} (Total 124s, Cost $0.11) |
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
| **Total Time** | **138s**                           | **124s**                                |
| **Total Cost** | **$0.15**                          | **$0.11**                               |

## Reproduce the Benchmark

You can reproduce the benchmark by following the steps below.

### Benchmark Environment

The benchmark tests both Snowflake and {{{ .lake }}} under similar conditions:

| Parameter      | Snowflake                                                | {{{ .lake }}}                            |
| -------------- | -------------------------------------------------------- | ----------------------------------------- |
| Warehouse Size | Small                                                    | Small                                     |
| Price          | [$4/hour](https://www.snowflake.com/en/pricing-options/) | [$3.2/hour](https://www.pingcap.com/pricing) |
| AWS Region     | us-east-2                                                | us-east-2                                 |
| Storage        | AWS S3                                                   | AWS S3                                    |

- The TPC-H SF100 dataset, sourced from [Amazon Redshift](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/CloudDataWarehouseBenchmark/Cloud-DWB-Derived-from-TPCH), was loaded into both {{{ .lake }}} and Snowflake without any specific tuning.

### Benchmark Methodology

The benchmark includes both Cold and Hot runs for query execution:

1. **Cold Run**: The data warehouse was suspended and resumed before executing the queries.
2. **Hot Run**: The data warehouse is not suspended, local disk cache is used.

### Prerequisites

- Have a [Snowflake account](https://singup.snowflake.com)
- Create a [{{{ .lake }}} account](https://tidbcloud.com)

### Data Loading

1. **Snowflake Data Load**:

    - Log into your [Snowflake account](https://app.snowflake.com/).
    - Create tables corresponding to the TPC-H schema. [SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql).
    - Use the `COPY INTO` command to load the data from AWS S3. [SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql).

2. **{{{ .lake }}} Data Load**:

    - Sign in to your [{{{ .lake }}} account](https://tidbcloud.com).
    - Create the necessary tables as per the TPC-H schema. [SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql).
    - Utilize a similar method to Snowflake for loading data from AWS S3. [SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql).

### TPC-H Queries

1. **Snowflake Queries**:

    - Log into your [Snowflake account](https://app.snowflake.com/).
    - Run the TPC-H queries. [SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/queries.sql).

2. **{{{ .lake }}} Queries**:

    - Sign in to your [{{{ .lake }}} account](https://tidbcloud.com).
    - Run the TPC-H queries. [SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/queries.sql).
