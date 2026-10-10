---
title: CREATE VECTOR INDEX
summary: HNSW (Hierarchical Navigable Small World) アルゴリズムを使用した効率的な類似検索を可能にするため、テーブルの VECTOR カラムに Vector インデックスを作成します。
---

# CREATE VECTOR INDEX

HNSW (Hierarchical Navigable Small World) アルゴリズムを使用した効率的な類似検索を可能にするため、テーブルの [VECTOR](/tidb-cloud-lake/sql/vector.md) カラムに Vector インデックスを作成します。

## 構文 {#syntax}

```sql
-- Create a Vector index on an existing table
CREATE [OR REPLACE] VECTOR INDEX [IF NOT EXISTS] <index_name>
ON [<database>.]<table_name>(<column>)
distance = '<metric>' [m = <number>] [ef_construct = <number>]

-- Create a Vector index when creating a table
CREATE [OR REPLACE] TABLE <table_name> (
    <column_definitions>,
    VECTOR INDEX <index_name> (<column>)
        distance = '<metric>' [m = <number>] [ef_construct = <number>]
)...
```

### パラメータ {#parameters}

- **`distance`** (必須) - 類似検索に使用する距離メトリックを指定します。複数のメトリックはカンマで組み合わせることができます。
    - `'cosine'` - コサイン距離（意味的類似性、テキスト埋め込みに最適）
    - `'l1'` - L1 距離 / マンハッタン距離（特徴比較、スパースデータに適しています）
    - `'l2'` - L2 距離 / ユークリッド距離（幾何学的類似性、画像特徴に最適）
    - 例: `distance = 'cosine,l1,l2'` は 3 つすべてのメトリックをサポートします

- **`m`** (任意、デフォルト: 16) - HNSW グラフ内で各ノードが持つ双方向接続の数を制御します。
    - 値を大きくするとメモリ使用量は増えますが、検索精度が向上する可能性があります
    - 0 より大きい必要があります
    - 一般的な範囲: 8-64

- **`ef_construct`** (任意、デフォルト: 100) - インデックス構築中の動的 Candidate リストのサイズを制御します。
    - 値を大きくするとインデックス品質は向上しますが、構築時間とメモリ使用量が増加します
    - `>= 40` である必要があります
    - 一般的な範囲: 40-500

## Vector インデックスの仕組み {#how-vector-index-works}

{{{ .lake }}} の Vector インデックスは、HNSW アルゴリズムを使用して多層グラフ構造を構築します。

1. **グラフ構造**: 各ベクトルはノードであり、最も近い近傍への接続を持ちます
2. **検索プロセス**: クエリはグラフのレイヤーを粗いものから細かいものへとたどり、近似最近傍を高速に見つけます
3. **量子化**: 生のベクトルは、ストレージ削減とクエリ性能向上のために量子化されます（精度低下はごくわずかです）
4. **自動構築**: データの書き込み時にインデックスは自動的に構築されます。すべての INSERT、COPY、またはデータロード (load) 操作で、新しい行に対するインデックスが自動生成されるため、手動メンテナンスは不要です

## 例 {#examples}

### Vector インデックス付きテーブルの作成 {#creating-a-table-with-vector-index}

```sql
-- Simple vector index for embeddings
CREATE TABLE documents (
    id INT,
    title VARCHAR,
    content TEXT,
    embedding VECTOR(1024),
    VECTOR INDEX idx_embedding(embedding) distance = 'cosine'
);
```

### カスタムパラメータを使用した Vector インデックスの作成 {#creating-a-vector-index-with-custom-parameters}

```sql
-- Vector index with multiple distance metrics and tuned parameters
CREATE TABLE images (
    id INT,
    filename VARCHAR,
    feature_vector VECTOR(512),
    VECTOR INDEX idx_features(feature_vector)
        distance = 'cosine,l2'
        m = 32
        ef_construct = 200
);
```

### 既存テーブルへの Vector インデックスの作成 {#creating-a-vector-index-on-an-existing-table}

```sql
CREATE TABLE products (
    id INT,
    name VARCHAR,
    description TEXT,
    embedding VECTOR(768)
);

-- Add vector index after table creation
CREATE VECTOR INDEX idx_product_embedding
ON products(embedding)
distance = 'cosine,l1,l2'
m = 20
ef_construct = 150;
```

### 異なるカラムに対する複数の Vector インデックス {#multiple-vector-indexes-on-different-columns}

```sql
CREATE TABLE multimodal_data (
    id INT,
    text_embedding VECTOR(384),
    image_embedding VECTOR(512),
    VECTOR INDEX idx_text(text_embedding) distance = 'cosine',
    VECTOR INDEX idx_image(image_embedding) distance = 'l2'
);
```

### インデックスの表示 {#viewing-indexes}

すべてのインデックスを表示するには、[SHOW INDEXES](/tidb-cloud-lake/sql/show-indexes.md) を使用します。

```sql
SHOW INDEXES;
```

結果:

```
┌──────────────────────┬────────┬──────────┬────────────────────────────┬──────────────────────────┐
│ name                 │ type   │ original │ definition                 │ created_on               │
├──────────────────────┼────────┼──────────┼────────────────────────────┼──────────────────────────┤
│ idx_embedding        │ VECTOR │          │ documents(embedding)       │ 2025-05-13 01:22:34.123  │
│ idx_product_embedding│ VECTOR │          │ products(embedding)        │ 2025-05-13 01:23:45.678  │
└──────────────────────┴────────┴──────────┴────────────────────────────┴──────────────────────────┘
```

### 類似検索での Vector インデックスの使用 {#using-vector-index-for-similarity-search}

```sql
-- Create a table with vector index
CREATE TABLE wiki_articles (
    id INT,
    title VARCHAR,
    embedding VECTOR(8),
    VECTOR INDEX idx_embedding(embedding) distance = 'cosine'
);

-- Insert sample data (8-dimensional vectors for demonstration)
INSERT INTO wiki_articles VALUES
(1, 'Machine Learning', [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]),
(2, 'Deep Learning', [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]),
(3, 'Natural Language Processing', [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]),
(4, 'Computer Vision', [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]);

-- Find the 2 most similar articles to a query vector using cosine distance
SELECT id, title, cosine_distance(embedding, [0.12, 0.22, 0.32, 0.42, 0.52, 0.62, 0.72, 0.82]) AS distance
FROM wiki_articles
ORDER BY distance ASC
LIMIT 2;
```

結果:

```
┌────┬─────────────────┬──────────────┐
│ id │ title           │ distance     │
├────┼─────────────────┼──────────────┤
│  1 │ Machine Learning│ 0.00012345   │
│  2 │ Deep Learning   │ 0.00023456   │
└────┴─────────────────┴──────────────┘
```

## 性能チューニング {#performance-tuning}

### 距離メトリックの選択 {#choosing-distance-metrics}

ユースケースに応じて適切な距離メトリックを選択してください。距離関数を使用したクエリについては、[ベクトル関数](/tidb-cloud-lake/sql/vector-functions.md) を参照してください。

- **Cosine distance**: BERT や GPT などのモデルによるテキスト埋め込みに最適で、ベクトルの大きさが重要でない場合に適しています
- **L2 (Euclidean) distance**: 絶対差が重要な画像特徴や空間データに最適です
- **L1 (Manhattan) distance**: スパースベクトルや、各次元の差異を強調したい場合に適しています

### HNSW パラメータのチューニング {#tuning-hnsw-parameters}

| パラメータ | 低い値                               | 高い値                               |
|----------------|--------------------------------------|--------------------------------------|
| `m`            | メモリ使用量が少ない、構築が速い     | 精度が高い、メモリ使用量が多い       |
| `ef_construct` | 構築が速い、品質が低い               | 品質が高い、構築が遅い               |

**推奨設定:**

- **小規模データセット (< 100K vectors)**: デフォルト設定 (`m=16`, `ef_construct=100`)
- **中規模データセット (100K - 1M vectors)**: `m=24`, `ef_construct=150`
- **大規模データセット (> 1M vectors)**: `m=32`, `ef_construct=200`
- **高精度要件**: `m=48`, `ef_construct=300`

## 制限事項 {#limitations}

- Vector インデックスは [VECTOR](/tidb-cloud-lake/sql/vector.md) データ型のカラムのみをサポートします
- `distance` パラメータは必須です。これがないインデックスは無視されます
- 量子化により距離計算にごくわずかな誤差が生じる場合があります（通常は < 0.01%）
- `m` の値を大きくするとインデックスサイズが増加します（ベクトルあたりおよそ `m * vector_dimension * 4 bytes`）