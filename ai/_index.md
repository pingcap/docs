---
title: TiDB for AI
summary: TiDB の統合されたベクトル検索、フルテキスト検索、シームレスな Python SDK を使用して、最新の AI アプリケーションを構築します。
---

# AI向けTiDB {#tidb-for-ai}

TiDBは、最新のAIアプリケーション向けに設計された分散SQLデータベースで、統合されたベクトル検索、全文検索、ハイブリッド検索機能を備えています。このドキュメントでは、TiDBを使用してAIを活用したアプリケーションを構築するために利用できるAI機能とツールの概要を説明します。

## クイックスタート {#quick-start}

TiDB の AI 機能をすぐに利用できるようになります。

| 書類                                          | 説明                                           |
| ------------------------------------------- | -------------------------------------------- |
| [Pythonを始めよう](/ai/quickstart-via-python.md) | Python を使用して、TiDB で最初の AI アプリケーションを数分で構築します。 |
| [SQLを始めよう](/ai/quickstart-via-sql.md)       | SQL を使用したベクター検索のクイック スタート ガイド。               |

## 概念 {#concepts}

TiDB の AI を活用した検索の背後にある基本的な概念を理解します。

| 書類                                               | 説明                          |
| ------------------------------------------------ | --------------------------- |
| [ベクトル検索](/ai/concepts/vector-search-overview.md) | ベクター検索の概念、仕組み、使用例など、包括的な概要。 |

## ガイド {#guides}

[`pytidb`](https://github.com/pingcap/pytidb) SDK または SQL を使用して TiDB で AI アプリケーションを構築するためのステップ バイ ステップ ガイド。

| 書類                                                          | 説明                                              |
| ----------------------------------------------------------- | ----------------------------------------------- |
| [TiDBに接続する](/ai/guides/connect.md)                          | `pytidb`を使用してTiDB Cloudまたはセルフマネージド クラスターに接続します。 |
| [表の操作](/ai/guides/tables.md)                                | ベクトル フィールドを使用してテーブルを作成、クエリ、および管理します。            |
| [ベクトル検索](/ai/guides/vector-search.md)                       | `pytidb`を使用して意味的類似性検索を実行します。                    |
| [全文検索](/ai/guides/vector-search-full-text-search-python.md) | BM25 ランキングによるキーワードベースのテキスト検索。                   |
| [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)       | より良い結果を得るために、ベクトル検索と全文検索を組み合わせます。               |
| [画像検索](/ai/guides/image-search.md)                          | マルチモーダル埋め込みを使用して画像を検索します。                       |
| [自動埋め込み](/ai/guides/auto-embedding.md)                      | データ挿入時に埋め込みを自動的に生成します。                          |
| [フィルタリング](/ai/guides/filtering.md)                          | メタデータ条件で検索結果をフィルタリングします。                        |

## 例 {#examples}

TiDB の AI 機能を紹介する完全なコード例とデモ。

| 書類                                                  | 説明                          |
| --------------------------------------------------- | --------------------------- |
| [基本的なCRUD操作](/ai/examples/basic-with-pytidb.md)     | `pytidb`を使用した基本的なテーブル操作。    |
| [ベクトル検索](/ai/examples/vector-search-with-pytidb.md) | 意味的類似性検索の例。                 |
| [RAG アプリケーション](/ai/examples/rag-with-pytidb.md)     | 検索拡張生成アプリケーションを構築します。       |
| [画像検索](/ai/examples/image-search-with-pytidb.md)    | Jina AI 埋め込みによるマルチモーダル画像検索。 |
| [会話記憶](/ai/examples/memory-with-pytidb.md)          | AI エージェントとチャットボットの永続メモリ。    |
| [テキストからSQLへ](/ai/examples/text2sql-with-pytidb.md)  | 自然言語を SQL クエリに変換します。        |

## 統合 {#integrations}

TiDB を一般的な AI フレームワーク、埋め込みプロバイダー、開発ツールと統合します。

| 書類                                                                                                      | 説明                                               |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| [統合の概要](/ai/integrations/vector-search-integration-overview.md)                                         | 利用可能なすべての統合の概要。                                  |
| [埋め込みプロバイダー](/ai/integrations/vector-search-auto-embedding-overview.md#available-text-embedding-models) | OpenAI、Cohere、Jina AI などの統合インターフェース。             |
| [ランチェーン](/ai/integrations/vector-search-integrate-with-langchain.md)                                    | LangChain で TiDB をベクトル ストアとして使用します。              |
| [ラマインデックス](/ai/integrations/vector-search-integrate-with-llamaindex.md)                                 | LlamaIndex を備えたベクター ストアとして TiDB を使用します。          |
| [MCP サーバー](/ai/integrations/tidb-mcp-server.md)                                                         | TiDB を Claude Code、Cursor、その他の AI 搭載 IDE に接続します。 |

## 参照 {#reference}

TiDB の AI およびベクトル検索機能に関する技術リファレンス ドキュメント。

| 書類                                                               | 説明                                   |
| ---------------------------------------------------------------- | ------------------------------------ |
| [ベクトルデータ型](/ai/reference/vector-search-data-types.md)            | ベクトル列の種類と使用法。                        |
| [関数と演算子](/ai/reference/vector-search-functions-and-operators.md) | 距離関数とベクトル演算。                         |
| [ベクター検索インデックス](/ai/reference/vector-search-index.md)             | パフォーマンス向上のためにベクター インデックスを作成および管理します。 |
| [性能チューニング](/ai/reference/vector-search-improve-performance.md)   | ベクトル検索パフォーマンスを最適化します。                |
| [制限事項](/ai/reference/vector-search-limitations.md)               | 現在の制限と制約。                            |
