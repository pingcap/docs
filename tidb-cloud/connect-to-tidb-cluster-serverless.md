---
title: Connect to Your TiDB Serverless Cluster
summary: Learn how to connect to your TiDB Serverless cluster via different methods.
---

# TiDB サーバーレスクラスタに接続する {#connect-to-your-tidb-serverless-cluster}

このドキュメントでは、TiDB サーバーレス クラスターに接続する方法を紹介します。

> **ヒント：**
>
> TiDB 専用クラスターに接続する方法については、 [TiDB 専用クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

TiDB サーバーレス クラスターがTiDB Cloud上に作成されたら、次のいずれかの方法で接続できます。

-   [プライベートエンドポイント経由で接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) (推奨)

    プライベート エンドポイント接続は、VPC 内の SQL クライアントが AWS PrivateLink 経由でサービスに安全にアクセスできるようにするプライベート エンドポイントを提供します。これにより、簡素化されたネットワーク管理でデータベース サービスへの安全性の高い一方向のアクセスが実現します。

-   [パブリックエンドポイント経由で接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)

    標準接続では、トラフィック フィルターを備えたパブリック エンドポイントが公開されるため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。

    TiDB サーバーレスは[TLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)サポートしており、アプリケーションから TiDB クラスターへのデータ送信のセキュリティを確保します。

-   [Chat2Query 経由で接続する (ベータ版)](/tidb-cloud/explore-data-with-chat2query.md)

    TiDB Cloud は人工知能 (AI) を活用しています。 [TiDB Cloudコンソール](https://tidbcloud.com/)の AI を活用した SQL エディターである Chat2Query (ベータ版) を使用すると、データの価値を最大化できます。

    Chat2Query では、 `--`入力してから AI に SQL クエリを自動的に生成させる指示を入力するか、SQL クエリを手動で作成して、ターミナルを使用せずにデータベースに対して SQL クエリを実行することができます。クエリ結果をテーブルで直感的に見つけたり、クエリログを簡単に確認したりできます。

## 次は何ですか {#what-s-next}

TiDB クラスターに正常に接続したら、 [TiDB で SQL ステートメントを探索する](/basic-sql-operations.md)を行うことができます。
