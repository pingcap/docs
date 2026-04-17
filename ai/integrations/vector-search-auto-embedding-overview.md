---
title: Auto Embedding Overview
summary: 自動埋め込み機能を使用して、ベクトルではなくプレーンテキストで意味検索を実行する方法を学びましょう。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-overview/']
---

# 自動埋め込みの概要 {#auto-embedding-overview}

自動埋め込み機能を使用すると、独自のベクトルを用意することなく、プレーンテキストで直接ベクトル検索を実行できます。この機能を使えば、テキストデータを直接挿入し、テキストクエリを使用して意味検索を実行できます。TiDBはバックグラウンドでテキストを自動的にベクトルに変換します。

自動埋め込み機能を使用するための基本的なワークフローは以下のとおりです。

1.  `EMBED_TEXT()`を使用して、テキスト列と生成されたベクトル列を持つ**テーブルを定義します**。
2.  **テキストデータを挿入すると**、ベクトルが自動的に生成され保存されます。
3.  **テキストを使用してクエリを実行します**。 `VEC_EMBED_COSINE_DISTANCE()`または`VEC_EMBED_L2_DISTANCE()`を使用して、意味的に類似したコンテンツを検索します。

> **注記：**
>
> 自動埋め込み機能は、AWS上でホストされているTiDB Cloud Starterインスタンスでのみ利用可能です。

## クイックスタートの例 {#quick-start-example}

> **ヒント：**
>
> Python の使用方法については、 [Pythonで自動埋め込みを使用する](#use-auto-embedding-in-python)を参照してください。

以下の例は、コサイン距離を用いた自動埋め込み機能を使用して意味検索を実行する方法を示しています。この例では、APIキーは不要です。

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

出力は以下のとおりです。

    +----+--------------------------------------------------------------+
    | id | content                                                      |
    +----+--------------------------------------------------------------+
    |  2 | Solar panels convert sunlight into renewable energy.         |
    |  1 | Electric vehicles reduce air pollution in cities.            |
    |  4 | Deep learning algorithms improve medical diagnosis accuracy. |
    +----+--------------------------------------------------------------+

前述の例では、Amazon Titan モデルを使用しています。その他のモデルについては、[利用可能なテキスト埋め込みモデル](#available-text-embedding-models)を参照してください。

## 自動埋め込み + ベクトルインデックス {#auto-embedding-vector-index}

自動埋め込みはクエリのパフォーマンスを向上させるための[ベクトルインデックス](/ai/reference/vector-search-index.md)と互換性があります。生成されたベクトル列にベクトル インデックスを定義でき、それは自動的に使用されます。

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
> -   ベクトルインデックスを定義する場合は、 `VEC_COSINE_DISTANCE()`または`VEC_L2_DISTANCE()`を使用します。
> -   クエリを実行する際は、 `VEC_EMBED_COSINE_DISTANCE()`または`VEC_EMBED_L2_DISTANCE()`を使用してください。

## 利用可能なテキスト埋め込みモデル {#available-text-embedding-models}

TiDB Cloudは様々な埋め込みモデルをサポートしています。ニーズに最適なモデルをお選びください。

| 埋め込みモデル  | 文書                                                                                 | TiDB Cloud <sup>1</sup>がホストしています | BYOK <sup>2</sup> |
| -------- | ---------------------------------------------------------------------------------- | -------------------------------- | ----------------- |
| アマゾンタイタン | [Amazon Titan 埋め込み](/ai/integrations/vector-search-auto-embedding-amazon-titan.md) | ✅                                |                   |
| 調和する     | [Cohere埋め込み](/ai/integrations/vector-search-auto-embedding-cohere.md)              | ✅                                | ✅                 |
| ジナAI     | [Jina AI埋め込み](/ai/integrations/vector-search-auto-embedding-jina-ai.md)            |                                  | ✅                 |
| OpenAI   | [OpenAI埋め込み](/ai/integrations/vector-search-auto-embedding-openai.md)              |                                  | ✅                 |
| 双子座      | [ジェミニ埋め込み](/ai/integrations/vector-search-auto-embedding-gemini.md)                |                                  | ✅                 |

TiDB Cloudがサポートする以下の推論サービスを通じて、オープンソースの埋め込みモデルを使用することもできます。

| 埋め込みモデル    | 文書                                                                                | TiDB Cloud <sup>1</sup>がホストしています | BYOK <sup>2</sup> | サポートされているモデルの例                     |
| ---------- | --------------------------------------------------------------------------------- | -------------------------------- | ----------------- | ---------------------------------- |
| 抱きしめる顔の推論  | [ハグする顔の埋め込み](/ai/integrations/vector-search-auto-embedding-huggingface.md)        |                                  | ✅                 | `bge-m3` 、 `multilingual-e5-large` |
| NVIDIA NIM | [NVIDIA NIM エンベディング](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md) |                                  | ✅                 | `bge-m3` 、 `nv-embed-v1`           |

<sup>1.</sup>ホスト型モデルはTiDB Cloudによってホストされており、APIキーは必要ありません。現在、これらのホスト型モデルは無料で利用できますが、すべてのユーザーが利用できるようにするために、一定の利用制限が適用される場合があります。

<sup>2</sup> BYOK（Bring Your Own Key）モデルでは、対応する埋め込みプロバイダーから独自のAPIキーを提供する必要があります。TiDB CloudはBYOKモデルの使用料を請求しません。これらのモデルの使用に伴うコストの管理と監視はお客様の責任となります。

## 自動埋め込みの仕組み {#how-auto-embedding-works}

自動埋め込みでは、 [`EMBED_TEXT()`](#embed_text)関数を使用して、選択した埋め込みモデルでテキストをベクトル埋め込みに変換します。生成されたベクトルは`VECTOR`列に格納され、 [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance)または[`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance)を使用してプレーンテキストでクエリできます。

内部的には、 [`VEC_EMBED_COSINE_DISTANCE()`](#vec_embed_cosine_distance)と[`VEC_EMBED_L2_DISTANCE()`](#vec_embed_l2_distance)は、テキストクエリが自動的にベクトル埋め込みに変換された状態で、 [`VEC_COSINE_DISTANCE()`](/ai/reference/vector-search-functions-and-operators.md#vec_cosine_distance)と[`VEC_L2_DISTANCE()`](/ai/reference/vector-search-functions-and-operators.md#vec_l2_distance)として実行されます。

## 主要関数 {#key-functions}

### <code>EMBED_TEXT()</code> {#code-embed-text-code}

テキストをベクトル埋め込みに変換します。

```sql
EMBED_TEXT("model_name", text_content[, additional_json_options])
```

`GENERATED ALWAYS AS`句でこの関数を使用すると、テキストデータの挿入または更新時に埋め込みを自動的に生成できます。

### <code>VEC_EMBED_COSINE_DISTANCE()</code> {#code-vec-embed-cosine-distance-code}

ベクトル列に格納されているベクトルとテキストクエリ間のコサイン類似度を計算します。

```sql
VEC_EMBED_COSINE_DISTANCE(vector_column, "query_text")
```

`ORDER BY`句でこの関数を使用すると、コサイン距離に基づいて結果をランク付けできます。VEC_COSINE_DISTANCE [`VEC_COSINE_DISTANCE()`](/ai/reference/vector-search-functions-and-operators.md#vec_cosine_distance)と同じ計算方法を使用しますが、クエリテキストの埋め込みを自動的に生成します。

### <code>VEC_EMBED_L2_DISTANCE()</code> {#code-vec-embed-l2-distance-code}

保存されたベクトルとテキストクエリ間のL2（ユークリッド）距離を計算します。

```sql
VEC_EMBED_L2_DISTANCE(vector_column, "query_text")
```

`ORDER BY`句でこの関数を使用すると、L2 距離に基づいて結果をランク付けできます。VEC_L2_DISTANCE [`VEC_L2_DISTANCE()`](/ai/reference/vector-search-functions-and-operators.md#vec_l2_distance)と同じ計算方法を使用しますが、クエリ テキストの埋め込みを自動的に生成します。

## Pythonで自動埋め込みを使用する {#use-auto-embedding-in-python}

TiDBは、さまざまな埋め込みプロバイダーやモデルとの統合のための統一インターフェースを提供します。

-   **プログラムによる使用**：特定のプロバイダーまたはモデル用の埋め込み関数を作成するには、AI SDK の`EmbeddingFunction`クラスを使用します。
-   **SQL の使用法**: `EMBED_TEXT`関数を使用して、テキストデータから直接埋め込みを生成します。

`EmbeddingFunction`クラスを使用すると、さまざまな埋め込みプロバイダーやモデルを操作できます。

```python
from pytidb.embeddings import EmbeddingFunction

embed_func = EmbeddingFunction(
    model_name="<provider_name>/<model_name>",
)
```

**パラメータ:**

-   `model_name` *(必須)* : 使用する埋め込みモデルを`{provider_name}/{model_name}`の形式で指定します。

-   `dimensions` *(オプション)* : 出力ベクトル埋め込みの次元数。指定しない場合、モデルにデフォルトの次元がない場合は、初期化時にテスト文字列が埋め込まれ、実際の次元が自動的に決定されます。

-   `api_key` *（オプション）* ：埋め込みサービスにアクセスするためのAPIキー。明示的に設定されていない場合は、プロバイダのデフォルト環境変数からキーを取得します。

-   `api_base` *(オプション)* : 埋め込みAPIサービスのベースURL。

-   `use_server` *(オプション)* : TiDB Cloud のホスト型埋め込みサービスを使用するかどうか。TiDB Cloud Starterの場合は、デフォルトで`True`になります。

-   `multimodal` *(オプション)* : マルチモーダル埋め込みモデルを使用するかどうか。有効にすると、 `use_server`は自動的に`False`に設定され、埋め込みサービスがクライアント側で呼び出されます。

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
