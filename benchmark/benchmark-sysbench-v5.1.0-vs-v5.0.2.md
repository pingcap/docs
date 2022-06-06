---
title: TiDB Sysbench Performance Test Report -- v5.1.0 vs. v5.0.2
---

# TiDBSysbenchパフォーマンステストレポート-v5.1.0とv5.0.2 {#tidb-sysbench-performance-test-report-v5-1-0-vs-v5-0-2}

## テストの概要 {#test-overview}

このテストは、オンライントランザクション処理（OLTP）シナリオでのTiDBv5.1.0とTiDBv5.0.2のSysbenchパフォーマンスを比較することを目的としています。結果は、v5.0.2と比較して、v5.1.0のポイント選択のパフォーマンスが19.4％向上し、読み取り/書き込みおよび更新インデックスのパフォーマンスがわずかに低下することを示しています。

## テスト環境（AWS EC2） {#test-environment-aws-ec2}

### ハードウェア構成 {#hardware-configuration}

| サービスの種類  | EC2タイプ     | インスタンス数 |
| :------- | :--------- | :------ |
| PD       | m5.xlarge  | 3       |
| TiKV     | i3.4xlarge | 3       |
| TiDB     | c5.4xlarge | 3       |
| Sysbench | c5.9xlarge | 1       |

### ソフトウェアバージョン {#software-version}

| サービスの種類  | ソフトウェアバージョン     |
| :------- | :-------------- |
| PD       | v5.0.2およびv5.1.0 |
| TiDB     | v5.0.2およびv5.1.0 |
| TiKV     | v5.0.2およびv5.1.0 |
| Sysbench | 1.0.20          |

### パラメータ設定 {#parameter-configuration}

TiDBv5.1.0とTiDBv5.0.2は同じ構成を使用します。

#### TiDBパラメータ設定 {#tidb-parameter-configuration}

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKVパラメータ設定 {#tikv-parameter-configuration}

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

#### TiDBグローバル変数構成 {#tidb-global-variable-configuration}

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

1.  TiUPを使用してTiDBv5.1.0およびv5.0.2をデプロイします。
2.  Sysbenchを使用して、16個のテーブルをインポートします。各テーブルには、1,000万行のデータが含まれています。
3.  各テーブルで`analyze table`のステートメントを実行します。
4.  さまざまな同時実行テストの前に復元に使用されるデータをバックアップします。これにより、各テストのデータの一貫性が保証されます。
5.  `read_write`クライアントを起動して、 `point_select` 、および`update_index`のテストを実行し`update_non_index` 。 HAProxyを介してTiDBでストレステストを実行します。テストには5分かかります。
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

| スレッド | v5.0.2 QPS | v5.0.2 95％の遅延（ミリ秒） | v5.1.0 QPS | v5.1.0 95％レイテンシ（ミリ秒） | QPSの改善 |
| :--- | :--------- | :----------------- | :--------- | :------------------- | :----- |
| 150  | 137732.27  | 1.86               | 158861.67  | 2                    | 15.34％ |
| 300  | 201420.58  | 2.91               | 238038.44  | 2.71                 | 18.18％ |
| 600  | 303631.52  | 3.49               | 428573.21  | 2.07                 | 41.15％ |
| 900  | 383628.13  | 3.55               | 464863.22  | 3.89                 | 21.18％ |
| 1200 | 391451.54  | 5.28               | 413656.74  | 13.46                | 5.67％  |
| 1500 | 410276.93  | 7.43               | 471418.78  | 10.65                | 14.90％ |

v5.0.2と比較して、v5.1.0のポイント選択のパフォーマンスは19.4％向上しています。

![Point Select](/media/sysbench_v510vsv502_point_select.png)

### 非インデックスパフォーマンスの更新 {#update-non-index-performance}

| スレッド | v5.0.2 QPS | v5.0.2 95％の遅延（ミリ秒） | v5.1.0 QPS | v5.1.0 95％レイテンシ（ミリ秒） | QPSの改善 |
| :--- | :--------- | :----------------- | :--------- | :------------------- | :----- |
| 150  | 29248.2    | 7.17               | 29362.7    | 8.13                 | 0.39％  |
| 300  | 40316.09   | 12.52              | 39651.52   | 13.7                 | -1.65％ |
| 600  | 51011.11   | 22.28              | 47047.9    | 27.66                | -7.77％ |
| 900  | 58814.16   | 27.66              | 59331.84   | 28.67                | 0.88％  |
| 1200 | 65286.52   | 32.53              | 67745.39   | 31.37                | 3.77％  |
| 1500 | 68300.86   | 39.65              | 67899.17   | 44.17                | -0.59％ |

v5.0.2と比較すると、v5.1.0の非インデックス更新のパフォーマンスは0.8％低下します。

![Update Non-index](/media/sysbench_v510vsv502_update_non_index.png)

### インデックスパフォーマンスの更新 {#update-index-performance}

| スレッド | v5.0.2 QPS | v5.0.2 95％の遅延（ミリ秒） | v5.1.0 QPS | v5.1.0 95％レイテンシ（ミリ秒） | QPSの改善 |
| :--- | :--------- | :----------------- | :--------- | :------------------- | :----- |
| 150  | 15066.54   | 14.73              | 14829.31   | 14.73                | -1.57％ |
| 300  | 18535.92   | 24.83              | 17401.01   | 29.72                | -6.12％ |
| 600  | 22862.73   | 41.1               | 21923.78   | 44.98                | -4.11％ |
| 900  | 25286.74   | 57.87              | 24916.76   | 58.92                | -1.46％ |
| 1200 | 27566.18   | 70.55              | 27800.62   | 69.29                | 0.85％  |
| 1500 | 28184.76   | 92.42              | 28679.72   | 86                   | 1.76％  |

v5.0.2と比較すると、v5.1.0の更新インデックスのパフォーマンスは1.8％低下します。

![Update Index](/media/sysbench_v510vsv502_update_index.png)

### 読み取り/書き込みパフォーマンス {#read-write-performance}

| スレッド | v5.0.2 QPS | v5.0.2 95％の遅延（ミリ秒） | v5.1.0 QPS | v5.1.0 95％レイテンシ（ミリ秒） | QPSの改善 |
| :--- | :--------- | :----------------- | :--------- | :------------------- | :----- |
| 150  | 66415.33   | 56.84              | 66591.49   | 57.87                | 0.27％  |
| 300  | 82488.39   | 97.55              | 81226.41   | 101.13               | -1.53％ |
| 600  | 99195.36   | 173.58             | 97357.86   | 179.94               | -1.85％ |
| 900  | 107382.76  | 253.35             | 101665.95  | 267.41               | -5.32％ |
| 1200 | 112389.23  | 337.94             | 107426.41  | 350.33               | -4.42％ |
| 1500 | 113548.73  | 450.77             | 109805.26  | 442.73               | -3.30％ |

v5.0.2と比較すると、v5.1.0の読み取り/書き込みパフォーマンスは2.7％低下します。

![Read Write](/media/sysbench_v510vsv502_read_write.png)
