---
title: Connect to Your TiDB Cloud Serverless Cluster
summary: さまざまな方法でTiDB Cloud Serverless クラスターに接続する方法を学習します。
---

# TiDB Cloudサーバーレスクラスタに接続する {#connect-to-your-tidb-cloud-serverless-cluster}

このドキュメントでは、 TiDB Cloud Serverless クラスターに接続する方法について説明します。

> **ヒント：**
>
> TiDB Cloud Dedicated クラスターに接続する方法については、 [TiDB Cloud専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

## 接続方法 {#connection-methods}

TiDB TiDB Cloud TiDB Cloud Serverless クラスターが作成されたら、次のいずれかの方法で接続できます。

-   直接接続

    直接接続とは、TCP経由のMySQLネイティブ接続システムを指します。MySQL接続をサポートする任意のツール（例： [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) ）を使用して、 TiDB Cloud Serverlessクラスターに接続できます。

-   [データサービス（ベータ版）](/tidb-cloud/data-service-overview.md)

    TiDB Cloudは、カスタムAPIエンドポイントを使用してHTTPSリクエスト経由でTiDB Cloud Serverlessクラスターに接続できるデータサービス機能を提供します。直接接続とは異なり、データサービスは生のSQLではなくRESTful APIを介してTiDB Cloud Serverlessデータにアクセスします。

-   [サーバーレスDriver（ベータ版）](/tidb-cloud/serverless-driver.md)

    TiDB Cloud はJavaScript 用のサーバーレス ドライバーを提供しており、これにより、直接接続と同じエクスペリエンスでエッジ環境のTiDB Cloud Serverless クラスターに接続できます。

上記の接続方法の中から、ニーズに応じて希望するものを選択できます。

| 接続方法         | ユーザーインターフェース | シナリオ                                                                                                                                |
| ------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| 直接接続         | SQL/ORM      | Java、Node.js、Python などの長期実行環境。                                                                                                      |
| データサービス      | RESTful API  | すべてのブラウザとアプリケーションのインタラクション。                                                                                                         |
| サーバーレスDriver | SQL/ORM      | [Vercelエッジ関数](https://vercel.com/docs/functions/edge-functions)や[Cloudflareワーカー](https://workers.cloudflare.com/)などのサーバーレスおよびエッジ環境。 |

## ネットワーク {#network}

TiDB Cloud Serverless には 2 つのネットワーク接続タイプがあります。

-   [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) （推奨）

    プライベートエンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink を介して安全にサービスにアクセスできるようにするプライベートエンドポイントを提供します。これにより、簡素化されたネットワーク管理により、データベースサービスへの非常に安全な一方向アクセスが提供されます。

-   [パブリックエンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)

    標準接続ではパブリック エンドポイントが公開されるため、ラップトップから SQL クライアントを介して TiDB クラスターに接続できます。

    TiDB Cloud Serverless には[TLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)必要です。これにより、アプリケーションから TiDB クラスターへのデータ転送のセキュリティが確保されます。

次の表は、さまざまな接続方法で使用できるネットワークを示しています。

| 接続方法               | ネットワーク                | 説明                                                                              |
| ------------------ | --------------------- | ------------------------------------------------------------------------------- |
| 直接接続               | パブリックまたはプライベートエンドポイント | 直接接続は、パブリック エンドポイントとプライベート エンドポイントの両方を介して行うことができます。                             |
| データサービス（ベータ版）      | /                     | Data Service (ベータ版) 経由でTiDB Cloud Serverless にアクセスする場合、ネットワーク タイプを指定する必要はありません。 |
| サーバーレスDriver（ベータ版） | パブリックエンドポイント          | Serverless Driver は、パブリック エンドポイント経由の接続のみをサポートします。                               |

## 次は何？ {#what-s-next}

TiDB クラスターに正常に接続すると、 [TiDBでSQL文を調べる](/basic-sql-operations.md) 。
