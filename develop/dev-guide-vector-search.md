---
title: Vector Search
summary: 概念、チュートリアル、統合、リファレンス ドキュメントなど、開発者向けに TiDB のベクトル検索機能を紹介します。
---

# ベクトル検索 {#vector-search}

[ベクトル検索](/ai/concepts/vector-search-overview.md)ドキュメント、画像、音声、動画など、多様なデータタイプを対象としたセマンティック類似検索を可能にします。MySQLの専門知識を活用することで、高度な検索機能を備えたスケーラブルなAIアプリケーションを構築できます。

## 始めましょう {#get-started}

TiDB ベクトル検索を開始するには、次のチュートリアルを参照してください。

-   [Pythonで始める](/ai/quickstart-via-python.md)
-   [SQL経由で開始する](/ai/quickstart-via-sql.md)

## 自動埋め込み {#auto-embedding}

自動埋め込み機能を使用すると、独自のベクターを用意することなく、プレーンテキストで直接ベクター検索を実行できます。この機能を使用すると、テキストデータを直接挿入し、テキストクエリを使用してセマンティック検索を実行できます。TiDBはバックグラウンドでテキストを自動的にベクターに変換します。

現在、TiDBはAmazon Titan、Cohere、Jina AI、OpenAI、Gemini、Hugging Face、NVIDIA NIMなど、様々な埋め込みモデルをサポートしています。ニーズに最適なモデルをお選びいただけます。詳細については、 [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)ご覧ください。

## 統合 {#integrations}

開発を加速させるために、TiDBベクトル検索を一般的なAIフレームワーク（LlamaIndexやLangChainなど）、埋め込みサービス（Jina AIなど）、ORMライブラリ（SQLAlchemy、Peewee、Django ORMなど）と統合できます。ニーズに最適なものを選択できます。

詳細については[ベクター検索統合の概要](/ai/integrations/vector-search-integration-overview.md)参照してください。

## テキスト検索 {#text-search}

意味的類似性に重点を置くベクトル検索とは異なり、全文検索では正確なキーワードでドキュメントを取得できます。

RAG シナリオでの検索品質を向上させるには、ベクトル検索とフルテキスト検索を組み合わせることができます。

| シナリオ                              | ドキュメント                                                               |
| --------------------------------- | -------------------------------------------------------------------- |
| SQL を使用してキーワードベースの検索を実行します。       | [SQLによる全文検索](/ai/guides/vector-search-full-text-search-sql.md)       |
| Python アプリケーションで全文検索を実装します。       | [Pythonによる全文検索](/ai/guides/vector-search-full-text-search-python.md) |
| より良い結果を得るために、ベクトル検索と全文検索を組み合わせます。 | [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)                |

## パフォーマンスを向上させる {#improve-performance}

ベクター検索クエリのパフォーマンスを最適化するには、ベクター インデックスの追加、インデックス構築の進行状況の監視、ディメンションの削減、ベクター列の除外、インデックスのウォームアップなどの一連のベスト プラクティスに従うことができます。

これらのベスト プラクティスの詳細については、 [ベクトル検索のパフォーマンスを向上させる](/ai/reference/vector-search-improve-performance.md)参照してください。

## 制限事項 {#limitations}

ベクトル検索を実装する前に、次の制限事項に注意してください。

-   ベクトルあたり最大16383次元
-   ベクター列は主キー、一意のインデックス、パーティション キーとして使用することはできません。
-   ベクトルと他のデータ型間の直接キャストは行いません（文字列を中間として使用します）

完全なリストについては、 [ベクトル検索の制限](/ai/reference/vector-search-limitations.md)参照してください。

## 参照 {#reference}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ベクトルインデックス](/ai/reference/vector-search-index.md)
