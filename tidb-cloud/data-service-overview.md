---
title: TiDB Cloud Data Service (Beta) Overview
summary: Learn about Data Service in TiDB Cloud and its scenarios.
---

# TiDB Cloudデータ サービス (ベータ版) の概要 {#tidb-cloud-data-service-beta-overview}

TiDB Cloud [データサービス（ベータ版）](https://tidbcloud.com/console/data-service)は、バックエンド アプリケーション開発を簡素化し、開発者が拡張性の高い安全なデータ駆動型アプリケーションを迅速に構築できるようにする、フルマネージドのローコードのサービスとしてのバックエンド ソリューションです。

Data Service を使用すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でTiDB Cloudデータにアクセスできます。この機能は、サーバーレスアーキテクチャを使用してコンピューティング リソースと柔軟なスケーリングを処理するため、インフラストラクチャやメンテナンスのコストを心配することなく、エンドポイントのクエリ ロジックに集中できます。

> **注記：**
>
> データサービスは[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターに対して利用可能です。 TiDB 専用クラスターでデータ サービスを使用するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

Data Service のエンドポイントは、SQL ステートメントを実行するようにカスタマイズできる Web API です。 `WHERE`句で使用される値など、SQL ステートメントのパラメータを指定できます。クライアントがエンドポイントを呼び出し、リクエスト URL 内のパラメータの値を指定すると、エンドポイントは指定されたパラメータを使用して対応する SQL ステートメントを実行し、結果を HTTP 応答の一部として返します。

エンドポイントをより効率的に管理するには、Data Apps を使用します。 Data Service のデータ アプリは、特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのコレクションです。データ アプリを作成すると、エンドポイントをグループ化し、API キーを使用して承認設定を構成し、エンドポイントへのアクセスを制限できます。このようにして、承認されたユーザーのみがデータにアクセスして操作できるようにし、アプリケーションの安全性を高めることができます。

> **ヒント：**
>
> TiDB Cloud は、 TiDB クラスター用の Chat2Query API を提供します。有効にすると、 TiDB Cloud は**Chat2Query**と呼ばれるシステム データ アプリと Data Service に Chat2Data エンドポイントを自動的に作成します。このエンドポイントを呼び出して、AI に指示を提供して SQL ステートメントを生成および実行させることができます。
>
> 詳細については、 [Chat2Query API を使ってみる](/tidb-cloud/use-chat2query-api.md)を参照してください。

## シナリオ {#scenarios}

Data Service を使用すると、 TiDB Cloud をHTTPS と互換性のあるアプリケーションまたはサービスとシームレスに統合できます。以下に、いくつかの典型的な使用シナリオを示します。

-   モバイルまたは Web アプリケーションから TiDB クラスターのデータベースに直接アクセスします。
-   サーバーレス エッジ関数を使用してエンドポイントを呼び出し、データベース接続プーリングによって引き起こされるスケーラビリティの問題を回避します。
-   Data Service をデータ ソースとして使用して、 TiDB Cloudをデータ視覚化プロジェクトと統合します。これにより、データベース接続のユーザー名とパスワードの公開が回避され、API がより安全で使いやすくなります。
-   MySQL インターフェイスがサポートしていない環境からデータベースに接続します。これにより、データにアクセスするための柔軟性とオプションが向上します。

## 次は何ですか {#what-s-next}

-   [データサービスを始めてみる](/tidb-cloud/data-service-get-started.md)
-   [Chat2Query API を使ってみる](/tidb-cloud/use-chat2query-api.md)
-   [データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)
-   [エンドポイントの管理](/tidb-cloud/data-service-manage-endpoint.md)
