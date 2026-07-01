---
title: TiDB の AI Integrations
summary: Auto Embedding プロバイダー、AI フレームワーク、ORM ライブラリ、クラウドサービス、MCP サーバーサポートを含む、TiDB の AI 連携の概要。
aliases: ['/ja/tidb/stable/vector-search-integration-overview/','/ja/tidb/dev/vector-search-integration-overview/','/ja/tidbcloud/vector-search-integration-overview/']
---

# TiDB の AI Integrations

このドキュメントでは、Auto Embedding プロバイダー、AI フレームワーク、Object Relational Mapping (ORM) ライブラリ、クラウドサービス、MCP サーバーサポートを含む、TiDB の AI 連携の概要を説明します。

> **Note:**
>
> - ベクトル検索機能はベータ版です。事前の通知なく変更される場合があります。バグを見つけた場合は、GitHub で [issue](https://github.com/pingcap/tidb/issues) を報告できます。
> - ベクトル検索機能は、[TiDB Self-Managed](/overview.md)、[{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter)、および [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) で利用できます。TiDB Self-Managed と TiDB Cloud Dedicated では、TiDB バージョンが v8.4.0 以降である必要があります（v8.5.0 以降を推奨します）。

## Auto Embedding {#auto-embedding}

[Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 機能を使用すると、プレーンテキストを使って直接ベクトル検索を実行できます。TiDB がバックグラウンドで自動的にテキストをベクトルに変換するため、自分で embedding を生成または管理する必要はありません。

TiDB Vector Search は最大 16383 次元のベクトルの保存をサポートしており、ほとんどの embedding モデルに対応できます。

ベクトルの生成には、自前でデプロイしたオープンソースの embedding モデル、またはサードパーティの embedding API のいずれかを使用できます。

次の表は、サポートされている embedding プロバイダーを示しています。各プロバイダーの設定方法については、対応するガイドを参照してください。

| プロバイダー          | ガイド                                      |
|-------------------|--------------------------------------------------------------------------------------|
| OpenAI            | [OpenAI](/ai/integrations/vector-search-auto-embedding-openai.md)                    |
| OpenAI Compatible | [OpenAI Compatible](/ai/integrations/embedding-openai-compatible.md)                 |
| Jina AI           | [Jina AI](/ai/integrations/vector-search-auto-embedding-jina-ai.md)                  |
| Cohere            | [Cohere](/ai/integrations/vector-search-auto-embedding-cohere.md)                    |
| Google Gemini     | [Google Gemini](/ai/integrations/vector-search-auto-embedding-gemini.md)             |
| Hugging Face      | [Hugging Face](/ai/integrations/vector-search-auto-embedding-huggingface.md)         |
| NVIDIA NIM        | [NVIDIA NIM](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md)            |
| Amazon Titan      | [Amazon Titan](/ai/integrations/vector-search-auto-embedding-amazon-titan.md)        |

## AI フレームワーク {#ai-frameworks}

TiDB は次の AI フレームワークを公式にサポートしており、これらのフレームワークで開発した AI アプリケーションを TiDB Vector Search に簡単に統合できます。

| AI フレームワーク | チュートリアル                                                        |
|---------------|---------------------------------------------------------------------------------------------------|
| LangChain     | [Integrate Vector Search with LangChain](/ai/integrations/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [Integrate Vector Search with LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) |

また、TiDB は AI アプリケーション向けのドキュメントストレージやナレッジグラフストレージなど、さまざまな用途にも使用できます。

## ORM libraries {#orm-libraries}

TiDB Vector Search を ORM ライブラリと統合して、TiDB データベースを操作できます。

次の表は、サポートされている ORM ライブラリと対応する統合チュートリアルを示しています。

| 言語    | ORM/クライアント       | インストール方法                    | チュートリアル |
|---------|--------------------|-----------------------------------|--------------|
| Python   | SQLAlchemy         | `pip install tidb-vector`         | [Integrate TiDB Vector Search with SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md) |
| Python   | peewee             | `pip install tidb-vector`         | [Integrate TiDB Vector Search with peewee](/ai/integrations/vector-search-integrate-with-peewee.md) |
| Python   | Django             | `pip install django-tidb[vector]` | [Integrate TiDB Vector Search with Django](/ai/integrations/vector-search-integrate-with-django-orm.md) |

## クラウドサービス {#cloud-services}

サードパーティのクラウド embedding サービスを使用してベクトルを生成し、それらを TiDB に保存できます。

次の表は、サポートされているクラウドサービスと対応するチュートリアルを示しています。

| クラウドサービス | ガイド |
|----------------|---------------------------------------------------------------------------------------------------------------------------|
| Jina AI        | [Integrate Vector Search with Jina AI Embeddings API](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md)  |
| Amazon Bedrock | [Integrate TiDB Vector Search with Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md)       |

## MCP server {#mcp-server}

[TiDB MCP Server](/ai/integrations/tidb-mcp-server.md) はオープンソースのツールであり、Model Context Protocol (MCP) を通じて自然言語の指示を使って TiDB データベースを操作できます。

次の表は、サポートされている MCP クライアントと対応するセットアップガイドを示しています。

| MCP client     | ガイド                                                                  |
|----------------|------------------------------------------------------------------------|
| Claude Code    | [Claude Code](/ai/integrations/tidb-mcp-claude-code.md)                |
| Claude Desktop | [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)          |
| Cursor         | [Cursor](/ai/integrations/tidb-mcp-cursor.md)                          |
| VS Code        | [VS Code](/ai/integrations/tidb-mcp-vscode.md)                         |
| Windsurf       | [Windsurf](/ai/integrations/tidb-mcp-windsurf.md)                      |