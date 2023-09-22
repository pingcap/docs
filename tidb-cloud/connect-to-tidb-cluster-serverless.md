---
title: Connect to Your TiDB Serverless Cluster
summary: Learn how to connect to your TiDB Serverless cluster via different methods.
---

# TiDB サーバーレスクラスタに接続する {#connect-to-your-tidb-serverless-cluster}

このドキュメントでは、TiDB サーバーレス クラスターに接続する方法について説明します。

> **ヒント：**
>
> TiDB 専用クラスターに接続する方法については、 [TiDB 専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

## 接続方法 {#connection-methods}

TiDB サーバーレス クラスターがTiDB Cloud上に作成されたら、次のいずれかの方法で接続できます。

-   直接接続

    直接接続とは、TCP を介した MySQL ネイティブ接続システムを意味します。 MySQL 接続をサポートするツール ( [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)など) を使用して、TiDB サーバーレス クラスターに接続できます。

-   [データサービス（ベータ版）](/tidb-cloud/data-service-overview.md)

    TiDB Cloudは、カスタム API エンドポイントを使用した HTTPS リクエスト経由で TiDB サーバーレス クラスターに接続できるデータ サービス機能を提供します。直接接続とは異なり、Data Service は生の SQL ではなく RESTful API を介して TiDB サーバーレス データにアクセスします。

-   [サーバーレスDriver(ベータ版)](/tidb-cloud/serverless-driver.md)

    TiDB Cloud は、 JavaScript 用のサーバーレス ドライバーを提供します。これにより、直接接続と同じエクスペリエンスでエッジ環境の TiDB サーバーレス クラスターに接続できます。

前述の接続方法では、ニーズに基づいて希望する接続方法を選択できます。

| 接続方法        | プロトコル | シナリオ                                                                                                                      |
| ----------- | ----- | ------------------------------------------------------------------------------------------------------------------------- |
| 直接接続        | TCP   | Java、Node.js、Python などの長時間実行環境。                                                                                           |
| データサービス     | HTTP  | すべてのブラウザとアプリケーションの対話。                                                                                                     |
| サーバーレスドライバー | HTTP  | [バーセルエッジ機能](https://vercel.com/docs/functions/edge-functions)や[Cloudflare ワーカー](https://workers.cloudflare.com/)などのエッジ環境。 |

## 通信網 {#network}

TiDB サーバーレスには 2 つのネットワーク接続タイプがあります。

-   [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) (推奨)

    プライベート エンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink 経由でサービスに安全にアクセスできるようにするプライベート エンドポイントを提供します。これにより、簡素化されたネットワーク管理でデータベース サービスへの安全性の高い一方向のアクセスが実現します。

-   [パブリックエンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)

    標準接続ではパブリック エンドポイントが公開されるため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。

    TiDB サーバーレスには[TLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)必要です。これにより、アプリケーションから TiDB クラスターへのデータ送信のセキュリティが確保されます。

次の表は、さまざまな接続方法で使用できるネットワークを示しています。

| 接続方法               | 通信網                    | 説明                                                               |
| ------------------ | ---------------------- | ---------------------------------------------------------------- |
| 直接接続               | パブリックまたはプライベート エンドポイント | 直接接続は、パブリック エンドポイントとプライベート エンドポイントの両方を介して行うことができます。              |
| データサービス（ベータ版）      | /                      | データ サービス (ベータ) 経由で TiDB サーバーレスにアクセスする場合、ネットワーク タイプを指定する必要はありません。 |
| サーバーレスDriver(ベータ版) | パブリックエンドポイント           | サーバーレスDriverは、パブリック エンドポイント経由の接続のみをサポートします。                      |

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続したら、 [TiDB で SQL ステートメントを探索する](/basic-sql-operations.md)を行うことができます。
