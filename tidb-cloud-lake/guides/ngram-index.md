---
title: Ngram Index
summary: Ngram インデックスは、ワイルドカード (`%`) を含む `LIKE` 演算子を使ったパターンマッチングクエリを高速化し、フルテーブルスキャンなしで高速な部分文字列検索を可能にします。
---

# Ngram Index

Ngram インデックスは、ワイルドカード (`%`) を含む `LIKE` 演算子を使ったパターンマッチングクエリを高速化し、フルテーブルスキャンなしで高速な部分文字列検索を可能にします。

## どのような問題を解決するのか？ {#what-problem-does-it-solve}

`LIKE` クエリによるパターンマッチングは、大規模データセットでは重大なパフォーマンス上の課題に直面します。

| 問題 | 影響 | Ngram インデックスによる解決策 |
|---------|--------|---------------------|
| **低速なワイルドカード検索** | `WHERE content LIKE '%keyword%'` はテーブル全体をスキャンする | n-gram セグメントを使ってデータブロックを事前に絞り込む |
| **フルテーブルスキャン** | すべてのパターン検索で全行を読み取る | パターンを含む関連データブロックのみを読み取る |
| **検索パフォーマンスの低下** | ユーザーは部分文字列検索の結果を長時間待つ | サブ秒レベルのパターンマッチング応答時間 |
| **従来のインデックスが非効率** | B-tree インデックスでは中間ワイルドカードを最適化できない | 文字レベルのインデックスにより任意のワイルドカード位置に対応 |

**例**: 1000 万件のログエントリから `'%error log%'` を検索する場合。ngram インデックスがなければ 1000 万行すべてをスキャンします。ngram インデックスがあれば、即座に約 1000 個の関連ブロックまで事前に絞り込めます。

## Ngram と Full-Text Index の比較: どちらを使うべきか？ {#ngram-vs-full-text-index-when-to-use-which}

| 機能 | Ngram Index | Full-Text Index |
|---------|-------------|-----------------|
| **主な用途** | `LIKE '%pattern%'` によるパターンマッチング | `MATCH()` を使った意味ベースのテキスト検索 |
| **検索タイプ** | 正確な部分文字列一致 | 関連度を伴う単語ベース検索 |
| **クエリ構文** | `WHERE column LIKE '%text%'` | `WHERE MATCH(column, 'text')` |
| **高度な機能** | 大文字・小文字を区別しない一致 | あいまい検索、関連度スコアリング、ブール演算子 |
| **パフォーマンスの重点** | 既存の LIKE クエリを高速化 | LIKE を高度な検索関数に置き換える |
| **最適な用途** | ログ分析、コード検索、正確なパターンマッチング | ドキュメント検索、コンテンツ発見、検索エンジン |

**次の場合は Ngram Index を選択してください:**

- 最適化したい既存の `LIKE '%pattern%'` クエリがある
- 正確な部分文字列一致が必要（大文字・小文字を区別しない）
- ログ、コード、ID などの構造化データを扱っている
- クエリ構文を変更せずにパフォーマンスを改善したい

**次の場合は Full-Text Index を選択してください:**

- ドキュメントやコンテンツ向けの検索機能を構築している
- あいまい検索、関連度スコアリング、または複雑なクエリが必要
- 自然言語テキストを扱っている
- 単純なパターンマッチングを超える高度な検索機能が必要

## Ngram インデックスの仕組み {#how-ngram-index-works}

Ngram インデックスは、テキストを重なり合う文字部分文字列（n-gram）に分割し、高速なパターン検索を実現します。

**`gram_size = 3` の例:**

```text
Input: "The quick brown"
N-grams: "The", "he ", "e q", " qu", "qui", "uic", "ick", "ck ", "k b", " br", "bro", "row", "own"
```

**クエリ処理:**

```sql
SELECT * FROM t WHERE content LIKE '%quick br%'
```

1. パターン `'quick br'` は n-gram にトークン化されます: "qui", "uic", "ick", "ck ", "k b", " br"
2. インデックスが、これらの n-gram を含むデータブロックを絞り込みます
3. 完全な `LIKE` フィルタは、事前に絞り込まれたブロックに対してのみ適用されます

> **Note:**
>
> - パターンは少なくとも `gram_size` 文字以上である必要があります（`gram_size=3` の場合、`'%yo%'` のような短いパターンではインデックスは使用されません）
> - 一致は大文字・小文字を区別しません（"FOO" は "foo"、"Foo"、"fOo" に一致します）
> - `LIKE` 演算子でのみ機能し、他のパターンマッチング関数では機能しません

## クイックセットアップ {#quick-setup}

```sql
-- Create table with text content
CREATE TABLE logs(id INT, message STRING);

-- Create ngram index with 3-character segments
CREATE NGRAM INDEX logs_message_idx ON logs(message) gram_size = 3;

-- Insert data (automatically indexed)
INSERT INTO logs VALUES (1, 'Application error occurred');

-- Search using LIKE - automatically optimized
SELECT * FROM logs WHERE message LIKE '%error%';
```

## 完全な例 {#complete-example}

この例では、ログ分析用の ngram インデックスを作成し、そのパフォーマンス上の利点を確認する方法を示します。

```sql
-- Create table for application logs
CREATE TABLE t_articles (
    id INT,
    content STRING
);

-- Create ngram index with 3-character segments
CREATE NGRAM INDEX ngram_idx_content
ON t_articles(content)
gram_size = 3;

-- Verify index creation
SHOW INDEXES;
```

```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        name       │  type  │ original │            definition            │         created_on         │      updated_on     │
├───────────────────┼────────┼──────────┼──────────────────────────────────┼────────────────────────────┼─────────────────────┤
│ ngram_idx_content │ NGRAM  │          │ t_articles(content)gram_size='3' │ 2025-05-13 01:02:58.598409 │ NULL                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```sql
-- Insert test data: 995 irrelevant rows + 5 target rows
INSERT INTO t_articles
SELECT number, CONCAT('Random text number ', number)
FROM numbers(995);

INSERT INTO t_articles VALUES
    (1001, 'The silence was deep and complete'),
    (1002, 'They walked in silence through the woods'),
    (1003, 'Silence fell over the room'),
    (1004, 'A moment of silence was observed'),
    (1005, 'In silence, they understood each other');

-- Search with pattern matching
SELECT id, content FROM t_articles WHERE content LIKE '%silence%';

-- Verify index usage
EXPLAIN SELECT id, content FROM t_articles WHERE content LIKE '%silence%';
```

**パフォーマンス結果:**

```sql
-[ EXPLAIN ]-----------------------------------
TableScan
├── table: default.default.t_articles
├── output columns: [id (#0), content (#1)]
├── read rows: 5
├── read size: < 1 KiB
├── partitions total: 2
├── partitions scanned: 1
├── pruning stats: [segments: <range pruning: 2 to 2>, blocks: <range pruning: 2 to 2, bloom pruning: 2 to 1>]
├── push downs: [filters: [is_true(like(t_articles.content (#1), '%silence%'))], limit: NONE]
└── estimated rows: 15.62
```

**主要なパフォーマンス指標:** `bloom pruning: 2 to 1` は、ngram インデックスがスキャン前にデータブロックの 50% を正常に除外したことを示しています。

## ベストプラクティス {#best-practices}

| プラクティス | 利点 |
|----------|---------|
| **適切な gram_size を選択する** | `gram_size=3` はほとんどのケースで有効。より長いパターンにはより大きな値を使用 |
| **頻繁に検索されるカラムにインデックスを作成する** | `LIKE '%pattern%'` クエリで使用されるカラムに注力する |
| **インデックス使用状況を監視する** | `EXPLAIN` を使用して `bloom pruning` 統計を確認する |
| **パターン長を考慮する** | 検索パターンが少なくとも `gram_size` 文字以上であることを確認する |

## Essential コマンド {#essential-commands}

完全なコマンドリファレンスについては、[Ngram Index](/tidb-cloud-lake/sql/ngram-index-sql.md) を参照してください。

| Command                                                  | 目的 |
|----------------------------------------------------------|----------------------------------------------|
| `CREATE NGRAM INDEX name ON table(column) gram_size = N` | N 文字セグメントの ngram インデックスを作成する |
| `SHOW INDEXES`                                           | ngram インデックスを含むすべてのインデックスを一覧表示する |
| `REFRESH NGRAM INDEX name ON table`                      | ngram インデックスを更新する |
| `DROP NGRAM INDEX name ON table`                         | ngram インデックスを削除する |

**Ngram インデックスを使用する場面**

**適しているケース:**

- ログ分析および監視システム
- コード検索およびパターンマッチング
- 製品カタログ検索
- `LIKE '%pattern%'` クエリが頻繁に使われるあらゆるアプリケーション

**推奨されないケース:**

- 短いパターン検索（`gram_size` 文字未満）
- 完全一致の文字列検索（代わりに等価比較を使用）
- 複雑なテキスト検索要件（代わりに Full-Text Index を使用）

---

*ngram インデックスは、大規模なテキストデータセットに対して `LIKE` クエリによる高速なパターンマッチングを必要とするアプリケーションに不可欠です。*