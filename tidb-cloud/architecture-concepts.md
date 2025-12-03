---
title: Architecture
summary: TiDB Cloudのアーキテクチャの概念について学習します。
---

# アーキテクチャ {#architecture}

<CustomContent language="en,zh">

TiDB Cloudは、オープンソースの HTAP (ハイブリッド トランザクションおよび分析処理) データベース[ティドブ](https://docs.pingcap.com/tidb/stable/overview)の柔軟性とパワーを Amazon Web Services (AWS)、Google Cloud、Microsoft Azure、Alibaba Cloud に提供する、完全に管理された Database-as-a-Service (DBaaS) です。

</CustomContent>

<CustomContent language="ja">

TiDB Cloudは、オープンソースの HTAP (ハイブリッド トランザクションおよび分析処理) データベース[ティドブ](https://docs.pingcap.com/tidb/stable/overview)の柔軟性とパワーを Amazon Web Services (AWS)、Google Cloud、Microsoft Azure に提供する、完全に管理された Database-as-a-Service (DBaaS) です。

</CustomContent>

TiDBはMySQLと互換性があり、既存のアプリケーションへの移行と連携が容易です。また、小規模なワークロードから大規模な高性能クラスタまで、あらゆるワークロードに対応できるシームレスなスケーラビリティを提供します。トランザクション（OLTP）と分析（OLAP）の両方のワークロードを1つのシステムでサポートすることで、運用を簡素化し、リアルタイムのインサイト獲得を可能にします。

TiDB Cloudすると、データベースの拡張、複雑な管理タスクの処理が容易になり、信頼性が高くパフォーマンスの高いアプリケーションの開発に集中できます。

<CustomContent language="en,zh">

-   AWS の場合、 TiDB Cloudは、自動スケーリングとコスト効率に優れたワークロード向けの**TiDB Cloud Starter** 、プロビジョニングされた容量を備えた本番環境対応のワークロード向けの**TiDB Cloud Essential** 、専用リソースと高度な機能を備えたエンタープライズ グレードのアプリケーション向けの**TiDB Cloud Dedicated を提供します**。
-   Google Cloud および Azure 向けに、 TiDB Cloud は専用リソースと高度な機能を備えたエンタープライズ グレードのアプリケーション向けに**TiDB Cloud Dedicated を**提供します。
-   Alibaba Cloud の場合、 TiDB Cloud は、自動スケーリングとコスト効率に優れたワークロード向け**の TiDB Cloud Starter**と、プロビジョニングされた容量を備えた本番環境対応のワークロード向け**の TiDB Cloud Essential**を提供します。

</CustomContent>

<CustomContent language="ja">

-   AWS の場合、 TiDB Cloudは、自動スケーリングとコスト効率に優れたワークロード向けの**TiDB Cloud Starter** 、プロビジョニングされた容量を備えた本番環境対応のワークロード向けの**TiDB Cloud Essential** 、専用リソースと高度な機能を備えたエンタープライズ グレードのアプリケーション向けの**TiDB Cloud Dedicated を提供します**。
-   Google Cloud および Azure 向けに、 TiDB Cloud は専用リソースと高度な機能を備えたエンタープライズ グレードのアプリケーション向けに**TiDB Cloud Dedicated を**提供します。

</CustomContent>

## TiDB Cloudスターター {#tidb-cloud-starter}

TiDB Cloud Starterは、フルマネージドのマルチテナントTiDBサービスです。瞬時に自動スケーリング可能なMySQL互換データベースを提供します。

スタータークラスタープランは、 TiDB Cloudを初めてご利用になる方に最適です。開発者や小規模チームに以下の機能を提供します。

-   **無料**: このプランは完全に無料で、開始するのにクレジットカードは必要ありません。
-   **ストレージ**: 初期 5 GiB の行ベースのstorageと 5 GiB の列ベースのstorageを提供します。
-   **リクエスト単位**: データベース操作用に 5000 万[リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)が含まれます。

## TiDB Cloudエッセンシャル {#tidb-cloud-essential}

ワークロードが増加し、リアルタイムの拡張性を必要とするアプリケーションの場合、Essential クラスター プランは次の機能により、ビジネスの成長に対応できる柔軟性とパフォーマンスを提供します。

-   **拡張機能**: スターター プランのすべての機能に加えて、より大規模で複雑なワークロードを処理する能力と高度なセキュリティ機能が含まれます。
-   **自動スケーリング**: 変化するワークロードの需要に効率的に対応するために、storageとコンピューティング リソースを自動的に調整します。
-   **高可用性**: フォールト トレランスと冗長性が組み込まれているため、インフラストラクチャに障害が発生した場合でも、アプリケーションの可用性と回復力を維持できます。
-   **予測可能な価格設定**: コンピューティング リソースのstorageとリクエスト容量単位 (RCU) に基づいて課金され、ニーズに合わせて拡張できる透明性の高い使用量ベースの価格設定が提供されるため、予期せぬ出費なく、使用した分だけを支払うことになります。

TiDB Cloud Essential は、さまざまな運用要件に対応するために 2 種類の高可用性を提供します。

-   デフォルトでは、ゾーン高可用性オプションを利用するクラスターでは、すべてのコンポーネントが同じ可用性ゾーン内に配置されるため、ネットワークレイテンシーが短縮されます。
-   最大限のインフラストラクチャ分離と冗長性を必要とするアプリケーションの場合、リージョン高可用性オプションにより、複数の可用性ゾーンにノードが分散されます。

詳細については[TiDB Cloud StarterとEssentialの高可用性](/tidb-cloud/serverless-high-availability.md)参照してください。

## TiDB Cloud専用 {#tidb-cloud-dedicated}

TiDB Cloud Dedicated は、ミッションクリティカルなビジネス向けに設計されており、複数の可用性ゾーンにわたる高可用性、水平スケーリング、完全な HTAP 機能を提供します。

VPC、VM、マネージドKubernetesサービス、クラウドstorageなどの分離されたクラウドリソース上に構築され、主要クラウドプロバイダーのインフラストラクチャを活用します。TiDB TiDB Cloud Dedicatedクラスターは、TiDBの機能セット全体をサポートし、迅速なスケーリング、信頼性の高いバックアップ、特定のVPC内でのデプロイメント、地理的レベルの災害復旧を可能にします。

![TiDB Cloud Dedicated Architecture](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloudコンソール {#tidb-cloud-console}

[TiDB Cloudコンソール](https://tidbcloud.com/)は、 TiDB Cloudクラスタ用のWebベースの管理インターフェースです。クラスタの管理、データのインポートまたは移行、パフォーマンスメトリックの監視、バックアップの設定、セキュリティ制御の設定、他のクラウドサービスとの統合など、すべて単一の使いやすいプラットフォームから実行できるツールを提供します。

## TiDB CloudCLI (ベータ版) {#tidb-cloud-cli-beta}

TiDB Cloud CLI `ticloud`を使用すると、ターミナルから簡単なコマンドでTiDB Cloudクラスタを直接管理できます。次のようなタスクを実行できます。

-   クラスターの作成、削除、および一覧表示。
-   クラスターにデータをインポートしています。
-   クラスターからデータをエクスポートしています。

詳細については[TiDB Cloud CLI リファレンス](/tidb-cloud/cli-reference.md)参照してください。

## TiDB CloudAPI (ベータ版) {#tidb-cloud-api-beta}

TiDB Cloud APIは、 TiDB Cloud StarterとTiDB Cloud Dedicated全体のリソースを管理するためのプログラム的なアクセスを提供するRESTベースのインターフェースです。プロジェクト、クラスタ、バックアップ、リストア、データのインポート、課金、その他のリソース管理といったタスクを、 [TiDB Cloudデータサービス](/tidb-cloud/data-service-overview.md)内で自動化し、効率的に処理できます。

詳細については[TiDB CloudAPI の概要](/tidb-cloud/api-overview.md)参照してください。

## ノード {#nodes}

TiDB Cloudでは、各クラスターは TiDB、TiKV、およびTiFlashノードで構成されます。

-   TiDB Cloud Dedicated クラスターでは、パフォーマンス要件に応じて、専用の TiDB、TiKV、 TiFlashノードの数とサイズを完全に管理できます。詳細については、 [スケーラビリティ](/tidb-cloud/scalability-concepts.md)ご覧ください。
-   TiDB Cloud StarterまたはTiDB Cloud Essentialクラスターでは、TiDB、TiKV、 TiFlashノードの数とサイズが自動的に管理されます。これによりシームレスなスケーリングが保証され、ユーザーがノードの設定や管理を行う必要がなくなります。

### TiDBノード {#tidb-node}

[TiDBノード](/tidb-computing.md)は、MySQL互換エンドポイントを使用してアプリケーションに接続するステートレスSQLレイヤーです。SQLクエリの解析、最適化、分散実行プランの作成などのタスクを処理します。

複数のTiDBノードを展開することで、水平方向にスケーリングし、より高いワークロードを管理できます。これらのノードは、TiProxyやHAProxyなどのロードバランサーと連携して、シームレスなインターフェースを提供します。TiDBノード自体はデータを保存せず、行ベースstorageの場合はTiKVノード、列ベースstorageの場合はTiFlashノードにデータ要求を転送します。

### TiKVノード {#tikv-node}

[TiKVノード](/tikv-overview.md)は、TiDBアーキテクチャにおけるデータstorageのバックボーンであり、信頼性、スケーラビリティ、高可用性を実現する分散トランザクション キー値storageエンジンとして機能します。

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

[TiFlashノード](/tiflash/tiflash-overview.md)は、TiDBアーキテクチャにおける特殊なタイプのstorageノードです。通常のTiKVノードとは異なり、 TiFlashは列指向storageモデルによる分析アクセラレーションを目的として設計されています。

**主な機能:**

-   **列型storage**

    TiFlashノードはデータを列形式で保存するため、分析クエリに最適化され、読み取り集中型のワークロードのパフォーマンスが大幅に向上します。

-   **ベクター検索インデックスのサポート**

    ベクター検索インデックス機能は、テーブルにTiFlashレプリカを使用するため、高度な検索機能が有効になり、複雑な分析シナリオでの効率が向上します。
