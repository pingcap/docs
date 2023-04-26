---
title: Geo-distributed Deployment topology
summary: Learn the geo-distributed deployment topology of TiDB.
---

# 地理的に分散された展開トポロジ {#geo-distributed-deployment-topology}

このドキュメントでは、2 つの都市にある 3 つのデータ センター (DC) の典型的なアーキテクチャを例として取り上げ、地理的に分散した展開アーキテクチャと主要な構成を紹介します。この例で使用されている都市は、上海 ( `sha`と呼ばれる) と北京 ( `bja`と`bjb`と呼ばれる) です。

## トポロジ情報 {#topology-information}

| 実例         | カウント | 物理マシン構成                         | BJ IP                                                  | 船         | コンフィグレーション                    |
| :--------- | :--- | :------------------------------ | :----------------------------------------------------- | :-------- | :---------------------------- |
| TiDB       | 5    | 16 仮想コア 32GB * 1                | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3<br/> 10.0.1.4     | 10.0.1.5  | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| PD         | 5    | 4 Vコア 8GB * 1                   | 10.0.1.6<br/> 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9     | 10.0.1.10 | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| TiKV       | 5    | 16 仮想コア 32GB 2TB (nvme ssd) * 1 | 10.0.1.11<br/> 10.0.1.12<br/> 10.0.1.13<br/> 10.0.1.14 | 10.0.1.15 | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| 監視とGrafana | 1    | 4 仮想コア 8GB * 1 500GB (ssd)      | 10.0.1.16                                              |           | デフォルトのポート<br/>グローバル ディレクトリの構成 |

### トポロジ テンプレート {#topology-templates}

-   [地理的に分散したトポロジ テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 主なパラメータ {#key-parameters}

このセクションでは、TiDB の地理的分散配置の主要なパラメーター構成について説明します。

#### TiKV パラメータ {#tikv-parameters}

-   gRPC 圧縮形式 (デフォルトでは`none` ):

    地理的に分散されたターゲット ノード間の gRPC パッケージの転送速度を上げるには、このパラメーターを`gzip`に設定します。

    ```yaml
    server.grpc-compression-type: gzip
    ```

-   ラベル構成:

    TiKV は異なるデータ センターに展開されるため、物理マシンがダウンすると、 Raftグループはデフォルトの 5 つのレプリカのうち 3 つを失い、クラスターが使用できなくなる可能性があります。この問題に対処するには、PD のスマート スケジューリングを有効にするようにラベルを構成できます。これにより、 Raftグループが、同じデータ センターの同じキャビネット内の同じマシン上の TiKV インスタンスに 3 つのレプリカを配置することを許可しなくなります。

-   TiKV 構成:

    同じ物理マシンに対して、同じホスト レベルのラベル情報が構成されています。

    ```yaml
    config:
      server.labels:
        zone: bj
        dc: bja
        rack: rack1
        host: host2
    ```

-   リモート TiKV ノードが不要なRaft選出を開始するのを防ぐには、リモート TiKV ノードが選出を開始するために必要なティックの最小数と最大数を増やす必要があります。デフォルトでは、2 つのパラメータは`0`に設定されています。

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 1000
    raftstore.raft-max-election-timeout-ticks: 1020
    ```

#### PD パラメータ {#pd-parameters}

-   PD メタデータ情報は、TiKV クラスターのトポロジーを記録します。 PD は、次の 4 つのディメンションでRaftグループのレプリカをスケジュールします。

    ```yaml
    replication.location-labels: ["zone","dc","rack","host"]
    ```

-   クラスターの高可用性を確保するには、 Raftグループ レプリカの数を`5`に調整します。

    ```yaml
    replication.max-replicas: 5
    ```

-   リモートの TiKV RaftレプリカがLeaderとして選出されることを禁止します。

    ```yaml
    label-property:
          reject-leader:
            - key: "dc"
              value: "sha"
    ```

    > **ノート：**
    >
    > TiDB 5.2 以降、デフォルトでは`label-property`構成はサポートされていません。レプリカ ポリシーを設定するには、 [配置ルール](/configure-placement-rules.md)を使用します。

ラベルとRaftグループ レプリカの数についての詳細は、 [トポロジ ラベルごとにレプリカをスケジュールする](/schedule-replicas-by-topology-labels.md)を参照してください。

> **ノート：**
>
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンとの一貫性を保つことができます。
> -   展開ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリに展開されます。
