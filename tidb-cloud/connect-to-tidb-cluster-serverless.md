---
title: Connect to Your TiDB Serverless Cluster
summary: さまざまな方法で TiDB Serverless クラスターに接続する方法を学習します。
---

# TiDB サーバーレスクラスタに接続する {#connect-to-your-tidb-serverless-cluster}

このドキュメントでは、TiDB Serverless クラスターに接続する方法について説明します。

> **ヒント：**
>
> TiDB 専用クラスターに接続する方法については、 [TiDB専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

## 接続方法 {#connection-methods}

TiDB Cloud上に TiDB Serverless クラスターが作成されたら、次のいずれかの方法で接続できます。

-   直接接続

    直接接続とは、TCP 経由の MySQL ネイティブ接続システムを意味します。1 [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)の MySQL 接続をサポートする任意のツールを使用して、TiDB Serverless クラスターに接続できます。

-   [データ サービス (ベータ版)](/tidb-cloud/data-service-overview.md)

    TiDB Cloud は、カスタム API エンドポイントを使用して HTTPS リクエスト経由で TiDB Serverless クラスターに接続できるデータ サービス機能を提供します。直接接続とは異なり、データ サービスは生の SQL ではなく RESTful API 経由で TiDB Serverless データにアクセスします。

-   [サーバーレスDriver(ベータ版)](/tidb-cloud/serverless-driver.md)

    TiDB Cloud はJavaScript 用のサーバーレス ドライバーを提供しており、これにより、直接接続と同じエクスペリエンスでエッジ環境の TiDB Serverless クラスターに接続できます。

上記の接続方法では、ニーズに応じて希望するものを選択できます。

| 接続方法         | ユーザーインターフェース | シナリオ                                                                                                                                  |
| ------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| 直接接続         | SQL/ORM      | Java、Node.js、Python などの長期実行環境。                                                                                                        |
| データサービス      | RESTful API  | すべてのブラウザとアプリケーションのインタラクション。                                                                                                           |
| サーバーレスDriver | SQL/ORM      | [Vercel エッジ機能](https://vercel.com/docs/functions/edge-functions)や[Cloudflare ワーカー](https://workers.cloudflare.com/)などのサーバーレス環境やエッジ環境。 |

## 通信網 {#network}

TiDB Serverless には 2 つのネットワーク接続タイプがあります。

-   [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) (推奨)

    プライベートエンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink 経由で安全にサービスにアクセスできるようにするプライベートエンドポイントを提供します。これにより、簡素化されたネットワーク管理でデータベースサービスへの非常に安全な一方向アクセスが提供されます。

-   [パブリックエンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)

    標準接続ではパブリック エンドポイントが公開されるため、ラップトップから SQL クライアントを介して TiDB クラスターに接続できます。

    TiDB Serverless には[TLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)必要であり、これによりアプリケーションから TiDB クラスターへのデータ転送のセキュリティが確保されます。

次の表は、さまざまな接続方法で使用できるネットワークを示しています。

| 接続方法               | 通信網                   | 説明                                                                     |
| ------------------ | --------------------- | ---------------------------------------------------------------------- |
| 直接接続               | パブリックまたはプライベートエンドポイント | 直接接続は、パブリック エンドポイントとプライベート エンドポイントの両方を介して行うことができます。                    |
| データ サービス (ベータ版)    | /                     | データ サービス (ベータ版) 経由で TiDB Serverless にアクセスする場合、ネットワーク タイプを指定する必要はありません。 |
| サーバーレスDriver(ベータ版) | パブリックエンドポイント          | Serverless Driver は、パブリック エンドポイント経由の接続のみをサポートします。                      |

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続されたら、 [TiDBでSQL文を調べる](/basic-sql-operations.md)実行できます。
