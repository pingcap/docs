---
title: ベクトル検索
summary: PostgreSQL-compatible TiDB Cloud Starter で、埋め込みの保存、類似検索の実行、HNSW インデックスの作成を行う方法を学びます。
---

# ベクトル検索

PostgreSQL-compatible {{{ .starter }}} は、`VECTOR` 型、距離演算子、HNSW インデックス、サーバー側の埋め込み関数を含む、pgvector 互換のベクトル保存と類似検索を提供します。

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} は現在パブリックプレビューです。

## ベクトル検索を有効にする {#enable-vector-search}

`VECTOR` 型とベクトル演算子は組み込みです。`vector` 拡張のメタデータを登録するには、次を実行します。

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

サーバー側の埋め込み関数を使用するには、`embedding` 拡張を有効にします。

```sql
CREATE EXTENSION IF NOT EXISTS embedding;
```

## ベクトルを保存する {#store-vectors}

固定次元のベクトルを保存するには、`VECTOR(n)` を使用します。

例:

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(3)
);
```

ベクトルリテラルを使用してベクトルを挿入できます。

```sql
INSERT INTO documents (content, embedding)
VALUES ('hello world', '[0.1, 0.2, 0.3]'::vector);
```

ベクトルの次元数は、対象の `VECTOR(n)` カラムで宣言された次元と一致している必要があります。

## 距離演算子 {#distance-operators}

PostgreSQL-compatible {{{ .starter }}} は、以下の pgvector 互換距離演算子をサポートしています。

| 演算子 | 距離メトリック | 対応する関数 |
| --- | --- | --- |
| `<->` | L2（ユークリッド）距離 | `l2_distance(a, b)` |
| `<=>` | コサイン距離 | `cosine_distance(a, b)` |
| `<#>` | 負の内積 | `vector_negative_inner_product(a, b)` |

たとえば、次のクエリはコサイン距離検索を実行します。

```sql
SELECT
    id,
    content,
    embedding <=> '[0.1, 0.2, 0.3]'::vector AS distance
FROM documents
ORDER BY distance
LIMIT 5;
```

以下のユーティリティ関数も使用できます。

| 関数 | 説明 |
| --- | --- |
| `l2_distance(a, b)` | ユークリッド距離を計算します。 |
| `cosine_distance(a, b)` | コサイン距離を計算します。 |
| `inner_product(a, b)` | 内積を計算します。 |
| `vector_negative_inner_product(a, b)` | `<#>` で使用される負の内積を計算します。 |
| `vector_dims(v)` | 次元数を返します。 |
| `vector_norm(v)` | L2 ノルムを返します。 |
| `l2_normalize(v)` | L2 正規化されたベクトルを返します。 |

## HNSW インデックスを作成する {#create-an-hnsw-index}

HNSW（Hierarchical Navigable Small World）インデックスは、近似最近傍検索を高速化します。

クエリで使用する距離メトリックに一致する演算子クラスを持つインデックスを作成します。

コサイン距離の場合:

```sql
CREATE INDEX idx_documents_embedding
ON documents
USING hnsw (embedding vector_cosine_ops);
```

L2 距離の場合:

```sql
CREATE INDEX idx_documents_embedding_l2
ON documents
USING hnsw (embedding vector_l2_ops);
```

内積の場合:

```sql
CREATE INDEX idx_documents_embedding_ip
ON documents
USING hnsw (embedding vector_ip_ops);
```

### HNSW インデックスパラメータを設定する {#configure-hnsw-index-parameters}

インデックス作成時に HNSW インデックスのビルドパラメータを設定できます。

```sql
CREATE INDEX idx_documents_embedding
ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

| パラメーター | Default | 説明 |
| --- | --- | --- |
| `m` | 16 | 各レイヤーあたりの最大接続数。値を大きくすると、追加のメモリを消費する代わりに再現率が向上する可能性があります。 |
| `ef_construction` | 64 | インデックス構築中の検索幅。値を大きくすると、ビルドが遅くなる代わりにインデックス品質が向上する可能性があります。 |

現在のセッションに対して HNSW の検索拡張係数を設定できます。

```sql
SET hnsw.ef_search = 100;
```

`hnsw.ef_search` のデフォルト値は `40` です。値を大きくすると、追加のクエリレイテンシーを伴う代わりに再現率が向上する可能性があります。

### HNSW インデックスが使用される条件 {#when-an-hnsw-index-is-used}

以下の条件をすべて満たす場合、オプティマイザは HNSW インデックスを使用できます。

- クエリが、インデックス付きベクトルカラムと定数ベクトルに対する距離式で `ORDER BY` している、またはそのカラムに対して定数のクエリテキストを使って `vec_embed_cosine_distance()` を使用している。
- クエリに `LIMIT` 句が含まれている。
- HNSW インデックスが、クエリ内の距離メトリックに一致する演算子クラスを使用している。
- HNSW インデックスの構築が完了しており、クエリで利用可能である。
- クエリに `WHERE` 句が含まれていない。

例:

```sql
SELECT id, content
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, 0.3]'::vector
LIMIT 10;
```

これらの条件を満たさない場合、クエリは正確な逐次スキャンにフォールバックします。結果は引き続き正しいままですが、HNSW インデックスは使用されません。

> **Note:**
>
> クエリベクトルとして使用されるバインドパラメータは、HNSW プランニングでは定数として扱われません。たとえば、`ORDER BY embedding <=> $1::vector LIMIT 10` は逐次スキャンにフォールバックします。

## SQL で埋め込みを生成する {#generate-embeddings-in-sql}

`embedding` 拡張は、サーバー側の埋め込み関数を提供します。

テキストから埋め込みを生成するには、次を実行します。

```sql
SELECT embedding('hello world');
```

明示的なモデルを指定して `embed_text()` を使用することもできます。

```sql
SELECT embed_text('text-embedding-v4', 'hello world');
```

現在サポートされている埋め込み次元は 256、512、1024 です。デフォルトの出力次元は 1024 です。

現在のセッションの出力次元を変更するには、次を実行します。

```sql
SET embedding.dimensions = 512;

SELECT embedding('hello world');
```

## エンドツーエンドの例 {#end-to-end-example}

次の例では、テーブルを作成し、埋め込みを生成し、HNSW インデックスを作成して、セマンティック検索を実行します。

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS embedding;

SET embedding.dimensions = 1024;

CREATE TABLE docs (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    vec VECTOR(1024)
);

INSERT INTO docs (content, vec) VALUES
    ('PostgreSQL is a relational database',
     embedding('PostgreSQL is a relational database')),
    ('TiDB Cloud provides a managed database service',
     embedding('TiDB Cloud provides a managed database service')),
    ('Vector search finds semantically similar documents',
     embedding('Vector search finds semantically similar documents'));

CREATE INDEX idx_docs_vec
ON docs
USING hnsw (vec vector_cosine_ops);

SELECT content
FROM docs
ORDER BY vec_embed_cosine_distance(vec, 'managed database')
LIMIT 3;
```

`vec_embed_cosine_distance()` クエリでは、コサイン距離検索に `idx_docs_vec` を使用できます。このインデックスを使用する `HNSW Scan` が実行計画に含まれているかどうかを確認するには、`SELECT` 文の前に `EXPLAIN` を追加します。

## 自動埋め込みを使用した検索 {#search-with-automatic-embedding}

1 回の関数呼び出しで、クエリテキストの埋め込みと距離計算を行えます。

次の例では、前のセクションで作成した `docs` テーブルを使用します。`docs.vec` カラムには、デフォルトの埋め込みモデルによって生成された 1024 次元の埋め込みが格納されています。

```sql
SELECT id, content
FROM docs
ORDER BY vec_embed_cosine_distance(vec, 'database for AI applications')
LIMIT 5;
```

クエリ埋め込みでは、保存済みの埋め込みと同じモデルおよび次元数を使用する必要があります。

使用可能な関数は次のとおりです。

| 関数 | 等価な操作 |
| --- | --- |
| `vec_embed_l2_distance(vec, text)` | `l2_distance(vec, embedding(text))` |
| `vec_embed_cosine_distance(vec, text)` | `cosine_distance(vec, embedding(text))` |
| `vec_embed_inner_product(vec, text)` | `inner_product(vec, embedding(text))` |

## 制限事項 {#limitations}

パブリックプレビュー期間中のベクトル検索には、次の制限があります。

- IVFFlat インデックスはサポートされていません。サポートされる近似最近傍インデックスの種類は HNSW です。
- HNSW インデックスには、1 つのベクトルカラムしか含められません。
- インデックス対象のベクトルカラムでは、`VECTOR(1024)` のように次元数を明示的に宣言する必要があります。HNSW インデックス作成に、次元数を指定しない `VECTOR` カラムは使用しないでください。
- テーブルには単一カラムの主キーが必要です。主キーがないテーブル、または複合主キーを持つテーブルでは HNSW インデックスを使用できません。
- 主キーが `INTEGER` または `BIGINT` の場合、その値は非負である必要があります。`UUID` および `TEXT` の主キーにはこの制限はありません。
- 部分 HNSW インデックスはサポートされていません。
- 距離演算では、次元数が一致するベクトルが必要です。
- `embedding()` 関数と `embed_text()` 関数を使用するには、十分な権限を持つデータベースユーザーが必要です。
- HNSW アクセラレーションにはクエリ形状に関する制限があります。[HNSW インデックスが使用される条件](#when-an-hnsw-index-is-used) で説明されている要件を満たさないクエリでは、代わりに正確なシーケンシャルスキャンが使用されます。