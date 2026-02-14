---
title: Jina AI Embeddings
summary: TiDB Cloudで Jina AI 埋め込みモデルを使用する方法を学びます。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-jina-ai/']
---

# Jina AI 埋め込み {#jina-ai-embeddings}

このドキュメントでは、TiDB Cloudで[Jina AI埋め込みモデル](https://jina.ai/embeddings/)と[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)を使用してテキスト クエリによるセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)は、AWS でホストされているTiDB Cloud Starter クラスターでのみ使用できます。

## 利用可能なモデル {#available-models}

Jina AI は、検索、RAG、エージェント アプリケーション向けに、高性能、マルチモーダル、多言語のロングコンテキスト埋め込みを提供します。

ご自身のJina AI APIキー（BYOK）をお持ちいただければ、すべてのJina AIモデルを`jina_ai/`プレフィックスでご利用いただけます。例：

**jina-embeddings-v4**

-   名前: `jina_ai/jina-embeddings-v4`
-   寸法: 2048
-   距離計量：コサイン、L2
-   最大入力テキストトークン数: 32,768
-   価格：Jina AIによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

**jina-embeddings-v3**

-   名前: `jina_ai/jina-embeddings-v3`
-   寸法: 1024
-   距離計量：コサイン、L2
-   最大入力テキストトークン数: 8,192
-   価格：Jina AIによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

利用可能なモデルの完全なリストについては、 [Jina AI ドキュメント](https://jina.ai/embeddings/)参照してください。

## 使用例 {#usage-example}

この例では、ベクター テーブルを作成し、ドキュメントを挿入し、Jina AI 埋め込みモデルを使用して類似性検索を実行する方法を示します。

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

[ジナAIプラットフォーム](https://jina.ai/embeddings/)から API キーを作成し、独自のキー (BYOK) を持って埋め込みサービスを使用します。

<SimpleTab groupId="language">
<div label="Python" value="python">

TiDB クライアントを使用して、Jina AI 埋め込みプロバイダーの API キーを設定します。

```python
tidb_client.configure_embedding_provider(
    provider="jina_ai",
    api_key="{your-jina-api-key}",
)
```

</div>
<div label="SQL" value="sql">

SQL を使用して Jina AI 埋め込みプロバイダーの API キーを設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_JINA_AI_API_KEY = "{your-jina-api-key}";
```

</div>
</SimpleTab>

### ステップ3: ベクターテーブルを作成する {#step-3-create-a-vector-table}

`jina_ai/jina-embeddings-v4`モデルを使用して 2048 次元のベクトルを生成するベクトル フィールドを持つテーブルを作成します。

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
        model_name="jina_ai/jina-embeddings-v4"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(2048) GENERATED ALWAYS AS (EMBED_TEXT(
        "jina_ai/jina-embeddings-v4",
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

`VEC_EMBED_COSINE_DISTANCE`関数を使用して、コサイン距離メトリックに基づいてベクトル検索を実行します。

```sql
SELECT
    `id`,
    `content`,
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to start learning Java programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

結果：

    +------+----------------------------------------------------------------+
    | id   | content                                                        |
    +------+----------------------------------------------------------------+
    |    1 | Java: Object-oriented language for cross-platform development. |
    |    4 | Java's syntax is used in Android apps.                         |
    +------+----------------------------------------------------------------+

</div>
</SimpleTab>

## オプション {#options}

[Jina AIオプション](https://jina.ai/embeddings/)すべて、 `EMBED_TEXT()`関数の`additional_json_options`パラメータを介してサポートされます。

**例: パフォーマンス向上のため「下流タスク」を指定する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(2048) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v4",
                `content`,
                '{"task": "retrieval.passage", "task@search": "retrieval.query"}'
              )) STORED
);
```

**例: 代替ディメンションを使用する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "jina_ai/jina-embeddings-v3",
                `content`,
                '{"dimensions":768}'
              )) STORED
);
```

利用可能なすべてのオプションについては、 [Jina AI ドキュメント](https://jina.ai/embeddings/)参照してください。

## 参照 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
