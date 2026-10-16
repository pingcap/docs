---
title: PostgreSQL Extensions
summary: PostgreSQL 互換の TiDB Cloud Starter でサポートされる PostgreSQL 拡張機能と組み込み機能について説明します。
---

# PostgreSQL Extensions

PostgreSQL 互換の {{{ .starter }}} は、ベクトル検索、全文検索、データインポート、統合、および一般的な PostgreSQL 開発ワークフロー向けに、あらかじめ定義された PostgreSQL 拡張機能と組み込み機能のセットを提供します。

> **Note:**
>
> PostgreSQL 互換の {{{ .starter }}} は現在パブリックプレビューです。プレビュー期間中は、拡張機能の提供状況や機能が変更される可能性があります。

## サポートされる拡張機能と機能 {#supported-extensions-and-capabilities}

現在サポートされている拡張機能と機能は次のとおりです。

| 拡張機能または機能 | 説明 | 有効化 |
| --- | --- | --- |
| `vector` | pgvector 互換の `VECTOR` 型、距離演算子、類似検索、および HNSW インデックスを提供します。 | 組み込みです。`CREATE EXTENSION vector` を使用して拡張機能メタデータを登録できます。 |
| `embedding` | `embedding()` や `embed_text()` などのサーバー側テキスト埋め込み関数を提供します。 | `CREATE EXTENSION embedding` を実行します。 |
| Full-Text Search | `tsvector`、`tsquery`、ランキング関数、および GIN インデックスを使用した PostgreSQL 互換の全文検索を提供します。 | 組み込みです。 |
| Chinese tokenization (`zhparser`-compatible) | 全文検索向けの中国語トークン化を提供します。 | 組み込みで、常に利用可能です。 |
| `parquet` | サポートされる URL から Parquet データのクエリおよびインポートを可能にします。 | `CREATE EXTENSION parquet` を実行します。 |
| `http` | SQL から直接 HTTP リクエストを可能にします。HTTP 関数は拡張機能を登録しなくても利用できます。 | 組み込みです。 |
| `uuid-ossp` | `uuid_generate_v4()` などの一般的な UUID 生成関数を提供します。 | 組み込みです。`CREATE EXTENSION "uuid-ossp"` を使用して拡張機能メタデータを登録できます。 |

## 拡張機能を有効にする {#enable-an-extension}

一部の拡張機能は自動的に利用可能ですが、他の拡張機能は `CREATE EXTENSION` を使用して明示的に有効化する必要があります。

例:

```sql
CREATE EXTENSION IF NOT EXISTS embedding;
CREATE EXTENSION IF NOT EXISTS parquet;
```

`vector` 型とベクトル演算子は組み込みです。拡張機能メタデータを参照するツールや ORM との互換性のために、次のステートメントを実行して `pg_extension` に `vector` を登録することもできます。

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

現在のデータベースに登録されている拡張機能を表示するには、次を実行します。

```sql
SELECT *
FROM pg_extension;
```

## 制限事項 {#limitations}

次の制限が適用されます。

- TiDB Cloud によって明示的に提供される拡張機能と組み込み機能のみがサポートされます。
- 任意のカスタム PostgreSQL 拡張機能やサードパーティ製 PostgreSQL 拡張機能をインストールすることはできません。
- サポートされる一部の拡張機能では、upstream PostgreSQL または対応するオープンソース拡張機能で利用可能な動作の一部のみが提供されます。
- パブリックプレビュー期間中は、拡張機能の提供状況や動作が変更される可能性があります。
- パブリックプレビュー期間中は `pg_cron` のジョブスケジューリングはサポートされません。`CREATE EXTENSION pg_cron` が成功する場合でも、`cron.schedule()` などのスケジューリング関数は利用できず、スケジュールされたジョブは実行できません。`cron.job` をクエリすると空の結果が返ることがありますが、これは `pg_cron` が動作していることを意味するものではありません。