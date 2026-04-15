---
title: NVIDIA NIM Embeddings
summary: TiDB CloudでNVIDIA NIM埋め込みモデルを使用する方法を学びましょう。
aliases: ['/ja/tidbcloud/vector-search-auto-embedding-nvidia-nim/']
---

# NVIDIA NIM エンベディング {#nvidia-nim-embeddings}

このドキュメントでは、TiDB CloudでNVIDIA NIM埋め込みモデルを[自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)使用して、テキストクエリによるセマンティック検索を実行する方法について説明します。

> **注記：**
>
> [自動埋め込み](/ai/integrations/vector-search-auto-embedding-overview.md)、AWS でホストされているTiDB Cloud Starterインスタンスでのみ利用できます。

## 利用可能なモデル {#available-models}

NVIDIA NIM 上でホストされている埋め込みモデルは、独自の[NVIDIA NIM APIキー](https://build.nvidia.com/settings/api-keys)(BYOK) をお持ちの場合、 `nvidia_nim/`プレフィックスを使用して使用できます。

便宜上、次のセクションでは人気のあるモデルを例として、自動埋め込みでの使用方法を示します。利用可能なモデルの完全なリストについては、 [NVIDIA NIM テキスト埋め込みモデル](https://build.nvidia.com/models?filters=usecase%3Ausecase_text_to_embedding)を参照してください。

## bge-m3 {#bge-m3}

-   名前: `nvidia_nim/baai/bge-m3`
-   寸法: 1024
-   距離指標：コサイン類似度、L2
-   入力可能なテキストトークンの最大数：8,192
-   価格：NVIDIAが請求
-   TiDB Cloudでホストされています: ❌
-   鍵をご持参ください：✅
-   ドキュメント： [https://docs.api.nvidia.com/nim/reference/baai-bge-m3](https://docs.api.nvidia.com/nim/reference/baai-bge-m3)

例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_NVIDIA_NIM_API_KEY = 'your-nvidia-nim-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "nvidia_nim/baai/bge-m3",
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

結果：

    +------+----------------------------------------------------------------+
    | id   | content                                                        |
    +------+----------------------------------------------------------------+
    |    1 | Java: Object-oriented language for cross-platform development. |
    |    4 | Java's syntax is used in Android apps.                         |
    +------+----------------------------------------------------------------+

## nv-embed-v1 {#nv-embed-v1}

この例では`nvidia/nv-embed-v1`モデルを使用して、ベクトルテーブルを作成し、ドキュメントを挿入し、類似性検索を実行する方法を示します。

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

認証が必要な NVIDIA NIM モデルを使用している場合は、API キーを構成できます。 [NVIDIA開発者プログラム](https://developer.nvidia.com/nim)を通じて NIM API エンドポイントに無料でアクセスすることも、 [NVIDIAビルドプラットフォーム](https://build.nvidia.com/settings/api-keys)プラットフォームから API キーを作成することもできます。

<SimpleTab groupId="language">
<div label="Python" value="python">

TiDBクライアントを使用して、NVIDIA NIMモデルのAPIキーを設定します。

```python
tidb_client.configure_embedding_provider(
    provider="nvidia_nim",
    api_key="{your-nvidia-api-key}",
)
```

</div>
<div label="SQL" value="sql">

SQLを使用してNVIDIA NIMモデルのAPIキーを設定します。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_NVIDIA_NIM_API_KEY = "{your-nvidia-api-key}";
```

</div>
</SimpleTab>

### ステップ3：ベクターテーブルを作成する {#step-3-create-a-vector-table}

NVIDIA NIMモデルを使用して埋め込みを生成するベクトルフィールドを持つテーブルを作成します。

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
        model_name="nvidia/nv-embed-v1"
    ).VectorField(source_field="content")

table = tidb_client.create_table(schema=Document, if_exists="overwrite")
```

</div>
<div label="SQL" value="sql">

```sql
CREATE TABLE sample_documents (
    `id`        INT PRIMARY KEY,
    `content`   TEXT,
    `embedding` VECTOR(4096) GENERATED ALWAYS AS (EMBED_TEXT(
        "nvidia/nv-embed-v1",
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
    Document(id=1, content="Machine learning algorithms can identify patterns in data."),
    Document(id=2, content="Deep learning uses neural networks with multiple layers."),
    Document(id=3, content="Natural language processing helps computers understand text."),
    Document(id=4, content="Computer vision enables machines to interpret images."),
    Document(id=5, content="Reinforcement learning learns through trial and error."),
]
table.bulk_insert(documents)
```

</div>
<div label="SQL" value="sql">

`INSERT INTO`ステートメントを使用してデータを挿入します。

```sql
INSERT INTO sample_documents (id, content)
VALUES
    (1, "Machine learning algorithms can identify patterns in data."),
    (2, "Deep learning uses neural networks with multiple layers."),
    (3, "Natural language processing helps computers understand text."),
    (4, "Computer vision enables machines to interpret images."),
    (5, "Reinforcement learning learns through trial and error.");
```

</div>
</SimpleTab>

### ステップ5：類似文書を検索する {#step-5-search-for-similar-documents}

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.search()` APIを使用してベクトル検索を実行します。

```python
results = table.search("How do neural networks work?") \
    .limit(3) \
    .to_list()

for doc in results:
    print(f"ID: {doc.id}, Content: {doc.content}")
```

</div>
<div label="SQL" value="sql">

`VEC_EMBED_COSINE_DISTANCE`関数を使用して、コサイン距離によるベクトル検索を実行します。

```sql
SELECT
    `id`,
    `content`,
    VEC_EMBED_COSINE_DISTANCE(embedding, "How do neural networks work?") AS _distance
FROM sample_documents
ORDER BY _distance ASC
LIMIT 3;
```

</div>
</SimpleTab>

## 関連項目 {#see-also}

-   [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md)
-   [ベクトル検索](/ai/concepts/vector-search-overview.md)
-   [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)
-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)
