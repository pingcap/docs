---
title: TiDB Sysbench Performance Test Report -- v5.0 vs. v4.0
---

# TiDB Sysbench パフォーマンス テスト レポート -- v5.0 と v4.0 {#tidb-sysbench-performance-test-report-v5-0-vs-v4-0}

## テストの目的 {#test-purpose}

このテストの目的は、オンライン トランザクション処理 (OLTP) シナリオにおける TiDB v5.0 と TiDB v4.0 の Sysbench パフォーマンスを比較することです。

## テスト環境（AWS EC2） {#test-environment-aws-ec2}

### ハードウェア構成 {#hardware-configuration}

| サービスの種類 | EC2タイプ     | インスタンス数 |
| :------ | :--------- | :------ |
| PD      | m5.xlarge  | 3       |
| TiKV    | i3.4xlarge | 3       |
| TiDB    | c5.4xlarge | 3       |
| システムベンチ | c5.9xlarge | 1       |

### ソフトウェアバージョン {#software-version}

| サービスの種類 | ソフトウェアバージョン |
| :------ | :---------- |
| PD      | 4.0と5.0     |
| TiDB    | 4.0と5.0     |
| TiKV    | 4.0と5.0     |
| システムベンチ | 1.0.20      |

### パラメータ設定 {#parameter-configuration}

#### TiDB v4.0 構成 {#tidb-v4-0-configuration}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV v4.0 構成 {#tikv-v4-0-configuration}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 3
raftdb.max-background-jobs: 3
raftdb.allow-concurrent-memtable-write: true
server.grpc-concurrency: 6
readpool.unified.min-thread-count: 5
readpool.unified.max-thread-count: 20
readpool.storage.normal-concurrency: 10
pessimistic-txn.pipelined: true
```

#### TiDB v5.0 構成 {#tidb-v5-0-configuration}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV v5.0 構成 {#tikv-v5-0-configuration}

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

#### TiDB v4.0 グローバル変数の構成 {#tidb-v4-0-global-variable-configuration}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
```

#### TiDB v5.0 グローバル変数の構成 {#tidb-v5-0-global-variable-configuration}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
set global tidb_enable_async_commit = 1;
set global tidb_enable_1pc = 1;
set global tidb_guarantee_linearizability = 0;
set global tidb_enable_clustered_index = 1; 

```

## テスト計画 {#test-plan}

1.  TiUPを使用して TiDB v5.0 および v4.0をデプロイ。
2.  Sysbench を使用して、各テーブルに 1,000 万行のデータが含まれる 16 のテーブルをインポートします。
3.  各テーブルに対して`analyze table`ステートメントを実行します。
4.  さまざまな同時実行テストの前に、復元に使用されるデータをバックアップします。これにより、各テストのデータの一貫性が確保されます。
5.  Sysbench クライアントを起動して、 `point_select` 、 `read_write` 、 `update_index` 、および`update_non_index`テストを実行します。 AWS NLB を介して TiDB でストレス テストを実行します。各タイプのテストでは、ウォームアップに 1 分、テストに 5 分かかります。
6.  各種類のテストが完了したら、クラスターを停止し、手順 4 のバックアップ データでクラスターを上書きし、クラスターを再起動します。

### テストデータの準備 {#prepare-test-data}

次のコマンドを実行してテスト データを準備します。

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

次のコマンドを実行してテストを実行します。

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

| スレッド | v4.0 QPS  | v4.0 95%レイテンシー(ミリ秒) | v5.0 QPS  | v5.0 95%レイテンシー(ミリ秒) | QPSの向上 |
| :--- | :-------- | :------------------ | :-------- | :------------------ | :----- |
| 150  | 159451.19 | 1.32                | 177876.25 | 1.23                | 11.56% |
| 300  | 244790.38 | 1.96                | 252675.03 | 1.82                | 3.22%  |
| 600  | 322929.05 | 3.75                | 331956.84 | 3.36                | 2.80%  |
| 900  | 364840.05 | 5.67                | 365655.04 | 5.09                | 0.22%  |
| 1200 | 376529.18 | 7.98                | 366507.47 | 7.04                | -2.66% |
| 1500 | 368390.52 | 10.84               | 372476.35 | 8.90                | 1.11%  |

v4.0 と比較して、TiDB v5.0 のポイント選択パフォーマンスは 2.7% 向上しました。

![Point Select](/media/sysbench_v5vsv4_point_select.png)

### インデックス以外のパフォーマンスを更新する {#update-non-index-performance}

| スレッド | v4.0 QPS | v4.0 95%レイテンシー(ミリ秒) | v5.0 QPS | v5.0 95%レイテンシー(ミリ秒) | QPSの向上 |
| :--- | :------- | :------------------ | :------- | :------------------ | :----- |
| 150  | 17243.78 | 11.04               | 30866.23 | 6.91                | 79.00% |
| 300  | 25397.06 | 15.83               | 45915.39 | 9.73                | 80.79% |
| 600  | 33388.08 | 25.28               | 60098.52 | 16.41               | 80.00% |
| 900  | 38291.75 | 36.89               | 70317.41 | 21.89               | 83.64% |
| 1200 | 41003.46 | 55.82               | 76376.22 | 28.67               | 86.27% |
| 1500 | 44702.84 | 62.19               | 80234.58 | 34.95               | 79.48% |

v4.0 と比較して、TiDB v5.0 の非インデックス更新パフォーマンスは 81% 向上しました。

![Update Non-index](/media/sysbench_v5vsv4_update_non_index.png)

### インデックスのパフォーマンスを更新する {#update-index-performance}

| スレッド | v4.0 QPS | v4.0 95%レイテンシー(ミリ秒) | v5.0 QPS | v5.0 95%レイテンシー(ミリ秒) | QPSの向上 |
| :--- | :------- | :------------------ | :------- | :------------------ | :----- |
| 150  | 11736.21 | 17.01               | 15631.34 | 17.01               | 33.19% |
| 300  | 15435.95 | 28.67               | 19957.06 | 22.69               | 29.29% |
| 600  | 18983.21 | 49.21               | 23218.14 | 41.85               | 22.31% |
| 900  | 20855.29 | 74.46               | 26226.76 | 53.85               | 25.76% |
| 1200 | 21887.64 | 102.97              | 28505.41 | 69.29               | 30.24% |
| 1500 | 23621.15 | 110.66              | 30341.06 | 82.96               | 28.45% |

v4.0 と比較して、TiDB v5.0 のインデックス更新パフォーマンスは 28% 向上しました。

![Update Index](/media/sysbench_v5vsv4_update_index.png)

### 読み取り/書き込みパフォーマンス {#read-write-performance}

| スレッド | v4.0 QPS  | v4.0 95%レイテンシー(ミリ秒) | v5.0 QPS  | v5.0 95%レイテンシー(ミリ秒) | QPSの向上 |
| :--- | :-------- | :------------------ | :-------- | :------------------ | :----- |
| 150  | 59979.91  | 61.08               | 66098.57  | 55.82               | 10.20% |
| 300  | 77118.32  | 102.97              | 84639.48  | 90.78               | 9.75%  |
| 600  | 90619.52  | 183.21              | 101477.46 | 167.44              | 11.98% |
| 900  | 97085.57  | 267.41              | 109463.46 | 240.02              | 12.75% |
| 1200 | 106521.61 | 331.91              | 115416.05 | 320.17              | 8.35%  |
| 1500 | 116278.96 | 363.18              | 118807.5  | 411.96              | 2.17%  |

v4.0 と比較して、TiDB v5.0 の読み取り/書き込みパフォーマンスは 9% 向上しました。

![Read Write](/media/sysbench_v5vsv4_read_write.png)
