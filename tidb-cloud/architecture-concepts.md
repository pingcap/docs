---
title: Architecture
summary: TiDB Cloudのアーキテクチャの概念について学習します。
---

# アーキテクチャ {#architecture}

TiDB Cloud は、オープンソースの HTAP (ハイブリッド トランザクションおよび分析処理) データベース[TiDB](https://docs.pingcap.com/tidb/stable/overview)の柔軟性とパワーを AWS、Azure、Google Cloud に提供する、完全に管理された Database-as-a-Service (DBaaS) です。

TiDBはMySQLと互換性があり、既存のアプリケーションへの移行と連携が容易です。また、小規模なワークロードから大規模な高性能クラスタまで、あらゆるワークロードに対応できるシームレスなスケーラビリティを提供します。トランザクション（OLTP）と分析（OLAP）の両方のワークロードを1つのシステムでサポートし、運用を簡素化し、リアルタイムの洞察を実現します。

TiDB Cloud には、自動スケーリングとコスト効率の高いワークロード向けの**TiDB Cloud** **Serverless**と、専用リソースと高度な機能を備えたエンタープライズグレードのアプリケーション向けの**TiDB Cloud Dedicated**という2つのデプロイメントオプションがあります。TiDB TiDB Cloudすると、データベースのスケーリング、複雑な管理タスクの処理が容易になり、信頼性が高く高性能なアプリケーションの開発に集中できます。

## TiDB Cloudサーバーレス {#tidb-cloud-serverless}

TiDB Cloud Serverlessは、従来のTiDBと同様のHTAP機能を提供するフルマネージドのサーバーレスソリューションです。オートスケーリング機能により、キャパシティプランニングや管理の複雑さに伴うユーザーの負担を軽減します。基本的な使用量は無料枠で提供され、無料枠を超えた使用量については使用量に応じて課金されます。TiDB TiDB Cloud Serverlessは、さまざまな運用要件に対応するために、2種類の高可用性オプションを提供しています。

デフォルトでは、ゾーン高可用性オプションを利用するクラスターではすべてのコンポーネントが同じ可用性ゾーン内に配置されるため、ネットワークレイテンシーが低減されます。

![TiDB Cloud Serverless zonal high availability](/media/tidb-cloud/serverless-zonal-high-avaliability-aws.png)

最大限のインフラストラクチャ分離と冗長性を必要とするアプリケーションの場合、リージョン高可用性オプションにより、複数の可用性ゾーンにノードが分散されます。

![TiDB Cloud Serverless regional high availability](/media/tidb-cloud/serverless-regional-high-avaliability-aws.png)

## TiDB Cloud専用 {#tidb-cloud-dedicated}

TiDB Cloud Dedicated は、ミッションクリティカルなビジネス向けに設計されており、複数の可用性ゾーンにわたる高可用性、水平スケーリング、完全な HTAP 機能を提供します。

VPC、VM、マネージドKubernetesサービス、クラウドstorageなどの分離されたクラウドリソース上に構築され、主要クラウドプロバイダーのインフラストラクチャを活用します。TiDB TiDB Cloud Dedicatedクラスターは、TiDBの完全な機能セットをサポートし、迅速なスケーリング、信頼性の高いバックアップ、特定のVPC内でのデプロイメント、地理的レベルの災害復旧を可能にします。

![TiDB Cloud Dedicated Architecture](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloudコンソール {#tidb-cloud-console}

[TiDB Cloudコンソール](https://tidbcloud.com/) 、 TiDB Cloud ServerlessとTiDB Cloud Dedicatedの両方に対応するWebベースの管理インターフェースです。クラスターの管理、データのインポートまたは移行、パフォーマンス指標の監視、バックアップの設定、セキュリティ制御の設定、他のクラウドサービスとの統合など、すべて単一の使いやすいプラットフォームから実行できるツールを提供します。

## TiDB CloudCLI (ベータ版) {#tidb-cloud-cli-beta}

TiDB Cloud CLI `ticloud` ）を使用すると、簡単なコマンドでターミナルから直接TiDB Cloud ServerlessとTiDB Cloud Dedicatedを管理できます。以下のようなタスクを実行できます。

-   クラスターの作成、削除、および一覧表示。
-   クラスターにデータをインポートしています。
-   クラスターからデータをエクスポートしています。

詳細については[TiDB CloudCLI リファレンス](/tidb-cloud/cli-reference.md)参照してください。

## TiDB CloudAPI (ベータ版) {#tidb-cloud-api-beta}

TiDB Cloud APIは、 TiDB Cloud ServerlessとTiDB Cloud Dedicated全体のリソースを管理するためのプログラム的なアクセスを提供するRESTベースのインターフェースです。プロジェクト、クラスタ、バックアップ、リストア、データのインポート、課金、その他のリソース管理といったタスクを自動化し、効率的に処理できます[TiDB Cloudデータサービス](/tidb-cloud/data-service-overview.md)

詳細については[TiDB CloudAPI の概要](/tidb-cloud/api-overview.md)参照してください。

## ノード {#nodes}

TiDB Cloudでは、各クラスターは TiDB、TiKV、およびTiFlashノードで構成されます。

-   TiDB Cloud Dedicated クラスターでは、パフォーマンス要件に応じて、専用の TiDB、TiKV、 TiFlashノードの数とサイズを完全に管理できます。詳細については、 [スケーラビリティ](/tidb-cloud/scalability-concepts.md)ご覧ください。
-   TiDB Cloud Serverless クラスターでは、TiDB、TiKV、 TiFlashノードの数とサイズが自動的に管理されます。これによりシームレスなスケーリングが保証され、ユーザーがノードの設定や管理を行う必要がなくなります。

### TiDBノード {#tidb-node}

[TiDBノード](/tidb-computing.md) 、MySQL 互換エンドポイントを使用してアプリケーションに接続するステートレス SQLレイヤーです。SQL クエリの解析、最適化、分散実行プランの作成などのタスクを処理します。

複数のTiDBノードを展開することで、水平方向にスケーリングし、より高いワークロードを管理できます。これらのノードは、TiProxyやHAProxyなどのロードバランサーと連携して、シームレスなインターフェースを提供します。TiDBノード自体はデータを保存せず、行ベースstorageの場合はTiKVノード、列ベースstorageの場合はTiFlashノードにデータ要求を転送します。

### TiKVノード {#tikv-node}

[TiKVノード](/tikv-overview.md)は、TiDBアーキテクチャのデータstorageのバックボーンであり、信頼性、スケーラビリティ、高可用性を実現する分散トランザクション キー値storageエンジンとして機能します。

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

[TiFlashノード](/tiflash/tiflash-overview.md) 、TiDBアーキテクチャにおける特殊なタイプのstorageノードです。通常のTiKVノードとは異なり、 TiFlashは列指向storageモデルによる分析アクセラレーションを目的として設計されています。

**主な機能:**

-   **列型storage**

    TiFlashノードはデータを列形式で保存するため、分析クエリに最適化され、読み取り集中型のワークロードのパフォーマンスが大幅に向上します。

-   **ベクター検索インデックスのサポート**

    ベクター検索インデックス機能は、テーブルにTiFlashレプリカを使用するため、高度な検索機能が有効になり、複雑な分析シナリオでの効率が向上します。
