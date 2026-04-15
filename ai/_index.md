---
title: TiDB for AI
summary: TiDBの統合されたベクトル検索、全文検索、そしてシームレスなPython SDKを活用して、最新のAIアプリケーションを構築しましょう。
---

# AI向けTiDB {#tidb-for-ai}

TiDBは、最新のAIアプリケーション向けに設計された分散型SQLデータベースであり、統合されたベクトル検索、全文検索、およびハイブリッド検索機能を提供します。このドキュメントでは、TiDBを使用してAI搭載アプリケーションを構築するために利用できるAI機能とツールについて概説します。

## クイックスタート {#quick-start}

TiDBのAI機能を活用して、すぐに運用を開始しましょう。

| 書類                                          | 説明                                           |
| ------------------------------------------- | -------------------------------------------- |
| [Pythonを始めよう](/ai/quickstart-via-python.md) | TiDBとPythonを使って、わずか数分で最初のAIアプリケーションを構築しましょう。 |
| [SQL入門](/ai/quickstart-via-sql.md)          | SQLを使用したベクター検索のクイックスタートガイド。                  |

## 概念 {#concepts}

TiDBにおけるAIを活用した検索の背後にある基礎概念を理解する。

| 書類                                               | 説明                                |
| ------------------------------------------------ | --------------------------------- |
| [ベクトル検索](/ai/concepts/vector-search-overview.md) | ベクトル検索の概念、仕組み、使用例など、包括的な概要を解説します。 |

## ガイド {#guides}

[`pytidb`](https://github.com/pingcap/pytidb) SDKまたはSQLを使用してTiDBでAIアプリケーションを構築するためのステップバイステップガイド。

| 書類                                                          | 説明                                                   |
| ----------------------------------------------------------- | ---------------------------------------------------- |
| [TiDBに接続する](/ai/guides/connect.md)                          | `pytidb`を使用してTiDB Cloudまたは TiDB Self-Managed に接続します。 |
| [テーブルの操作](/ai/guides/tables.md)                             | ベクトルフィールドを使用してテーブルを作成、クエリ、管理します。                     |
| [ベクトル検索](/ai/guides/vector-search.md)                       | `pytidb`を使用して意味的類似性検索を実行します。                         |
| [全文検索](/ai/guides/vector-search-full-text-search-python.md) | BM25ランキングを用いたキーワードベースのテキスト検索。                        |
| [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)       | より良い結果を得るために、ベクトル検索と全文検索を組み合わせましょう。                  |
| [画像検索](/ai/guides/image-search.md)                          | マルチモーダル埋め込みを使用して画像を検索する。                             |
| [自動埋め込み](/ai/guides/auto-embedding.md)                      | データ挿入時に埋め込みを自動的に生成する。                                |
| [フィルタリング](/ai/guides/filtering.md)                          | メタデータ条件で検索結果を絞り込む。                                   |

## 例 {#examples}

TiDBのAI機能を紹介する、完全なコード例とデモ。

| 書類                                                    | 説明                           |
| ----------------------------------------------------- | ---------------------------- |
| [基本的なCRUD操作](/ai/examples/basic-with-pytidb.md)       | `pytidb`を使用した基本的なテーブル操作。     |
| [ベクトル検索](/ai/examples/vector-search-with-pytidb.md)   | 意味的類似性検索の例。                  |
| [RAGアプリケーション](/ai/examples/rag-with-pytidb.md)        | 検索拡張型生成アプリケーションを構築する。        |
| [画像検索](/ai/examples/image-search-with-pytidb.md)      | Jina AI埋め込みを用いたマルチモーダル画像検索。  |
| [会話記憶](/ai/examples/memory-with-pytidb.md)            | AIエージェントおよびチャットボットのための永続メモリ。 |
| [テキストからSQLへの変換](/ai/examples/text2sql-with-pytidb.md) | 自然言語をSQLクエリに変換する。            |

## 統合 {#integrations}

TiDBを、人気のAIフレームワーク、組み込みプロバイダー、開発ツールと統合します。

| 書類                                                                                                      | 説明                                         |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| [統合の概要](/ai/integrations/vector-search-integration-overview.md)                                         | 利用可能なすべての連携機能の概要。                          |
| [埋め込みプロバイダー](/ai/integrations/vector-search-auto-embedding-overview.md#available-text-embedding-models) | OpenAI、Cohere、Jina AIなどに対応した統合インターフェース。    |
| [ラングチェーン](/ai/integrations/vector-search-integrate-with-langchain.md)                                   | LangChainでTiDBをベクトルストアとして使用する。             |
| [ラマインデックス](/ai/integrations/vector-search-integrate-with-llamaindex.md)                                 | TiDBをLlamaIndexを使用したベクターストアとして利用する。        |
| [MCPサーバー](/ai/integrations/tidb-mcp-server.md)                                                          | TiDBをClaude Code、Cursor、その他のAI搭載IDEに接続します。 |

## 参照 {#reference}

TiDBのAIおよびベクトル検索機能に関する技術リファレンスドキュメント。

| 書類                                                               | 説明                                   |
| ---------------------------------------------------------------- | ------------------------------------ |
| [ベクトルデータ型](/ai/reference/vector-search-data-types.md)            | ベクトル列の型と使用方法。                        |
| [関数と演算子](/ai/reference/vector-search-functions-and-operators.md) | 距離関数とベクトル演算。                         |
| [ベクトル検索インデックス](/ai/reference/vector-search-index.md)             | パフォーマンス向上のために、ベクターインデックスを作成および管理します。 |
| [性能チューニング](/ai/reference/vector-search-improve-performance.md)   | ベクトル検索のパフォーマンスを最適化します。               |
| [制限事項](/ai/reference/vector-search-limitations.md)               | 現在の制約と制限。                            |
