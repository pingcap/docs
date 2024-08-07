---
title: CALIBRATE RESOURCE
summary: TiDB データベースの CALIBRATE RESOURCE の使用法の概要。
---

# <code>CALIBRATE RESOURCE</code> {#code-calibrate-resource-code}

`CALIBRATE RESOURCE`ステートメントは、現在のクラスターの[「リクエストユニット（RU）」](/tidb-resource-control#what-is-request-unit-ru)容量を推定して出力するために使用されます。

> **注記：**
>
> この機能は TiDB Self-Hosted にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

## 概要 {#synopsis}

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE' WorkloadOption

WorkloadOption ::=
( 'WORKLOAD' ('TPCC' | 'OLTP_READ_WRITE' | 'OLTP_READ_ONLY' | 'OLTP_WRITE_ONLY') )
| ( 'START_TIME' 'TIMESTAMP' ('DURATION' stringLit | 'END_TIME' 'TIMESTAMP')?)?

```

## 権限 {#privileges}

このコマンドを実行するには、次の要件が満たされていることを確認してください。

-   [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)有効にしました。
-   ユーザーには`SUPER`または`RESOURCE_GROUP_ADMIN`権限があります。
-   [実際の作業負荷に基づいて容量を見積もる](#estimate-capacity-based-on-actual-workload)するには、ユーザーは`METRICS_SCHEMA`スキーマ内のすべてのテーブルに対して`SELECT`権限を持っている必要があります。

## 容量を推定する方法 {#methods-for-estimating-capacity}

TiDB は推定に 2 つの方法を提供します。

### 実際の作業負荷に基づいて容量を見積もる {#estimate-capacity-based-on-actual-workload}

アプリケーションがすでに本番環境で実行されている場合、または実際のビジネス テストを実行できる場合は、一定期間の実際のワークロードを使用して合計容量を見積もることをお勧めします。見積りの精度を向上させるには、次の制約に従ってください。

-   `START_TIME`パラメータを使用して、推定を開始する時点を`2006-01-02 15:04:05`の形式で指定します。デフォルトの推定終了時刻は現在の時刻です。
-   `START_TIME`パラメータを指定した後、 `END_TIME`パラメータを使用して推定終了時間を指定するか、 `DURATION`パラメータを使用して`START_TIME`からの推定時間ウィンドウを指定できます。
-   時間枠は 10 分から 24 時間までです。
-   指定された時間枠内で、TiDB と TiKV の CPU 使用率が低すぎる場合、容量を見積もることはできません。

> **注記：**
>
> TiKV は macOS 上の CPU 使用率メトリックを監視しません。macOS 上の実際のワークロードに基づく容量推定はサポートされていません。

### ハードウェアの展開に基づいて容量を見積もる {#estimate-capacity-based-on-hardware-deployment}

この方法は、主に現在のクラスター構成と、さまざまなワークロードで観測された経験値に基づいて容量を推定します。ワークロードの種類によって必要なハードウェアの比率が異なるため、同じハードウェア構成の出力容量は異なる場合があります。ここでの`WORKLOAD`パラメーターは、次の異なるワークロード タイプを受け入れます。デフォルト値は`TPCC`です。

-   `TPCC` : 大量のデータ書き込みを伴うワークロードに適用されます。 `TPC-C`と同様のワークロード モデルに基づいて推定されます。
-   `OLTP_WRITE_ONLY` : 大量のデータ書き込みを伴うワークロードに適用されます。 `sysbench oltp_write_only`と同様のワークロード モデルに基づいて推定されます。
-   `OLTP_READ_WRITE` : 偶数データの読み取りと書き込みのワークロードに適用されます。 `sysbench oltp_read_write`と同様のワークロード モデルに基づいて推定されます。
-   `OLTP_READ_ONLY` : 大量のデータ読み取りが行われるワークロードに適用されます。 `sysbench oltp_read_only`と同様のワークロード モデルに基づいて推定されます。
-   `TPCH_10` : AP クエリに適用されます。2 からの 22 のクエリに基づいて推定されます`TPCH-10G`

> **注記：**
>
> クラスターの RU 容量は、クラスターのトポロジと各コンポーネントのハードウェアおよびソフトウェア構成によって異なります。各クラスターが提供できる実際の RU も、実際のワークロードに関連します。ハードウェア展開に基づく推定値は参考値のみであり、実際の最大値とは異なる場合があります[実際の作業負荷に基づいて容量を見積もる](#estimate-capacity-based-on-actual-workload)にすることをお勧めします。

## 例 {#examples}

実際のワークロードに応じて RU 容量を表示するには、開始時刻`START_TIME`と時間ウィンドウ`DURATION`を指定します。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '20m';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

実際のワークロードに応じて RU 容量を表示するには、開始時刻`START_TIME`と終了時刻`END_TIME`を指定します。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' END_TIME '2023-04-18 08:20:00';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

時間ウィンドウ範囲`DURATION` 10 分から 24 時間の範囲にない場合は、エラーが発生します。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '25h';
ERROR 1105 (HY000): the duration of calibration is too long, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '9m';
ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
```

[実際の作業負荷に基づく容量推定](#estimate-capacity-based-on-actual-workload)機能の監視メトリックには、 `tikv_cpu_quota` 、 `tidb_server_maxprocs` 、 `resource_manager_resource_unit` 、 `process_cpu_usage` 、 `tiflash_cpu_quota` 、 `tiflash_resource_manager_resource_unit` 、および`tiflash_process_cpu_usage`含まれます。CPU クォータ監視データが空の場合、次の例に示すように、対応する監視メトリック名にエラーが発生します。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '60m';
Error 1105 (HY000): There is no CPU quota metrics, metrics 'tikv_cpu_quota' is empty
```

時間ウィンドウ内のワークロードが低すぎる場合、または`resource_manager_resource_unit`と`process_cpu_usage`監視データが欠落している場合は、次のエラーが報告されます。また、TiKV は macOS 上の CPU 使用率を監視しないため、実際のワークロードに基づく容量推定をサポートしておらず、このエラーも報告されます。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '60m';
ERROR 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead
```

RU 容量を表示するには`WORKLOAD`指定します。デフォルト値は`TPCC`です。

```sql
CALIBRATE RESOURCE;
+-------+
| QUOTA |
+-------+
| 190470 |
+-------+
1 row in set (0.01 sec)

CALIBRATE RESOURCE WORKLOAD OLTP_WRITE_ONLY;
+-------+
| QUOTA |
+-------+
| 27444 |
+-------+
1 row in set (0.01 sec)
```
