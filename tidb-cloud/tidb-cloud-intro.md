---
title: TiDB Cloud Introduction
summary: Learn about TiDB Cloud and its architecture.
category: intro
---

# TiDB Cloudの紹介 {#tidb-cloud-introduction}

[TiDB Cloud](https://pingcap.com/products/tidbcloud)は、フルマネージドのサービスとしてのデータベース（DBaaS）であり、TiDBの優れた機能をすべてクラウドにもたらし、データベースの複雑さではなく、アプリケーションに集中できるようにします。

## TiDB Cloudが選ばれる理由 {#why-tidb-cloud}

-   フルマネージドTiDBサービス

    使いやすいWebベースの管理プラットフォームを使用して、数回クリックするだけでTiDBクラスターをデプロイ、拡張、および管理します。

-   マルチクラウドサポート

    クラウドベンダーロックインなしで柔軟性を維持します。 TiDB Cloudは現在AWSとGCPで利用可能であり、今後さらに多くのプラットフォームが利用可能になります。

-   高い耐障害性

    データは複数のアベイラビリティーゾーンに複製され、ミッションクリティカルなアプリケーションのビジネス継続性を確保するために毎日バックアップされます。

-   生産性の向上

    数回クリックするだけで、 TiDB Cloudへの導入、運用、監視が簡単になり、生産性が向上します。

-   エンタープライズグレードのセキュリティ

    飛行中と静止中の両方で暗号化をサポートし、専用のネットワークとマシンでデータをセキュリティします。

-   ワールドクラスのサポート

    サポートポータル、電子メール、チャット、またはビデオ会議を通じて、同じワールドクラスのサポートを利用できます。

-   シンプルな料金プラン

    使用した分だけ支払い、隠された料金なしで透明で前払いの価格設定にします。

## 建築 {#architecture}

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

-   TiDB VPC（仮想プライベートクラウド）

    TiDB Cloudクラスタごとに、 TiDB Operatorノード、ロギングノードなどを含むすべてのTiDBノードと補助ノードが独立したVPCにデプロイされます。

-   TiDB Cloudセントラルサービス

    請求、アラート、メタストレージ、ダッシュボードUIなどの中央サービスは独立して展開されます。ダッシュボードUIにアクセスして、インターネット経由でTiDBクラスタを操作できます。

-   あなたのVPC

    VPCピアリング接続を介してTiDBクラスタに接続できます。詳細は[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。
