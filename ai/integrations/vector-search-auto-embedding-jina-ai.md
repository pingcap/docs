---
title: Jina AI Embeddings
summary: TiDB CloudでJina AI埋め込みモデルを使用する方法を学びましょう。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-jina-ai/']
---

# Jina AI埋め込み {#jina-ai-embeddings}

このドキュメントでは、TiDB Cloudで[Jina AI埋め込みモデル](https://jina.ai/embeddings/)with [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)を使用して、テキスト クエリによるセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)、AWS でホストされているTiDB Cloud Starterインスタンスでのみ利用できます。

## 利用可能なモデル {#available-models}

Jina AIは、検索、RAG、およびエージェントアプリケーション向けに、高性能でマルチモーダルかつ多言語対応の長文コンテキスト埋め込みを提供します。

Jina AI APIキー（BYOK）をお持ちの場合は、 `jina_ai/`プレフィックスを使用してすべてのJina AIモデルをご利用いただけます。例：

**jina-embeddings-v4**

-   名前: `jina_ai/jina-embeddings-v4`
-   寸法: 2048
-   距離指標：コサイン類似度、L2
-   入力可能なテキストトークンの最大数：32,768
-   価格：Jina AIによる課金
-   TiDB Cloudでホストされています: ❌
-   鍵をご持参ください：✅

**jina-embeddings-v3**

-   名前: `jina_ai/jina-embeddings-v3`
-   寸法: 1024
-   距離指標：コサイン類似度、L2
-   入力可能なテキストトークンの最大数：8,192
-   価格：Jina AIによる課金
-   TiDB Cloudでホストされています: ❌
-   鍵をご持参ください：✅

利用可能なモデルの完全なリストについては、 [Jina AI ドキュメント](https://jina.ai/embeddings/)を参照してください。

## 使用例 {#usage-example}

この例では、Jina AIの埋め込みモデルを使用して、ベクターテーブルを作成し、ドキュメントを挿入し、類似性検索を実行する方法を示します。

### ステップ1：データベースに接続する {#step-1-connect-to-the-database}

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

### ステップ2：APIキーを設定する {#step-2-configure-the-api-key}

[Jina AIプラットフォーム](https://jina.ai/embeddings/)から API キーを作成し、埋め込みサービスを使用するために独自のキーを使用 (BYOK) します。

<SimpleTab groupId="language">
<div label="Python" value="python">

TiDBクライアントを使用して、Jina AI埋め込みプロバイダーのAPIキーを設定します。

```python
tidb_client.configure_embedding_provider(
    provider="jina_ai",
    api_key="{your-jina-api-key}",
)
```

</div>
<div label="SQL" value="sql">

SQLを使用して、Jina AI埋め込みプロバイダーのAPIキーを設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_JINA_AI_API_KEY = "{your-jina-api-key}";
```

</div>
</SimpleTab>

### ステップ3：ベクターテーブルを作成する {#step-3-create-a-vector-table}

`jina_ai/jina-embeddings-v4`モデルを使用して 2048 次元ベクトルを生成するベクトルフィールドを持つテーブルを作成します。

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

### ステップ4：テーブルにデータを挿入する {#step-4-insert-data-into-the-table}

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

### ステップ5：類似文書を検索する {#step-5-search-for-similar-documents}

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.search()` APIを使用してベクトル検索を実行します。

```python
results = table.search("How to start learning Java programming?") \
    .limit(2) \
    .to_list()
print(results)
```

</div>
<div label="SQL" value="sql">

`VEC_EMBED_COSINE_DISTANCE`関数を使用して、コサイン距離メトリックに基づくベクトル検索を実行します。

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

すべての[Jina AIのオプション](https://jina.ai/embeddings/)は`additional_json_options`関数の`EMBED_TEXT()`パラメータを通じてサポートされます。

**例：パフォーマンス向上のため「下流タスク」を指定してください**

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

**例：別の次元を使用する**

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

利用可能なすべてのオプションについては、 [Jina AI ドキュメント](https://jina.ai/embeddings/)を参照してください。

## 関連項目 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
