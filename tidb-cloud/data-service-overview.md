---
title: TiDB Cloud Data Service (Beta) Overview
summary: Learn about Data Service in TiDB Cloud and its scenarios.
---

# TiDB Cloudデータ サービス (ベータ) の概要 {#tidb-cloud-data-service-beta-overview}

TiDB Cloud は、カスタム API エンドポイントを使用して HTTPS 要求を介してTiDB Cloudデータにアクセスできるようにする[データ サービス (ベータ)](https://tidbcloud.com/console/data-service)機能を提供します。この機能は、サーバーレスアーキテクチャを使用してコンピューティング リソースとエラスティック スケーリングを処理するため、インフラストラクチャやメンテナンス コストを気にすることなく、エンドポイントのクエリ ロジックに集中できます。

> **ノート：**
>
> Data Service は[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスタのみ利用可能です。

Data Service のエンドポイントは、SQL ステートメントを実行するためにカスタマイズできる Web API です。 `WHERE`節で使用される値など、SQL ステートメントのパラメーターを指定できます。クライアントがエンドポイントを呼び出し、要求 URL のパラメーターに値を提供すると、エンドポイントは提供されたパラメーターを使用して対応する SQL ステートメントを実行し、結果を HTTP 応答の一部として返します。

エンドポイントをより効率的に管理するために、Data Apps を使用できます。 Data Service のデータ アプリは、特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのグループです。データ アプリを作成することで、エンドポイントをグループ化し、API キーを使用して承認設定を構成して、エンドポイントへのアクセスを制限できます。このようにして、許可されたユーザーのみがデータにアクセスして操作できるようにし、アプリケーションをより安全にすることができます。

> **ヒント：**
>
> TiDB Cloud は、Serverless Tierクラスター用の Chat2Query API を提供します。有効にすると、 TiDB Cloud は、 **Chat2Query**と呼ばれるシステム データ アプリと Data Service の Chat2Data エンドポイントを自動的に作成します。このエンドポイントを呼び出して、命令を提供することで AI に SQL ステートメントを生成および実行させることができます。
>
> 詳細については、 [Chat2Query API の使用を開始する](/tidb-cloud/use-chat2query-api.md)を参照してください。

## シナリオ {#scenarios}

Data Service を使用すると、HTTPS と互換性のある任意のアプリケーションまたはサービスとTiDB Cloudをシームレスに統合できます。次に、いくつかの一般的な使用シナリオを示します。

-   モバイルまたは Web アプリケーションから TiDB クラスターのデータベースに直接アクセスします。
-   サーバーレス エッジ関数を使用してエンドポイントを呼び出し、データベース接続プールによって引き起こされるスケーラビリティの問題を回避します。
-   Data Service をデータ ソースとして使用して、 TiDB Cloudをデータ視覚化プロジェクトと統合します。これにより、データベース接続のユーザー名とパスワードが公開されるのを回避し、API をより安全で使いやすくします。
-   MySQL インターフェイスがサポートしていない環境からデータベースに接続します。これにより、データにアクセスするための柔軟性とオプションが提供されます。

## 次は何ですか {#what-s-next}

-   [データ サービスを開始する](/tidb-cloud/data-service-get-started.md)
-   [Chat2Query API を使ってみる](/tidb-cloud/use-chat2query-api.md)
-   [データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)
-   [エンドポイントを管理する](/tidb-cloud/data-service-manage-endpoint.md)
