---
title: Hugging Face Embeddings
summary: TiDB Cloudで Hugging Face 埋め込みモデルを使用する方法を学びます。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-huggingface/']
---

# ハグフェイス埋め込み {#hugging-face-embeddings}

このドキュメントでは、TiDB Cloudの[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)で Hugging Face 埋め込みモデルを使用して、テキスト クエリによるセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)は、AWS でホストされているTiDB Cloud Starter クラスターでのみ使用できます。

## 利用可能なモデル {#available-models}

独自の[ハグ顔推論API](https://huggingface.co/docs/inference-providers/index)キー (BYOK) を持ち込む場合、Hugging Face モデルは`huggingface/`プレフィックスで使用できます。

便宜上、以下のセクションではいくつかの一般的なモデルを例として使用します。利用可能なモデルの完全なリストについては、 [ハグフェイスモデル](https://huggingface.co/models?library=sentence-transformers&#x26;inference_provider=hf-inference&#x26;sort=trending)参照してください。すべてのモデルがHugging Face Inference APIで利用可能であるわけではなく、確実に動作するわけでもありませんのでご了承ください。

## 多言語-e5-ラージ {#multilingual-e5-large}

-   名前: `huggingface/intfloat/multilingual-e5-large`
-   寸法: 1024
-   距離計量：コサイン、L2
-   価格：Hugging Faceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/intfloat/multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large)

例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/intfloat/multilingual-e5-large",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## bge-m3 {#bge-m3}

-   名前: `huggingface/BAAI/bge-m3`
-   寸法: 1024
-   距離計量：コサイン、L2
-   価格：Hugging Faceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/BAAI/bge-m3",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## オールミニLM-L6-v2 {#all-minilm-l6-v2}

-   名前: `huggingface/sentence-transformers/all-MiniLM-L6-v2`
-   寸法: 384
-   距離計量：コサイン、L2
-   価格：Hugging Faceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(384) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-MiniLM-L6-v2",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## all-mpnet-base-v2 {#all-mpnet-base-v2}

-   名前: `huggingface/sentence-transformers/all-mpnet-base-v2`
-   寸法: 768
-   距離計量：コサイン、L2
-   価格：Hugging Faceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/sentence-transformers/all-mpnet-base-v2",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## Qwen3-埋め込み-0.6B {#qwen3-embedding-0-6b}

> **注記：**
>
> Hugging Face Inference API はこのモデルでは不安定になる可能性があります。

-   名前: `huggingface/Qwen/Qwen3-Embedding-0.6B`
-   寸法: 1024
-   距離計量：コサイン、L2
-   最大入力テキストトークン数: 512
-   価格：Hugging Faceによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅
-   プロジェクトホーム: [https://huggingface.co/Qwen/Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_HUGGINGFACE_API_KEY = 'your-huggingface-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "huggingface/Qwen/Qwen3-Embedding-0.6B",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

## Pythonの使用例 {#python-usage-example}

この例では、ベクター テーブルを作成し、ドキュメントを挿入し、Hugging Face 埋め込みモデルを使用して類似性検索を実行する方法を示します。

### ステップ1: データベースに接続する {#step-1-connect-to-the-database}

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

### ステップ2: APIキーを設定する {#step-2-configure-the-api-key}

プライベートモデルをご利用の場合、またはより高いレート制限が必要な場合は、Hugging Face APIトークンを設定できます。トークンは[ハグフェイストークンの設定](https://huggingface.co/settings/tokens)ページ目から作成できます。

TiDB クライアントを使用して、Hugging Face モデルの API トークンを設定します。

```python
tidb_client.configure_embedding_provider(
    provider="huggingface",
    api_key="{your-huggingface-token}",
)
```

### ステップ3: ベクターテーブルを作成する {#step-3-create-a-vector-table}

Hugging Face モデルを使用して埋め込みを生成するベクトル フィールドを含むテーブルを作成します。

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.datatype import TEXT

class Document(TableModel):
    __tablename__ = "sample_documents"
    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = EmbeddingFunction(
        model_name="huggingface/sentence-transformers/all-MiniLM-L6-v2"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

> **ヒント：**
>
> ベクトルの次元は選択したモデルによって異なります。例えば、 `huggingface/sentence-transformers/all-MiniLM-L6-v2`は384次元のベクトルが生成され、 `huggingface/sentence-transformers/all-mpnet-base-v2`では768次元のベクトルが生成されます。

### ステップ4: テーブルにデータを挿入する {#step-4-insert-data-into-the-table}

`table.insert()`または`table.bulk_insert()` API を使用してデータを追加します。

```python
documents = [
    Document(id=1, content="Machine learning algorithms can identify patterns in data."),
    Document(id=2, content="Deep learning uses neural networks with multiple layers."),
    Document(id=3, content="Natural language processing helps computers understand text."),
    Document(id=4, content="Computer vision enables machines to interpret images."),
    Document(id=5, content="Reinforcement learning learns through trial and error."),
]
table.bulk_insert(documents)
```

### ステップ5: 類似文書を検索する {#step-5-search-for-similar-documents}

`table.search()` API を使用してベクトル検索を実行します。

```python
results = table.search("How do neural networks work?") \
    .limit(3) \
    .to_list()

for doc in results:
    print(f"ID: {doc.id}, Content: {doc.content}")
```

## 参照 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
