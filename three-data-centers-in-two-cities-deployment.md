---
title: Three Availability Zones in Two Regions Deployment
summary: 2 つのリージョンの 3 つの可用性ゾーンへのデプロイメント ソリューションを学習します。
---

# 2つのリージョンに3つのアベイラビリティゾーンを展開 {#three-availability-zones-in-two-regions-deployment}

このドキュメントでは、2 つのリージョン展開における 3 つの可用性ゾーン (AZ) のアーキテクチャと構成について説明します。

このドキュメントの「リージョン」という用語は地理的なエリアを指し、大文字の「リージョン」は TiKV のデータstorageの基本単位を指します。「AZ」はリージョン内の隔離された場所を指し、各リージョンには複数の AZ があります。このドキュメントで説明されているソリューションは、1 つの都市に複数のデータ センターがあるシナリオにも適用されます。

## 概要 {#overview}

2 つのリージョンに 3 つの AZ を配置するアーキテクチャは、高可用性と耐障害性を備えたデプロイメント ソリューションであり、本番データ AZ、同じリージョンに災害復旧 AZ、別のリージョンに災害復旧 AZ を提供します。このモードでは、2 つのリージョンにある 3 つの AZ が相互接続されます。1 つの AZ に障害が発生したり災害が発生しても、他の AZ は引き続き正常に動作し、主要なアプリケーションまたはすべてのアプリケーションを引き継ぐことができます。1 つのリージョンに複数の AZ を配置するデプロイメントと比較して、このソリューションにはリージョン間の高可用性という利点があり、リージョン レベルの自然災害にも耐えることができます。

分散データベース TiDB は、 Raftアルゴリズムを使用して 2 リージョン 3 AZアーキテクチャをネイティブにサポートし、データベース クラスター内のデータの一貫性と高可用性を保証します。同じリージョン内の AZ 間のネットワークレイテンシーは比較的低いため、アプリケーション トラフィックを同じリージョン内の 2 つの AZ にディスパッチし、TiKVリージョンリーダーと PD リーダーの分散を制御することで、トラフィック負荷をこれら 2 つの AZ で共有できます。

## デプロイメントアーキテクチャ {#deployment-architecture}

このセクションでは、シアトルとサンフランシスコを例に、TiDB の分散データベースの 2 つのリージョンに 3 つの AZ を展開するモードについて説明します。

この例では、2 つの AZ (AZ1 と AZ2) がシアトルにあり、もう 1 つの AZ (AZ3) がサンフランシスコにあります。AZ1 と AZ2 間のネットワークレイテンシーは3 ミリ秒未満です。シアトルの AZ3 と AZ1/AZ2 間のネットワークレイテンシーは約 20 ミリ秒です (ISP 専用ネットワークを使用)。

クラスター展開のアーキテクチャは次のとおりです。

-   TiDB クラスターは、シアトルの AZ1、シアトルの AZ2、サンフランシスコの AZ3 の 2 つのリージョンの 3 つの AZ にデプロイされています。
-   クラスターには 5 つのレプリカがあり、AZ1 に 2 つ、AZ2 に 2 つ、AZ3 に 1 つあります。TiKVコンポーネントの場合、各ラックにラベルがあり、各ラックにレプリカがあることを意味します。
-   ユーザーにとって透過的なデータの一貫性と高可用性を確保するために、 Raftプロトコルが採用されています。

![3-AZ-in-2-region architecture](/media/three-data-centers-in-two-cities-deployment-01.png)

このアーキテクチャは可用性が高く、リージョンリーダーの分散は、同じリージョン (シアトル) にある 2 つの AZ (AZ1 と AZ2) に制限されています。リージョンリーダーの分散が制限されていない 3 つの AZ ソリューションと比較すると、このアーキテクチャには次の利点と欠点があります。

-   **利点**

    -   リージョンリーダーは、レイテンシーが低い同じリージョンの AZ にあるため、書き込みが高速になります。
    -   2つのAZが同時にサービスを提供できるため、リソースの使用率が高くなります。
    -   1 つの AZ に障害が発生しても、サービスは引き続き利用可能であり、データの安全性が確保されます。

-   **デメリット**

    -   データの一貫性はRaftアルゴリズムによって実現されるため、同じリージョンの 2 つの AZ が同時に障害を起こした場合、別のリージョン (サンフランシスコ) の災害復旧 AZ に生き残ったレプリカは 1 つだけ残ります。これでは、ほとんどのレプリカが生き残るというRaftアルゴリズムの要件を満たすことができません。その結果、クラスターが一時的に利用できなくなる可能性があります。保守スタッフは生き残った 1 つのレプリカからクラスターを復旧する必要があり、複製されていない少量のホット データが失われます。ただし、このようなケースはまれです。
    -   ISP 専用ネットワークが使用されるため、このアーキテクチャのネットワーク インフラストラクチャにはコストが高くなります。
    -   2 つのリージョンの 3 つの AZ に 5 つのレプリカが構成され、データの冗長性が増加し、storageコストが高くなります。

### 展開の詳細 {#deployment-details}

2 つのリージョン (シアトルとサンフランシスコ) の 3 つの AZ の展開プランの構成は、次のようになります。

![3-AZ-2-region](/media/three-data-centers-in-two-cities-deployment-02.png)

上の図から、シアトルには AZ1 と AZ2 の 2 つの AZ があることがわかります。AZ1 には、rac1、rac2、rac3 の 3 セットのラックがあります。AZ2 には、rac4 と rac5 の 2 つのラックがあります。サンフランシスコの AZ3 には、rac6 ラックがあります。

AZ1 の rac1 では、1 台のサーバーが TiDB および PD サービスとともにデプロイされ、他の 2 台のサーバーが TiKV サービスとともにデプロイされています。各 TiKVサーバーは、2 つの TiKV インスタンス (tikv-server) とともにデプロイされています。これは、rac2、rac4、rac5、および rac6 と同様です。

TiDBサーバー、制御マシン、および監視サーバーは rac3 上にあります。TiDBサーバーは、定期的なメンテナンスとバックアップ用にデプロイされています。Prometheus、Grafana、および復元ツールは、制御マシンと監視マシンにデプロイされています。

別のバックアップサーバーを追加して、 Drainer を展開することができます。Drainerは、ファイルを出力してbinlogデータを指定された場所に保存し、増分バックアップを実現します。

## コンフィグレーション {#configuration}

### 例 {#example}

たとえば、次の`tiup topology.yaml` yaml ファイルを参照してください。

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/data/tidb_cluster/tidb-deploy"
  data_dir: "/data/tidb_cluster/tidb-data"

server_configs:
  tikv:
    server.grpc-compression-type: gzip
  pd:
    replication.location-labels: ["az","replication zone","rack","host"]

pd_servers:
  - host: 10.63.10.10
    name: "pd-10"
  - host: 10.63.10.11
    name: "pd-11"
  - host: 10.63.10.12
    name: "pd-12"
  - host: 10.63.10.13
    name: "pd-13"
  - host: 10.63.10.14
    name: "pd-14"

tidb_servers:
  - host: 10.63.10.10
  - host: 10.63.10.11
  - host: 10.63.10.12
  - host: 10.63.10.13
  - host: 10.63.10.14

tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { az: "1", replication zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { az: "1", replication zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { az: "2", replication zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { az: "2", replication zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { az: "3", replication zone: "5", rack: "5", host: "34" }
      raftstore.raft-min-election-timeout-ticks: 50
      raftstore.raft-max-election-timeout-ticks: 60

monitoring_servers:
  - host: 10.63.10.60

grafana_servers:
  - host: 10.63.10.60

alertmanager_servers:
  - host: 10.63.10.60
```

### ラベルデザイン {#labels-design}

2 つのリージョンに 3 つの AZ を展開する場合、ラベル設計では可用性と災害復旧を考慮する必要があります。展開の物理構造に基づいて 4 つのレベル ( `az` 、 `replication zone` 、 `rack` 、および`host` ) を定義することをお勧めします。

![Label logical definition](/media/three-data-centers-in-two-cities-deployment-03.png)

PD 構成で、TiKV ラベルのレベル情報を追加します。

```yaml
server_configs:
  pd:
    replication.location-labels: ["az","replication zone","rack","host"]
```

`tikv_servers`の構成は、TiKV の実際の物理的な展開場所のラベル情報に基づいており、PD がグローバルな管理とスケジュールを実行しやすくなります。

```yaml
tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { az: "1", replication zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { az: "1", replication zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { az: "2", replication zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { az: "2", replication zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { az: "3", replication zone: "5", rack: "5", host: "34" }
```

### パラメータ設定を最適化する {#optimize-parameter-configuration}

2 つのリージョンに 3 つの AZ を展開する場合、パフォーマンスを最適化するには、通常のパラメータを設定するだけでなく、コンポーネントパラメータも調整する必要があります。

-   TiKV で gRPC メッセージ圧縮を有効にします。クラスターのデータはネットワークで送信されるため、gRPC メッセージ圧縮を有効にしてネットワーク トラフィックを削減できます。

    ```yaml
    server.grpc-compression-type: gzip
    ```

-   別のリージョン (サンフランシスコ) の TiKV ノードのネットワーク構成を最適化します。サンフランシスコの AZ3 の次の TiKV パラメータを変更し、この TiKV ノードのレプリカがRaft選出に参加しないようにします。

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 50
    raftstore.raft-max-election-timeout-ticks: 60
    ```

> **注記：**
>
> `raftstore.raft-min-election-timeout-ticks`と`raftstore.raft-max-election-timeout-ticks`を使用して TiKV ノードの選出タイムアウト ティックを大きく設定すると、そのノードの領域がリーダーになる可能性が大幅に低下します。ただし、一部の TiKV ノードがオフラインで、残りのアクティブな TiKV ノードがRaftログで遅れているという災害シナリオでは、選出タイムアウト ティックが大きいこの TiKV ノードの領域のみがリーダーになることができます。この TiKV ノードの領域は、選出を開始する前に少なくとも `raftstore.raft-min-election-timeout-ticks&#39; で設定された期間待機する必要があるため、このようなシナリオでクラスターの可用性に潜在的な影響が生じないように、これらの値を過度に大きく設定しないようにすることをお勧めします。

-   スケジュールを構成します。クラスターが有効になったら、 `tiup ctl:v{CLUSTER_VERSION} pd`ツールを使用してスケジュール ポリシーを変更します。TiKV Raftレプリカの数を変更します。この数は計画どおりに構成します。この例では、レプリカの数は 5 です。

    ```bash
    config set max-replicas 5
    ```

-   Raftリーダーを AZ3 にスケジュールすることを禁止します。Raft リーダーを別のリージョン (AZ3) にスケジュールすると、シアトルの AZ1/AZ2 とサンフランシスコの AZ3 の間に不要なネットワーク オーバーヘッドが発生します。ネットワーク帯域幅とレイテンシーも TiDB クラスターのパフォーマンスに影響します。

    ```bash
    config set label-property reject-leader dc 3
    ```

    > **注記：**
    >
    > TiDB v5.2 以降では、 `label-property`構成はデフォルトでサポートされません。レプリカ ポリシーを設定するには、 [配置ルール](/configure-placement-rules.md)を使用します。

-   PD の優先度を設定します。PD リーダーが別のリージョン (AZ3) にある状況を回避するには、ローカル PD (シアトル) の優先度を上げ、別のリージョン (サンフランシスコ) の PD の優先度を下げることができます。数値が大きいほど、優先度が高くなります。

    ```bash
    member leader_priority PD-10 5
    member leader_priority PD-11 5
    member leader_priority PD-12 5
    member leader_priority PD-13 5
    member leader_priority PD-14 1
    ```
