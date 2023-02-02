---
title: Three Data Centers in Two Cities Deployment
summary: Learn the deployment solution to three data centers in two cities.
---

# 2 つの地域に配置された 3 つのデータ センター {#three-data-centers-in-two-cities-deployment}

このドキュメントでは、2 つの都市に配置された 3 つのデータ センター (DC) のアーキテクチャと構成について説明します。

## 概要 {#overview}

2 つの都市にある 3 つの DC のアーキテクチャは、本番データ センター、同じ都市のディザスター リカバリー センター、および別の都市のディザスター リカバリー センターを提供する、高可用性と耐障害性のある展開ソリューションです。このモードでは、2 つの都市の 3 つの DC が相互接続されます。 1 つの DC に障害が発生したり、障害が発生したりした場合でも、他の DC は正常に動作し、主要なアプリケーションまたはすべてのアプリケーションを引き継ぐことができます。 1 つの都市に配置された複数の DC と比較して、このソリューションには都市間の高可用性という利点があり、都市レベルの自然災害に耐えることができます。

分散データベース TiDB は、 Raftアルゴリズムを使用することで 2 都市に 3 つの DCアーキテクチャをネイティブにサポートし、データベース クラスター内のデータの一貫性と高可用性を保証します。同じ都市内の DC 間のネットワークレイテンシーは比較的低いため、アプリケーション トラフィックは同じ都市内の 2 つの DC にディスパッチでき、TiKVリージョンリーダーと PD リーダーの分散を制御することで、これら 2 つの DC でトラフィック負荷を共有できます。 .

## 導入アーキテクチャ {#deployment-architecture}

このセクションでは、シアトルとサンフランシスコの例を挙げて、TiDB の分散データベースの 2 つの都市にある 3 つの DC の配置モードについて説明します。

この例では、2 つの DC (IDC1 と IDC2) がシアトルにあり、別の DC (IDC3) がサンフランシスコにあります。 IDC1 と IDC2 の間のネットワークレイテンシーは 3 ミリ秒未満です。シアトルの IDC3 と IDC1/IDC2 間のネットワークレイテンシーは約 20 ミリ秒です (ISP 専用ネットワークを使用)。

クラスタ展開のアーキテクチャは次のとおりです。

-   TiDB クラスターは、シアトルの IDC1、シアトルの IDC2、およびサンフランシスコの IDC3 の 2 つの都市にある 3 つの DC にデプロイされます。
-   クラスタには、IDC1 に 2 つ、IDC2 に 2 つ、IDC3 に 1 つの 5 つのレプリカがあります。 TiKVコンポーネントの場合、各ラックにはラベルがあり、これは各ラックにレプリカがあることを意味します。
-   Raftプロトコルは、データの一貫性と高可用性を確保するために採用されており、ユーザーに対して透過的です。

![3-DC-in-2-city architecture](/media/three-data-centers-in-two-cities-deployment-01.png)

このアーキテクチャは可用性が高いです。リージョンリーダーの配布は、同じ都市 (シアトル) にある 2 つの DC (IDC1 と IDC2) に制限されています。リージョンリーダーの配布が制限されていない 3 DC ソリューションと比較すると、このアーキテクチャには次の長所と短所があります。

-   **利点**

    -   リージョンリーダーは同じ都市の DC にあり、レイテンシーが短いため、書き込みは高速です。
    -   2 つの DC が同時にサービスを提供できるため、リソースの使用率が高くなります。
    -   1 つの DC に障害が発生した場合でも、サービスは引き続き利用可能で、データの安全性が確保されます。

-   **短所**

    -   データの整合性はRaftアルゴリズムによって達成されるため、同じ都市の 2 つの DC が同時に故障した場合、別の都市 (サンフランシスコ) のディザスター リカバリー DC には生き残ったレプリカが 1 つだけ残ります。これは、ほとんどのレプリカが存続するRaftアルゴリズムの要件を満たすことができません。その結果、クラスターが一時的に使用できなくなる可能性があります。メンテナンス スタッフは、生き残った 1 つのレプリカからクラスターを回復する必要があり、複製されていない少量のホット データが失われます。しかし、このケースはまれなケースです。
    -   ISP専用ネットワークを利用するため、このアーキテクチャのネットワークインフラはコストが高くなります。
    -   2 つの都市の 3 つの DC に 5 つのレプリカが構成されているため、データの冗長性が増し、ストレージ コストが高くなります。

### 導入の詳細 {#deployment-details}

2 つの都市 (シアトルとサンフランシスコ) 展開計画の 3 つの DC の構成は、次のように示されています。

![3-DC-2-city](/media/three-data-centers-in-two-cities-deployment-02.png)

-   上の図から、シアトルには IDC1 と IDC2 の 2 つの DC があることがわかります。 IDC1 には、RAC1、RAC2、および RAC3 の 3 つのラック セットがあります。 IDC2 には、RAC4 と RAC5 の 2 つのラックがあります。サンフランシスコの IDC3 DC には RAC6 ラックがあります。
-   上記の RAC1 ラックから、TiDB サービスと PD サービスが同じサーバーにデプロイされます。 2 つの TiKV サーバーのそれぞれに、2 つの TiKV インスタンス (tikv-server) がデプロイされます。これは、RAC2、RAC4、RAC5、および RAC6 に似ています。
-   TiDBサーバー、制御マシン、および監視サーバーは RAC3 上にあります。 TiDBサーバーは、定期的なメンテナンスとバックアップのためにデプロイされます。 Prometheus、Grafana、および復元ツールは、制御マシンと監視マシンにデプロイされます。
-   Drainerをデプロイするために、別のバックアップサーバーを追加できます。 Drainerは、増分バックアップを実現するために、ファイルを出力することによって binlog データを指定された場所に保存します。

## コンフィグレーション {#configuration}

### 例 {#example}

たとえば、次の`tiup topology.yaml`つの yaml ファイルを参照してください。

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/data/tidb_cluster/tidb-deploy"
  data_dir: "/data/tidb_cluster/tidb-data"

server_configs:
  tikv:
    server.grpc-compression-type: gzip
  pd:
    replication.location-labels:  ["dc","zone","rack","host"]

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
      server.labels: { dc: "1", zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { dc: "1", zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { dc: "2", zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { dc: "2", zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { dc: "3", zone: "5", rack: "5", host: "34" }
      raftstore.raft-min-election-timeout-ticks: 1000
      raftstore.raft-max-election-timeout-ticks: 1200

monitoring_servers:
  - host: 10.63.10.60

grafana_servers:
  - host: 10.63.10.60

alertmanager_servers:
  - host: 10.63.10.60
```

### ラベルデザイン {#labels-design}

2 つの都市に 3 つの DC を展開する場合、ラベルの設計では、可用性と災害復旧を考慮する必要があります。デプロイメントの物理構造に基づいて、4 つのレベル ( `dc` 、 `zone` 、 `rack` 、 `host` ) を定義することをお勧めします。

![Label logical definition](/media/three-data-centers-in-two-cities-deployment-03.png)

PD 構成で、TiKV ラベルのレベル情報を追加します。

```yaml
server_configs:
  pd:
    replication.location-labels:  ["dc","zone","rack","host"]
```

`tikv_servers`の構成は、TiKV の実際の物理的な展開場所のラベル情報に基づいているため、PD はグローバルな管理とスケジューリングを実行しやすくなります。

```yaml
tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { dc: "1", zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { dc: "1", zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { dc: "2", zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { dc: "2", zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { dc: "3", zone: "5", rack: "5", host: "34" }
```

### パラメータ構成の最適化 {#optimize-parameter-configuration}

2 つの都市に 3 つの DC を展開する場合、パフォーマンスを最適化するには、通常のパラメーターを構成するだけでなく、コンポーネントのパラメーターも調整する必要があります。

-   TiKV で gRPC メッセージ圧縮を有効にします。クラスターのデータはネットワークで送信されるため、gRPC メッセージ圧縮を有効にしてネットワーク トラフィックを下げることができます。

    ```yaml
    server.grpc-compression-type: gzip
    ```

-   別の都市 (サンフランシスコ) の TiKV ノードのネットワーク構成を最適化します。サンフランシスコの IDC3 (単独) の次の TiKV パラメータを変更し、この TiKV ノードのレプリカがRaft選択に参加しないようにしてください。

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 1000
    raftstore.raft-max-election-timeout-ticks: 1200
    ```

-   スケジューリングを構成します。クラスターが有効になったら、 `tiup ctl:<cluster-version> pd`ツールを使用してスケジューリング ポリシーを変更します。 TiKV Raftレプリカの数を変更します。この数を計画どおりに構成します。この例では、レプリカの数は 5 です。

    ```yaml
    config set max-replicas 5
    ```

-   Raftリーダーを IDC3 にスケジューリングすることを禁止します。 Raftリーダーを別の都市 (IDC3) にスケジュールすると、シアトルの IDC1/IDC2 とサンフランシスコの IDC3 の間で不要なネットワーク オーバーヘッドが発生します。ネットワーク帯域幅とレイテンシーも、TiDB クラスターのパフォーマンスに影響します。

    ```yaml
    config set label-property reject-leader dc 3
    ```

    > **ノート：**
    >
    > TiDB 5.2 以降、デフォルトでは`label-property`構成はサポートされていません。レプリカ ポリシーを設定するには、 [配置ルール](/configure-placement-rules.md)を使用します。

-   PD の優先度を設定します。 PD リーダーが別の都市 (IDC3) にいる状況を回避するには、ローカル PD の優先度を上げ (シアトル)、別の都市 (サンフランシスコ) にある PD の優先度を下げることができます。数値が大きいほど優先度が高くなります。

    ```yaml
    member leader_priority PD-10 5
    member leader_priority PD-11 5
    member leader_priority PD-12 5
    member leader_priority PD-13 5
    member leader_priority PD-14 1
    ```
