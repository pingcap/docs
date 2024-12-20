---
title: Geo-distributed Deployment topology
summary: TiDB の地理的に分散されたデプロイメント トポロジについて学習します。
---

# 地理的に分散した展開トポロジ {#geo-distributed-deployment-topology}

このドキュメントでは、2 つの都市にある 3 つのデータ センター (DC) の一般的なアーキテクチャを例に、地理的に分散された展開アーキテクチャと主要な構成を紹介します。この例で使用される都市は、上海 ( `sha`と呼びます) と北京 ( `bja`と`bjb`と呼びます) です。

## トポロジ情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                          | BJ IP                                                  | 船         | コンフィグレーション                 |
| :------------- | :--- | :------------------------------- | :----------------------------------------------------- | :-------- | :------------------------- |
| ティビ            | 5    | 16 VCore 32GB * 1                | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3<br/> 10.0.1.4     | 10.0.1.5  | デフォルトポート<br/>グローバルディレクトリ構成 |
| PD             | 5    | 4 VCore 8GB * 1                  | 10.0.1.6<br/> 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9     | 10.0.1.10 | デフォルトポート<br/>グローバルディレクトリ構成 |
| ティクヴ           | 5    | 16 VCore 32GB 4TB (nvme ssd) * 1 | 10.0.1.11<br/> 10.0.1.12<br/> 10.0.1.13<br/> 10.0.1.14 | 10.0.1.15 | デフォルトポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB (SSD)      | 10.0.1.16                                              |           | デフォルトポート<br/>グローバルディレクトリ構成 |

### トポロジーテンプレート {#topology-templates}

-   [地理的に分散されたトポロジーテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)

上記の TiDB クラスタ トポロジ ファイルの構成項目の詳細については、 [TiUP を使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

### 主なパラメータ {#key-parameters}

このセクションでは、TiDB の地理的に分散されたデプロイメントの主要なパラメータ構成について説明します。

#### TiKVパラメータ {#tikv-parameters}

-   gRPC 圧縮形式 (デフォルトは`none` ):

    地理的に分散されたターゲット ノード間の gRPC パッケージの送信速度を上げるには、このパラメータを`gzip`に設定します。

    ```yaml
    server.grpc-compression-type: gzip
    ```

-   ラベル構成:

    TiKV は異なるデータ センターにまたがって展開されるため、物理マシンがダウンすると、 Raftグループはデフォルトの 5 つのレプリカのうち 3 つを失い、クラスターが使用できなくなる可能性があります。この問題に対処するには、PD のスマート スケジューリングを有効にするようにラベルを構成します。これにより、 Raftグループでは、同じデータ センターの同じキャビネット内の同じマシン上の TiKV インスタンスに 3 つのレプリカを配置できないようになります。

-   TiKV 構成:

    同じ物理マシンに対して同じホストレベルのラベル情報が構成されます。

    ```yaml
    config:
      server.labels:
        zone: bj
        dc: bja
        rack: rack1
        host: host2
    ```

-   リモート TiKV ノードが不要なRaft選出を開始するのを防ぐには、リモート TiKV ノードが選出を開始するために必要なティックの最小数と最大数を増やす必要があります。デフォルトでは、この 2 つのパラメータは`0`に設定されています。

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 50
    raftstore.raft-max-election-timeout-ticks: 60
    ```

> **注記：**
>
> `raftstore.raft-min-election-timeout-ticks`と`raftstore.raft-max-election-timeout-ticks`使用して TiKV ノードの選出タイムアウト ティックを大きく設定すると、そのノードの領域がリーダーになる可能性が大幅に低下します。ただし、一部の TiKV ノードがオフラインになり、残りのアクティブな TiKV ノードがRaftログで遅れをとる災害シナリオでは、選出タイムアウト ティックが大きいこの TiKV ノードの領域のみがリーダーになることができます。この TiKV ノードの領域は、選出を開始する前に少なくとも `raftstore.raft-min-election-timeout-ticks&#39; で設定された期間待機する必要があるため、このようなシナリオでクラスターの可用性に潜在的な影響が生じないように、これらの値を過度に大きく設定しないようにすることをお勧めします。

#### PDパラメータ {#pd-parameters}

-   PD メタデータ情報には、TiKV クラスターのトポロジが記録されます。PD は、次の 4 つの次元に基づいてRaftグループのレプリカをスケジュールします。

    ```yaml
    replication.location-labels: ["zone","dc","rack","host"]
    ```

-   クラスターの高可用性を確保するには、 Raftグループのレプリカの数を`5`に調整します。

    ```yaml
    replication.max-replicas: 5
    ```

-   リモート TiKVRaftレプリカがLeaderとして選出されることを禁止します。

    ```yaml
    label-property:
          reject-leader:
            - key: "dc"
              value: "sha"
    ```

    > **注記：**
    >
    > TiDB 5.2 以降、 `label-property`構成はデフォルトではサポートされていません。レプリカ ポリシーを設定するには、 [配置ルール](/configure-placement-rules.md)を使用します。

ラベルとRaftグループのレプリカの数に関する詳細については、 [トポロジラベルによるレプリカのスケジュール](/schedule-replicas-by-topology-labels.md)参照してください。

> **注記：**
>
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。TiUPTiUPコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーをコントロール マシンと一致させることもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
