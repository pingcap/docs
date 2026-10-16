---
title: 全文検索
summary: PostgreSQL 互換の TiDB Cloud Starter で全文検索を使用する方法を学びます。
---

# 全文検索

PostgreSQL 互換の {{{ .starter }}} は、`tsvector`、`tsquery`、言語固有のトークナイザー、ランキング関数、GIN インデックスを使用した PostgreSQL 互換の全文検索をサポートしています。

> **Note:**
>
> PostgreSQL 互換の {{{ .starter }}} は現在パブリックプレビューです。

全文検索は組み込み機能であり、別途拡張機能をインストールする必要はありません。中国語のトークン化も、`zhparser` 互換の設定を通じて利用できます。

## サポートされるテキスト検索設定 {#supported-text-search-configurations}

以下のテキスト検索設定がサポートされています。

| 設定 | エイリアス | 説明 |
| --- | --- | --- |
| `jieba` | `chinese`, `zhparser` | 中国語の単語分割。 |
| `chinese_ngram` | `zhparser_ngram` | 複数字の単語に対してバイグラムを重ねて適用する中国語の単語分割。 |
| `simple` | - | 英語およびラテン文字テキスト向けの空白ベースのトークン化。ステミングやストップワードの除去は行いません。 |
| `english` | - | 最小限のストップワードリストを使用する空白ベースのトークン化。ステミングは行いません。 |
| `english_stem` | - | PostgreSQL 互換の英語ストップワードを使用する English Snowball ステミング。 |

デフォルトのテキスト検索設定は `simple` です。

現在のデフォルト設定は、次のように確認できます。

```sql
SHOW default_text_search_config;
```

> **Note:**
>
> PostgreSQL とは異なり、`english` 設定ではステミングは行われません。英語のステミング検索が必要な場合は `english_stem` を使用してください。

## 全文検索用の GIN インデックスを作成する {#create-a-gin-index-for-full-text-search}

GIN インデックスを使用すると、全文検索クエリを高速化できます。

`tsvector` カラムに GIN インデックスを作成します。

```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    tsv TSVECTOR
);

CREATE INDEX idx_documents_tsv
ON documents
USING GIN (tsv);
```

GIN の式インデックスを作成することもできます。

```sql
CREATE INDEX idx_documents_content_fts
ON documents
USING GIN (to_tsvector('simple', content));
```

`@@` 演算子で使用される式がインデックス化された式と一致する場合、オプティマイザは自動的に GIN インデックスを使用できます。

## 英語テキストを検索する {#search-english-text}

厳密なトークン一致には `simple` を使用します。

次のクエリは、前のセクションで作成した GIN 式インデックスを使用できます。これは同じ `to_tsvector('simple', content)` 式を使用しているためです。

```sql
SELECT *
FROM documents
WHERE to_tsvector('simple', content)
      @@ to_tsquery('simple', 'database');
```

ステミングとストップワード除去が必要な場合は `english_stem` を使用します。

```sql
CREATE INDEX idx_documents_english
ON documents
USING GIN (to_tsvector('english_stem', content));

SELECT *
FROM documents
WHERE to_tsvector('english_stem', content)
      @@ plainto_tsquery('english_stem', 'running');
```

インデックス式と検索クエリでは、同じテキスト検索設定を使用してください。

## 中国語テキストを検索する {#search-chinese-text}

中国語のトークン化には `jieba` 設定を使用します。

例:

```sql
CREATE INDEX idx_documents_chinese
ON documents
USING GIN (to_tsvector('jieba', content));

SELECT *
FROM documents
WHERE to_tsvector('jieba', content)
      @@ plainto_tsquery('jieba', '数据库');
```

エイリアス `chinese` と `zhparser` は、同じ中国語トークン化機能を使用します。

## クエリ関数 {#query-functions}

PostgreSQL 互換の {{{ .starter }}} は、一般的な PostgreSQL のテキスト検索クエリ関数をサポートしています。

| 関数 | 説明 | 例 |
| --- | --- | --- |
| `plainto_tsquery` | プレーンテキストをテキスト検索クエリに変換します。 | `plainto_tsquery('simple', 'database search')` |
| `to_tsquery` | PostgreSQL のテキスト検索演算子を使用してクエリを作成します。 | `to_tsquery('simple', 'database & search')` |
| `phraseto_tsquery` | フレーズクエリを作成します。 | `phraseto_tsquery('simple', 'hello world')` |
| `websearch_to_tsquery` | Web 検索スタイルの構文を使用してクエリを作成します。 | `websearch_to_tsquery('simple', '"exact phrase" -exclude')` |

## ブール検索 {#boolean-search}

ブール検索式には `to_tsquery()` を使用します。

```sql
-- AND
SELECT *
FROM documents
WHERE tsv @@ to_tsquery('simple', 'database & performance');

-- OR
SELECT *
FROM documents
WHERE tsv @@ to_tsquery('simple', 'postgres | mysql');

-- NOT
SELECT *
FROM documents
WHERE tsv @@ to_tsquery('simple', 'database & !oracle');
```

## 検索結果をランク付けする {#rank-search-results}

一致したドキュメントをランク付けするには `ts_rank()` を使用します。

例:

```sql
SELECT
    content,
    ts_rank(
        to_tsvector('jieba', content),
        plainto_tsquery('jieba', '数据库')
    ) AS rank
FROM documents
WHERE to_tsvector('jieba', content)
      @@ plainto_tsquery('jieba', '数据库')
ORDER BY rank DESC
LIMIT 10;
```

## 重み付きで検索する {#search-with-weights}

異なるフィールドに異なる重みを割り当てるには `setweight()` を使用します。

例:

```sql
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    tsv TSVECTOR
);

UPDATE articles
SET tsv =
    setweight(to_tsvector('jieba', title), 'A') ||
    setweight(to_tsvector('jieba', body), 'B');

WITH q AS (
    SELECT plainto_tsquery('jieba', '数据库') AS query
)
SELECT
    a.title,
    ts_rank(a.tsv, q.query) AS rank
FROM articles AS a, q
WHERE a.tsv @@ q.query
ORDER BY rank DESC;
```

## 制限事項 {#limitations}

パブリックプレビュー期間中は、以下の制限が適用されます。

- [サポートされるテキスト検索設定](#supported-text-search-configurations) に記載されているテキスト検索設定のみがサポートされます。
- `english` 設定では、PostgreSQL スタイルのステミングは実行されません。英語のステミング検索を行うには、`english_stem` を使用してください。
- `:*` フラグを使用したプレフィックス一致はサポートされていません。プレフィックスフラグは無視されるため、プレフィックス検索に `to_tsquery('simple', 'data:*')` のような式を使用しないでください。
- `ts_headline()` は、中国語の漢字スクリプトの検索語をハイライトしません。中国語の検索結果でハイライトが必要な場合は、アプリケーションレイヤーでハイライトを実装してください。
- `plainto_tsquery()` のようなスカラーのテキスト検索関数は、`FROM` 句内でテーブル式として使用できません。代わりに、CTE を使用するか、クエリ内に関数を直接記述してください。
- `tsvector` 値の最大サイズは 1 MiB です。