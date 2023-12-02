---
title: Hybrid Deployment Topology
summary: Learn the hybrid deployment topology of TiDB clusters.
---

# ハイブリッド展開トポロジ {#hybrid-deployment-topology}

このドキュメントでは、TiKV と TiDB のハイブリッド展開のトポロジと主要なパラメーターについて説明します。

ハイブリッド展開は通常、次のシナリオで使用されます。

導入マシンには、十分なメモリを備えた複数の CPU プロセッサが搭載されています。物理マシン リソースの使用率を向上させるために、複数のインスタンスを 1 台のマシンにデプロイできます。つまり、TiDB と TiKV の CPU リソースは、NUMA ノード バインディングによって分離されます。 PD と Prometheus は一緒にデプロイされますが、それらのデータ ディレクトリでは別のファイル システムを使用する必要があります。

## トポロジ情報 {#topology-information}

| 実例           | カウント | 物理マシンの構成                    | IP                                   | コンフィグレーション                                                                                                                                                                       |
| :----------- | :--- | :-------------------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB         | 6    | 32 コア 64GB                  | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | CPU コアをバインドするように NUMA を構成する                                                                                                                                                      |
| PD           | 3    | 16 仮想コア 32 GB               | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | `location_labels`パラメータを設定します                                                                                                                                                     |
| TiKV         | 6    | 32 コア 64GB                  | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | <li>インスタンスレベルのポートと status_port を分離します。<br/> 2. グローバルパラメータ`readpool` 、 `storage` 、および`raftstore`を設定します。<br/> 3. インスタンスレベルのホストのラベルを構成します。<br/> 4. CPU コアをバインドするように NUMA を構成する</li> |
| モニタリングとグラファナ | 1    | 4 VCore 8GB * 1 500GB (SSD) | 10.0.1.10                            | デフォルト設定                                                                                                                                                                          |

### トポロジテンプレート {#topology-templates}

-   [ハイブリッド展開用のシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-multi-instance.yaml)
-   [ハイブリッド展開用の複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml)

上記の TiDB クラスター トポロジー ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB を展開するためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 主要パラメータ {#key-parameters}

このセクションでは、単一のマシンに複数のインスタンスをデプロイするときの主要なパラメーターを紹介します。これは主に、TiDB および TiKV の複数のインスタンスが単一のマシンにデプロイされるシナリオで使用されます。以下に示す計算方法に従って、結果を構成テンプレートに入力する必要があります。

-   TiKVの構成を最適化する

    -   スレッド プールに自己適応するように`readpool`を設定するには。 `readpool.unified.max-thread-count`パラメータを設定すると、 `readpool.storage`と`readpool.coprocessor`で統合スレッド プールを共有し、それぞれ自己適応スイッチを設定できます。

        -   `readpool.storage`と`readpool.coprocessor`を有効にします。

            ```yaml
            readpool.storage.use-unified-pool: true
            readpool.coprocessor.use-unified-pool: true
            ```

        -   計算方法:

                readpool.unified.max-thread-count = cores * 0.8 / the number of TiKV instances

    -   storageCF (すべての RocksDB 列ファミリー) をメモリに自己適応するように構成するには。 `storage.block-cache.capacity`パラメータを設定すると、CF がメモリ使用量のバランスを自動的に調整できます。

        -   計算方法:

                storage.block-cache.capacity = (MEM_TOTAL * 0.5 / the number of TiKV instances)

    -   複数の TiKV インスタンスが同じ物理ディスクにデプロイされている場合は、TiKV 構成に`capacity`パラメーターを追加します。

            raftstore.capacity = disk total capacity / the number of TiKV instances

-   ラベルのスケジュール設定

    TiKV の複数のインスタンスが 1 台のマシンにデプロイされているため、物理マシンがダウンすると、 Raftグループはデフォルトの 3 つのレプリカのうち 2 つを失い、クラスターが使用できなくなる可能性があります。この問題に対処するには、ラベルを使用して PD のスマート スケジューリングを有効にすることができます。これにより、 Raftグループが同じマシン上の複数の TiKV インスタンスに 3 つ以上のレプリカを持つことが保証されます。

    -   TiKV 構成

        同じホストレベルのラベル情報が同じ物理マシンに構成されます。

        ```yml
        config:
          server.labels:
            host: tikv1
        ```

    -   PD構成

        PD がリージョンを識別してスケジュールできるようにするには、PD のラベル タイプを構成します。

        ```yml
        pd:
          replication.location-labels: ["host"]
        ```

-   `numa_node`コアバインディング

    -   インスタンス パラメータ モジュールで、対応する`numa_node`パラメータを設定し、CPU コアの数を追加します。

    -   NUMA を使用してコアをバインドする前に、numactl ツールがインストールされていることを確認し、物理マシンの CPU の情報を確認してください。その後、パラメータを設定します。

    -   `numa_node`パラメータは`numactl --membind`設定に対応します。

> **注記：**
>
> -   構成ファイルのテンプレートを編集するときは、必要なパラメータ、IP、ポート、およびディレクトリを変更します。
> -   各コンポーネントは、デフォルトでグローバル`<deploy_dir>/<components_name>-<port>` `deploy_dir`として使用します。たとえば、TiDB がポート`4001`指定している場合、デフォルトではその`deploy_dir`は`/tidb-deploy/tidb-4001`です。したがって、複数インスタンスのシナリオでは、デフォルト以外のポートを指定するときに、ディレクトリを再度指定する必要はありません。
> -   構成ファイルに`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシン上に`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンの一貫性を保つことができます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
