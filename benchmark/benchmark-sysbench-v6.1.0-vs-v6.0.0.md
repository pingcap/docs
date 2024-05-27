---
title: TiDB Sysbench Performance Test Report -- v6.1.0 vs. v6.0.0
summary: TiDB v6.1.0 は、v6.0.0 と比較して、書き込みが多いワークロードで 2.33% ～ 4.61% のパフォーマンス向上を示しています。テスト環境には、AWS EC2 インスタンスと Sysbench 1.1.0-df89d34 が含まれています。両方のバージョンで同じパラメータ構成を使用しています。テスト計画には、デプロイ、データのインポート、ストレス テストの実行が含まれます。結果では、ポイント選択のパフォーマンスがわずかに低下している一方で、非インデックス更新、インデックス更新、読み取り書き込みのパフォーマンスはそれぞれ 2.90%、4.61%、2.23% 向上しています。
---

# TiDB Sysbench パフォーマンス テスト レポート - v6.1.0 と v6.0.0 {#tidb-sysbench-performance-test-report-v6-1-0-vs-v6-0-0}

## テストの概要 {#test-overview}

このテストは、オンライン トランザクション処理 (OLTP) シナリオにおける TiDB v6.1.0 と TiDB v6.0.0 の Sysbench パフォーマンスを比較することを目的としています。結果では、書き込みワークロードにおいて v6.1.0 のパフォーマンスが向上していることがわかりました。書き込みが多いワークロードのパフォーマンスは 2.33% ～ 4.61% 向上しています。

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
| PD      | v6.0.0 および v6.1.0 |
| ティビ     | v6.0.0 および v6.1.0 |
| ティクヴ    | v6.0.0 および v6.1.0 |
| システムベンチ | 1.1.0-df89d34     |

### パラメータ設定 {#parameter-configuration}

TiDB v6.1.0 と TiDB v6.0.0 は同じ構成を使用します。

#### TiDBパラメータ設定 {#tidb-parameter-configuration}

```yaml
log.level: "error"
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKVパラメータ設定 {#tikv-parameter-configuration}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 8
server.grpc-concurrency: 6
readpool.storage.normal-concurrency: 10
```

#### TiDB グローバル変数の設定 {#tidb-global-variable-configuration}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
set global tidb_enable_async_commit = 1;
set global tidb_enable_1pc = 1;
set global tidb_guarantee_linearizability = 0;
set global tidb_enable_clustered_index = 1;
set global tidb_prepared_plan_cache_size=1000;
```

#### HAProxy 設定 - haproxy.cfg {#haproxy-configuration-haproxy-cfg}

TiDB で HAProxy を使用する方法の詳細については、 [TiDB で HAProxy を使用するためのベスト プラクティス](/best-practices/haproxy-best-practices.md)参照してください。

```yaml
global                                     # Global configuration.
   pidfile     /var/run/haproxy.pid        # Writes the PIDs of HAProxy processes into this file.
   maxconn     4000                        # The maximum number of concurrent connections for a single HAProxy process.
   user        haproxy                     # The same with the UID parameter.
   group       haproxy                     # The same with the GID parameter. A dedicated user group is recommended.
   nbproc      64                          # The number of processes created when going daemon. When starting multiple processes to forward requests, ensure that the value is large enough so that HAProxy does not block processes.
   daemon                                  # Makes the process fork into background. It is equivalent to the command line "-D" argument. It can be disabled by the command line "-db" argument.

defaults                                   # Default configuration.
   log global                              # Inherits the settings of the global configuration.
   retries 2                               # The maximum number of retries to connect to an upstream server. If the number of connection attempts exceeds the value, the backend server is considered unavailable.
   timeout connect  2s                     # The maximum time to wait for a connection attempt to a backend server to succeed. It should be set to a shorter time if the server is located on the same LAN as HAProxy.
   timeout client 30000s                   # The maximum inactivity time on the client side.
   timeout server 30000s                   # The maximum inactivity time on the server side.

listen tidb-cluster                        # Database load balancing.
   bind 0.0.0.0:3390                       # The Floating IP address and listening port.
   mode tcp                                # HAProxy uses layer 4, the transport layer.
   balance leastconn                      # The server with the fewest connections receives the connection. "leastconn" is recommended where long sessions are expected, such as LDAP, SQL and TSE, rather than protocols using short sessions, such as HTTP. The algorithm is dynamic, which means that server weights might be adjusted on the fly for slow starts for instance.
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## テスト計画 {#test-plan}

1.  TiUPを使用して TiDB v6.1.0 および v6.0.0をデプロイ。
2.  Sysbench を使用して、各テーブルに 1,000 万行のデータが含まれる 16 個のテーブルをインポートします。
3.  各テーブルに対して`analyze table`ステートメントを実行します。
4.  さまざまな同時実行テストの前に、復元に使用するデータをバックアップします。これにより、各テストのデータの一貫性が確保されます。
5.  Sysbench クライアントを起動して、テスト`point_select` 、および`update_non_index` `read_write`実行します。HAProxy 経由で`update_index`に対してストレス テストを実行します。各ワークロードでの各同時実行に対して、テストには 20 分かかります。
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
    --time=1200 \
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

| スレッド | v6.0.0 TPS | v6.1.0 TPS | v6.0.0 95%レイテンシー(ms) | v6.1.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 268934.84  | 265353.15  | 1.89                 | 1.96                 | -1.33     |
| 600  | 365217.96  | 358976.94  | 2.57                 | 2.66                 | -1.71     |
| 900  | 420799.64  | 407625.11  | 3.68                 | 3.82                 | -3.13     |

v6.0.0 と比較すると、v6.1.0 の Point Select パフォーマンスはわずかに 2.1% 低下します。

![Point Select](/media/sysbench_v600vsv610_point_select.png)

### 非インデックスパフォーマンスの更新 {#update-non-index-performance}

| スレッド | v6.0.0 TPS | v6.1.0 TPS | v6.0.0 95%レイテンシー(ms) | v6.1.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 41778.95   | 42991.9    | 11.24                | 11.45                | 2.90      |
| 600  | 52045.39   | 54099.58   | 20.74                | 20.37                | 3.95      |
| 900  | 59243.35   | 62084.65   | 27.66                | 26.68                | 4.80      |

v6.0.0 と比較して、v6.1.0 の非インデックス更新パフォーマンスは 3.88% 向上しました。

![Update Non-index](/media/sysbench_v600vsv610_update_non_index.png)

### インデックスのパフォーマンスを更新 {#update-index-performance}

| スレッド | v6.0.0 TPS | v6.1.0 TPS | v6.0.0 95%レイテンシー(ms) | v6.1.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 18085.79   | 19198.89   | 25.28                | 23.95                | 6.15      |
| 600  | 22210.8    | 22877.58   | 42.61                | 41.85                | 3.00      |
| 900  | 25249.81   | 26431.12   | 55.82                | 53.85                | 4.68      |

v6.0.0 と比較して、v6.1.0 の更新インデックスのパフォーマンスは 4.61% 向上しました。

![Update Index](/media/sysbench_v600vsv610_update_index.png)

### 読み取り書き込みパフォーマンス {#read-write-performance}

| スレッド | v6.0.0 TPS | v6.1.0 TPS | v6.0.0 95%レイテンシー(ms) | v6.1.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 4856.23    | 4914.11    | 84.47                | 82.96                | 1.19      |
| 600  | 5676.46    | 5848.09    | 161.51               | 150.29               | 3.02      |
| 900  | 6072.97    | 6223.95    | 240.02               | 223.34               | 2.49      |

v6.0.0 と比較して、v6.1.0 の読み取り書き込みパフォーマンスは 2.23% 向上しました。

![Read Write](/media/sysbench_v600vsv610_read_write.png)
