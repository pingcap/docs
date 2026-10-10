---
title: "{{{ .lake }}} vs. Snowflake: データ取り込みベンチマーク"
summary: このページでは、TPC-H SF100 データセットのロード、ClickBench Hits データセットのロード、および鮮度ベンチマークに焦点を当て、{{{ .lake }}} と Snowflake のデータ取り込み性能とコストを比較したベンチマークを紹介します。
---

# {{{ .lake }}} vs. Snowflake: データ取り込みベンチマーク

## 概要 {#overview}

{{{ .lake }}} と Snowflake を評価するために、次の 4 つのベンチマークを実施しました。

1. **TPC-H SF100 データセットのロード**: 大規模データセット（100GB、約 6 億行）のロード性能とコストに焦点を当てます。
2. **ClickBench Hits データセットのロード**: ワイドテーブルのデータセット（76GB、約 1 億行、105 カラム）のロード効率をテストし、多数のカラムに伴う課題を重視します。
3. **1 秒の鮮度**: 1 秒という厳しい鮮度要件内でデータを取り込むプラットフォームの能力を測定します。
4. **5 秒の鮮度**: 5 秒の鮮度制約下での各プラットフォームのデータ取り込み能力を比較します。

## プラットフォーム {#platforms}

- **[Snowflake](https://snowflake.com)**: スケーラブルなコンピュートとデータ共有を重視した、広く知られたクラウドデータプラットフォームです。
- **[{{{ .lake }}}](https://tidbcloud.com)**: スケーラビリティとコスト効率に重点を置いたクラウドネイティブのデータウェアハウスです。

## ベンチマーク条件 {#benchmark-conditions}

同じ S3 バケットのデータを使用し、`Small-Size` Warehouse で実施しました。

> **Note:**
>
> この比較は、Snowflake Gen1 standard warehouses（`GENERATION = '1'`）に基づいています。

## 性能とコストの比較 {#performance-and-cost-comparison}

- **TPC-H SF100 データ**: {{{ .lake }}} は Snowflake と比べて **48% のコスト削減**を実現します。
- **ClickBench Hits データ**: {{{ .lake }}} は **84% のコスト削減**を達成します。
- **1 秒の鮮度**: {{{ .lake }}} は Snowflake より **400 倍**多くのデータをロードします。
- **5 秒の鮮度**: {{{ .lake }}} は **27 倍超**のデータをロードします。

## データ取り込みベンチマーク {#data-ingestion-benchmarks}

![Data loading benchmark](/media/tidb-cloud-lake/data-loading-benchmark.png)

### TPC-H SF100 データセット {#tpc-h-sf100-dataset}

| 指標 | Snowflake | {{{ .lake }}} | 説明 |
| -------------- | --------- | -------------- | ------------------------- |
| **合計時間** | 695s      | 446s           | データセットのロードにかかる時間。 |
| **合計コスト** | $0.77     | $0.40          | データロードのコスト。 |

- データ量: 100GB
- 行数: 約 6 億

### ClickBench Hits データセット {#clickbench-hits-dataset}

| 指標 | Snowflake | {{{ .lake }}} | 説明 |
| -------------- | --------- | -------------- | ------------------------- |
| **合計時間** | 51m 17s   | 9m 58s         | データセットのロードにかかる時間。 |
| **合計コスト** | $3.42     | $0.53          | データロードのコスト。 |

- データ量: 76GB
- 行数: 約 1 億
- テーブル幅: 105 カラム

## 鮮度ベンチマーク {#freshness-benchmarks}

![Freshness benchmark](/media/tidb-cloud-lake/freshness-benchmark.png)

### 1 秒鮮度ベンチマーク {#1-second-freshness-benchmark}

1 秒の鮮度要件内で取り込まれるデータ量を評価します。

| 指標 | Snowflake | {{{ .lake }}} | 説明 |
| -------------- | --------- | -------------- | ----------------------------------------------- |
| **合計時間** | 1s        | 1s             | ロード時間枠。 |
| **合計行数** | 100 Rows  | 40,000 Rows    | 1 秒以内に正常に取り込まれたデータ量。 |

### 5 秒鮮度ベンチマーク {#5-second-freshness-benchmark}

5 秒の鮮度要件内で取り込めるデータ量を評価します。

| 指標 | Snowflake   | {{{ .lake }}} | 説明 |
| -------------- | ----------- | -------------- | ----------------------------------------------- |
| **合計時間** | 5s          | 5s             | ロード時間枠。 |
| **合計行数** | 90,000 Rows | 2,500,000 Rows | 5 秒以内に正常に取り込まれたデータ量。 |

## ベンチマークの再現 {#reproduce-the-benchmark}

以下の手順に従って、このベンチマークを再現できます。

### ベンチマーク環境 {#benchmark-environment}

このベンチマークでは、Snowflake と {{{ .lake }}} の両方を同様の条件でテストしています。

| パラメータ      | Snowflake                                                | {{{ .lake }}}                            |
| -------------- | -------------------------------------------------------- | ----------------------------------------- |
| Warehouse サイズ | Small                                                    | Small                                     |
| 価格          | [$4/hour](https://www.snowflake.com/en/pricing-options/) | [$3.2/hour](https://www.pingcap.com/pricing/) |
| AWS Region     | us-east-2                                                | us-east-2                                 |
| ストレージ        | AWS S3                                                   | AWS S3                                    |

- TPC-H SF100 データセットは、[Amazon Redshift](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/CloudDataWarehouseBenchmark/Cloud-DWB-Derived-from-TPCH) をソースとしています。
- ClickBench データセットは、[ClickBench](https://github.com/ClickHouse/ClickBench) をソースとしています。

### 前提条件 {#prerequisites}

- [Snowflake account](https://signup.snowflake.com) を持っていること
- [{{{ .lake }}} account](https://tidbcloud.com/) を作成すること

### データ取り込みベンチマーク {#data-ingestion-benchmark}

データ取り込みベンチマークは、次の手順で再現できます。

<details>
  <summary>TPC-H データロード</summary>

1. **Snowflake Data Load**:

    - [Snowflake account](https://app.snowflake.com/) にログインします。
    - TPC-H スキーマに対応するテーブルを作成します。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql)。
    - `COPY INTO` コマンドを使用して AWS S3 からデータをロードします。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql)。

2. **{{{ .lake }}} Data Load**:

    - [{{{ .lake }}} account](https://tidbcloud.com) にサインインします。
    - TPC-H スキーマに従って必要なテーブルを作成します。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql)。
    - Snowflake と同様の方法で AWS S3 からデータをロードします。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql)。

</details>

<details>
  <summary>ClickBench Hits データロード</summary>

1. **Snowflake Data Load**:

    - [Snowflake account](https://app.snowflake.com/) にログインします。
    - `hits` スキーマに対応するテーブルを作成します。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/hits/snowflake/schema.sql)。
    - `COPY INTO` コマンドを使用して AWS S3 からデータをロードします。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/hits/snowflake/copy.sql)。

2. **{{{ .lake }}} Data Load**:

    - [{{{ .lake }}} account](https://tidbcloud.com) にサインインします。
    - `hits` スキーマに従って必要なテーブルを作成します。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/hits/lake/schema.sql)。
    - Snowflake と同様の方法で AWS S3 からデータをロードします。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/hits/lake/copy.sql)。

</details>

### 鮮度ベンチマーク {#freshness-benchmark}

鮮度ベンチマークのデータ生成とデータ取り込みは、次の手順で再現できます。

1. {{{ .lake }}} で [external stage](/tidb-cloud-lake/sql/create-stage.md#example-2-create-external-stage-with-connection) を作成します。

    ```sql
    CREATE STAGE hits_unload_stage
    URL = 's3://unload/files/'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>'
    );
    ```

2. データを external stage にアンロード (unload) します。

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

3. external stage から `hits` テーブルにデータをロード (load) します。

    ```sql
    COPY INTO hits
        FROM @hits_unload_stage
        PATTERN = '.*[.]tsv.gz'
        FILE_FORMAT = (TYPE = TSV,  COMPRESSION=auto);
    ```

4. ダッシュボードで結果を測定します。