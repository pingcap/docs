---
title: Data Service (Beta)
summary: TiDB Cloudのデータ サービスの概念について学習します。
---

# データサービス（ベータ版） {#data-service-beta}

TiDB Cloud [データサービス（ベータ版）](https://tidbcloud.com/project/data-service)は、バックエンド アプリケーション開発を簡素化し、開発者が拡張性が高く安全なデータ駆動型アプリケーションを迅速に構築できるようにする、完全に管理されたローコードの BaaS (Backend-as-a-Service) ソリューションです。

Data Service を使用すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でTiDB Cloudデータにアクセスできます。この機能は、サーバーレスアーキテクチャを使用してコンピューティングリソースと柔軟なスケーリングを処理するため、インフラストラクチャやメンテナンスコストを気にすることなく、エンドポイントのクエリロジックに集中できます。

詳細については[TiDB Cloudデータ サービス (ベータ版) の概要](/tidb-cloud/data-service-overview.md)参照してください。

## データアプリ {#data-app}

[データサービス（ベータ版）](https://tidbcloud.com/project/data-service)のデータアプリは、特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのコレクションです。データアプリを作成することで、エンドポイントをグループ化し、APIキーを使用してエンドポイントへのアクセスを制限する認証設定を構成できます。これにより、承認されたユーザーのみがデータにアクセスして操作できるようにし、アプリケーションのセキュリティを強化できます。

詳細については[データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)参照してください。

## データアプリのエンドポイント {#data-app-endpoints}

[データサービス（ベータ版）](https://tidbcloud.com/project/data-service)のエンドポイントは、SQL 文を実行するためにカスタマイズできる Web API です。SQL 文には、 `WHERE`節で使用される値などのパラメータを指定できます。クライアントがエンドポイントを呼び出し、リクエスト URL でパラメータの値を指定すると、エンドポイントは指定されたパラメータを使用して対応する SQL 文を実行し、結果を HTTP レスポンスの一部として返します。

詳細については[エンドポイントの管理](/tidb-cloud/data-service-manage-endpoint.md)参照してください。

## Chat2Query API {#chat2query-api}

TiDB Cloudの Chat2Query API は、AI が指示を与えることで SQL 文を生成・実行できる RESTful インターフェースです。その後、API がクエリ結果を返します。

詳細については[Chat2Query APIを使い始める](/tidb-cloud/use-chat2query-api.md)参照してください。

## AI統合 {#ai-integrations}

サードパーティ製ツールをデータアプリに統合することで、サードパーティ製ツールが提供する高度な自然言語処理機能と人工知能（AI）機能をアプリケーションに導入し、強化することができます。この統合により、アプリケーションはより複雑なタスクを実行し、インテリジェントなソリューションを提供できるようになります。

現在、GPT や Dify などのサードパーティ ツールをTiDB Cloudコンソールに統合できます。

詳細については[データアプリをサードパーティツールと統合する](/tidb-cloud/data-service-integrations.md)参照してください。

## コードとしてのコンフィグレーション {#configuration-as-code}

TiDB Cloud は、 JSON 構文を使用してデータ アプリの構成全体をコードとして表現する、 コンフィグレーション as Code (CaC) アプローチを提供します。

データ アプリを GitHub に接続することで、 TiDB Cloud はCaC アプローチを使用して、データ アプリの構成を[設定ファイル](/tidb-cloud/data-service-app-config-files.md)として優先 GitHub リポジトリおよびブランチにプッシュできます。

GitHub接続で自動同期とデプロイが有効になっている場合は、GitHub上の設定ファイルを更新することでデータアプリを変更することもできます。設定ファイルの変更をGitHubにプッシュすると、新しい設定がTiDB Cloudに自動的にデプロイされます。

詳細については[GitHub でデータ アプリを自動デプロイ](/tidb-cloud/data-service-manage-github-connection.md)参照してください。
