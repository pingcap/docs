---
title: Geo-distributed Deployment topology
summary: TiDB の地理的に分散された展開トポロジについて学習します。
---

# 地理的に分散した展開トポロジ {#geo-distributed-deployment-topology}

このドキュメントでは、2つの都市に3つのデータセンター（DC）を配置した典型的なアーキテクチャを例に、地理的に分散したデプロイメントアーキテクチャと主要な構成について説明します。この例で使用する都市は、上海（ `sha` ）と北京（ `bja`と`bjb` ）です。

## トポロジ情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                          | BJ IP                                                  | 船         | コンフィグレーション                 |
| :------------- | :--- | :------------------------------- | :----------------------------------------------------- | :-------- | :------------------------- |
| TiDB           | 5    | 16 VCore 32GB * 1                | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3<br/> 10.0.1.4     | 10.0.1.5  | デフォルトポート<br/>グローバルディレクトリ構成 |
| PD             | 5    | 4 VCore 8GB * 1                  | 10.0.1.6<br/> 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9     | 10.0.1.10 | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiKV           | 5    | 16 VCore 32GB 4TB (nvme ssd) * 1 | 10.0.1.11<br/> 10.0.1.12<br/> 10.0.1.13<br/> 10.0.1.14 | 10.0.1.15 | デフォルトポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB (SSD)      | 10.0.1.16                                              |           | デフォルトポート<br/>グローバルディレクトリ構成 |

> **注記：**
>
> インスタンスのIPアドレスは例としてのみ示されています。実際の導入では、IPアドレスを実際のIPアドレスに置き換えてください。

### トポロジテンプレート {#topology-templates}

-   [地理的に分散したトポロジテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

### 主なパラメータ {#key-parameters}

このセクションでは、TiDB の地理的に分散されたデプロイメントの主要なパラメータ構成について説明します。

#### TiKVパラメータ {#tikv-parameters}

-   gRPC 圧縮形式 (デフォルトは`none` ):

    地理的に分散されたターゲットノード間の gRPC パッケージの転送速度を上げるには、このパラメータを`gzip`に設定します。

    ```yaml
    server.grpc-compression-type: gzip
    ```

-   ラベル構成:

    TiKVは複数のデータセンターにまたがって展開されているため、物理マシンがダウンすると、 Raftグループはデフォルトの5つのレプリカのうち3つを失い、クラスターが利用できなくなる可能性があります。この問題に対処するには、ラベルを設定してPDのスマートスケジューリングを有効にします。これにより、 Raftグループは、同じデータセンターの同じキャビネット内の同じマシン上のTiKVインスタンスに3つのレプリカを配置することを許可しません。

-   TiKV 構成:

    同じ物理マシンに対して同じホストレベルのラベル情報が構成されています。

    ```yaml
    config:
      server.labels:
        zone: bj
        dc: bja
        rack: rack1
        host: host2
    ```

-   リモートTiKVノードが不要なRaft選出を開始するのを防ぐには、リモートTiKVノードが選出を開始するために必要な最小ティック数と最大ティック数を増やす必要があります。これらの2つのパラメータはデフォルトで`0`に設定されています。

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 50
    raftstore.raft-max-election-timeout-ticks: 60
    ```

> **注記：**
>
> TiKVノードの選出タイムアウト値を`raftstore.raft-min-election-timeout-ticks`と`raftstore.raft-max-election-timeout-ticks`大きく設定すると、そのノード上のリージョンがリーダーになる可能性が大幅に低下します。ただし、一部のTiKVノードがオフラインになり、残りのアクティブなTiKVノードのRaftログが遅延しているような災害シナリオでは、このTiKVノード上の選出タイムアウト値が大きいリージョンのみがリーダーになることができます。このTiKVノード上のリージョンは、選出を開始する前に少なくとも`raftstore.raft-min-election-timeout-ticks`で設定された期間待機する必要があるため、このようなシナリオではクラスターの可用性への影響を防ぐため、これらの値を過度に大きく設定しないことをお勧めします。

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
    > TiDB 5.2以降、 `label-property`構成はデフォルトではサポートされません。レプリカポリシーを設定するには、 [配置ルール](/configure-placement-rules.md)使用してください。

ラベルとRaftグループのレプリカの数に関する詳細については、 [トポロジラベルによるレプリカのスケジュール](/schedule-replicas-by-topology-labels.md)参照してください。

> **注記：**
>
> -   設定ファイルに`tidb`ユーザーを手動で作成する必要はありません。TiUPTiUPコンポーネントは、ターゲットマシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、コントロールマシンと同じユーザーを維持することもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
