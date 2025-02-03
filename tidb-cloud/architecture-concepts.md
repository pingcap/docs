---
title: Architecture
summary: TiDB Cloudのアーキテクチャの概念について学習します。
---

# アーキテクチャ {#architecture}

TiDB Cloud は、オープンソースの HTAP (ハイブリッド トランザクションおよび分析処理) データベースである[ティビ](https://docs.pingcap.com/tidb/stable/overview)の柔軟性とパワーを Google Cloud と AWS にもたらす、フルマネージドの Database-as-a-Service (DBaaS) です。

TiDB は MySQL と互換性があり、既存のアプリケーションへの移行や操作が容易なだけでなく、小規模なワークロードから大規模で高性能なクラスターまで、あらゆるワークロードを処理できるシームレスなスケーラビリティも提供します。トランザクション (OLTP) と分析 (OLAP) の両方のワークロードを 1 つのシステムでサポートし、操作を簡素化してリアルタイムの洞察を可能にします。

TiDB Cloud には、自動スケーリングとコスト効率に優れたワークロード向けの**TiDB Cloud** **Serverless**と、専用リソースと高度な機能を備えたエンタープライズ グレードのアプリケーション向けの**TiDB Cloud Dedicated という**2 つのデプロイメント オプションがあります。TiDB TiDB Cloudと、データベースのスケーリング、複雑な管理タスクの処理が容易になり、信頼性が高くパフォーマンスの高いアプリケーションの開発に集中できます。

## TiDB Cloudサーバーレス {#tidb-cloud-serverless}

TiDB Cloud Serverless は、従来の TiDB と同様の HTAP 機能を提供する完全マネージド型のサーバーレス ソリューションです。また、自動スケーリング機能も備えているため、容量計画や管理の複雑さに関連するユーザーの負担を軽減できます。基本的な使用には無料レベルが用意されており、無料制限を超えた使用には消費量に基づいて課金されます。TiDB TiDB Cloud Serverless は、さまざまな運用要件に対応するために 2 種類の高可用性を提供します。

デフォルトでは、ゾーン高可用性オプションを利用するクラスターでは、すべてのコンポーネントが同じ可用性ゾーン内に配置されるため、ネットワークのレイテンシーが短くなります。

![TiDB Cloud Serverless zonal high availability](/media/tidb-cloud/serverless-zonal-high-avaliability-aws.png)

最大限のインフラストラクチャの分離と冗長性を必要とするアプリケーションの場合、リージョン高可用性オプションにより、複数の可用性ゾーンにノードが分散されます。

![TiDB Cloud Serverless regional high availability](/media/tidb-cloud/serverless-regional-high-avaliability-aws.png)

## TiDB Cloud専用 {#tidb-cloud-dedicated}

TiDB Cloud Dedicated は、ミッションクリティカルなビジネス向けに設計されており、複数の可用性ゾーンにわたる高可用性、水平スケーリング、完全な HTAP 機能を提供します。

VPC、VM、マネージド Kubernetes サービス、クラウドstorageなどの分離されたクラウド リソース上に構築されており、主要なクラウド プロバイダーのインフラストラクチャを活用します。TiDB TiDB Cloud Dedicated クラスターは、完全な TiDB 機能セットをサポートし、迅速なスケーリング、信頼性の高いバックアップ、特定の VPC 内での展開、地理的レベルの災害復旧を可能にします。

![TiDB Cloud Dedicated Architecture](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloudコンソール {#tidb-cloud-console}

[TiDB Cloudコンソール](https://tidbcloud.com/)は、 TiDB Cloud Serverless とTiDB Cloud Dedicated の両方に対応する Web ベースの管理インターフェイスです。クラスターの管理、データのインポートまたは移行、パフォーマンス メトリックの監視、バックアップの構成、セキュリティ制御のセットアップ、他のクラウド サービスとの統合を行うためのツールをすべて、単一の使いやすいプラットフォームから提供します。

## TiDB CloudCLI (ベータ版) {#tidb-cloud-cli-beta}

TiDB Cloud CLI `ticloud`使用すると、簡単なコマンドでターミナルから直接TiDB Cloud Serverless とTiDB Cloud Dedicated を管理できます。次のようなタスクを実行できます。

-   クラスターの作成、削除、および一覧表示。
-   クラスターにデータをインポートしています。
-   クラスターからデータをエクスポートしています。

詳細については[TiDB CloudCLI リファレンス](/tidb-cloud/cli-reference.md)参照してください。

## TiDB CloudAPI (ベータ版) {#tidb-cloud-api-beta}

TiDB Cloud API は、 TiDB Cloud Serverless とTiDB Cloud Dedicated 全体のリソースを管理するためのプログラムによるアクセスを提供する REST ベースのインターフェースです。これにより、プロジェクト、クラスター、バックアップ、復元、データのインポート、課金、その他のリソースの管理などのタスクを[TiDB Cloudデータ サービス](/tidb-cloud/data-service-overview.md)で自動化して効率的に処理できるようになります。

詳細については[TiDB CloudAPI の概要](/tidb-cloud/api-overview.md)参照してください。

## ノード {#nodes}

TiDB Cloudでは、各クラスターは TiDB、TiKV、およびTiFlashノードで構成されます。

-   TiDB Cloud Dedicated クラスターでは、パフォーマンス要件に応じて、専用の TiDB、TiKV、およびTiFlashノードの数とサイズを完全に管理できます。詳細については、 [スケーラビリティ](/tidb-cloud/scalability-concepts.md)参照してください。
-   TiDB Cloud Serverless クラスターでは、TiDB、TiKV、 TiFlashノードの数とサイズが自動的に管理されます。これによりシームレスなスケーリングが保証され、ユーザーがノードの構成や管理タスクを処理する必要がなくなります。

### TiDBノード {#tidb-node}

A [TiDBノード](/tidb-computing.md) 、MySQL 互換エンドポイントを使用してアプリケーションに接続するステートレス SQLレイヤーです。SQL クエリの解析、最適化、分散実行プランの作成などのタスクを処理します。

複数の TiDB ノードを展開して水平方向に拡張し、より高いワークロードを管理できます。これらのノードは、TiProxy や HAProxy などのロード バランサーと連携して、シームレスなインターフェイスを提供します。TiDB ノード自体はデータを保存しません。行ベースのstorageの場合は TiKV ノードに、列ベースのstorageの場合はTiFlashノードにデータ要求を転送します。

### TiKVノード {#tikv-node}

[TiKVノード](/tikv-overview.md) 、TiDBアーキテクチャにおけるデータstorageのバックボーンであり、信頼性、スケーラビリティ、高可用性を実現する分散トランザクション キー値storageエンジンとして機能します。

**主な機能:**

-   **地域ベースのデータstorage**

    -   データは[地域](https://docs.pingcap.com/tidb/dev/glossary#regionpeerraft-group)に分割され、それぞれが特定のキー範囲 (左閉じ、右開きの間隔: `StartKey` ～ `EndKey` ) をカバーします。
    -   効率的なデータ分散を確保するために、各 TiKV ノード内に複数のリージョンが共存します。

-   **トランザクションサポート**

    -   TiKV ノードは、キー値レベルでネイティブの分散トランザクション サポートを提供し、デフォルトの分離レベルとしてスナップショット分離を保証します。
    -   TiDB ノードは、SQL 実行プランを TiKV ノード API への呼び出しに変換し、シームレスな SQL レベルのトランザクション サポートを可能にします。

-   **高可用性**

    -   TiKV ノード内のすべてのデータは、耐久性を確保するために複製されます (デフォルト: 3 つのレプリカ)。
    -   TiKV はネイティブの高可用性を保証し、自動フェイルオーバーをサポートして、ノード障害から保護します。

-   **スケーラビリティと信頼性**

    -   TiKV ノードは、分散一貫性とフォールト トレランスを維持しながら、拡大するデータセットを処理するように設計されています。

### TiFlashノード {#tiflash-node}

[TiFlashノード](/tiflash/tiflash-overview.md)は、TiDBアーキテクチャ内の特殊なタイプのstorageノードです。通常の TiKV ノードとは異なり、 TiFlash は列型storageモデルによる分析アクセラレーション用に設計されています。

**主な機能:**

-   **列型storage**

    TiFlashノードはデータを列形式で保存するため、分析クエリに最適化され、読み取り集中型のワークロードのパフォーマンスが大幅に向上します。

-   **ベクトル検索インデックスのサポート**

    ベクター検索インデックス機能は、テーブルにTiFlashレプリカを使用するため、高度な検索機能が有効になり、複雑な分析シナリオでの効率が向上します。
