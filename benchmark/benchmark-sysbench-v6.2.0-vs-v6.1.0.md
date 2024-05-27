---
title: TiDB Sysbench Performance Test Report -- v6.2.0 vs. v6.1.0
summary: TiDB v6.2.0 と v6.1.0 は、Sysbench テストで同様のパフォーマンスを示しています。ポイント選択のパフォーマンスはわずかに 3.58% 低下しています。非インデックス更新とインデックス更新のパフォーマンスは基本的に変化がなく、それぞれ 0.85% と 0.47% 低下しています。読み取り書き込みのパフォーマンスは 1.21% 低下しています。
---

# TiDB Sysbench パフォーマンス テスト レポート - v6.2.0 と v6.1.0 {#tidb-sysbench-performance-test-report-v6-2-0-vs-v6-1-0}

## テストの概要 {#test-overview}

このテストは、オンライン トランザクション処理 (OLTP) シナリオにおける TiDB v6.2.0 と TiDB v6.1.0 の Sysbench パフォーマンスを比較することを目的としています。結果によると、v6.2.0 のパフォーマンスは基本的に v6.1.0 と同じでした。Point Select のパフォーマンスはわずかに 3.58% 低下しました。

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
| PD      | v6.1.0 および v6.2.0 |
| ティビ     | v6.1.0 および v6.2.0 |
| ティクヴ    | v6.1.0 および v6.2.0 |
| システムベンチ | 1.1.0-df89d34     |

### パラメータ設定 {#parameter-configuration}

TiDB v6.2.0 と TiDB v6.1.0 は同じ構成を使用します。

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
readpool.unified.max-thread-count: 10
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

1.  TiUPを使用して TiDB v6.2.0 および v6.1.0をデプロイ。
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

| スレッド | v6.1.0 TPS | v6.2.0 TPS | v6.1.0 95%レイテンシー(ms) | v6.2.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 243530.01  | 236885.24  | 1.93                 | 2.07                 | -2.73     |
| 600  | 304121.47  | 291395.84  | 3.68                 | 4.03                 | -4.18     |
| 900  | 327301.23  | 314720.02  | 5                    | 5.47                 | -3.84     |

v6.1.0 と比較すると、v6.2.0 の Point Select パフォーマンスはわずかに 3.58% 低下します。

![Point Select](/media/sysbench_v610vsv620_point_select.png)

### 非インデックスパフォーマンスの更新 {#update-non-index-performance}

| スレッド | v6.1.0 TPS | v6.2.0 TPS | v6.1.0 95%レイテンシー(ms) | v6.2.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 42608.8    | 42372.82   | 11.45                | 11.24                | -0.55     |
| 600  | 54264.47   | 53672.69   | 18.95                | 18.95                | -1.09     |
| 900  | 60667.47   | 60116.14   | 26.2                 | 26.68                | -0.91     |

v6.1.0 と比較すると、v6.2.0 の Update Non-index パフォーマンスは基本的に変化せず、0.85% 減少しました。

![Update Non-index](/media/sysbench_v610vsv620_update_non_index.png)

### インデックスのパフォーマンスを更新 {#update-index-performance}

| スレッド | v6.1.0 TPS | v6.2.0 TPS | v6.1.0 95%レイテンシー(ms) | v6.2.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 19384.75   | 19353.58   | 23.52                | 23.52                | -0.16     |
| 600  | 24144.78   | 24007.57   | 38.25                | 37.56                | -0.57     |
| 900  | 26770.9    | 26589.84   | 51.94                | 52.89                | -0.68     |

v6.1.0 と比較すると、v6.2.0 の Update Index のパフォーマンスは基本的に変化せず、0.47% 減少しました。

![Update Index](/media/sysbench_v610vsv620_update_index.png)

### 読み取り書き込みパフォーマンス {#read-write-performance}

| スレッド | v6.1.0 TPS | v6.2.0 TPS | v6.1.0 95%レイテンシー(ms) | v6.2.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 4849.67    | 4797.59    | 86                   | 84.47                | -1.07     |
| 600  | 5643.89    | 5565.17    | 161.51               | 161.51               | -1.39     |
| 900  | 5954.91    | 5885.22    | 235.74               | 235.74               | -1.17     |

v6.1.0 と比較すると、v6.2.0 の読み取り書き込みパフォーマンスは 1.21% 低下します。

![Read Write](/media/sysbench_v610vsv620_read_write.png)
