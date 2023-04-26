---
title: TiDB Sysbench Performance Test Report -- v5.2.0 vs. v5.1.1
---

# TiDB Sysbench パフォーマンス テスト レポート -- v5.2.0 対 v5.1.1 {#tidb-sysbench-performance-test-report-v5-2-0-vs-v5-1-1}

## テストの概要 {#test-overview}

このテストは、オンライン トランザクション処理 (OLTP) シナリオで TiDB v5.2.0 と TiDB v5.1.1 の Sysbench パフォーマンスを比較することを目的としています。結果は、v5.1.1 と比較して、v5.2.0 のポイント選択のパフォーマンスが 11.03% 向上し、他のシナリオのパフォーマンスがわずかに低下したことを示しています。

## テスト環境（AWS EC2） {#test-environment-aws-ec2}

### ハードウェア構成 {#hardware-configuration}

| サービスの種類 | EC2タイプ     | インスタンス数 |
| :------ | :--------- | :------ |
| PD      | m5.xlarge  | 3       |
| TiKV    | i3.4xlarge | 3       |
| TiDB    | c5.4xlarge | 3       |
| シスベンチ   | c5.9xlarge | 1       |

### ソフトウェアバージョン {#software-version}

| サービスの種類 | ソフトウェアバージョン       |
| :------ | :---------------- |
| PD      | v5.1.1 および v5.2.0 |
| TiDB    | v5.1.1 および v5.2.0 |
| TiKV    | v5.1.1 および v5.2.0 |
| シスベンチ   | 1.1.0-ead2689     |

### パラメータ構成 {#parameter-configuration}

TiDB v5.2.0 と TiDB v5.1.1 は同じ構成を使用します。

#### TiDB パラメーター構成 {#tidb-parameter-configuration}

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV パラメータ設定 {#tikv-parameter-configuration}

{{< copyable "" >}}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 8
raftdb.max-background-jobs: 4
raftdb.allow-concurrent-memtable-write: true
server.grpc-concurrency: 6
readpool.unified.min-thread-count: 5
readpool.unified.max-thread-count: 20
readpool.storage.normal-concurrency: 10
pessimistic-txn.pipelined: true
server.enable-request-batch: false
```

#### TiDB グローバル変数の構成 {#tidb-global-variable-configuration}

{{< copyable "" >}}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
set global tidb_enable_async_commit = 1;
set global tidb_enable_1pc = 1;
set global tidb_guarantee_linearizability = 0;
set global tidb_enable_clustered_index = 1;
```

## テスト計画 {#test-plan}

1.  TiUPを使用して TiDB v5.2.0 および v5.1.1をデプロイ。
2.  Sysbench を使用して、各テーブルに 1,000 万行のデータがある 16 個のテーブルをインポートします。
3.  各テーブルで`analyze table`ステートメントを実行します。
4.  異なる同時実行テストの前に、復元に使用されるデータをバックアップします。これにより、各テストのデータの一貫性が確保されます。
5.  Sysbench クライアントを起動して、 `point_select` 、 `read_write` 、 `update_index` 、および`update_non_index`テストを実行します。 HAProxy を介して TiDB でストレス テストを実行します。テストには 5 分かかります。
6.  各タイプのテストが完了したら、クラスターを停止し、手順 4 のバックアップ データでクラスターを上書きし、クラスターを再起動します。

### テストデータの準備 {#prepare-test-data}

次のコマンドを実行して、テスト データを準備します。

{{< copyable "" >}}

```bash
sysbench oltp_common \
    --threads=16 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$aws_nlb_host \
    --mysql-port=$aws_nlb_port \
    --mysql-user=root \
    --mysql-password=password \
    prepare --tables=16 --table-size=10000000
```

### テストを実行する {#perform-the-test}

次のコマンドを実行して、テストを実行します。

{{< copyable "" >}}

```bash
sysbench $testname \
    --threads=$threads \
    --time=300 \
    --report-interval=1 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$aws_nlb_host \
    --mysql-port=$aws_nlb_port \
    run --tables=16 --table-size=10000000
```

## 試験結果 {#test-results}

### ポイントセレクト性能 {#point-select-performance}

| スレッド | v5.1.1 QPS | v5.1.1 95%レイテンシー(ミリ秒) | v5.2.0 QPS | v5.2.0 95%レイテンシー(ミリ秒) | QPS の向上 |
| :--- | :--------- | :-------------------- | :--------- | :-------------------- | :------ |
| 150  | 143014.13  | 2.35                  | 174402.5   | 1.23                  | 21.95%  |
| 300  | 199133.06  | 3.68                  | 272018     | 1.64                  | 36.60%  |
| 600  | 389391.65  | 2.18                  | 393536.4   | 2.11                  | 1.06%   |
| 900  | 468338.82  | 2.97                  | 447981.98  | 3.3                   | -4.35%  |
| 1200 | 448348.52  | 5.18                  | 468241.29  | 4.65                  | 4.44%   |
| 1500 | 454376.79  | 7.04                  | 483888.42  | 6.09                  | 6.49%   |

v5.1.1 と比較して、v5.2.0 の Point Select パフォーマンスは 11.03% 向上しています。

![Point Select](/media/sysbench_v511vsv520_point_select.png)

### インデックス以外のパフォーマンスを更新 {#update-non-index-performance}

| スレッド | v5.1.1 QPS | v5.1.1 95%レイテンシー(ミリ秒) | v5.2.0 QPS | v5.2.0 95%レイテンシー(ミリ秒) | QPS の向上 |
| :--- | :--------- | :-------------------- | :--------- | :-------------------- | :------ |
| 150  | 31198.68   | 6.43                  | 30714.73   | 6.09                  | -1.55%  |
| 300  | 43577.15   | 10.46                 | 42997.92   | 9.73                  | -1.33%  |
| 600  | 57230.18   | 17.32                 | 56168.81   | 16.71                 | -1.85%  |
| 900  | 65325.11   | 23.1                  | 64098.04   | 22.69                 | -1.88%  |
| 1200 | 71528.26   | 28.67                 | 69908.15   | 28.67                 | -2.26%  |
| 1500 | 76652.5    | 33.12                 | 74371.79   | 33.72                 | -2.98%  |

v5.1.1 と比較すると、v5.2.0 の Update Non-index パフォーマンスは 1.98% 低下しています。

![Update Non-index](/media/sysbench_v511vsv520_update_non_index.png)

### インデックスのパフォーマンスを更新する {#update-index-performance}

| スレッド | v5.1.1 QPS | v5.1.1 95%レイテンシー(ミリ秒) | v5.2.0 QPS | v5.2.0 95%レイテンシー(ミリ秒) | QPS の向上 |
| :--- | :--------- | :-------------------- | :--------- | :-------------------- | :------ |
| 150  | 15641.04   | 13.22                 | 15320      | 13.46                 | -2.05%  |
| 300  | 19787.73   | 21.89                 | 19161.35   | 22.69                 | -3.17%  |
| 600  | 24566.74   | 36.89                 | 23616.07   | 38.94                 | -3.87%  |
| 900  | 27516.57   | 50.11                 | 26270.04   | 54.83                 | -4.53%  |
| 1200 | 29421.10   | 63.32                 | 28002.65   | 69.29                 | -4.82%  |
| 1500 | 30957.84   | 77.19                 | 28624.44   | 95.81                 | -7.54%  |

v5.0.2 と比較すると、v5.1.0 の Update Index のパフォーマンスは 4.33% 低下しています。

![Update Index](/media/sysbench_v511vsv520_update_index.png)

### 読み書き性能 {#read-write-performance}

| スレッド | v5.1.1 QPS | v5.1.1 95%レイテンシー(ミリ秒) | v5.2.0 QPS | v5.2.0 95%レイテンシー(ミリ秒) | QPS の向上 |
| :--- | :--------- | :-------------------- | :--------- | :-------------------- | :------ |
| 150  | 68471.02   | 57.87                 | 69246      | 54.83                 | 1.13%   |
| 300  | 86573.09   | 97.55                 | 85340.42   | 94.10                 | -1.42%  |
| 600  | 101760.75  | 176.73                | 102221.31  | 173.58                | 0.45%   |
| 900  | 111877.55  | 248.83                | 109276.45  | 257.95                | -2.32%  |
| 1200 | 117479.4   | 337.94                | 114231.33  | 344.08                | -2.76%  |
| 1500 | 119662.91  | 419.45                | 116663.28  | 434.83                | -2.51%  |

v5.0.2 と比較すると、v5.1.0 の読み書きパフォーマンスは 1.24% 低下しています。

![Read Write](/media/sysbench_v511vsv520_read_write.png)
