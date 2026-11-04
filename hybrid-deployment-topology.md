---
title: Hybrid Deployment Topology
summary: TiDB クラスターのハイブリッド展開トポロジーについて学習します。
---

# ハイブリッド展開トポロジー {#hybrid-deployment-topology}

このドキュメントでは、TiKV と TiDB のハイブリッドデプロイのトポロジーと主要なパラメーターについて説明します。

ハイブリッドデプロイは通常、次のシナリオで使用されます。

デプロイメントマシンには、十分なメモリを備えた複数のCPUプロセッサーが搭載されています。物理マシンリソースの利用率を向上させるため、TiDBとTiKVのCPUリソースはNUMAノードバインディングによって分離され、単一のマシンに複数のインスタンスをデプロイできます。PDとPrometheusは一緒にデプロイされますが、それぞれのデータディレクトリは別々のファイルシステムを使用する必要があります。

## トポロジー情報 {#topology-information}

| インスタンス             | 数 | 物理マシン構成                     | IP                                   | 設定                                                                                                                                                             |
| :------------- | :--- | :-------------------------- | :----------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | 6    | 32 VCore 64GB               | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | CPUコアをバインドするためにNUMAを構成する                                                                                                                                               |
| PD             | 3    | 16 VCore 32 GB              | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | `location_labels`パラメーターを設定する                                                                                                                                            |
| TiKV           | 6    | 32 VCore 64GB               | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | <li>1. インスタンスレベルのポートと status_port を分離します。<br/> 2. グローバルパラメーター `readpool`、`storage`、`raftstore`を設定します。<br/> 3. インスタンスレベルのホストのラベルを構成します。<br/> 4. CPUコアをバインドするためのNUMAを構成する</li> |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB (SSD) | 10.0.1.10                            | デフォルト設定                                                                                                                                                                |

> **Note:**
>
> インスタンスのIPアドレスは例としてのみ示されています。実際の導入では、IPアドレスを実際のIPアドレスに置き換えてください。

### トポロジーテンプレート {#topology-templates}

- [ハイブリッドデプロイのためのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-multi-instance.yaml)
- [ハイブリッドデプロイのための複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml)

上記の TiDB クラスタートポロジーファイルの設定項目の詳細については、 [TiUPを使用して TiDB をデプロイするためのトポロジー設定ファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 主なパラメーター {#key-parameters}

このセクションでは、単一マシンに複数のインスタンスをデプロイする際の主要なパラメーターについて説明します。これは主に、単一マシンにTiDBとTiKVの複数のインスタンスをデプロイするシナリオで使用されます。以下の計算方法に従って、結果を構成テンプレートに入力する必要があります。

- TiKVの設定を最適化する

    - `readpool`スレッドプールに自己適応するように設定します。`readpool.unified.max-thread-count`パラメーターを設定することで、 `readpool.storage`と`readpool.coprocessor`が統合スレッドプールを共有し、それぞれ自己適応スイッチを設定できます。

        - `readpool.storage`と`readpool.coprocessor`を有効にする:

            ```yaml
            readpool.storage.use-unified-pool: true
            readpool.coprocessor.use-unified-pool: true
            ```

        - 計算方法：

            ```
            readpool.unified.max-thread-count = cores * 0.8 / the number of TiKV instances
            ```

    - storageCF（すべてのRocksDB列ファミリー）をメモリに適応させるように設定するには、 `storage.block-cache.capacity`パラメーターを設定することで、CFがメモリ使用量を自動的に調整できるようになります。

        - 計算方法：

            ```
            storage.block-cache.capacity = (MEM_TOTAL * 0.5 / the number of TiKV instances)
            ```

    - 複数の TiKV インスタンスが同じ物理ディスクにデプロイされている場合は、TiKV 構成に`capacity`パラメーターを追加します。

        ```
        raftstore.capacity = disk total capacity / the number of TiKV instances
        ```

- ラベルスケジュール設定

    1台のマシンに複数のTiKVインスタンスがデプロイされているため、物理マシンがダウンすると、 Raftグループはデフォルトの3つのレプリカのうち2つを失い、クラスターが利用できなくなる可能性があります。この問題に対処するには、ラベルを使用してPDのスマートスケジューリングを有効にします。これにより、 Raftグループは同一マシン上の複数のTiKVインスタンスに2つ以上のレプリカを持つようになります。

    - TiKV構成

        同じ物理マシンに対して同じホストレベルのラベル情報が構成されています。

        ```yml
        config:
          server.labels:
            host: tikv1
        ```

    - PD構成

        PD がリージョンを識別してスケジュールできるようにするには、PD のラベルタイプを構成します。

        ```yml
        pd:
          replication.location-labels: ["host"]
        ```

- `numa_node`コアバインディング

    - インスタンスパラメーターモジュールで、対応するパラメーター`numa_node`を設定し、CPUコアの数を追加します。

    - NUMAを使用してコアをバインドする前に、numactlツールがインストールされていること、および物理マシンのCPU情報を確認してください。その後、パラメーターを設定してください。

    - `numa_node`パラメーターは`numactl --membind`構成に対応します。

> **Note:**
>
> - 設定ファイルテンプレートを編集するときは、必要なパラメーター、IP、ポート、およびディレクトリを変更します。
> - 各コンポーネントでは、グローバルポートの`<deploy_dir>/<components_name>-<port>`がデフォルトの`deploy_dir`として使用されます。例えば、TiDBにポート`4001`を指定した場合、そのポートの`deploy_dir`はデフォルトで`/tidb-deploy/tidb-4001`になります。したがって、マルチインスタンスのシナリオでは、デフォルト以外のポートを指定する場合でも、ディレクトリを再度指定する必要はありません。
> - 設定ファイルに`tidb`ユーザーを手動で作成する必要はありません。TiUPTiUPコンポーネントは、ターゲットマシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、コントロールマシンと同じユーザーを維持することもできます。
> - デプロイメントディレクトリを相対パスとして構成すると、クラスターはユーザーのホームディレクトリにデプロイされます。
