---
title: TiDB Sysbench Performance Test Report -- v5.3.0 vs. v5.2.2
summary: TiDB v5.3.0 と v5.2.2 は、オンライン トランザクション処理 (OLTP) の Sysbench パフォーマンス テストで比較されました。結果は、v5.3.0 のパフォーマンスが v5.2.2 とほぼ同じであることを示しています。v5.3.0 のポイント選択パフォーマンスは 0.81% 低下し、非インデックス更新パフォーマンスは 0.95% 向上し、インデックス更新パフォーマンスは 1.83% 向上し、読み取り書き込みパフォーマンスは 0.62% 低下しました。
---

# TiDB Sysbench パフォーマンス テスト レポート - v5.3.0 と v5.2.2 {#tidb-sysbench-performance-test-report-v5-3-0-vs-v5-2-2}

## テストの概要 {#test-overview}

このテストは、オンライン トランザクション処理 (OLTP) シナリオにおける TiDB v5.3.0 と TiDB v5.2.2 の Sysbench パフォーマンスを比較することを目的としています。結果から、v5.3.0 のパフォーマンスは v5.2.2 とほぼ同じであることがわかります。

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
| PD      | v5.2.2 および v5.3.0 |
| ティビ     | v5.2.2 および v5.3.0 |
| ティクヴ    | v5.2.2 および v5.3.0 |
| システムベンチ | 1.1.0-ead2689     |

### パラメータ設定 {#parameter-configuration}

TiDB v5.3.0 と TiDB v5.2.2 は同じ構成を使用します。

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

#### HAProxy 設定 - haproxy.cfg {#haproxy-configuration-haproxy-cfg}

TiDB で HAProxy を使用する方法の詳細については、 [TiDB で HAProxy を使用するためのベスト プラクティス](/best-practices/haproxy-best-practices.md)参照してください。

```yaml
global                                     # Global configuration.
   chroot      /var/lib/haproxy            # Changes the current directory and sets superuser privileges for the startup process to improve security.
   pidfile     /var/run/haproxy.pid        # Writes the PIDs of HAProxy processes into this file.
   maxconn     4000                        # The maximum number of concurrent connections for a single HAProxy process.
   user        haproxy                     # Same with the UID parameter.
   group       haproxy                     # Same with the GID parameter. A dedicated user group is recommended.
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
   balance roundrobin                      # The server with the fewest connections receives the connection. "leastconn" is recommended where long sessions are expected, such as LDAP, SQL and TSE, rather than protocols using short sessions, such as HTTP. The algorithm is dynamic, which means that server weights might be adjusted on the fly for slow starts for instance.
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## テスト計画 {#test-plan}

1.  TiUPを使用して TiDB v5.3.0 および v5.2.2をデプロイ。
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

| スレッド | v5.2.2TPS | v5.3.0TPS | v5.2.2 95%レイテンシー(ms) | v5.3.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :-------- | :-------- | :------------------- | :------------------- | :-------- |
| 300  | 267673.17 | 267516.77 | 1.76                 | 1.67                 | -0.06     |
| 600  | 369820.29 | 361672.56 | 2.91                 | 2.97                 | -2.20     |
| 900  | 417143.31 | 416479.47 | 4.1                  | 4.18                 | -0.16     |

v5.2.2 と比較すると、v5.3.0 のポイント選択パフォーマンスはわずかに 0.81% 低下します。

![Point Select](/media/sysbench_v522vsv530_point_select.png)

### 非インデックスパフォーマンスの更新 {#update-non-index-performance}

| スレッド | v5.2.2TPS | v5.3.0TPS | v5.2.2 95%レイテンシー(ms) | v5.3.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :-------- | :-------- | :------------------- | :------------------- | :-------- |
| 300  | 39715.31  | 40041.03  | 11.87                | 12.08                | 0.82      |
| 600  | 50239.42  | 51110.04  | 20.74                | 20.37                | 1.73      |
| 900  | 57073.97  | 57252.74  | 28.16                | 27.66                | 0.31      |

v5.2.2 と比較すると、v5.3.0 の Update Non-index パフォーマンスはわずかに 0.95% 向上しています。

![Update Non-index](/media/sysbench_v522vsv530_update_non_index.png)

### インデックスのパフォーマンスを更新 {#update-index-performance}

| スレッド | v5.2.2TPS | v5.3.0TPS | v5.2.2 95%レイテンシー(ms) | v5.3.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :-------- | :-------- | :------------------- | :------------------- | :-------- |
| 300  | 17634.03  | 17821.1   | 25.74                | 25.74                | 1.06      |
| 600  | 20998.59  | 21534.13  | 46.63                | 45.79                | 2.55      |
| 900  | 23420.75  | 23859.64  | 64.47                | 62.19                | 1.87      |

v5.2.2 と比較すると、v5.3.0 の更新インデックスのパフォーマンスはわずかに 1.83% 向上しています。

![Update Index](/media/sysbench_v522vsv530_update_index.png)

### 読み取り書き込みパフォーマンス {#read-write-performance}

| スレッド | v5.2.2TPS | v5.3.0TPS | v5.2.2 95%レイテンシー(ms) | v5.3.0 95%レイテンシー(ms) | TPS改善率（％） |
| :--- | :-------- | :-------- | :------------------- | :------------------- | :-------- |
| 300  | 3872.01   | 3848.63   | 106.75               | 106.75               | -0.60     |
| 600  | 4514.17   | 4471.77   | 200.47               | 196.89               | -0.94     |
| 900  | 4877.05   | 4861.45   | 287.38               | 282.25               | -0.32     |

v5.2.2 と比較すると、v5.3.0 の読み取り書き込みパフォーマンスはわずかに 0.62% 低下します。

![Read Write](/media/sysbench_v522vsv530_read_write.png)
