---
title: Gemini Embeddings
summary: TiDB Cloudで Google Gemini 埋め込みモデルを使用する方法を学びます。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-gemini/']
---

# ジェミニ埋め込み {#gemini-embeddings}

このドキュメントでは、TiDB Cloudの[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)で Gemini 埋め込みモデルを使用して、テキスト クエリによるセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)は、AWS でホストされているTiDB Cloud Starter クラスターでのみ使用できます。

## 利用可能なモデル {#available-models}

ご自身のGemini APIキー（BYOK）をお持ちいただければ、すべてのGeminiモデルを`gemini/`プレフィックスでご利用いただけます。例：

**ジェミニ埋め込み-001**

-   名前: `gemini/gemini-embedding-001`
-   寸法: 128～3072 (デフォルト: 3072)
-   距離計量：コサイン、L2
-   最大入力テキストトークン数: 2,048
-   価格: Google が請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

利用可能なモデルの完全なリストについては、 [Gemini ドキュメント](https://ai.google.dev/gemini-api/docs/embeddings)参照してください。

## 使用例 {#usage-example}

この例では、Google Gemini 埋め込みモデルを使用してベクター テーブルを作成し、ドキュメントを挿入し、類似性検索を実行する方法を示します。

### ステップ1: データベースに接続する {#step-1-connect-to-the-database}

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
from pytidb import TiDBClient

tidb_client = TiDBClient.connect(
    host="{gateway-region}.prod.aws.tidbcloud.com",
    port=4000,
    username="{prefix}.root",
    password="{password}",
    database="{database}",
    ensure_db=True,
)
```

</div>
<div label="SQL" value="sql">

```bash
mysql -h {gateway-region}.prod.aws.tidbcloud.com \
    -P 4000 \
    -u {prefix}.root \
    -p{password} \
    -D {database}
```

</div>
</SimpleTab>

### ステップ2: APIキーを設定する {#step-2-configure-the-api-key}

[Google AIスタジオ](https://makersuite.google.com/app/apikey)から API キーを作成し、独自のキー (BYOK) を持って埋め込みサービスを使用します。

<SimpleTab groupId="language">
<div label="Python" value="python">

TiDB クライアントを使用して、Google Gemini 埋め込みプロバイダの API キーを設定します。

```python
tidb_client.configure_embedding_provider(
    provider="google_gemini",
    api_key="{your-google-api-key}",
)
```

</div>
<div label="SQL" value="sql">

SQL を使用して Google Gemini 埋め込みプロバイダの API キーを設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_GEMINI_API_KEY = "{your-google-api-key}";
```

</div>
</SimpleTab>

### ステップ3: ベクターテーブルを作成する {#step-3-create-a-vector-table}

`gemini-embedding-001`モデルを使用して 3072 次元のベクトルを生成するベクトル フィールドを持つテーブルを作成します (デフォルト)。

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.datatype import TEXT

class Document(TableModel):
    __tablename__ = "sample_documents"
    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = EmbeddingFunction(
        model_name="gemini-embedding-001"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
        "gemini-embedding-001",
        `content`
    )) STORED
);
```

</div>
</SimpleTab>

### ステップ4: テーブルにデータを挿入する {#step-4-insert-data-into-the-table}

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.insert()`または`table.bulk_insert()` API を使用してデータを追加します。

```python
documents = [
    Document(id=1, content="Java: Object-oriented language for cross-platform development."),
    Document(id=2, content="Java coffee: Bold Indonesian beans with low acidity."),
    Document(id=3, content="Java island: Densely populated, home to Jakarta."),
    Document(id=4, content="Java's syntax is used in Android apps."),
    Document(id=5, content="Dark roast Java beans enhance espresso blends."),
]
table.bulk_insert(documents)
```

</div>
<div label="SQL" value="sql">

`INSERT INTO`ステートメントを使用してデータを挿入します。

```sql
INSERT INTO sample_documents (id, content)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");
```

</div>
</SimpleTab>

### ステップ5: 類似文書を検索する {#step-5-search-for-similar-documents}

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.search()` API を使用してベクトル検索を実行します。

```python
results = table.search("How to start learning Java programming?") \
    .limit(2) \
    .to_list()
print(results)
```

</div>
<div label="SQL" value="sql">

`VEC_EMBED_COSINE_DISTANCE`関数を使用して、コサイン距離に基づいてベクトル検索を実行します。

```sql
SELECT
    `id`,
    `content`,
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to start learning Java programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

</div>
</SimpleTab>

## カスタム埋め込み寸法 {#custom-embedding-dimensions}

`gemini-embedding-001`モデルは、Matryoshka Representation Learning (MRL) を通じて柔軟な次元をサポートしています。埋め込み関数で必要な次元を指定できます。

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
# For 1536 dimensions
embedding: list[float] = EmbeddingFunction(
    model_name="gemini-embedding-001",
    dimensions=1536
).VectorField(source_field="content")

# For 768 dimensions
embedding: list[float] = EmbeddingFunction(
    model_name="gemini-embedding-001",
    dimensions=768
).VectorField(source_field="content")
```

</div>
<div label="SQL" value="sql">

```sql
-- For 1536 dimensions
`embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
    "gemini-embedding-001",
    `content`,
    '{"embedding_config": {"output_dimensionality": 1536}}'
)) STORED

-- For 768 dimensions
`embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
    "gemini-embedding-001",
    `content`,
    '{"embedding_config": {"output_dimensionality": 768}}'
)) STORED
```

</div>
</SimpleTab>

パフォーマンス要件とstorageの制約に基づいてディメンションを選択してください。ディメンションを大きくすると精度が向上しますが、より多くのstorageとコンピューティングリソースが必要になります。

## オプション {#options}

[ジェミニオプション](https://ai.google.dev/gemini-api/docs/embeddings)すべて、 `EMBED_TEXT()`関数の`additional_json_options`パラメータを介してサポートされます。

**例: 品質を向上させるためにタスクの種類を指定する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"task_type": "SEMANTIC_SIMILARITY"}'
              )) STORED
);
```

**例: 代替ディメンションを使用する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"output_dimensionality": 768}'
              )) STORED
);
```

利用可能なすべてのオプションについては、 [Gemini ドキュメント](https://ai.google.dev/gemini-api/docs/embeddings)参照してください。

## 参照 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
