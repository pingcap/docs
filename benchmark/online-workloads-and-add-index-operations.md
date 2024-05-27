---
title: Interaction Test on Online Workloads and `ADD INDEX` Operations
summary: このドキュメントでは、オンライン ワークロードと `ADD INDEX` 操作間の相互作用効果をテストします。
---

# オンライン ワークロードと<code>ADD INDEX</code>操作のインタラクション テスト {#interaction-test-on-online-workloads-and-code-add-index-code-operations}

## テスト目的 {#test-purpose}

このドキュメントでは、OLTP シナリオにおけるオンライン ワークロードと`ADD INDEX`操作間の相互作用効果をテストします。

## テストバージョン、時間、場所 {#test-version-time-and-place}

TiDB バージョン: v3.0.1

日時: 2019年7月

場所: 北京

## テスト環境 {#test-environment}

このテストは、3 つの TiDB インスタンス、3 つの TiKV インスタンス、3 つの PD インスタンスがデプロイされた Kubernetes クラスターで実行されます。

### バージョン情報 {#version-information}

| 成分   | ギットハッシュ                                    |
| :--- | :----------------------------------------- |
| ティビ  | `9e4e8da3c58c65123db5f26409759fe1847529f8` |
| ティクヴ | `4151dc8878985df191b47851d67ca21365396133` |
| PD   | `811ce0b9a1335d1b2a049fd97ef9e186f1c9efc1` |

Sysbench バージョン: 1.0.17

### TiDBパラメータ設定 {#tidb-parameter-configuration}

TiDB、TiKV、PD はすべてデフォルト[TiDB Operator](https://github.com/pingcap/tidb-operator)構成を使用します。

### クラスタトポロジー {#cluster-topology}

| マシンIP                                  | デプロイメントインスタンス |
| :------------------------------------- | :------------ |
| 172.31.8.8                             | システムベンチ       |
| 172.31.7.69、172.31.5.152、172.31.11.133 | PD            |
| 172.31.4.172、172.31.1.155、172.31.9.210 | ティクヴ          |
| 172.31.7.80、172.31.5.163、172.31.11.123 | ティビ           |

### Sysbench を使用したオンライン ワークロード シミュレーション {#online-workloads-simulation-using-sysbench}

Sysbench を使用して、 **2,000,000 行のデータを含むテーブルを**Kubernetes クラスターにインポートします。

データをインポートするには、次のコマンドを実行します。

```sh
sysbench oltp_common \
    --threads=16 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    prepare --tables=1 --table-size=2000000
```

テストを実行するには、次のコマンドを実行します。

```sh
sysbench $testname \
    --threads=$threads \
    --time=300000 \
    --report-interval=15 \
    --rand-type=uniform \
    --rand-seed=$RANDOM \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    run --tables=1 --table-size=2000000
```

## テストプラン1: <code>ADD INDEX</code>ステートメントのターゲット列への書き込み操作を頻繁に実行する {#test-plan-1-frequently-perform-write-operations-to-the-target-column-of-the-code-add-index-code-statement}

1.  `oltp_read_write`目のテストを開始します。
2.  手順 1 と同時に実行します。1 `alter table sbtest1 add index c_idx(c)`使用してインデックスを追加します。
3.  ステップ 2 の最後に実行します。インデックスが正常に追加されたら、テスト`oltp_read_write`を停止します。
4.  `alter table ... add index`の期間と、この期間の Sysbench の平均 TPS と QPS を取得します。
5.  2 つのパラメータ`tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`の値を徐々に増やし、手順 1 ～ 4 を繰り返します。

### 試験結果 {#test-results}

#### <code>ADD INDEX</code>操作なしの<code>oltp_read_write</code>のテスト結果 {#test-result-of-code-oltp-read-write-code-without-code-add-index-code-operations}

| sysbench TPS | sysbench QPS |
| :----------- | :----------- |
| 350.31       | 6806         |

#### <code>tidb_ddl_reorg_batch_size = 32</code> {#code-tidb-ddl-reorg-batch-size-32-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 402           | 338.4        | 6776         |
| 2                         | 266           | 330.3        | 6001         |
| 4                         | 174           | 288.5        | 5769         |
| 8                         | 129           | 280.6        | 5612         |
| 16                        | 90            | 263.5        | 5273         |
| 32                        | 54            | 229.2        | 4583         |
| 48                        | 57            | 230.1        | 4601         |

![add-index-load-1-b32](/media/add-index-load-1-b32.png)

#### <code>tidb_ddl_reorg_batch_size = 64</code> {#code-tidb-ddl-reorg-batch-size-64-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 264           | 269.4        | 5388         |
| 2                         | 163           | 266.2        | 5324         |
| 4                         | 105           | 272.5        | 5430         |
| 8                         | 78            | 262.5        | 5228         |
| 16                        | 57            | 215.5        | 4308         |
| 32                        | 42            | 185.2        | 3715         |
| 48                        | 45            | 189.2        | 3794         |

![add-index-load-1-b64](/media/add-index-load-1-b64.png)

#### <code>tidb_ddl_reorg_batch_size = 128</code> {#code-tidb-ddl-reorg-batch-size-128-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 171           | 289.1        | 5779         |
| 2                         | 110           | 274.2        | 5485         |
| 4                         | 79            | 250.6        | 5011         |
| 8                         | 51            | 246.1        | 4922         |
| 16                        | 39            | 171.1        | 3431         |
| 32                        | 35            | 130.8        | 2629         |
| 48                        | 35            | 120.5        | 2425         |

![add-index-load-1-b128](/media/add-index-load-1-b128.png)

#### <code>tidb_ddl_reorg_batch_size = 256</code> {#code-tidb-ddl-reorg-batch-size-256-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 145           | 283.0        | 5659         |
| 2                         | 96            | 282.2        | 5593         |
| 4                         | 56            | 236.5        | 4735         |
| 8                         | 45            | 194.2        | 3882         |
| 16                        | 39            | 149.3        | 2893         |
| 32                        | 36            | 113.5        | 2268         |
| 48                        | 33            | 86.2         | 1715         |

![add-index-load-1-b256](/media/add-index-load-1-b256.png)

#### <code>tidb_ddl_reorg_batch_size = 512</code> {#code-tidb-ddl-reorg-batch-size-512-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 135           | 257.8        | 5147         |
| 2                         | 78            | 252.8        | 5053         |
| 4                         | 49            | 222.7        | 4478         |
| 8                         | 36            | 145.4        | 2904         |
| 16                        | 33            | 109          | 2190         |
| 32                        | 33            | 72.5         | 1503         |
| 48                        | 33            | 54.2         | 1318         |

![add-index-load-1-b512](/media/add-index-load-1-b512.png)

#### <code>tidb_ddl_reorg_batch_size = 1024</code> {#code-tidb-ddl-reorg-batch-size-1024-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 111           | 244.3        | 4885         |
| 2                         | 78            | 228.4        | 4573         |
| 4                         | 54            | 168.8        | 3320         |
| 8                         | 39            | 123.8        | 2475         |
| 16                        | 36            | 59.6         | 1213         |
| 32                        | 42            | 93.2         | 1835         |
| 48                        | 51            | 115.7        | 2261         |

![add-index-load-1-b1024](/media/add-index-load-1-b1024.png)

#### <code>tidb_ddl_reorg_batch_size = 2048</code> {#code-tidb-ddl-reorg-batch-size-2048-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 918           | 243.3        | 4855         |
| 2                         | 1160          | 209.9        | 4194         |
| 4                         | 342           | 185.4        | 3707         |
| 8                         | 1316          | 151.0        | 3027         |
| 16                        | 795           | 30.5         | 679          |
| 32                        | 1130          | 26.69        | 547          |
| 48                        | 893           | 27.5         | 552          |

![add-index-load-1-b2048](/media/add-index-load-1-b2048.png)

#### <code>tidb_ddl_reorg_batch_size = 4096</code> {#code-tidb-ddl-reorg-batch-size-4096-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 3042          | 200.0        | 4001         |
| 2                         | 3022          | 203.8        | 4076         |
| 4                         | 858           | 195.5        | 3971         |
| 8                         | 3015          | 177.1        | 3522         |
| 16                        | 837           | 143.8        | 2875         |
| 32                        | 942           | 114          | 2267         |
| 48                        | 187           | 54.2         | 1416         |

![add-index-load-1-b4096](/media/add-index-load-1-b4096.png)

### テストの結論 {#test-conclusion}

`ADD INDEX`文のターゲット列に対して頻繁に書き込み操作 (このテストには`UPDATE` 、および`DELETE` `INSERT`が含まれます) を実行すると、デフォルトの`ADD INDEX`構成はシステムのオンライン ワークロードに大きな影響を与えます。これは主に、同時操作`ADD INDEX`と列更新によって発生する書き込み競合が原因です。システムのパフォーマンスは次のようになります。

-   パラメータ`tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`の値が増加すると、パラメータ`TiKV_prewrite_latch_wait_duration`の値が大幅に増加し、書き込み速度が低下します。
-   `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`の値が非常に大きい場合は、 `admin show ddl`コマンドを実行して、 `Write conflict, txnStartTS 410327455965380624 is stale [try again later], ErrCount:38, SnapshotVersion: 410327228136030220`などの DDL ジョブの再試行を複数回確認できます。この状況では、 `ADD INDEX`操作の完了に非常に長い時間がかかります。

## テストプラン 2: <code>ADD INDEX</code>ステートメントのターゲット列への書き込み操作を実行しない (クエリのみ) {#test-plan-2-do-not-perform-write-operations-to-the-target-column-of-the-code-add-index-code-statement-query-only}

1.  `oltp_read_only`目のテストを開始します。
2.  手順 1 と同時に実行します。1 `alter table sbtest1 add index c_idx(c)`使用してインデックスを追加します。
3.  ステップ 2 の最後に実行します。インデックスが正常に追加されたら、テスト`oltp_read_only`を停止します。
4.  `alter table ... add index`の期間と、この期間の Sysbench の平均 TPS と QPS を取得します。
5.  2 つのパラメータ`tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`の値を徐々に増やし、手順 1 ～ 4 を繰り返します。

### 試験結果 {#test-results}

#### <code>ADD INDEX</code>操作なしの<code>oltp_read_only</code>のテスト結果 {#test-result-of-code-oltp-read-only-code-without-code-add-index-code-operations}

| sysbench TPS | sysbench QPS |
| :----------- | :----------- |
| 550.9        | 8812.8       |

#### <code>tidb_ddl_reorg_batch_size = 32</code> {#code-tidb-ddl-reorg-batch-size-32-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 376           | 548.9        | 8780         |
| 2                         | 212           | 541.5        | 8523         |
| 4                         | 135           | 538.6        | 8549         |
| 8                         | 114           | 536.7        | 8393         |
| 16                        | 77            | 533.9        | 8292         |
| 32                        | 46            | 533.4        | 8103         |
| 48                        | 46            | 532.2        | 8074         |

![add-index-load-2-b32](/media/add-index-load-2-b32.png)

#### <code>tidb_ddl_reorg_batch_size = 1024</code> {#code-tidb-ddl-reorg-batch-size-1024-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 91            | 536.8        | 8316         |
| 2                         | 52            | 533.9        | 8165         |
| 4                         | 40            | 522.4        | 7947         |
| 8                         | 36            | 510          | 7860         |
| 16                        | 33            | 485.5        | 7704         |
| 32                        | 31            | 467.5        | 7516         |
| 48                        | 30            | 562.1        | 7442         |

![add-index-load-2-b1024](/media/add-index-load-2-b1024.png)

#### <code>tidb_ddl_reorg_batch_size = 4096</code> {#code-tidb-ddl-reorg-batch-size-4096-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 103           | 502.2        | 7823         |
| 2                         | 63            | 486.5        | 7672         |
| 4                         | 52            | 467.4        | 7516         |
| 8                         | 39            | 452.5        | 7302         |
| 16                        | 35            | 447.2        | 7206         |
| 32                        | 30            | 441.9        | 7057         |
| 48                        | 30            | 440.1        | 7004         |

![add-index-load-2-b4096](/media/add-index-load-2-b4096.png)

### テストの結論 {#test-conclusion}

`ADD INDEX`番目のステートメントのターゲット列に対してのみクエリ操作を実行する場合、 `ADD INDEX`の操作がオンライン ワークロードに与える影響は明らかではありません。

## テストプラン3: <code>ADD INDEX</code>ステートメントのターゲット列はオンラインワークロードとは無関係です {#test-plan-3-the-target-column-of-the-code-add-index-code-statement-is-irrelevant-to-online-workloads}

1.  `oltp_read_write`目のテストを開始します。
2.  手順 1 と同時に実行します。1 `alter table test add index pad_idx(pad)`使用してインデックスを追加します。
3.  ステップ 2 の最後に実行します。インデックスが正常に追加されたら、テスト`oltp_read_only`を停止します。
4.  `alter table ... add index`の期間と、この期間の Sysbench の平均 TPS と QPS を取得します。
5.  2 つのパラメータ`tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`の値を徐々に増やし、手順 1 ～ 4 を繰り返します。

### 試験結果 {#test-results}

### <code>ADD INDEX</code>操作なしの<code>oltp_read_write</code>のテスト結果 {#test-result-of-code-oltp-read-write-code-without-code-add-index-code-operations}

| sysbench TPS | sysbench QPS |
| :----------- | :----------- |
| 350.31       | 6806         |

#### <code>tidb_ddl_reorg_batch_size = 32</code> {#code-tidb-ddl-reorg-batch-size-32-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 372           | 350.4        | 6892         |
| 2                         | 207           | 344.2        | 6700         |
| 4                         | 140           | 343.1        | 6672         |
| 8                         | 121           | 339.1        | 6579         |
| 16                        | 76            | 340          | 6607         |
| 32                        | 42            | 343.1        | 6695         |
| 48                        | 42            | 333.4        | 6454         |

![add-index-load-3-b32](/media/add-index-load-3-b32.png)

#### <code>tidb_ddl_reorg_batch_size = 1024</code> {#code-tidb-ddl-reorg-batch-size-1024-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 94            | 352.4        | 6794         |
| 2                         | 50            | 332          | 6493         |
| 4                         | 45            | 330          | 6456         |
| 8                         | 36            | 325.5        | 6324         |
| 16                        | 32            | 312.5        | 6294         |
| 32                        | 32            | 300.6        | 6017         |
| 48                        | 31            | 279.5        | 5612         |

![add-index-load-3-b1024](/media/add-index-load-3-b1024.png)

#### <code>tidb_ddl_reorg_batch_size = 4096</code> {#code-tidb-ddl-reorg-batch-size-4096-code}

| tidb_ddl_reorg_worker_cnt | インデックス期間を追加する | sysbench TPS | sysbench QPS |
| :------------------------ | :------------ | :----------- | :----------- |
| 1                         | 116           | 325.5        | 6324         |
| 2                         | 65            | 312.5        | 6290         |
| 4                         | 50            | 300.6        | 6017         |
| 8                         | 37            | 279.5        | 5612         |
| 16                        | 34            | 250.4        | 5365         |
| 32                        | 32            | 220.2        | 4924         |
| 48                        | 33            | 214.8        | 4544         |

![add-index-load-3-b4096](/media/add-index-load-3-b4096.png)

### テストの結論 {#test-conclusion}

`ADD INDEX`番目のステートメントのターゲット列がオンライン ワークロードに関係ない場合、 `ADD INDEX`の操作がワークロードに与える影響は明らかではありません。

## まとめ {#summary}

-   `ADD INDEX`ステートメントのターゲット列に対して頻繁に書き込み操作 ( `INSERT` `UPDATE`を含む) を実行すると、デフォルト`DELETE` `ADD INDEX`構成では比較的頻繁に書き込み競合が発生し、オンライン ワークロードに大きな影響を与えます。同時に、 `ADD INDEX`操作は再試行が連続するため、完了するまでに長い時間がかかります。このテストでは、 `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`の積をデフォルト値の 1/32 に変更できます。たとえば、 `tidb_ddl_reorg_worker_cnt`を`4`に、 `tidb_ddl_reorg_batch_size`を`256`に設定すると、パフォーマンスが向上します。
-   `ADD INDEX`ステートメントのターゲット列に対してのみクエリ操作を実行する場合、またはターゲット列がオンライン ワークロードに直接関連していない場合は、デフォルトの`ADD INDEX`構成を使用できます。
