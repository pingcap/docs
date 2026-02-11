---
title: Connect to Your TiDB Cloud Starter or Essential Cluster
summary: さまざまな方法でTiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続する方法を学習します。
---

# TiDB Cloud StarterまたはEssential クラスタに接続する {#connect-to-your-tidb-cloud-starter-or-essential-cluster}

このドキュメントでは、TiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続する方法について説明します。

> **ヒント：**
>
> -   TiDB Cloud Dedicated クラスターに接続する方法については、 [TiDB Cloud専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。
> -   このドキュメントでは、TiDB Cloud StarterおよびTiDB Cloud Essentialのネットワーク接続方法に焦点を当てています。特定のツール、ドライバー、またはORMを介してTiDBに接続するには、 [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md)参照してください。

## ネットワーク接続方法 {#network-connection-methods}

TiDB Cloud Starter またはTiDB Cloud Essential クラスターがTiDB Cloud上に作成されたら、次のいずれかの方法でそのクラスターに接続できます。

-   直接接続

    直接接続とは、TCP経由のMySQLネイティブ接続システムを指します。MySQL接続をサポートする任意のツール（例： [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)を使用してクラスタに接続できます。

-   [データサービス（ベータ版）](/tidb-cloud/data-service-overview.md)

    TiDB Cloud は、カスタム API エンドポイントを使用した HTTPS リクエストを介して、AWS でホストされているTiDB Cloud Starter クラスターに接続できるデータサービス機能を提供します。直接接続とは異なり、データサービスは生の SQL ではなく RESTful API を介してクラスターデータにアクセスします。

-   [サーバーレスDriver（ベータ版）](/develop/serverless-driver.md)

    TiDB Cloud はJavaScript 用のサーバーレス ドライバーを提供しており、これにより、直接接続と同じエクスペリエンスでエッジ環境のTiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続できます。

上記の接続方法の中から、ニーズに応じて希望するものを選択できます。

| 接続方法         | ユーザーインターフェース | シナリオ                                                                                                                                |
| ------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| 直接接続         | SQL/ORM      | Java、Node.js、Python などの長期実行環境。                                                                                                      |
| データサービス      | RESTful API  | すべてのブラウザとアプリケーションのインタラクション。                                                                                                         |
| サーバーレスDriver | SQL/ORM      | [Vercelエッジ関数](https://vercel.com/docs/functions/edge-functions)や[Cloudflareワーカー](https://workers.cloudflare.com/)などのサーバーレスおよびエッジ環境。 |

## ネットワーク {#network}

TiDB Cloud Starter とTiDB Cloud Essential には、次の 2 つのネットワーク接続タイプがあります。

-   [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) （推奨）

    プライベートエンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink を介して安全にサービスにアクセスできるようにするプライベートエンドポイントを提供します。これにより、簡素化されたネットワーク管理により、データベースサービスへの非常に安全な一方向アクセスが提供されます。

-   [パブリックエンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)

    標準接続ではパブリック エンドポイントが公開されるため、ラップトップから SQL クライアントを介して TiDB クラスターに接続できます。

    TiDB Cloud Starter およびTiDB Cloud Essential には[TLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)必要です。これにより、アプリケーションから TiDB クラスターへのデータ転送のセキュリティが確保されます。

次の表は、さまざまな接続方法で使用できるネットワークを示しています。

| 接続方法               | ネットワーク                | 説明                                                                                          |
| ------------------ | --------------------- | ------------------------------------------------------------------------------------------- |
| 直接接続               | パブリックまたはプライベートエンドポイント | 直接接続は、パブリック エンドポイントとプライベート エンドポイントの両方を介して行うことができます。                                         |
| データサービス（ベータ版）      | /                     | Data Service (ベータ版) を介して AWS でホストされているTiDB Cloud Starter にアクセスする場合、ネットワーク タイプを指定する必要はありません。 |
| サーバーレスDriver（ベータ版） | パブリックエンドポイント          | Serverless Driver は、パブリック エンドポイント経由の接続のみをサポートします。                                           |

## 次は何？ {#what-s-next}

TiDB クラスターに正常に接続すると、次の操作を実行できます[TiDBでSQL文を調べる](/basic-sql-operations.md) 。
