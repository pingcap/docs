---
title: Architecture
summary: TiDB Cloudのアーキテクチャ概念について学びましょう。
---

# アーキテクチャ {#architecture}

<CustomContent language="en,zh">

TiDB Cloudは、フルマネージド型のデータベース・アズ・ア・サービス（DBaaS）であり、オープンソースのHTAP（ハイブリッド・トランザクション・アンド・アナリティカル・プロセッシング）データベースである[TiDB](https://docs.pingcap.com/tidb/stable/overview)の柔軟性とパワーを、Amazon Web Services（AWS）、Google Cloud、Microsoft Azure、およびAlibaba Cloudに提供します。

</CustomContent>

<CustomContent language="ja">

TiDB Cloudは、フルマネージド型のデータベース・アズ・ア・サービス（DBaaS）であり、オープンソースのHTAP（ハイブリッド・トランザクション・アンド・アナリティカル・プロセッシング）データベースである[TiDB](https://docs.pingcap.com/tidb/stable/overview)の柔軟性とパワーを、Amazon Web Services（AWS）、Google Cloud、およびMicrosoft Azureに提供します。

</CustomContent>

TiDBはMySQLと互換性があるため、既存のアプリケーションとの移行や連携が容易です。また、小規模なワークロードから大規模な高性能システムまで、あらゆる規模のワークロードに対応できるシームレスな拡張性を提供します。トランザクション処理（OLTP）と分析処理（OLAP）の両方のワークロードを1つのシステムでサポートすることで、運用を簡素化し、リアルタイムのインサイトを実現します。

TiDB Cloudを使えば、データベースのスケーリング、複雑な管理タスクの処理が容易になり、信頼性が高く高性能なアプリケーションの開発に集中できます。

<CustomContent language="en,zh">

-   AWS向けには、 TiDB Cloudは、自動スケーリングとコスト効率の高いワークロード向けの**TiDB Cloud Starter** 、プロビジョニングされた容量を備えた本番環境対応ワークロード向けの**TiDB Cloud Essential** 、専用リソースと高度な機能を備えたエンタープライズグレードのアプリケーション向けの**TiDB Cloud Dedicated**。
-   Google CloudおよびAzure向けに、 TiDB Cloudは、専用リソースと高度な機能を備えたエンタープライズグレードのアプリケーション向けに、 **TiDB Cloud Dedicatedを**提供します。
-   Alibaba Cloud向けに、 TiDB Cloudは、自動スケーリングとコスト効率の高いワークロード向けの**TiDB Cloud Starter**と、プロビジョニングされた容量を備えた本番環境対応ワークロード向け**のTiDB Cloud Essential**を提供しています。

</CustomContent>

<CustomContent language="ja">

-   AWS向けには、 TiDB Cloudは、自動スケーリングとコスト効率の高いワークロード向けの**TiDB Cloud Starter** 、プロビジョニングされた容量を備えた本番環境対応ワークロード向けの**TiDB Cloud Essential** 、専用リソースと高度な機能を備えたエンタープライズグレードのアプリケーション向けの**TiDB Cloud Dedicated**。
-   TiDB Cloudは、Google CloudおよびAzure向けに、専用リソースと高度な機能を備えたエンタープライズグレードのアプリケーション向けサービス**「TiDB Cloud Dedicated」**を提供しています。

</CustomContent>

## TiDB Cloud Starter {#tidb-cloud-starter}

TiDB Cloud Starterは、フルマネージド型のマルチテナントTiDBサービスです。MySQL互換の、自動スケーリング機能を備えた即時利用可能なデータベースを提供します。

Starterプランは、 TiDB Cloudを初めて利用する方に最適です。開発者や小規模チーム向けに、以下の機能を提供します。

-   **無料**：このプランは完全に無料で、利用開始にクレジットカードは必要ありません。
-   **ストレージ**：初期容量として、行ベースのstorageが5 GiB、列ベースのstorageが5 GiB提供されます。
-   **要求単位**: データベース操作の 5,000 万[要求単位（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)が含まれます。

## TiDB Cloud Essential {#tidb-cloud-essential}

ワークロードが増加し、リアルタイムでの拡張性を必要とするアプリケーション向けに、 Essentialプランは以下の機能を備え、ビジネスの成長に合わせて柔軟かつ高性能なソリューションを提供します。

-   **機能強化**：Starterプランのすべての機能に加え、より大規模で複雑なワークロードを処理できる能力、および高度なセキュリティ機能が含まれています。
-   **自動スケーリング**：変化するワークロードの需要に効率的に対応するために、storageとコンピューティングリソースを自動的に調整します。
-   **高可用性**：組み込みの耐障害性と冗長性により、インフラストラクチャの障害発生時でも、アプリケーションの可用性と回復力が維持されます。
-   **予測可能な料金体系**：コンピューティングリソースのstorageとリクエストキャパシティユニット（RCU）に基づいて課金されるため、ニーズに合わせて拡張可能な透明性の高い使用量ベースの料金体系が提供され、予期せぬ追加料金なしで使用した分だけを支払うことができます。

TiDB Cloud Essentialは、さまざまな運用要件に対応するため、2種類の高可用性機能を提供します。

-   ゾーン高可用性：すべてのコンポーネントを同じ可用性ゾーン内に配置することで、ネットワークレイテンシーを低減します。
-   地域別高可用性：ノードを複数の可用性ゾーンに分散させることで、インフラストラクチャの最大限の分離性と冗長性を実現します。

詳細については、[TiDB Cloudにおける高可用性](/tidb-cloud/serverless-high-availability.md)参照してください。

## TiDB Cloud Dedicated {#tidb-cloud-dedicated}

TiDB Cloud Dedicatedは、ミッションクリティカルなビジネス向けに設計されており、複数のアベイラビリティゾーンにわたる高可用性、水平スケーリング、および完全なHTAP機能を提供します。

VPC、VM、マネージドKubernetesサービス、クラウドstorageなどの独立したクラウドリソース上に構築されたTiDB Cloud Dedicatedクラスターは、TiDBの全機能セットをサポートし、迅速なスケーリング、信頼性の高いバックアップ、特定のVPC内でのデプロイ、および地理的レベルのディザスタリカバリ。

![TiDB Cloud Dedicated Architecture](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloudコンソール {#tidb-cloud-console}

[TiDB Cloudコンソール](https://tidbcloud.com/)TiDB CloudリソースのWebベースの管理インターフェースです。単一の使いやすいプラットフォームから、 TiDB Cloudリソースの管理、データのインポートまたは移行、パフォーマンス指標の監視、バックアップの設定、セキュリティ制御の設定、および他のクラウドサービスとの統合を行うためのツールを提供します。

## TiDB Cloud CLI（ベータ版） {#tidb-cloud-cli-beta}

TiDB Cloud CLI `ticloud`と、簡単なコマンドでターミナルから直接TiDB Cloud StarterおよびEssentialインスタンスを管理できます。次のようなタスクを実行できます。

-   TiDB Cloud StarterおよびEssentialインスタンスの作成、削除、一覧表示。
-   TiDB Cloud StarterおよびEssentialインスタンスへのデータインポート。
-   TiDB Cloud StarterおよびEssentialインスタンスからデータをエクスポートします。

詳細については、 [TiDB Cloud CLI リファレンス](/tidb-cloud/cli-reference.md)を参照してください。

## TiDB CloudAPI（ベータ版） {#tidb-cloud-api-beta}

TiDB Cloud APIは、RESTベースのインターフェースであり、 TiDB Cloud StarterおよびTiDB Cloud Dedicated全体にわたるリソースをプログラムから管理するためのアクセスを提供します。これにより、 [TiDB Cloudデータサービス](/tidb-cloud/data-service-overview.md)。

詳細については、 [TiDB Cloud APIの概要](https://docs.pingcap.com/api/tidb-cloud-api-overview)参照してください。

## ノード {#nodes}

ノードはTiDBアーキテクチャの中核となるコンポーネントです。TiDBノード、TiKVノード、およびTiFlashノードは連携して、SQLクエリの処理、データの保存、および分析ワークロードの高速化を行います。

-   TiDB Cloud Dedicatedクラスターでは、パフォーマンス要件に応じて、専用の TiDB、TiKV、およびTiFlashノードの数とサイズを完全に管理できます。詳細については、[拡張性](/tidb-cloud/scalability-concepts.md)参照してください。
-   TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスでは、TiDB、TiKV、およびTiFlashノードの数とサイズは自動的に管理されます。これにより、シームレスなスケーリングが実現され、ユーザーがノードの設定や管理作業を行う必要がなくなります。

### TiDBノード {#tidb-node}

[TiDBノード](/tidb-computing.md)MySQL互換エンドポイントを使用してアプリケーションに接続するステートレスなSQLレイヤーです。SQLクエリの解析、最適化、分散実行プランの作成などのタスクを処理します。

TiDBノードを複数デプロイすることで、水平方向に拡張し、より高いワークロードに対応できます。これらのノードは、TiProxyやHAProxyなどのロードバランサーと連携して、シームレスなインターフェースを提供します。TiDBノード自体はデータを保存せず、データ要求を行ベースstorageの場合はTiKVノードに、列ベースstorageの場合はTiFlashノードに転送します。

### TiKVノード {#tikv-node}

[TiKVノード](/tikv-overview.md)、TiDBアーキテクチャにおけるデータstorageの基盤であり、信頼性、拡張性、高可用性を提供する分散型トランザクションキーバリューstorageエンジンとして機能します。

**主な特徴：**

-   **地域ベースのデータstorage**

    -   データは[地域](https://docs.pingcap.com/tidb/dev/glossary#regionpeerraft-group)ごとに分割され、それぞれが特定のキー範囲（左端が閉じ、右端が開いた区間： `StartKey`から`EndKey` ）をカバーします。
    -   効率的なデータ配信を確保するため、各TiKVノード内には複数のリージョンが共存している。

-   **トランザクションサポート**

    -   TiKVノードは、キーバリューレベルでネイティブな分散トランザクションをサポートし、スナップショット分離をデフォルトの分離レベルとして保証します。
    -   TiDBノードは、SQL実行プランをTiKVノードAPIへの呼び出しに変換することで、シームレスなSQLレベルのトランザクションサポートを実現します。

-   **高可用性**

    -   TiKVノード内のすべてのデータは、耐久性を確保するために複製されます（デフォルト：3つのレプリカ）。
    -   TiKVはネイティブな高可用性を保証し、自動フェイルオーバーをサポートすることで、ノード障害からシステムを保護します。

-   **拡張性と信頼性**

    -   TiKVノードは、分散の一貫性と耐障害性を維持しながら、拡大するデータセットを処理できるように設計されています。

### TiFlashノード {#tiflash-node}

[TiFlashノード](/tiflash/tiflash-overview.md)TiDBアーキテクチャ内の特殊なstorageノードです。通常のTiKVノードとは異なり、 TiFlashはカラム型storageモデルによる分析高速化のために設計されています。

**主な特徴：**

-   **柱状storage**

    TiFlashノードはデータを列形式で保存するため、分析クエリに最適化されており、読み取り負荷の高いワークロードのパフォーマンスを大幅に向上させます。

-   **ベクトル検索インデックスのサポート**

    ベクトル検索インデックス機能は、テーブルにTiFlashレプリカを使用することで、高度な検索機能を実現し、複雑な分析シナリオにおける効率性を向上させます。
