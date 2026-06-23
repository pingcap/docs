---
title: "{{{ .lake }}} vs. Snowflake: Data Ingestion Benchmark"
summary: This page presents a benchmark comparison of data ingestion performance and cost between {{{ .lake }}} and Snowflake, focusing on TPC-H SF100 dataset loading, ClickBench Hits dataset loading, and freshness benchmarks.
---

# {{{ .lake }}} vs. Snowflake: Data Ingestion Benchmark

## Overview

We conducted four specific benchmarks to evaluate {{{ .lake }}} versus Snowflake:

1. **TPC-H SF100 Dataset Loading**: Focuses on loading performance and cost for a large-scale dataset (100GB, ~600 million rows).
2. **ClickBench Hits Dataset Loading**: Tests efficiency in loading a wide-table dataset (76GB, ~100 million rows, 105 columns), emphasizing challenges associated with high column counts.
3. **1-Second Freshness**: Measures the platforms' ability to ingest data within a strict 1-second freshness requirement.
4. **5-Second Freshness**: Compares the platforms' data ingestion capabilities under a 5-second freshness constraint.

## Platforms

- **[Snowflake](https://snowflake.com)**: A well-known cloud data platform emphasizing scalable compute, data sharing.
- **[{{{ .lake }}}](https://tidbcloud.com)**: A cloud-native data warehouse built on the open-source {{{ .lake }}} project, focusing on scalability and cost-efficiency.

## Benchmark Conditions

Conducted on a `Small-Size` warehouse (16vCPU, AWS us-east-2) using data from the same S3 bucket.

## Performance and Cost Comparison

- **TPC-H SF100 Data**: {{{ .lake }}} offers a **67% cost reduction** over Snowflake.
- **ClickBench Hits Data**: {{{ .lake }}} achieves a **91% cost reduction**.
- **1-Second Freshness**: {{{ .lake }}} loads **400 times** more data than Snowflake.
- **5-Second Freshness**: {{{ .lake }}} loads over **27 times** more data.

## Data Ingestion Benchmarks

![Data loading benchmark](/media/tidb-cloud-lake/data-loading-benchmark.png)

### TPC-H SF100 Dataset

| Metric         | Snowflake | {{{ .lake }}} | Description               |
| -------------- | --------- | -------------- | ------------------------- |
| **Total Time** | 695s      | 446s           | Time to load the dataset. |
| **Total Cost** | $0.77     | $0.25          | Cost of data loading.     |

- Data Volume: 100GB
- Rows: Approx. 600 million

### ClickBench Hits Dataset

| Metric         | Snowflake | {{{ .lake }}} | Description               |
| -------------- | --------- | -------------- | ------------------------- |
| **Total Time** | 51m 17s   | 9m 58s         | Time to load the dataset. |
| **Total Cost** | $3.42     | $0.30          | Cost of data loading.     |

- Data Volume: 76GB
- Rows: Approx. 100 million
- Table Width: 105 columns

## Freshness Benchmarks

![Freshness benchmark](/media/tidb-cloud-lake/freshness-benchmark.png)

### 1-Second Freshness Benchmark

Evaluates the volume of data ingested within a 1-second freshness requirement.

| Metric         | Snowflake | {{{ .lake }}} | Description                                     |
| -------------- | --------- | -------------- | ----------------------------------------------- |
| **Total Time** | 1s        | 1s             | Loading time frame.                             |
| **Total Rows** | 100 Rows  | 40,000 Rows    | Volume of data successfully ingested within 1s. |

### 5-Second Freshness Benchmark

Assesses the volume of data that can be ingested within a 5-second freshness requirement.

| Metric         | Snowflake   | {{{ .lake }}} | Description                                     |
| -------------- | ----------- | -------------- | ----------------------------------------------- |
| **Total Time** | 5s          | 5s             | Loading time frame.                             |
| **Total Rows** | 90,000 Rows | 2,500,000 Rows | Volume of data successfully ingested within 5s. |

## Reproduce the Benchmark

You can reproduce the benchmark by following the steps below.

### Benchmark Environment

The benchmark tests both Snowflake and {{{ .lake }}} under similar conditions:

| Parameter      | Snowflake                                                | {{{ .lake }}}                            |
| -------------- | -------------------------------------------------------- | ----------------------------------------- |
| Warehouse Size | Small                                                    | Small                                     |
| vCPU           | 16                                                       | 16                                        |
| Price          | [$4/hour](https://www.snowflake.com/en/pricing-options/) | [$2/hour](https://www.pingcap.com/pricing/) |
| AWS Region     | us-east-2                                                | us-east-2                                 |
| Storage        | AWS S3                                                   | AWS S3                                    |

- The TPC-H SF100 dataset, sourced from [Amazon Redshift](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/CloudDataWarehouseBenchmark/Cloud-DWB-Derived-from-TPCH).
- The ClickBench dataset, sourced from [ClickBench](https://github.com/ClickHouse/ClickBench).

### Prerequisites

- Have a [Snowflake account](https://signup.snowflake.com)
- Create a [{{{ .lake }}} account](https://tidbcloud.com/)

### Data Ingestion Benchmark

The data ingestion benchmark can be reproduced using the following steps:

<details>
  <summary>TPC-H Data Loading</summary>

1. **Snowflake Data Load**:

    - Log into your [Snowflake account](https://app.snowflake.com/).
    - Create tables corresponding to the TPC-H schema. [SQL Script](https://github.com/databendlabs/benchmarks/blob/main/tpch-100/snowflake/setup.sql).
    - Use the `COPY INTO` command to load the data from AWS S3. [SQL Script](https://github.com/databendlabs/benchmarks/blob/main/tpch-100/snowflake/setup.sql).

2. **{{{ .lake }}} Data Load**:

    - Sign in to your [{{{ .lake }}} account](https://tidbcloud.com).
    - Create the necessary tables as per the TPC-H schema. [SQL Script](https://github.com/databendlabs/benchmarks/blob/main/tpch-100/databend/setup.sql).
    - Use a method similar to Snowflake for loading data from AWS S3. [SQL Script](https://github.com/databendlabs/benchmarks/blob/main/tpch-100/databend/setup.sql).

</details>

<details>
  <summary>ClickBench Hits Data Loading</summary>

1. **Snowflake Data Load**:

    - Log into your [Snowflake account](https://app.snowflake.com/).
    - Create tables corresponding to the `hits` schema. [SQL Script](https://gist.github.com/BohuTANG/2a23e5f829a8d180f7388c530526ab21?permalink_comment_id=4991762#file-hits-snowflake-schema).
    - Use the `COPY INTO` command to load the data from AWS S3. [SQL Script](https://gist.github.com/BohuTANG/2a23e5f829a8d180f7388c530526ab21?permalink_comment_id=4991762#gistcomment-4991762).

2. **{{{ .lake }}} Data Load**:

    - Sign in to your [{{{ .lake }}} account](https://tidbcloud.com).
    - Create the necessary tables as per the `hits` schema. [SQL Script](https://gist.github.com/BohuTANG/ab45d251c533dcf0b1ccd3ea1263b8a0#file-hits-databend-schema).
    - Use a method similar to Snowflake for loading data from AWS S3. [SQL Script](https://gist.github.com/BohuTANG/ab45d251c533dcf0b1ccd3ea1263b8a0?permalink_comment_id=4991767#gistcomment-4991767).

</details>

### Freshness Benchmark

Data generation and ingestion for the freshness benchmark can be reproduced using the following steps:

1. Create an [external stage](/tidb-cloud-lake/sql/create-stage.md#example-2-create-external-stage-with-connection) in {{{ .lake }}}.

    ```sql
    CREATE STAGE hits_unload_stage
    URL = 's3://unload/files/'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>'
    );
    ```

2. Unload data to the external stage.

    ```sql
    CREATE or REPLACE FILE FORMAT tsv_unload_format_gzip
        TYPE = TSV,
        COMPRESSION = gzip;

    COPY INTO @hits_unload_stage
    FROM (
        SELECT *
        FROM hits limit <the-rows-you-want>
    )
    FILE_FORMAT = (FORMAT_NAME = 'tsv_unload_format_gzip')
    DETAILED_OUTPUT = true;
    ```

3. Load data from the external stage to the `hits` table.

    ```sql
    COPY INTO hits
        FROM @hits_unload_stage
        PATTERN = '.*[.]tsv.gz'
        FILE_FORMAT = (TYPE = TSV,  COMPRESSION=auto);
    ```

4. Measure results from the dashboard.
