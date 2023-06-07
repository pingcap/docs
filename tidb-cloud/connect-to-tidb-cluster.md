---
title: Connect to Your TiDB Cluster
summary: Learn how to connect to your TiDB cluster via different methods.
---

# TiDBクラスタに接続する {#connect-to-your-tidb-cluster}

TiDB クラスターがTiDB Cloud上に作成されたら、TiDB クラスターに接続できます。 TiDB サーバーレス クラスターと TiDB 専用クラスターのどちらを使用しているかに応じて、使用可能な接続方法は次のようになります。

## TiDB サーバーレス {#tidb-serverless}

TiDB サーバーレス クラスターの場合、次のいずれかの方法でクラスターに接続できます。

-   [<a href="/tidb-cloud/set-up-private-endpoint-connections.md">プライベートエンドポイント経由で接続する</a>](/tidb-cloud/set-up-private-endpoint-connections.md) (推奨)

    プライベート エンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink 経由でサービスに安全にアクセスできるようにするプライベート エンドポイントを提供します。これにより、簡素化されたネットワーク管理でデータベース サービスへの安全性の高い一方向のアクセスが実現します。

-   [<a href="/tidb-cloud/connect-via-standard-connection.md#tidb-serverless">標準接続で接続する</a>](/tidb-cloud/connect-via-standard-connection.md#tidb-serverless)

    標準接続では、トラフィック フィルターを備えたパブリック エンドポイントが公開されるため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。

    TiDB サーバーレスは[<a href="/tidb-cloud/secure-connections-to-serverless-tier-clusters.md">TLS接続</a>](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md)をサポートしており、アプリケーションから TiDB クラスターへのデータ送信のセキュリティを確保します。

-   [<a href="/tidb-cloud/explore-data-with-chat2query.md">Chat2Query 経由で接続する (ベータ版)</a>](/tidb-cloud/explore-data-with-chat2query.md)

    TiDB Cloud は人工知能 (AI) を活用しています。 [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)の AI を活用した SQL エディターである Chat2Query (ベータ版) を使用すると、データの価値を最大化できます。

    Chat2Query では、 `--`を入力してから AI に SQL クエリを自動的に生成させる指示を入力するか、SQL クエリを手動で作成して、ターミナルを使用せずにデータベースに対して SQL クエリを実行することができます。クエリ結果をテーブルで直感的に見つけたり、クエリログを簡単に確認したりできます。

## TiDB専用 {#tidb-dedicated}

TiDB 専用クラスターの場合、次のいずれかの方法でクラスターに接続できます。

-   [<a href="/tidb-cloud/connect-via-standard-connection.md#tidb-dedicated">標準接続で接続する</a>](/tidb-cloud/connect-via-standard-connection.md#tidb-dedicated)

    標準接続では、トラフィック フィルターを備えたパブリック エンドポイントが公開されるため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。 TLS を使用して TiDB クラスターに接続できます。これにより、アプリケーションから TiDB クラスターへのデータ送信のセキュリティが確保されます。

-   [<a href="/tidb-cloud/set-up-private-endpoint-connections.md">プライベートエンドポイント経由で接続する</a>](/tidb-cloud/set-up-private-endpoint-connections.md) (推奨)

    プライベート エンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink 経由でサービスに安全にアクセスできるようにするプライベート エンドポイントを提供します。これにより、簡素化されたネットワーク管理でデータベース サービスへの安全性の高い一方向のアクセスが実現します。

-   [<a href="/tidb-cloud/set-up-vpc-peering-connections.md">VPC ピアリング経由で接続する</a>](/tidb-cloud/set-up-vpc-peering-connections.md)

    レイテンシーを短縮し、セキュリティを強化したい場合は、VPC ピアリングを設定し、クラウド アカウント内の対応するクラウド プロバイダー上の VM インスタンスを使用してプライベート エンドポイント経由で接続します。

-   [<a href="/tidb-cloud/connect-via-sql-shell.md">SQL シェル経由で接続する</a>](/tidb-cloud/connect-via-sql-shell.md) : TiDB SQLを試して、TiDB と MySQL の互換性をすぐにテストするか、ユーザー権限を管理します。

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続したら、 [<a href="/basic-sql-operations.md">TiDB で SQL ステートメントを探索する</a>](/basic-sql-operations.md)を行うことができます。
