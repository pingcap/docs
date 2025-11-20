---
title: Connect to Your TiDB Cloud Premium Instance
summary: さまざまな方法でTiDB Cloud Premium インスタンスに接続する方法を学習します。
---

# TiDB Cloud Premiumインスタンスに接続する {#connect-to-your-tidb-cloud-premium-instance}

このドキュメントでは、 TiDB Cloud Premium インスタンスに接続する方法について説明します。

> **ヒント：**
>
> TiDB Cloud Dedicated クラスターに接続する方法については、 [TiDB Cloud専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

## 接続方法 {#connection-methods}

TiDB TiDB Cloud TiDB Cloud Premium インスタンスが作成されると、直接接続を介してそのインスタンスに接続できます。

直接接続とは[MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) TCP経由のMySQLネイティブ接続システムを指します。1 など、MySQL接続をサポートする任意のツールを使用してインスタンスに接続できます。

| 接続方法 | ユーザーインターフェース | シナリオ                           |
| ---- | ------------ | ------------------------------ |
| 直接接続 | SQL/ORM      | Java、Node.js、Python などの長期実行環境。 |

## ネットワーク {#network}

TiDB Cloud Premium には 2 つのネットワーク接続タイプがあります。

-   [プライベートエンドポイント](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md) （推奨）

    プライベートエンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink を介して安全にサービスにアクセスできるようにするプライベートエンドポイントを提供します。これにより、簡素化されたネットワーク管理により、データベースサービスへの非常に安全な一方向アクセスが提供されます。

-   [パブリックエンドポイント](/tidb-cloud/premium/connect-to-premium-via-public-connection.md)

    標準接続ではパブリック エンドポイントが公開されるため、ラップトップから SQL クライアントを介して TiDB インスタンスに接続できます。

<!-- To ensure the security of data transmission, you need to [establish a TLS connection](/tidb-cloud/premium/tidb-cloud-tls-connect-to-premium.md) from your client to your instance. -->

使用できるネットワークを次の表に示します。

| 接続方法 | ネットワーク                | 説明                                                  |
| ---- | --------------------- | --------------------------------------------------- |
| 直接接続 | パブリックまたはプライベートエンドポイント | 直接接続は、パブリック エンドポイントとプライベート エンドポイントの両方を介して行うことができます。 |

## 次は何？ {#what-s-next}

TiDB インスタンスに正常に接続すると、次の操作を実行できます[TiDBでSQL文を調べる](/basic-sql-operations.md) 。
