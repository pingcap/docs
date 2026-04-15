---
title: OpenAI-Compatible Embeddings
summary: TiDB Vector SearchをOpenAI互換の埋め込みモデルと統合して、埋め込みデータを保存し、セマンティック検索を実行する方法を学びましょう。
---

# OpenAI互換埋め込み {#openai-compatible-embeddings}

このチュートリアルでは、OpenAI互換の埋め込みサービスを使用してテキスト埋め込みを生成し、TiDBに保存し、意味検索を実行する方法を説明します。

> **注記：**
>
> 現在、 [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)、AWS でホストされているTiDB Cloud Starterインスタンスでのみ利用できます。

## OpenAI互換の埋め込みサービス {#openai-compatible-embedding-services}

OpenAI Embedding APIは広く利用されているため、多くのプロバイダーが以下のような互換性のあるAPIを提供しています。

-   [オラマ](https://ollama.com/)
-   [vLLM](https://vllm.ai/)

TiDB Python SDK [pytidb](https://github.com/pingcap/pytidb) 、OpenAI 互換の埋め込みサービスと統合するための`EmbeddingFunction`クラスを提供します。

## 使用例 {#usage-example}

この例では、OpenAI互換の埋め込みモデルを使用して、ベクトルテーブルを作成し、ドキュメントを挿入し、類似性検索を実行する方法を示します。

### ステップ1：データベースに接続する {#step-1-connect-to-the-database}

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

### ステップ2：埋め込み関数を定義する {#step-2-define-the-embedding-function}

OpenAI互換の埋め込みサービスと統合するには、 `EmbeddingFunction`クラスを初期化し、 `model_name`パラメータに`openai/`プレフィックスを設定します。

```python
from pytidb.embeddings import EmbeddingFunction

openai_like_embed = EmbeddingFunction(
    model_name="openai/{model_name}",
    api_base="{your-api-base}",
    api_key="{your-api-key}",
)
```

パラメータは以下のとおりです。

-   `model_name` : 使用するモデルを指定します。 `openai/{model_name}`の形式を使用してください。
-   `api_base` : OpenAI互換の埋め込みAPIサービスのベースURL。
-   `api_key` : 埋め込みAPIサービスで認証するために使用されるAPIキー。

**例：Ollamaを`nomic-embed-text`モデルで使用する**

```python
openai_like_embed = EmbeddingFunction(
    model_name="openai/nomic-embed-text",
    api_base="http://localhost:11434/v1",
)
```

**例： `intfloat/e5-mistral-7b-instruct`モデルで vLLM を使用する**

```python
openai_like_embed = EmbeddingFunction(
    model_name="openai/intfloat/e5-mistral-7b-instruct",
    api_base="http://localhost:8000/v1"
)
```

### ステップ3：ベクターテーブルを作成する {#step-3-create-a-vector-table}

Ollamaと`nomic-embed-text`モデルを使用するベクトルフィールドを持つテーブルを作成します。

```python
from pytidb.schema import TableModel, Field
from pytidb.embeddings import EmbeddingFunction
from pytidb.datatype import TEXT

openai_like_embed = EmbeddingFunction(
    model_name="openai/nomic-embed-text",
    api_base="{your-api-base}",
)

class Document(TableModel):
    __tablename__ = "sample_documents"
    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = openai_like_embed.VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

### ステップ4：テーブルにデータを挿入する {#step-4-insert-data-into-the-table}

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

[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)を有効にすると、データの挿入時に TiDB が自動的にベクトル値を生成します。

### ステップ5：類似文書を検索する {#step-5-search-for-similar-documents}

`table.search()` APIを使用してベクトル検索を実行します。

```python
results = table.search("How to start learning Java programming?") \
    .limit(2) \
    .to_list()
print(results)
```

[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)を有効にすると、TiDB はベクトル検索中にクエリ テキストの埋め込みを自動的に生成します。
