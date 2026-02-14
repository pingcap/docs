---
title: Auto Embedding Overview
summary: 自動埋め込みを使用して、ベクトルではなくプレーンテキストでセマンティック検索を実行する方法を学習します。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-overview/']
---

# 自動埋め込みの概要 {#auto-embedding-overview}

自動埋め込み機能を使用すると、独自のベクターを用意することなく、プレーンテキストで直接ベクター検索を実行できます。この機能を使用すると、テキストデータを直接挿入し、テキストクエリを使用してセマンティック検索を実行できます。TiDBはバックグラウンドでテキストを自動的にベクターに変換します。

自動埋め込みを使用する場合の基本的なワークフローは次のとおりです。

1.  `EMBED_TEXT()`を使用して、テキスト列と生成されたベクター列を持つ**テーブルを定義します**。
2.  **テキスト データを挿入します**。ベクターは自動的に生成され、保存されます。
3.  **テキストを使用したクエリ**- 意味的に類似したコンテンツを見つけるには`VEC_EMBED_COSINE_DISTANCE()`または`VEC_EMBED_L2_DISTANCE()`を使用します。

> **注記：**
>
> 自動埋め込みは、AWS でホストされているTiDB Cloud Starter クラスターでのみ利用できます。

## クイックスタートの例 {#quick-start-example}

> **ヒント：**
>
> Python の使用方法については、 [Pythonで自動埋め込みを使用する](#use-auto-embedding-in-python)参照してください。

以下の例は、コサイン距離を用いた自動埋め込みを使用してセマンティック検索を実行する方法を示しています。この例ではAPIキーは必要ありません。

```sql
-- Create a table with auto-embedding
-- The dimension of the vector column must match the dimension of the embedding model;
-- Otherwise, TiDB returns an error when inserting data.
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED
);

-- Insert text data (vectors are generated automatically)
INSERT INTO documents (content) VALUES
    ("Electric vehicles reduce air pollution in cities."),
    ("Solar panels convert sunlight into renewable energy."),
    ("Plant-based diets lower carbon footprints significantly."),
    ("Deep learning algorithms improve medical diagnosis accuracy."),
    ("Blockchain technology enhances data security systems.");

-- Search for semantically similar content using text query
SELECT id, content FROM documents
ORDER BY VEC_EMBED_COSINE_DISTANCE(
    content_vector,
    "Renewable energy solutions for environmental protection"
)
LIMIT 3;
```

出力は次のようになります。

    +----+--------------------------------------------------------------+
    | id | content                                                      |
    +----+--------------------------------------------------------------+
    |  2 | Solar panels convert sunlight into renewable energy.         |
    |  1 | Electric vehicles reduce air pollution in cities.            |
    |  4 | Deep learning algorithms improve medical diagnosis accuracy. |
    +----+--------------------------------------------------------------+

上記の例ではAmazon Titanモデルを使用しています。他のモデルについては[利用可能なテキスト埋め込みモデル](#available-text-embedding-models)参照してください。

## 自動埋め込み + ベクトルインデックス {#auto-embedding-vector-index}

自動埋め込みは[ベクトルインデックス](/ai/reference/vector-search-index.md)と互換性があり、クエリパフォーマンスを向上させます。生成されたベクター列にベクターインデックスを定義すると、自動的に使用されます。

```sql
-- Create a table with auto-embedding and a vector index
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED,
    VECTOR INDEX ((VEC_COSINE_DISTANCE(content_vector)))
);

-- Insert text data (vectors are generated automatically)
INSERT INTO documents (content) VALUES
    ("Electric vehicles reduce air pollution in cities."),
    ("Solar panels convert sunlight into renewable energy."),
    ("Plant-based diets lower carbon footprints significantly."),
    ("Deep learning algorithms improve medical diagnosis accuracy."),
    ("Blockchain technology enhances data security systems.");

-- Search for semantically similar content with a text query on the vector index using the same VEC_EMBED_COSINE_DISTANCE() function
SELECT id, content FROM documents
ORDER BY VEC_EMBED_COSINE_DISTANCE(
    content_vector,
    "Renewable energy solutions for environmental protection"
)
LIMIT 3;
```

> **注記：**
>
> -   ベクトルインデックスを定義するときは、 `VEC_COSINE_DISTANCE()`または`VEC_L2_DISTANCE()`を使用します。
> -   クエリを実行するときは、 `VEC_EMBED_COSINE_DISTANCE()`または`VEC_EMBED_L2_DISTANCE()`を使用します。

## 利用可能なテキスト埋め込みモデル {#available-text-embedding-models}

TiDB Cloudは様々な埋め込みモデルをサポートしています。ニーズに最適なモデルをお選びください。

| 埋め込みモデル  | ドキュメント                                                                             | TiDB Cloud <sup>1</sup>がホスト | BYOK <sup>2</sup> |
| -------- | ---------------------------------------------------------------------------------- | --------------------------- | ----------------- |
| アマゾンタイタン | [Amazon Titan 埋め込み](/ai/integrations/vector-search-auto-embedding-amazon-titan.md) | ✅                           |                   |
| コヒア      | [コヒーレ埋め込み](/ai/integrations/vector-search-auto-embedding-cohere.md)                | ✅                           | ✅                 |
| ジナ・アイ    | [Jina AI 埋め込み](/ai/integrations/vector-search-auto-embedding-jina-ai.md)           |                             | ✅                 |
| オープンAI   | [OpenAI 埋め込み](/ai/integrations/vector-search-auto-embedding-openai.md)             |                             | ✅                 |
| ジェミニ     | [ジェミニ埋め込み](/ai/integrations/vector-search-auto-embedding-gemini.md)                |                             | ✅                 |

TiDB Cloudがサポートする次の推論サービスを通じて、オープンソースの埋め込みモデルを使用することもできます。

| 埋め込みモデル    | ドキュメント                                                                         | TiDB Cloud <sup>1</sup>がホスト | BYOK <sup>2</sup> | サポートされているモデルの例                   |
| ---------- | ------------------------------------------------------------------------------ | --------------------------- | ----------------- | -------------------------------- |
| 抱きしめる顔の推論  | [ハグフェイス埋め込み](/ai/integrations/vector-search-auto-embedding-huggingface.md)     |                             | ✅                 | `bge-m3` `multilingual-e5-large` |
| NVIDIA NIM | [NVIDIA NIM 埋め込み](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md) |                             | ✅                 | `bge-m3` `nv-embed-v1`           |

<sup>1</sup>ホストモデルはTiDB Cloudによってホストされており、APIキーは必要ありません。現在、これらのホストモデルは無料でご利用いただけますが、すべてのユーザーが利用できるよう、一定の使用制限が適用される場合があります。

<sup>2</sup> BYOK（Bring Your Own Key）モデルでは、対応する埋め込みプロバイダーからご自身のAPIキーをご提供いただく必要があります。TiDB TiDB CloudはBYOKモデルの使用料を請求しません。これらのモデルの使用に伴うコストの管理と監視はお客様の責任となります。

## 自動埋め込みの仕組み {#how-auto-embedding-works}

自動埋め込みは、 [`EMBED_TEXT()`](#embed_text)関数を使用して、選択した埋め込みモデルに基づいてテキストをベクトル埋め込みに変換します。生成されたベクトルは`VECTOR`列に保存され、 [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance)または[`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance)使用してプレーンテキストでクエリできます。

内部的には、 [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance)と[`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance) [`VEC_COSINE_DISTANCE()`](/ai/reference/vector-search-functions-and-operators.md#vec_cosine_distance)と[`VEC_L2_DISTANCE()`](/ai/reference/vector-search-functions-and-operators.md#vec_l2_distance)として実行され、テキスト クエリは自動的にベクトル埋め込みに変換されます。

## 主な関数 {#key-functions}

### <code>EMBED_TEXT()</code> {#code-embed-text-code}

テキストをベクトル埋め込みに変換します。

```sql
EMBED_TEXT("model_name", text_content[, additional_json_options])
```

テキスト データを挿入または更新するときに埋め込みを自動的に生成するには、この関数を`GENERATED ALWAYS AS`節で使用します。

### <code>VEC_EMBED_COSINE_DISTANCE()</code> {#code-vec-embed-cosine-distance-code}

ベクトル列に格納されたベクトルとテキスト クエリ間のコサイン類似度を計算します。

```sql
VEC_EMBED_COSINE_DISTANCE(vector_column, "query_text")
```

この関数を`ORDER BY`節で使用すると、コサイン距離に基づいて結果をランク付けできます。3 [`VEC_COSINE_DISTANCE()`](/ai/reference/vector-search-functions-and-operators.md#vec_cosine_distance)同じ計算式を用いますが、クエリテキストの埋め込みを自動生成します。

### <code>VEC_EMBED_L2_DISTANCE()</code> {#code-vec-embed-l2-distance-code}

保存されたベクトルとテキスト クエリ間の L2 (ユークリッド) 距離を計算します。

```sql
VEC_EMBED_L2_DISTANCE(vector_column, "query_text")
```

この関数を`ORDER BY`節で使用すると、L2距離に基づいて結果をランク付けできます。3 [`VEC_L2_DISTANCE()`](/ai/reference/vector-search-functions-and-operators.md#vec_l2_distance)同じ計算式を用いますが、クエリテキストの埋め込みは自動的に生成されます。

## Pythonで自動埋め込みを使用する {#use-auto-embedding-in-python}

TiDB は、さまざまな埋め込みプロバイダーやモデルと統合するための統一されたインターフェースを提供します。

-   **プログラムによる使用**: AI SDK の`EmbeddingFunction`クラスを使用して、特定のプロバイダーまたはモデルの埋め込み関数を作成します。
-   **SQL の使用**: `EMBED_TEXT`関数を使用して、テキスト データから直接埋め込みを生成します。

さまざまな埋め込みプロバイダーおよびモデルを操作するには、 `EmbeddingFunction`クラスを使用します。

```python
from pytidb.embeddings import EmbeddingFunction

embed_func = EmbeddingFunction(
    model_name="<provider_name>/<model_name>",
)
```

**パラメータ:**

-   `model_name` *(必須)* : 使用する埋め込みモデルを`{provider_name}/{model_name}`形式で指定します。

-   `dimensions` *(オプション)* : 出力ベクトル埋め込みの次元数。指定されておらず、モデルにデフォルトの次元がない場合、初期化時にテスト文字列が埋め込まれ、実際の次元が自動的に決定されます。

-   `api_key` *(オプション)* : 埋め込みサービスにアクセスするためのAPIキー。明示的に設定されていない場合は、プロバイダーのデフォルトの環境変数からキーを取得します。

-   `api_base` *(オプション)* : 埋め込み API サービスのベース URL。

-   `use_server` *(オプション)* : TiDB Cloud のホスト型埋め込みサービスを使用するかどうか。TiDB TiDB Cloud Starter の場合、デフォルトは`True`です。

-   `multimodal` *(オプション)* : マルチモーダル埋め込みモデルを使用するかどうか。有効にすると、 `use_server`は自動的に`False`に設定され、埋め込みサービスはクライアント側で呼び出されます。

## 参照 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ベクター検索インデックス](/ai/reference/vector-search-index.md)
