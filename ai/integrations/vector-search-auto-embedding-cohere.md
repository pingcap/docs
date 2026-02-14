---
title: Cohere Embeddings
summary: TiDB Cloudで Cohere 埋め込みモデルを使用する方法を学習します。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-cohere/']
---

# コヒーレ埋め込み {#cohere-embeddings}

このドキュメントでは、TiDB Cloudの[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)で Cohere 埋め込みモデルを使用して、テキスト クエリによるセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)は、AWS でホストされているTiDB Cloud Starter クラスターでのみ使用できます。

## 利用可能なモデル {#available-models}

TiDB Cloud は、以下の[コヒア](https://cohere.com/)埋め込みモデルをネイティブに提供します。API キーは必要ありません。

**Cohere Embed v3 モデル**

-   名前: `tidbcloud_free/cohere/embed-english-v3`
-   寸法: 1024
-   距離計量：コサイン、L2
-   言語: 英語
-   最大入力テキストトークン数: 512 (トークンあたり約 4 文字)
-   最大入力テキスト文字数: 2,048
-   価格: 無料
-   TiDB Cloudがホスト: ✅ `tidbcloud_free/cohere/embed-english-v3`
-   鍵をご持参ください: ✅ `cohere/embed-english-v3.0`

**Cohere Multilingual Embed v3 モデル**

-   名前: `tidbcloud_free/cohere/embed-multilingual-v3`
-   寸法: 1024
-   距離計量：コサイン、L2
-   言語: 100以上の言語
-   最大入力テキストトークン数: 512 (トークンあたり約 4 文字)
-   最大入力テキスト文字数: 2,048
-   価格: 無料
-   TiDB Cloudがホスト: ✅ `tidbcloud_free/cohere/embed-multilingual-v3`
-   鍵をご持参ください: ✅ `cohere/embed-multilingual-v3.0`

または、ご自身のCohere APIキー（BYOK）をお持ちいただければ、 `cohere/`プレフィックスですべてのCohereモデルをご利用いただけます。例：

**Cohere Embed v4 モデル**

-   名前: `cohere/embed-v4.0`
-   寸法: 256、512、1024、1536 (デフォルト)
-   距離計量：コサイン、L2
-   最大入力テキストトークン数: 128,000
-   価格: Cohereによる請求
-   TiDB Cloudがホスト: ❌
-   鍵をご持参ください: ✅

Cohere モデルの完全なリストについては、 [Cohereドキュメント](https://docs.cohere.com/docs/cohere-embed)参照してください。

## SQL の使用例 (TiDB Cloudホスト) {#sql-usage-example-tidb-cloud-hosted}

次の例は、自動埋め込みを備えたTiDB Cloudでホストされている Cohere 埋め込みモデルを使用する方法を示しています。

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
> -   Cohere埋め込みモデルの場合、テーブルを定義する際に関数`EMBED_TEXT()`に`input_type`指定する必要があります。例えば、 `'{"input_type": "search_document", "input_type@search": "search_query"}'`指定すると、データ挿入時に`input_type`が`search_document`に設定され、ベクトル検索時に`search_query`自動的に適用されます。
> -   `@search`サフィックスは、フィールドがベクトル検索クエリ中にのみ有効になることを示します。そのため、クエリを記述するときに`input_type`再度指定する必要はありません。

データの挿入とクエリ:

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

## オプション（TiDB Cloudホスト） {#options-tidb-cloud-hosted}

**Embed v3**モデルと**Multilingual Embed v3**モデルはどちらも次のオプションをサポートしており、 `EMBED_TEXT()`関数の`additional_json_options`パラメータで指定できます。

-   `input_type` （必須）: 埋め込みの目的を示す特別なトークンを先頭に付加します。同じタスクの埋め込みを生成する際は、常に同じ入力タイプを使用する必要があります。そうでない場合、埋め込みは異なる意味空間にマッピングされ、互換性がなくなります。唯一の例外はセマンティック検索で、ドキュメントは`search_document`で、クエリは`search_query`で埋め込まれます。

    -   `search_document` : ドキュメントから埋め込みを生成し、ベクター データベースに保存します。
    -   `search_query` : クエリから埋め込みを生成し、ベクトル データベースに保存されている埋め込みを検索します。
    -   `classification` : テキスト分類器の入力として使用される埋め込みを生成します。
    -   `clustering` : クラスタリングタスクの埋め込みを生成します。

-   `truncate` （オプション）: 最大トークン長を超える入力をAPIがどのように処理するかを制御します。以下のいずれかの値を指定できます。

    -   `NONE` (デフォルト): 入力が最大入力トークン長を超えた場合にエラーを返します。
    -   `START` : 入力が収まるまで先頭からのテキストを破棄します。
    -   `END` : 入力が収まるまで末尾からテキストを破棄します。

## 使用例（BYOK） {#usage-example-byok}

この例では、Bring Your Own Key (BYOK) Cohere モデルを使用してベクター テーブルを作成し、ドキュメントを挿入し、類似性検索を実行する方法を示します。

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

[Cohereダッシュボード](https://dashboard.cohere.com/api-keys)から API キーを作成し、独自のキー (BYOK) を持って埋め込みサービスを使用します。

<SimpleTab groupId="language">
<div label="Python" value="python">

TiDB クライアントを使用して、Cohere 埋め込みプロバイダーの API キーを構成します。

```python
tidb_client.configure_embedding_provider(
    provider="cohere",
    api_key="{your-cohere-api-key}",
)
```

</div>
<div label="SQL" value="sql">

SQL を使用して Cohere 埋め込みプロバイダーの API キーを設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_COHERE_API_KEY = "{your-cohere-api-key}";
```

</div>
</SimpleTab>

### ステップ3: ベクターテーブルを作成する {#step-3-create-a-vector-table}

`cohere/embed-v4.0`モデルを使用して 1536 次元のベクトル (デフォルトの次元) を生成するベクトル フィールドを持つテーブルを作成します。

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

### ステップ4: テーブルにデータを挿入する {#step-4-insert-data-into-the-table}

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

### ステップ5: 類似文書を検索する {#step-5-search-for-similar-documents}

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.search()` API を使用してベクトル検索を実行します。

```python
results = table.search("How to learn Python programming?") \
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
    VEC_EMBED_COSINE_DISTANCE(embedding, "How to learn Python programming?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 2;
```

</div>
</SimpleTab>

## オプション（BYOK） {#options-byok}

[Cohere埋め込みオプション](https://docs.cohere.com/v2/reference/embed)すべて、 `EMBED_TEXT()`関数の`additional_json_options`パラメータを介してサポートされます。

**例: 検索操作と挿入操作に異なる`input_type`を指定する**

フィールドがベクトル検索クエリ中にのみ有効であることを示すには、サフィックス`@search`を使用します。

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

**例: 代替ディメンションを使用する**

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

利用可能なすべてのオプションについては、 [Cohereドキュメント](https://docs.cohere.com/v2/reference/embed)参照してください。

## 参照 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
