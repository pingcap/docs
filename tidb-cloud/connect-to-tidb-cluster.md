---
title: Connect to Your TiDB Cluster
summary: Learn how to connect to your TiDB cluster via different methods.
---

# TiDBクラスタに接続する {#connect-to-your-tidb-cluster}

TiDB Cloudで TiDB クラスターが作成されたら、TiDB クラスターに接続できます。 Serverless Tier クラスターまたは Dedicated Tier クラスターのどちらを使用しているかに応じて、次のように使用可能な接続方法を見つけることができます。

## サーバーレス層 {#serverless-tier}

サーバーレス層クラスターの場合、標準接続またはTiDB Cloudコンソールの SQL エディター (ベータ) を介してクラスターに接続できます。

-   [標準接続で接続](/tidb-cloud/connect-via-standard-connection.md#serverless-tier)

    標準接続では、トラフィック フィルターを使用してパブリック エンドポイントが公開されるため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。

    サーバーレス層のみ[TLS 接続をサポート](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md) 。アプリケーションから TiDB クラスターへのデータ転送のセキュリティを確保します。

-   SQL エディター経由で接続 (ベータ)

    SQL エディターは[TiDB Cloudコンソール](https://tidbcloud.com/)の Web ベースの SQL エディターで、Serverless Tier のデータベースに対して SQL クエリを直接編集および実行できます。 SQL エディターにアクセスするには、 [**クラスタ**](https://tidbcloud.com/console/clusters)ページに移動し、クラスターを見つけて [**接続**] をクリックし、ドロップダウン リストで [ <strong>SQL エディター</strong>] を選択します。

## 専用ティア {#dedicated-tier}

Dedicated Tier クラスターの場合、次のいずれかの方法でクラスターに接続できます。

-   [標準接続で接続](/tidb-cloud/connect-via-standard-connection.md#dedicated-tier)

    標準接続では、トラフィック フィルターを使用してパブリック エンドポイントが公開されるため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。 TLS を使用して TiDB クラスターに接続できます。これにより、アプリケーションから TiDB クラスターへのデータ転送のセキュリティが保証されます。

-   [プライベート エンドポイント経由で接続する](/tidb-cloud/set-up-private-endpoint-connections.md) (推奨)

    プライベート エンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink を介してサービスに安全にアクセスできるようにするプライベート エンドポイントを提供します。これにより、ネットワーク管理が簡素化されたデータベース サービスへの高度に安全な一方向アクセスが提供されます。

-   [VPC ピアリング経由で接続する](/tidb-cloud/set-up-vpc-peering-connections.md)

    レイテンシーを下げてセキュリティを強化したい場合は、VPC ピアリングをセットアップし、クラウド アカウントの対応するクラウド プロバイダーの VM インスタンスを使用して、プライベート エンドポイント経由で接続します。

-   [SQL シェル経由で接続](/tidb-cloud/connect-via-sql-shell.md) : TiDB SQLを試して、TiDB と MySQL との互換性をすばやくテストするか、ユーザー権限を管理します。

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続したら、次のことができ[TiDB で SQL ステートメントを調べる](/basic-sql-operations.md) 。
