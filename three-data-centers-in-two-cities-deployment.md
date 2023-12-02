---
title: Three Availability Zones in Two Regions Deployment
summary: Learn the deployment solution to three availability zones in two regions.
---

# 2 つのリージョンに 3 つのアベイラビリティーゾーンを展開 {#three-availability-zones-in-two-regions-deployment}

このドキュメントでは、2 つのリージョン展開における 3 つのアベイラビリティ ゾーン (AZ) のアーキテクチャと構成を紹介します。

このドキュメントの「リージョン」という用語は地理的エリアを指しますが、大文字の「リージョン」は TiKV のデータstorageの基本単位を指します。 「AZ」はリージョン内の孤立した場所を指し、各リージョンには複数の AZ があります。このドキュメントで説明されているソリューションは、複数のデータ センターが 1 つの都市にあるシナリオにも当てはまります。

## 概要 {#overview}

2 つのリージョンにある 3 つの AZ のアーキテクチャは、本番データ AZ、同じリージョンにディザスタ リカバリ AZ、および別のリージョンにディザスタ リカバリ AZ を提供する、可用性が高く、災害に強い展開ソリューションです。このモードでは、2 つのリージョンの 3 つの AZ が相互接続されます。 1 つの AZ に障害が発生したり災害が発生したりしても、他の AZ は引き続き正常に動作し、主要なアプリケーションまたはすべてのアプリケーションを引き継ぐことができます。 1 つのリージョンでのマルチ AZ 展開と比較して、このソリューションにはリージョン間の高可用性という利点があり、リージョン レベルの自然災害にも耐えることができます。

分散データベース TiDB は、 Raftアルゴリズムを使用して 2 リージョン内 3 AZアーキテクチャをネイティブにサポートし、データベース クラスター内のデータの一貫性と高可用性を保証します。同じリージョン内の AZ 間のネットワークレイテンシーは比較的低いため、アプリケーション トラフィックを同じリージョン内の 2 つの AZ にディスパッチでき、TiKVリージョンリーダーと PD リーダーの分散を制御することでこれら 2 つの AZ でトラフィック負荷を共有できます。 。

## 導入アーキテクチャ {#deployment-architecture}

このセクションでは、シアトルとサンフランシスコを例に、TiDB の分散データベースの 2 つのリージョンに 3 つの AZ を配置するモードについて説明します。

この例では、2 つの AZ (AZ1 および AZ2) がシアトルにあり、もう 1 つの AZ (AZ3) がサンフランシスコにあります。 AZ1 と AZ2 の間のネットワークレイテンシーは3 ミリ秒未満です。シアトルの AZ3 と AZ1/AZ2 間のネットワークレイテンシーは約 20 ミリ秒です (ISP 専用ネットワークを使用)。

クラスター展開のアーキテクチャは次のとおりです。

-   TiDB クラスターは、シアトルの AZ1、シアトルの AZ2、サンフランシスコの AZ3 の 2 つのリージョンの 3 つの AZ にデプロイされています。
-   クラスターには 5 つのレプリカがあり、AZ1 に 2 つ、AZ2 に 2 つ、AZ3 に 1 つあります。 TiKVコンポーネントの場合、各ラックにはラベルが付いています。これは、各ラックにレプリカがあることを意味します。
-   Raftプロトコルは、ユーザーにとって透過的なデータの一貫性と高可用性を確保するために採用されています。

![3-AZ-in-2-region architecture](/media/three-data-centers-in-two-cities-deployment-01.png)

このアーキテクチャは可用性が高くなります。リージョンリーダーの分布は、同じリージョン (シアトル) 内の 2 つの AZ (AZ1 および AZ2) に制限されます。リージョンリーダーの分布が制限されない 3 AZ ソリューションと比較して、このアーキテクチャには次のような利点と欠点があります。

-   **利点**

    -   リージョンリーダーは同じリージョンの AZ にあり、レイテンシーが低いため、書き込みが高速になります。
    -   2 つの AZ は同時にサービスを提供できるため、リソース使用率が高くなります。
    -   1 つの AZ に障害が発生した場合でも、サービスは引き続き利用可能であり、データの安全性が確保されます。

-   **短所**

    -   データの整合性はRaftアルゴリズムによって実現されるため、同じリージョン内の 2 つの AZ に同時に障害が発生した場合、別のリージョン (サンフランシスコ) のディザスター リカバリー AZ には 1 つのレプリカのみが残ります。これでは、ほとんどのレプリカが存続するというRaftアルゴリズムの要件を満たすことができません。その結果、クラスターが一時的に使用できなくなる可能性があります。メンテナンス スタッフは、残っている 1 つのレプリカからクラスターを回復する必要がありますが、レプリケートされていない少量のホット データが失われます。しかし、このケースはまれな出来事です。
    -   このアーキテクチャのネットワーク インフラストラクチャは、ISP の専用ネットワークを使用するため、コストが高くなります。
    -   2 つのリージョンの 3 つの AZ に 5 つのレプリカが構成されているため、データの冗長性が向上し、storageコストが増加します。

### 導入の詳細 {#deployment-details}

2 つのリージョン (シアトルとサンフランシスコ) の展開計画における 3 つの AZ の構成を以下に示します。

![3-AZ-2-region](/media/three-data-centers-in-two-cities-deployment-02.png)

上の図から、シアトルには AZ1 と AZ2 の 2 つの AZ があることがわかります。 AZ1 には、rac1、rac2、rac3 の 3 セットのラックがあります。 AZ2 には rac4 と rac5 の 2 つのラックがあります。サンフランシスコの AZ3 には rac6 ラックが搭載されています。

AZ1 の rac1 では、1 つのサーバーがTiDB および PD サービスを使用してデプロイされ、他の 2 つのサーバーが TiKV サービスを使用してデプロイされます。各 TiKVサーバーは2 つの TiKV インスタンス (tikv-server) でデプロイされます。これは、rac2、rac4、rac5、および rac6 と同様です。

TiDBサーバー、制御マシン、および監視サーバーはrac3 上にあります。 TiDBサーバーは、定期的なメンテナンスとバックアップのために導入されます。 Prometheus、Grafana、および復元ツールは、制御マシンと監視マシンにデプロイされます。

別のバックアップサーバーを追加して、 Drainerを展開できます。 Drainer は、増分バックアップを実現するために、ファイルを出力することによってbinlogデータを指定された場所に保存します。

## コンフィグレーション {#configuration}

### 例 {#example}

例として、次の`tiup topology.yaml` yaml ファイルを参照してください。

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

2 つのリージョンに 3 つの AZ を展開する場合、ラベルの設計では可用性と災害復旧を考慮する必要があります。デプロイメントの物理構造に基づいて 4 つのレベル ( `az` 、 `replication zone` 、 `rack` 、および`host` ) を定義することをお勧めします。

![Label logical definition](/media/three-data-centers-in-two-cities-deployment-03.png)

PD 構成で、TiKV ラベルのレベル情報を追加します。

```yaml
server_configs:
  pd:
    replication.location-labels: ["az","replication zone","rack","host"]
```

`tikv_servers`の構成は、TiKV の実際の物理展開場所のラベル情報に基づいており、PD によるグローバルな管理とスケジューリングの実行が容易になります。

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

### パラメータ設定の最適化 {#optimize-parameter-configuration}

2 つのリージョンに 3 つの AZ を展開する場合、パフォーマンスを最適化するには、通常のパラメーターを構成するだけでなく、コンポーネントパラメーターも調整する必要があります。

-   TiKV で gRPC メッセージ圧縮を有効にします。クラスターのデータはネットワーク内で送信されるため、gRPC メッセージ圧縮を有効にしてネットワーク トラフィックを軽減できます。

    ```yaml
    server.grpc-compression-type: gzip
    ```

-   別のリージョン (サンフランシスコ) の TiKV ノードのネットワーク構成を最適化します。サンフランシスコの AZ3 の次の TiKV パラメーターを変更し、この TiKV ノードのレプリカがRaft選挙に参加しないようにします。

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 1000
    raftstore.raft-max-election-timeout-ticks: 1200
    ```

-   スケジュールを設定します。クラスターが有効になったら、 `tiup ctl:v<CLUSTER_VERSION> pd`ツールを使用してスケジューリング ポリシーを変更します。 TiKV Raftレプリカの数を変更します。この番号を計画どおりに構成します。この例では、レプリカの数は 5 です。

    ```bash
    config set max-replicas 5
    ```

-   Raftリーダーを AZ3 にスケジュールすることを禁止します。 Raftリーダーを別のリージョン (AZ3) にスケジュールすると、シアトルの AZ1/AZ2 とサンフランシスコの AZ3 の間で不要なネットワーク オーバーヘッドが発生します。ネットワーク帯域幅とレイテンシーも、TiDB クラスターのパフォーマンスに影響します。

    ```bash
    config set label-property reject-leader dc 3
    ```

    > **注記：**
    >
    > TiDB v5.2 以降、 `label-property`構成はデフォルトではサポートされません。レプリカ ポリシーを設定するには、 [配置ルール](/configure-placement-rules.md)を使用します。

-   PDの優先度を設定します。 PD リーダーが別のリージョン (AZ3) にある状況を回避するには、ローカル PD (シアトル) の優先順位を上げ、別のリージョン (サンフランシスコ) の PD の優先順位を下げることができます。数値が大きいほど優先度が高くなります。

    ```bash
    member leader_priority PD-10 5
    member leader_priority PD-11 5
    member leader_priority PD-12 5
    member leader_priority PD-13 5
    member leader_priority PD-14 1
    ```
