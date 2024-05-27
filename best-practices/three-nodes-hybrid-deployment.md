---
title: Best Practices for Three-Node Hybrid Deployment
summary: TiDB クラスターは、3 台のマシンにコスト効率よく導入できます。このハイブリッド導入のベスト プラクティスには、安定性とパフォーマンスのためのパラメーターの調整が含まれます。リソース消費を制限し、スレッド プールのサイズを調整することが、クラスターを最適化する鍵となります。TiKV バックグラウンド タスクと TiDB 実行演算子のパラメーターを調整することも重要です。
---

# 3ノードハイブリッド展開のベストプラクティス {#best-practices-for-three-node-hybrid-deployment}

TiDB クラスターの場合、高パフォーマンスは必要ないがコストを抑える必要がある場合は、TiDB、TiKV、PD コンポーネントを 3 台のマシンにハイブリッド方式でデプロイできます。

このドキュメントでは、3 ノードのハイブリッド展開の例と、展開されたクラスターに対する TPC-C テストを示します。この例に基づいて、このドキュメントでは展開シナリオとそのパラメータ調整のベスト プラクティスを示します。

## 展開の前提条件とテスト方法 {#prerequisites-for-deployment-and-the-test-method}

この例では、それぞれ 16 個の CPU コアと 32 GB のメモリを備えた 3 台の物理マシンがデプロイメントに使用されています。各マシン (ノード) には、1 つの TiDB インスタンス、1 つの TiKV インスタンス、および 1 つの PD インスタンスがハイブリッド方式でデプロイされています。

PD と TiKV はどちらもディスクに情報を保存するため、ディスクの読み取りおよび書き込みのレイテンシーはPD および TiKV サービスのレイテンシーに直接影響します。PD と TiKV がディスク リソースを競合して互いに影響し合う状況を回避するには、PD と TiKV に異なるディスクを使用することをお勧めします。

この例では、TPC-C 5000 ウェアハウス データがTiUPベンチで使用され、 `terminals`パラメータを`128` (同時実行) に設定してテストが 12 時間続きます。クラスターのパフォーマンス安定性に関連するメトリックに細心の注意が払われます。

下の画像は、デフォルトのパラメータ設定で 12 時間以内のクラスターの QPS モニターを示しています。画像から、明らかなパフォーマンスのジッターが確認できます。

![QPS with default config](/media/best-practices/three-nodes-default-config-qps.png)

パラメータ調整後、パフォーマンスが向上します。

![QPS with modified config](/media/best-practices/three-nodes-final-config-qps.png)

## パラメータ調整 {#parameter-adjustment}

上の画像では、デフォルトのスレッド プール構成とバックグラウンド タスクへのリソース割り当てが十分なリソースを持つマシン向けであるため、パフォーマンスのジッターが発生します。ハイブリッド展開シナリオでは、リソースは複数のコンポーネント間で共有されるため、構成パラメーターを使用してリソースの消費を制限する必要があります。

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

このセクションでは、フォアグラウンド アプリケーションのスレッド プールのリソース割り当てに関連するパラメータを調整するためのベスト プラクティスを紹介します。これらのスレッド プールのサイズを小さくするとパフォーマンスが低下しますが、リソースが制限されているハイブリッド展開シナリオでは、クラスター自体で高いパフォーマンスを実現するのは困難です。このシナリオでは、パフォーマンスよりもクラスターの全体的な安定性が優先されます。

実際の負荷テストを実施する場合は、まずデフォルトの構成を使用して、各スレッド プールの実際のリソース使用量を観察します。次に、対応する構成項目を調整し、使用量が少ないスレッド プールのサイズを縮小します。

#### <code>readpool.unified.max-thread-count</code> {#code-readpool-unified-max-thread-count-code}

このパラメータのデフォルト値は、マシン スレッド数の 80% です。ハイブリッド展開シナリオでは、この値を手動で計算して指定する必要があります。まず、TiKV によって使用される CPU スレッドの予想数の 80% に設定できます。

#### <code>server.grpc-concurrency</code> {#code-server-grpc-concurrency-code}

このパラメータのデフォルトは`4`です。既存のデプロイメント プランでは、CPU リソースが制限されており、実際のリクエストは少ないためです。監視パネルを監視し、このパラメータの値を下げて、使用率を 80% 未満に保つことができます。

このテストでは、このパラメータの値は`2`に設定されています。gRPC**ポーリング CPU**パネルを観察すると、使用率が約 80% であることがわかります。

![gRPC Pool CPU](/media/best-practices/three-nodes-grpc-pool-usage.png)

#### <code>storage.scheduler-worker-pool-size</code> {#code-storage-scheduler-worker-pool-size-code}

TiKV がマシンの CPU コア数が`16`以上であることを検出すると、このパラメータ値はデフォルトで`8`になります。CPU コア数が`16`未満の場合、パラメータ値はデフォルトで`4`になります。このパラメータは、TiKV が複雑なトランザクション要求を単純なキー値の読み取りまたは書き込みに変換するが、スケジューラ スレッド プールが書き込みを実行しない場合に使用されます。

理想的には、スケジューラ スレッド プールの使用率は 50% ～ 75% に保たれます。gRPC スレッド プールと同様に、ハイブリッド展開中は`storage.scheduler-worker-pool-size`パラメータのデフォルト値が大きくなり、リソースの使用量が不十分になります。このテストでは、このパラメータの値は`2`に設定されています。これは、**スケジューラ ワーカー CPU**パネルの対応するメトリックを観察することによって導き出された結論であり、ベスト プラクティスと一致しています。

![Scheduler Worker CPU](/media/best-practices/three-nodes-scheduler-pool-usage.png)

### TiKV バックグラウンド タスクのリソース構成 {#resource-configuration-for-tikv-background-tasks}

フォアグラウンド タスクに加えて、TiKV はバックグラウンド タスクで定期的にデータを並べ替え、古いデータを消去します。デフォルト構成では、高トラフィックの書き込みシナリオに備えて、これらのタスクに十分なリソースが割り当てられます。

ただし、ハイブリッド展開シナリオでは、この既定の構成はベスト プラクティスに準拠していません。次のパラメーターを調整して、バックグラウンド タスクのリソース使用量を制限する必要があります。

#### <code>rocksdb.max-background-jobs</code>と<code>rocksdb.max-sub-compactions</code> {#code-rocksdb-max-background-jobs-code-and-code-rocksdb-max-sub-compactions-code}

RocksDB スレッド プールは、圧縮ジョブとフラッシュ ジョブを実行するために使用されます。デフォルト値`rocksdb.max-background-jobs`は`8`ですが、これは明らかに必要なリソースを超えています。したがって、リソースの使用を制限するには値を調整する必要があります。

`rocksdb.max-sub-compactions` 、単一の圧縮ジョブに許可される同時サブタスクの数を示します。デフォルトは`3`です。書き込みトラフィックが高くない場合は、この値を下げることができます。

テストでは、 `rocksdb.max-background-jobs`値は`3`に設定され、 `rocksdb.max-sub-compactions`値は`1`に設定されています。TPC-C 負荷での 12 時間のテスト中に書き込み停止は発生しません。実際の負荷に応じて 2 つのパラメータ値を最適化する場合は、監視メトリックに基づいて値を徐々に下げることができます。

-   書き込み停止が発生する場合は、値を`rocksdb.max-background-jobs`増やします。
-   書き込み停止が続く場合は、 `rocksdb.max-sub-compactions`の値を`2`または`3`設定します。

#### <code>rocksdb.rate-bytes-per-sec</code> {#code-rocksdb-rate-bytes-per-sec-code}

このパラメータは、バックグラウンド圧縮ジョブのディスク トラフィックを制限するために使用されます。デフォルト構成では、このパラメータに制限はありません。圧縮ジョブがフォアグラウンド サービスのリソースを占有する状況を回避するには、ディスクの順次読み取りおよび書き込み速度に応じてこのパラメータ値を調整し、フォアグラウンド サービスに十分なディスク帯域幅を予約します。

RocksDB スレッド プールを最適化する方法は、コンパクション スレッド プールを最適化する方法と似ています。書き込みストールが発生するかどうかによって、調整した値が適切かどうかを判断できます。

#### <code>gc.max_write_bytes_per_sec</code> {#code-gc-max-write-bytes-per-sec-code}

TiDB はマルチバージョン同時実行制御 (MVCC) モデルを使用するため、TiKV は定期的にバックグラウンドで古いバージョンのデータを消去します。使用可能なリソースが制限されている場合、この操作により定期的なパフォーマンスのジッターが発生します。1 パラメータを使用して、このよう`gc.max_write_bytes_per_sec`操作のリソース使用量を制限できます。

![GC Impact](/media/best-practices/three-nodes-gc-impact.png)

設定ファイルでこのパラメータ値を設定するだけでなく、tikv-ctl でこの値を動的に調整することもできます。

```shell
tiup ctl:v<CLUSTER_VERSION> tikv --host=${ip:port} modify-tikv-config -n gc.max_write_bytes_per_sec -v ${limit}
```

> **注記：**
>
> 頻繁に更新されるアプリケーション シナリオでは、GC トラフィックを制限すると、MVCC バージョンが蓄積され、読み取りパフォーマンスに影響する可能性があります。現在、パフォーマンス ジッターとパフォーマンス低下のバランスをとるには、このパラメーターの値を複数回調整する必要がある場合があります。

### TiDBパラメータ調整 {#tidb-parameter-adjustment}

通常、 `tidb_hash_join_concurrency`や`tidb_index_lookup_join_concurrency`などのシステム変数を使用して、実行演算子の TiDB パラメータを調整できます。

このテストでは、これらのパラメータは調整されません。実際のアプリケーションの負荷テストで、実行オペレータが CPU リソースを過度に消費する場合は、アプリケーションのシナリオに応じて特定のオペレータのリソース使用量を制限することができます。詳細については、 [TiDB システム変数](/system-variables.md)参照してください。

#### <code>performance.max-procs</code> {#code-performance-max-procs-code}

このパラメータは、Go プロセス全体で使用できる CPU コアの数を制御するために使用されます。デフォルトでは、値は現在のマシンまたは cgroup の CPU コアの数と同じです。

Go の実行中、一部のスレッドは`performance.max-procs`などのバックグラウンド タスクに使用されます。1 パラメータの値を制限しないと、これらのバックグラウンド タスクが CPU を過剰に消費することになります。
