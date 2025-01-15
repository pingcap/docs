---
title: Data Service (Beta)
summary: TiDB Cloudのデータ サービスの概念について学習します。
---

# データ サービス (ベータ版) {#data-service-beta}

TiDB Cloud [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)は、バックエンド アプリケーション開発を簡素化し、開発者が高度にスケーラブルで安全なデータ駆動型アプリケーションを迅速に構築できるようにする、完全に管理されたローコードのバックエンド サービス ソリューションです。

データ サービスを使用すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でTiDB Cloudデータにアクセスできます。この機能は、サーバーレスアーキテクチャを使用してコンピューティング リソースと柔軟なスケーリングを処理するため、インフラストラクチャやメンテナンスのコストを気にすることなく、エンドポイントのクエリ ロジックに集中できます。

詳細については[TiDB Cloudデータ サービス (ベータ版) の概要](/tidb-cloud/data-service-overview.md)参照してください。

## データアプリ {#data-app}

[データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)のデータ アプリは、特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのコレクションです。データ アプリを作成すると、エンドポイントをグループ化し、API キーを使用して承認設定を構成し、エンドポイントへのアクセスを制限できます。これにより、承認されたユーザーのみがデータにアクセスして操作できるようにすることができ、アプリケーションのセキュリティが強化されます。

詳細については[データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)参照してください。

## データアプリエンドポイント {#data-app-endpoints}

[データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)のエンドポイントは、SQL ステートメントを実行するためにカスタマイズできる Web API です。3 句で使用される値など、SQL ステートメントのパラメーターを指定できます。クライアントがエンドポイントを呼び出し、要求 URL でパラメーターの値を提供すると、エンドポイントは`WHERE`されたパラメーターを使用して対応する SQL ステートメントを実行し、結果を HTTP 応答の一部として返します。

詳細については[エンドポイントの管理](/tidb-cloud/data-service-manage-endpoint.md)参照してください。

## チャット2クエリAPI {#chat2query-api}

TiDB Cloudでは、Chat2Query API は、指示を与えることで AI を使用して SQL ステートメントを生成および実行できる RESTful インターフェースです。その後、API がクエリ結果を返します。

詳細については[Chat2Query APIを使い始める](/tidb-cloud/use-chat2query-api.md)参照してください。

## AI統合 {#ai-integrations}

サードパーティ ツールをデータ アプリに統合すると、サードパーティ ツールが提供する高度な自然言語処理機能と人工知能 (AI) 機能によってアプリケーションが強化されます。この統合により、アプリケーションはより複雑なタスクを実行し、インテリジェントなソリューションを提供できるようになります。

現在、GPT や Dify などのサードパーティ ツールをTiDB Cloudコンソールに統合できます。

詳細については[データアプリをサードパーティツールと統合する](/tidb-cloud/data-service-integrations.md)参照してください。

## コードとしてのコンフィグレーション {#configuration-as-code}

TiDB Cloud は、 JSON 構文を使用してデータ アプリの構成全体をコードとして表現するコンフィグレーション as Code (CaC) アプローチを提供します。

データ アプリを GitHub に接続することで、 TiDB Cloud はCaC アプローチを使用して、データ アプリの構成を[設定ファイル](/tidb-cloud/data-service-app-config-files.md)として優先 GitHub リポジトリとブランチにプッシュできます。

GitHub 接続で自動同期とデプロイメントが有効になっている場合は、GitHub 上の構成ファイルを更新してデータ アプリを変更することもできます。構成ファイルの変更を GitHub にプッシュすると、新しい構成がTiDB Cloudに自動的にデプロイされます。

詳細については[GitHub でデータ アプリを自動的にデプロイ](/tidb-cloud/data-service-manage-github-connection.md)参照してください。
