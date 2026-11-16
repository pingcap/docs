---
title: Connect to Your {{{ .starter }}} or Essential Instance
summary: "{{{ .starter }}}または{{{ .essential }}}インスタンスにさまざまな方法で接続する方法を学びましょう。"
---

# {{{ .starter }}}またはEssentialインスタンスに接続します {#connect-to-your-tidb-cloud-starter-or-essential-instance}

このドキュメントでは、{{{ .starter }}}または{{{ .essential }}}インスタンスへの接続方法について説明します。

> **Tip:**
>
> - TiDB Cloud Dedicatedクラスターに接続する方法については、 [TiDB Cloud Dedicatedクラスターに接続します](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。
> - このドキュメントでは、{{{ .starter }}}および{{{ .essential }}}のネットワーク接続方法について説明します。特定のツール、ドライバー、または ORM を介して TiDB に接続する方法については、 [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md)を参照してください。

## ネットワーク接続方法 {#network-connection-methods}

TiDB Cloud上に{{{ .starter }}}または{{{ .essential }}}インスタンスが作成されたら、以下のいずれかの方法で接続できます。

- 直接接続

    直接接続とは、TCP を介した MySQL ネイティブ接続システムのことです。MySQL 接続をサポートするツールであれば、[MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)などを使用して{{{ .starter }}}またはEssentialインスタンスに接続できます。

- [Data Service（PREVIEW）](/tidb-cloud/data-service-overview.md)

    TiDB CloudにはData Service機能があり、カスタムAPIエンドポイントを使用してHTTPSリクエスト経由でAWS上でホストされている{{{ .starter }}}インスタンスに接続できます。直接接続とは異なり、Data Serviceは生のSQLではなくRESTful APIを介して{{{ .starter }}}またはEssentialインスタンスのデータにアクセスします。

- [Serverless Driver（PREVIEW）](/develop/serverless-driver.md)

    TiDB CloudはJavaScript用のサーバーレスドライバーを提供しており、これにより、エッジ環境にある{{{ .starter }}}または{{{ .essential }}}インスタンスに、直接接続時と同様の操作感で接続できます。

上記の接続方法の中から、ご自身のニーズに合わせてお好みの方法をお選びください。

| 接続方法         | ユーザーインターフェース | シナリオ                                                                                                                                       |
| ------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 直接接続         | SQL/ORM      | Java、Node.js、Pythonなどの長時間稼働環境。                                                                                                             |
| Data Service      | RESTful API  | すべてのブラウザーおよびアプリケーションとのやり取り。                                                                                                                 |
| Serverless Driver | SQL/ORM      | [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions)や[Cloudflare Workers](https://workers.cloudflare.com/)などのサーバーレスおよびエッジ環境。 |

## ネットワーク {#network}

{{{ .starter }}}と{{{ .essential }}}には、2種類のネットワーク接続タイプがあります。

- [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)(推奨)

    プライベートエンドポイント接続は、VPC内のSQLクライアントがAWS PrivateLink経由でサービスに安全にアクセスできるようにするプライベートエンドポイントを提供します。AWS PrivateLinkは、簡素化されたネットワーク管理で、データベースサービスへの高度に安全な一方向アクセスを提供します。

- [パブリックエンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)

    標準接続ではパブリックエンドポイントが提供されるため、ノートパソコンからSQLクライアントを介して{{{ .starter }}}またはEssentialインスタンスに接続できます。

    {{{ .starter }}}と{{{ .essential }}}は[TLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を必要とします。TLSは、アプリケーションから{{{ .starter }}}またはEssentialインスタンスへのデータ送信のセキュリティを保証します。

以下の表は、さまざまな接続方法で使用できるネットワークを示しています。

| 接続方法               | ネットワーク                | 説明                                                                                |
| ------------------ | --------------------- | --------------------------------------------------------------------------------- |
| 直接接続               | パブリックまたはプライベートエンドポイント | 直接接続は、パブリックエンドポイントとプライベートエンドポイントの両方を介して行えます。                                 |
| Data Service（PREVIEW）      | /                     | AWS上でホストされている{{{ .starter }}}にData Service (PREVIEW)経由でアクセスする場合、ネットワークの種類を指定する必要はありません。 |
| Serverless Driver（PREVIEW） | パブリックエンドポイント             | Serverless Driverは、パブリックエンドポイント経由の接続のみをサポートしています。                                 |

## 次は？ {#what-s-next}

{{{ .starter }}}またはEssentialインスタンスに正常に接続したら、 [TiDBを使用してSQL文を探索する](/basic-sql-operations.md)ことができます。
