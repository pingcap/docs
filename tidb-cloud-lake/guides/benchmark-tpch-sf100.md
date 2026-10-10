---
title: "TPC-H ベンチマーク: {{{ .lake }}} vs. Snowflake"
summary: このガイドでは、TPC-H SF100 データセットを使用して {{{ .lake }}} と Snowflake のパフォーマンスおよびコストを比較します。データのロードとクエリ実行のベンチマークに加え、結果を再現するための手順も含まれています。
---

# TPC-H ベンチマーク: {{{ .lake }}} vs. Snowflake

## 概要 {#quick-overview}

### TPC-H {#tpc-h}

TPC-H ベンチマークは、複雑なクエリとデータメンテナンスに焦点を当てた、意思決定支援システムを評価するための標準です。この分析では、TPC-H SF100（SF1 = 600 万行）データセットを使用して {{{ .lake }}} と Snowflake を比較します。このデータセットは 100GB のデータと、22 個のクエリにまたがる約 6 億行で構成されています。

> **Note:**
>
> TPC Benchmark™ および TPC-H™ は、Transaction Processing Performance Council（[TPC](http://www.tpc.org)）の商標です。本ベンチマークは TPC-H に着想を得ていますが、公式の TPC-H 結果と直接比較できるものではありません。

### Snowflake と {{{ .lake }}} {#snowflake-and-lake}

- **[Snowflake](https://www.snowflake.com)**: Snowflake は、ストレージとコンピュートの分離、オンデマンドでスケーラブルなコンピューティング、データ共有、クローン機能などの高度な機能で広く知られています。

- **[{{{ .lake }}}](https://www.tidbcloud.com)**: {{{ .lake }}} は Snowflake と同様の機能を提供するクラウドネイティブなデータウェアハウスであり、ストレージとコンピュートを分離し、必要に応じてスケーラブルなコンピューティングを提供します。

    特に大規模分析において、Snowflake に対するモダンでコスト効率の高い代替手段として位置付けられています。

## パフォーマンスとコストの比較 {#performance-and-cost-comparison}

- **データロードコスト**: {{{ .lake }}} は、Snowflake と比較してデータロードコストを **48% 削減** します。
- **クエリ実行コスト**: {{{ .lake }}} は、クエリ実行において Snowflake より約 **35% 低コスト** です（コールドラン時。ホットラン時は約 27%）。

> **Note:**
>
> このベンチマークでは、Snowflake と {{{ .lake }}} の両方で特別なチューニングを行わず、デフォルト設定を使用しています。この比較は Snowflake Gen1 standard warehouses（`GENERATION = '1'`）に基づいています。また、**私たちの言葉をうのみにせず、ぜひご自身で実行して結果を検証してください。**

### データロードベンチマーク {#data-loading-benchmark}

![TPC-H SF100 data loading benchmark](/media/tidb-cloud-lake/tpch-sf100-data-loading-benchmark.png)

| テーブル         | Snowflake (695s, Cost $0.77) | {{{ .lake }}} (446s, Cost $0.40) | 行数        |
| ---------------- | --------------------------- | -------------------------------- | ----------- |
| customer         | 18.137                      | 13.436                           | 15,000,000  |
| lineitem         | 477.740                     | 305.812                          | 600,037,902 |
| nation           | 1.347                       | 0.708                            | 25          |
| orders           | 103.088                     | 64.323                           | 150,000,000 |
| part             | 19.908                      | 12.192                           | 20,000,000  |
| partsupp         | 67.410                      | 45.346                           | 80,000,000  |
| region           | 0.743                       | 0.725                            | 5           |
| supplier         | 3.000                       | 3.687                            | 10,000,000  |
| **合計時間**     | **695s**                    | **446s**                         |             |
| **合計コスト**   | **$0.77**                   | **$0.40**                        |             |
| **ストレージサイズ** | **20.8GB**               | **24.5GB**                       |             |

### クエリベンチマーク: コールドラン {#query-benchmark-cold-run}

![TPC-H SF100 Cold Run Benchmark](/media/tidb-cloud-lake/tpch-sf100-cold-run-benchmark.png)

| クエリ           | Snowflake (Total 207s, Cost $0.23) | {{{ .lake }}} (Total 166s, Cost $0.15) |
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
| **合計時間**   | **207s**                          | **166s**                               |
| **合計コスト** | **$0.23**                         | **$0.15**                              |

### クエリベンチマーク: ホットラン {#query-benchmark-hot-run}

![TPC-H SF100 Hot Run Benchmark](/media/tidb-cloud-lake/tpch-sf100-hot-run-benchmark.png)

| クエリ           | Snowflake (Total 138s, Cost $0.15) | {{{ .lake }}} (Total 124s, Cost $0.11) |
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
| **合計時間**   | **138s**                           | **124s**                                |
| **合計コスト** | **$0.15**                          | **$0.11**                               |

## ベンチマークの再現 {#reproduce-the-benchmark}

以下の手順に従うことで、このベンチマークを再現できます。

### ベンチマーク環境 {#benchmark-environment}

このベンチマークでは、Snowflake と {{{ .lake }}} の両方を類似した条件でテストしています。

| パラメータ      | Snowflake                                                | {{{ .lake }}}                            |
| -------------- | -------------------------------------------------------- | ----------------------------------------- |
| Warehouse サイズ | Small                                                    | Small                                     |
| 価格           | [$4/hour](https://www.snowflake.com/en/pricing-options/) | [$3.2/hour](https://www.pingcap.com/pricing) |
| AWS Region     | us-east-2                                                | us-east-2                                 |
| ストレージ     | AWS S3                                                   | AWS S3                                    |

- [Amazon Redshift](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/CloudDataWarehouseBenchmark/Cloud-DWB-Derived-from-TPCH) から取得した TPC-H SF100 データセットを、特別なチューニングを行わずに {{{ .lake }}} と Snowflake の両方へロードしました。

### ベンチマーク手法 {#benchmark-methodology}

このベンチマークには、クエリ実行に対する Cold Run と Hot Run の両方が含まれます。

1. **Cold Run**: クエリを実行する前に、データウェアハウスを一時停止してから再開しました。
2. **Hot Run**: データウェアハウスは一時停止せず、ローカルディスクキャッシュを使用します。

### 前提条件 {#prerequisites}

- [Snowflake account](https://signup.snowflake.com) を持っていること
- [{{{ .lake }}} account](https://tidbcloud.com) を作成すること

### データロード {#data-loading}

1. **Snowflake のデータロード**:

    - [Snowflake account](https://app.snowflake.com/) にログインします。
    - TPC-H スキーマに対応するテーブルを作成します。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql)。
    - `COPY INTO` コマンドを使用して AWS S3 からデータをロード (load) します。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/setup.sql)。

2. **{{{ .lake }}} のデータロード**:

    - [{{{ .lake }}} account](https://tidbcloud.com) にサインインします。
    - TPC-H スキーマに従って必要なテーブルを作成します。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql)。
    - Snowflake と同様の方法で AWS S3 からデータをロードします。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/setup.sql)。

### TPC-H クエリ {#tpc-h-queries}

1. **Snowflake のクエリ**:

    - [Snowflake account](https://app.snowflake.com/) にログインします。
    - TPC-H クエリを実行します。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/snowflake/queries.sql)。

2. **{{{ .lake }}} のクエリ**:

    - [{{{ .lake }}} account](https://tidbcloud.com) にサインインします。
    - TPC-H クエリを実行します。[SQL Script](https://lakesql-bin.tidbcloud.com/datasets/tpch/tpch-100/lake/queries.sql)。