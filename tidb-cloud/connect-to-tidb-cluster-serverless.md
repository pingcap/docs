---
title: Connect to Your TiDB Cloud Starter or Essential Instance
summary: TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスにさまざまな方法で接続する方法を学びましょう。
---

# TiDB Cloud StarterまたはEssentialインスタンスに接続します {#connect-to-your-tidb-cloud-starter-or-essential-instance}

このドキュメントでは、TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスへの接続方法について説明します。

> **ヒント：**
>
> -   TiDB Cloud Dedicatedクラスターに接続する方法については、 [TiDB Cloud Dedicatedクラスタに接続します](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。
> -   このドキュメントでは、TiDB Cloud StarterおよびTiDB Cloud Essentialのネットワーク接続方法について説明します。特定のツール、ドライバ、または ORM を介して TiDB に接続する方法については、 [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md)参照してください。

## ネットワーク接続方法 {#network-connection-methods}

TiDB TiDB Cloud上にTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスが作成されたら、以下のいずれかの方法で接続できます。

-   直接接続

    直接接続とは、TCP を介した MySQL ネイティブ接続システムのことです。MySQL 接続をサポートするツールであれば、MySQL などを使用してTiDB Cloud StarterまたはEssential [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)に接続できます。 。

-   [データサービス（ベータ版）](/tidb-cloud/data-service-overview.md)

    TiDB Cloudにはデータサービス機能があり、カスタムAPIエンドポイントを使用してHTTPSリクエスト経由でAWS上でホストされているTiDB Cloud Starterインスタンスに接続できます。直接接続とは異なり、データサービスは生のSQLではなくRESTful APIを介してTiDB Cloud StarterまたはEssentialインスタンスのデータにアクセスします。

-   [サーバーレスDriver（ベータ版）](/develop/serverless-driver.md)

    TiDB CloudはJavaScript用のサーバーレスドライバを提供しており、これにより、エッジ環境にあるTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに、直接接続時と同様の操作感で接続できます。

上記の接続方法の中から、ご自身のニーズに合わせてお好みの方法をお選びください。

| 接続方法         | ユーザーインターフェース | シナリオ                                                                                                                                       |
| ------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 直接接続         | SQL/ORM      | Java、Node.js、Pythonなどの長時間稼働環境。                                                                                                             |
| データサービス      | RESTful API  | すべてのブラウザおよびアプリケーションとのやり取り。                                                                                                                 |
| サーバーレスDriver | SQL/ORM      | [Vercel Edgeの機能](https://vercel.com/docs/functions/edge-functions)や[Cloudflare Workers](https://workers.cloudflare.com/)などのサーバーレスおよびエッジ環境。 |

## ネットワーク {#network}

TiDB Cloud StarterとTiDB Cloud Essentialには、2種類のネットワーク接続タイプがあります。

-   [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)(推奨)

    プライベートエンドポイント接続は、VPC内のSQLクライアントがAWS PrivateLink経由でサービスに安全にアクセスできるようにするプライベートエンドポイントを提供します。AWS PrivateLinkは、簡素化されたネットワーク管理で、データベースサービスへの高度に安全な一方向アクセスを提供します。

-   [公開エンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)

    標準接続では公開エンドポイントが提供されるため、ノートパソコンからSQLクライアントを介してTiDB Cloud StarterまたはEssentialインスタンスに接続できます。

    TiDB Cloud StarterとTiDB Cloud Essentialは[TLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を必要とします。TLSは、アプリケーションからTiDB Cloud StarterまたはEssentialインスタンスへのデータ送信のセキュリティを保証します。

以下の表は、さまざまな接続方法で使用できるネットワークを示しています。

| 接続方法               | ネットワーク                | 説明                                                                                |
| ------------------ | --------------------- | --------------------------------------------------------------------------------- |
| 直接接続               | パブリックまたはプライベートエンドポイント | 直接接続は、パブリックエンドポイントとプライベートエンドポイントの両方を介して行うことができます。                                 |
| データサービス（ベータ版）      | /                     | データサービス（ベータ版）を介してAWS上でホストされているTiDB Cloud Starterにアクセスする場合、ネットワークの種類を指定する必要はありません。 |
| サーバーレスDriver（ベータ版） | 公開エンドポイント             | Serverless Driverは、パブリックエンドポイント経由の接続のみをサポートしています。                                 |

## 次は？ {#what-s-next}

TiDB Cloud StarterまたはEssentialインスタンスに正常に接続したら、 [TiDBを使用してSQLステートメントを探索する](/basic-sql-operations.md)ことができます。
