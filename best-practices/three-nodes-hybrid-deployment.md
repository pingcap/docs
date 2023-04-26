---
title: Best Practices for Three-Node Hybrid Deployment
summary: Learn the best practices for three-node hybrid deployment.
---

# 3 ノード ハイブリッド展開のベスト プラクティス {#best-practices-for-three-node-hybrid-deployment}

TiDB クラスターの場合、高パフォーマンスの要件はないがコストを制御する必要がある場合は、TiDB、TiKV、および PD コンポーネントを 3 台のマシンにハイブリッド方式でデプロイできます。

このドキュメントでは、3 ノード ハイブリッド展開の例と、展開されたクラスターに対する TPC-C テストを提供します。この例に基づいて、このドキュメントでは、展開シナリオとそのパラメーター調整のベスト プラクティスを提供します。

## 展開の前提条件とテスト方法 {#prerequisites-for-deployment-and-the-test-method}

この例では、デプロイに 3 台の物理マシンが使用され、それぞれに 16 個の CPU コアと 32 GB のメモリが搭載されています。各マシン (ノード) には、1 つの TiDB インスタンス、1 つの TiKV インスタンス、および 1 つの PD インスタンスがハイブリッド方式でデプロイされます。

PD と TiKV はどちらも情報をディスクに保存するため、ディスクの読み取りと書き込みのレイテンシーは PD と TiKV サービスのレイテンシーに直接影響します。 PD と TiKV がディスク リソースを競合して相互に影響を与えるという状況を回避するには、PD と TiKV に別のディスクを使用することをお勧めします。

この例では、TPC-C 5000 Warehouse データがTiUPベンチで使用され、テストは`terminals`パラメータを`128` (同時実行) に設定して 12 時間続きます。クラスターのパフォーマンスの安定性に関連するメトリックには細心の注意が払われます。

以下の画像は、デフォルトのパラメーター構成を使用した 12 時間以内のクラスターの QPS モニターを示しています。画像から明らかなパフォーマンスのジッターを見ることができます。

![QPS with default config](/media/best-practices/three-nodes-default-config-qps.png)

パラメータ調整後、パフォーマンスが向上しました。

![QPS with modified config](/media/best-practices/three-nodes-final-config-qps.png)

## パラメータ調整 {#parameter-adjustment}

デフォルトのスレッド プール構成とバックグラウンド タスクへのリソース割り当ては、十分なリソースを持つマシン向けであるため、上の画像ではパフォーマンスのジッターが発生しています。ハイブリッド展開シナリオでは、リソースが複数のコンポーネント間で共有されるため、構成パラメーターを使用してリソースの消費を制限する必要があります。

このテストの最終的なクラスター構成は次のとおりです。

{{< copyable "" >}}

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

以下に、これらのパラメータの意味と調整方法を紹介します。

### TiKV スレッド プール サイズのコンフィグレーション {#configuration-of-tikv-thread-pool-size}

このセクションでは、フォアグラウンド アプリケーションのスレッド プールのリソース割り当てに関連するパラメーターを調整するためのベスト プラクティスを紹介します。これらのスレッド プール サイズを小さくするとパフォーマンスが低下しますが、リソースが限られているハイブリッド展開シナリオでは、クラスター自体が高いパフォーマンスを達成するのは困難です。このシナリオでは、クラスターの全体的な安定性がパフォーマンスより優先されます。

実際の負荷テストを実施する場合は、最初に既定の構成を使用して、各スレッド プールの実際のリソース使用量を観察できます。次に、対応する構成項目を調整して、使用率の低いスレッド プールのサイズを小さくします。

#### <code>readpool.unified.max-thread-count</code> {#code-readpool-unified-max-thread-count-code}

このパラメータのデフォルト値は、マシン スレッド数の 80% です。ハイブリッド展開シナリオでは、この値を手動で計算して指定する必要があります。最初に、TiKV が使用する CPU スレッドの予想数の 80% に設定できます。

#### <code>server.grpc-concurrency</code> {#code-server-grpc-concurrency-code}

このパラメータのデフォルトは`4`です。既存の展開計画では、CPU リソースが制限されており、実際の要求が少ないためです。監視パネルを観察し、このパラメーターの値を下げて、使用率を 80% 未満に抑えることができます。

このテストでは、このパラメーターの値は`2`に設定されます。 **gRPC ポーリング CPU**パネルを観察すると、使用率が約 80% であることがわかります。

![gRPC Pool CPU](/media/best-practices/three-nodes-grpc-pool-usage.png)

#### <code>storage.scheduler-worker-pool-size</code> {#code-storage-scheduler-worker-pool-size-code}

マシンの CPU コア数が`16`以上であることを TiKV が検出すると、このパラメーター値のデフォルトは`8`になります。 CPU コア数が`16`より小さい場合、パラメータ値はデフォルトで`4`になります。このパラメーターは、TiKV が複雑なトランザクション要求を単純なキー値の読み取りまたは書き込みに変換するときに使用されますが、スケジューラー スレッド プールは書き込みを実行しません。

理想的には、スケジューラ スレッド プールの使用率は 50% から 75% の間に維持されます。 gRPC スレッド プールと同様に、ハイブリッド デプロイ中は`storage.scheduler-worker-pool-size`パラメーターの既定値が大きくなるため、リソースの使用が不十分になります。このテストでは、このパラメーターの値は`2`に設定されています。これは、ベスト プラクティスに沿ったものであり、 **Scheduler ワーカーの CPU**パネルで対応するメトリックを観察することによって導き出された結論です。

![Scheduler Worker CPU](/media/best-practices/three-nodes-scheduler-pool-usage.png)

### TiKV バックグラウンド タスクのリソース構成 {#resource-configuration-for-tikv-background-tasks}

フォアグラウンド タスクに加えて、TiKV は定期的にデータを並べ替え、バックグラウンド タスクで古いデータをクリーンアップします。既定の構成では、トラフィックの多い書き込みのシナリオに対して、これらのタスクに十分なリソースが割り当てられます。

ただし、ハイブリッド展開シナリオでは、この既定の構成はベスト プラクティスに沿っていません。次のパラメーターを調整して、バックグラウンド タスクのリソース使用量を制限する必要があります。

#### <code>rocksdb.max-background-jobs</code>および<code>rocksdb.max-sub-compactions</code> {#code-rocksdb-max-background-jobs-code-and-code-rocksdb-max-sub-compactions-code}

RocksDB スレッド プールは、圧縮およびフラッシュ ジョブの実行に使用されます。デフォルト値の`rocksdb.max-background-jobs` `8`で、明らかに必要なリソースを超えています。したがって、値を調整してリソースの使用を制限する必要があります。

`rocksdb.max-sub-compactions` 1 つの圧縮ジョブで許可される同時サブタスクの数を示します。デフォルトは`3`です。書き込みトラフィックが高くない場合は、この値を下げることができます。

テストでは、 `rocksdb.max-background-jobs`値は`3`に設定され、 `rocksdb.max-sub-compactions`値は`1`に設定されます。 TPC-C 負荷での 12 時間のテスト中に、書き込みストールは発生しません。実際の負荷に応じて 2 つのパラメーター値を最適化する場合、モニタリング メトリックに基づいて値を徐々に下げることができます。

-   書き込みストールが発生した場合は、 `rocksdb.max-background-jobs`の値を増やします。
-   書き込みストールが続く場合は、値`rocksdb.max-sub-compactions`を`2`または`3`に設定します。

#### <code>rocksdb.rate-bytes-per-sec</code> {#code-rocksdb-rate-bytes-per-sec-code}

このパラメーターは、バックグラウンド圧縮ジョブのディスク トラフィックを制限するために使用されます。デフォルト構成では、このパラメーターに制限はありません。圧縮ジョブがフォアグラウンド サービスのリソースを占有する状況を回避するために、ディスクのシーケンシャル読み取りおよび書き込み速度に従ってこのパラメーター値を調整できます。これにより、フォアグラウンド サービス用に十分なディスク帯域幅が予約されます。

RocksDB スレッド プールを最適化する方法は、圧縮スレッド プールを最適化する方法と似ています。書き込みストールが発生するかどうかによって、調整した値が適切かどうかを判断できます。

#### <code>gc.max_write_bytes_per_sec</code> {#code-gc-max-write-bytes-per-sec-code}

TiDB はマルチバージョン同時実行制御 (MVCC) モデルを使用するため、TiKV はバックグラウンドで古いバージョンのデータを定期的に消去します。使用可能なリソースが限られている場合、この操作によって定期的なパフォーマンスのジッターが発生します。 `gc.max_write_bytes_per_sec`パラメータを使用して、このような操作のリソース使用を制限できます。

![GC Impact](/media/best-practices/three-nodes-gc-impact.png)

構成ファイルでこのパラメーター値を設定するだけでなく、tikv-ctl でこの値を動的に調整することもできます。

{{< copyable "" >}}

```shell
tiup ctl:v<CLUSTER_VERSION> tikv --host=${ip:port} modify-tikv-config -n gc.max_write_bytes_per_sec -v ${limit}
```

> **ノート：**
>
> 更新が頻繁に行われるアプリケーション シナリオでは、GC トラフィックを制限すると、MVCC バージョンが積み重なり、読み取りパフォーマンスに影響を与える可能性があります。現在、パフォーマンスのジッタとパフォーマンスの低下のバランスを取るには、このパラメータの値を調整するために複数回試行する必要がある場合があります。

### TiDB パラメータ調整 {#tidb-parameter-adjustment}

通常、 `tidb_hash_join_concurrency`や`tidb_index_lookup_join_concurrency`などのシステム変数を使用して、実行オペレーターの TiDB パラメーターを調整できます。

このテストでは、これらのパラメーターは調整されません。実際のアプリケーションの負荷テストで、実行オペレーターが CPU リソースを過度に消費する場合、アプリケーションのシナリオに応じて、特定のオペレーターのリソース使用を制限できます。詳細については、 [TiDB システム変数](/system-variables.md)を参照してください。

#### <code>performance.max-procs</code> {#code-performance-max-procs-code}

このパラメーターは、Go プロセス全体で使用できる CPU コアの数を制御するために使用されます。デフォルトでは、値は現在のマシンまたは cgroup の CPU コアの数と同じです。

Go の実行中は、GC などのバックグラウンド タスクにスレッドの一部が使用されます。 `performance.max-procs`パラメータの値を制限しないと、これらのバックグラウンド タスクが CPU を大量に消費します。
