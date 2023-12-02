---
title: TiDB Sysbench Performance Test Report -- v4.0 vs. v3.0
summary: Compare the Sysbench performance of TiDB 4.0 and TiDB 3.0.
---

# TiDB Sysbench パフォーマンス テスト レポート -- v4.0 と v3.0 {#tidb-sysbench-performance-test-report-v4-0-vs-v3-0}

## テストの目的 {#test-purpose}

このテストの目的は、オンライン トランザクション処理 (OLTP) シナリオにおける TiDB 4.0 と TiDB 3.0 の Sysbench パフォーマンスを比較することです。

## テスト環境（AWS EC2） {#test-environment-aws-ec2}

### ハードウェア構成 {#hardware-configuration}

| サービスの種類 | EC2タイプ     | インスタンス数 |
| :------ | :--------- | :------ |
| PD      | m5.xlarge  | 3       |
| TiKV    | i3.4xlarge | 3       |
| TiDB    | c5.4xlarge | 3       |
| システムベンチ | m5.4x大     | 1       |

### ソフトウェアバージョン {#software-version}

| サービスの種類 | ソフトウェアバージョン |
| :------ | :---------- |
| PD      | 3.0 と 4.0   |
| TiDB    | 3.0 と 4.0   |
| TiKV    | 3.0 と 4.0   |
| システムベンチ | 1.0.20      |

### パラメータ設定 {#parameter-configuration}

#### TiDB v3.0 構成 {#tidb-v3-0-configuration}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV v3.0 構成 {#tikv-v3-0-configuration}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 3
raftdb.max-background-jobs: 3
raftdb.allow-concurrent-memtable-write: true
server.grpc-concurrency: 6
readpool.storage.normal-concurrency: 10
readpool.coprocessor.normal-concurrency: 5
```

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

#### グローバル変数の設定 {#global-variable-configuration}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
set global tidb_disable_txn_auto_retry=0;
```

## テスト計画 {#test-plan}

1.  TiUPを使用して TiDB v4.0 および v3.0をデプロイ。
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

| スレッド | v3.0 QPS    | v3.0 95%レイテンシー(ミリ秒) | v4.0 QPS    | v4.0 95%レイテンシー(ミリ秒) | QPSの向上 |
| :--- | :---------- | :------------------ | :---------- | :------------------ | :----- |
| 150  | 117085.701  | 1.667               | 118165.1357 | 1.608               | 0.92%  |
| 300  | 200621.4471 | 2.615               | 207774.0859 | 2.032               | 3.57%  |
| 600  | 283928.9323 | 4.569               | 320673.342  | 3.304               | 12.94% |
| 900  | 343218.2624 | 6.686               | 383913.3855 | 4.652               | 11.86% |
| 1200 | 347200.2366 | 8.092               | 408929.4372 | 6.318               | 17.78% |
| 1500 | 366406.2767 | 10.562              | 418268.8856 | 7.985               | 14.15% |

v3.0 と比較して、TiDB v4.0 のポイント選択パフォーマンスは 14% 向上しました。

![Point Select](/media/sysbench-v4vsv3-point-select.png)

### インデックス以外のパフォーマンスを更新する {#update-non-index-performance}

| スレッド | v3.0 QPS    | v3.0 95%レイテンシー(ミリ秒) | v4.0 QPS    | v4.0 95%レイテンシー(ミリ秒) | QPSの向上 |
| :--- | :---------- | :------------------ | :---------- | :------------------ | :----- |
| 150  | 15446.41024 | 11.446              | 16954.39971 | 10.844              | 9.76%  |
| 300  | 22276.15572 | 17.319              | 24364.44689 | 16.706              | 9.37%  |
| 600  | 28784.88353 | 29.194              | 31635.70833 | 28.162              | 9.90%  |
| 900  | 32194.15548 | 42.611              | 35787.66078 | 38.942              | 11.16% |
| 1200 | 33954.69114 | 58.923              | 38552.63158 | 51.018              | 13.54% |
| 1500 | 35412.0032  | 74.464              | 40859.63755 | 62.193              | 15.38% |

v3.0 と比較して、TiDB v4.0 の非インデックス更新パフォーマンスは 15% 向上しました。

![Update Non-index](/media/sysbench-v4vsv3-update-non-index.png)

### インデックスのパフォーマンスを更新する {#update-index-performance}

| スレッド | v3.0 QPS    | v3.0 95%レイテンシー(ミリ秒) | v4.0 QPS    | v4.0 95%レイテンシー(ミリ秒) | QPSの向上 |
| :--- | :---------- | :------------------ | :---------- | :------------------ | :----- |
| 150  | 11164.40571 | 16.706              | 11954.73635 | 16.408              | 7.08%  |
| 300  | 14460.98057 | 28.162              | 15243.40899 | 28.162              | 5.41%  |
| 600  | 17112.73036 | 53.85               | 18535.07515 | 50.107              | 8.31%  |
| 900  | 18233.83426 | 86.002              | 20339.6901  | 70.548              | 11.55% |
| 1200 | 18622.50283 | 127.805             | 21390.25122 | 94.104              | 14.86% |
| 1500 | 18980.34447 | 170.479             | 22359.996   | 114.717             | 17.81% |

v3.0 と比較して、TiDB v4.0 のインデックス更新パフォーマンスは 17% 向上しました。

![Update Index](/media/sysbench-v4vsv3-update-index.png)

### 読み取り/書き込みパフォーマンス {#read-write-performance}

| スレッド | v3.0 QPS    | v3.0 95%レイテンシー(ミリ秒) | v4.0 QPS    | v4.0 95%レイテンシー(ミリ秒) | QPSの向上 |
| :--- | :---------- | :------------------ | :---------- | :------------------ | :----- |
| 150  | 43768.33633 | 71.83               | 53912.63705 | 59.993              | 23.18% |
| 300  | 55655.63589 | 121.085             | 71327.21336 | 97.555              | 28.16% |
| 600  | 64642.96992 | 223.344             | 84487.75483 | 176.731             | 30.70% |
| 900  | 68947.25293 | 325.984             | 90177.94612 | 257.95              | 30.79% |
| 1200 | 71334.80099 | 434.829             | 92779.71507 | 344.078             | 30.06% |
| 1500 | 72069.9115  | 580.017             | 95088.50812 | 434.829             | 31.94% |

v3.0 と比較して、TiDB v4.0 の読み取り/書き込みパフォーマンスは 31% 向上しました。

![Read Write](/media/sysbench-v4vsv3-read-write.png)
