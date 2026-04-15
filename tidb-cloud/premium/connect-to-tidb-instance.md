---
title: Connect to Your TiDB Cloud Premium Instance
summary: さまざまな方法でTiDB Cloud Premiumインスタンスに接続する方法を学びましょう。
---

# TiDB Cloud Premiumインスタンスに接続します {#connect-to-your-tidb-cloud-premium-instance}

このドキュメントでは、 TiDB Cloud Premiumインスタンスへの接続方法について説明します。

> **ヒント：**
>
> TiDB Cloud Dedicatedクラスターに接続する方法については、 [TiDB Cloud Dedicatedクラスタに接続します](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

## 接続方法 {#connection-methods}

TiDB TiDB Cloud TiDB Cloud Premiumインスタンスが作成されたら、直接接続で接続できます。

直接接続とは、TCP を介した MySQL ネイティブ接続システムのことです。MySQL 接続をサポートするツールであれば、 [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)などを使用してインスタンスに接続できます。 。

| 接続方法 | ユーザーインターフェース | シナリオ                           |
| ---- | ------------ | ------------------------------ |
| 直接接続 | SQL/ORM      | Java、Node.js、Pythonなどの長時間稼働環境。 |

## ネットワーク {#network}

TiDB Cloud Premiumには、2種類のネットワーク接続タイプがあります。

-   [プライベートエンドポイント](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)(推奨)

    プライベートエンドポイント接続は、VPC内のSQLクライアントがAWS PrivateLink経由でサービスに安全にアクセスできるようにするプライベートエンドポイントを提供します。AWS PrivateLinkは、簡素化されたネットワーク管理で、データベースサービスへの高度に安全な一方向アクセスを提供します。

-   [公開エンドポイント](/tidb-cloud/premium/connect-to-premium-via-public-connection.md)

    標準接続では公開エンドポイントが提供されるため、ノートパソコンからSQLクライアントを介してTiDB Cloud Premiumインスタンスに接続できます。

<!-- To ensure the security of data transmission, you need to [establish a TLS connection](/tidb-cloud/premium/tidb-cloud-tls-connect-to-premium.md) from your client to your instance. -->

以下の表は、利用可能なネットワークを示しています。

| 接続方法 | ネットワーク                | 説明                                                |
| ---- | --------------------- | ------------------------------------------------- |
| 直接接続 | パブリックまたはプライベートエンドポイント | 直接接続は、パブリックエンドポイントとプライベートエンドポイントの両方を介して行うことができます。 |

## 次は？ {#what-s-next}

TiDB Cloud Premium インスタンスに正常に接続したら、 [TiDBを使用してSQLステートメントを探索する](/basic-sql-operations.md)ことができます。
