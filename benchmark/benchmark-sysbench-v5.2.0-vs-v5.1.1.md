---
title: TiDB Sysbench Performance Test Report -- v5.2.0 vs. v5.1.1
summary: TiDB v5.2.0 では、v5.1.1 と比較して、Point Select パフォーマンスが 11.03% 向上しています。ただし、他のシナリオではパフォーマンスがわずかに低下しています。ハードウェアとソフトウェアの構成、テスト プラン、および結果の詳細は、レポートに記載されています。
---

# TiDB Sysbench パフォーマンス テスト レポート - v5.2.0 と v5.1.1 {#tidb-sysbench-performance-test-report-v5-2-0-vs-v5-1-1}

## テストの概要 {#test-overview}

このテストは、オンライン トランザクション処理 (OLTP) シナリオにおける TiDB v5.2.0 と TiDB v5.1.1 の Sysbench パフォーマンスを比較することを目的としています。結果によると、v5.1.1 と比較して、v5.2.0 の Point Select パフォーマンスは 11.03% 向上し、他のシナリオのパフォーマンスはわずかに低下しています。

## テスト環境（AWS EC2） {#test-environment-aws-ec2}

### ハードウェア構成 {#hardware-configuration}

| サービスの種類 | EC2タイプ     | インスタンス数 |
| :------ | :--------- | :------ |
| PD      | m5.特大      | 3       |
| ティクヴ    | i3.4xlarge | 3       |
| ティビ     | c5.4特大     | 3       |
| システムベンチ | c5.9特大     | 1       |

### ソフトウェアバージョン {#software-version}

| サービスの種類 | ソフトウェアバージョン       |
| :------ | :---------------- |
| PD      | v5.1.1 および v5.2.0 |
| ティビ     | v5.1.1 および v5.2.0 |
| ティクヴ    | v5.1.1 および v5.2.0 |
| システムベンチ | 1.1.0-ead2689     |

### パラメータ設定 {#parameter-configuration}

TiDB v5.2.0 と TiDB v5.1.1 は同じ構成を使用します。

#### TiDBパラメータ設定 {#tidb-parameter-configuration}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKVパラメータ設定 {#tikv-parameter-configuration}

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

#### TiDB グローバル変数の設定 {#tidb-global-variable-configuration}

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
2.  Sysbench を使用して、各テーブルに 1,000 万行のデータが含まれる 16 個のテーブルをインポートします。
3.  各テーブルに対して`analyze table`ステートメントを実行します。
4.  さまざまな同時実行テストの前に、復元に使用するデータをバックアップします。これにより、各テストのデータの一貫性が確保されます。
5.  Sysbench クライアント`read_write`起動して、テスト`point_select` `update_non_index`実行します。HAProxy 経由で`update_index`に対してストレス テストを実行します。テストには 5 分かかります。
6.  各タイプのテストが完了したら、クラスターを停止し、手順 4 のバックアップ データでクラスターを上書きして、クラスターを再起動します。

### テストデータを準備する {#prepare-test-data}

テストデータを準備するには、次のコマンドを実行します。

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

テストを実行するには、次のコマンドを実行します。

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

### ポイントセレクトパフォーマンス {#point-select-performance}

| スレッド | v5.1.1 品質保証 | v5.1.1 95%レイテンシー(ms) | v5.2.0 品質保証 | v5.2.0 95%レイテンシー(ms) | QPSの改善 |
| :--- | :---------- | :------------------- | :---------- | :------------------- | :----- |
| 150  | 143014.13   | 2.35                 | 174402.5    | 1.23                 | 21.95% |
| 300  | 199133.06   | 3.68                 | 272018      | 1.64                 | 36.60% |
| 600  | 389391.65   | 2.18                 | 393536.4    | 2.11                 | 1.06%  |
| 900  | 468338.82   | 2.97                 | 447981.98   | 3.3                  | -4.35% |
| 1200 | 448348.52   | 5.18                 | 468241.29   | 4.65                 | 4.44%  |
| 1500 | 454376.79   | 7.04                 | 483888.42   | 6.09                 | 6.49%  |

v5.1.1 と比較して、v5.2.0 のポイント選択パフォーマンスは 11.03% 向上しました。

![Point Select](/media/sysbench_v511vsv520_point_select.png)

### 非インデックスパフォーマンスの更新 {#update-non-index-performance}

| スレッド | v5.1.1 品質保証 | v5.1.1 95%レイテンシー(ms) | v5.2.0 品質保証 | v5.2.0 95%レイテンシー(ms) | QPSの改善 |
| :--- | :---------- | :------------------- | :---------- | :------------------- | :----- |
| 150  | 31198.68    | 6.43                 | 30714.73    | 6.09                 | -1.55% |
| 300  | 43577.15    | 10.46                | 42997.92    | 9.73                 | -1.33% |
| 600  | 57230.18    | 17.32                | 56168.81    | 16.71                | -1.85% |
| 900  | 65325.11    | 23.1                 | 64098.04    | 22.69                | -1.88% |
| 1200 | 71528.26    | 28.67                | 69908.15    | 28.67                | -2.26% |
| 1500 | 76652.5     | 33.12                | 74371.79    | 33.72                | -2.98% |

v5.1.1 と比較すると、v5.2.0 の非インデックス更新パフォーマンスは 1.98% 減少します。

![Update Non-index](/media/sysbench_v511vsv520_update_non_index.png)

### インデックスのパフォーマンスを更新 {#update-index-performance}

| スレッド | v5.1.1 品質保証 | v5.1.1 95%レイテンシー(ms) | v5.2.0 品質保証 | v5.2.0 95%レイテンシー(ms) | QPSの改善 |
| :--- | :---------- | :------------------- | :---------- | :------------------- | :----- |
| 150  | 15641.04    | 13.22                | 15320       | 13.46                | -2.05% |
| 300  | 19787.73    | 21.89                | 19161.35    | 22.69                | -3.17% |
| 600  | 24566.74    | 36.89                | 23616.07    | 38.94                | -3.87% |
| 900  | 27516.57    | 50.11                | 26270.04    | 54.83                | -4.53% |
| 1200 | 29421.10    | 63.32                | 28002.65    | 69.29                | -4.82% |
| 1500 | 30957.84    | 77.19                | 28624.44    | 95.81                | -7.54% |

v5.0.2 と比較すると、v5.1.0 の更新インデックスのパフォーマンスは 4.33% 低下します。

![Update Index](/media/sysbench_v511vsv520_update_index.png)

### 読み取り書き込みパフォーマンス {#read-write-performance}

| スレッド | v5.1.1 品質保証 | v5.1.1 95%レイテンシー(ms) | v5.2.0 品質保証 | v5.2.0 95%レイテンシー(ms) | QPSの改善 |
| :--- | :---------- | :------------------- | :---------- | :------------------- | :----- |
| 150  | 68471.02    | 57.87                | 69246       | 54.83                | 1.13%  |
| 300  | 86573.09    | 97.55                | 85340.42    | 94.10                | -1.42% |
| 600  | 101760.75   | 176.73               | 102221.31   | 173.58               | 0.45%  |
| 900  | 111877.55   | 248.83               | 109276.45   | 257.95               | -2.32% |
| 1200 | 117479.4    | 337.94               | 114231.33   | 344.08               | -2.76% |
| 1500 | 119662.91   | 419.45               | 116663.28   | 434.83               | -2.51% |

v5.0.2 と比較すると、v5.1.0 の読み取り書き込みパフォーマンスは 1.24% 低下します。

![Read Write](/media/sysbench_v511vsv520_read_write.png)
