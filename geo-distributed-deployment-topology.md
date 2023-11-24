---
title: Geo-distributed Deployment topology
summary: Learn the geo-distributed deployment topology of TiDB.
---

# 地理的に分散した導入トポロジ {#geo-distributed-deployment-topology}

このドキュメントでは、2 つの都市にある 3 つのデータ センター (DC) の一般的なアーキテクチャを例に挙げ、地理的に分散された展開アーキテクチャと主要な構成を紹介します。この例で使用されている都市は、上海 ( `sha`と呼ばれます) と北京 ( `bja`および`bjb`と呼ばれます) です。

## トポロジ情報 {#topology-information}

| 実例           | カウント | 物理マシンの構成                         | BJ IP                                                  | 船         | コンフィグレーション                  |
| :----------- | :--- | :------------------------------- | :----------------------------------------------------- | :-------- | :-------------------------- |
| TiDB         | 5    | 16Vコア 32GB*1                     | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3<br/> 10.0.1.4     | 10.0.1.5  | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD           | 5    | 4Vコア8GB*1                        | 10.0.1.6<br/> 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9     | 10.0.1.10 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiKV         | 5    | 16 VCore 32GB 4TB (nvme ssd) * 1 | 10.0.1.11<br/> 10.0.1.12<br/> 10.0.1.13<br/> 10.0.1.14 | 10.0.1.15 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニタリングとグラファナ | 1    | 4 VCore 8GB * 1 500GB (SSD)      | 10.0.1.16                                              |           | デフォルトのポート<br/>グローバルディレクトリ構成 |

### トポロジテンプレート {#topology-templates}

-   [地理的に分散されたトポロジ テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)

上記の TiDB クラスター トポロジー ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB を展開するためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 主要パラメータ {#key-parameters}

このセクションでは、TiDB 地理分散展開の主要なパラメーター構成について説明します。

#### TiKVパラメータ {#tikv-parameters}

-   gRPC 圧縮形式 (デフォルトでは`none` ):

    地理的に分散されたターゲット ノード間の gRPC パッケージの送信速度を高めるには、このパラメーターを`gzip`に設定します。

    ```yaml
    server.grpc-compression-type: gzip
    ```

-   ラベル構成:

    TiKV は異なるデータセンターに展開されているため、物理マシンがダウンすると、 Raftグループはデフォルトの 5 つのレプリカのうち 3 つを失い、クラスターが使用できなくなる可能性があります。この問題に対処するには、ラベルを構成して PD のスマート スケジューリングを有効にすることができます。これにより、 Raftグループは、同じデータ センターの同じキャビネット内の同じマシン上の TiKV インスタンスに 3 つのレプリカを配置することができなくなります。

-   TiKV 構成:

    同じホストレベルのラベル情報が同じ物理マシンに構成されます。

    ```yaml
    config:
      server.labels:
        zone: bj
        dc: bja
        rack: rack1
        host: host2
    ```

-   リモート TiKV ノードが不必要なRaft選挙を開始しないようにするには、リモート TiKV ノードが選挙を開始するために必要な最小および最大ティック数を増やす必要があります。 2 つのパラメータはデフォルトで`0`に設定されます。

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 1000
    raftstore.raft-max-election-timeout-ticks: 1020
    ```

#### PDパラメータ {#pd-parameters}

-   PD メタデータ情報には、TiKV クラスターのトポロジーが記録されます。 PD は、次の 4 つの次元でRaftグループ レプリカをスケジュールします。

    ```yaml
    replication.location-labels: ["zone","dc","rack","host"]
    ```

-   クラスターの高可用性を確保するには、 Raftグループのレプリカの数を`5`に調整します。

    ```yaml
    replication.max-replicas: 5
    ```

-   リモート TiKV RaftレプリカがLeaderとして選出されることを禁止します。

    ```yaml
    label-property:
          reject-leader:
            - key: "dc"
              value: "sha"
    ```

    > **注記：**
    >
    > TiDB 5.2 以降、 `label-property`構成はデフォルトではサポートされていません。レプリカ ポリシーを設定するには、 [配置ルール](/configure-placement-rules.md)を使用します。

ラベルとRaftグループ レプリカの数の詳細については、 [トポロジーラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md)を参照してください。

> **注記：**
>
> -   構成ファイルに`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンの一貫性を保つことができます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
