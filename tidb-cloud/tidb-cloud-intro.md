---
title: TiDB Cloud Introduction
summary: Learn about TiDB Cloud and its architecture.
category: intro
---

# TiDB Cloudの概要 {#tidb-cloud-introduction}

[TiDB](https://docs.pingcap.com/tidb/stable/overview)クラウドに提供する、フルマネージドの Database-as-a-Service (DBaaS) です。 TiDB Cloudは、データベースの導入と管理を簡単に行う方法を提供し、データベースの複雑さではなく、アプリケーションに集中できるようにします。 TiDB Cloudクラスターを作成して、Google Cloud Platform (GCP) およびアマゾン ウェブ サービス (AWS) 上でミッションクリティカルなアプリケーションを迅速に構築できます。

![TiDB Cloud Overview](/media/tidb-cloud/tidb-cloud-overview.png)

## TiDB Cloudを選ぶ理由 {#why-tidb-cloud}

TiDB Cloud を使用すると、トレーニングをほとんど、またはまったく受けなくても、インフラストラクチャ管理やクラスター展開などの複雑なタスクを簡単に処理できます。

-   開発者とデータベース管理者 (DBA) は、大量のオンライン トラフィックを簡単に処理し、複数のデータセットにわたる大量のデータを迅速に分析できます。

-   あらゆる規模の企業は、前払いなしでTiDB Cloudを簡単に導入および管理して、ビジネスの成長に適応できます。

TiDB Cloudの詳細については、次のビデオをご覧ください。

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="TiDB クラウドを選ぶ理由" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

TiDB Cloudを使用すると、次の主要な機能を利用できます。

-   **高速かつカスタマイズされたスケーリング**

    ACIDトランザクションを維持しながら、重要なワークロードに合わせて数百のノードに弾力的かつ透過的に拡張します。シャーディングを気にする必要はありません。また、ビジネス ニーズに応じてパフォーマンス ノードとstorageノードを個別に拡張できます。

-   **MySQL の互換性**

    TiDB の MySQL 互換性により、生産性が向上し、アプリケーションの市場投入までの時間が短縮されます。コードを書き直すことなく、既存の MySQL インスタンスからデータを簡単に移行できます。 TiDB Cloud [遊び場](/tidb-cloud/tidb-cloud-glossary.md#playground)には、GitHub イベントの事前ロードされたデータセットが含まれているため、SQL を即座に作成して実行できます。

-   **高可用性と信頼性**

    当然のことながら、設計により可用性が高くなります。複数のアベイラビリティーゾーンにわたるデータのレプリケーション、毎日のバックアップ、自動フェイルオーバーにより、ハードウェア障害、ネットワークの分断、データセンターの損失に関係なく、ビジネスの継続性が保証されます。

-   **リアルタイム分析**

    組み込みの分析エンジンを使用して、リアルタイムの分析クエリ結果を取得します。 TiDB Cloudは、ミッションクリティカルなアプリケーションを妨げることなく、現在のデータに対して一貫した分析クエリを実行します。データをロードしたりクライアントに接続したりせずに、TiDB Cloud の速度を[遊び場](/tidb-cloud/tidb-cloud-glossary.md#playground)つで気軽に体験してください。

-   **エンタープライズグレードのSecurity**

    送信中と保存中の両方の暗号化をサポートし、専用のネットワークとマシンでデータをセキュリティ。 TiDB Cloud は、SOC 2 Type 2、ISO 27001:2013、ISO 27701 によって認定されており、GDPR に完全に準拠しています。

-   **フルマネージドサービス**

    使いやすい Web ベースの管理プラットフォームを介して、数回クリックするだけで TiDB クラスターをデプロイ、拡張、監視、管理できます。

-   **マルチクラウドのサポート**

    クラウド ベンダーにロックインされることなく、柔軟性を維持します。 TiDB Cloudは現在、AWS と GCP で利用できます。

-   **シンプルな料金プラン**

    隠れた手数料のない透明性のある前払い価格で、使用した分だけお支払いください。

-   **ワールドクラスのサポート**

    弊社のサポート ポータル、<a href="mailto:tidbcloud-support@pingcap.com">電子メール</a>、チャット、またはビデオ会議を通じて、世界クラスのサポートを受けてください。

## アーキテクチャ {#architecture}

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

-   TiDB VPC (仮想プライベートクラウド)

    各TiDB Cloudクラスターでは、すべての TiDB ノードと補助ノード ( TiDB Operatorノードやロギング ノードを含む) が独立した VPC にデプロイされます。

-   TiDB Cloudセントラル サービス

    請求、アラート、メタstorage、ダッシュボード UI などのセントラル サービスは独立して展開されます。インターネット経由でダッシュボード UI にアクセスし、TiDB クラスターを操作できます。

-   あなたの VPC

    プライベート エンドポイント接続または VPC ピアリング接続を介して TiDB クラスターに接続できます。詳細は[VPC ピア接続のセットアップ](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。
