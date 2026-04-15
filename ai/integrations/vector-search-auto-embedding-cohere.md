---
title: Cohere Embeddings
summary: TiDB CloudでCohere埋め込みモデルを使用する方法を学びましょう。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-cohere/']
---

# Cohere埋め込み {#cohere-embeddings}

このドキュメントでは、 TiDB Cloudで Cohere 埋め込みモデルを[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)で使用する方法、テキストクエリによるセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)、AWS でホストされているTiDB Cloud Starterインスタンスでのみ利用できます。

## 利用可能なモデル {#available-models}

TiDB Cloud は、次の[調和する](https://cohere.com/)埋め込みモデルをネイティブに提供します。 API キーは必要ありません。

**Cohere Embed v3 モデル**

-   名前: `tidbcloud_free/cohere/embed-english-v3`
-   寸法: 1024
-   距離指標：コサイン類似度、L2
-   言語：英語
-   入力可能なテキストトークンの最大数：512個（1トークンあたり約4文字）
-   入力可能なテキスト文字数：最大2,048文字
-   価格：無料
-   TiDB Cloudがホストしています: ✅ `tidbcloud_free/cohere/embed-english-v3`
-   鍵をご持参ください：✅ `cohere/embed-english-v3.0`

**Cohere Multilingual Embed v3 モデル**

-   名前: `tidbcloud_free/cohere/embed-multilingual-v3`
-   寸法: 1024
-   距離指標：コサイン類似度、L2
-   対応言語：100以上の言語
-   入力可能なテキストトークンの最大数：512個（1トークンあたり約4文字）
-   入力可能なテキスト文字数：最大2,048文字
-   価格：無料
-   TiDB Cloudがホストしています: ✅ `tidbcloud_free/cohere/embed-multilingual-v3`
-   鍵をご持参ください：✅ `cohere/embed-multilingual-v3.0`

あるいは、独自のCohere APIキー（BYOK）をお持ちの場合は`cohere/`プレフィックスを使用してすべてのCohereモデルをご利用いただけます。例：

**Cohere Embed v4 モデル**

-   名前: `cohere/embed-v4.0`
-   寸法：256、512、1024、1536（デフォルト）
-   距離指標：コサイン類似度、L2
-   入力可能なテキストトークンの最大数：128,000
-   価格：Cohereが請求
-   TiDB Cloudでホストされています: ❌
-   鍵をご持参ください：✅

Cohere モデルの完全なリストについては、 [Cohereのドキュメント](https://docs.cohere.com/docs/cohere-embed)を参照してください。

## SQLの使用例（TiDB Cloudホスト型） {#sql-usage-example-tidb-cloud-hosted}

以下の例は、TiDB CloudでホストされているCohere埋め込みモデルを自動埋め込み機能で使用する方法を示しています。

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/cohere/embed-multilingual-v3",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

> **注記：**
>
> -   Cohere埋め込みモデルの場合、テーブルを定義する際に、{{ `input_type` `EMBED_TEXT()` }を指定する必要があります。例えば、 `'{"input_type": "search_document", "input_type@search": "search_query"}'`は、データ挿入時に`input_type`が`search_document`に設定され、ベクトル検索時に`search_query`が自動的に適用されることを意味します。
> -   `@search`サフィックスは、そのフィールドがベクトル検索クエリの実行時のみ有効であることを示しています。そのため、クエリを作成する際に`input_type`を再度指定する必要はありません。

データ挿入とデータ照会：

```sql
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

結果：

    +------+----------------------------------------------------------------+
    | id   | content                                                        |
    +------+----------------------------------------------------------------+
    |    1 | Java: Object-oriented language for cross-platform development. |
    |    4 | Java's syntax is used in Android apps.                         |
    +------+----------------------------------------------------------------+

## オプション（TiDB Cloudホスティング） {#options-tidb-cloud-hosted}

**Embed v3**モデルと**Multilingual Embed v3**モデルの両方で、以下のオプションがサポートされています。これらのオプションは、 `additional_json_options`関数の`EMBED_TEXT()`パラメータを介して指定できます。

-   `input_type` (必須): 埋め込みの目的を示す特別なトークンを先頭に追加します。同じタスクの埋め込みを生成する場合は、常に同じ入力タイプを使用する必要があります。そうしないと、埋め込みが異なる意味空間にマッピングされ、互換性がなくなります。唯一の例外はセマンティック検索で、ドキュメントは`search_document`で埋め込まれ、クエリは`search_query`で埋め込まれます。

    -   `search_document` : ドキュメントから埋め込みを生成し、ベクトルデータベースに保存します。
    -   `search_query` : クエリから埋め込みを生成し、ベクトルデータベースに保存されている埋め込みに対して検索を行います。
    -   `classification` : テキスト分類器への入力として使用される埋め込みを生成します。
    -   `clustering` : クラスタリングタスク用の埋め込みを生成します。

-   `truncate` （オプション）：APIが最大トークン長を超える入力をどのように処理するかを制御します。以下のいずれかの値を指定できます。

    -   `NONE` (デフォルト): 入力が最大入力トークン長を超えた場合にエラーを返します。
    -   `START` : 入力が収まるまで、先頭からテキストを破棄します。
    -   `END` : 入力が収まるまで末尾からテキストを破棄します。

## 使用例（BYOK） {#usage-example-byok}

この例では、Bring Your Own Key (BYOK) Cohere モデルを使用して、ベクター テーブルを作成し、ドキュメントを挿入し、類似性検索を実行する方法を示します。

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

[Cohereダッシュボード](https://dashboard.cohere.com/api-keys)からAPIキーを作成し、独自のキー(BYOK)を使用して埋め込みサービスを使用します。

<SimpleTab groupId="language">
<div label="Python" value="python">

TiDBクライアントを使用して、Cohere埋め込みプロバイダのAPIキーを設定します。

```python
tidb_client.configure_embedding_provider(
    provider="cohere",
    api_key="{your-cohere-api-key}",
)
```

</div>
<div label="SQL" value="sql">

SQLを使用して、Cohere埋め込みプロバイダのAPIキーを設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_COHERE_API_KEY = "{your-cohere-api-key}";
```

</div>
</SimpleTab>

### ステップ3：ベクターテーブルを作成する {#step-3-create-a-vector-table}

`cohere/embed-v4.0`モデルを使用して 1536 次元ベクトル (デフォルトの次元) を生成するベクトルフィールドを持つテーブルを作成します。

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
        model_name="cohere/embed-v4.0"
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
        "cohere/embed-v4.0",
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
    Document(id=1, content="Python: High-level programming language for data science and web development."),
    Document(id=2, content="Python snake: Non-venomous constrictor found in tropical regions."),
    Document(id=3, content="Python framework: Django and Flask are popular web frameworks."),
    Document(id=4, content="Python libraries: NumPy and Pandas for data analysis."),
    Document(id=5, content="Python ecosystem: Rich collection of packages and tools."),
]
table.bulk_insert(documents)
```

</div>
<div label="SQL" value="sql">

`INSERT INTO`ステートメントを使用してデータを挿入します。

```sql
INSERT INTO sample_documents (id, content)
VALUES
    (1, "Python: High-level programming language for data science and web development."),
    (2, "Python snake: Non-venomous constrictor found in tropical regions."),
    (3, "Python framework: Django and Flask are popular web frameworks."),
    (4, "Python libraries: NumPy and Pandas for data analysis."),
    (5, "Python ecosystem: Rich collection of packages and tools.");
```

</div>
</SimpleTab>

### ステップ5：類似文書を検索する {#step-5-search-for-similar-documents}

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.search()` APIを使用してベクトル検索を実行します。

```python
results = table.search("How to learn Python programming?") \
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
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to learn Python programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

</div>
</SimpleTab>

## オプション（BYOK） {#options-byok}

[Cohereの埋め込みオプション](https://docs.cohere.com/v2/reference/embed)は`additional_json_options`関数の`EMBED_TEXT()`パラメータを介してサポートされます。

**例：検索操作と挿入操作で異なる`input_type`を指定する**

`@search`という接尾辞を使用して、そのフィールドがベクトル検索クエリ実行時のみ有効であることを示します。

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

**例：別の次元を使用する**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(512) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"output_dimension": 512}'
              )) STORED
);
```

利用可能なすべてのオプションについては、 [Cohereのドキュメント](https://docs.cohere.com/v2/reference/embed)を参照してください。

## 関連項目 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
