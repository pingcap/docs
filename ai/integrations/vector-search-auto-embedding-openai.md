---
title: OpenAI Embeddings
summary: TiDB CloudでOpenAIの埋め込みモデルを使用する方法を学びましょう。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-openai/']
---

# OpenAI埋め込み {#openai-embeddings}

このドキュメントでは、 TiDB Cloudで OpenAI 埋め込みモデルを[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)で使用する方法、テキストクエリによる意味検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)、AWS でホストされているTiDB Cloud Starterインスタンスでのみ利用できます。

## 利用可能なモデル {#available-models}

OpenAI APIキー（BYOK）をお持ちの場合は、 `openai/`というプレフィックスを付けて、すべてのOpenAIモデルをご利用いただけます。例：

**テキスト埋め込み3（小）**

-   名前: `openai/text-embedding-3-small`
-   寸法：512～1536（デフォルト：1536）
-   距離指標：コサイン類似度、L2
-   価格：OpenAIが課金
-   TiDB Cloudでホストされています: ❌
-   鍵をご持参ください：✅

**テキスト埋め込み3（大）**

-   名前: `openai/text-embedding-3-large`
-   寸法：256～3072（デフォルト：3072）
-   距離指標：コサイン類似度、L2
-   価格：OpenAIが課金
-   TiDB Cloudでホストされています: ❌
-   鍵をご持参ください：✅

利用可能なモデルの完全なリストについては、 [OpenAIドキュメント](https://platform.openai.com/docs/guides/embeddings)を参照してください。

## 使用例 {#usage-example}

この例では、OpenAIの埋め込みモデルを使用して、ベクトルテーブルを作成し、ドキュメントを挿入し、類似性検索を実行する方法を示します。

AI SDKまたはネイティブSQL関数を使用して、OpenAI Embeddings APIをTiDBと統合し、埋め込みを自動生成できます。

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

[OpenAI APIプラットフォーム](https://platform.openai.com/api-keys)で API キーを作成し、独自のキー (BYOK) を使用して埋め込みサービスを使用します。

<SimpleTab groupId="language">
<div label="Python" value="python">

TiDBクライアントを使用して、OpenAI埋め込みプロバイダーのAPIキーを設定します。

```python
tidb_client.configure_embedding_provider(
    provider="openai",
    api_key="{your-openai-api-key}",
)
```

</div>
<div label="SQL" value="sql">

SQLを使用してOpenAI埋め込みプロバイダーのAPIキーを設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = "{your-openai-api-key}";
```

</div>
</SimpleTab>

### ステップ3：ベクターテーブルを作成する {#step-3-create-a-vector-table}

`openai/text-embedding-3-small`モデルを使用して 1536 次元ベクトルを生成するベクトルフィールドを持つテーブルを作成します。

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
        model_name="openai/text-embedding-3-small"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(1536) GENERATED ALWAYS AS (EMBED_TEXT(
        "openai/text-embedding-3-small",
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

`VEC_EMBED_COSINE_DISTANCE`関数を使用して、コサイン距離によるベクトル検索を実行します。

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

## Azure OpenAIを使用する {#use-azure-openai}

Azure で OpenAI 埋め込みモデルを使用するには、グローバル変数`TIDB_EXP_EMBED_OPENAI_API_BASE` Azure リソースの URL に設定します。例:

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = 'your-openai-api-key-here';
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = 'https://<your-resource-name>.openai.azure.com/openai/v1';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
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

リソース URL が`https://<your-resource-name>.cognitiveservices.azure.com/`と表示されていても、OpenAI と互換性のあるリクエストおよびレスポンス形式を維持するために、API ベースとして`https://<your-resource-name>.openai.azure.com/openai/v1`を使用する必要があります。

Azure OpenAI から OpenAI に直接切り替えるには、 `TIDB_EXP_EMBED_OPENAI_API_BASE`を空の文字列に設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = '';
```

> **注記：**
>
> -   セキュリティ上の理由から、API ベースとして設定できるのは Azure OpenAI の URL または OpenAI の URL のみです。任意のベース URL は許可されていません。
> -   OpenAI互換の別の埋め込みサービスを利用するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## オプション {#options}

すべての[OpenAIの埋め込みオプション](https://platform.openai.com/docs/api-reference/embeddings/create)は`additional_json_options`関数の`EMBED_TEXT()`パラメータを通じてサポートされます。

**例：text-embedding-3-large に別の次元を使用する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
                `content`,
                '{"dimensions": 1024}'
              )) STORED
);
```

利用可能なすべてのオプションについては、 [OpenAIドキュメント](https://platform.openai.com/docs/api-reference/embeddings/create)を参照してください。

## 関連項目 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
