---
title: Hybrid Deployment Topology
summary: TiDB クラスターのハイブリッド展開トポロジについて学習します。
---

# ハイブリッド展開トポロジ {#hybrid-deployment-topology}

このドキュメントでは、TiKV と TiDB のハイブリッド展開のトポロジと主要なパラメータについて説明します。

ハイブリッド展開は通常、次のシナリオで使用されます。

デプロイメントマシンには、十分なメモリを備えた複数のCPUプロセッサが搭載されています。物理マシンリソースの利用率を向上させるため、TiDBとTiKVのCPUリソースはNUMAノードバインディングによって分離され、単一のマシンに複数のインスタンスをデプロイできます。PDとPrometheusは一緒にデプロイされますが、それぞれのデータディレクトリは別々のファイルシステムを使用する必要があります。

## トポロジ情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                     | IP                                   | コンフィグレーション                                                                                                                                                             |
| :------------- | :--- | :-------------------------- | :----------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | 6    | 32 VCore 64GB               | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | CPUコアをバインドするためにNUMAを構成する                                                                                                                                               |
| PD             | 3    | 16 VCore 32 GB              | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | `location_labels`パラメータを設定する                                                                                                                                            |
| TiKV           | 6    | 32 VCore 64GB               | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | <li>インスタンス レベルのポートと status_port を分離します。<br/> 2. グローバルパラメータ`readpool` `storage`設定します`raftstore`<br/> 3. インスタンス レベルのホストのラベルを構成します。<br/> 4. CPUコアをバインドするためのNUMAを構成する</li> |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB (SSD) | 10.0.1.10                            | デフォルト設定                                                                                                                                                                |

> **注記：**
>
> インスタンスのIPアドレスは例としてのみ示されています。実際の導入では、IPアドレスを実際のIPアドレスに置き換えてください。

### トポロジテンプレート {#topology-templates}

-   [ハイブリッド展開のためのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-multi-instance.yaml)
-   [ハイブリッド展開のための複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

### 主なパラメータ {#key-parameters}

このセクションでは、単一マシンに複数のインスタンスをデプロイする際の主要なパラメータについて説明します。これは主に、単一マシンにTiDBとTiKVの複数のインスタンスをデプロイするシナリオで使用されます。以下の計算方法に従って、結果を構成テンプレートに入力する必要があります。

-   TiKVの設定を最適化する

    -   `readpool`スレッドプールに自己適応するように設定します。3 パラメータ`readpool.unified.max-thread-count`設定することで、 `readpool.storage`と`readpool.coprocessor`統合スレッドプールを共有し、それぞれ自己適応スイッチを設定できます。

        -   `readpool.storage`と`readpool.coprocessor`有効にする:

            ```yaml
            readpool.storage.use-unified-pool: true
            readpool.coprocessor.use-unified-pool: true
            ```

        -   計算方法：

                readpool.unified.max-thread-count = cores * 0.8 / the number of TiKV instances

    -   storageCF（すべてのRocksDB列ファミリー）をメモリに適応させるように設定するには、 `storage.block-cache.capacity`パラメータを設定することで、CFがメモリ使用量を自動的に調整できるようになります。

        -   計算方法：

                storage.block-cache.capacity = (MEM_TOTAL * 0.5 / the number of TiKV instances)

    -   複数の TiKV インスタンスが同じ物理ディスクにデプロイされている場合は、TiKV 構成に`capacity`パラメータを追加します。

            raftstore.capacity = disk total capacity / the number of TiKV instances

-   ラベルスケジュール設定

    1台のマシンに複数のTiKVインスタンスがデプロイされているため、物理マシンがダウンすると、 Raftグループはデフォルトの3つのレプリカのうち2つを失い、クラスターが利用できなくなる可能性があります。この問題に対処するには、ラベルを使用してPDのスマートスケジューリングを有効にします。これにより、 Raftグループは同一マシン上の複数のTiKVインスタンスに2つ以上のレプリカを持つようになります。

    -   TiKV構成

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

    -   インスタンスパラメータモジュールで、対応するパラメータ`numa_node`を設定し、CPUコアの数を追加します。

    -   NUMAを使用してコアをバインドする前に、numactlツールがインストールされていること、および物理マシンのCPU情報を確認してください。その後、パラメータを設定してください。

    -   `numa_node`パラメータは`numactl --membind`構成に対応します。

> **注記：**
>
> -   構成ファイル テンプレートを編集するときは、必要なパラメータ、IP、ポート、およびディレクトリを変更します。
> -   各コンポーネントは、グローバルポートの`<deploy_dir>/<components_name>-<port>`デフォルトでポート`deploy_dir`として使用します。例えば、TiDBがポート`4001`を指定した場合、そのポート`deploy_dir`デフォルトで`/tidb-deploy/tidb-4001`なります。したがって、マルチインスタンスのシナリオでは、デフォルト以外のポートを指定する場合、ディレクトリを再度指定する必要はありません。
> -   設定ファイルに`tidb`ユーザーを手動で作成する必要はありません。TiUPTiUPコンポーネントは、ターゲットマシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、コントロールマシンと同じユーザーを維持することもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
