---
title: TiDB Cloud Data Service (Beta) Overview
summary: Learn about Data Service in TiDB Cloud and its scenarios.
---

# TiDB Cloudデータ サービス (ベータ版) の概要 {#tidb-cloud-data-service-beta-overview}

TiDB Cloud は、カスタム API エンドポイントを使用して HTTPS リクエスト経由でTiDB Cloudデータにアクセスできるようにする[<a href="https://tidbcloud.com/console/data-service">データサービス（ベータ版）</a>](https://tidbcloud.com/console/data-service)機能を提供します。この機能は、サーバーレスアーキテクチャを使用してコンピューティング リソースと柔軟なスケーリングを処理するため、インフラストラクチャやメンテナンスのコストを心配することなく、エンドポイントのクエリ ロジックに集中できます。

> **ノート：**
>
> データ サービスは[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB サーバーレス</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターでのみ使用できます。

Data Service のエンドポイントは、SQL ステートメントを実行するようにカスタマイズできる Web API です。 `WHERE`句で使用される値など、SQL ステートメントのパラメータを指定できます。クライアントがエンドポイントを呼び出し、リクエスト URL 内のパラメータの値を指定すると、エンドポイントは指定されたパラメータを使用して対応する SQL ステートメントを実行し、結果を HTTP 応答の一部として返します。

エンドポイントをより効率的に管理するには、Data Apps を使用します。 Data Service のデータ アプリは、特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのグループです。データ アプリを作成すると、エンドポイントをグループ化し、API キーを使用して承認設定を構成し、エンドポイントへのアクセスを制限できます。このようにして、承認されたユーザーのみがデータにアクセスして操作できるようにし、アプリケーションの安全性を高めることができます。

> **ヒント：**
>
> TiDB Cloud は、 TiDB サーバーレス クラスター用の Chat2Query API を提供します。有効にすると、 TiDB Cloud は**Chat2Query**と呼ばれるシステム データ アプリと Data Service に Chat2Data エンドポイントを自動的に作成します。このエンドポイントを呼び出して、AI に指示を提供して SQL ステートメントを生成および実行させることができます。
>
> 詳細については、 [<a href="/tidb-cloud/use-chat2query-api.md">Chat2Query API を使ってみる</a>](/tidb-cloud/use-chat2query-api.md)を参照してください。

## シナリオ {#scenarios}

Data Service を使用すると、 TiDB Cloud をHTTPS と互換性のあるアプリケーションまたはサービスとシームレスに統合できます。以下に、いくつかの典型的な使用シナリオを示します。

-   モバイルまたは Web アプリケーションから TiDB クラスターのデータベースに直接アクセスします。
-   サーバーレス エッジ関数を使用してエンドポイントを呼び出し、データベース接続プーリングによって引き起こされるスケーラビリティの問題を回避します。
-   Data Service をデータ ソースとして使用して、 TiDB Cloudをデータ視覚化プロジェクトと統合します。これにより、データベース接続のユーザー名とパスワードの公開が回避され、API がより安全で使いやすくなります。
-   MySQL インターフェイスがサポートしていない環境からデータベースに接続します。これにより、データにアクセスするための柔軟性とオプションが向上します。

## 次は何ですか {#what-s-next}

-   [<a href="/tidb-cloud/data-service-get-started.md">データサービスを始めてみる</a>](/tidb-cloud/data-service-get-started.md)
-   [<a href="/tidb-cloud/use-chat2query-api.md">Chat2Query API を使ってみる</a>](/tidb-cloud/use-chat2query-api.md)
-   [<a href="/tidb-cloud/data-service-manage-data-app.md">データアプリを管理する</a>](/tidb-cloud/data-service-manage-data-app.md)
-   [<a href="/tidb-cloud/data-service-manage-endpoint.md">エンドポイントの管理</a>](/tidb-cloud/data-service-manage-endpoint.md)
