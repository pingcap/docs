---
title: TiDB Sysbench Performance Test Report -- v6.1.0 vs. v6.0.0
---

# TiDBSysbenchパフォーマンステストレポート-v6.1.0とv6.0.0 {#tidb-sysbench-performance-test-report-v6-1-0-vs-v6-0-0}

## テストの概要 {#test-overview}

このテストは、オンライントランザクション処理（OLTP）シナリオでのTiDBv6.1.0とTiDBv6.0.0のSysbenchパフォーマンスを比較することを目的としています。結果は、v6.1.0のパフォーマンスが書き込みワークロードで改善されていることを示しています。書き込みの多いワークロードのパフォーマンスは、2.33％〜4.61％向上します。

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
| PD       | v6.0.0およびv6.1.0 |
| TiDB     | v6.0.0およびv6.1.0 |
| TiKV     | v6.0.0およびv6.1.0 |
| Sysbench | 1.1.0-df89d34   |

### パラメータ設定 {#parameter-configuration}

TiDBv6.1.0とTiDBv6.0.0は同じ構成を使用します。

#### TiDBパラメータ設定 {#tidb-parameter-configuration}

{{< copyable "" >}}

```yaml
log.level: "error"
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
server.grpc-concurrency: 6
readpool.storage.normal-concurrency: 10
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
set global tidb_prepared_plan_cache_size=1000;
```

#### HAProxy設定-haproxy.cfg {#haproxy-configuration-haproxy-cfg}

TiDBでHAProxyを使用する方法の詳細については、 [TiDBでHAProxyを使用するためのベストプラクティス](/best-practices/haproxy-best-practices.md)を参照してください。

{{< copyable "" >}}

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

1.  TiUPを使用してTiDBv6.1.0およびv6.0.0をデプロイします。
2.  Sysbenchを使用して、16個のテーブルをインポートします。各テーブルには、1,000万行のデータが含まれています。
3.  各テーブルで`analyze table`のステートメントを実行します。
4.  さまざまな同時実行テストの前に復元に使用されるデータをバックアップします。これにより、各テストのデータの一貫性が保証されます。
5.  `read_write`クライアントを起動して、 `point_select` 、および`update_index`のテストを実行し`update_non_index` 。 HAProxyを介してTiDBでストレステストを実行します。各ワークロードでの同時実行ごとに、テストには20分かかります。
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

| スレッド | v6.0.0 TPS | v6.1.0 TPS | v6.0.0 95％レイテンシ（ミリ秒） | v6.1.0 95％レイテンシ（ミリ秒） | TPSの改善（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 268934.84  | 265353.15  | 1.89                 | 1.96                 | -1.33     |
| 600  | 365217.96  | 358976.94  | 2.57                 | 2.66                 | -1.71     |
| 900  | 420799.64  | 407625.11  | 3.68                 | 3.82                 | -3.13     |

v6.0.0と比較すると、v6.1.0のポイント選択のパフォーマンスは2.1％わずかに低下します。

![Point Select](/media/sysbench_v600vsv610_point_select.png)

### 非インデックスパフォーマンスの更新 {#update-non-index-performance}

| スレッド | v6.0.0 TPS | v6.1.0 TPS | v6.0.0 95％レイテンシ（ミリ秒） | v6.1.0 95％レイテンシ（ミリ秒） | TPSの改善（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 41778.95   | 42991.9    | 11.24                | 11.45                | 2.90      |
| 600  | 52045.39   | 54099.58   | 20.74                | 20.37                | 3.95      |
| 900  | 59243.35   | 62084.65   | 27.66                | 26.68                | 4.80      |

v6.0.0と比較して、v6.1.0の非インデックス更新のパフォーマンスは3.88％向上しています。

![Update Non-index](/media/sysbench_v600vsv610_update_non_index.png)

### インデックスパフォーマンスの更新 {#update-index-performance}

| スレッド | v6.0.0 TPS | v6.1.0 TPS | v6.0.0 95％レイテンシ（ミリ秒） | v6.1.0 95％レイテンシ（ミリ秒） | TPSの改善（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 18085.79   | 19198.89   | 25.28                | 23.95                | 6.15      |
| 600  | 22210.8    | 22877.58   | 42.61                | 41.85                | 3.00      |
| 900  | 25249.81   | 26431.12   | 55.82                | 53.85                | 4.68      |

v6.0.0と比較して、v6.1.0の更新インデックスのパフォーマンスは4.61％向上しています。

![Update Index](/media/sysbench_v600vsv610_update_index.png)

### 読み取り/書き込みパフォーマンス {#read-write-performance}

| スレッド | v6.0.0 TPS | v6.1.0 TPS | v6.0.0 95％レイテンシ（ミリ秒） | v6.1.0 95％レイテンシ（ミリ秒） | TPSの改善（％） |
| :--- | :--------- | :--------- | :------------------- | :------------------- | :-------- |
| 300  | 4856.23    | 4914.11    | 84.47                | 82.96                | 1.19      |
| 600  | 5676.46    | 5848.09    | 161.51               | 150.29               | 3.02      |
| 900  | 6072.97    | 6223.95    | 240.02               | 223.34               | 2.49      |

v6.0.0と比較して、v6.1.0の読み取り/書き込みパフォーマンスは2.23％向上しています。

![Read Write](/media/sysbench_v600vsv610_read_write.png)
