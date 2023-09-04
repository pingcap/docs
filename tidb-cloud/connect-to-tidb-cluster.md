---
title: Connect to Your TiDB Dedicated Cluster
summary: Learn how to connect to your TiDB Dedicated cluster via different methods.
---

# TiDB 専用クラスタに接続する {#connect-to-your-tidb-dedicated-cluster}

このドキュメントでは、TiDB 専用クラスターに接続する方法を紹介します。

> **ヒント：**
>
> TiDB サーバーレス クラスターに接続する方法については、 [TiDB サーバーレスクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster-serverless.md)を参照してください。

TiDB 専用クラスターがTiDB Cloud上に作成されたら、次のいずれかの方法でそれに接続できます。

-   [標準接続で接続する](/tidb-cloud/connect-via-standard-connection.md)

    標準接続では、トラフィック フィルターを備えたパブリック エンドポイントが公開されるため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。 TLS を使用して TiDB クラスターに接続できます。これにより、アプリケーションから TiDB クラスターへのデータ送信のセキュリティが確保されます。

-   [プライベートエンドポイント経由でAWSに接続する](/tidb-cloud/set-up-private-endpoint-connections.md) (推奨)

    AWS でホストされている TiDB 専用クラスターの場合、プライベート エンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink 経由でサービスに安全にアクセスできるようにするプライベート エンドポイントを提供します。これにより、簡素化されたネットワーク管理でデータベース サービスへの安全性の高い一方向のアクセスが提供されます。

-   [プライベート エンドポイント経由で Google Cloud に接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md) (推奨)

    Google Cloud でホストされている TiDB 専用クラスターの場合、プライベート エンドポイント接続は、VPC 内の SQL クライアントが Google Cloud Private Service Connect 経由でサービスに安全にアクセスできるようにするプライベート エンドポイントを提供します。これにより、簡素化されたネットワーク管理でデータベース サービスへの安全性の高い一方向のアクセスが実現します。 。

-   [VPC ピアリング経由で接続する](/tidb-cloud/set-up-vpc-peering-connections.md)

    レイテンシーを短縮し、セキュリティを強化したい場合は、VPC ピアリングを設定し、クラウド アカウント内の対応するクラウド プロバイダー上の VM インスタンスを使用してプライベート エンドポイント経由で接続します。

-   [Chat2Query 経由で接続する (ベータ版)](/tidb-cloud/explore-data-with-chat2query.md)

    > **注記：**
    >
    > [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターで Chat2Query を使用するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

    TiDB Cloudは人工知能 (AI) を活用しています。クラスターが AWS でホストされており、クラスターの TiDB バージョンが v6.5.0 以降[TiDB Cloudコンソール](https://tidbcloud.com/)場合は、AI を活用した SQL エディターである Chat2Query (ベータ版) を使用して、データの価値を最大化できます。

    Chat2Query では、 `--`入力してから AI に SQL クエリを自動的に生成させる指示を入力するか、SQL クエリを手動で作成して、ターミナルを使用せずにデータベースに対して SQL クエリを実行することができます。クエリ結果をテーブルで直感的に見つけたり、クエリログを簡単に確認したりできます。

-   [SQL シェル経由で接続する](/tidb-cloud/connect-via-sql-shell.md) : TiDB SQLを試して、TiDB と MySQL の互換性をすぐにテストするか、ユーザー権限を管理します。

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続したら、 [TiDB で SQL ステートメントを探索する](/basic-sql-operations.md)を行うことができます。
