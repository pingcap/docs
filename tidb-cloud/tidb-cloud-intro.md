---
title: TiDB Cloud Introduction
summary: Learn about TiDB Cloud and its architecture.
category: intro
---

# TiDB Cloudの紹介 {#tidb-cloud-introduction}

[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)は、オープンソースのハイブリッド トランザクションおよび分析処理 (HTAP) データベースである[TiDB](https://docs.pingcap.com/tidb/stable/overview)クラウドに提供する、フルマネージドの Database-as-a-Service (DBaaS) です。 TiDB Cloudは、データベースの導入と管理を簡単に行う方法を提供し、データベースの複雑さではなく、アプリケーションに集中できるようにします。 TiDB Cloudクラスターを作成して、Google Cloud およびアマゾン ウェブ サービス (AWS) 上にミッションクリティカルなアプリケーションを迅速に構築できます。

![TiDB Cloud Overview](/media/tidb-cloud/tidb-cloud-overview.png)

## TiDB Cloudを選ぶ理由 {#why-tidb-cloud}

TiDB Cloud を使用すると、トレーニングをほとんど、またはまったく受けなくても、インフラストラクチャ管理やクラスター展開などの複雑なタスクを簡単に処理できます。

-   開発者とデータベース管理者 (DBA) は、大量のオンライン トラフィックを簡単に処理し、複数のデータセットにわたる大量のデータを迅速に分析できます。

-   あらゆる規模の企業は、前払いなしでTiDB Cloudを簡単に導入および管理して、ビジネスの成長に適応できます。

TiDB Cloudの詳細については、次のビデオをご覧ください。

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="Why TiDB Cloud?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />

TiDB Cloudを使用すると、次の主要な機能を利用できます。

-   **高速かつカスタマイズされたスケーリング**

    ACIDトランザクションを維持しながら、重要なワークロードに合わせて数百のノードに弾力的かつ透過的に拡張します。シャーディングを気にする必要はありません。また、ビジネス ニーズに応じてパフォーマンス ノードとstorageノードを個別に拡張できます。

-   **MySQL の互換性**

    TiDB の MySQL 互換性により、生産性が向上し、アプリケーションの市場投入までの時間が短縮されます。コードを書き直すことなく、既存の MySQL インスタンスからデータを簡単に移行できます。

-   **高可用性と信頼性**

    当然のことながら、設計により可用性が高くなります。複数のアベイラビリティーゾーンにわたるデータのレプリケーション、毎日のバックアップ、および自動フェイルオーバーにより、ハードウェア障害、ネットワークの分断、またはデータセンターの損失に関係なく、ビジネスの継続性が確保されます。

-   **リアルタイム分析**

    組み込みの分析エンジンを使用して、リアルタイムの分析クエリ結果を取得します。 TiDB Cloudは、ミッションクリティカルなアプリケーションを妨げることなく、現在のデータに対して一貫した分析クエリを実行します。

-   **エンタープライズグレードのSecurity**

    送信中と保存中の両方の暗号化をサポートし、専用のネットワークとマシンでデータをセキュリティ。 TiDB Cloud は、SOC 2 Type 2、ISO 27001:2013、ISO 27701 によって認定されており、GDPR に完全に準拠しています。

-   **フルマネージドサービス**

    使いやすい Web ベースの管理プラットフォームを介して、数回クリックするだけで TiDB クラスターをデプロイ、拡張、監視、管理できます。

-   **マルチクラウドのサポート**

    クラウド ベンダーにロックインされることなく、柔軟性を維持します。 TiDB Cloudは現在、AWS と Google Cloud で利用できます。

-   **シンプルな料金プラン**

    隠れた手数料のない透明性のある前払い価格で、使用した分だけお支払いください。

-   **ワールドクラスのサポート**

    弊社のサポート ポータル、<a href="mailto:tidbcloud-support@pingcap.com">電子メール</a>、チャット、またはビデオ会議を通じて、世界クラスのサポートを受けてください。

## 導入オプション {#deployment-options}

TiDB Cloud には、次の 2 つの展開オプションが用意されています。

-   [TiDB サーバーレス](https://www.pingcap.com/tidb-serverless)

    TiDB Serverless は、フルマネージドのマルチテナント TiDB 製品です。即時自動スケーリングの MySQL 互換データベースを提供し、豊富な無料枠と、無料制限を超えた場合の従量制課金を提供します。

-   [TiDB専用](https://www.pingcap.com/tidb-dedicated)

    TiDB D dedicated は、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番環境向けです。

TiDB サーバーレスと TiDB 専用の機能の比較については、 [TiDB: 高度なオープンソースの分散 SQL データベース](https://www.pingcap.com/get-started-tidb)を参照してください。

## アーキテクチャ {#architecture}

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

-   TiDB VPC (仮想プライベートクラウド)

    各TiDB Cloudクラスターでは、すべての TiDB ノードと補助ノード ( TiDB Operatorノードやロギング ノードを含む) が独立した VPC にデプロイされます。

-   TiDB Cloudセントラル サービス

    請求、アラート、メタstorage、ダッシュボード UI などのセントラル サービスは独立して展開されます。インターネット経由でダッシュボード UI にアクセスし、TiDB クラスターを操作できます。

-   あなたの VPC

    プライベート エンドポイント接続または VPC ピアリング接続を介して TiDB クラスターに接続できます。詳細は[プライベートエンドポイント接続のセットアップ](/tidb-cloud/set-up-private-endpoint-connections.md)または[VPC ピア接続のセットアップ](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。
