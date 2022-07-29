---
title: TiDB Sysbench Performance Test Report -- v5.0 vs. v4.0
---

# TiDBSysbenchパフォーマンステストレポート-v5.0とv4.0 {#tidb-sysbench-performance-test-report-v5-0-vs-v4-0}

## テスト目的 {#test-purpose}

このテストは、オンライントランザクション処理（OLTP）シナリオでのTiDBv5.0とTiDBv4.0のSysbenchパフォーマンスを比較することを目的としています。

## テスト環境（AWS EC2） {#test-environment-aws-ec2}

### ハードウェア構成 {#hardware-configuration}

| サービスの種類  | EC2タイプ     | インスタンス数 |
| :------- | :--------- | :------ |
| PD       | m5.xlarge  | 3       |
| TiKV     | i3.4xlarge | 3       |
| TiDB     | c5.4xlarge | 3       |
| Sysbench | c5.9xlarge | 1       |

### ソフトウェアバージョン {#software-version}

| サービスの種類  | ソフトウェアバージョン |
| :------- | :---------- |
| PD       | 4.0および5.0   |
| TiDB     | 4.0および5.0   |
| TiKV     | 4.0および5.0   |
| Sysbench | 1.0.20      |

### パラメータ設定 {#parameter-configuration}

#### TiDBv4.0構成 {#tidb-v4-0-configuration}

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKVv4.0構成 {#tikv-v4-0-configuration}

{{< copyable "" >}}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 3
raftdb.max-background-jobs: 3
raftdb.allow-concurrent-memtable-write: true
server.request-batch-enable-cross-command: false
server.grpc-concurrency: 6
readpool.unified.min-thread-count: 5
readpool.unified.max-thread-count: 20
readpool.storage.normal-concurrency: 10
pessimistic-txn.pipelined: true
```

#### TiDBv5.0構成 {#tidb-v5-0-configuration}

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKVv5.0構成 {#tikv-v5-0-configuration}

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

#### TiDBv4.0グローバル変数構成 {#tidb-v4-0-global-variable-configuration}

{{< copyable "" >}}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
```

#### TiDBv5.0グローバル変数構成 {#tidb-v5-0-global-variable-configuration}

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

1.  TiUPを使用してTiDBv5.0およびv4.0をデプロイします。
2.  Sysbenchを使用して16個のテーブルをインポートします。各テーブルには、1,000万行のデータが含まれています。
3.  各テーブルで`analyze table`のステートメントを実行します。
4.  さまざまな同時実行テストの前に、復元に使用されるデータをバックアップします。これにより、各テストのデータの一貫性が保証されます。
5.  `read_write`クライアントを起動して、 `point_select` 、および`update_index`のテストを実行し`update_non_index` 。 AWSNLBを介してTiDBでストレステストを実行します。各タイプのテストでは、ウォームアップに1分、テストに5分かかります。
6.  各タイプのテストが完了したら、クラスタを停止し、手順4でクラスタをバックアップデータで上書きして、クラスタを再起動します。

### テストデータを準備する {#prepare-test-data}

次のコマンドを実行して、テストデータを準備します。

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

### テストを実行します {#perform-the-test}

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

### ポイントセレクトパフォーマンス {#point-select-performance}

| スレッド | v4.0 QPS  | v4.0 95％レイテンシ（ミリ秒） | v5.0 QPS  | v5.0 95％レイテンシ（ミリ秒） | QPSの改善 |
| :--- | :-------- | :----------------- | :-------- | :----------------- | :----- |
| 150  | 159451.19 | 1.32               | 177876.25 | 1.23               | 11.56％ |
| 300  | 244790.38 | 1.96               | 252675.03 | 1.82               | 3.22％  |
| 600  | 322929.05 | 3.75               | 331956.84 | 3.36               | 2.80%  |
| 900  | 364840.05 | 5.67               | 365655.04 | 5.09               | 0.22%  |
| 1200 | 376529.18 | 7.98               | 366507.47 | 7.04               | -2.66％ |
| 1500 | 368390.52 | 10.84              | 372476.35 | 8.90               | 1.11%  |

v4.0と比較して、TiDB v5.0のポイント選択のパフォーマンスは2.7％向上しています。

![Point Select](/media/sysbench_v5vsv4_point_select.png)

### 非インデックスパフォーマンスの更新 {#update-non-index-performance}

| スレッド | v4.0 QPS | v4.0 95％レイテンシ（ミリ秒） | v5.0 QPS | v5.0 95％レイテンシ（ミリ秒） | QPSの改善 |
| :--- | :------- | :----------------- | :------- | :----------------- | :----- |
| 150  | 17243.78 | 11.04              | 30866.23 | 6.91               | 79.00％ |
| 300  | 25397.06 | 15.83              | 45915.39 | 9.73               | 80.79％ |
| 600  | 33388.08 | 25.28              | 60098.52 | 16.41              | 80.00% |
| 900  | 38291.75 | 36.89              | 70317.41 | 21.89              | 83.64％ |
| 1200 | 41003.46 | 55.82              | 76376.22 | 28.67              | 86.27％ |
| 1500 | 44702.84 | 62.19              | 80234.58 | 34.95              | 79.48％ |

v4.0と比較して、TiDB v5.0のインデックス以外の更新のパフォーマンスは81％向上しています。

![Update Non-index](/media/sysbench_v5vsv4_update_non_index.png)

### インデックスのパフォーマンスを更新する {#update-index-performance}

| スレッド | v4.0 QPS | v4.0 95％レイテンシ（ミリ秒） | v5.0 QPS | v5.0 95％レイテンシ（ミリ秒） | QPSの改善 |
| :--- | :------- | :----------------- | :------- | :----------------- | :----- |
| 150  | 11736.21 | 17.01              | 15631.34 | 17.01              | 33.19% |
| 300  | 15435.95 | 28.67              | 19957.06 | 22.69              | 29.29% |
| 600  | 18983.21 | 49.21              | 23218.14 | 41.85              | 22.31％ |
| 900  | 20855.29 | 74.46              | 26226.76 | 53.85              | 25.76％ |
| 1200 | 21887.64 | 102.97             | 28505.41 | 69.29              | 30.24% |
| 1500 | 23621.15 | 110.66             | 30341.06 | 82.96              | 28.45％ |

v4.0と比較して、TiDB v5.0の更新インデックスのパフォーマンスは28％向上しています。

![Update Index](/media/sysbench_v5vsv4_update_index.png)

### 読み取り/書き込みパフォーマンス {#read-write-performance}

| スレッド | v4.0 QPS  | v4.0 95％レイテンシ（ミリ秒） | v5.0 QPS  | v5.0 95％レイテンシ（ミリ秒） | QPSの改善 |
| :--- | :-------- | :----------------- | :-------- | :----------------- | :----- |
| 150  | 59979.91  | 61.08              | 66098.57  | 55.82              | 10.20% |
| 300  | 77118.32  | 102.97             | 84639.48  | 90.78              | 9.75％  |
| 600  | 90619.52  | 183.21             | 101477.46 | 167.44             | 11.98％ |
| 900  | 97085.57  | 267.41             | 109463.46 | 240.02             | 12.75% |
| 1200 | 106521.61 | 331.91             | 115416.05 | 320.17             | 8.35％  |
| 1500 | 116278.96 | 363.18             | 118807.5  | 411.96             | 2.17%  |

v4.0と比較して、TiDB v5.0の読み取り/書き込みパフォーマンスは9％向上しています。

![Read Write](/media/sysbench_v5vsv4_read_write.png)
