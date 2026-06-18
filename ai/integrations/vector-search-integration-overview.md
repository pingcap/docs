---
title: AI Integrations for TiDB
summary: Auto Embedding プロバイダー、AI フレームワーク、ORM ライブラリ、クラウドサービス、MCP サーバーのサポートなど、TiDB の AI 統合の概要。
aliases: ['/ja/tidb/stable/vector-search-integration-overview/','/ja/tidb/dev/vector-search-integration-overview/','/ja/tidbcloud/vector-search-integration-overview/']
---

# AI Integrations for TiDB

このドキュメントでは、Auto Embedding プロバイダー、AI フレームワーク、オブジェクト リレーショナル マッピング (ORM) ライブラリ、クラウドサービス、MCP サーバーのサポートなど、TiDB の AI 統合の概要について説明します。

> **注記：**
>
> -   ベクトル検索機能はベータ版です。予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。
> -   ベクトル検索機能は[TiDBセルフマネージド](/overview.md) 、 [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential) 、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用可能です。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## Auto Embedding {#auto-embedding}

[Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 機能を使用すると、プレーンテキストを使って直接ベクトル検索を実行できます。TiDB はバックグラウンドでテキストを自動的にベクトルに変換するため、自分で埋め込みを生成または管理する必要はありません。

TiDB Vector Search supports storing vectors of up to 16383 dimensions, which accommodates most embedding models.

You can use either self-deployed open-source embedding models or third-party embedding APIs to generate vectors.

The following table lists the supported embedding providers. For details on how to configure each provider, see the corresponding guide.

| Provider          | Guide                                                                                |
|-------------------|--------------------------------------------------------------------------------------|
| OpenAI            | [OpenAI](/ai/integrations/vector-search-auto-embedding-openai.md)                    |
| OpenAI Compatible | [OpenAI Compatible](/ai/integrations/embedding-openai-compatible.md)                 |
| Jina AI           | [Jina AI](/ai/integrations/vector-search-auto-embedding-jina-ai.md)                  |
| Cohere            | [Cohere](/ai/integrations/vector-search-auto-embedding-cohere.md)                    |
| Google Gemini     | [Google Gemini](/ai/integrations/vector-search-auto-embedding-gemini.md)             |
| Hugging Face      | [Hugging Face](/ai/integrations/vector-search-auto-embedding-huggingface.md)         |
| NVIDIA NIM        | [NVIDIA NIM](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md)            |
| Amazon Titan      | [Amazon Titan](/ai/integrations/vector-search-auto-embedding-amazon-titan.md)        |

## ORM libraries {#orm-libraries}

TiDB Vector Search を ORM ライブラリと統合して、TiDB データベースと対話することができます。

次の表に、サポートされている ORM ライブラリと対応する統合チュートリアルを示します。

| 言語   | ORM/クライアント      | インストール方法                          | チュートリアル                                                                                   |
| ---- | --------------- | --------------------------------- | ----------------------------------------------------------------------------------------- |
| Python | SQLAlchemy        | `pip install tidb-vector`         | [TiDBベクトル検索をSQLAlchemyと統合する](/ai/integrations/vector-search-integrate-with-sqlalchemy.md) |
| Python | peewee           | `pip install tidb-vector`         | [TiDBベクトル検索をpeeweeと統合する](/ai/integrations/vector-search-integrate-with-peewee.md)         |
| Python | Django            | `pip install django-tidb[vector]` | [TiDBベクトル検索をDjangoに統合する](/ai/integrations/vector-search-integrate-with-django-orm.md)     |

## AIフレームワーク

TiDB は以下の AI フレームワークを公式にサポートしており、これらのフレームワークを使用して開発された AI アプリケーションを TiDB Vector Search に簡単に統合できます。

| AI framework | Tutorial                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------|
| LangChain     | [Integrate Vector Search with LangChain](/ai/integrations/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [Integrate Vector Search with LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) |

また、TiDB は、ドキュメントのstorageや AI アプリケーションのナレッジ グラフのstorageなど、さまざまなタスクにも使用できます。

## Cloud services

サードパーティのクラウド埋め込みサービスを使用してベクトルを生成し、TiDB に保存できます。

次の表に、サポートされているクラウドサービスと対応するチュートリアルを示します。

| Cloud service  | Tutorial                                                                                                                  |
|----------------|---------------------------------------------------------------------------------------------------------------------------|
| Jina AI        | [Integrate Vector Search with Jina AI Embeddings API](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md)  |
| Amazon Bedrock | [Integrate TiDB Vector Search with Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md)       |

## MCP server

[TiDB MCP Server](/ai/integrations/tidb-mcp-server.md) は、Model Context Protocol (MCP) を通じて自然言語の指示を使用して TiDB データベースを操作できるオープンソースツールです。

次の表に、サポートされている MCP クライアントと対応するセットアップガイドを示します。

| MCP client     | Guide                                                                  |
|----------------|------------------------------------------------------------------------|
| Claude Code    | [Claude Code](/ai/integrations/tidb-mcp-claude-code.md)                |
| Claude Desktop | [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)          |
| Cursor         | [Cursor](/ai/integrations/tidb-mcp-cursor.md)                          |
| VS Code        | [VS Code](/ai/integrations/tidb-mcp-vscode.md)                         |
| Windsurf       | [Windsurf](/ai/integrations/tidb-mcp-windsurf.md)                      |
