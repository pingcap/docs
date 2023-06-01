---
title: CALIBRATE RESOURCE
summary: An overview of the usage of CALIBRATE RESOURCE for the TiDB database.
---

# <code>CALIBRATE RESOURCE</code> {#code-calibrate-resource-code}

`CALIBRATE RESOURCE`ステートメントは、現在のクラスターの[<a href="/tidb-resource-control#what-is-request-unit-ru">「リクエストユニット(RU)」</a>](/tidb-resource-control#what-is-request-unit-ru)を推定して出力するために使用されます。

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> この機能は[<a href="/tidb-cloud/select-cluster-tier.md#serverless-tier-beta">Serverless Tierクラスター</a>](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)では使用できません。

</CustomContent>

## あらすじ {#synopsis}

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE' WorkloadOption

WorkloadOption ::=
( 'WORKLOAD' ('TPCC' | 'OLTP_READ_WRITE' | 'OLTP_READ_ONLY' | 'OLTP_WRITE_ONLY') )
| ( 'START_TIME' 'TIMESTAMP' ('DURATION' stringLit | 'END_TIME' 'TIMESTAMP')?)?

```

## 権限 {#privileges}

このコマンドを実行するには、次の要件が満たされていることを確認してください。

-   [<a href="/system-variables.md#tidb_enable_resource_control-new-in-v660">`tidb_enable_resource_control`</a>](/system-variables.md#tidb_enable_resource_control-new-in-v660)有効にしました。
-   ユーザーには`SUPER`または`RESOURCE_GROUP_ADMIN`権限があります。
-   ユーザーは`METRICS_SCHEMA`スキーマ内のすべてのテーブルに対する`SELECT`権限を持っています。

## 容量の見積もり方法 {#methods-for-estimating-capacity}

TiDB は 2 つの推定方法を提供します。

### 実際のワークロードに基づいて容量を見積もる {#estimate-capacity-based-on-actual-workload}

アプリケーションがすでに本番環境で実行されている場合、または実際のビジネス テストを実行できる場合は、一定期間にわたる実際のワークロードを使用して総容量を見積もることをお勧めします。推定の精度を向上させるには、次の制約に従ってください。

-   `START_TIME`パラメーターを使用して、推定を開始する時点を`2006-01-02 15:04:05`の形式で指定します。デフォルトの推定終了時刻は現在時刻です。
-   `START_TIME`パラメーターを指定した後、 `END_TIME`パラメーターを使用して推定終了時刻を指定するか、 `DURATION`パラメーターを使用して`START_TIME`からの推定時間ウィンドウを指定できます。
-   時間枠の範囲は 10 分から 24 時間です。
-   指定した時間枠内で、TiDB および TiKV の CPU 使用率が低すぎる場合、容量を見積もることはできません。

### ハードウェア導入に基づいて容量を見積もる {#estimate-capacity-based-on-hardware-deployment}

この方法では主に、現在のクラスター構成に基づいて容量を推定し、さまざまなワークロードで観察された経験値を組み合わせます。ワークロードの種類が異なれば必要なハードウェアの比率も異なるため、同じハードウェア構成でも出力容量が異なる場合があります。ここの`WORKLOAD`パラメータは、次のさまざまなワークロード タイプを受け入れます。デフォルト値は`TPCC`です。

-   `TPCC` : 大量のデータ書き込みを伴うワークロードに適用されます。これは、 `TPC-C`と同様のワークロード モデルに基づいて推定されます。
-   `OLTP_WRITE_ONLY` : 大量のデータ書き込みを伴うワークロードに適用されます。これは、 `sysbench oltp_write_only`と同様のワークロード モデルに基づいて推定されます。
-   `OLTP_READ_WRITE` : データの読み取りと書き込みが均等なワークロードに適用されます。これは、 `sysbench oltp_read_write`と同様のワークロード モデルに基づいて推定されます。
-   `OLTP_READ_ONLY` : 大量のデータを読み取るワークロードに適用されます。これは、 `sysbench oltp_read_only`と同様のワークロード モデルに基づいて推定されます。

> **ノート：**
>
> クラスターの RU 容量は、クラスターのトポロジー、各コンポーネントのハードウェアおよびソフトウェア構成によって異なります。各クラスターが提供できる実際の RU は、実際のワークロードにも関係します。ハードウェア導入に基づく推定値は参考用であり、実際の最大値とは異なる場合があります。 [<a href="#estimate-capacity-based-on-actual-workload">実際のワークロードに基づいて容量を見積もる</a>](#estimate-capacity-based-on-actual-workload)にオススメです。

## 例 {#examples}

開始時間`START_TIME`と時間枠`DURATION`を指定して、実際のワークロードに応じた RU 容量を表示します。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '20m';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

開始時刻`START_TIME`と終了時刻`END_TIME`を指定して、実際のワークロードに応じた RU 容量を表示します。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' END_TIME '2023-04-18 08:20:00';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

時間枠範囲`DURATION` 10 分から 24 時間の範囲に収まらない場合、エラーが発生します。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '25h';
ERROR 1105 (HY000): the duration of calibration is too long, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '9m';
ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
```

時間枠内のワークロードが低すぎる場合、エラーが発生します。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '60m';
ERROR 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead
```

RU 容量を表示するには`WORKLOAD`を指定します。デフォルト値は`TPCC`です。

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
