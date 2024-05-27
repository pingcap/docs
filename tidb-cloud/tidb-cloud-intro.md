---
title: TiDB Cloud Introduction
summary: TiDB Cloudとそのアーキテクチャについて学びます。
category: intro
---

# TiDB Cloudの紹介 {#tidb-cloud-introduction}

[TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 、オープンソースのハイブリッド トランザクションおよび分析処理 (HTAP) データベースである[ティビ](https://docs.pingcap.com/tidb/stable/overview)クラウドに提供する、フルマネージドの Database-as-a-Service (DBaaS) です。TiDB TiDB Cloud は、データベースの複雑な部分ではなく、アプリケーションに集中できるように、データベースを簡単に導入および管理する方法を提供します。TiDB TiDB Cloudクラスターを作成して、Google Cloud と Amazon Web Services (AWS) でミッション クリティカルなアプリケーションを迅速に構築できます。

![TiDB Cloud Overview](/media/tidb-cloud/tidb-cloud-overview.png)

## TiDB Cloud理由 {#why-tidb-cloud}

TiDB Cloudと、ほとんどまたはまったくトレーニングを受けなくても、インフラストラクチャ管理やクラスターの展開などの複雑なタスクを簡単に処理できます。

-   開発者とデータベース管理者 (DBA) は、大量のオンライン トラフィックを簡単に処理し、複数のデータセットにわたる大量のデータを迅速に分析できます。

-   あらゆる規模の企業は、前払いなしでTiDB Cloud を簡単に導入および管理し、ビジネスの成長に適応できます。

TiDB Cloudの詳細については、次のビデオをご覧ください。

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="TiDB Cloud を選ぶ理由" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

TiDB Cloudを使用すると、次の主な機能を利用できます。

-   **高速かつカスタマイズされたスケーリング**

    ACIDトランザクションを維持しながら、重要なワークロードに対して数百のノードに柔軟かつ透過的に拡張できます。シャーディングを気にする必要はありません。また、ビジネス ニーズに応じてパフォーマンス ノードとstorageノードを個別に拡張できます。

-   **MySQL 互換性**

    TiDB の MySQL 互換性により、アプリケーションの生産性が向上し、市場投入までの時間が短縮されます。コードを書き直すことなく、既存の MySQL インスタンスからデータを簡単に移行できます。

-   **高可用性と信頼性**

    設計上、自然に高い可用性を実現します。複数のアベイラビリティ ゾーンにわたるデータ レプリケーション、毎日のバックアップ、自動フェイルオーバーにより、ハードウェア障害、ネットワーク パーティション、データ センターの損失に関係なく、ビジネスの継続性が確保されます。

-   **リアルタイム分析**

    組み込みの分析エンジンを使用して、リアルタイムの分析クエリ結果を取得します。TiDB TiDB Cloud は、ミッションクリティカルなアプリケーションを妨げることなく、現在のデータに対して一貫した分析クエリを実行します。

-   **エンタープライズグレードのSecurity**

    専用ネットワークとマシンでデータをセキュリティ。転送中と保存中の両方の暗号化をサポートします。TiDB TiDB Cloud は、SOC 2 タイプ 2、ISO 27001:2013、ISO 27701 の認定を受けており、GDPR に完全に準拠しています。

-   **フルマネージドサービス**

    使いやすい Web ベースの管理プラットフォームを使用して、数回のクリックで TiDB クラスターをデプロイ、拡張、監視、管理できます。

-   **マルチクラウドサポート**

    クラウド ベンダーに縛られることなく柔軟性を維持できます。TiDB TiDB Cloudは現在、AWS と Google Cloud で利用できます。

-   **シンプルな料金プラン**

    使用した分だけお支払いください。料金が透明で前払いなので、隠れた料金はありません。

-   **世界クラスのサポート**

    サポート ポータル、<a href="mailto:tidbcloud-support@pingcap.com">電子メール</a>、チャット、またはビデオ会議を通じて世界クラスのサポートを受けることができます。

## 展開オプション {#deployment-options}

TiDB Cloud、次の 2 つのデプロイメント オプションが提供されます。

-   [TiDB サーバーレス](https://www.pingcap.com/tidb-serverless)

    TiDB Serverless は、完全に管理されたマルチテナントの TiDB サービスです。瞬時に自動スケーリングされる MySQL 互換データベースを提供し、十分な無料利用枠と、無料制限を超えた場合の使用量に基づく課金を提供します。

-   [TiDB専用](https://www.pingcap.com/tidb-dedicated)

    TiDB Dedicated は、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番向けです。

TiDB Serverless と TiDB Dedicated の機能比較については、 [TiDB: 高度なオープンソースの分散SQLデータベース](https://www.pingcap.com/get-started-tidb)参照してください。

## アーキテクチャ {#architecture}

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

-   TiDB VPC (仮想プライベートクラウド)

    各TiDB Cloudクラスターでは、 TiDB Operatorノードとログ ノードを含むすべての TiDB ノードと補助ノードが独立した VPC にデプロイされます。

-   TiDB Cloudセントラル サービス

    課金、アラート、メタstorage、ダッシュボード UI などのセントラル サービスは独立してデプロイされます。ダッシュボード UI にアクセスして、インターネット経由で TiDB クラスターを操作できます。

-   あなたのVPC

    プライベートエンドポイント接続または VPC ピアリング接続を介して TiDB クラスターに接続できます。詳細については、 [プライベートエンドポイント接続を設定する](/tidb-cloud/set-up-private-endpoint-connections.md)または[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。
