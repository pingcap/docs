---
title: Geo-distributed Deployment topology
summary: Learn the geo-distributed deployment topology of TiDB.
---

# 地理的に分散された展開トポロジ {#geo-distributed-deployment-topology}

このドキュメントでは、2つの都市にある3つのデータセンター（DC）の一般的なアーキテクチャを例として取り上げ、地理的に分散した展開アーキテクチャと主要な構成を紹介します。この例で使用されている都市は、上海（ `sha`と呼ばれる）と北京（ `bja`と`bjb`と呼ばれる）です。

## トポロジー情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                        | BJ IP                                                  | 輸送する      | Configuration / コンフィグレーション  |
| :------------- | :--- | :----------------------------- | :----------------------------------------------------- | :-------- | :-------------------------- |
| TiDB           | 5    | 16 VCore 32GB * 1              | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3<br/> 10.0.1.4     | 10.0.1.5  | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD             | 5    | 4 VCore 8GB * 1                | 10.0.1.6<br/> 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9     | 10.0.1.10 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiKV           | 5    | 16 VCore 32GB 2TB（nvme ssd）* 1 | 10.0.1.11<br/> 10.0.1.12<br/> 10.0.1.13<br/> 10.0.1.14 | 10.0.1.15 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB（ssd）     | 10.0.1.16                                              |           | デフォルトのポート<br/>グローバルディレクトリ構成 |

### トポロジテンプレート {#topology-templates}

-   [地理的に分散されたトポロジテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)

上記のTiDBクラスタトポロジファイルの構成項目の詳細については、 [TiUPを使用してTiDBを展開するためのトポロジConfiguration / コンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 重要なパラメータ {#key-parameters}

このセクションでは、TiDB地理分散展開の主要なパラメーター構成について説明します。

#### TiKVパラメータ {#tikv-parameters}

-   gRPC圧縮形式（デフォルトでは`none` ）：

    地理的に分散されたターゲットノード間のgRPCパッケージの伝送速度を上げるには、このパラメーターを`gzip`に設定します。

    ```yaml
    server.grpc-compression-type: gzip
    ```

-   ラベル構成：

    TiKVはさまざまなデータセンターに展開されているため、物理マシンがダウンすると、Raft Groupはデフォルトの5つのレプリカのうち3つを失い、クラスタが使用できなくなる可能性があります。この問題に対処するには、PDのスマートスケジューリングを有効にするようにラベルを構成できます。これにより、Raft Groupは、同じデータセンターの同じキャビネット内の同じマシン上のTiKVインスタンスに3つのレプリカを配置できなくなります。

-   TiKV構成：

    同じ物理マシンに対して、同じホストレベルのラベル情報が設定されます。

    ```yaml
    config:
      server.labels:
        zone: bj
        dc: bja
        rack: rack1
        host: host2
    ```

-   リモートTiKVノードが不要なRaft選挙を開始しないようにするには、リモートTiKVノードが選挙を開始するために必要なティックの最小数と最大数を増やす必要があります。 2つのパラメータはデフォルトで`0`に設定されています。

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 1000
    raftstore.raft-max-election-timeout-ticks: 1020
    ```

#### PDパラメータ {#pd-parameters}

-   PDメタデータ情報は、TiKVクラスタのトポロジーを記録します。 PDは、RaftGroupレプリカを次の4つのディメンションでスケジュールします。

    ```yaml
    replication.location-labels: ["zone","dc","rack","host"]
    ```

-   クラスタの高可用性を確保するには、RaftGroupレプリカの数を`5`に調整します。

    ```yaml
    replication.max-replicas: 5
    ```

-   リモートTiKVRaftレプリカがリーダーとして選出されることを禁止します。

    ```yaml
    label-property:
          reject-leader:
            - key: "dc"
              value: "sha"
    ```

    > **ノート：**
    >
    > TiDB 5.2以降、 `label-property`構成はデフォルトでサポートされていません。レプリカポリシーを設定するには、 [配置ルール](/configure-placement-rules.md)を使用します。

ラベルとRaftGroupレプリカの数の詳細については、 [トポロジラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md)を参照してください。

> **ノート：**
>
> -   構成ファイルに`tidb`人のユーザーを手動で作成する必要はありません。 TiUPクラスタコンポーネントは、ターゲットマシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーを制御マシンとの一貫性を保つこともできます。
> -   展開ディレクトリを相対パスとして構成すると、クラスタはユーザーのホームディレクトリに展開されます。
