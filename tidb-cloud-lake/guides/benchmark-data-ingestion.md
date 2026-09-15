---
title: "{{{ .lake }}} vs. Snowflake: 数据摄取基准测试"
summary: 本页展示了 {{{ .lake }}} 与 Snowflake 在数据摄取性能和成本方面的基准对比，重点关注 TPC-H SF100 数据集加载、ClickBench Hits 数据集加载以及新鲜度基准测试。
---

# {{{ .lake }}} vs. Snowflake: 数据摄取基准测试

## 概览 {#overview}

我们进行了四项具体的基准测试，以评估 {{{ .lake }}} 与 Snowflake：

1. **TPC-H SF100 数据集加载**：重点比较大规模数据集（100GB，约 6 亿行）的加载性能和成本。
2. **ClickBench Hits 数据集加载**：测试宽表数据集（76GB，约 1 亿行，105 列）的加载效率，重点关注高列数带来的挑战。
3. **1 秒新鲜度**：衡量平台在严格的 1 秒新鲜度要求下摄取数据的能力。
4. **5 秒新鲜度**：比较平台在 5 秒新鲜度约束下的数据摄取能力。

## 平台 {#platforms}

- **[Snowflake](https://snowflake.com)**：知名的云数据平台，强调可扩展计算和数据共享。
- **[{{{ .lake }}}](https://tidbcloud.com)**：云原生数据仓库，专注于扩展性和成本效益。

## 基准测试条件 {#benchmark-conditions}

在 `Small-Size` 计算集群上进行测试，并使用同一个 S3 存储桶中的数据。

> **Note:**
>
> 此比较基于 Snowflake Gen1 标准计算集群（`GENERATION = '1'`）。

## 性能与成本对比 {#performance-and-cost-comparison}

- **TPC-H SF100 数据**：与 Snowflake 相比，{{{ .lake }}} 可将成本降低 **48%**。
- **ClickBench Hits 数据**：{{{ .lake }}} 实现了 **84%** 的成本降低。
- **1 秒新鲜度**：{{{ .lake }}} 的数据加载量是 Snowflake 的 **400 倍**。
- **5 秒新鲜度**：{{{ .lake }}} 的数据加载量超过 **27 倍**。

## 数据摄取基准测试 {#data-ingestion-benchmarks}

![Data loading benchmark](/media/tidb-cloud-lake/data-loading-benchmark.png)

### TPC-H SF100 数据集 {#tpc-h-sf100-dataset}

| 指标         | Snowflake | {{{ .lake }}} | 描述            |
| -------------- | --------- | -------------- | ---------------------- |
| **Total Time** | 695s      | 446s           | 加载数据集所需的时间。 |
| **Total Cost** | $0.77     | $0.40          | 数据加载的成本。       |

- Data Volume: 100GB
- Rows: Approx. 600 million

### ClickBench Hits 数据集 {#clickbench-hits-dataset}

| 指标         | Snowflake | {{{ .lake }}} | 描述            |
| -------------- | --------- | -------------- | ---------------------- |
| **Total Time** | 51m 17s   | 9m 58s         | 加载数据集所需的时间。 |
| **Total Cost** | $3.42     | $0.53          | 数据加载的成本。       |

- Data Volume: 76GB
- Rows: Approx. 100 million
- Table Width: 105 columns

## 新鲜度基准测试 {#freshness-benchmarks}

![Freshness benchmark](/media/tidb-cloud-lake/freshness-benchmark.png)

### 1 秒新鲜度基准测试 {#1-second-freshness-benchmark}

评估在 1 秒新鲜度要求内成功摄取的数据量。

| 指标         | Snowflake | {{{ .lake }}} | 描述                         |
| -------------- | --------- | -------------- | ----------------------------------- |
| **Total Time** | 1s        | 1s             | 数据加载时间窗口。                  |
| **Total Rows** | 100 Rows  | 40,000 Rows    | 在 1 秒内成功摄取的数据量。         |

### 5 秒新鲜度基准测试 {#5-second-freshness-benchmark}

评估在 5 秒新鲜度要求内可摄取的数据量。

| 指标         | Snowflake   | {{{ .lake }}} | 描述                         |
| -------------- | ----------- | -------------- | ----------------------------------- |
| **Total Time** | 5s          | 5s             | 数据加载时间窗口。                  |
| **Total Rows** | 90,000 Rows | 2,500,000 Rows | 在 5 秒内成功摄取的数据量。         |

## 复现基准测试 {#reproduce-the-benchmark}

你可以按照以下步骤复现该基准测试。

### 基准测试环境 {#benchmark-environment}

该基准测试在相似条件下对 Snowflake 和 {{{ .lake }}} 进行了测试：

| 参数      | Snowflake                                                | {{{ .lake }}}                            |
| -------------- | -------------------------------------------------------- | ----------------------------------------- |
| 计算集群大小 | 小型                                                    | 小型                                     |
| 价格          | [$4/hour](https://www.snowflake.com/en/pricing-options/) | [$3.2/hour](https://www.pingcap.com/pricing/) |
| AWS Region     | us-east-2                                                | us-east-2                                 |
| 存储        | AWS S3                                                   | AWS S3                                    |

- TPC-H SF100 数据集来源于 [Amazon Redshift](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/CloudDataWarehouseBenchmark/Cloud-DWB-Derived-from-TPCH)。
- ClickBench 数据集来源于 [ClickBench](https://github.com/ClickHouse/ClickBench)。

### 前提条件 {#prerequisites}

- 拥有一个 [Snowflake account](https://signup.snowflake.com)
- 创建一个 [{{{ .lake }}} account](https://tidbcloud.com/)

### 数据摄取基准测试 {#data-ingestion-benchmark}

可以按照以下步骤复现数据摄取基准测试：

<details>
  <summary>TPC-H Data Loading</summary>

1. **Snowflake Data Load**：

    - 登录你的 [Snowflake account](https://app.snowflake.com/)。
    - 创建与 TPC-H schema 对应的表。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql)。
    - 使用 `COPY INTO` 命令从 AWS S3 加载数据。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql)。

2. **{{{ .lake }}} Data Load**：

    - 登录你的 [{{{ .lake }}} account](https://tidbcloud.com)。
    - 按照 TPC-H schema 创建所需的表。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql)。
    - 使用与 Snowflake 类似的方法从 AWS S3 加载数据。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql)。

</details>

<details>
  <summary>ClickBench Hits Data Loading</summary>

1. **Snowflake Data Load**：

    - 登录你的 [Snowflake account](https://app.snowflake.com/)。
    - 创建与 `hits` schema 对应的表。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/hits/snowflake/schema.sql)。
    - 使用 `COPY INTO` 命令从 AWS S3 加载数据。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/hits/snowflake/copy.sql)。

2. **{{{ .lake }}} Data Load**：

    - 登录你的 [{{{ .lake }}} account](https://tidbcloud.com)。
    - 按照 `hits` schema 创建所需的表。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/hits/lake/schema.sql)。
    - 使用与 Snowflake 类似的方法从 AWS S3 加载数据。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/hits/lake/copy.sql)。

</details>

### 新鲜度基准测试 {#freshness-benchmark}

可以按照以下步骤复现新鲜度基准测试的数据生成和摄取过程：

1. 在 {{{ .lake }}} 中创建一个 [外部 Stage](/tidb-cloud-lake/sql/create-stage.md#example-2-create-external-stage-with-connection)。

    ```sql
    CREATE STAGE hits_unload_stage
    URL = 's3://unload/files/'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>'
    );
    ```

2. 将数据卸载到 external stage。

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

3. 将数据从 external stage 加载到 `hits` 表。

    ```sql
    COPY INTO hits
        FROM @hits_unload_stage
        PATTERN = '.*[.]tsv.gz'
        FILE_FORMAT = (TYPE = TSV,  COMPRESSION=auto);
    ```

4. 从仪表板中查看结果。
