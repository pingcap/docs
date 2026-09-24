---
title: TiDB for AI
summary: SQL、統合検索、TiDB Cloud Starter、および永続的な共有 file systems を使用して、TiDB で AI アプリケーションとエージェントワークフローを構築します。
---

# AI向けTiDB {#tidb-for-ai}

TiDBは、AIアプリケーションの構築とAIエージェントワークフローの実行のためのデータ機能とワークスペース機能を提供します。

- アプリケーション開発では、SQL または [TiDB AI 向け Python SDK (`pytidb`)](https://github.com/pingcap/pytidb) を使用して、構造化データ、ベクトル検索、全文検索、ハイブリッド検索、および AI を活用した検索取得を利用できます。
- AI エージェントと自動化では、[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) を使用して TiDB Cloud Starter インスタンスと SQL ワークフローを管理し、[TiDB Cloud Filesystem](/tidb-cloud-filesystem/_index.md) をローカルマシン、CI ジョブ、一時的なエージェントサンドボックス間で永続的な共有ストレージとして使用できます。TiDB Cloud Filesystem は、マウントされたワークスペース、Git ワークフロー、ジャーナル、および委任されたシークレットも提供します。

## はじめに {#get-started}

構築したいものに応じて、開始する方法を選択してください。

| 目標 | まずはこちら |
| --- | --- |
| ベクトル検索を使用した AI アプリケーションを構築する | [Python によるベクトル検索のクイックスタート](/ai/quickstart-via-python.md) または [SQL によるベクトル検索のクイックスタート](/ai/quickstart-via-sql.md) |
| TiDB Cloud を使用してエージェントおよび自動化ワークフローを構築する | [TiDB Cloud CLI のクイックスタート](/ai/ti/ti-quick-start.md) |

## TiDB で AI アプリケーションを構築する {#build-ai-applications-with-tidb}

[`pytidb`](https://github.com/pingcap/pytidb) SDK または SQL を使用して TiDB に接続し、データを検索および取得して、AI を活用したアプリケーションを構築できます。

### TiDB に接続する {#connect-to-tidb}

| ドキュメント | 説明 |
| --- | --- |
| [Python で TiDB に接続する](/ai/guides/connect.md) | `pytidb` を使用して TiDB Cloud または TiDB Self-Managed に接続します。 |

### 検索と取得 {#search-retrieval}

#### ベクトル検索 {#vector-search}

| ドキュメント | 説明 |
| --- | --- |
| [ベクトル検索の概要](/ai/guides/vector-search-overview.md) | 概念、仕組み、ユースケースを含む、ベクトル検索の包括的な概要。 |
| [ベクトル検索ガイド](/ai/guides/vector-search.md) | `pytidb` を使用してセマンティック類似検索を実行します。 |
| [ベクトル検索の例](/ai/guides/vector-search-with-pytidb.md) | `pytidb` を使用したセマンティック類似検索の例。 |

#### 全文検索 {#full-text-search}

| ドキュメント | 説明 |
| --- | --- |
| [Python による全文検索](/ai/guides/vector-search-full-text-search-python.md) | `pytidb` を使用した BM25 ランキングによるキーワードベースのテキスト検索。 |
| [SQL による全文検索](/ai/guides/vector-search-full-text-search-sql.md) | SQL を使用した BM25 ランキングによるキーワードベースのテキスト検索。 |
| [全文検索の例](/ai/guides/fulltext-search-with-pytidb.md) | `pytidb` を使用した全文検索の例。 |

#### ハイブリッド検索 {#hybrid-search}

| ドキュメント | 説明 |
| --- | --- |
| [ハイブリッド検索ガイド](/ai/guides/vector-search-hybrid-search.md) | ベクトル検索と全文検索を組み合わせて、より良い結果を得ます。 |
| [ハイブリッド検索の例](/ai/guides/hybrid-search-with-pytidb.md) | `pytidb` を使用したハイブリッド検索の例。 |

#### 自動埋め込み {#auto-embeddings}

| ドキュメント | 説明 |
| --- | --- |
| [自動埋め込みガイド](/ai/guides/auto-embedding.md) | データ挿入時に埋め込みを自動的に生成します。 |
| [自動埋め込みの例](/ai/guides/auto-embedding-with-pytidb.md) | `pytidb` を使用した自動埋め込みの例。 |

#### 画像検索 {#image-search}

| ドキュメント | 説明 |
| --- | --- |
| [画像検索ガイド](/ai/guides/image-search.md) | マルチモーダル埋め込みを使用して画像を検索します。 |
| [画像検索の例](/ai/guides/image-search-with-pytidb.md) | Jina AI埋め込みを使用したマルチモーダル画像検索の例。 |

#### リランキング {#reranking}

| ドキュメント | 説明 |
| --- | --- |
| [再ランキング](/ai/guides/reranking.md) | 検索結果をリランキングして関連性を向上させます。 |

### データを操作する {#work-with-data}

| ドキュメント | 説明 |
| --- | --- |
| [表の操作](/ai/guides/tables.md) | ベクトルフィールドを持つテーブルを作成、クエリ、管理します。 |
| [フィルタリング](/ai/guides/filtering.md) | メタデータ条件で検索結果をフィルタリングします。 |
| [結合クエリ](/ai/guides/join-queries.md) | テーブル間で結合クエリを実行します。 |
| [生のSQLクエリ](/ai/guides/raw-queries.md) | 生のSQLクエリを直接実行します。 |
| [トランザクション](/ai/guides/transactions.md) | データ整合性のためにトランザクションを使用します。 |

### アプリケーション例 {#application-examples}

| ドキュメント | 説明 |
| --- | --- |
| [RAGの例](/ai/guides/rag-with-pytidb.md) | Retrieval-Augmented Generation アプリケーションを構築します。 |
| [会話メモリの例](/ai/guides/memory-with-pytidb.md) | AIエージェントやチャットボット向けの永続メモリ。 |
| [Text-to-SQLの例](/ai/guides/text2sql-with-pytidb.md) | 自然言語をSQLクエリに変換します。 |

## TiDB Cloud CLI でエージェントと自動化ワークフローを構築する {#build-agent-and-automation-workflows-with-tidb-cloud-cli}

TiDB Cloud CLI (`ti`) を使用すると、ユーザー、スクリプト、CIジョブ、AIエージェントがターミナルから TiDB Cloud を管理できます。これを使用して TiDB Cloud Starter と SQL 操作を自動化したり、それらを使用するマシンやサンドボックスとは独立してファイルやワークスペースを利用可能な状態に保ったりできます。

| やりたいこと | まずはこちら |
| --- | --- |
| `ti` が管理する対象と使用するタイミングを理解する | [TiDB Cloud CLI の概要](/ai/ti/ti-overview.md) |
| `ti` をインストールして設定し、最初のワークフローを完了する | [TiDB Cloud CLI を使い始める](/ai/ti/ti-quick-start.md) |
| TiDB Cloud Starter インスタンス、ブランチ、SQL 操作を自動化する | [TiDB Cloud Starter インスタンスを管理する](/ai/ti/guides/manage-starter-instances.md) |
| マシン、CIジョブ、サンドボックス間でファイルを永続化して共有する | [TiDB Cloud CLI で TiDB Cloud Filesystem を使用する](/ai/ti/guides/manage-filesystems-via-cli.md) |
| マウントされたワークスペース、Git ワークスペース、ジャーナル、または委任されたシークレットを使用する | [ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md)、[Git ワークスペースを管理する](/tidb-cloud-filesystem/manage-git-workspaces.md)、[ファイルシステム内のジャーナルを使用する](/tidb-cloud-filesystem/use-filesystem-journals.md)、および [ファイルシステムの Vault シークレットを管理する](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md) |
| エンドツーエンドの自動化またはエージェントの例をたどる | [日次の TiDB Cloud CLI ワークフローを実行する](/ai/ti/guides/ti-daily-workflow-example.md) または [エージェントサンドボックスで TiDB Cloud Filesystem を使用する](/ai/ti/guides/ti-agent-sandbox-example.md) |
| コマンド、グローバルオプション、出力動作、エラーを調べる | [TiDB Cloud CLI コマンドリファレンス](/ai/ti/reference/ti-cli-reference.md) |

## 統合 {#integrations}

TiDBを、埋め込みプロバイダー、AIフレームワーク、アプリケーションライブラリ、クラウドサービス、AI開発ツールに接続します。

| 統合領域                                                                                                      | まずはこちら |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| すべての統合 | [TiDB 向け AI 統合](/ai/integrations/vector-search-integration-overview.md) |
| 自動埋め込みプロバイダー | [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md) |
| AIフレームワーク | [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) |
| ORMライブラリ | [SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md), [Django ORM](/ai/integrations/vector-search-integrate-with-django-orm.md), and [Peewee](/ai/integrations/vector-search-integrate-with-peewee.md) |
| クラウド埋め込みサービス | [Jina AI Embedding](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md) and [Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md) |
| MCPクライアントとAI開発ツール | [TiDB MCP Server](/ai/integrations/tidb-mcp-server.md) |

## 参照 {#reference}

TiDBのAIおよびベクトル検索機能に関する技術リファレンスドキュメント。

| ドキュメント                                                               | 説明                                   |
| ---------------------------------------------------------------- | ------------------------------------ |
| [ベクトルデータ型](/ai/reference/vector-search-data-types.md)            | ベクトル列の型と使用方法。                        |
| [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md) | 距離関数とベクトル演算。                         |
| [ベクトル検索インデックス](/ai/reference/vector-search-index.md)             | パフォーマンス向上のために、ベクトルインデックスを作成および管理します。 |
| [ベクトル検索の性能チューニング](/ai/reference/vector-search-improve-performance.md)   | ベクトル検索のパフォーマンスを最適化します。               |
| [ベクトル検索の制限事項](/ai/reference/vector-search-limitations.md)               | 現在の制約と制限。                            |
