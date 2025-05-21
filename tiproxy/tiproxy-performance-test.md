---
title: TiProxy Performance Test Report
summary: TiProxy のパフォーマンスと HAProxy との比較について学びます。
---

# TiProxy パフォーマンステストレポート {#tiproxy-performance-test-report}

このレポートでは、Sysbench の OLTP シナリオで TiProxy のパフォーマンスをテストし、 [HAプロキシ](https://www.haproxy.org/)と比較します。

結果は次のとおりです。

-   TiProxy の QPS 上限はワークロードの種類によって影響を受けます。クライアントの同時実行数が同じで、TiProxy の CPU 使用率が 80% 未満の場合、QPS は HAProxy より 5% 未満低くなります。このような場合、クライアントの同時実行数を増やすことで QPS を改善できる場合が多くあります。同じ QPS の場合、TiProxy の CPU 使用率は HAProxy より約 25% 高くなります。そのため、より多くの CPU リソースを確保する必要があります。
-   TiProxyが保持できるTiDBサーバーインスタンスの数は、ワークロードの種類によって異なります。Sysbenchの基本ワークロードでは、TiProxyは同じモデルのTiDBサーバーインスタンスを5～12個保持できます。
-   クエリ結果セットの行数は TiProxy の QPS に大きな影響を与え、その影響は HAProxy の場合と同じです。
-   TiProxy のパフォーマンスは、vCPU の数にほぼ比例して向上します。そのため、vCPU の数を増やすことで、QPS の上限を効果的に向上させることができます。
-   長い接続の数と短い接続を作成する頻度は、TiProxy の QPS にほとんど影響を与えません。

## テスト環境 {#test-environment}

### ハードウェア構成 {#hardware-configuration}

| サービス    | 機械タイプ | CPUモデル                                     | インスタンス数 |
| ------- | ----- | ------------------------------------------ | ------- |
| TiProxy | 4C8G  | インテル(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 1       |
| HAプロキシ  | 4C8G  | インテル(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 1       |
| PD      | 4C8G  | インテル(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 3       |
| TiDB    | 8C16G | インテル(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 8       |
| TiKV    | 8C16G | インテル(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 8       |
| システムベンチ | 8C16G | インテル(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 1       |

### ソフトウェア {#software}

| サービス    | ソフトウェアバージョン |
| ------- | ----------- |
| TiProxy | バージョン1.0.0  |
| HAプロキシ  | 2.9.0       |
| PD      | バージョン8.0.0  |
| TiDB    | バージョン8.0.0  |
| TiKV    | バージョン8.0.0  |
| システムベンチ | 1.0.17      |

### コンフィグレーション {#configuration}

#### TiProxy の設定 {#tiproxy-configuration}

テストでは、クライアントと TiProxy 間、または TiProxy と TiDBサーバー間で TLS が有効になっていません。

```yaml
proxy.conn-buffer-size: 131072
```

#### HAProxy 設定 - <code>haproxy.cfg</code>ファイル {#haproxy-configuration-code-haproxy-cfg-code-file}

```yaml
global                                      # Global configuration.
    log         127.0.0.1 local2            # Specifies the global syslog server. You can define up to two.
    pidfile     /var/run/haproxy.pid        # Write the PID of the HAProxy process to pidfile.
    maxconn     4096                        # The maximum number of concurrent connections that a single HAProxy process can accept, equivalent to the command line parameter "-n".
    nbthread    4                           # The maximum number of threads. The upper limit of the number of threads is the same as the number of CPUs.
    user        haproxy                     # Same as UID parameter.
    group       haproxy                     # Same as GID parameter. A dedicated user group is recommended.
    daemon                                  # Run HAProxy as a daemon in the background, which is equivalent to the command line parameter "-D". You can also disable it with the "-db" parameter on the command line.
    stats socket /var/lib/haproxy/stats     # The location where the statistics are saved.

defaults                                    # Default configuration.
    log global                              # Inherit the settings of the global configuration section.
    retries 2                               # The maximum number of times to try to connect to the upstream server. If the number of retries exceeds this value, the backend server is considered unavailable.
    timeout connect  2s                     # The timeout period for HAProxy to connect to the backend server. If the server is located on the same LAN as HAProxy, set it to a shorter time.
    timeout client 30000s                   # The timeout period for the client to be inactive after the data transmission is completed.
    timeout server 30000s                   # The timeout period for the server to be inactive.

listen tidb-cluster                         # Configure database load balancing.
    bind 0.0.0.0:3390                       # Floating IP address and listening port.
    mode tcp                                # HAProxy uses layer 4, the transport layer.
    balance leastconn                      # The server with the least number of connections receives the connection first. `leastconn` is recommended for long session services, such as LDAP, SQL, and TSE, rather than short session protocols, such as HTTP. This algorithm is dynamic, and the server weight is adjusted during operation for slow-start servers.
    server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3      # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
    server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
    server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## 基本的な作業負荷テスト {#basic-workload-test}

### テスト計画 {#test-plan}

このテストは、ポイントセレクト、読み取り専用、書き込み専用、読み取り/書き込みの4種類のワークロードにおけるTiProxyとHAProxyのQPSを比較することを目的としています。各ワークロードは異なる同時実行性でテストされ、TiProxyとHAProxyのQPSを比較します。

テストを実行するには、次のコマンドを使用します。

```bash
sysbench $testname \
    --threads=$threads \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### ポイント選択 {#point-select}

TiProxy テスト結果:

| スレッド | QPS    | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | TiProxy CPU使用率 | TiDB 全体の CPU 使用率 |
| ---- | ------ | ------------- | -------------- | -------------- | ---------------- |
| 20   | 41273  | 0.48          | 0.64           | 190%           | 900%             |
| 50   | 100255 | 0.50          | 0.62           | 330%           | 1900%            |
| 100  | 137688 | 0.73          | 1.01           | 400%           | 2600%            |

HAProxy テスト結果:

| スレッド | QPS    | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | HAProxy CPU 使用率 | TiDB 全体の CPU 使用率 |
| ---- | ------ | ------------- | -------------- | --------------- | ---------------- |
| 20   | 44833  | 0.45          | 0.61           | 140%            | 1000%            |
| 50   | 103631 | 0.48          | 0.61           | 270%            | 2100%            |
| 100  | 163069 | 0.61          | 0.77           | 360%            | 3100%            |

### 読み取り専用 {#read-only}

TiProxy テスト結果:

| スレッド | QPS    | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | TiProxy CPU使用率 | TiDB 全体の CPU 使用率 |
| ---- | ------ | ------------- | -------------- | -------------- | ---------------- |
| 50   | 72076  | 11.09         | 12.75          | 290%           | 2500%            |
| 100  | 109704 | 14.58         | 17.63          | 370%           | 3800%            |
| 200  | 117519 | 27.21         | 32.53          | 400%           | 4100%            |

HAProxy テスト結果:

| スレッド | QPS    | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | HAProxy CPU 使用率 | TiDB 全体の CPU 使用率 |
| ---- | ------ | ------------- | -------------- | --------------- | ---------------- |
| 50   | 75760  | 10.56         | 12.08          | 250%            | 2600%            |
| 100  | 121730 | 13.14         | 15.83          | 350%            | 4200%            |
| 200  | 131712 | 24.27         | 30.26          | 370%            | 4500%            |

### 書き込み専用 {#write-only}

TiProxy テスト結果:

| スレッド | QPS    | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | TiProxy CPU使用率 | TiDB 全体の CPU 使用率 |
| ---- | ------ | ------------- | -------------- | -------------- | ---------------- |
| 100  | 81957  | 7.32          | 10.27          | 290%           | 3900%            |
| 300  | 103040 | 17.45         | 31.37          | 330%           | 4700%            |
| 500  | 104869 | 28.59         | 52.89          | 340%           | 4800%            |

HAProxy テスト結果:

| スレッド | QPS    | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | HAProxy CPU 使用率 | TiDB 全体の CPU 使用率 |
| ---- | ------ | ------------- | -------------- | --------------- | ---------------- |
| 100  | 81708  | 7.34          | 10.65          | 240%            | 3700%            |
| 300  | 106008 | 16.95         | 31.37          | 320%            | 4800%            |
| 500  | 122369 | 24.45         | 47.47          | 350%            | 5300%            |

### 読み書き {#read-write}

TiProxy テスト結果:

| スレッド | QPS    | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | TiProxy CPU使用率 | TiDB 全体の CPU 使用率 |
| ---- | ------ | ------------- | -------------- | -------------- | ---------------- |
| 50   | 58571  | 17.07         | 19.65          | 250%           | 2600%            |
| 100  | 88432  | 22.60         | 29.19          | 330%           | 3900%            |
| 200  | 108758 | 36.73         | 51.94          | 380%           | 4800%            |

HAProxy テスト結果:

| スレッド | QPS    | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | HAProxy CPU 使用率 | TiDB 全体の CPU 使用率 |
| ---- | ------ | ------------- | -------------- | --------------- | ---------------- |
| 50   | 61226  | 16.33         | 19.65          | 190%            | 2800%            |
| 100  | 96569  | 20.70         | 26.68          | 290%            | 4100%            |
| 200  | 120163 | 31.28         | 49.21          | 340%            | 5200%            |

## 結果セットテスト {#result-set-test}

### テスト計画 {#test-plan}

このテストは、異なる結果セット行数におけるTiProxyとHAProxyのパフォーマンスを比較することを目的としています。このテストでは、同時実行数を100に設定し、結果セット行数を10、100、1000、10000とした場合のTiProxyとHAProxyのQPSを比較します。

テストを実行するには、次のコマンドを使用します。

```bash
sysbench oltp_read_only \
    --threads=100 \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    --skip_trx=true \
    --point_selects=0 \
    --sum_ranges=0 \
    --order_ranges=0 \
    --distinct_ranges=0 \
    --simple_ranges=1 \
    --range_size=$range_size
    run --tables=32 --table-size=1000000
```

### テスト結果 {#test-results}

TiProxy テスト結果:

| 範囲サイズ | QPS   | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | TiProxy CPU使用率 | TiDB 全体の CPU 使用率 | 受信ネットワーク（MiB/秒） | 送信ネットワーク（MiB/秒） |
| ----- | ----- | ------------- | -------------- | -------------- | ---------------- | --------------- | --------------- |
| 10    | 80157 | 1.25          | 1.61           | 340%           | 2600%            | 140             | 140             |
| 100   | 55936 | 1.79          | 2.43           | 370%           | 2800%            | 820             | 820             |
| 1000  | 10313 | 9.69          | 13.70          | 310%           | 1500%            | 1370            | 1370            |
| 10000 | 1064  | 93.88         | 142.39         | 250%           | 600%             | 1430            | 1430            |

HAProxy テスト結果:

| 範囲サイズ | QPS   | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | HAProxy CPU 使用率 | TiDB 全体の CPU 使用率 | 受信ネットワーク（MiB/秒） | 送信ネットワーク（MiB/秒） |
| ----- | ----- | ------------- | -------------- | --------------- | ---------------- | --------------- | --------------- |
| 10    | 94376 | 1.06          | 1.30           | 250%            | 4000%            | 150             | 150             |
| 100   | 70129 | 1.42          | 1.76           | 270%            | 3300%            | 890             | 890             |
| 1000  | 9501  | 11.18         | 14.73          | 240%            | 1500%            | 1180            | 1180            |
| 10000 | 955   | 104.61        | 320.17         | 180%            | 1200%            | 1200            | 1200            |

## スケーラビリティテスト {#scalability-test}

### テスト計画 {#test-plan}

このテストは、TiProxy のパフォーマンスがスペックに比例しているかどうかを検証し、TiProxy のスペックをアップグレードすることで QPS の上限を向上できるかどうかを確認することを目的としています。このテストでは、vCPU 数と同時実行数が異なる TiProxy インスタンスを使用して QPS を比較します。

テストを実行するには、次のコマンドを使用します。

```bash
sysbench oltp_point_select \
    --threads=$threads \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### テスト結果 {#test-results}

| 仮想CPU | スレッド | QPS    | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | TiProxy CPU使用率 | TiDB 全体の CPU 使用率 |
| ----- | ---- | ------ | ------------- | -------------- | -------------- | ---------------- |
| 2     | 40   | 58508  | 0.68          | 0.97           | 190%           | 1200%            |
| 4     | 80   | 104890 | 0.76          | 1.16           | 390%           | 2000%            |
| 6     | 120  | 155520 | 0.77          | 1.14           | 590%           | 2900%            |
| 8     | 160  | 202134 | 0.79          | 1.18           | 800%           | 3900%            |

## 長時間接続テスト {#long-connection-test}

### テスト計画 {#test-plan}

このテストは、クライアントが長時間接続を使用する場合、多数のアイドル接続がQPSに最小限の影響しか与えないことを検証することを目的としています。このテストでは、5,000、10,000、15,000のアイドル状態の長時間接続を作成し、 `sysbench`実行します。

このテストでは、 `conn-buffer-size`構成のデフォルト値を使用します。

```yaml
proxy.conn-buffer-size: 32768
```

テストを実行するには、次のコマンドを使用します。

```bash
sysbench oltp_point_select \
    --threads=50 \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### テスト結果 {#test-results}

| 接続数   | QPS   | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | TiProxy CPU使用率 | TiProxyメモリ使用量 (MB) | TiDB 全体の CPU 使用率 |
| ----- | ----- | ------------- | -------------- | -------------- | ------------------ | ---------------- |
| 5000  | 96620 | 0.52          | 0.64           | 330%           | 920                | 1800%            |
| 10000 | 96143 | 0.52          | 0.65           | 330%           | 1710               | 1800%            |
| 15000 | 96048 | 0.52          | 0.65           | 330%           | 2570               | 1900%            |

## 短時間接続テスト {#short-connection-test}

### テスト計画 {#test-plan}

このテストは、クライアントが短い接続を使用する場合、頻繁な接続の作成と破棄がQPSに最小限の影響しか与えないことを検証することを目的としています。このテストでは、別のクライアントプログラムを起動し、 `sysbench`実行しながら、1秒あたり100、200、300の短い接続を作成および切断します。

テストを実行するには、次のコマンドを使用します。

```bash
sysbench oltp_point_select \
    --threads=50 \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### テスト結果 {#test-results}

| 1秒あたりの新規接続数 | QPS   | 平均レイテンシー（ミリ秒） | P95レイテンシー(ミリ秒) | TiProxy CPU使用率 | TiDB 全体の CPU 使用率 |
| ----------- | ----- | ------------- | -------------- | -------------- | ---------------- |
| 100         | 95597 | 0.52          | 0.65           | 330%           | 1800%            |
| 200         | 94692 | 0.53          | 0.67           | 330%           | 1800%            |
| 300         | 94102 | 0.53          | 0.68           | 330%           | 1900%            |
