---
title: TiDB Sysbench Performance Test Report -- v6.0.0 vs. v5.4.0
---

# TiDB Sysbench パフォーマンス テスト レポート -- v6.0.0 と v5.4.0 {#tidb-sysbench-performance-test-report-v6-0-0-vs-v5-4-0}

## テストの概要 {#test-overview}

このテストは、オンライン トランザクション処理 (OLTP) シナリオにおける TiDB v6.0.0 と TiDB v5.4.0 の Sysbench パフォーマンスを比較することを目的としています。結果は、v6.0.0 のパフォーマンスが読み取り/書き込みワークロードで 16.17% 大幅に向上していることを示しています。他のワークロードのパフォーマンスは基本的に v5.4.0 と同じです。

## テスト環境（AWS EC2） {#test-environment-aws-ec2}

### ハードウェア構成 {#hardware-configuration}

| サービスの種類 | EC2タイプ     | インスタンス数 |
| :------ | :--------- | :------ |
| PD      | m5.xlarge  | 3       |
| TiKV    | i3.4xlarge | 3       |
| TiDB    | c5.4xlarge | 3       |
| システムベンチ | c5.9xlarge | 1       |

### ソフトウェアバージョン {#software-version}

| サービスの種類 | ソフトウェアバージョン       |
| :------ | :---------------- |
| PD      | v5.4.0 および v6.0.0 |
| TiDB    | v5.4.0 および v6.0.0 |
| TiKV    | v5.4.0 および v6.0.0 |
| システムベンチ | 1.1.0-df89d34     |

### パラメータ設定 {#parameter-configuration}

TiDB v6.0.0 と TiDB v5.4.0 は同じ構成を使用します。

#### TiDBパラメータの設定 {#tidb-parameter-configuration}

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
raftdb.max-background-jobs: 4
raftdb.allow-concurrent-memtable-write: true
server.grpc-concurrency: 6
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

#### HAProxy 構成 - haproxy.cfg {#haproxy-configuration-haproxy-cfg}

TiDB で HAProxy を使用する方法の詳細については、 [TiDB で HAProxy を使用するためのベスト プラクティス](/best-practices/haproxy-best-practices.md)を参照してください。

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

1.  TiUPを使用して TiDB v6.0.0 および v5.4.0をデプロイ。
2.  Sysbench を使用して、各テーブルに 1,000 万行のデータが含まれる 16 のテーブルをインポートします。
3.  各テーブルに対して`analyze table`ステートメントを実行します。
4.  さまざまな同時実行テストの前に、復元に使用されるデータをバックアップします。これにより、各テストのデータの一貫性が確保されます。
5.  Sysbench クライアントを起動して、 `point_select` 、 `read_write` 、 `update_index` 、および`update_non_index`テストを実行します。 HAProxy を介して TiDB でストレス テストを実行します。各ワークロードでの同時実行ごとに、テストには 20 分かかります。
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

### ポイントセレクト性能 {#point-select-performance}

| スレッド | v5.4.0 TPS | v6.0.0 TPS | v5.4.0 95%レイテンシー(ミリ秒) | v6.0.0 95%レイテンシー(ミリ秒) | TPS の向上 (%) |
| :--- | :--------- | :--------- | :-------------------- | :-------------------- | :---------- |
| 300  | 260085.19  | 265207.73  | 1.82                  | 1.93                  | 1.97        |
| 600  | 378098.48  | 365173.66  | 2.48                  | 2.61                  | -3.42       |
| 900  | 441294.61  | 424031.23  | 3.75                  | 3.49                  | -3.91       |

v5.4.0 と比較すると、v6.0.0 のポイント選択パフォーマンスは 1.79% 若干低下しています。

![Point Select](/media/sysbench_v540vsv600_point_select.png)

### インデックス以外のパフォーマンスを更新する {#update-non-index-performance}

| スレッド | v5.4.0 TPS | v6.0.0 TPS | v5.4.0 95%レイテンシー(ミリ秒) | v6.0.0 95%レイテンシー(ミリ秒) | TPS の向上 (%) |
| :--- | :--------- | :--------- | :-------------------- | :-------------------- | :---------- |
| 300  | 41528.7    | 40814.23   | 11.65                 | 11.45                 | -1.72       |
| 600  | 53220.96   | 51746.21   | 19.29                 | 20.74                 | -2.77       |
| 900  | 59977.58   | 59095.34   | 26.68                 | 28.16                 | -1.47       |

v5.4.0 と比較すると、v6.0.0 のインデックス以外の更新のパフォーマンスは 1.98% わずかに低下しています。

![Update Non-index](/media/sysbench_v540vsv600_update_non_index.png)

### インデックスのパフォーマンスを更新する {#update-index-performance}

| スレッド | v5.4.0 TPS | v6.0.0 TPS | v5.4.0 95%レイテンシー(ミリ秒) | v6.0.0 95%レイテンシー(ミリ秒) | TPS の向上 (%) |
| :--- | :--------- | :--------- | :-------------------- | :-------------------- | :---------- |
| 300  | 18659.11   | 18187.54   | 23.95                 | 25.74                 | -2.53       |
| 600  | 23195.83   | 22270.81   | 40.37                 | 44.17                 | -3.99       |
| 900  | 25798.31   | 25118.78   | 56.84                 | 57.87                 | -2.63       |

v5.4.0 と比較すると、v6.0.0 の更新インデックスのパフォーマンスは 3.05% 低下します。

![Update Index](/media/sysbench_v540vsv600_update_index.png)

### 読み取り/書き込みパフォーマンス {#read-write-performance}

| スレッド | v5.4.0 TPS | v6.0.0 TPS | v5.4.0 95%レイテンシー(ミリ秒) | v6.0.0 95%レイテンシー(ミリ秒) | TPS の向上 (%) |
| :--- | :--------- | :--------- | :-------------------- | :-------------------- | :---------- |
| 300  | 4141.72    | 4829.01    | 97.55                 | 82.96                 | 16.59       |
| 600  | 4892.76    | 5693.12    | 173.58                | 153.02                | 16.36       |
| 900  | 5217.94    | 6029.95    | 257.95                | 235.74                | 15.56       |

v5.4.0 と比較して、v6.0.0 の読み取り/書き込みパフォーマンスは 16.17% 大幅に向上しています。

![Read Write](/media/sysbench_v540vsv600_read_write.png)
