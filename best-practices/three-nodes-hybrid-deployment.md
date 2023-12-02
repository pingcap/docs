---
title: Best Practices for Three-Node Hybrid Deployment
summary: Learn the best practices for three-node hybrid deployment.
---

# 3 ノードのハイブリッド展開のベスト プラクティス {#best-practices-for-three-node-hybrid-deployment}

TiDB クラスターの場合、高パフォーマンスの要件はないが、コストを制御する必要がある場合は、TiDB、TiKV、および PD コンポーネントを 3 台のマシンにハイブリッド方式でデプロイできます。

このドキュメントでは、3 ノードのハイブリッド展開と、展開されたクラスターに対する TPC-C テストの例を示します。このドキュメントでは、この例に基づいて、展開シナリオとそのパラメーター調整のベスト プラクティスを提供します。

## 導入の前提条件とテスト方法 {#prerequisites-for-deployment-and-the-test-method}

この例では、展開に 3 台の物理マシンが使用されており、それぞれに 16 個の CPU コアと 32 GB のメモリが搭載されています。各マシン (ノード) 上に、1 つの TiDB インスタンス、1 つの TiKV インスタンス、および 1 つの PD インスタンスがハイブリッド方式でデプロイされます。

PD と TiKV は両方ともディスク上に情報を保存するため、ディスクの読み取りおよび書き込みのレイテンシーは、PD サービスと TiKV サービスのレイテンシーに直接影響します。 PD と TiKV がディスク リソースを競合して相互に影響を与える状況を回避するには、PD と TiKV に異なるディスクを使用することをお勧めします。

この例では、TPC-C 5000 Warehouse データがTiUPベンチで使用され、テストは`terminals`パラメーターを`128` (同時実行) に設定して 12 時間続きます。クラスターのパフォーマンスの安定性に関連するメトリックには細心の注意が払われます。

以下の画像は、デフォルトのパラメーター構成による 12 時間以内のクラスターの QPS モニターを示しています。画像から、明らかなパフォーマンスのジッターがわかります。

![QPS with default config](/media/best-practices/three-nodes-default-config-qps.png)

パラメータ調整後、パフォーマンスが向上しました。

![QPS with modified config](/media/best-practices/three-nodes-final-config-qps.png)

## パラメータ調整 {#parameter-adjustment}

デフォルトのスレッド プール構成とバックグラウンド タスクへのリソース割り当ては、十分なリソースを持つマシンに対して行われているため、上の画像ではパフォーマンスのジッターが発生します。ハイブリッド展開シナリオでは、リソースが複数のコンポーネント間で共有されるため、構成パラメータを介してリソースの消費を制限する必要があります。

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

### TiKV スレッド プール サイズのコンフィグレーション {#configuration-of-tikv-thread-pool-size}

このセクションでは、フォアグラウンド アプリケーションのスレッド プールのリソース割り当てに関連するパラメーターを調整するためのベスト プラクティスを提供します。これらのスレッド プール サイズを減らすとパフォーマンスが低下しますが、リソースが限られているハイブリッド展開シナリオでは、クラスター自体が高いパフォーマンスを達成するのは困難です。このシナリオでは、パフォーマンスよりもクラスター全体の安定性が優先されます。

実際の負荷テストを実施する場合は、最初にデフォルト構成を使用して、各スレッド プールの実際のリソース使用量を観察できます。その後、対応する構成項目を調整し、使用率が低いスレッド プールのサイズを減らすことができます。

#### <code>readpool.unified.max-thread-count</code> {#code-readpool-unified-max-thread-count-code}

このパラメータのデフォルト値は、マシン スレッド数の 80% です。ハイブリッド展開シナリオでは、この値を手動で計算して指定する必要があります。まず、TiKV が使用する予想される CPU スレッド数の 80% に設定します。

#### <code>server.grpc-concurrency</code> {#code-server-grpc-concurrency-code}

このパラメータのデフォルトは`4`です。既存の展開計画では CPU リソースが限られており、実際のリクエストが少ないためです。監視パネルを観察し、このパラメータの値を下げて、使用率を 80% 未満に保つことができます。

このテストでは、このパラメーターの値は`2`に設定されます。 **gRPC ポーリング CPU**パネルを観察すると、使用率がちょうど約 80% であることがわかります。

![gRPC Pool CPU](/media/best-practices/three-nodes-grpc-pool-usage.png)

#### <code>storage.scheduler-worker-pool-size</code> {#code-storage-scheduler-worker-pool-size-code}

TiKV がマシンの CPU コア番号が`16`以上であることを検出すると、このパラメーター値はデフォルトで`8`に設定されます。 CPU コア数が`16`より小さい場合、パラメータ値のデフォルトは`4`です。このパラメーターは、TiKV が複雑なトランザクション リクエストを単純なキーと値の読み取りまたは書き込みに変換するときに使用されますが、スケジューラー スレッド プールは書き込みを実行しません。

スケジューラ スレッド プールの使用率は 50% ～ 75% の間に維持されるのが理想的です。 gRPC スレッド プールと同様に、ハイブリッド デプロイメント中は`storage.scheduler-worker-pool-size`パラメータのデフォルトがより大きな値に設定されるため、リソースの使用量が不十分になります。このテストでは、このパラメーターの値は`2`に設定されています。これはベスト プラクティス、つまり**スケジューラー ワーカー CPU**パネルで対応するメトリックを観察することによって得られた結論と一致しています。

![Scheduler Worker CPU](/media/best-practices/three-nodes-scheduler-pool-usage.png)

### TiKV バックグラウンド タスクのリソース構成 {#resource-configuration-for-tikv-background-tasks}

フォアグラウンド タスクに加えて、TiKV はバックグラウンド タスクで定期的にデータを並べ替え、古いデータを消去します。デフォルト構成では、高トラフィック書き込みのシナリオに備えて、これらのタスクに十分なリソースが割り当てられます。

ただし、ハイブリッド展開シナリオでは、このデフォルト構成はベスト プラクティスに従っていません。次のパラメータを調整して、バックグラウンド タスクのリソース使用量を制限する必要があります。

#### <code>rocksdb.max-background-jobs</code>と<code>rocksdb.max-sub-compactions</code> {#code-rocksdb-max-background-jobs-code-and-code-rocksdb-max-sub-compactions-code}

RocksDB スレッド プールは、圧縮ジョブとフラッシュ ジョブを実行するために使用されます。デフォルト値の`rocksdb.max-background-jobs` `8`ですが、これは明らかに必要なリソースを超えています。したがって、リソースの使用量を制限するには、値を調整する必要があります。

`rocksdb.max-sub-compactions`単一の圧縮ジョブに許可される同時サブタスクの数を示します。デフォルトは`3`です。書き込みトラフィックが高くない場合は、この値を下げることができます。

テストでは、 `rocksdb.max-background-jobs`値は`3`に設定され、 `rocksdb.max-sub-compactions`値は`1`に設定されます。 TPC-C 負荷による 12 時間のテスト中に書き込み停止は発生しません。実際の負荷に応じて 2 つのパラメーター値を最適化する場合、モニタリング メトリックに基づいて値を段階的に下げることができます。

-   書き込みストールが発生した場合は、 `rocksdb.max-background-jobs`の値を増やします。
-   書き込み停止が続く場合は、 `rocksdb.max-sub-compactions`の値を`2`または`3`に設定します。

#### <code>rocksdb.rate-bytes-per-sec</code> {#code-rocksdb-rate-bytes-per-sec-code}

このパラメータは、バックグラウンド圧縮ジョブのディスク トラフィックを制限するために使用されます。デフォルト設定では、このパラメータに制限はありません。圧縮ジョブがフォアグラウンド サービスのリソースを占有する状況を回避するには、ディスクの順次読み取りおよび書き込み速度に応じてこのパラメーター値を調整します。これにより、フォアグラウンド サービス用に十分なディスク帯域幅が確保されます。

RocksDB スレッド プールを最適化する方法は、圧縮スレッド プールを最適化する方法と似ています。調整した値が適切かどうかは、書き込みストールが発生するかどうかによって判断できます。

#### <code>gc.max_write_bytes_per_sec</code> {#code-gc-max-write-bytes-per-sec-code}

TiDB はマルチバージョン同時実行制御 (MVCC) モデルを使用するため、TiKV はバックグラウンドで古いバージョンのデータを定期的にクリーンアップします。利用可能なリソースが限られている場合、この操作により定期的なパフォーマンスのジッターが発生します。 `gc.max_write_bytes_per_sec`パラメータを使用すると、このような操作のリソース使用量を制限できます。

![GC Impact](/media/best-practices/three-nodes-gc-impact.png)

構成ファイルでこのパラメーター値を設定することに加えて、tikv-ctl でこの値を動的に調整することもできます。

```shell
tiup ctl:v<CLUSTER_VERSION> tikv --host=${ip:port} modify-tikv-config -n gc.max_write_bytes_per_sec -v ${limit}
```

> **注記：**
>
> 頻繁に更新が行われるアプリケーション シナリオでは、GC トラフィックを制限すると、MVCC バージョンが蓄積し、読み取りパフォーマンスに影響を与える可能性があります。現在、パフォーマンスのジッターとパフォーマンスの低下の間のバランスを達成するには、このパラメーターの値の調整を複数回試行する必要がある場合があります。

### TiDBパラメータ調整 {#tidb-parameter-adjustment}

一般に、 `tidb_hash_join_concurrency`や`tidb_index_lookup_join_concurrency`などのシステム変数を使用して、実行オペレーターの TiDB パラメーターを調整できます。

このテストでは、これらのパラメータは調整されていません。実際のアプリケーションの負荷テストで、実行オペレーターが過剰な量の CPU リソースを消費する場合、アプリケーションのシナリオに応じて特定のオペレーターのリソース使用量を制限できます。詳細については、 [TiDB システム変数](/system-variables.md)を参照してください。

#### <code>performance.max-procs</code> {#code-performance-max-procs-code}

このパラメータは、Go プロセス全体で使用できる CPU コアの数を制御するために使用されます。デフォルトでは、この値は現在のマシンまたは cgroup の CPU コアの数と等しくなります。

Go の実行中、スレッドの一部は GC などのバックグラウンド タスクに使用されます。 `performance.max-procs`パラメータの値を制限しない場合、これらのバックグラウンド タスクは CPU を過剰に消費します。
