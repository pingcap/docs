---
title: Connect to Your TiDB Dedicated Cluster
summary: さまざまな方法で TiDB 専用クラスターに接続する方法を学習します。
---

# TiDB専用クラスタに接続する {#connect-to-your-tidb-dedicated-cluster}

このドキュメントでは、TiDB 専用クラスターに接続する方法について説明します。

> **ヒント：**
>
> TiDB Serverless クラスターに接続する方法については、 [TiDB サーバーレスクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster-serverless.md)参照してください。

TiDB Cloud上に TiDB 専用クラスターが作成されたら、次のいずれかの方法でそのクラスターに接続できます。

-   [標準接続で接続する](/tidb-cloud/connect-via-standard-connection.md)

    標準接続では、トラフィック フィルター付きのパブリック エンドポイントが公開されるため、ラップトップから SQL クライアントを介して TiDB クラスターに接続できます。TLS を使用して TiDB クラスターに接続できるため、アプリケーションから TiDB クラスターへのデータ転送のセキュリティが確保されます。

-   [AWS のプライベートエンドポイント経由で接続する](/tidb-cloud/set-up-private-endpoint-connections.md) (推奨)

    AWS でホストされている TiDB 専用クラスターの場合、プライベートエンドポイント接続によりプライベートエンドポイントが提供され、VPC 内の SQL クライアントが AWS PrivateLink 経由で安全にサービスにアクセスできるようになります。これにより、簡素化されたネットワーク管理でデータベースサービスへの非常に安全な一方向アクセスが提供されます。

-   [プライベートエンドポイント経由で Google Cloud に接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md) (推奨)

    Google Cloud でホストされている TiDB 専用クラスタの場合、プライベート エンドポイント接続によりプライベート エンドポイントが提供され、VPC 内の SQL クライアントは Google Cloud Private Service Connect を介して安全にサービスにアクセスできるようになります。これにより、簡素化されたネットワーク管理でデータベース サービスへの非常に安全な一方向アクセスが実現します。

-   [VPCピアリング経由で接続](/tidb-cloud/set-up-vpc-peering-connections.md)

    レイテンシーを低くしてセキュリティを強化したい場合は、VPC ピアリングを設定し、クラウド アカウント内の対応するクラウド プロバイダーの VM インスタンスを使用してプライベート エンドポイント経由で接続します。

-   [Chat2Query経由で接続（ベータ版）](/tidb-cloud/explore-data-with-chat2query.md)

    > **注記：**
    >
    > [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターで Chat2Query を使用するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

    TiDB Cloudは人工知能 (AI) を活用しています。クラスターが AWS でホストされており、クラスターの TiDB バージョンが v6.5.0 以降である場合は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の AI 搭載 SQL エディターである Chat2Query (ベータ版) を使用して、データの価値を最大化できます。

    Chat2Query では、単に`--`と入力して指示を入力するだけで AI に SQL クエリを自動的に生成させるか、SQL クエリを手動で記述してターミナルなしでデータベースに対して SQL クエリを実行することができます。クエリ結果をテーブルで直感的に見つけ、クエリ ログを簡単に確認できます。

-   [SQL シェル経由で接続する](/tidb-cloud/connect-via-sql-shell.md) : TiDB SQL を試して、TiDB と MySQL の互換性をすぐにテストしたり、ユーザー権限を管理したりします。

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続されたら、 [TiDBでSQL文を調べる](/basic-sql-operations.md)実行できます。
