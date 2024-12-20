---
title: Hybrid Deployment Topology
summary: TiDB クラスターのハイブリッド展開トポロジについて学習します。
---

# ハイブリッド展開トポロジ {#hybrid-deployment-topology}

このドキュメントでは、TiKV と TiDB のハイブリッド展開のトポロジと主要なパラメータについて説明します。

ハイブリッド展開は通常、次のシナリオで使用されます。

デプロイメントマシンには、十分なメモリを備えた複数の CPU プロセッサがあります。物理マシンリソースの利用率を向上させるために、複数のインスタンスを 1 台のマシンにデプロイできます。つまり、TiDB と TiKV の CPU リソースは、NUMA ノードバインディングによって分離されます。PD と Prometheus は一緒にデプロイされますが、それらのデータディレクトリは別のファイルシステムを使用する必要があります。

## トポロジ情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                     | IP                                   | コンフィグレーション                                                                                                                                                           |
| :------------- | :--- | :-------------------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | 6    | 32 VCore 64GB               | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | CPUコアをバインドするためにNUMAを構成する                                                                                                                                             |
| PD             | 3    | 16 VCore 32 GB              | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | `location_labels`パラメータを設定する                                                                                                                                          |
| ティクヴ           | 6    | 32 VCore 64GB               | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | <li>インスタンスレベルのポートと status_port を分離します。<br/> 2. グローバルパラメータ`readpool` `storage`設定します`raftstore`<br/> 3. インスタンスレベルのホストのラベルを構成します。<br/> 4. CPUコアをバインドするためにNUMAを構成する</li> |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB (SSD) | 10.0.1.10                            | デフォルト設定                                                                                                                                                              |

### トポロジーテンプレート {#topology-templates}

-   [ハイブリッド展開のためのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-multi-instance.yaml)
-   [ハイブリッド展開のための複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml)

上記の TiDB クラスタ トポロジ ファイルの構成項目の詳細については、 [TiUP を使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

### 主なパラメータ {#key-parameters}

このセクションでは、1 台のマシンに複数のインスタンスを展開する場合の重要なパラメータについて説明します。これは主に、TiDB および TiKV の複数のインスタンスが 1 台のマシンに展開されるシナリオで使用されます。以下の計算方法に従って、結果を構成テンプレートに入力する必要があります。

-   TiKVの設定を最適化する

    -   `readpool`スレッド プールに自己適応するように設定します。3 パラメータ`readpool.unified.max-thread-count`設定することで、 `readpool.storage`と`readpool.coprocessor`統合スレッド プールを共有し、それぞれ自己適応スイッチを設定できます。

        -   `readpool.storage`と`readpool.coprocessor`有効にする:

            ```yaml
            readpool.storage.use-unified-pool: true
            readpool.coprocessor.use-unified-pool: true
            ```

        -   計算方法：

                readpool.unified.max-thread-count = cores * 0.8 / the number of TiKV instances

    -   storageCF (すべての RocksDB 列ファミリ) をメモリに自己適応するように構成します。1 `storage.block-cache.capacity`を構成すると、CF が自動的にメモリ使用量をバランスさせることができます。

        -   計算方法：

                storage.block-cache.capacity = (MEM_TOTAL * 0.5 / the number of TiKV instances)

    -   複数の TiKV インスタンスが同じ物理ディスクにデプロイされている場合は、TiKV 構成に`capacity`パラメータを追加します。

            raftstore.capacity = disk total capacity / the number of TiKV instances

-   ラベルスケジュール設定

    1 台のマシンに複数の TiKV インスタンスがデプロイされているため、物理マシンがダウンすると、 Raftグループはデフォルトの 3 つのレプリカのうち 2 つを失い、クラスターが使用できなくなる可能性があります。この問題に対処するには、ラベルを使用して PD のスマート スケジューリングを有効にします。これにより、 Raftグループが同じマシン上の複数の TiKV インスタンスに 2 つ以上のレプリカを持つようになります。

    -   TiKVの構成

        同じ物理マシンに対して同じホストレベルのラベル情報が構成されています。

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

    -   インスタンスパラメータモジュールで、対応するパラメータ`numa_node`を設定し、CPU コアの数を追加します。

    -   NUMA を使用してコアをバインドする前に、numactl ツールがインストールされていることを確認し、物理マシンの CPU の情報を確認します。その後、パラメータを設定します。

    -   `numa_node`パラメータは`numactl --membind`構成に対応します。

> **注記：**
>
> -   構成ファイル テンプレートを編集するときは、必要なパラメータ、IP、ポート、およびディレクトリを変更します。
> -   各コンポーネントは、デフォルトでグローバル`<deploy_dir>/<components_name>-<port>` `deploy_dir`として使用します。たとえば、TiDB が`4001`ポートを指定した場合、デフォルトでは`deploy_dir` `/tidb-deploy/tidb-4001`になります。したがって、マルチインスタンス シナリオでは、デフォルト以外のポートを指定するときに、ディレクトリを再度指定する必要はありません。
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。TiUPTiUPコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーをコントロール マシンと一致させることもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
