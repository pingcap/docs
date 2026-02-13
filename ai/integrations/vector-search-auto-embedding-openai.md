---
title: OpenAI Embeddings
summary: TiDB Cloudで OpenAI 埋め込みモデルを使用する方法を学びます。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-openai/']
---

# OpenAI 埋め込み {#openai-embeddings}

このドキュメントでは、TiDB Cloudの[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)で OpenAI 埋め込みモデルを使用して、テキスト クエリによるセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)は、AWS でホストされているTiDB Cloud Starter クラスターでのみ使用できます。

## 利用可能なモデル {#available-models}

ご自身のOpenAI APIキー（BYOK）をお持ちいただく場合、すべてのOpenAIモデルは`openai/`プレフィックスでご利用いただけます。例：

**テキスト埋め込み 3 小**

-   名前: `openai/text-embedding-3-small`
-   寸法: 512-1536 (デフォルト: 1536)
-   距離計量：コサイン、L2
-   価格: OpenAIによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

**テキスト埋め込み 3 大きい**

-   名前: `openai/text-embedding-3-large`
-   寸法: 256-3072 (デフォルト: 3072)
-   距離計量：コサイン、L2
-   価格: OpenAIによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

利用可能なモデルの完全なリストについては、 [OpenAIドキュメント](https://platform.openai.com/docs/guides/embeddings)参照してください。

## 使用例 {#usage-example}

この例では、OpenAI 埋め込みモデルを使用してベクター テーブルを作成し、ドキュメントを挿入し、類似性検索を実行する方法を示します。

自動埋め込み生成用の AI SDK またはネイティブ SQL関数を使用して、OpenAI Embeddings API を TiDB と統合できます。

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

[OpenAI APIプラットフォーム](https://platform.openai.com/api-keys)で API キーを作成し、埋め込みサービスを使用するには独自のキー (BYOK) を使用します。

<SimpleTab groupId="language">
<div label="Python" value="python">

TiDB クライアントを使用して、OpenAI 埋め込みプロバイダーの API キーを設定します。

```python
tidb_client.configure_embedding_provider(
    provider="openai",
    api_key="{your-openai-api-key}",
)
```

</div>
<div label="SQL" value="sql">

SQL を使用して OpenAI 埋め込みプロバイダーの API キーを設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = "{your-openai-api-key}";
```

</div>
</SimpleTab>

### ステップ3: ベクターテーブルを作成する {#step-3-create-a-vector-table}

`openai/text-embedding-3-small`モデルを使用して 1536 次元のベクトルを生成するベクトル フィールドを持つテーブルを作成します。

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

## Azure OpenAI を使用する {#use-azure-openai}

AzureでOpenAI埋め込みモデルを使用するには、グローバル変数`TIDB_EXP_EMBED_OPENAI_API_BASE` AzureリソースのURLに設定します。例：

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

リソース URL が`https://<your-resource-name>.cognitiveservices.azure.com/`と表示される場合でも、OpenAI 互換のリクエストおよびレスポンス形式を維持するには、API ベースとして`https://<your-resource-name>.openai.azure.com/openai/v1`使用する必要があります。

Azure OpenAI から OpenAI に直接切り替えるには、 `TIDB_EXP_EMBED_OPENAI_API_BASE`空の文字列に設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = '';
```

> **注記：**
>
> -   セキュリティ上の理由から、API ベースは Azure OpenAI URL または OpenAI URL のみに設定できます。任意のベース URL は許可されません。
> -   OpenAI 互換の別の埋め込みサービスを利用する場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## オプション {#options}

[OpenAI埋め込みオプション](https://platform.openai.com/docs/api-reference/embeddings/create)すべて、 `EMBED_TEXT()`関数の`additional_json_options`パラメータを介してサポートされます。

**例: text-embedding-3-large に代替ディメンションを使用する**

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

利用可能なすべてのオプションについては、 [OpenAIドキュメント](https://platform.openai.com/docs/api-reference/embeddings/create)参照してください。

## 参照 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
