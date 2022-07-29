---
title: Hybrid Deployment Topology
summary: Learn the hybrid deployment topology of TiDB clusters.
---

# ハイブリッド展開トポロジ {#hybrid-deployment-topology}

このドキュメントでは、TiKVとTiDBのハイブリッド展開のトポロジと主要なパラメータについて説明します。

ハイブリッド展開は通常、次のシナリオで使用されます。

デプロイメントマシンには、十分なメモリを備えた複数のCPUプロセッサがあります。物理マシンリソースの使用率を向上させるために、複数のインスタンスを単一のマシンにデプロイできます。つまり、TiDBとTiKVのCPUリソースはNUMAノードバインディングによって分離されます。 PDとPrometheusは一緒にデプロイされますが、それらのデータディレクトリは別々のファイルシステムを使用する必要があります。

## トポロジー情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                    | 知財                                   | Configuration / コンフィグレーション                                                                                                                                            |
| :------------- | :--- | :------------------------- | :----------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | 6    | 32 VCore 64GB              | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | CPUコアをバインドするようにNUMAを構成する                                                                                                                                              |
| PD             | 3    | 16 VCore 32 GB             | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | `location_labels`つのパラメーターを構成します                                                                                                                                       |
| TiKV           | 6    | 32 VCore 64GB              | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | <li>インスタンスレベルのポートとstatus_portを分離します。<br/> 2.グローバルパラメータ`readpool` 、および`raftstore`を設定し`storage` 。<br/> 3.インスタンスレベルのホストのラベルを構成します。<br/> 4.CPUコアをバインドするようにNUMAを構成します</li> |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB（ssd） | 10.0.1.10                            | デフォルト設定                                                                                                                                                               |

### トポロジテンプレート {#topology-templates}

-   [ハイブリッド展開用のシンプルなテンプレート](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-multi-instance.yaml)
-   [ハイブリッド展開用の複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml)

上記のTiDBクラスタトポロジファイルの構成項目の詳細については、 [TiUPを使用してTiDBを展開するためのトポロジConfiguration / コンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 重要なパラメータ {#key-parameters}

このセクションでは、単一のマシンに複数のインスタンスをデプロイする場合の主要なパラメーターを紹介します。これは主に、TiDBとTiKVの複数のインスタンスが単一のマシンにデプロイされるシナリオで使用されます。以下に示す計算方法に従って、結果を構成テンプレートに入力する必要があります。

-   TiKVの構成を最適化する

    -   `readpool`をスレッドプールに自己適応するように構成します。 `readpool.unified.max-thread-count`パラメータを設定することにより、 `readpool.storage`と`readpool.coprocessor`に統合スレッドプールを共有させ、それぞれ自己適応型スイッチを設定できます。

        -   `readpool.storage`と`readpool.coprocessor`を有効にする：

            ```yaml
            readpool.storage.use-unified-pool: true
            readpool.coprocessor.use-unified-pool: true
            ```

        -   計算方法：

            ```
            readpool.unified.max-thread-count = cores * 0.8 / the number of TiKV instances
            ```

    -   ストレージCF（すべてのRocksDB列ファミリー）をメモリに自己適応するように構成します。 `storage.block-cache.capacity`パラメータを設定することにより、CFにメモリ使用量のバランスを自動的にとらせることができます。

        -   `storage.block-cache`は、デフォルトでCF自己適応を有効にします。変更する必要はありません。

            ```yaml
            storage.block-cache.shared: true
            ```

        -   計算方法：

            ```
            storage.block-cache.capacity = (MEM_TOTAL * 0.5 / the number of TiKV instances)
            ```

    -   複数のTiKVインスタンスが同じ物理ディスクにデプロイされている場合は、TiKV構成に`capacity`つのパラメーターを追加します。

        ```
        raftstore.capacity = disk total capacity / the number of TiKV instances
        ```

-   ラベルスケジューリング構成

    TiKVの複数のインスタンスが単一のマシンにデプロイされているため、物理マシンがダウンすると、Raftグループはデフォルトの3つのレプリカのうち2つを失い、クラスタが使用できなくなる可能性があります。この問題に対処するには、ラベルを使用してPDのスマートスケジューリングを有効にします。これにより、 Raftが同じマシン上の複数のTiKVインスタンスに3つ以上のレプリカを持つようになります。

    -   TiKV構成

        同じ物理マシンに対して、同じホストレベルのラベル情報が構成されています。

        ```yml
        config:
          server.labels:
            host: tikv1
        ```

    -   PD構成

        PDがリージョンを識別してスケジュールできるようにするには、PDのラベルタイプを構成します。

        ```yml
        pd:
          replication.location-labels: ["host"]
        ```

-   `numa_node`コアバインディング

    -   インスタンスパラメータモジュールで、対応する`numa_node`パラメータを設定し、CPUコアの数を追加します。

    -   NUMAを使用してコアをバインドする前に、numactlツールがインストールされていることを確認し、物理マシンのCPUの情報を確認してください。その後、パラメータを設定します。

    -   `numa_node`パラメーターは`numactl --membind`構成に対応します。

> **ノート：**
>
> -   構成ファイルテンプレートを編集するときは、必要なパラメーター、IP、ポート、およびディレクトリーを変更してください。
> -   各コンポーネントは、デフォルトでグローバル`<deploy_dir>/<components_name>-<port>`を`deploy_dir`として使用します。たとえば、TiDBが`4001`ポートを指定している場合、その`deploy_dir`はデフォルトで`/tidb-deploy/tidb-4001`です。したがって、マルチインスタンスシナリオでは、デフォルト以外のポートを指定するときに、ディレクトリを再度指定する必要はありません。
> -   構成ファイルに`tidb`人のユーザーを手動で作成する必要はありません。 TiUPクラスタコンポーネントは、ターゲットマシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーと制御マシンの一貫性を保つこともできます。
> -   展開ディレクトリを相対パスとして構成すると、クラスタはユーザーのホームディレクトリに展開されます。
