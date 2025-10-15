---
title: What is TiDB Cloud
summary: TiDB Cloudとそのアーキテクチャについて学習します。
category: intro
---

# TiDB Cloudとは {#what-is-tidb-cloud}

[TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 、オープンソースのハイブリッドトランザクションおよび分析処理（HTAP）データベースである[ティドブ](https://docs.pingcap.com/tidb/stable/overview)クラウドに提供する、フルマネージドの Database-as-a-Service（DBaaS）です。TiDB TiDB Cloud は、データベースの複雑な処理に煩わされることなく、アプリケーションに集中できるよう、データベースの導入と管理を容易にします。<customcontent language="en,zh"> TiDB Cloudクラスターを作成して、Amazon Web Services (AWS)、Google Cloud、Microsoft Azure、Alibaba Cloud 上でミッションクリティカルなアプリケーションを迅速に構築できます。</customcontent><customcontent language="ja"> TiDB Cloudクラスターを作成して、Amazon Web Services (AWS)、Google Cloud、Microsoft Azure 上でミッションクリティカルなアプリケーションを迅速に構築できます。</customcontent>

![TiDB Cloud Overview](/media/tidb-cloud/tidb-cloud-overview.png)

## TiDB Cloudを選ぶ理由 {#why-tidb-cloud}

TiDB Cloud を使用すると、ほとんどまたはまったくトレーニングを必要とせずに、インフラストラクチャ管理やクラスターの展開などの複雑なタスクを簡単に処理できます。

-   開発者とデータベース管理者 (DBA) は、大量のオンライン トラフィックを簡単に処理し、複数のデータセットにわたる大量のデータを迅速に分析できます。

-   あらゆる規模の企業は、前払いなしで、ビジネスの成長に合わせてTiDB Cloud を簡単に導入および管理できます。

TiDB Cloudの詳細については、次のビデオをご覧ください。

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="Why TiDB Cloud?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

TiDB Cloudを使用すると、次の主な機能を利用できます。

-   **高速かつカスタマイズされたスケーリング**

    ACIDトランザクションを維持しながら、重要なワークロード向けに数百ノードまで柔軟かつ透過的にスケールできます。シャーディングを気にする必要はありません。また、ビジネスニーズに合わせて、パフォーマンスノードとstorageノードを個別にスケールできます。

-   **MySQLの互換性**

    TiDBのMySQL互換性により、アプリケーションの生産性を向上させ、市場投入までの時間を短縮できます。コードを書き直すことなく、既存のMySQLインスタンスから簡単にデータを移行できます。

-   **高可用性と信頼性**

    設計上、高い可用性を実現します。複数のアベイラビリティゾーンにわたるデータレプリケーション、毎日のバックアップ、自動フェイルオーバーにより、ハードウェア障害、ネットワークの分断、データセンターの損失など、いかなる状況においてもビジネスの継続性を確保します。

-   **リアルタイム分析**

    内蔵の分析エンジンにより、リアルタイムの分析クエリ結果を取得できます。TiDB TiDB Cloud は、ミッションクリティカルなアプリケーションに影響を与えることなく、最新のデータに対して一貫した分析クエリを実行します。

-   **エンタープライズグレードのSecurity**

    専用ネットワークとマシンでデータをセキュリティ。転送中と保存中の両方の暗号化をサポートします。TiDB TiDB Cloudは、SOC 2 Type 2、ISO 27001:2013、ISO 27701の認証を取得しており、GDPRにも完全準拠しています。

-   **フルマネージドサービス**

    使いやすい Web ベースの管理プラットフォームを使用して、数回のクリックだけで TiDB クラスターをデプロイ、拡張、監視、管理できます。

-   **マルチクラウドサポート**

    <CustomContent language="en,zh">

    クラウドベンダーに縛られることなく、柔軟性を維持できます。TiDB TiDB Cloud は現在、AWS、Azure、Google Cloud、Alibaba Cloud で利用可能です。

    </CustomContent>

    <CustomContent language="ja">

    クラウドベンダーに縛られることなく、柔軟性を維持できます。TiDB TiDB Cloud は現在、AWS、Azure、Google Cloud で利用可能です。

    </CustomContent>

-   **シンプルな料金プラン**

    透明性のある前払い価格設定で、使用した分だけお支払いいただけます。隠れた料金はありません。

-   **世界クラスのサポート**

    サポート ポータル、<a href="mailto:tidbcloud-support@pingcap.com">電子メール</a>、チャット、またはビデオ会議を通じて世界クラスのサポートを受けることができます。

## 展開オプション {#deployment-options}

TiDB Cloud は次の展開オプションを提供します。

-   TiDB Cloud Serverless（Starter に名称変更）

    TiDB Cloud Starterは、フルマネージドのマルチテナント型TiDBサービスです。MySQL互換データベースを瞬時に自動スケーリングし、十分な無料クォータと、無料クォータを超えた場合の使用量に応じた課金体系を提供します。

    <CustomContent language="en,zh">

    現在、 TiDB Cloud Starter は AWS で一般公開されており、Alibaba Cloud ではパブリック プレビュー中です。

    </CustomContent>

-   TiDB Cloudエッセンシャル

    ワークロードが増加し、リアルタイムの拡張性を必要とするアプリケーションに対して、 TiDB Cloud Essential はビジネスの成長に対応できる柔軟性とパフォーマンスを提供します。

    <CustomContent language="en,zh">

    現在、 TiDB Cloud Essential は AWS および Alibaba Cloud でパブリック プレビュー中です。

    Alibaba Cloud 上のTiDB Cloud Starter とTiDB Cloud Essential の機能比較については、 [Alibaba Cloud 上の TiDB](https://www.pingcap.com/partners/alibaba-cloud/)参照してください。

    </CustomContent>

    <CustomContent language="ja">

    現在、 TiDB Cloud Essential は AWS でパブリックプレビュー中です。

    </CustomContent>

-   TiDB Cloud専用

    TiDB Cloud Dedicated は、ミッションクリティカルなビジネス向けに設計されており、複数の可用性ゾーンにわたる高可用性、水平スケーリング、および完全な[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)機能を提供します。

    現在、 TiDB Cloud DedicatedはAWSとGoogle Cloudで一般提供されており、Azureではパブリックプレビュー中です。詳細については、 [TiDB Cloud専用](https://www.pingcap.com/tidb-cloud-dedicated)ご覧ください。

## アーキテクチャ {#architecture}

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

-   TiDB VPC (仮想プライベートクラウド)

    各TiDB Cloudクラスターでは、 TiDB Operatorノードとログ ノードを含むすべての TiDB ノードと補助ノードが同じ VPC にデプロイされます。

-   TiDB Cloudセントラル サービス

    課金、アラート、メタstorage、ダッシュボードUIなどのセントラルサービスは独立してデプロイされます。ダッシュボードUIにアクセスして、インターネット経由でTiDBクラスターを操作できます。

-   あなたのVPC

    TiDB クラスターには、プライベートエンドポイント接続または VPC ピアリング接続を介して接続できます。詳細は[プライベートエンドポイント接続を設定する](/tidb-cloud/set-up-private-endpoint-connections.md)または[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。
