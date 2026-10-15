---
title: SQL によるハイブリッド検索
summary: TiDB で、挿入時に自動生成される埋め込みを使って、1 つの SQL クエリで全文検索とベクトル検索を組み合わせる方法を学びます。
---

# SQL によるハイブリッド検索

ハイブリッド検索は、同じテーブルに対して全文検索とベクトル検索を実行し、2 つの結果リストをマージします。全文検索は、エラーコードや製品名のような正確なキーワードを見つけます。ベクトル検索は、単語が異なっていても意味が似ているテキストを見つけます。2 つの結果リストをマージすることで、クエリに正確な用語と、意図を説明する文章の両方が含まれる場合に役立ちます。

このドキュメントでは、1 つの SQL クエリでハイブリッド検索を行う方法を説明します。TiDB は、テキストを挿入すると自動的に埋め込みを生成します。`pytidb` Python SDK で同じことを行うには、[ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md) を参照してください。

## 前提条件 {#prerequisites}

全文検索はまだ初期段階にあり、より多くの顧客に向けて順次提供されています。現在、全文検索は次のリージョンの {{{ .starter }}} でのみ利用できます。

- AWS: `Oregon (us-west-2)` 、 `N. Virginia (us-east-1)` 、 `Tokyo (ap-northeast-1)` 、 `Frankfurt (eu-central-1)` 、および`Singapore (ap-southeast-1)`

Auto Embedding は、AWS でホストされている {{{ .starter }}} インスタンスでのみ利用できます。

このチュートリアルを完了するには、前述のリージョンのいずれかにある {{{ .starter }}} インスタンスと、それに接続された MySQL クライアントが必要です。インスタンスがない場合は、[{{{ .starter }}} インスタンスの作成](/develop/dev-guide-build-cluster-in-cloud.md) に従って作成してください。

## ステップ 1. テーブルを作成する {#step-1-create-a-table}

テキストカラム、TiDB がそのテキストから値を埋めるベクトルカラム、全文インデックス、およびベクトルインデックスを持つテーブルを作成します。

```sql
USE test;

CREATE TABLE docs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED,
    FULLTEXT INDEX ft_content (content) WITH PARSER STANDARD,
    VECTOR INDEX idx_vec ((VEC_COSINE_DISTANCE(content_vector)))
);
```

`EMBED_TEXT()` は TiDB Cloud でホストされる埋め込みモデルを呼び出すため、この例では API キーは不要です。ベクトル次元 `1024` は、モデルの出力サイズと一致している必要があります。他のモデルについては、[自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md) を参照してください。

## ステップ 2. テキストを挿入する {#step-2-insert-text}

テキストのみを挿入します。TiDB は挿入時に各行の埋め込みを生成します。

```sql
INSERT INTO docs (content) VALUES
  ('TiDB error 8200 means a vector index cannot be added to a partitioned table.'),
  ('Store agent memory in one table with a vector index and transactions.'),
  ('Solar panels convert sunlight into renewable energy.'),
  ('Use EXPLAIN to check whether a query uses the vector index.'),
  ('Partitioning a table by tenant lets the optimizer prune partitions.'),
  ('A cat sat on the warm windowsill all afternoon.');
```

## ステップ 3. 意味で検索する {#step-3-search-by-meaning}

クエリテキストを `VEC_EMBED_COSINE_DISTANCE()` に渡します。TiDB は同じモデルでクエリを埋め込み、距離に基づいて行をランク付けします。

```sql
SELECT id, content FROM docs
ORDER BY VEC_EMBED_COSINE_DISTANCE(content_vector, 'why does adding a vector index fail on my partitioned table')
LIMIT 3;
```

```
+----+------------------------------------------------------------------------------+
| id | content                                                                      |
+----+------------------------------------------------------------------------------+
|  1 | TiDB error 8200 means a vector index cannot be added to a partitioned table. |
|  4 | Use EXPLAIN to check whether a query uses the vector index.                  |
|  2 | Store agent memory in one table with a vector index and transactions.        |
+----+------------------------------------------------------------------------------+
```

## ステップ 4. キーワードで検索する {#step-4-search-by-keyword}

`fts_match_word()` を使用して、クエリ語の少なくとも 1 つを含む行を見つけ、関連度でランク付けします。

```sql
SELECT id, content FROM docs
WHERE fts_match_word('error 8200', content)
ORDER BY fts_match_word('error 8200', content) DESC
LIMIT 3;
```

```
+----+------------------------------------------------------------------------------+
| id | content                                                                      |
+----+------------------------------------------------------------------------------+
|  1 | TiDB error 8200 means a vector index cannot be added to a partitioned table. |
+----+------------------------------------------------------------------------------+
```

## ステップ 5. 1 つのクエリで両方の検索を組み合わせる {#step-5-combine-both-searches-in-one-query}

次のクエリは、両方の検索を実行し、それぞれの結果リストをランク付けし、まずベクトル検索と全文検索が返した Top-K の候補 ID に対して Reciprocal Rank Fusion (RRF) を実行します。その後、融合された上位ヒットを `docs` に結合してドキュメント内容を取得します。各行は、出現した各リストごとに `1 / (60 + rank)` のスコアを受け取り、それらのスコアが加算されます。両方のリストで高順位の行は上位に上がります。定数 `60` は RRF で一般的に使われる値で、値を大きくすると、上位ランクの行が下位ランクの行より有利になる度合いが小さくなります。

```sql
WITH
vec AS (
  SELECT id,
         ROW_NUMBER() OVER (ORDER BY distance, id) AS r
  FROM (
    SELECT /*+ READ_FROM_STORAGE(TIFLASH[docs]) */
           id,
           VEC_EMBED_COSINE_DISTANCE(
             content_vector,
             'vector index error 8200 partitioned table'
           ) AS distance
    FROM docs
    ORDER BY distance
    LIMIT 20
  ) v
),
fts AS (
  SELECT id,
         ROW_NUMBER() OVER (ORDER BY score DESC, id) AS r
  FROM (
    SELECT id,
           fts_match_word(
             'vector index error 8200 partitioned table',
             content
           ) AS score
    FROM docs
    WHERE fts_match_word(
      'vector index error 8200 partitioned table',
      content
    )
    ORDER BY score DESC
    LIMIT 20
  ) f
),
hits AS (
  SELECT id,
         1.0 / (60 + r) AS contribution,
         r AS vector_rank,
         NULL AS fulltext_rank
  FROM vec
  UNION ALL
  SELECT id,
         1.0 / (60 + r),
         NULL,
         r
  FROM fts
),
top_hits AS (
  SELECT id,
         SUM(contribution) AS rrf_score,
         MAX(vector_rank) AS vector_rank,
         MAX(fulltext_rank) AS fulltext_rank
  FROM hits
  GROUP BY id
  ORDER BY rrf_score DESC, id
  LIMIT 3
)
SELECT d.id, d.content,
       t.rrf_score,
       t.vector_rank,
       t.fulltext_rank
FROM top_hits t
JOIN docs d ON d.id = t.id
ORDER BY t.rrf_score DESC, t.id;
```

```
+----+------------------------------------------------------------------------------+-----------+-------------+---------------+
| id | content                                                                      | rrf_score | vector_rank | fulltext_rank |
+----+------------------------------------------------------------------------------+-----------+-------------+---------------+
|  1 | TiDB error 8200 means a vector index cannot be added to a partitioned table. |   0.03279 |           1 |             1 |
|  2 | Store agent memory in one table with a vector index and transactions.        |   0.03200 |           3 |             2 |
|  4 | Use EXPLAIN to check whether a query uses the vector index.                  |   0.03200 |           2 |             3 |
+----+------------------------------------------------------------------------------+-----------+-------------+---------------+
```

各検索は、マージ前に 20 件の候補を取得します。マージ結果に関連する行が不足している場合は、この `LIMIT` を増やしてください。

全文検索の関連度スコアは、TiFlash が新しく書き込まれた行をバックグラウンドで再編成した後に変化することがあり、その結果、スコアが近い行同士の順位が入れ替わる場合があります。そのため、新しくロードしたばかりのテーブルでは、出力の `fulltext_rank` と `rrf_score` の値が上記の例と異なることがあります。

`READ_FROM_STORAGE(TIFLASH[docs])` ヒントは、ベクトル検索が、ベクトルインデックスが存在する TiFlash から読み取るようにします。小さなテーブルでは、オプティマイザが代わりに TiKV から読み取り、ベクトルインデックスをスキップすることがあります。同じことは、小さなテーブルに対する他のベクトル検索、たとえばステップ 3 のクエリでも起こる可能性があります。`EXPLAIN` に `annIndex:` が表示されない場合は、そこにも同じヒントを追加してください。オプティマイザが両方のインデックスを選択しているか確認するには、クエリに対して `EXPLAIN` を実行します。`operator info` カラムには、ベクトル検索では `annIndex:`、全文検索では `textSearch:` が表示されます。ベクトルインデックスの使用確認について詳しくは、[ベクトルインデックスが使用されているかどうかを確認する](/ai/reference/vector-search-index.md#check-whether-the-vector-index-is-used) を参照してください。

## 関連情報 {#see-also}

- [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
- [SQLによる全文検索](/ai/guides/vector-search-full-text-search-sql.md)
- [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
- [ベクトル検索インデックス](/ai/reference/vector-search-index.md)