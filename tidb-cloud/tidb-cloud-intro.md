---
title: TiDB Cloud Introduction
summary: Learn about TiDB Cloud and its architecture.
category: intro
---

# TiDB Cloudの紹介 {#tidb-cloud-introduction}

[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)は、オープンソースの Hybrid Transactional and Analytical Processing (HTAP) データベースである[TiDB](https://docs.pingcap.com/tidb/stable/overview)クラウドにもたらす、完全に管理された Database-as-a-Service (DBaaS) です。 TiDB Cloud は、データベースの複雑さではなく、アプリケーションに集中できるように、データベースを展開および管理する簡単な方法を提供します。 TiDB Cloudクラスターを作成して、Google Cloud Platform (GCP) および Amazon Web Services (AWS) でミッション クリティカルなアプリケーションをすばやく構築できます。

![TiDB Cloud Overview](/media/tidb-cloud/tidb-cloud-overview.png)

## TiDB Cloudを選ぶ理由 {#why-tidb-cloud}

TiDB Cloud を使用すると、トレーニングをほとんどまたはまったく受けなくても、インフラストラクチャ管理やクラスター展開などの複雑なタスクを簡単に処理できます。

-   開発者とデータベース管理者 (DBA) は、大量のオンライン トラフィックを簡単に処理し、複数のデータセットにまたがる大量のデータを迅速に分析できます。

-   あらゆる規模の企業がTiDB Cloud を簡単に展開および管理して、前払いなしでビジネスの成長に適応できます。

TiDB Cloudの詳細については、次のビデオをご覧ください。

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="TiDB クラウドを選ぶ理由" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

TiDB Cloudを使用すると、次の主要な機能を利用できます。

-   **高速でカスタマイズされたスケーリング**

    ACIDトランザクションを維持しながら、重要なワークロード用に数百のノードに柔軟かつ透過的にスケーリングします。シャーディングを気にする必要はありません。また、ビジネス ニーズに応じて、パフォーマンス ノードとstorageノードを個別にスケーリングできます。

-   **MySQL の互換性**

    TiDB の MySQL 互換性により、生産性を向上させ、アプリケーションの市場投入までの時間を短縮します。コードを書き直すことなく、既存の MySQL インスタンスからデータを簡単に移行できます。事前に読み込まれた GitHub イベントのデータセットが含まれているTiDB Cloud [遊び場](/tidb-cloud/tidb-cloud-glossary.md#playground)で、SQL を自由に作成してすぐに実行してください。

-   **高可用性と信頼性**

    設計による自然な高可用性。複数のアベイラビリティ ゾーンにわたるデータ レプリケーション、毎日のバックアップ、および自動フェイルオーバーにより、ハードウェア障害、ネットワーク パーティション、またはデータ センターの損失に関係なく、ビジネスの継続性が確保されます。

-   **リアルタイム分析**

    組み込みの分析エンジンを使用して、リアルタイムの分析クエリ結果を取得します。 TiDB Cloud は、ミッション クリティカルなアプリケーションに影響を与えることなく、現在のデータに対して一貫した分析クエリを実行します。データをロードしたり、クライアントに接続したりすることなく、TiDB Cloud の速度を[遊び場](/tidb-cloud/tidb-cloud-glossary.md#playground)で気軽に体験してください。

-   **エンタープライズ グレードのSecurity**

    飛行中と保管中の両方の暗号化をサポートして、専用のネットワークとマシンでデータをセキュリティ。 TiDB Cloud は、SOC 2 Type 2、ISO 27001:2013、ISO 27701 によって認定されており、GDPR に完全に準拠しています。

-   **フルマネージド サービス**

    使いやすい Web ベースの管理プラットフォームを使用して、数回クリックするだけで TiDB クラスターをデプロイ、スケーリング、監視、および管理します。

-   **マルチクラウドのサポート**

    クラウド ベンダー ロックインなしで柔軟性を維持します。 TiDB Cloudは現在、AWS と GCP で利用できます。

-   **シンプルな料金プラン**

    隠れた料金のない透明な前払い料金で、使用した分だけお支払いください。

-   **ワールドクラスのサポート**

    サポート ポータル、<a href="mailto:tidbcloud-support@pingcap.com">電子メール</a>、チャット、またはビデオ会議を通じて、世界クラスのサポートを受けてください。

## アーキテクチャ {#architecture}

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

-   TiDB VPC (仮想プライベート クラウド)

    各TiDB Cloudクラスターでは、TiDBTiDB Operatorノードと補助ノードが独立した VPC にデプロイされます。

-   TiDB Cloudセントラル サービス

    課金、アラート、メタstorage、ダッシュボード UI などのセントラル サービスは、個別にデプロイされます。ダッシュボード UI にアクセスして、インターネット経由で TiDB クラスターを操作できます。

-   あなたの VPC

    プライベート エンドポイント接続または VPC ピアリング接続を介して TiDB クラスターに接続できます。詳細は[プライベート エンドポイント接続のセットアップ](/tidb-cloud/set-up-private-endpoint-connections.md)または[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。
