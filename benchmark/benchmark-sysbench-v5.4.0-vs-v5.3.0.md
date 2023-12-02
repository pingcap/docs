---
title: TiDB Sysbench Performance Test Report -- v5.4.0 vs. v5.3.0
---

# TiDB Sysbench パフォーマンス テスト レポート -- v5.4.0 と v5.3.0 {#tidb-sysbench-performance-test-report-v5-4-0-vs-v5-3-0}

## テストの概要 {#test-overview}

このテストは、オンライン トランザクション処理 (OLTP) シナリオにおける TiDB v5.4.0 と TiDB v5.3.0 の Sysbench パフォーマンスを比較することを目的としています。結果は、書き込みの多いワークロードにおいて v5.4.0 のパフォーマンスが 2.59% ～ 4.85% 向上していることを示しています。

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
| PD      | v5.3.0 および v5.4.0 |
| TiDB    | v5.3.0 および v5.4.0 |
| TiKV    | v5.3.0 および v5.4.0 |
| システムベンチ | 1.1.0-ead2689     |

### パラメータ設定 {#parameter-configuration}

TiDB v5.4.0 と TiDB v5.3.0 は同じ構成を使用します。

#### TiDBパラメータの設定 {#tidb-parameter-configuration}

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

#### HAProxy 構成 - haproxy.cfg {#haproxy-configuration-haproxy-cfg}

TiDB で HAProxy を使用する方法の詳細については、 [TiDB で HAProxy を使用するためのベスト プラクティス](/best-practices/haproxy-best-practices.md)を参照してください。

```yaml
global                                     # Global configuration.
   chroot      /var/lib/haproxy            # Changes the current directory and sets superuser privileges for the startup process to improve security.
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
   balance roundrobin                      # The server with the fewest connections receives the connection. "leastconn" is recommended where long sessions are expected, such as LDAP, SQL and TSE, rather than protocols using short sessions, such as HTTP. The algorithm is dynamic, which means that server weights might be adjusted on the fly for slow starts for instance.
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## テスト計画 {#test-plan}

1.  TiUPを使用して TiDB v5.4.0 および v5.3.0をデプロイ。
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

| スレッド | v5.3.0 TPS | v5.4.0 TPS | v5.3.0 95%レイテンシー(ミリ秒) | v5.4.0 95%レイテンシー(ミリ秒) | TPS の向上 (%) |
| :--- | :--------- | :--------- | :-------------------- | :-------------------- | :---------- |
| 300  | 266041.84  | 264345.73  | 1.96                  | 2.07                  | -0.64       |
| 600  | 351782.71  | 348715.98  | 3.43                  | 3.49                  | -0.87       |
| 900  | 386553.31  | 399777.11  | 5.09                  | 4.74                  | 3.42        |

v5.3.0 と比較して、v5.4.0 のポイント選択パフォーマンスは 0.64% わずかに向上しています。

![Point Select](/media/sysbench_v530vsv540_point_select.png)

### インデックス以外のパフォーマンスを更新する {#update-non-index-performance}

| スレッド | v5.3.0 TPS | v5.4.0 TPS | v5.3.0 95%レイテンシー(ミリ秒) | v5.4.0 95%レイテンシー(ミリ秒) | TPS の向上 (%) |
| :--- | :--------- | :--------- | :-------------------- | :-------------------- | :---------- |
| 300  | 40804.31   | 41187.1    | 11.87                 | 11.87                 | 0.94        |
| 600  | 51239.4    | 53172.03   | 20.74                 | 19.65                 | 3.77        |
| 900  | 57897.56   | 59666.8    | 27.66                 | 27.66                 | 3.06        |

v5.3.0 と比較して、v5.4.0 の非インデックス更新のパフォーマンスは 2.59% 向上しています。

![Update Non-index](/media/sysbench_v530vsv540_update_non_index.png)

### インデックスのパフォーマンスを更新する {#update-index-performance}

| スレッド | v5.3.0 TPS | v5.4.0 TPS | v5.3.0 95%レイテンシー(ミリ秒) | v5.4.0 95%レイテンシー(ミリ秒) | TPS の向上 (%) |
| :--- | :--------- | :--------- | :-------------------- | :-------------------- | :---------- |
| 300  | 17737.82   | 18716.5    | 26.2                  | 24.83                 | 5.52        |
| 600  | 21614.39   | 22670.74   | 44.98                 | 42.61                 | 4.89        |
| 900  | 23933.7    | 24922.05   | 62.19                 | 61.08                 | 4.13        |

v5.3.0 と比較して、v5.4.0 の更新インデックスのパフォーマンスは 4.85% 向上しています。

![Update Index](/media/sysbench_v530vsv540_update_index.png)

### 読み取り/書き込みパフォーマンス {#read-write-performance}

| スレッド | v5.3.0 TPS | v5.4.0 TPS | v5.3.0 95%レイテンシー(ミリ秒) | v5.4.0 95%レイテンシー(ミリ秒) | TPS の向上 (%) |
| :--- | :--------- | :--------- | :-------------------- | :-------------------- | :---------- |
| 300  | 3810.78    | 3929.29    | 108.68                | 106.75                | 3.11        |
| 600  | 4514.28    | 4684.64    | 193.38                | 186.54                | 3.77        |
| 900  | 4842.49    | 4988.49    | 282.25                | 277.21                | 3.01        |

v5.3.0 と比較して、v5.4.0 の読み取り/書き込みパフォーマンスは 3.30% 向上しています。

![Read Write](/media/sysbench_v530vsv540_read_write.png)
