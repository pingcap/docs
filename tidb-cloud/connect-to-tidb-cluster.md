---
title: Connect to Your TiDB Cluster
summary: Learn how to connect to your TiDB cluster via different methods.
---

# TiDBクラスタに接続する {#connect-to-your-tidb-cluster}

TiDB クラスターがTiDB Cloudに作成されたら、TiDB クラスターに接続できます。 Serverless TierクラスターまたはDedicated Tierクラスターのどちらを使用しているかに応じて、次のように使用可能な接続方法を見つけることができます。

## Serverless Tier {#serverless-tier}

Serverless Tierクラスターの場合、標準接続またはTiDB Cloudコンソールの Chat2Query (ベータ) を介してクラスターに接続できます。

-   [標準接続で接続](/tidb-cloud/connect-via-standard-connection.md#serverless-tier)

    標準接続は、トラフィック フィルターを使用してパブリック エンドポイントを公開するため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。

    Serverless Tierのみ[TLS 接続をサポート](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md) 。アプリケーションから TiDB クラスターへのデータ転送のセキュリティを確保します。

-   [Chat2Query (ベータ版) 経由で接続する](/tidb-cloud/explore-data-with-chat2query.md)

    TiDB Cloud は人工知能 (AI) を利用しています。 [TiDB Cloudコンソール](https://tidbcloud.com/)の AI 搭載 SQL エディターである Chat2Query (ベータ版) を使用して、データの価値を最大化できます。

    Chat2Query では、単に`--`を入力してから命令を入力し、AI に SQL クエリを自動的に生成させるか、SQL クエリを手動で記述してから、ターミナルを使用せずにデータベースに対して SQL クエリを実行することができます。クエリ結果をテーブルで直感的に検索し、クエリ ログを簡単に確認できます。

## Dedicated Tier {#dedicated-tier}

Dedicated Tierクラスターの場合、次のいずれかの方法でクラスターに接続できます。

-   [標準接続で接続](/tidb-cloud/connect-via-standard-connection.md#dedicated-tier)

    標準接続は、トラフィック フィルターを使用してパブリック エンドポイントを公開するため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。 TLS を使用して TiDB クラスターに接続できます。これにより、アプリケーションから TiDB クラスターへのデータ転送のセキュリティが保証されます。

-   [プライベート エンドポイント経由で接続する](/tidb-cloud/set-up-private-endpoint-connections.md) (推奨)

    プライベート エンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink を介してサービスに安全にアクセスできるようにするプライベート エンドポイントを提供します。これにより、ネットワーク管理が簡素化されたデータベース サービスへの高度に安全な一方向アクセスが提供されます。

-   [VPC ピアリング経由で接続する](/tidb-cloud/set-up-vpc-peering-connections.md)

    レイテンシーを下げてセキュリティを強化したい場合は、VPC ピアリングをセットアップし、クラウド アカウントの対応するクラウド プロバイダーの VM インスタンスを使用して、プライベート エンドポイント経由で接続します。

-   [SQL シェル経由で接続](/tidb-cloud/connect-via-sql-shell.md) : TiDB SQLを試して、TiDB と MySQL との互換性をすばやくテストするか、ユーザー権限を管理します。

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続したら、 [TiDB で SQL ステートメントを調べる](/basic-sql-operations.md)ことができます。
