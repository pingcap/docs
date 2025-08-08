---
title: Best Practices for Three-Node Hybrid Deployment
summary: TiDBクラスタは、3台のマシンでコスト効率よく導入できます。このハイブリッド導入におけるベストプラクティスとしては、安定性とパフォーマンスを向上させるためのパラメータ調整が挙げられます。リソース消費量の制限とスレッドプールサイズの調整は、クラスタを最適化する上で重要です。TiKVバックグラウンドタスクとTiDB実行オペレータのパラメータ調整も重要です。
---

# 3ノードハイブリッド展開のベストプラクティス {#best-practices-for-three-node-hybrid-deployment}

TiDB クラスターの場合、高パフォーマンスは要求されないもののコストを制御する必要がある場合は、TiDB、TiKV、PD コンポーネントを 3 台のマシンにハイブリッド方式で展開できます。

このドキュメントでは、3ノードのハイブリッド展開例と、展開されたクラスターに対するTPC-Cテストを紹介します。この例に基づいて、展開シナリオとそのパラメータ調整に関するベストプラクティスを紹介します。

## 展開の前提条件とテスト方法 {#prerequisites-for-deployment-and-the-test-method}

この例では、16個のCPUコアと32GBのメモリを搭載した3台の物理マシンがデプロイメントに使用されます。各マシン（ノード）には、TiDBインスタンス、TiKVインスタンス、PDインスタンスがそれぞれ1つずつ、ハイブリッド方式でデプロイされます。

PDとTiKVはどちらもディスク上に情報を保存するため、ディスクの読み取りおよび書き込みレイテンシーはPDおよびTiKVサービスのレイテンシーに直接影響します。PDとTiKVがディスクリソースを競合し、互いに影響を与える状況を回避するため、PDとTiKVには異なるディスクを使用することをお勧めします。

この例では、TPC-C 5000 WarehouseのデータをTiUPベンチで使用し、パラメータ`terminals`を`128` （同時実行）に設定して12時間テストを実施します。クラスターのパフォーマンス安定性に関連するメトリクスに細心の注意を払います。

下の画像は、デフォルトのパラメータ設定で12時間以内にクラスターのQPSをモニターしたデータです。画像から明らかなパフォーマンスのジッターが確認できます。

![QPS with default config](/media/best-practices/three-nodes-default-config-qps.png)

パラメータ調整後、パフォーマンスが向上します。

![QPS with modified config](/media/best-practices/three-nodes-final-config-qps.png)

## パラメータ調整 {#parameter-adjustment}

上の画像では、デフォルトのスレッドプール構成とバックグラウンドタスクへのリソース割り当てが、十分なリソースを持つマシン向けに設定されているため、パフォーマンスのジッターが発生しています。ハイブリッド展開シナリオでは、リソースが複数のコンポーネント間で共有されるため、構成パラメータによってリソース消費を制限する必要があります。

このテストの最終的なクラスター構成は次のとおりです。

```yaml
tikv:
    readpool.unified.max-thread-count: 6
    server.grpc-concurrency: 2
    storage.scheduler-worker-pool-size: 2
    gc.max-write-bytes-per-sec: 300K
    rocksdb.max-background-jobs: 3
    rocksdb.max-sub-compactions: 1
    rocksdb.rate-bytes-per-sec: "200M"

  tidb:
    performance.max-procs: 8
```

以下のセクションでは、これらのパラメータの意味と調整方法を紹介します。

### TiKVスレッドプールサイズのコンフィグレーション {#configuration-of-tikv-thread-pool-size}

このセクションでは、フォアグラウンドアプリケーションのスレッドプールのリソース割り当てに関連するパラメータを調整するためのベストプラクティスを紹介します。これらのスレッドプールサイズを縮小するとパフォーマンスが低下しますが、リソースが限られているハイブリッド展開シナリオでは、クラスター自体で高いパフォーマンスを達成することは困難です。このシナリオでは、パフォーマンスよりもクラスター全体の安定性が優先されます。

実際の負荷テストを実施する場合は、まずデフォルト設定を使用して、各スレッドプールの実際のリソース使用量を観察します。その後、関連する設定項目を調整し、使用量が少ないスレッドプールのサイズを縮小します。

#### <code>readpool.unified.max-thread-count</code> {#code-readpool-unified-max-thread-count-code}

このパラメータのデフォルト値は、マシンのスレッド数の80%です。ハイブリッド展開シナリオでは、この値を手動で計算して指定する必要があります。まずは、TiKVが使用するCPUスレッド数の80%に設定することをお勧めします。

#### <code>server.grpc-concurrency</code> {#code-server-grpc-concurrency-code}

このパラメータのデフォルトは`4`です。既存のデプロイメントプランではCPUリソースが限られており、実際のリクエスト数も少ないためです。監視パネルを監視し、このパラメータの値を下げて使用率を80%未満に保つことができます。

このテストでは、このパラメータの値は`2`に設定されています。gRPC**ポーリング CPU**パネルを確認すると、使用率が約 80% であることがわかります。

![gRPC Pool CPU](/media/best-practices/three-nodes-grpc-pool-usage.png)

#### <code>storage.scheduler-worker-pool-size</code> {#code-storage-scheduler-worker-pool-size-code}

TiKVがマシンのCPUコア数が`16`以上であることを検出すると、このパラメータ値はデフォルトで`8`に設定されます。CPUコア数が`16`未満の場合、このパラメータ値はデフォルトで`4`に設定されます。このパラメータは、TiKVが複雑なトランザクション要求を単純なキー値の読み取りまたは書き込みに変換するものの、スケジューラスレッドプールが書き込みを実行しない場合に使用されます。

理想的には、スケジューラスレッドプールの使用率は50%～75%に維持されます。gRPCスレッドプールと同様に、ハイブリッド展開中はパラメータ`storage.scheduler-worker-pool-size`デフォルトで大きな値に設定され、リソースの使用量が不足する可能性があります。このテストでは、このパラメータの値はベストプラクティスに沿って`2`に設定されており、これは**スケジューラワーカーCPU**パネルの対応するメトリックを観察した結果に基づいています。

![Scheduler Worker CPU](/media/best-practices/three-nodes-scheduler-pool-usage.png)

### TiKVバックグラウンドタスクのリソース構成 {#resource-configuration-for-tikv-background-tasks}

TiKVはフォアグラウンドタスクに加えて、バックグラウンドタスクでも定期的にデータのソートと古いデータの削除を実行します。デフォルト設定では、高トラフィックの書き込みシナリオに対応できるよう、これらのタスクに十分なリソースが割り当てられます。

ただし、ハイブリッド展開シナリオでは、このデフォルト構成はベストプラクティスに準拠していません。以下のパラメータを調整して、バックグラウンドタスクのリソース使用量を制限する必要があります。

#### <code>rocksdb.max-background-jobs</code>と<code>rocksdb.max-sub-compactions</code> {#code-rocksdb-max-background-jobs-code-and-code-rocksdb-max-sub-compactions-code}

RocksDBスレッドプールは、コンパクションジョブとフラッシュジョブを実行するために使用されます。デフォルト値は`rocksdb.max-background-jobs`ですが、 `8`設定されており、明らかに必要なリソースを超えています。そのため、リソース使用量を制限するために値を調整する必要があります。

`rocksdb.max-sub-compactions` 、単一の圧縮ジョブで許可される同時サブタスクの数を示します。デフォルトは`3`です。書き込みトラフィックが多くない場合は、この値を下げることができます。

このテストでは、 `rocksdb.max-background-jobs`値は`3` `rocksdb.max-sub-compactions`値は`1`に設定されています。TPC-C負荷での12時間テスト中、書き込みストールは発生しませんでした。実際の負荷に応じて2つのパラメータ値を最適化する際は、監視指標に基づいて値を徐々に下げることができます。

-   書き込み停止が発生する場合は、値を`rocksdb.max-background-jobs`増やします。
-   書き込み停止が続く場合は、値`rocksdb.max-sub-compactions`を`2`または`3`に設定します。

#### <code>rocksdb.rate-bytes-per-sec</code> {#code-rocksdb-rate-bytes-per-sec-code}

このパラメータは、バックグラウンド圧縮ジョブのディスクトラフィックを制限するために使用されます。デフォルト設定では、このパラメータに制限はありません。圧縮ジョブがフォアグラウンドサービスのリソースを占有する状況を回避するには、ディスクのシーケンシャル読み取りおよび書き込み速度に応じてこのパラメータ値を調整し、フォアグラウンドサービスに十分なディスク帯域幅を確保します。

RocksDBスレッドプールの最適化方法は、コンパクションスレッドプールの最適化方法と似ています。書き込みストールが発生するかどうかで、調整した値が適切かどうかを判断できます。

#### <code>gc.max_write_bytes_per_sec</code> {#code-gc-max-write-bytes-per-sec-code}

TiDBはマルチバージョン同時実行制御（MVCC）モデルを使用しているため、TiKVは定期的に古いバージョンのデータをバックグラウンドで消去します。利用可能なリソースが限られている場合、この操作によって定期的なパフォーマンスジッターが発生します。1パラメータ`gc.max_write_bytes_per_sec`使用すると、このような操作のリソース使用量を制限できます。

![GC Impact](/media/best-practices/three-nodes-gc-impact.png)

設定ファイルでこのパラメータ値を設定するだけでなく、tikv-ctl でこの値を動的に調整することもできます。

```shell
tiup ctl:v<CLUSTER_VERSION> tikv --host=${ip:port} modify-tikv-config -n gc.max_write_bytes_per_sec -v ${limit}
```

> **注記：**
>
> 頻繁に更新されるアプリケーションシナリオでは、GCトラフィックを制限するとMVCCバージョンが蓄積され、読み取りパフォーマンスに影響する可能性があります。現在、パフォーマンスジッターとパフォーマンス低下のバランスをとるには、このパラメータの値を複数回調整する必要がある可能性があります。

### TiDBパラメータ調整 {#tidb-parameter-adjustment}

通常、 `tidb_hash_join_concurrency`や`tidb_index_lookup_join_concurrency`などのシステム変数を使用して、実行オペレータの TiDB パラメータを調整できます。

このテストでは、これらのパラメータは調整されていません。実際のアプリケーションの負荷テストにおいて、実行オペレータがCPUリソースを過度に消費する場合は、アプリケーションのシナリオに応じて特定のオペレータのリソース使用量を制限することができます。詳細については、 [TiDB システム変数](/system-variables.md)参照してください。

#### <code>performance.max-procs</code> {#code-performance-max-procs-code}

このパラメータは、Goプロセス全体で使用できるCPUコアの数を制御するために使用されます。デフォルトでは、この値は現在のマシンまたはcgroupのCPUコア数と同じです。

Goの実行中、GCなどの`performance.max-procs`グラウンドタスクには一定量のスレッドが使用されます。1パラメータの値を制限しないと、これらのバックグラウンドタスクがCPUを過剰に消費することになります。
