---
title: Best Practices for Three-Node Hybrid Deployment
summary: Learn the best practices for three-node hybrid deployment.
---

# 3ノードハイブリッド展開のベストプラクティス {#best-practices-for-three-node-hybrid-deployment}

TiDBクラスタの場合、高性能の要件はないがコストを管理する必要がある場合は、TiDB、TiKV、およびPDコンポーネントを3台のマシンにハイブリッド方式で展開できます。

このドキュメントでは、3ノードハイブリッド展開の例と、展開されたクラスタに対するTPC-Cテストを提供します。この例に基づいて、このドキュメントでは、展開シナリオとそのパラメーター調整のベストプラクティスを提供します。

## 展開の前提条件とテスト方法 {#prerequisites-for-deployment-and-the-test-method}

この例では、3台の物理マシンが展開に使用され、それぞれに16個のCPUコアと32GBのメモリが搭載されています。各マシン（ノード）に、1つのTiDBインスタンス、1つのTiKVインスタンス、および1つのPDインスタンスがハイブリッド方式でデプロイされます。

PDとTiKVはどちらもディスクに情報を格納するため、ディスクの読み取りと書き込みの遅延は、PDとTiKVサービスの遅延に直接影響します。 PDとTiKVがディスクリソースをめぐって競合し、相互に影響を与える状況を回避するために、PDとTiKVに異なるディスクを使用することをお勧めします。

この例では、TPC-C 5000ウェアハウスデータがTiUPベンチで使用され、テストは`terminals`パラメーターを`128` （同時実行）に設定して12時間続きます。クラスタのパフォーマンスの安定性に関連するメトリックに細心の注意が払われています。

以下の画像は、デフォルトのパラメーター構成で12時間以内のクラスタのQPSモニターを示しています。画像から、明らかなパフォーマンスジッターを確認できます。

![QPS with default config](/media/best-practices/three-nodes-default-config-qps.png)

パラメータ調整後、性能が向上します。

![QPS with modified config](/media/best-practices/three-nodes-final-config-qps.png)

## パラメータ調整 {#parameter-adjustment}

デフォルトのスレッドプール構成とバックグラウンドタスクへのリソース割り当ては、十分なリソースを備えたマシン用であるため、上の画像ではパフォーマンスジッターが発生しています。ハイブリッド展開シナリオでは、リソースは複数のコンポーネント間で共有されるため、構成パラメーターを使用してリソース消費を制限する必要があります。

このテストの最終的なクラスタ構成は次のとおりです。

{{< copyable "" >}}

```yaml
tikv:
    readpool.unified.max-thread-count: 6
    server.grpc-concurrency: 2
    storage.scheduler-worker-pool-size: 2
    gc.max-write-bytes-per-sec: 300K
    rocksdb.max-background-jobs: 3
    rocksdb.max-sub-compactions: 1
    rocksdb.rate-bytes-per-sec: “200M”

  tidb:
    performance.max-procs: 8
```

次のセクションでは、これらのパラメータの意味と調整方法を紹介します。

### TiKVスレッドプールサイズのConfiguration / コンフィグレーション {#configuration-of-tikv-thread-pool-size}

このセクションでは、フォアグラウンドアプリケーションのスレッドプールのリソース割り当てに関連するパラメーターを調整するためのベストプラクティスを提供します。これらのスレッドプールサイズを減らすとパフォーマンスが低下しますが、リソースが限られているハイブリッド展開シナリオでは、クラスタ自体で高いパフォーマンスを実現するのは困難です。このシナリオでは、クラスタの全体的な安定性がパフォーマンスよりも優先されます。

実際の負荷テストを実施する場合は、最初にデフォルト構成を使用して、各スレッドプールの実際のリソース使用量を観察できます。次に、対応する構成項目を調整し、使用率の低いスレッドプールのサイズを減らすことができます。

#### <code>readpool.unified.max-thread-count</code> {#code-readpool-unified-max-thread-count-code}

このパラメータのデフォルト値は、マシンスレッド数の80％です。ハイブリッド展開シナリオでは、この値を手動で計算して指定する必要があります。最初に、TiKVが使用するCPUスレッドの予想数の80％に設定できます。

#### <code>server.grpc-concurrency</code> {#code-server-grpc-concurrency-code}

このパラメーターのデフォルトは`4`です。既存の展開計画では、CPUリソースが制限されており、実際の要求が少ないためです。監視パネルを監視し、このパラメーターの値を下げて、使用率を80％未満に保つことができます。

このテストでは、このパラメーターの値は`2`に設定されます。 **gRPCポーリングCPU**パネルを観察すると、使用率が約80％であることがわかります。

![gRPC Pool CPU](/media/best-practices/three-nodes-grpc-pool-usage.png)

#### <code>storage.scheduler-worker-pool-size</code> {#code-storage-scheduler-worker-pool-size-code}

TiKVがマシンのCPUコア番号が`16`以上であることを検出すると、このパラメーター値はデフォルトで`8`になります。 CPUコア数が`16`より小さい場合、パラメーター値はデフォルトで`4`になります。このパラメーターは、TiKVが複雑なトランザクション要求を単純なKey-Value読み取りまたは書き込みに変換するが、スケジューラースレッドプールが書き込みを実行しない場合に使用されます。

理想的には、スケジューラスレッドプールの使用率は50％から75％の間に保たれます。 gRPCスレッドプールと同様に、 `storage.scheduler-worker-pool-size`パラメーターは、ハイブリッドデプロイメント中にデフォルトでより大きな値に設定されるため、リソースの使用量が不十分になります。このテストでは、このパラメーターの値を`2`に設定します。これは、ベストプラクティスに沿ったものであり、 **SchedulerワーカーのCPU**パネルで対応するメトリックを観察することで結論が導き出されます。

![Scheduler Worker CPU](/media/best-practices/three-nodes-scheduler-pool-usage.png)

### TiKVバックグラウンドタスクのリソース構成 {#resource-configuration-for-tikv-background-tasks}

フォアグラウンドタスクに加えて、TiKVは定期的にデータを並べ替え、バックグラウンドタスクで古いデータをクリーンアップします。デフォルト構成では、トラフィックの多い書き込みのシナリオに対して、これらのタスクに十分なリソースが割り当てられます。

ただし、ハイブリッド展開シナリオでは、このデフォルト構成はベストプラクティスに沿っていません。次のパラメータを調整して、バックグラウンドタスクのリソース使用量を制限する必要があります。

#### <code>rocksdb.max-background-jobs</code>および<code>rocksdb.max-sub-compactions</code> {#code-rocksdb-max-background-jobs-code-and-code-rocksdb-max-sub-compactions-code}

RocksDBスレッドプールは、圧縮およびフラッシュジョブを実行するために使用されます。デフォルト値の`rocksdb.max-background-jobs`は`8`であり、これは明らかに必要なリソースを超えています。したがって、リソースの使用を制限するように値を調整する必要があります。

`rocksdb.max-sub-compactions`は、単一の圧縮ジョブで許可される同時サブタスクの数を示します。デフォルトは`3`です。書き込みトラフィックが高くない場合は、この値を下げることができます。

テストでは、 `rocksdb.max-background-jobs`の値は`3`に設定され、 `rocksdb.max-sub-compactions`の値は`1`に設定されます。 TPC-C負荷を使用した12時間のテストでは、書き込みストールは発生しません。実際の負荷に応じて2つのパラメータ値を最適化する場合、監視メトリックに基づいて値を徐々に下げることができます。

-   書き込みストールが発生した場合は、値を`rocksdb.max-background-jobs`に増やします。
-   書き込みストールが続く場合は、値`rocksdb.max-sub-compactions`を`2`または`3`に設定します。

#### <code>rocksdb.rate-bytes-per-sec</code> {#code-rocksdb-rate-bytes-per-sec-code}

このパラメーターは、バックグラウンド圧縮ジョブのディスクトラフィックを制限するために使用されます。デフォルト設定では、このパラメーターに制限はありません。圧縮ジョブがフォアグラウンドサービスのリソースを占有する状況を回避するために、フォアグラウンドサービス用に十分なディスク帯域幅を予約するディスクのシーケンシャル読み取りおよび書き込み速度に応じてこのパラメーター値を調整できます。

RocksDBスレッドプールを最適化する方法は、圧縮スレッドプールを最適化する方法と似ています。書き込みストールが発生するかどうかによって、調整した値が適切かどうかを判断できます。

#### <code>gc.max_write_bytes_per_sec</code> {#code-gc-max-write-bytes-per-sec-code}

TiDBはマルチバージョン同時実行制御（MVCC）モデルを使用するため、TiKVはバックグラウンドで古いバージョンのデータを定期的にクリーンアップします。使用可能なリソースが限られている場合、この操作により定期的なパフォーマンスジッターが発生します。 `gc.max_write_bytes_per_sec`パラメーターを使用して、このような操作のリソース使用量を制限できます。

![GC Impact](/media/best-practices/three-nodes-gc-impact.png)

構成ファイルでこのパラメーター値を設定することに加えて、tikv-ctlでこの値を動的に調整することもできます。

{{< copyable "" >}}

```shell
tiup ctl tikv --host=${ip:port} modify-tikv-config -n gc.max_write_bytes_per_sec -v ${limit}
```

> **ノート：**
>
> 頻繁に更新されるアプリケーションシナリオでは、GCトラフィックを制限すると、MVCCバージョンが積み重なって、読み取りパフォーマンスに影響を与える可能性があります。現在、パフォーマンスジッターとパフォーマンス低下のバランスをとるために、このパラメーターの値を調整するために複数回試行する必要がある場合があります。

### TiDBパラメータ調整 {#tidb-parameter-adjustment}

一般に、 `tidb_hash_join_concurrency`や`tidb_index_lookup_join_concurrency`などのシステム変数を使用して、実行演算子のTiDBパラメーターを調整できます。

このテストでは、これらのパラメーターは調整されません。実際のアプリケーションの負荷テストでは、実行オペレーターが過剰な量のCPUリソースを消費する場合、アプリケーションのシナリオに応じて特定のオペレーターのリソース使用量を制限できます。詳細については、 [TiDBシステム変数](/system-variables.md)を参照してください。

#### <code>performance.max-procs</code> {#code-performance-max-procs-code}

このパラメーターは、Goプロセス全体で使用できるCPUコアの数を制御するために使用されます。デフォルトでは、値は現在のマシンまたはcgroupのCPUコアの数と同じです。

Goが実行されている場合、スレッドの一部がGCなどのバックグラウンドタスクに使用されます。 `performance.max-procs`パラメーターの値を制限しない場合、これらのバックグラウンドタスクはCPUを大量に消費します。
